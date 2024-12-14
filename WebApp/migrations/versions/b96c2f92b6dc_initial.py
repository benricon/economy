"""initial

Revision ID: b96c2f92b6dc
Revises: 
Create Date: 2024-12-13 22:39:14.342594

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b96c2f92b6dc'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('categories',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('level', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('parent', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['parent'], ['categories.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('transaction',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.Column('account', sa.String(length=50), nullable=False),
    sa.Column('description', sa.String(length=255), nullable=False),
    sa.Column('amount', sa.Numeric(precision=10, scale=2), nullable=False),
    sa.Column('is_categorized', sa.Boolean(), nullable=True),
    sa.Column('category_level_1', sa.Integer(), nullable=True),
    sa.Column('category_level_2', sa.Integer(), nullable=True),
    sa.Column('category_level_3', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['category_level_1'], ['categories.id'], ),
    sa.ForeignKeyConstraint(['category_level_2'], ['categories.id'], ),
    sa.ForeignKeyConstraint(['category_level_3'], ['categories.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('subtransaction',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.Column('account', sa.String(length=50), nullable=False),
    sa.Column('description', sa.String(length=255), nullable=False),
    sa.Column('amount', sa.Numeric(precision=10, scale=2), nullable=False),
    sa.Column('is_categorized', sa.Boolean(), nullable=True),
    sa.Column('parent_transaction_id', sa.Integer(), nullable=False),
    sa.Column('category_level_1', sa.Integer(), nullable=True),
    sa.Column('category_level_2', sa.Integer(), nullable=True),
    sa.Column('category_level_3', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['category_level_1'], ['categories.id'], ),
    sa.ForeignKeyConstraint(['category_level_2'], ['categories.id'], ),
    sa.ForeignKeyConstraint(['category_level_3'], ['categories.id'], ),
    sa.ForeignKeyConstraint(['parent_transaction_id'], ['transaction.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('subtransaction')
    op.drop_table('transaction')
    op.drop_table('categories')
    # ### end Alembic commands ###