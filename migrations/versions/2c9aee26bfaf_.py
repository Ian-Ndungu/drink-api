"""empty message

Revision ID: 2c9aee26bfaf
Revises: 
Create Date: 2024-09-03 13:56:49.361830

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2c9aee26bfaf'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('order', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.Integer(), nullable=True))
        # Added a name for the foreign key constraint
        batch_op.create_foreign_key('fk_order_user_id', 'users', ['user_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('order', schema=None) as batch_op:
        # Use the same name as above to drop the foreign key
        batch_op.drop_constraint('fk_order_user_id', type_='foreignkey')
        batch_op.drop_column('user_id')

    # ### end Alembic commands ###
