"""empty message

Revision ID: 722e9773617a
Revises: 9dd18762d796
Create Date: 2019-09-22 02:17:48.858007

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '722e9773617a'
down_revision = '9dd18762d796'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('comment',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('comment', sa.Text(), nullable=False),
    sa.Column('author', sa.String(length=50), nullable=True),
    sa.Column('comment_time', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('comment')
    # ### end Alembic commands ###
