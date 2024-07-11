"""empty message

Revision ID: 1f24c123afa8
Revises: 4d1bc30c9500
Create Date: 2024-07-11 14:39:29.817871

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '1f24c123afa8'
down_revision: Union[str, None] = '4d1bc30c9500'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('media_block',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('block_id', sa.Integer(), nullable=False),
    sa.Column('photo_id', sa.Text(), nullable=True),
    sa.Column('video_id', sa.Text(), nullable=True),
    sa.Column('callback_button_id', sa.Text(), nullable=True),
    sa.Column('updated', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('media_task',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('task_id', sa.Integer(), nullable=False),
    sa.Column('photo_id', sa.Text(), nullable=False),
    sa.Column('updated', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('media_video')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('media_video',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('block_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('photo_id', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('video_id', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('callback_button_id', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('updated', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='media_video_pkey')
    )
    op.drop_table('media_task')
    op.drop_table('media_block')
    # ### end Alembic commands ###
