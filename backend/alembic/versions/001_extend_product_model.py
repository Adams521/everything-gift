"""扩展Product模型添加商品详细属性字段

Revision ID: 001_extend_product
Revises: 
Create Date: 2024-01-01 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001_extend_product'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # 添加价格相关字段
    op.add_column('products', sa.Column('original_price', sa.Float(), nullable=True))
    op.add_column('products', sa.Column('discount_price', sa.Float(), nullable=True))
    
    # 添加图片和视频字段
    op.add_column('products', sa.Column('image_urls', postgresql.JSON(astext_type=sa.Text()), nullable=True))
    op.add_column('products', sa.Column('video_url', sa.String(), nullable=True))
    
    # 添加平台商品ID
    op.add_column('products', sa.Column('platform_product_id', sa.String(), nullable=True))
    op.create_index(op.f('ix_products_platform_product_id'), 'products', ['platform_product_id'], unique=False)
    
    # 添加销量相关字段
    op.add_column('products', sa.Column('sales_count', sa.Integer(), nullable=True))
    op.add_column('products', sa.Column('sales_amount', sa.Float(), nullable=True))
    
    # 添加评价相关字段
    op.add_column('products', sa.Column('review_count', sa.Integer(), nullable=True))
    op.add_column('products', sa.Column('good_review_count', sa.Integer(), nullable=True))
    op.add_column('products', sa.Column('bad_review_count', sa.Integer(), nullable=True))
    op.add_column('products', sa.Column('good_review_rate', sa.Float(), nullable=True))
    op.add_column('products', sa.Column('average_rating', sa.Float(), nullable=True))
    
    # 添加店铺信息字段
    op.add_column('products', sa.Column('shop_name', sa.String(), nullable=True))
    op.add_column('products', sa.Column('shop_url', sa.String(), nullable=True))
    
    # 添加商品规格参数字段
    op.add_column('products', sa.Column('specifications', postgresql.JSON(astext_type=sa.Text()), nullable=True))
    
    # 添加数据来源和更新时间字段
    op.add_column('products', sa.Column('data_source', sa.String(), nullable=True))
    op.add_column('products', sa.Column('last_updated', sa.DateTime(timezone=True), nullable=True))


def downgrade():
    # 删除新增的字段
    op.drop_column('products', 'last_updated')
    op.drop_column('products', 'data_source')
    op.drop_column('products', 'specifications')
    op.drop_column('products', 'shop_url')
    op.drop_column('products', 'shop_name')
    op.drop_column('products', 'average_rating')
    op.drop_column('products', 'good_review_rate')
    op.drop_column('products', 'bad_review_count')
    op.drop_column('products', 'good_review_count')
    op.drop_column('products', 'review_count')
    op.drop_column('products', 'sales_amount')
    op.drop_column('products', 'sales_count')
    op.drop_index(op.f('ix_products_platform_product_id'), table_name='products')
    op.drop_column('products', 'platform_product_id')
    op.drop_column('products', 'video_url')
    op.drop_column('products', 'image_urls')
    op.drop_column('products', 'discount_price')
    op.drop_column('products', 'original_price')
