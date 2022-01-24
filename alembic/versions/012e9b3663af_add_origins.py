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
    ('brazil', 'BR', 'south_america', 'Brazil', 'Brazilien', True, False),
    ('vietnam', 'VN', 'asia', 'Vietnam', 'Vietnam', True, False),
    ('colombia', 'CO', 'south_america', 'Colombia', 'Kolumbien', True, False),
    ('indonesia', 'ID', 'asia', 'Indonesia', 'Indonesien', True, False),
    ('ethiopia', 'ET', 'africa', 'Ethiopia', 'Äthiopien', True, False),
    ('honduras', 'HN', 'south_america', 'Honduras', 'Honduras', True, False),
    ('india', 'IN', 'asia', 'India', 'Indien', True, False),
    ('uganda', 'UG', 'africa', 'Uganda', 'Uganda', True, False),
    ('mexico', 'MX', 'south_america', 'Mexico', 'Mexico', True, False),
    ('guatemala', 'GT', 'south_america', 'Guatemala', 'Guatemala', True, False),
    ('peru', 'PE', 'south_america', 'Peru', 'Peru', True, False),
    ('nicaragua', 'NI', 'south_america', 'Nicaragua', 'Nicaragua', True, False),
    ('china', 'CN', 'asia', 'China', 'China', True, False),
    ('ivory_coast', 'CI', 'africa', 'Ivory Coast', 'Elfenbeinküste', True, False),
    ('costa_rica', 'CR', 'south_america', 'Costa Rica', 'Costa Rica', True, False),
    ('kenya', 'KE', 'africa', 'Kenya', 'Kenya', True, False),
    ('papua_new_guinea', 'PG', 'oceania', 'Papua New Guinea', 'Papua Neu Guinea', True, False),
    ('tanzania', 'TZ', 'africa', 'Tanzania', 'Tanzania', True, False),
    ('el_salvador', 'SV', 'south_america', 'El Salvador', 'El Salvador', True, False),
    ('ecuador', 'EC', 'south_america', 'Ecuador', 'Ecuador', True, False),
    ('cameroon', 'CM', 'africa', 'Cameroon', 'Kamerun', True, False),
    ('laos', 'LA', 'asia', 'Laos', 'Laos', True, False),
    ('madagascar', 'MG', 'africa', 'Madagascar', 'Madagaskar', True, False),
    ('gabon', 'GA', 'africa', 'Gabon', 'Gabon', True, False),
    ('thailand', 'TH', 'asia', 'Thailand', 'Thailand', True, False),
    ('venezuela', 'VE', 'south_america', 'Venezuela', 'Venezuela', True, False),
    ('dominican_republic', 'DO', 'south_america', 'Dominican Republic', 'Dominikanische Republik', True, False),
    ('haiti', 'HT', 'south_america', 'Haiti', 'Haiti', True, False),
    ('congo', 'CG', 'africa', 'Congo', 'Kongo', True, False),
    ('rwanda', 'RW', 'africa', 'Rwanda', 'Ruanda', True, False),
    ('burundi', 'BI', 'africa', 'Burundi', 'Burundi', True, False),
    ('philippines', 'PH', 'asia', 'Philippines', 'Philippinen', True, False),
    ('togo', 'TG', 'africa', 'Togo', 'Togo', True, False),
    ('guinea', 'GN', 'africa', 'Guinea', 'Guinea', True, False),
    ('yemen', 'YE', 'asia', 'Yemen', 'Yemen', True, False),
    ('cuba', 'CU', 'south_america', 'Cuba', 'Kuba', True, False),
    ('panama', 'PA', 'south_america', 'Panama', 'Panama', True, False),
    ('bolivia', 'BO', 'south_america', 'Bolivia', 'Bolivien', True, False),
    ('central_african_republic', 'CF', 'africa', 'Central African Republic', 'Zentralafrikanische Republik', True, False),
    ('nigeria', 'NG', 'africa', 'Nigeria', 'Nigeria', True, False),
    ('ghana', 'GH', 'africa', 'Ghana', 'Ghana', True, False),
    ('sierra_leone', 'SL', 'africa', 'Sierra Leone', 'Sierra Leone', True, False),
    ('jamaica', 'JM', 'south_america', 'Jamaica', 'Jamaika', True, False),
    ('paraguay', 'PY', 'south_america', 'Paraguay', 'Paraguay', True, False),
    ('malawi', 'MW', 'africa', 'Malawi', 'Malawi', True, False),
    ('trinidad_tobago', 'TT', 'africa', 'Trinidad and Tobago', 'Trinidad und Tobago', True, False),
    ('zimbabwe', 'ZW', 'africa', 'Zimbabwe', 'Zimbabwe', True, False),
    ('liberia', 'LR', 'africa', 'Liberia', 'Liberia', True, False),
    ('zambia', 'ZM', 'africa', 'Zambia', 'Zambia', True, False),
    # some countries I expect roasters to join
    ('usa', 'US', 'north_america', 'United States of America', 'Vereinigte Staaten von Amerika', False, True),
    ('canada', 'CA', 'north_america', 'Canada', 'Kanada', False, True),
    ('britain', 'BG', 'europe', 'Great Britain', 'Großbritannien', False, True),
    ('ireland', 'IE', 'europe', 'Ireland', 'Irland', False, True),
    ('germany', 'DE', 'europe', 'Germany', 'Deutschland', False, True),
    ('france', 'FR', 'europe', 'France', 'Frankreich', False, True),
    ('spain', 'ES', 'europe', 'Spain', 'Spanien', False, True),
    ('portugal', 'PT', 'europe', 'Portugal', 'Portugal', False, True),
    ('italy', 'IT', 'europe', 'Italy', 'Italien', False, True),
    ('netherlands', 'NL', 'europe', 'Netherland', 'Niederlande', False, True),
    ('belgium', 'BE', 'europe', 'Belgium', 'Belgien', False, True),
    ('swiss', 'CH', 'europe', 'Switzerland', 'Schweiz', False, True),
    ('austria', 'AT', 'europe', 'Austria', 'Österreich', False, True),
    ('slovenia', 'SI', 'europe', 'Slovenia', 'Slovenien', False, True),
    ('slovakia', 'SK', 'europe', 'Slovakia', 'Slovakei', False, True),
    ('hungary', 'HU', 'europe', 'Hungary', 'Ungarn', False, True),
    ('czechya', 'CZ', 'europe', 'Czechya', 'Tschechien', False, True),
    ('poland', 'PL', 'europe', 'Poland', 'Polen', False, True),
    ('denmark', 'DK', 'europe', 'Denmark', 'Dänemark', False, True),
    ('sweden', 'SE', 'europe', 'Sweden', 'Schweden', False, True),
    ('norway', 'NO', 'europe', 'Norway', 'Norwegen', False, True),
    ('finland', 'FI', 'europe', 'Finland', 'Finland', False, True),
    ('japan', 'JP', 'asia', 'Japan', 'Japan', False, True),
    ('singapore', 'SG', 'asia', 'Singapore', 'Singapur', False, True)
)
languageCodes = ('en', 'de')

