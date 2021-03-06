"""empty message

Revision ID: 0547c288f0c6
Revises: 8efa3922727e
Create Date: 2017-08-18 10:24:52.283355

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0547c288f0c6'
down_revision = '8efa3922727e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('roles', sa.Column('default', sa.Boolean(), nullable=True))
    op.add_column('roles', sa.Column('permissions', sa.Integer(), nullable=True))
    op.create_index(op.f('ix_roles_default'), 'roles', ['default'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_roles_default'), table_name='roles')
    op.drop_column('roles', 'permissions')
    op.drop_column('roles', 'default')
    # ### end Alembic commands ###
