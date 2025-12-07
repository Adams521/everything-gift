"""Add product attributes

Revision ID: 20251207144318
Revises: 5d2b92505504
Create Date: 2025-12-07 14:43:18

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = '20251207144318'
down_revision = '5d2b92505504'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 添加商品属性字段
    op.add_column('products', sa.Column('brand', sa.String(), nullable=True))
    op.add_column('products', sa.Column('material', sa.String(), nullable=True))
    op.add_column('products', sa.Column('suitable_scenes', postgresql.JSON(astext_type=sa.Text()), nullable=True))
    op.add_column('products', sa.Column('tags', postgresql.JSON(astext_type=sa.Text()), nullable=True))
    op.add_column('products', sa.Column('suitable_gender', sa.String(), nullable=True))
    op.add_column('products', sa.Column('suitable_age_range', sa.String(), nullable=True))
    op.add_column('products', sa.Column('style', sa.String(), nullable=True))
    op.add_column('products', sa.Column('rating', sa.Float(), nullable=True))
    op.add_column('products', sa.Column('sales_count', sa.Integer(), nullable=True))
    op.add_column('products', sa.Column('stock_status', sa.String(), nullable=True))
    
    # 创建索引
    op.create_index(op.f('ix_products_brand'), 'products', ['brand'], unique=False)
    op.create_index(op.f('ix_products_style'), 'products', ['style'], unique=False)


def downgrade() -> None:
    # 删除索引
    op.drop_index(op.f('ix_products_style'), table_name='products')
    op.drop_index(op.f('ix_products_brand'), table_name='products')
    
    # 删除字段
    op.drop_column('products', 'stock_status')
    op.drop_column('products', 'sales_count')
    op.drop_column('products', 'rating')
    op.drop_column('products', 'style')
    op.drop_column('products', 'suitable_age_range')
    op.drop_column('products', 'suitable_gender')
    op.drop_column('products', 'tags')
    op.drop_column('products', 'suitable_scenes')
    op.drop_column('products', 'material')
    op.drop_column('products', 'brand')

