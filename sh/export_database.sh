#!/bin/bash

# 导出 PostgreSQL 数据库数据
# 用于将数据库内容导出为 SQL 文件，可以在其他机器上导入

set -e

echo "=========================================="
echo "导出 PostgreSQL 数据库数据"
echo "=========================================="

# 配置
BACKUP_DIR="./database-backups"
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
BACKUP_FILE="${BACKUP_DIR}/giftdb-backup-${TIMESTAMP}.sql"
BACKUP_TAR="${BACKUP_DIR}/giftdb-backup-${TIMESTAMP}.tar.gz"

# 创建备份目录
mkdir -p "${BACKUP_DIR}"

# 检查 PostgreSQL 容器是否运行
echo ""
echo "1. 检查 PostgreSQL 容器..."
if ! docker ps | grep -q "gift-postgres"; then
    echo "   ⚠️  PostgreSQL 容器未运行，正在启动..."
    docker compose up -d postgres
    echo "   等待容器启动..."
    sleep 5
fi

# 等待数据库就绪
echo ""
echo "2. 等待数据库就绪..."
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
    exit 1
fi

# 导出数据库
echo ""
echo "3. 导出数据库..."
echo "   目标文件: ${BACKUP_FILE}"

docker exec gift-postgres pg_dump -U user -d giftdb > "${BACKUP_FILE}"

if [ $? -eq 0 ] && [ -f "${BACKUP_FILE}" ]; then
    FILE_SIZE=$(du -h "${BACKUP_FILE}" | cut -f1)
    echo "   ✓ 导出成功，文件大小: $FILE_SIZE"
else
    echo "   ✗ 导出失败"
    exit 1
fi

# 压缩备份文件
echo ""
echo "4. 压缩备份文件..."
tar czf "${BACKUP_TAR}" -C "${BACKUP_DIR}" "$(basename "${BACKUP_FILE}")"
rm "${BACKUP_FILE}"

TAR_SIZE=$(du -h "${BACKUP_TAR}" | cut -f1)
echo "   ✓ 压缩完成，文件大小: $TAR_SIZE"

# 显示数据库统计信息
echo ""
echo "5. 数据库统计信息："
TABLE_COUNT=$(docker exec gift-postgres psql -U user -d giftdb -t -c "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public';" 2>/dev/null | tr -d ' ' || echo "0")
echo "   表数量: $TABLE_COUNT"

if [ "$TABLE_COUNT" -gt 0 ]; then
    echo ""
    echo "   各表数据量："
    docker exec gift-postgres psql -U user -d giftdb -c "
        SELECT 
            schemaname || '.' || tablename AS table_name,
            pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
        FROM pg_tables
        WHERE schemaname = 'public'
        ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
    " 2>/dev/null | grep -v "rows)" | sed 's/^/   /' || echo "   无法获取表信息"
fi

echo ""
echo "=========================================="
echo "✅ 导出完成！"
echo "=========================================="
echo ""
echo "备份文件位置:"
echo "  ${BACKUP_TAR}"
echo ""
echo "使用方法："
echo "1. 将备份文件传输到目标机器"
echo "2. 在目标机器上运行: bash sh/导入数据库数据.sh ${BACKUP_TAR}"
echo ""

