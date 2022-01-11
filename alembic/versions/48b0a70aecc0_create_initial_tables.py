"""Create initial tables

Revision ID: 48b0a70aecc0
Revises: 3fd8fa1b5e9b
Create Date: 2022-01-10 20:33:12.639293

"""
from alembic import op
import sqlalchemy as sa
from alembic import command, config
from sqlalchemy.sql.schema import ForeignKey, UniqueConstraint


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
        sa.Column('ref_name', sa.VARCHAR(64), primary_key=True, comment='provided name in snake-case')
    )
    op.create_table(
        'continent_i18n',
        sa.Column('continent_ref_name', sa.VARCHAR(64), nullable=False),
        sa.Column('language_code', sa.CHAR(2), nullable=False),
        sa.Column('translation', sa.VARCHAR(128), nullable=False),
        sa.PrimaryKeyConstraint('continent_ref_name', 'language_code', name='pk_continent_i18n'),
        sa.ForeignKeyConstraint(['continent_ref_name'], ['continent.ref_name'], name='fk_continent_i18n_cont'),
        sa.ForeignKeyConstraint(['language_code'], ['language.code'], name='fk_continent_i18n_lang')
    )
    op.create_table(
        'country',
        sa.Column('code', sa.CHAR(2), nullable=False, comment='ISO 3166-1 alpha-2 country code'),
        sa.Column('continent_ref_name', sa.VARCHAR(64), nullable=False),
        sa.PrimaryKeyConstraint('code', name='pk_country'),
        sa.ForeignKeyConstraint(['continent_ref_name'], ['continent.ref_name'], name='fk_country_cont')
    )
    op.create_table(
        'country_i18n',
        sa.Column('country_code', sa.CHAR(2), nullable=False),
        sa.Column('language_code', sa.CHAR(2), nullable=False),
        sa.Column('translation', sa.VARCHAR(128), nullable=False),
        sa.PrimaryKeyConstraint('country_code', 'language_code', name='pk_country_i18n'),
        sa.ForeignKeyConstraint(['country_code'], ['country.code'], name='fk_country_i18n_count'),
        sa.ForeignKeyConstraint(['language_code'], ['language.code'], name='fk_country_i18n_lang')
    )
    op.create_table(
        'area',
        sa.Column('ref_name', sa.VARCHAR(64), nullable=False, comment='provided name in snake-case'),
        sa.Column('country_code', sa.CHAR(2), nullable=False),
        sa.PrimaryKeyConstraint('ref_name', 'country_code', name='pk_area'),
        sa.ForeignKeyConstraint(['country_code'], ['country.code'], name='fk_area_count')
    )
    op.create_table(
        'area_i18n',
        sa.Column('area_ref_name', sa.VARCHAR(64), nullable=False),
        sa.Column('language_code', sa.CHAR(2), nullable=False),
        sa.Column('translation', sa.VARCHAR(128), nullable=False),
        sa.PrimaryKeyConstraint('area_ref_name', 'language_code', name='pk_area_i18n'),
        sa.ForeignKeyConstraint(['area_ref_name'], ['area.ref_name'], name='fk_area_i18n_area'),
        sa.ForeignKeyConstraint(['language_code'], ['language.code'], name='fk_area_i18n_lang')
    )
    op.create_table(
        'region',
        sa.Column('ref_name', sa.VARCHAR(64), nullable=False, comment='provided name in snake-case'),
        sa.Column('area_ref_name', sa.VARCHAR(64), nullable=False),
        sa.Column('display_name', sa.VARCHAR(128), nullable=False, comment='original name in latin alphabet'),
        sa.PrimaryKeyConstraint('ref_name', name='pk_region'),
        sa.ForeignKeyConstraint(['area_ref_name'], ['area.ref_name'], name='fk_region_area')
    )
    op.create_table(
        'washing_station',
        sa.Column('id', sa.INTEGER, autoincrement=True, comment='is added by crawler -> autogenerate id'),
        sa.Column('region_ref_name', sa.VARCHAR(64), nullable=False),
        sa.Column('display_name', sa.VARCHAR(128), nullable=False, comment='original name in latin alphabet'),
        sa.PrimaryKeyConstraint('id', name='pk_washing_station'),
        sa.ForeignKeyConstraint(['region_ref_name'], ['region.ref_name'], name='fk_washing_station_reg')
    )
    op.create_table(
        'producer',
        sa.Column('id', sa.INTEGER, autoincrement=True, comment='is added by crawler -> autogenerate id'),
        sa.Column('display_name', sa.VARCHAR(128), nullable=False, comment='original name in latin alphabet'),
        sa.PrimaryKeyConstraint('id', name='pk_producer')
    )
    op.create_table(
        'farm',
        sa.Column('id', sa.INTEGER, autoincrement=True, comment='is added by crawler -> autogenerate id'),
        sa.Column('display_name', sa.VARCHAR(128), nullable=False, comment='original name in latin alphabet'),
        sa.Column('region_ref_name', sa.VARCHAR(64), nullable=False),
        sa.Column('producer_id', sa.INTEGER),
        sa.Column('elevation_min', sa.INTEGER, comment='in masl'),
        sa.Column('elevation_max', sa.INTEGER, comment='in masl'),
        sa.PrimaryKeyConstraint('id', name='pk_farm'),
        sa.ForeignKeyConstraint(['region_ref_name'], ['region.ref_name'], name='fk_farm_reg'),
        sa.ForeignKeyConstraint(['producer_id'], ['producer.id'], name='fk_farm_prod')
    )
    op.create_table(
        'roaster',
        sa.Column('id', sa.INTEGER, autoincrement=True, comment='is added by crawler -> autogenerate id'),
        sa.Column('country_code', sa.CHAR(2), nullable=False),
        sa.Column('display_name', sa.VARCHAR(128), nullable=False, comment='original name in latin alphabet'),
        sa.Column('url', sa.VARCHAR(256)),
        sa.PrimaryKeyConstraint('id', name='pk_roaster'),
        sa.ForeignKeyConstraint(['country_code'], ['country.code'], name='fk_roaster_count')
    )
    op.create_table(
        'flavour',
        sa.Column('id', sa.INTEGER, autoincrement=True, comment='partly added by crawler -> autogenerate id'),
        sa.Column('parent_flavour', sa.INTEGER, comment='specialization hierarchy, base is NULL'),
        sa.Column('is_sca', sa.BOOLEAN, default=False),
        sa.PrimaryKeyConstraint('id', name='pk_flavour'),
        sa.ForeignKeyConstraint(['parent_flavour'], ['flavour.id'], name='fk_flavour_flav')
    )
    op.create_table(
        'flavour_colors',
        sa.Column('flavour_id', sa.INTEGER, nullable=False),
        sa.Column('color', sa.CHAR(6), nullable=False, comment='hex value'),
        sa.Column('text_color', sa.CHAR(6), nullable=False, comment='hex value'),
        sa.PrimaryKeyConstraint('flavour_id', name='pk_flavour_colors'),
        sa.ForeignKeyConstraint(['flavour_id'], ['flavour.id'], name='fk_flavour_colors_id')
    )
    op.create_table(
        'flavour_i18n',
        sa.Column('flavour_id', sa.INTEGER, nullable=False),
        sa.Column('language_code', sa.CHAR(2), nullable=False),
        sa.Column('translation', sa.VARCHAR(128), nullable=False),
        sa.PrimaryKeyConstraint('flavour_id', 'language_code', name='pk_flavour_i18n'),
        sa.ForeignKeyConstraint(['flavour_id'], ['flavour.id'], name='fk_flavour_i18n_flav'),
        sa.ForeignKeyConstraint(['language_code'], ['language.code'], name='fk_flavour_i18n_lang')
    )
    op.create_table(
        'processing',
        sa.Column('ref_name', sa.VARCHAR(64), nullable=False, comment='provided name in snake-case'),
        sa.Column('parent_processing', sa.VARCHAR(64), comment='specialization hierarchy, base is NULL'),
        sa.PrimaryKeyConstraint('ref_name', name='pk_processing'),
        sa.ForeignKeyConstraint(['parent_processing'], ['processing.ref_name'], name='fk_processing_proc')
    )
    op.create_table(
        'processing_i18n',
        sa.Column('processing_ref_name', sa.VARCHAR(64), primary_key=True),
        sa.Column('language_code', sa.CHAR(2), primary_key=True),
        sa.Column('translation', sa.VARCHAR(128), nullable=False),
        sa.PrimaryKeyConstraint('processing_ref_name', 'language_code', name='pk_processing_i18n'),
        sa.ForeignKeyConstraint(['processing_ref_name'], ['processing.ref_name'], name='fk_processing_i18n_proc'),
        sa.ForeignKeyConstraint(['language_code'], ['language.code'], name='fk_processing_i18n_lang')
    )
    op.create_table(
        'variety',
        sa.Column('ref_name', sa.VARCHAR(64), comment='provided name in snake-case'),
        sa.Column('display_name', sa.VARCHAR(128), nullable=False),
        sa.PrimaryKeyConstraint('ref_name', name='pk_variety')
    )
    op.create_table(
        'variety_inheritance',
        sa.Column('child_variety', sa.VARCHAR(64), nullable=False),
        sa.Column('parent_variety', sa.VARCHAR(64), nullable=False),
        sa.PrimaryKeyConstraint('child_variety', 'parent_variety', name='pk_variety_inheritance'),
        sa.ForeignKeyConstraint(['child_variety'], ['variety.ref_name'], name='fk_variety_inheritance_child'),
        sa.ForeignKeyConstraint(['parent_variety'], ['variety.ref_name'], name='fk_variety_inheritance_parent')
    )
    op.create_table(
        'green',
        sa.Column('id', sa.INTEGER, autoincrement=True),
        sa.Column('region_ref_name', sa.VARCHAR(64), nullable=False),
        sa.Column('washing_station_id', sa.INTEGER),
        sa.Column('farm_id', sa.INTEGER),
        sa.Column('producer_id', sa.INTEGER),
        sa.Column('elevation_min', sa.INTEGER),
        sa.Column('elevation_max', sa.INTEGER),
        sa.Column('processing_ref_name', sa.VARCHAR(64)),
        sa.PrimaryKeyConstraint('id', name='pk_green'),
        sa.ForeignKeyConstraint(['region_ref_name'], ['region.ref_name'], name='fk_green_reg'),
        sa.ForeignKeyConstraint(['washing_station_id'], ['washing_station.id'], name='fk_green_wash'),
        sa.ForeignKeyConstraint(['farm_id'], ['farm.id'], name='fk_green_farm'),
        sa.ForeignKeyConstraint(['producer_id'], ['producer.id'], name='fk_green_prod'),
        sa.ForeignKeyConstraint(['processing_ref_name'], ['processing.ref_name'], name='fk_green_proc')
    )
    op.create_table(
        'green_varieties',
        sa.Column('green_id', sa.INTEGER, nullable=False),
        sa.Column('variety_ref_name', sa.VARCHAR(64), nullable=False),
        sa.PrimaryKeyConstraint('green_id', 'variety_ref_name', name='pk_green_varieties'),
        sa.ForeignKeyConstraint(['green_id'], ['green.id'], name='fk_green_varieties_green'),
        sa.ForeignKeyConstraint(['variety_ref_name'], ['variety.ref_name'], name='fk_green_varieties_var')
    )
    op.create_table(
        'coffee',
        sa.Column('id', sa.INTEGER, autoincrement=True),
        sa.Column('display_name', sa.VARCHAR(128), nullable=False),
        sa.Column('roaster_id', sa.INTEGER, nullable=False),
        sa.PrimaryKeyConstraint('id', name='pk_coffee'),
        sa.ForeignKeyConstraint(['roaster_id'], ['roaster.id'], name='fk_coffee_roast'),
    )
    op.create_table(
        'coffee_greens',
        sa.Column('coffee_id', sa.INTEGER, nullable=False),
        sa.Column('green_id', sa.INTEGER, nullable=False),
        sa.Column('percentage', sa.INTEGER, default=100),
        sa.PrimaryKeyConstraint('coffee_id', 'green_id', name='pk_coffee_greens'),
        sa.ForeignKeyConstraint(['coffee_id'], ['coffee.id'], name='fk_coffee_greens_cof'),
        sa.ForeignKeyConstraint(['green_id'], ['green.id'], name='fk_coffee_greens_gree')
    )
    op.create_table(
        'coffee_flavours',
        sa.Column('coffee_id', sa.INTEGER, nullable=False),
        sa.Column('flavour_id', sa.INTEGER, nullable=False),
        sa.PrimaryKeyConstraint('coffee_id', 'flavour_id', name='pk_coffee_flavours'),
        sa.ForeignKeyConstraint(['coffee_id'], ['coffee.id'], name='fk_coffee_flavours_cof'),
        sa.ForeignKeyConstraint(['flavour_id'], ['flavour.id'], name='fk_coffee_flavours_flav')
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
    op.drop_table('coffee_flavours')
    op.drop_table('coffee_greens')
    op.drop_table('coffee')
    op.drop_table('green_varieties')
    op.drop_table('green')
    op.drop_table('variety_inheritance')
    op.drop_table('variety')
    op.drop_table('processing_i18n')
    op.drop_table('processing')
    op.drop_table('flavour_i18n')
    op.drop_table('flavour_colors')
    op.drop_table('flavour')
    op.drop_table('roaster')
    op.drop_table('farm')
    op.drop_table('producer')
    op.drop_table('washing_station')
    op.drop_table('region')
    op.drop_table('area_i18n')
    op.drop_table('area')
    op.drop_table('country_i18n')
    op.drop_table('country')
    op.drop_table('continent_i18n')
    op.drop_table('continent')
    op.drop_table('language')
