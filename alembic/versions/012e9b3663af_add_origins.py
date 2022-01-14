"""Add origins

Revision ID: 012e9b3663af
Revises: 377df7490195
Create Date: 2022-01-12 21:58:54.149244

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '012e9b3663af'
down_revision = '48b0a70aecc0'
branch_labels = None
depends_on = None

countries = (
    # the worlds largest coffee producers
    ('brazil', 'BR', 'south_america', 'Brazil', 'Brazilien'),
    ('vietnam', 'VN', 'asia', 'Vietnam', 'Vietnam'),
    ('colombia', 'CO', 'south_america', 'Colombia', 'Columbien'),
    ('indonesia', 'ID', 'asia', 'Indonesia', 'Indonesien'),
    ('ethiopia', 'ET', 'africa', 'Ethiopia', 'Äthiopien'),
    ('honduras', 'HN', 'south_america', 'Honduras', 'Honduras'),
    ('india', 'IN', 'asia', 'India', 'Indien'),
    ('uganda', 'UG', 'africa', 'Uganda', 'Uganda'),
    ('mexico', 'MX', 'south_america', 'Mexico', 'Mexico'),
    ('guatemala', 'GT', 'south_america', 'Guatemala', 'Guatemala'),
    ('peru', 'PE', 'south_america', 'Peru', 'Peru'),
    ('nicaragua', 'NI', 'south_america', 'Nicaragua', 'Nicaragua'),
    ('china', 'CN', 'asia', 'China', 'China'),
    ('ivory_coast', 'CI', 'africa', 'Ivory Coast', 'Elfenbeinküste'),
    ('costa_rica', 'CR', 'south_america', 'Costa Rica', 'Costa Rica'),
    ('kenya', 'KE', 'africa', 'Kenya', 'Kenya'),
    ('papua_new_guinea', 'PG', 'oceania', 'Papua New Guinea', 'Papua Neu Guinea'),
    ('tanzania', 'TZ', 'africa', 'Tanzania', 'Tanzania'),
    ('el_salvador', 'SV', 'south_america', 'El Salvador', 'El Salvador'),
    ('ecuador', 'EC', 'south_america', 'Ecuador', 'Ecuador'),
    ('cameroon', 'CM', 'africa', 'Cameroon', 'Kamerun'),
    ('laos', 'LA', 'asia', 'Laos', 'Laos'),
    ('madagascar', 'MG', 'africa', 'Madagascar', 'Madagaskar'),
    ('gabon', 'GA', 'africa', 'Gabon', 'Gabon'),
    ('thailand', 'TH', 'asia', 'Thailand', 'Thailand'),
    ('venezuela', 'VE', 'south_america', 'Venezuela', 'Venezuela'),
    ('dominican_republic', 'DO', 'south_america', 'Dominican Republic', 'Dominikanische Republik'),
    ('haiti', 'HT', 'south_america', 'Haiti', 'Haiti'),
    ('congo', 'CG', 'africa', 'Congo', 'Kongo'),
    ('rwanda', 'RW', 'africa', 'Rwanda', 'Ruanda'),
    ('burundi', 'BI', 'africa', 'Burundi', 'Burundi'),
    ('philippines', 'PH', 'asia', 'Philippines', 'Philippinen'),
    ('togo', 'TG', 'africa', 'Togo', 'Togo'),
    ('guinea', 'GN', 'africa', 'Guinea', 'Guinea'),
    ('yemen', 'YE', 'asia', 'Yemen', 'Yemen'),
    ('cuba', 'CU', 'south_america', 'Cuba', 'Kuba'),
    ('panama', 'PA', 'south_america', 'Panama', 'Panama'),
    ('bolivia', 'BO', 'south_america', 'Bolivia', 'Bolivien'),
    ('central_african_republic', 'CF', 'africa', 'Central African Republic', 'Zentralafrikanische Republik'),
    ('nigeria', 'NG', 'africa', 'Nigeria', 'Nigeria'),
    ('ghana', 'GH', 'africa', 'Ghana', 'Ghana'),
    ('sierra_leone', 'SL', 'africa', 'Sierra Leone', 'Sierra Leone'),
    ('jamaica', 'JM', 'south_america', 'Jamaica', 'Jamaika'),
    ('paraguay', 'PY', 'south_america', 'Paraguay', 'Paraguay'),
    ('malawi', 'MW', 'africa', 'Malawi', 'Malawi'),
    ('trinidad_tobago', 'TT', 'africa', 'Trinidad and Tobago', 'Trinidad und Tobago'),
    ('zimbabwe', 'ZW', 'africa', 'Zimbabwe', 'Zimbabwe'),
    ('liberia', 'LR', 'africa', 'Liberia', 'Liberia'),
    ('zambia', 'ZM', 'africa', 'Zambia', 'Zambia'),
    # some countries I expect roasters to join
    ('usa', 'US', 'north_america', 'United States of America', 'Vereinigte Staaten von Amerika'),
    ('canada', 'CA', 'north_america', 'Canada', 'Kanada'),
    ('britain', 'BG', 'europe', 'Great Britain', 'Großbritannien'),
    ('ireland', 'IE', 'europe', 'Ireland', 'Irland'),
    ('germany', 'DE', 'europe', 'Germany', 'Deutschland'),
    ('france', 'FR', 'europe', 'France', 'Frankreich'),
    ('spain', 'ES', 'europe', 'Spain', 'Spanien'),
    ('portugal', 'PT', 'europe', 'Portugal', 'Portugal'),
    ('italy', 'IT', 'europe', 'Italy', 'Italien'),
    ('netherlands', 'NL', 'europe', 'Netherland', 'Niederlande'),
    ('belgium', 'BE', 'europe', 'Belgium', 'Belgien'),
    ('swiss', 'CH', 'europe', 'Switzerland', 'Schweiz'),
    ('austria', 'AT', 'europe', 'Austria', 'Österreich'),
    ('slovenia', 'SI', 'europe', 'Slovenia', 'Slovenien'),
    ('slovakia', 'SK', 'europe', 'Slovakia', 'Slovakei'),
    ('hungary', 'HU', 'europe', 'Hungary', 'Ungarn'),
    ('czechya', 'CZ', 'europe', 'Czechya', 'Tschechien'),
    ('poland', 'PL', 'europe', 'Poland', 'Polen'),
    ('denmark', 'DK', 'europe', 'Denmark', 'Dänemark'),
    ('sweden', 'SE', 'europe', 'Sweden', 'Schweden'),
    ('norway', 'NO', 'europe', 'Norway', 'Norwegen'),
    ('finland', 'FI', 'europe', 'Finland', 'Finland'),
    ('japan', 'JP', 'asia', 'Japan', 'Japan'),
    ('singapore', 'SG', 'asia', 'Singapore', 'Singapur')
)

def upgrade():
    meta = sa.MetaData(bind=op.get_bind())
    meta.reflect()

    lang_table = sa.Table('language', meta)
    op.bulk_insert(lang_table,
        [
            {'code':'EN'},
            {'code':'DE'}
        ]
    )
    cont_table =  sa.Table('continent', meta)
    op.bulk_insert(cont_table,
        [
            {'name':'africa'},
            {'name':'asia'},
            {'name':'europe'},
            {'name':'north_america'},
            {'name':'south_america'},
            {'name':'oceania'},
        ]
    )
    cont_i18n_table =  sa.Table('continent_translation', meta)
    op.bulk_insert(cont_i18n_table,
        [
            {'continent':'africa', 'language':'EN', 'value':'Africa'},
            {'continent':'africa', 'language':'DE', 'value':'Afrika'},
            {'continent':'asia', 'language':'EN', 'value':'Asia'},
            {'continent':'asia', 'language':'DE', 'value':'Asien'},
            {'continent':'europe', 'language':'EN', 'value':'Europe'},
            {'continent':'europe', 'language':'DE', 'value':'Europa'},
            {'continent':'north_america', 'language':'EN', 'value':'North America'},
            {'continent':'north_america', 'language':'DE', 'value':'Nordamerika'},
            {'continent':'south_america', 'language':'EN', 'value':'South America'},
            {'continent':'south_america', 'language':'DE', 'value':'Südamerika'},
            {'continent':'oceania', 'language':'EN', 'value':'Oceania'},
            {'continent':'oceania', 'language':'DE', 'value':'Australien und Ozeanien'}
        ]
    )

    countryTable =  sa.Table('country', meta)
    countryList = []
    for c in countries:
        dct = {'name':c[0], 'continent':c[2]}
        countryList.append(dct)
    op.bulk_insert(countryTable, countryList)

    countryI18nTable =  sa.Table('country_translation', meta)
    countryI18nList = []
    for c in countries:
        dct1 = {'country':c[0], 'language':'EN', 'value':c[3]}
        dct2 = {'country':c[0], 'language':'DE', 'value':c[4]}
        countryI18nList.append(dct1)
        countryI18nList.append(dct2)
    op.bulk_insert(countryI18nTable, countryI18nList)

    countryCodeTable =  sa.Table('country_code', meta)
    countryCodeList = []
    for c in countries:
        dct = {'country':c[0], 'code':c[1]}
        countryCodeList.append(dct)
    op.bulk_insert(countryCodeTable, countryCodeList)


def downgrade():
    meta = sa.MetaData(bind=op.get_bind())
    meta.reflect()
    countryCodeTable =  sa.Table('country_code', meta)
    countryI18nTable =  sa.Table('country_translation', meta)
    countryTable =  sa.Table('country', meta)
    for c in countries:
        sa.delete(countryCodeTable).where(countryCodeTable.c.country == c[0])
        sa.delete(countryI18nTable).where(countryI18nTable.c.country == c[0])
        sa.delete(countryTable).where(countryTable.c.name == c[0])
    
    continents = (
        'africa',
        'asia',
        'europe',
        'north_america',
        'south_america',
        'oceania'
    )
    continentTable = sa.Table('continent', meta)
    continentI18nTable = sa.Table('continent_translation', meta)
    for c in continents:
        sa.delete(continentTable).where(continentTable.c.name == c)
        sa.delete(continentI18nTable).where(continentI18nTable.c.continent == c)
    
    languageTable = sa.Table('language', meta)
    sa.delete(languageTable).where(languageTable.c.code == 'EN')
    sa.delete(languageTable).where(languageTable.c.code == 'DE')
