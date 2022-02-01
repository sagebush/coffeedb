"""Create initial tables

Revision ID: 48b0a70aecc0
Revises: 3fd8fa1b5e9b
Create Date: 2022-01-10 20:33:12.639293

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '48b0a70aecc0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'language',
        sa.Column('code', sa.CHAR(2), primary_key=True, comment='ISO 3166-1 alpha-2 country code')
    )
    op.create_table(
        'continent',
        sa.Column('name', sa.VARCHAR(64), primary_key=True, comment='provided name in snake-case')
    )
    op.create_table(
        'continent_translation',
        sa.Column('continent_name', sa.VARCHAR(64), nullable=False),
        sa.Column('language_code', sa.CHAR(2), nullable=False),
        sa.Column('value', sa.VARCHAR(128), nullable=False),
        sa.PrimaryKeyConstraint('continent_name', 'language_code', name='pk_continent_translation'),
        sa.ForeignKeyConstraint(['continent_name'], ['continent.name'], name='fk_continent_translation_cont'),
        sa.ForeignKeyConstraint(['language_code'], ['language.code'], name='fk_continent_translation_lang')
    )
    op.create_table(
        'country',
        sa.Column('name', sa.VARCHAR(64), nullable=False, comment='provided name in snake-case'),
        sa.Column('continent_name', sa.VARCHAR(64), nullable=False),
        sa.PrimaryKeyConstraint('name', name='pk_country'),
        sa.ForeignKeyConstraint(['continent_name'], ['continent.name'], name='fk_country_cont')
    )
    op.create_table(
        'country_roles',
        sa.Column('country_name', sa.VARCHAR(64), nullable=False),
        sa.Column('has_producer', sa.BOOLEAN, default=False),
        sa.Column('has_roaster', sa.BOOLEAN, default=False),
        sa.PrimaryKeyConstraint('country_name', name='pk_country'),
        sa.ForeignKeyConstraint(['country_name'], ['country.name'], name='fk_country_roles_count')
    )
    op.create_table(
        'country_translation',
        sa.Column('country_name', sa.VARCHAR(64), nullable=False),
        sa.Column('language_code', sa.CHAR(2), nullable=False),
        sa.Column('value', sa.VARCHAR(128), nullable=False),
        sa.PrimaryKeyConstraint('country_name', 'language_code', name='pk_country_translation'),
        sa.ForeignKeyConstraint(['country_name'], ['country.name'], name='fk_country_translation_count'),
        sa.ForeignKeyConstraint(['language_code'], ['language.code'], name='fk_country_translation_lang')
    )
    op.create_table(
        'country_code',
        sa.Column('country_name', sa.VARCHAR(64), nullable=False),
        sa.Column('code', sa.CHAR(2), nullable=False),
        sa.PrimaryKeyConstraint('country_name', name='pk_country_code'),
        sa.ForeignKeyConstraint(['country_name'], ['country.name'], name='fk_country_code_count'),
    )
    op.create_table(
        'region',
        sa.Column('name', sa.VARCHAR(64), nullable=False, comment='provided name in snake-case'),
        sa.Column('country_name', sa.VARCHAR(64), nullable=False),
        sa.Column('display_name', sa.VARCHAR(128), nullable=False, comment='original name in latin alphabet'),
        sa.PrimaryKeyConstraint('name', 'country_name' , name='pk_region'),
        sa.ForeignKeyConstraint(['country_name'], ['country.name'], name='fk_region_country')
    )
    op.create_table(
        'washing_station',
        sa.Column('name', sa.VARCHAR(64), nullable=False),
        sa.Column('region_name', sa.VARCHAR(64), nullable=False),
        sa.Column('display_name', sa.VARCHAR(128), nullable=False, comment='original name in latin alphabet'),
        sa.PrimaryKeyConstraint('name', name='pk_washing_station'),
        sa.ForeignKeyConstraint(['region_name'], ['region.name'], name='fk_washing_station_reg')
    )
    op.create_table(
        'producer',
        sa.Column('name', sa.VARCHAR(64), nullable=False),
        sa.Column('display_name', sa.VARCHAR(128), nullable=False, comment='original name in latin alphabet'),
        sa.PrimaryKeyConstraint('name', name='pk_producer')
    )
    op.create_table(
        'farm',
        sa.Column('name', sa.VARCHAR(64), nullable=False),
        sa.Column('display_name', sa.VARCHAR(128), nullable=False, comment='original name in latin alphabet'),
        sa.Column('country_name', sa.VARCHAR(64), nullable=False),
        sa.Column('region_name', sa.VARCHAR(64), nullable=False),
        sa.Column('producer_name', sa.VARCHAR(64)),
        sa.Column('elevation_min', sa.INTEGER, comment='in masl'),
        sa.Column('elevation_max', sa.INTEGER, comment='in masl'),
        sa.PrimaryKeyConstraint('name', name='pk_farm'),
        sa.ForeignKeyConstraint(['country_name', 'region_name'], ['region.country_name', 'region.name'], name='fk_farm_reg'),
        sa.ForeignKeyConstraint(['producer_name'], ['producer.name'], name='fk_farm_prod')
    )
    op.create_table(
        'roaster',
        sa.Column('name', sa.VARCHAR(64), nullable=False),
        sa.Column('country_name', sa.VARCHAR(64), nullable=False),
        sa.Column('display_name', sa.VARCHAR(128), nullable=False, comment='original name in latin alphabet'),
        sa.Column('url', sa.VARCHAR(256)),
        sa.PrimaryKeyConstraint('name', name='pk_roaster'),
        sa.ForeignKeyConstraint(['country_name'], ['country.name'], name='fk_roaster_count')
    )
    op.create_table(
        'flavour',
        sa.Column('name', sa.VARCHAR(64), nullable=False),
        sa.Column('parent_flavour', sa.VARCHAR(64), comment='specialization hierarchy, base is NULL'),
        sa.Column('is_sca', sa.BOOLEAN, default=False),
        sa.PrimaryKeyConstraint('name', name='pk_flavour'),
        sa.ForeignKeyConstraint(['parent_flavour'], ['flavour.name'], name='fk_flavour_flav')
    )
    op.create_table(
        'flavour_modifier',
        sa.Column('name', sa.VARCHAR(64), nullable=False),
        sa.Column('equivalent_flavour', sa.VARCHAR(128)),
        sa.Column('pattern', sa.VARCHAR(64), nullable=False),
        sa.PrimaryKeyConstraint('name', name='pk_flavour_modifier'),
        sa.ForeignKeyConstraint(['equivalent_flavour'], ['flavour.name'], name='fk_flavour_modifier_flav')
    )
    op.create_table(
        'flavour_colors',
        sa.Column('flavour_name', sa.VARCHAR(64), nullable=False),
        sa.Column('color', sa.CHAR(6), nullable=False, comment='hex value'),
        sa.Column('text_color', sa.CHAR(6), nullable=False, comment='hex value'),
        sa.PrimaryKeyConstraint('flavour_name', name='pk_flavour_colors'),
        sa.ForeignKeyConstraint(['flavour_name'], ['flavour.name'], name='fk_flavour_colors_id')
    )
    op.create_table(
        'flavour_translation',
        sa.Column('flavour_name', sa.VARCHAR(64), nullable=False),
        sa.Column('language_code', sa.CHAR(2), nullable=False),
        sa.Column('value', sa.VARCHAR(128), nullable=False),
        sa.PrimaryKeyConstraint('flavour_name', 'language_code', name='pk_flavour_translation'),
        sa.ForeignKeyConstraint(['flavour_name'], ['flavour.name'], name='fk_flavour_translation_flav'),
        sa.ForeignKeyConstraint(['language_code'], ['language.code'], name='fk_flavour_translation_lang')
    )
    op.create_table(
        'flavour_modifier_translation',
        sa.Column('flavour_modifier_name', sa.VARCHAR(64), nullable=False),
        sa.Column('language_code', sa.CHAR(2), nullable=False),
        sa.Column('value', sa.VARCHAR(128), nullable=False),
        sa.PrimaryKeyConstraint('flavour_modifier_name', 'language_code', name='pk_flavour_modifier_translation'),
        sa.ForeignKeyConstraint(['flavour_modifier_name'], ['flavour_modifier.name'], name='fk_flavour_modifier_translation_mod'),
        sa.ForeignKeyConstraint(['language_code'], ['language.code'], name='fk_flavour_modifier_translation_lang')
    )

    # processing details
    op.create_table(
        'honey_grade',
        sa.Column('name', sa.VARCHAR(64), nullable=False),
        sa.Column('display_name', sa.VARCHAR(128), nullable=False),
        sa.Column('strength', sa.INTEGER, nullable=False),
        sa.PrimaryKeyConstraint('name', name='pk_honey_grade')
    )
    op.create_table(
        'drying_device',
        sa.Column('name', sa.VARCHAR(64), nullable=False),
        sa.PrimaryKeyConstraint('name', name='pk_drying_device')
    )
    op.create_table(
        'fermentation_type',
        sa.Column('name', sa.VARCHAR(64), nullable=False),
        sa.PrimaryKeyConstraint('name', name='pk_fermentation_type')
    )
    op.create_table(
        'fermentation_modifier',
        sa.Column('name', sa.VARCHAR(64), nullable=False),
        sa.PrimaryKeyConstraint('name', name='pk_fermentation_modifier')
    )
    op.create_table(
        'bean_grading',
        sa.Column('name', sa.VARCHAR(64), nullable=False),
        sa.Column('display_name', sa.VARCHAR(128), nullable=False),
        sa.PrimaryKeyConstraint('name', name='pk_bean_size_category_modifier')
    )
    op.create_table(
        'processing',
        sa.Column('name', sa.VARCHAR(64), nullable=False, comment='provided name in snake-case'),
        sa.Column('pattern', sa.VARCHAR(16), comment='F(dry fermentation), f(wet fermentation), p(ulping), d(rying), h(ulling), w(ashing), (d)i(gestion), m(oisturing)'),
        sa.Column('default_drying_name', sa.VARCHAR(64), nullable=False),
        sa.Column('default_fermentation_type_name', sa.VARCHAR(64), nullable=False),
        sa.Column('default_fermentation_duration', sa.INTEGER, nullable=False),
        sa.PrimaryKeyConstraint('name', name='pk_processing'),
        sa.ForeignKeyConstraint(['default_drying_name'], ['drying_device.name'], name='fk_processing_drying'),
        sa.ForeignKeyConstraint(['default_fermentation_type_name'], ['fermentation_type.name'], name='fk_processing_ferm_type'),
    )
    op.create_table(
        'drying_device_translation',
        sa.Column('drying_device_name', sa.VARCHAR(64)),
        sa.Column('language_code', sa.CHAR(2)),
        sa.Column('value', sa.VARCHAR(128), nullable=False),
        sa.PrimaryKeyConstraint('drying_device_name', 'language_code', name='pk_drying_device_translation'),
        sa.ForeignKeyConstraint(['drying_device_name'], ['drying_device.name'], name='fk_drying_device_translation_device'),
        sa.ForeignKeyConstraint(['language_code'], ['language.code'], name='fk_drying_device_translation_lang')
    )
    op.create_table(
        'fermentation_type_translation',
        sa.Column('type_name', sa.VARCHAR(64)),
        sa.Column('language_code', sa.CHAR(2)),
        sa.Column('value', sa.VARCHAR(128), nullable=False),
        sa.PrimaryKeyConstraint('type_name', 'language_code', name='pk_fermentation_type_translation'),
        sa.ForeignKeyConstraint(['type_name'], ['fermentation_type.name'], name='fk_fermentation_type_translation_type'),
        sa.ForeignKeyConstraint(['language_code'], ['language.code'], name='fk_fermentation_type_translation_lang')
    )
    op.create_table(
        'fermentation_modifier_translation',
        sa.Column('modifier_name', sa.VARCHAR(64)),
        sa.Column('language_code', sa.CHAR(2)),
        sa.Column('value', sa.VARCHAR(128), nullable=False),
        sa.PrimaryKeyConstraint('modifier_name', 'language_code', name='pk_fermentation_modifier_translation'),
        sa.ForeignKeyConstraint(['modifier_name'], ['fermentation_modifier.name'], name='fk_fermentation_modifier_translation_modifier'),
        sa.ForeignKeyConstraint(['language_code'], ['language.code'], name='fk_fermentation_modifier_translation_lang')
    )
    op.create_table(
        'processing_translation',
        sa.Column('processing_name', sa.VARCHAR(64)),
        sa.Column('language_code', sa.CHAR(2)),
        sa.Column('value', sa.VARCHAR(128), nullable=False),
        sa.PrimaryKeyConstraint('processing_name', 'language_code', name='pk_processing_translation'),
        sa.ForeignKeyConstraint(['processing_name'], ['processing.name'], name='fk_processing_translation_proc'),
        sa.ForeignKeyConstraint(['language_code'], ['language.code'], name='fk_processing_translation_lang')
    )

    # decaf
    op.create_table(
        'decaf',
        sa.Column('name', sa.VARCHAR(64), nullable=False),
        sa.PrimaryKeyConstraint('name', name='pk_decaf')
    )
    op.create_table(
        'decaf_translation',
        sa.Column('decaf_name', sa.VARCHAR(64)),
        sa.Column('language_code', sa.CHAR(2)),
        sa.Column('value', sa.VARCHAR(128), nullable=False),
        sa.PrimaryKeyConstraint('decaf_name', 'language_code', name='pk_decaf_translation'),
        sa.ForeignKeyConstraint(['decaf_name'], ['decaf.name'], name='fk_decaf_translation_decaf'),
        sa.ForeignKeyConstraint(['language_code'], ['language.code'], name='fk_decaf_translation_lang')
    )
    
    # varieties
    op.create_table(
        'variety',
        sa.Column('name', sa.VARCHAR(64), comment='provided name in snake-case'),
        sa.Column('display_name', sa.VARCHAR(128), nullable=False),
        sa.PrimaryKeyConstraint('name', name='pk_variety')
    )
    op.create_table(
        'variety_inheritance',
        sa.Column('child', sa.VARCHAR(64), nullable=False),
        sa.Column('parent', sa.VARCHAR(64), nullable=False),
        sa.PrimaryKeyConstraint('child', 'parent', name='pk_variety_inheritance'),
        sa.ForeignKeyConstraint(['child'], ['variety.name'], name='fk_variety_inheritance_child'),
        sa.ForeignKeyConstraint(['parent'], ['variety.name'], name='fk_variety_inheritance_parent')
    )

    #green
    op.create_table(
        'green',
        sa.Column('id', sa.INTEGER, autoincrement=True),
        sa.Column('region_name', sa.VARCHAR(64), nullable=False),
        sa.Column('washing_station_name', sa.VARCHAR(64)),
        sa.Column('farm_name', sa.VARCHAR(64)),
        sa.Column('producer_name', sa.VARCHAR(64)),
        sa.Column('elevation_min', sa.INTEGER),
        sa.Column('elevation_max', sa.INTEGER),
        sa.Column('processing_name', sa.VARCHAR(64)),
        sa.Column('decaf_name', sa.VARCHAR(64)),
        sa.Column('lot_number', sa.INTEGER),
        sa.Column('harvest_from', sa.DATE),
        sa.Column('harvest_to', sa.DATE),
        sa.PrimaryKeyConstraint('id', name='pk_green'),
        sa.ForeignKeyConstraint(['region_name'], ['region.name'], name='fk_green_reg'),
        sa.ForeignKeyConstraint(['washing_station_name'], ['washing_station.name'], name='fk_green_wash'),
        sa.ForeignKeyConstraint(['farm_name'], ['farm.name'], name='fk_green_farm'),
        sa.ForeignKeyConstraint(['producer_name'], ['producer.name'], name='fk_green_prod'),
        sa.ForeignKeyConstraint(['processing_name'], ['processing.name'], name='fk_green_proc'),
        sa.ForeignKeyConstraint(['decaf_name'], ['decaf.name'], name='fk_green_decaf'),
    )
    op.create_table(
        'green_variety',
        sa.Column('green_id', sa.INTEGER, nullable=False),
        sa.Column('variety_name', sa.VARCHAR(64), nullable=False),
        sa.PrimaryKeyConstraint('green_id', 'variety_name', name='pk_green_variety'),
        sa.ForeignKeyConstraint(['green_id'], ['green.id'], name='fk_green_variety_green'),
        sa.ForeignKeyConstraint(['variety_name'], ['variety.name'], name='fk_green_variety_var')
    )
    op.create_table(
        'green_fermentation_duration',
        sa.Column('id', sa.INTEGER, autoincrement=True),
        sa.Column('green_id', sa.INTEGER, nullable=False),
        sa.Column('duration', sa.INTEGER, nullable=False),
        sa.PrimaryKeyConstraint('id', name='pk_green_fermentation_duration'),
        sa.ForeignKeyConstraint(['green_id'], ['green.id'], name='fk_green_fermentation_duration_green')
    )
    op.create_table(
        'green_fermentation_flavour',
        sa.Column('id', sa.INTEGER, autoincrement=True),
        sa.Column('green_id', sa.INTEGER, nullable=False),
        sa.Column('flavour_name', sa.VARCHAR(64), nullable=False),
        sa.PrimaryKeyConstraint('id', name='pk_green_fermentation_flavour'),
        sa.ForeignKeyConstraint(['green_id'], ['green.id'], name='fk_green_fermentation_flavour_green'),
        sa.ForeignKeyConstraint(['flavour_name'], ['flavour.name'], name='fk_green_fermentation_flavour_flav')
    )
    op.create_table(
        'green_honey_grade',
        sa.Column('id', sa.INTEGER, autoincrement=True),
        sa.Column('green_id', sa.INTEGER, nullable=False),
        sa.Column('honey_grade_name', sa.VARCHAR(64), nullable=False),
        sa.PrimaryKeyConstraint('id', name='pk_green_honey_grade'),
        sa.ForeignKeyConstraint(['green_id'], ['green.id'], name='fk_green_honey_grade_green'),
        sa.ForeignKeyConstraint(['honey_grade_name'], ['honey_grade.name'], name='fk_green_honey_grade_grade')
    )
    op.create_table(
        'green_bean_grading',
        sa.Column('id', sa.INTEGER, autoincrement=True),
        sa.Column('green_id', sa.INTEGER, nullable=False),
        sa.Column('bean_grading_name', sa.VARCHAR(64), nullable=False),
        sa.PrimaryKeyConstraint('id', name='pk_green_bean_grading'),
        sa.ForeignKeyConstraint(['green_id'], ['green.id'], name='fk_green_bean_grading_green'),
        sa.ForeignKeyConstraint(['bean_grading_name'], ['bean_grading.name'], name='fk_green_bean_grading_grad')
    )
    op.create_table(
        'green_drying_device',
        sa.Column('id', sa.INTEGER, autoincrement=True),
        sa.Column('green_id', sa.INTEGER, nullable=False),
        sa.Column('drying_device_name', sa.VARCHAR(64), nullable=False),
        sa.PrimaryKeyConstraint('id', name='pk_green_drying_device'),
        sa.ForeignKeyConstraint(['green_id'], ['green.id'], name='fk_green_drying_device_green'),
        sa.ForeignKeyConstraint(['drying_device_name'], ['drying_device.name'], name='fk_green_drying_device_dev')
    )
    op.create_table(
        'green_fermentation_type',
        sa.Column('id', sa.INTEGER, autoincrement=True),
        sa.Column('green_id', sa.INTEGER, nullable=False),
        sa.Column('fermentation_type_name', sa.VARCHAR(64), nullable=False),
        sa.PrimaryKeyConstraint('id', name='pk_green_fermentation_type'),
        sa.ForeignKeyConstraint(['green_id'], ['green.id'], name='fk_green_fermentation_type_green'),
        sa.ForeignKeyConstraint(['fermentation_type_name'], ['fermentation_type.name'], name='fk_green_fermentation_type_type')
    )
    op.create_table(
        'green_fermentation_modifier',
        sa.Column('id', sa.INTEGER, autoincrement=True),
        sa.Column('green_id', sa.INTEGER, nullable=False),
        sa.Column('fermentation_modifier_name', sa.VARCHAR(64), nullable=False),
        sa.PrimaryKeyConstraint('id', name='pk_green_fermentation_modifier'),
        sa.ForeignKeyConstraint(['green_id'], ['green.id'], name='fk_green_fermentation_modifier_green'),
        sa.ForeignKeyConstraint(['fermentation_modifier_name'], ['fermentation_modifier.name'], name='fk_green_fermentation_modifier_mod')
    )

    # coffee related
    op.create_table(
        'roast',
        sa.Column('name', sa.VARCHAR(64), nullable=False),
        sa.PrimaryKeyConstraint('name', name='pk_roast')
    )
    op.create_table(
        'roast_translation',
        sa.Column('roast_name', sa.VARCHAR(64), nullable=False),
        sa.Column('language_code', sa.CHAR(2), nullable=False),
        sa.Column('value', sa.VARCHAR(128), nullable=False),
        sa.PrimaryKeyConstraint('roast_name', 'language_code', name='pk_roast_translation'),
        sa.ForeignKeyConstraint(['roast_name'], ['roast.name'], name='fk_roast_translation_roast'),
        sa.ForeignKeyConstraint(['language_code'], ['language.code'], name='fk_roast_translation_lang')
    )
    op.create_table(
        'certification',
        sa.Column('name', sa.VARCHAR(64), nullable=False),
        sa.PrimaryKeyConstraint('name', name='pk_certification')
    )
    op.create_table(
        'certification_translation',
        sa.Column('certification_name', sa.VARCHAR(64)),
        sa.Column('language_code', sa.CHAR(2)),
        sa.Column('value', sa.VARCHAR(128), nullable=False),
        sa.PrimaryKeyConstraint('certification_name', 'language_code', name='pk_certification_translation'),
        sa.ForeignKeyConstraint(['certification_name'], ['certification.name'], name='fk_certification_translation_cert'),
        sa.ForeignKeyConstraint(['language_code'], ['language.code'], name='fk_certification_translation_lang')
    )

    # coffee
    op.create_table(
        'coffee',
        sa.Column('id', sa.INTEGER, autoincrement=True),
        sa.Column('display_name', sa.VARCHAR(128), nullable=False),
        sa.Column('roaster_name', sa.VARCHAR(64), nullable=False),
        sa.Column('roast_name', sa.VARCHAR(64)),
        sa.Column('score', sa.INTEGER),
        sa.Column('certification', sa.VARCHAR(64)),
        sa.PrimaryKeyConstraint('id', name='pk_coffee'),
        sa.ForeignKeyConstraint(['roast_name'], ['roast.name'], name='fk_coffee_roast'),
        sa.ForeignKeyConstraint(['roaster_name'], ['roaster.name'], name='fk_coffee_roaster')
    )
    op.create_table(
        'coffee_green',
        sa.Column('coffee_id', sa.INTEGER, nullable=False),
        sa.Column('green_id', sa.INTEGER, nullable=False),
        sa.Column('percentage', sa.INTEGER, default=100),
        sa.PrimaryKeyConstraint('coffee_id', 'green_id', name='pk_coffee_green'),
        sa.ForeignKeyConstraint(['coffee_id'], ['coffee.id'], name='fk_coffee_green_cof'),
        sa.ForeignKeyConstraint(['green_id'], ['green.id'], name='fk_coffee_green_green')
    )
    op.create_table(
        'coffee_flavour',
        sa.Column('coffee_id', sa.INTEGER, nullable=False),
        sa.Column('flavour_name', sa.VARCHAR(64), nullable=False),
        sa.PrimaryKeyConstraint('coffee_id', 'flavour_name', name='pk_coffee_flavour'),
        sa.ForeignKeyConstraint(['coffee_id'], ['coffee.id'], name='fk_coffee_flavour_cof'),
        sa.ForeignKeyConstraint(['flavour_name'], ['flavour.name'], name='fk_coffee_flavour_flav')
    )
    op.create_table(
        'coffee_flavour_modifier',
        sa.Column('coffee_id', sa.INTEGER, nullable=False),
        sa.Column('flavour_name', sa.VARCHAR(64), nullable=False),
        sa.Column('flavour_modifier_name', sa.VARCHAR(64), nullable=False),
        sa.PrimaryKeyConstraint('coffee_id', 'flavour_name', name='pk_coffee_flavour_modifier'),
        sa.ForeignKeyConstraint(['coffee_id'], ['coffee.id'], name='fk_coffee_flavour_modifier_cof'),
        sa.ForeignKeyConstraint(['flavour_name'], ['flavour.name'], name='fk_coffee_flavour_modifier_flav'),
        sa.ForeignKeyConstraint(['flavour_modifier_name'], ['flavour_modifier.name'], name='fk_coffee_flavour_modifier_mod')
    )
    op.create_table(
        'coffee_availability',
        sa.Column('id', sa.INTEGER, autoincrement=True),
        sa.Column('coffee_id', sa.INTEGER, nullable=False),
        sa.Column('available_from', sa.DATE, nullable=False),
        sa.Column('available_to', sa.DATE),
        sa.Column('url', sa.VARCHAR(256)),
        sa.PrimaryKeyConstraint('id', name='pk_coffee_availability'),
        sa.ForeignKeyConstraint(['coffee_id'], ['coffee.id'], name='fk_coffee_availability_cof')
    )


def downgrade():
    op.drop_table('coffee_availability')
    op.drop_table('coffee_flavour_modifier')
    op.drop_table('coffee_flavour')
    op.drop_table('coffee_green')
    op.drop_table('coffee')
    op.drop_table('certification_translation')
    op.drop_table('certification')
    op.drop_table('roast_translation')
    op.drop_table('roast')
    op.drop_table('green_fermentation_modifier')
    op.drop_table('green_fermentation_type')
    op.drop_table('green_drying_device')
    op.drop_table('green_honey_grade')
    op.drop_table('green_fermentation_flavour')
    op.drop_table('green_fermentation_duration')
    op.drop_table('green_variety')
    op.drop_table('green')
    op.drop_table('variety_inheritance')
    op.drop_table('variety')
    op.drop_table('decaf_translation')
    op.drop_table('decaf')
    op.drop_table('processing_translation')
    op.drop_table('fermentation_modifier_translation')
    op.drop_table('fermentation_type_translation')
    op.drop_table('drying_device_translation')
    op.drop_table('processing')
    op.drop_table('bean_grading')
    op.drop_table('fermentation_modifier')
    op.drop_table('fermentation_type')
    op.drop_table('drying_device')
    op.drop_table('honey_grade')
    op.drop_table('flavour_modifier_translation')
    op.drop_table('flavour_translation')
    op.drop_table('flavour_colors')
    op.drop_table('flavour_modifier')
    op.drop_table('flavour')
    op.drop_table('roaster')
    op.drop_table('farm')
    op.drop_table('producer')
    op.drop_table('washing_station')
    op.drop_table('region')
    op.drop_table('country_code')
    op.drop_table('country_translation')
    op.drop_table('country_roles')
    op.drop_table('country')
    op.drop_table('continent_translation')
    op.drop_table('continent')
    op.drop_table('language')