language_tn = 'language'
continent_tn = 'continent'
continentTransl_tn = 'continent_translation'
country_tn = 'country'
coutryRoles_tn = 'country_roles'
country_transl_tn = 'country_translation'
countryCode_tn = 'country_code'


def upgrade():
    meta = sa.MetaData(bind=op.get_bind())
    meta.reflect()

    langTable = sa.Table(language_tn, meta)
    for lc in languageCodes:
        op.execute(insert(langTable).values(code=lc))
        
    contTable =  sa.Table(continent_tn, meta)
    contI18nTable = sa.Table(continentTransl_tn, meta)
    for cont in continents:
        op.execute(insert(contTable).values(name=cont[0]))
        op.execute(insert(contI18nTable).values(continent_name=cont[0], language_code='en', value=cont[1]))
        op.execute(insert(contI18nTable).values(continent_name=cont[0], language_code='de', value=cont[2]))

    countryTable =  sa.Table(country_tn, meta)
    countryRoleTable =  sa.Table(coutryRoles_tn, meta)
    countryI18nTable =  sa.Table(country_transl_tn, meta)
    countryCodeTable =  sa.Table(countryCode_tn, meta)
    for c in countries:
        op.execute(insert(countryTable).values(name=c[0], continent_name=c[2]))
        op.execute(insert(countryRoleTable).values(country_name=c[0], has_producer=c[5], has_roaster=c[6]))
        op.execute(insert(countryI18nTable).values(country_name=c[0], language_code='en', value=c[3]))
        op.execute(insert(countryI18nTable).values(country_name=c[0], language_code='de', value=c[4]))
        op.execute(insert(countryCodeTable).values(country_name=c[0], code=c[1]))


def downgrade():
    meta = sa.MetaData(bind=op.get_bind())
    meta.reflect()

    countryRoleTable =  sa.Table(coutryRoles_tn, meta)
    countryCodeTable =  sa.Table(countryCode_tn, meta)
    countryI18nTable =  sa.Table(country_transl_tn, meta)
    countryTable =  sa.Table(country_tn, meta)
    for c in countries:
        op.execute(delete(countryCodeTable).where(countryCodeTable.c.country_name == c[0]))
        op.execute(delete(countryI18nTable).where(countryI18nTable.c.country_name == c[0]))
        op.execute(delete(countryRoleTable).where(countryTable.c.name == c[0]))
        op.execute(delete(countryTable).where(countryTable.c.name == c[0]))
    
    continentTable = sa.Table(continent_tn, meta)
    continentI18nTable = sa.Table(continentTransl_tn, meta)
    for c in continents:
        op.execute(delete(continentI18nTable).where(continentI18nTable.c.continent_name == c[0]))
        op.execute(delete(continentTable).where(continentTable.c.name == c[0]))
    
    languageTable = sa.Table(language_tn, meta)
    for lang in languageCodes:
        op.execute(delete(languageTable).where(languageTable.c.code == lang))
