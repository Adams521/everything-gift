#!/bin/bash

# 导入 PostgreSQL 数据库数据
# 从 SQL 备份文件恢复数据库

set -e

echo "=========================================="
echo "导入 PostgreSQL 数据库数据"
echo "=========================================="

# 检查参数
if [ $# -eq 0 ]; then
    echo ""
    echo "用法: $0 <备份文件>"
    echo ""
    echo "示例:"
    echo "  $0 database-backups/giftdb-backup-20241207-120000.tar.gz"
    echo "  $0 database-backups/giftdb-backup-20241207-120000.sql"
    echo ""
    exit 1
fi

BACKUP_FILE="$1"

# 检查文件是否存在
if [ ! -f "$BACKUP_FILE" ]; then
    echo "✗ 备份文件不存在: $BACKUP_FILE"
    exit 1
fi

echo ""
echo "备份文件: $BACKUP_FILE"
FILE_SIZE=$(du -h "$BACKUP_FILE" | cut -f1)
echo "文件大小: $FILE_SIZE"

# 解压（如果是 tar.gz）
TEMP_DIR=$(mktemp -d)
SQL_FILE=""

if [[ "$BACKUP_FILE" == *.tar.gz ]]; then
    echo ""
    echo "1. 解压备份文件..."
    tar xzf "$BACKUP_FILE" -C "$TEMP_DIR"
    SQL_FILE=$(find "$TEMP_DIR" -name "*.sql" | head -1)
    if [ -z "$SQL_FILE" ]; then
        echo "   ✗ 未找到 SQL 文件"
        rm -rf "$TEMP_DIR"
        exit 1
    fi
    echo "   ✓ 解压完成: $(basename "$SQL_FILE")"
elif [[ "$BACKUP_FILE" == *.sql ]]; then
    SQL_FILE="$BACKUP_FILE"
else
    echo "   ✗ 不支持的备份文件格式（需要 .sql 或 .tar.gz）"
    exit 1
fi

# 检查 PostgreSQL 容器
echo ""
echo "2. 检查 PostgreSQL 容器..."
if ! docker ps | grep -q "gift-postgres"; then
    echo "   ⚠️  PostgreSQL 容器未运行，正在启动..."
    docker compose up -d postgres
    echo "   等待容器启动..."
    sleep 5
fi

# 等待数据库就绪
echo ""
echo "3. 等待数据库就绪..."
MAX_RETRIES=30
RETRY_COUNT=0

while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
    if docker exec gift-postgres pg_isready -U user -d giftdb > /dev/null 2>&1; then
        echo "   ✓ 数据库已就绪"
        break
    fi
    RETRY_COUNT=$((RETRY_COUNT + 1))
    echo "   等待中... ($RETRY_COUNT/$MAX_RETRIES)"
    sleep 2
done

if [ $RETRY_COUNT -eq $MAX_RETRIES ]; then
    echo "   ✗ 数据库启动超时"
    rm -rf "$TEMP_DIR"
    exit 1
fi

# 确认操作
echo ""
echo "⚠️  警告：导入数据将覆盖现有数据库内容！"
read -p "是否继续？(yes/no) " -r
if [[ ! $REPLY =~ ^[Yy][Ee][Ss]$ ]]; then
    echo "已取消"
    rm -rf "$TEMP_DIR"
    exit 0
fi

# 备份现有数据库（如果存在数据）
echo ""
echo "4. 备份现有数据库（如果存在）..."
EXISTING_TABLES=$(docker exec gift-postgres psql -U user -d giftdb -t -c "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public';" 2>/dev/null | tr -d ' ' || echo "0")

if [ "$EXISTING_TABLES" -gt 0 ]; then
    BACKUP_DIR="./database-backups"
    mkdir -p "${BACKUP_DIR}"
    EXISTING_BACKUP="${BACKUP_DIR}/existing-backup-$(date +%Y%m%d-%H%M%S).sql"
    echo "   发现现有数据，创建备份: $(basename "$EXISTING_BACKUP")"
    docker exec gift-postgres pg_dump -U user -d giftdb > "$EXISTING_BACKUP" 2>/dev/null || echo "   备份失败（继续导入）"
fi

# 清空现有数据库（可选）
echo ""
echo "5. 准备导入数据..."
read -p "是否清空现有数据库？(yes/no，默认: yes) " -r
if [[ $REPLY =~ ^[Yy][Ee][Ss]$ ]] || [ -z "$REPLY" ]; then
    echo "   清空现有数据库..."
    docker exec gift-postgres psql -U user -d giftdb -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;" 2>/dev/null || echo "   清空失败（继续导入）"
fi

# 导入数据
echo ""
echo "6. 导入数据..."
echo "   这可能需要一些时间..."

docker exec -i gift-postgres psql -U user -d giftdb < "$SQL_FILE"

if [ $? -eq 0 ]; then
    echo "   ✓ 导入成功"
else
    echo "   ✗ 导入失败"
    rm -rf "$TEMP_DIR"
    exit 1
fi

# 清理临时文件
rm -rf "$TEMP_DIR"

# 验证导入
echo ""
echo "7. 验证导入结果..."
TABLE_COUNT=$(docker exec gift-postgres psql -U user -d giftdb -t -c "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public';" 2>/dev/null | tr -d ' ' || echo "0")
echo "   表数量: $TABLE_COUNT"

if [ "$TABLE_COUNT" -gt 0 ]; then
    echo ""
    echo "   各表数据量："
    docker exec gift-postgres psql -U user -d giftdb -c "
        SELECT 
            tablename AS table_name,
            (SELECT COUNT(*) FROM information_schema.columns WHERE table_name = t.tablename) AS column_count
        FROM pg_tables t
        WHERE schemaname = 'public'
        ORDER BY tablename;
    " 2>/dev/null | grep -v "rows)" | sed 's/^/   /' || echo "   无法获取表信息"
fi

echo ""
echo "=========================================="
echo "✅ 导入完成！"
echo "=========================================="
echo ""
echo "下一步："
echo "1. 验证数据: docker exec gift-postgres psql -U user -d giftdb -c '\\dt'"
echo "2. 重启后端服务: docker compose restart backend"
echo ""

