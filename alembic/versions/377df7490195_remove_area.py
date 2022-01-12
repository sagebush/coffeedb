"""Remove area

Revision ID: 377df7490195
Revises: 48b0a70aecc0
Create Date: 2022-01-12 20:23:37.359616

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '377df7490195'
down_revision = '48b0a70aecc0'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_constraint('fk_region_area', 'region', 'foreignkey')
    op.alter_column('region', 'area_ref_name', new_column_name='country_code', type_=sa.CHAR(2), existing_nullable=False, existing_type=sa.VARCHAR(64) )
    op.create_foreign_key('fk_region_country','region', 'country', ['country_code'], ['code'])
    op.drop_table('area_i18n')
    op.drop_table('area')


def downgrade():
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
    op.drop_constraint('fk_region_country', 'region', 'foreignkey')
    op.alter_column('region', 'country_ref_name', new_column_name='area_ref_name', existing_nullable=False, existing_type=sa.VARCHAR(64) )
    op.create_foreign_key('fk_region_area', 'region', 'area', ['area_ref_name'], ['ref_name'])
