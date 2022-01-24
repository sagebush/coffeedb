"""Add roast values

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
    meta = sa.MetaData(bind=op.get_bind())
    meta.reflect()

    roast_table = sa.Table('roast', meta)
    roast_translation_table = sa.Table('roast_translation', meta)
    for r in roastValues:
        op.execute(insert(roast_table).values(name=r[0]))
        op.execute(insert(roast_translation_table).values(roast_name=r[0], language_code='en', value=r[1]))
        op.execute(insert(roast_translation_table).values(roast_name=r[0], language_code='de', value=r[2]))


def downgrade():
    meta = sa.MetaData(bind=op.get_bind())
    meta.reflect()

    roast_table = sa.Table('roast', meta)
    roast_translation_table = sa.Table('roast_translation', meta)
    for r in roastValues:
        op.execute(delete(roast_translation_table).where(roast_name=r[0]))
        op.execute(delete(roast_table).where(name=r[0]))

