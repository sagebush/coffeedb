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

processing =(
    #(name, pattern, defaultDrying, defaultFermType, defaultFermDuration):
	('natural', 'Fph', 'ground', 'aerobic', 0, 'natural', 'natural'),
	('washed', 'pfwdh', 'ground', 'aerobic', 24, 'washed', 'gewaschen'),
	('wetHulled', 'pfhd', 'ground', 'aerobic', 12, 'wet hulled', 'nass geschält'),
	('honey', 'pFh', 'ground', 'aerobic', 0, 'honey', 'honey'),
	('monsooned', 'Fphm', 'ground', 'aerobic', 0, 'monsooned', 'monsooniert'),
	('digested', 'iwdwd', 'ground', 'anaerobic', 24, 'digested', 'verdaut'),
	('doubleFerm', 'pfwfwdh', 'ground', 'aerobic', 24, 'double fermentation', 'doppelt fermentiert'),
)
honey_grade = (
	('white', 0),
	('yellow', 1),
	('orange', 2),
	('red', 3),
	('black', 4)
)
bean_size_categories = (
    ('aa', 'AA'),
    ('ab', 'AB'),
    ('pb', 'PB'),
    ('e', 'E')
)
drying_device = (
	('ground', 'sundried', 'sonnengetrocknet'),
	('raised_beds', 'dried on raised beds', 'auf Tischen getrocknet'),
	('mechanical_dryers' 'mechanically dried', 'mechanisch getrocknet')
)
ferm_type = (
    ('cm', 'carbonic maceration', 'carbonic maceration'),
	('aerobic', 'aerobic fermentation', 'aerobe Fermentation'),
	('semianaerobic', 'semi-anaerobic fermentation', 'semi-anaerobe Fermentation'),
	('anaerobic', 'anaerobic fermentation', 'anaerobe Fermentation')
)
ferm_mod = (
	('lactic', 'lactic bacteria', 'Milchsäurebakterien'),
    ('acetic', 'acetic bacteria', 'acetogene Bakterien'),
	('yeasts', 'yeast', 'Hefe'),
	('wild_cultures', 'local bacteria', 'regional Bakterien'),
	('thermic_shock', 'thermal shock', 'thermischer Schock')
)
def upgrade():
    meta = sa.MetaData(bind=op.get_bind())
    meta.reflect()

    honeyTable =  sa.Table('honey_grade', meta)
    for hon in honey_grade:
        op.execute(insert(honeyTable).values(name=hon[0], display_name=hon[0], strength=hon[1]))

    dryingTable =  sa.Table('drying_device', meta)
    dryingTransTable =  sa.Table('drying_device_translation', meta)
    for dry in drying_device:
        op.execute(insert(dryingTable).values(name=dry[0]))
        op.execute(insert(dryingTransTable).values(drying_device_name=dry[0], language_code='en', value=dry[1]))
        op.execute(insert(dryingTransTable).values(drying_device_name=dry[0], language_code='de', value=dry[2]))

    fermTypeTable =  sa.Table('fermentation_type', meta)
    fermTypeTransTable =  sa.Table('fermentation_type_translation', meta)
    for type in ferm_type:
        op.execute(insert(fermTypeTable).values(name=type[0]))
        op.execute(insert(fermTypeTransTable).values(type_name=type[0], language_code='en', value=type[1]))
        op.execute(insert(fermTypeTransTable).values(type_name=type[0], language_code='de', value=type[2]))

    fermModTable =  sa.Table('fermentation_modifier', meta)
    fermModTransTable =  sa.Table('fermentation_modifier_translation', meta)
    for mod in ferm_mod:
        op.execute(insert(fermModTable).values(name=mod[0]))
        op.execute(insert(fermModTransTable).values(modifier_name=mod[0], language_code='en', value=mod[1]))
        op.execute(insert(fermModTransTable).values(modifier_name=mod[0], language_code='de', value=mod[2]))

    procTable =  sa.Table('processing', meta)
    procTranslationTable =  sa.Table('processing_translation', meta)
    for proc in processing:
        op.execute(insert(procTable).values(name=proc[0], pattern=proc[1], default_drying_name=proc[2], \
            default_fermentation_type_name=proc[3], default_fermentation_duration=proc[4]))
        op.execute(insert(procTranslationTable).values(processing_name=proc[0], language_code='en', value=proc[2]))
        op.execute(insert(procTranslationTable).values(processing_name=proc[0], language_code='de', value=proc[3]))


def downgrade():
    meta = sa.MetaData(bind=op.get_bind())
    meta.reflect()

    procTable =  sa.Table('processing', meta)
    procTranslationTable =  sa.Table('processing_translation', meta)
    for proc in processing:
        op.execute(delete(procTable).where(procTable.c.name == proc[0]))
        op.execute(delete(procTranslationTable).where(procTranslationTable.c.processing_name == proc[0]))

    fermModTable =  sa.Table('fermentation_modifier', meta)
    fermModTransTable =  sa.Table('fermentation_modifier_translation', meta)
    for mod in ferm_mod:
        op.execute(delete(fermModTable).where(fermModTable.c.name == mod[0]))
        op.execute(delete(fermModTransTable).where(fermModTransTable.c.modifier_name == mod[0]))

    fermTypeTable =  sa.Table('fermentation_type', meta)
    fermTypeTransTable =  sa.Table('fermentation_type_translation', meta)
    for type in ferm_type:
        op.execute(delete(fermTypeTable).where(fermTypeTable.c.name == type[0]))
        op.execute(delete(fermTypeTransTable).where(fermTypeTransTable.c.type_name == type[0]))

    fermTypeTable =  sa.Table('fermentation_type', meta)
    fermTypeTransTable =  sa.Table('fermentation_type_translation', meta)
    for type in ferm_type:
        op.execute(delete(fermTypeTable).where(fermTypeTable.c.name == type[0]))
        op.execute(delete(fermTypeTransTable).where(fermTypeTransTable.c.type_name == type[0]))

    dryingTable =  sa.Table('drying_device', meta)
    dryingTransTable =  sa.Table('drying_device_translation', meta)
    for dry in drying_device:
        op.execute(delete(dryingTable).where(dryingTable.c.name == dry[0]))
        op.execute(delete(dryingTransTable).where(dryingTransTable.c.drying_device_name == dry[0]))

    honeyTable =  sa.Table('honey_grade', meta)
    for hon in honey_grade:
        op.execute(delete(honeyTable).values(name=hon[0], display_name=hon[0], strength=hon[1]))

