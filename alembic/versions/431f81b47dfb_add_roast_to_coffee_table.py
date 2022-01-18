"""Add roast to coffee table

Revision ID: 431f81b47dfb
Revises: 012e9b3663af
Create Date: 2022-01-16 14:35:13.297139

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.expression import insert, delete


# revision identifiers, used by Alembic.
revision = '431f81b47dfb'
down_revision = '012e9b3663af'
branch_labels = None
depends_on = None

roastValues = (
    ('filter', 'Filter roast', 'Filter röstung'),
    ('espresso', 'Espresso roast', 'Espresso röstung'),
    ('omni', 'Omni roast', 'Omni röstung')
)

def upgrade():
    # for table coffee, add column cupping points, roast profile (filter, espresso, omni, unspecified)

    roast_table = op.create_table(
        'roast',
        sa.Column('name', sa.VARCHAR(64), nullable=False),
        sa.PrimaryKeyConstraint('name', name='pk_roast')
    )
    roast_translation_table = op.create_table(
        'roast_translation',
        sa.Column('roast_name', sa.VARCHAR(64), nullable=False),
        sa.Column('language', sa.CHAR(2), nullable=False),
        sa.Column('value', sa.VARCHAR(128), nullable=False),
        sa.PrimaryKeyConstraint('roast_name', 'language', name='pk_roast_translation'),
        sa.ForeignKeyConstraint(['roast_name'], ['roast.name'], name='fk_roast_translation_roast'),
        sa.ForeignKeyConstraint(['language'], ['language.code'], name='fk_roast_translation_lang')
    )
    for r in roastValues:
        insert(roast_table).values(name=r[0])
        insert(roast_translation_table).values(roast=r[0], language='EN', value=r[1])
        insert(roast_translation_table).values(roast=r[0], language='DE', value=r[2])

    op.add_column('coffee', sa.Column('score', sa.INTEGER))
    op.add_column('coffee', sa.Column('roast_name', sa.VARCHAR(64)))
    op.create_foreign_key('fk_coffee_roast', 'coffee', 'roast', ['roast_name'], ['name'])
    

def downgrade():
    op.drop_constraint('fk_coffee_roast', 'coffee', type_='foreignkey')
    op.drop_column('coffee', 'roast_name')
    op.drop_column('coffee', 'score')
    op.drop_table('roast_translation')
    op.drop_table('roast')

