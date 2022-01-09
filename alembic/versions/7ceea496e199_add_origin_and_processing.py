"""add origin and processing

Revision ID: 7ceea496e199
Revises: 
Create Date: 2022-01-08 17:46:33.400856

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.schema import ForeignKey

# revision identifiers, used by Alembic.
revision = '7ceea496e199'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    originTable = op.create_table(
        'origin',
        sa.Column('id', sa.INTEGER, autoincrement=True, primary_key=True),
        sa.Column('ref_name', sa.VARCHAR(64), nullable=False),
    )
    op.bulk_insert(originTable,
        [
            {'ref_name':'brazil'},
            {'ref_name':'vietnam'},
            {'ref_name':'colombia'},
            {'ref_name':'indonesia'},
            {'ref_name':'ethiopia'},
            {'ref_name':'honduras'},
            {'ref_name':'india'},
            {'ref_name':'uganda'},
            {'ref_name':'mexico'},
            {'ref_name':'guatemala'},
            {'ref_name':'peru'},
            {'ref_name':'nicaragua'},
            {'ref_name':'china'},
            {'ref_name':'ivory_coast'},
            {'ref_name':'costa_rica'},
            {'ref_name':'kenya'},
            {'ref_name':'papua_new_guinea'},
            {'ref_name':'tanzania'},
            {'ref_name':'el_salvador'},
            {'ref_name':'ecuador'},
            {'ref_name':'cameroon'},
            {'ref_name':'laos'},
            {'ref_name':'madagascar'},
            {'ref_name':'gabon'},
            {'ref_name':'thailand'},
            {'ref_name':'venezuela'},
            {'ref_name':'dominican_republic'},
            {'ref_name':'haiti'},
            {'ref_name':'congo'},
            {'ref_name':'rwanda'},
            {'ref_name':'burundi'},
            {'ref_name':'philippines'},
            {'ref_name':'togo'},
            {'ref_name':'guinea'},
            {'ref_name':'yemen'},
            {'ref_name':'cuba'},
            {'ref_name':'panama'},
            {'ref_name':'bolivia'},
            {'ref_name':'central_african_republic'},
            {'ref_name':'nigeria'},
            {'ref_name':'ghana'},
            {'ref_name':'sierra_leone'},
            {'ref_name':'jamaica'},
            {'ref_name':'paraguay'},
            {'ref_name':'malawi'},
            {'ref_name':'trinidad_tobago'},
            {'ref_name':'zimbabwe'},
            {'ref_name':'liberia'},
            {'ref_name':'zambia'},
        ]
    )
    processingTable = op.create_table(
        'processing',
        sa.Column('id', sa.INTEGER, primary_key=True, nullable=False),
        sa.Column('ref_name', sa.VARCHAR(64), nullable=False),
    )
    op.bulk_insert(processingTable,
        [
            {'id':1, 'ref_name':'washed'},
            {'id':2, 'ref_name':'natural'},
            {'id':3, 'ref_name':'honey'},
            {'id':4, 'ref_name':'anaerobic'},
            {'id':5, 'ref_name':'carbonic_marceration'},
            {'id':6, 'ref_name':'anaerobic_thermal_shock'},
            {'id':7, 'ref_name':'anaerobic_washed'},
            {'id':8, 'ref_name':'double_anaerobic'},
            {'id':9, 'ref_name':'red_honey'},
            {'id':10, 'ref_name':'yellow_honey'},
            {'id':11, 'ref_name':'black_honey'},
            {'id':12, 'ref_name':'white_honey'},
        ]
    )
    processingRelationsTable = op.create_table(
        'processing_relations',
        sa.Column('id', sa.INTEGER, autoincrement=True, primary_key=True),
        sa.Column('processing_id', sa.INTEGER, ForeignKey("processing.id"), nullable=False),
        sa.Column('parent_id', sa.INTEGER, ForeignKey("processing.id"), nullable=False),
    )
    op.bulk_insert(processingRelationsTable,
        [
            {'processing_id':5, 'parent_id':4},
            {'processing_id':6, 'parent_id':4},
            {'processing_id':7, 'parent_id':4},
            {'processing_id':8, 'parent_id':4},
            {'processing_id':9, 'parent_id':3},
            {'processing_id':10, 'parent_id':3},
            {'processing_id':11, 'parent_id':3},
            {'processing_id':12, 'parent_id':3},
        ]
    )

def downgrade():
    op.drop_table('origin')
    op.drop_table('language')
