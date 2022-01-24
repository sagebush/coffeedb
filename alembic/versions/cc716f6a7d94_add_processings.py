"""Add processings

Revision ID: cc716f6a7d94
Revises: 8bd1a5cbd0a8
Create Date: 2022-01-18 20:51:13.907396

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.expression import insert, delete


# revision identifiers, used by Alembic.
revision = 'cc716f6a7d94'
down_revision = '8bd1a5cbd0a8'
branch_labels = None
depends_on = None

processings = (
    ('washed', '', 'washed', 'gewaschen'),
    ('natural', '', 'natural', 'natural'),
    ('honey', '', 'honey', 'honey'),
    ('anaerobic', '', 'anaerobic fermentation', 'anaerobe Fermentation'),
    ('aerobic', '', 'aerobic fermentation', 'aerobe Fermentation'),
    ('monsooned', '', 'monsooned', 'monsooniert'),
    ('red_honey', 'honey', 'red honey', 'red honey'),
    ('yellow_honey', 'honey', 'yellow honey', 'yellow honey'),
    ('white_honey', 'honey', 'white honey', 'white honey'),
    ('black_honey', 'honey', 'black honey', 'black honey'),
    ('carbonic_maceration', 'anaerobic', 'carbonic maceration', 'carbonic maceration'),
    ('double_anaerobic', 'anaerobic', 'double anaerobic fermentation', 'doppelt anaerobe Fermentation'),
    ('complex_anaerobic', 'anaerobic', 'complex anaerobic fermentation', 'komplexe anaerobe Fermentation'),
    ('thermic_shock_anaerobic', 'complex_anaerobic','thermal shock anaerobic', 'anaerober thermischer Schock'),
    ('other', '', 'other', 'andere')
)

def upgrade():
    meta = sa.MetaData(bind=op.get_bind())
    meta.reflect()

    procTable =  sa.Table('processing', meta)
    procTranslationTable =  sa.Table('processing_translation', meta)
    for proc in processings:
        if len(proc[1]) == 0:
            op.execute(insert(procTable).values(name=proc[0]))
        else:
            op.execute(insert(procTable).values(name=proc[0],parent_processing=proc[1]))
        op.execute(insert(procTranslationTable).values(processing_name=proc[0], language_code='en', value=proc[2]))
        op.execute(insert(procTranslationTable).values(processing_name=proc[0], language_code='de', value=proc[3]))


def downgrade():
    meta = sa.MetaData(bind=op.get_bind())
    meta.reflect()

    procTable = sa.Table('processing', meta)
    procTranslationTable = sa.Table('processing_translation', meta)
    for proc in reversed(processings):
        op.execute(delete(procTranslationTable).where(procTranslationTable.c.processing_name == proc[0]))
        op.execute(delete(procTable).where(procTable.c.name == proc[0]))
