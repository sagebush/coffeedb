"""Add tables for new coffees

Revision ID: 8bd1a5cbd0a8
Revises: 431f81b47dfb
Create Date: 2022-01-16 14:57:04.973083

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import func


# revision identifiers, used by Alembic.
revision = '8bd1a5cbd0a8'
down_revision = '431f81b47dfb'
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'incoming_coffee',
        sa.Column('id', sa.INTEGER, autoincrement=True),
        sa.Column('url', sa.VARCHAR(512), nullable=False),
        sa.Column('language', sa.CHAR(2), nullable=False),
        sa.Column('date', sa.DATETIME, server_default=func.now()),
        sa.Column('name', sa.VARCHAR(128), nullable=False),
        sa.Column('roaster', sa.VARCHAR(128), nullable=False),
        sa.Column('roast', sa.VARCHAR(128)),
        sa.Column('score', sa.INTEGER),
        sa.PrimaryKeyConstraint('id', name='pk_incoming_coffee'),
        sa.UniqueConstraint('url', name='uk_incoming_coffee_url')
    )
    op.create_table(
        'incoming_green',
        sa.Column('id', sa.INTEGER, autoincrement=True),
        sa.Column('incoming_coffee_id', sa.INTEGER, nullable=False),
        sa.Column('blend_percentage', sa.INTEGER, default=100),
        sa.Column('country', sa.VARCHAR(128), nullable=False),
        sa.Column('region', sa.VARCHAR(128)),
        sa.Column('washing_station', sa.VARCHAR(128)),
        sa.Column('farm', sa.VARCHAR(128)),
        sa.Column('producer', sa.VARCHAR(128)),
        sa.Column('elevation_min', sa.INTEGER),
        sa.Column('elevation_max', sa.INTEGER),
        sa.Column('processing', sa.VARCHAR(128)),
        sa.PrimaryKeyConstraint('id', name='pk_incoming_green'),
        sa.ForeignKeyConstraint(['incoming_coffee_id'], ['incoming_coffee.id'], name='fk_incoming_green_coffee')
    )
    op.create_table(
        'incoming_green_varieties',
        sa.Column('incoming_green_id', sa.INTEGER, nullable=False),
        sa.Column('variety', sa.VARCHAR(128)),
        sa.PrimaryKeyConstraint('incoming_green_id', name='pk_incoming_green_varieties'),
        sa.ForeignKeyConstraint(['incoming_green_id'], ['incoming_green.id'], name='fk_incoming_green_varieties_green')
    )
    op.create_table(
        'incoming_coffee_flavours',
        sa.Column('coffee_id', sa.INTEGER, nullable=False),
        sa.Column('flavour', sa.VARCHAR(128), nullable=False),
        sa.PrimaryKeyConstraint('coffee_id', 'flavour', name='pk_incoming_coffee_flavours'),
        sa.ForeignKeyConstraint(['coffee_id'], ['incoming_coffee.id'], name='fk_incoming_coffee_flavours_flavour')
    )


def downgrade():
    op.drop_table('incoming_coffee_flavours')
    op.drop_table('incoming_green_varieties')
    op.drop_table('incoming_green')
    op.drop_table('incoming_coffee')
