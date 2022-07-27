"""init

Revision ID: f32bad96e7a2
Revises: 
Create Date: 2022-07-27 21:23:31.257326

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f32bad96e7a2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('chains',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('rpc', sa.String(), nullable=False),
    sa.Column('token_contract_address', sa.String(), nullable=False),
    sa.Column('last_checked_block', sa.Integer(), server_default='0', nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('named_addresses',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('address', sa.String(), nullable=True),
    sa.Column('name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('transactions',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('hash', sa.String(), nullable=True),
    sa.Column('chain_id', sa.Integer(), nullable=True),
    sa.Column('from_address', sa.String(), nullable=False),
    sa.Column('to_address', sa.String(), nullable=False),
    sa.Column('value', sa.Numeric(precision=20, scale=10), nullable=False),
    sa.ForeignKeyConstraint(['chain_id'], ['chains.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('transactions')
    op.drop_table('named_addresses')
    op.drop_table('chains')
    # ### end Alembic commands ###