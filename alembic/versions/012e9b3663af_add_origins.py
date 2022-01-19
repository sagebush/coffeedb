"""Add origins

Revision ID: 012e9b3663af
Revises: 377df7490195
Create Date: 2022-01-12 21:58:54.149244

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.expression import insert, delete


# revision identifiers, used by Alembic.
revision = '012e9b3663af'
down_revision = '48b0a70aecc0'
branch_labels = None
depends_on = None

continents = (
    ('africa', 'Africa', 'Afrika'),
    ('asia', 'Asia', 'Asien'),
    ('europe', 'Europe', 'Europa'),
    ('north_america', 'North America', 'Nordamerika'),
    ('south_america', 'South America', 'Südamerika'),
    ('oceania', 'Oceania', 'Australien und Ozeanien'),
)
countries = (
    # the worlds largest coffee producers
    ('brazil', 'BR', 'south_america', 'Brazil', 'Brazilien', True),
    ('vietnam', 'VN', 'asia', 'Vietnam', 'Vietnam', True),
    ('colombia', 'CO', 'south_america', 'Colombia', 'Columbien', True),
    ('indonesia', 'ID', 'asia', 'Indonesia', 'Indonesien', True),
    ('ethiopia', 'ET', 'africa', 'Ethiopia', 'Äthiopien', True),
    ('honduras', 'HN', 'south_america', 'Honduras', 'Honduras', True),
    ('india', 'IN', 'asia', 'India', 'Indien', True),
    ('uganda', 'UG', 'africa', 'Uganda', 'Uganda', True),
    ('mexico', 'MX', 'south_america', 'Mexico', 'Mexico', True),
    ('guatemala', 'GT', 'south_america', 'Guatemala', 'Guatemala', True),
    ('peru', 'PE', 'south_america', 'Peru', 'Peru', True),
    ('nicaragua', 'NI', 'south_america', 'Nicaragua', 'Nicaragua', True),
    ('china', 'CN', 'asia', 'China', 'China', True),
    ('ivory_coast', 'CI', 'africa', 'Ivory Coast', 'Elfenbeinküste', True),
    ('costa_rica', 'CR', 'south_america', 'Costa Rica', 'Costa Rica', True),
    ('kenya', 'KE', 'africa', 'Kenya', 'Kenya', True),
    ('papua_new_guinea', 'PG', 'oceania', 'Papua New Guinea', 'Papua Neu Guinea', True),
    ('tanzania', 'TZ', 'africa', 'Tanzania', 'Tanzania', True),
    ('el_salvador', 'SV', 'south_america', 'El Salvador', 'El Salvador', True),
    ('ecuador', 'EC', 'south_america', 'Ecuador', 'Ecuador', True),
    ('cameroon', 'CM', 'africa', 'Cameroon', 'Kamerun', True),
    ('laos', 'LA', 'asia', 'Laos', 'Laos', True),
    ('madagascar', 'MG', 'africa', 'Madagascar', 'Madagaskar', True),
    ('gabon', 'GA', 'africa', 'Gabon', 'Gabon', True),
    ('thailand', 'TH', 'asia', 'Thailand', 'Thailand', True),
    ('venezuela', 'VE', 'south_america', 'Venezuela', 'Venezuela', True),
    ('dominican_republic', 'DO', 'south_america', 'Dominican Republic', 'Dominikanische Republik', True),
    ('haiti', 'HT', 'south_america', 'Haiti', 'Haiti', True),
    ('congo', 'CG', 'africa', 'Congo', 'Kongo', True),
    ('rwanda', 'RW', 'africa', 'Rwanda', 'Ruanda', True),
    ('burundi', 'BI', 'africa', 'Burundi', 'Burundi', True),
    ('philippines', 'PH', 'asia', 'Philippines', 'Philippinen', True),
    ('togo', 'TG', 'africa', 'Togo', 'Togo', True),
    ('guinea', 'GN', 'africa', 'Guinea', 'Guinea', True),
    ('yemen', 'YE', 'asia', 'Yemen', 'Yemen', True),
    ('cuba', 'CU', 'south_america', 'Cuba', 'Kuba', True),
    ('panama', 'PA', 'south_america', 'Panama', 'Panama', True),
    ('bolivia', 'BO', 'south_america', 'Bolivia', 'Bolivien', True),
    ('central_african_republic', 'CF', 'africa', 'Central African Republic', 'Zentralafrikanische Republik', True),
    ('nigeria', 'NG', 'africa', 'Nigeria', 'Nigeria', True),
    ('ghana', 'GH', 'africa', 'Ghana', 'Ghana', True),
    ('sierra_leone', 'SL', 'africa', 'Sierra Leone', 'Sierra Leone', True),
    ('jamaica', 'JM', 'south_america', 'Jamaica', 'Jamaika', True),
    ('paraguay', 'PY', 'south_america', 'Paraguay', 'Paraguay', True),
    ('malawi', 'MW', 'africa', 'Malawi', 'Malawi', True),
    ('trinidad_tobago', 'TT', 'africa', 'Trinidad and Tobago', 'Trinidad und Tobago', True),
    ('zimbabwe', 'ZW', 'africa', 'Zimbabwe', 'Zimbabwe', True),
    ('liberia', 'LR', 'africa', 'Liberia', 'Liberia', True),
    ('zambia', 'ZM', 'africa', 'Zambia', 'Zambia', True),
    # some countries I expect roasters to join
    ('usa', 'US', 'north_america', 'United States of America', 'Vereinigte Staaten von Amerika', False),
    ('canada', 'CA', 'north_america', 'Canada', 'Kanada', False),
    ('britain', 'BG', 'europe', 'Great Britain', 'Großbritannien', False),
    ('ireland', 'IE', 'europe', 'Ireland', 'Irland', False),
    ('germany', 'DE', 'europe', 'Germany', 'Deutschland', False),
    ('france', 'FR', 'europe', 'France', 'Frankreich', False),
    ('spain', 'ES', 'europe', 'Spain', 'Spanien', False),
    ('portugal', 'PT', 'europe', 'Portugal', 'Portugal', False),
    ('italy', 'IT', 'europe', 'Italy', 'Italien', False),
    ('netherlands', 'NL', 'europe', 'Netherland', 'Niederlande', False),
    ('belgium', 'BE', 'europe', 'Belgium', 'Belgien', False),
    ('swiss', 'CH', 'europe', 'Switzerland', 'Schweiz', False),
    ('austria', 'AT', 'europe', 'Austria', 'Österreich', False),
    ('slovenia', 'SI', 'europe', 'Slovenia', 'Slovenien', False),
    ('slovakia', 'SK', 'europe', 'Slovakia', 'Slovakei', False),
    ('hungary', 'HU', 'europe', 'Hungary', 'Ungarn', False),
    ('czechya', 'CZ', 'europe', 'Czechya', 'Tschechien', False),
    ('poland', 'PL', 'europe', 'Poland', 'Polen', False),
    ('denmark', 'DK', 'europe', 'Denmark', 'Dänemark', False),
    ('sweden', 'SE', 'europe', 'Sweden', 'Schweden', False),
    ('norway', 'NO', 'europe', 'Norway', 'Norwegen', False),
    ('finland', 'FI', 'europe', 'Finland', 'Finland', False),
    ('japan', 'JP', 'asia', 'Japan', 'Japan', False),
    ('singapore', 'SG', 'asia', 'Singapore', 'Singapur', False)
)
languageCodes = ('EN', 'DE')


def upgrade():
    meta = sa.MetaData(bind=op.get_bind())
    meta.reflect()

    langTable = sa.Table('language', meta)
    for lc in languageCodes:
        op.execute(insert(langTable).values(code=lc))
        
    contTable =  sa.Table('continent', meta)
    contI18nTable = sa.Table('continent_translation', meta)
    for cont in continents:
        op.execute(insert(contTable).values(name=cont[0]))
        op.execute(insert(contI18nTable).values(continent_name=cont[0], language_code='EN', value=cont[1]))
        op.execute(insert(contI18nTable).values(continent_name=cont[0], language_code='DE', value=cont[2]))

    countryTable =  sa.Table('country', meta)
    countryI18nTable =  sa.Table('country_translation', meta)
    countryCodeTable =  sa.Table('country_code', meta)
    for c in countries:
        op.execute(insert(countryTable).values(name=c[0], continent_name=c[2], is_producer=c[5]))
        op.execute(insert(countryI18nTable).values(country_name=c[0], language_code='EN', value=c[3]))
        op.execute(insert(countryI18nTable).values(country_name=c[0], language_code='DE', value=c[4]))
        op.execute(insert(countryCodeTable).values(country_name=c[0], code=c[1]))


def downgrade():
    meta = sa.MetaData(bind=op.get_bind())
    meta.reflect()

    countryCodeTable =  sa.Table('country_code', meta)
    countryI18nTable =  sa.Table('country_translation', meta)
    countryTable =  sa.Table('country', meta)
    for c in countries:
        op.execute(delete(countryCodeTable).where(countryCodeTable.c.country_name == c[0]))
        op.execute(delete(countryI18nTable).where(countryI18nTable.c.country_name == c[0]))
        op.execute(delete(countryTable).where(countryTable.c.name == c[0]))
    
    continentTable = sa.Table('continent', meta)
    continentI18nTable = sa.Table('continent_translation', meta)
    for c in continents:
        op.execute(delete(continentTable).where(continentTable.c.name == c[0]))
        op.execute(delete(continentI18nTable).where(continentI18nTable.c.continent_name == c[0]))
    
    languageTable = sa.Table('language', meta)
    for lang in languageCodes:
        op.execute(delete(languageTable).where(languageTable.c.code == lang))
