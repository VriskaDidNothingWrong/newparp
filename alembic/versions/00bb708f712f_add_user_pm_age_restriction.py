"""Add User.pm_age_restriction.

Revision ID: 00bb708f712f
Revises: 21c8e613be53
Create Date: 2017-06-10 23:41:43.466608

"""

# revision identifiers, used by Alembic.
revision = '00bb708f712f'
down_revision = '21c8e613be53'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('pm_age_restriction', sa.Boolean(), nullable=False, server_default='false'))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'pm_age_restriction')
    ### end Alembic commands ###
