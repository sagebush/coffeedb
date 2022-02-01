"""Add varietals

Revision ID: 076084c80c69
Revises: dc0a95a14146
Create Date: 2022-01-24 20:41:09.848413

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.expression import insert, delete


# revision identifiers, used by Alembic.
revision = '076084c80c69'
down_revision = 'dc0a95a14146'
branch_labels = None
depends_on = None

varietals = (
    ('abysinia', ('ethiopian_landrace',), 'Abysinia'),
    ('ababuna', ('ethiopian_landrace',), 'Ababuna'),
    ('acaia', ('mundo_novo',), 'Acaiá'),
    ('amarello', ('typica',), 'Amarello'),
    ('anacafe14', ('catimor', 'pacamara',), 'Anacafe 14'),
    ('arabica', (), 'Arabica'),
    ('arabigo', ('typica',), 'Arabigo'),
    ('arago', ('ethiopian_landrace',), 'Arago'),
    ('arla', ('t5296',), 'Arla'),
    ('arusha', ('bourbon',), 'Arusha'),
    ('andong_sari', ('ethiopian_landrace', 'colombia', 'caturra', 'timor',), 'Andong Sari'),
    ('ateng', ('t5296',), 'Ateng'),
    ('awada', ('ethiopian_landrace',), 'Awada'),
    ('batian', ('sl28', 'sl34', 'sudan_rume', 'n39', 'k7', 'sl4', 'timor',), 'Batian'),
    ('barako', ('liberica',), 'Barako'),
    ('bedessa', ('ethiopian_landrace',), 'Bedessa'),
    ('benguet', ('arabica',), 'Benguet'),
    ('bergundal', ('typica',), 'Bergundal'),
    ('bernardina', ('arabica',), 'Bernardina'),
    ('blawan_paumah', ('typica',), 'Blawa Paumah'),
    ('blue_mountain', ('typica',), 'Blue Mountain'),
    ('brutte', ('arabica',), 'Brutte'),
    ('bogor_prada', ('t5296',), 'Bogor Prada'),
    ('bm71', ('bourbon',), 'BM71'),
    ('bm139', ('bourbon',),  'BM139'),
    ('bonifieur', ('arabica',), 'Bonifieur'),
    ('bourbon', ('typica',), 'Bourbon'),
    ('bourbon_red', ('bourbon',), 'Red Bourbon'),
    ('bourbon_orange', ('bourbon',), 'Orange Bourbon'),
    ('bourbon_yellow', ('bourbon',), 'Yellow Bourbon'),
    ('bourbon_pink', ('bourbon',), 'Pink Bourbon'),
    ('bourbon_vermelho', ('bourbon',), 'Bourbon Vermelho'),
    ('canephora', (), 'Canephora'),
    ('casiopea', ('caturra', 'et41',), 'Casiopea'),
    ('catimor', ('caturra', 'timor832',), 'Catimor'),
    ('catimor129', ('caturra', 'timor1343',), 'Catimor 129'),
    ('catigua', ('catuai', 'timor',), 'Catigua'),
    ('catisic', ('catimor',), 'Catisic'),
    ('catrenic', ('t5296',), 'Catrenic'),
    ('catuai', ('caturra', 'mundo_novo',), 'Catuai'),
    ('catuai_yellow', ('catuai',), 'Yellow Catuai'),
    ('catuai_orange', ('catuai',), 'Orange Catuai'),
    ('caturra', ('bourbon',), 'Caturra'),
    ('cauvery', ('catimor',), 'Cauvery'),
    ('castillo', ('colombia', 'caturra',), 'Castillo'),
    ('cenicafe1', ('caturra', 'timor1343',), 'Cenicafé 1'),
    ('centroamericano', ('t5296', 'sudan_rume',), 'Centroamericano'),
    ('cera', ('bourbon',), 'Cera'),
    ('chandragiri', ('sarchimor',), 'Chandragiri'),
    ('cioccie', ('ethiopian_landrace',), 'Cioccie'),
    ('charrier', (), 'Charrier'),
    ('chickumalgur', ('typica',), 'Chickumalgur'),
    ('criollo', ('typica',),  'Criollo'),
    ('cuscatleco', ('t5296',), 'Cuscatleco'),
    ('colombia', ('catimor',), 'Colombia'),
    ('costa_rica_95', ('catimor',),  'Costa Rica 95'),
    ('dalle', ('ethiopian_landrace',), 'Dalle'),
    ('devamachy', ('arabica', 'robusta',), 'Devamachy'),
    ('dega', ('ethiopian_landrace',), 'Dega'),
    ('dilla_alghe', ('ethiopian_landrace',), 'Dilla Alghe'),
    ('djimma', ('ethiopian_landrace',), 'Djimma'),
    ('eugenioides', ('arabica', 'canephora',), 'Eugenioides'),
    ('excelsa', ('liberica',), 'Excelsa'),
    ('ethiopian_landrace', ('arabica',), 'ethiopian landrace'),
    ('evaluna', ('naryelis', 'et06',), 'Evaluna'),
    ('et01', ('ethiopian_landrace',),  'ET01'),
    ('et06', ('ethiopian_landrace',), 'ET06'),
    ('et26', ('ethiopian_landrace',), 'ET26'),
    ('et41', ('ethiopian_landrace',), 'ET41'),
    ('e531', ('ethiopian_landrace',), 'E531'),
    ('ennarea', ('ethiopian_landrace',), 'Ennarea'),
    ('frontron', ('catimor',),  'Frontron'),
    ('garnica', ('mundo_novo', 'caturra',), 'Garnica'),
    ('garundang', ('typica',), 'Garundang'),
    ('gawe', ('ethiopian_landrace',), 'Gawe'),
    ('gera', ('ethiopian_landrace',), 'Gera'),
    ('gesha', ('ethiopian_landrace',), 'Gesha'),
    ('ghimbi', ('ethiopian_landrace',), 'Ghimbi'),
    ('h3', ('caturra', 'e531',), 'H3'),
    ('harrar', ('ethiopian_landrace',), 'Harrar'),
    ('haru', ('ethiopian_landrace',), 'Haru'),
    ('iacl25', ('villa_sarchi', 'timor'), 'IACL25'),
    ('iapar59', ('t5296',), 'IAPAR59'),
    ('ibairi', ('bourbon',),  'Ibairi'),
    ('icatu', ('bourbon_vermelho', 'robusta', 'mundo_novo',), 'Icatú'),
    ('ihcafe90', ('catimor',), 'IHCAFE90'),
    ('ipar103', ('t5296',), 'Ipar103'),
    ('jackson', ('bourbon',), 'Jackson'),
    ('jarc74110', ('ethiopian_landrace',), '74110'),
    ('jarc74112', ('ethiopian_landrace',), '74112'),
    ('jarc74158', ('ethiopian_landrace',), '74158'),
    ('jarc74160', ('ethiopian_landrace',), '74160'),
    ('java', ('ethiopian_landrace',), 'Java'),
    ('jember', ('kent', 's288',),  'Jember'),
    ('k7', ('typica',), 'K7'),
    ('k20', ('typica',), 'K20'),
    ('kahawa_sug', ('robusta',), 'Kahawa Sūg'),
    ('kent', ('typica',), 'Kent'),
    ('kp423', ('kent',), 'KP423'),
    ('kona', ('typica',), 'Kona'),
    ('kurume', ('ethiopian_landrace',), 'Kurume'),
    ('laurina', ('bourbon',), 'Lauriña'),
    ('lempira', ('catimor',), 'Lempira'),
    ('liberica', (), 'Liberica'),
    ('limani', ('t5296',), 'Limani'),
    ('mandela', ('caturra',), 'Mandela'),
    ('maragogype', ('typica',), 'Maragogype'),
    ('maracaturra', ('caturra', 'maragogype',), 'Maracaturra'),
    ('maragesha', ('gesha', 'maragogype'), 'Maragesha'),
    ('marsellsa', ('t5296',), 'Marsellsa'),
    ('mayaguez', ('bourbon',), 'Mayaguez 139'),
    ('mechara', ('ethiopian_landrace',), 'Mechara'),
    ('melka', ('ethiopian_landrace',), 'Melka'),
    ('melko_ch2', ('ethiopian_landrace',), 'Melko CH2'),
    ('mettu', ('ethiopian_landrace',), 'Mettu'),
    ('mibirizi', ('typica',), 'Mibirizi'),
    ('milenio', ('t5296', 'sudan_rume',), 'Milenio'),
    ('miqe', ('ethiopian_landrace',), 'Miqe'),
    ('mokha', ('bourbon',), 'Mokha'),
    ('mundo_maya', ('t5296', 'et01',), 'Mundo Maya'),
    ('mundo_novo', ('bourbon', 'typica',), 'Mundo Novo'),
    ('mugi', ('ethiopian_landrace',), 'Mugi'),
    ('nganda', ('canephora',), 'Nganda'),
    ('nayarita', ('naryelis', 'et26',),  'Nayarita'),
    ('naryelis', ('catimor',), 'Naryelis'),
    ('nemaya', ('robusta',),  'Nemaya'),
    ('nyasaland', ('typica',), 'Nyasaland'),
    ('n39', ('bourbon',), 'N39'),
    ('obata', ('t5296',), 'Obata Rojo'),
    ('oro_azteca', ('t5296',), 'Oro Azteca'),
    ('ouro', ('typica', 'bourbon',), 'Ouro'),
    ('pacamara', ('pacas', 'maragogype',), 'Pacamara'),
    ('pacas', ('bourbon',), 'Pacas'),
    ('pache_colis', ('caturra', 'pache',), 'Pache Colis'),
    ('pache', ('typica',), 'Pache'),
    ('parainema', ('t5296',), 'Parainema'),
    ('paraiso', ('t5296',), 'Paraiso'),
    ('papayo', ('ethiopian_landrace',), 'Papayo'),
    ('pop3303', ('blue_mountain',), 'Pop3303'),
    ('pluma_hidalgo', ('typica',), 'Pluma Hidalgo'),
    ('rab_c15', ('kent', 'robusta',), 'Rab C15'),
    ('rambung', ('ethiopian_landrace',), 'Rambung'),
    ('rasuna', ('typica', 'catimor',), 'Rasuna'),
    ('rubi', ('bourbon', 'typica',), 'Rubi'),
    ('ruiru11', ('catimor', 'k7', 'sl28', 'n39', 'sudan_rume',), 'Ruiru11'),
    ('robusta', ('canephora',), 'Robusta'),
    ('s288', ('arabica', 'liberica',), 'S288'),
    ('s795', ('arabica', 'liberica',), 'S795'),
    ('sagada', ('arabica',), 'Sagada'),
    ('santos', ('bourbon',), 'Santos'),
    ('san_bernando', ('typica',), 'Sao Bernando'),
    ('san_ramon', ('typica',), 'San Ramón'),
    ('sarchimor', ('timor832', 'villa_sarchi',), 'Sarchimor'),
    ('sawa', ('ethiopian_landrace',), 'Sawa'),
    ('semperflores', ('bourbon',), 'Semperflores'),
    ('sidamo', ('ethiopian_landrace',), 'Sidamo'),
    ('sidikalang', ('typica',), 'Sidikalang'),
    ('sidra', ('typica', 'bourbon',), 'Sidra'),
    ('sigarar_utang', ('ateng', 'timor', 'bourbon',), 'Sigarar Utang'),
    ('sl4', ('arago', 'tafari_kela', 'cioccie',), 'SL4'),
    ('sl6', ('kent', 'canephora',), 'SL6'),
    ('sl7', ('san_ramon', 's795', 'arago', 'timor',), 'SL7'),
    ('sl9', ('tafari_kela', 'timor',), 'SL9'),
    ('sl10', ('caturra', 'cioccie', 's795',), 'SL10'),
    ('sl14', ('typica',), 'SL14'),
    ('sl28', ('bourbon',), 'SL28'),
    ('sl34', ('typica',),  'SL34'),
    ('s228', ('liberica', 'ethiopian_landrace'), 'S228'),
    ('starmaya', ('marsellsa', 'ethiopian_landrace',), 'Starmaya'),
    ('sudan_rume', ('ethiopian_landrace',), 'Sudan Rume'),
    ('sudan_barbuk', ('ethiopian_landrace',), 'Sudan Barbuk'),
    ('sulawesi_toraja', ('s795',), 'Sulawesi Toraja'),
    ('t5175', ('timor832', 'caturra',), 'T5175'),
    ('t5296', ('timor832', 'villa_sarchi',), 'T5296'),
    ('t8667', ('caturra', 'timor832',), 'T8667'),
    ('tabi', ('t5296',), 'Tabi'),
    ('tafari_kela', ('ethiopian_landrace',), 'Tafari Kela'),
    ('tanganyika', ('bourbon',), 'Tanganyika'),
    ('tegu', ('ethiopian_landrace',), 'Tegu'),
    ('tekisic', ('bourbon',), 'Tekisic'),
    ('timor', ('arabica', 'robusta',), 'Timor'),
    ('timor1343', ('timor',), 'Timor 1343'),
    ('timor832', ('timor',), 'Timor 832'),
    ('topazio', ('mundo_novo', 'catuai',), 'Topazio'),
    ('tupi', ('t5296',), 'Tupi'),
    ('typica', ('ethiopian_landrace',), 'Typica'),
    ('usda762', ('ethiopian_landrace',), 'USDA 762'),
    ('villa_sarchi', ('bourbon',), 'Villa Sarchi'),
    ('villalobos', ('typica',), 'Villalobos'),
    ('venecia', ('bourbon',), 'Venecia'),
    ('wellaga', ('ethiopian_landrace',), 'Wellaga'),
    ('wenago', ('ethiopian_landrace',), 'Wenago'),
    ('wolisho', ('ethiopian_landrace',), 'Wolisho'),
    ('yellow_bourbon', ('bourbon',), 'Yellow Bourbon'),
    ('yirgacheffe', ('ethiopian_landrace',), 'Yirgacheffe'),
)


def upgrade():
    meta = sa.MetaData(bind=op.get_bind())
    meta.reflect()

    varTable =  sa.Table('variety', meta)
    #insertIntoVar = []
    for var in varietals:
        #insertIntoVar.append({'name': var[0], 'display_name':var[2]})
        op.execute(insert(varTable).values(name=var[0], display_name=var[2]))
    #op.bulk_insert(varTable, insertIntoVar)

    varInheritTable =  sa.Table('variety_inheritance', meta)
    #insertIntoVarInherit = []
    for var in varietals:
        if len(var[1]) > 0:
            for parent in var[1]:
                #insertIntoVarInherit.append({'child':var[0], 'parent':parent})
                op.execute(insert(varInheritTable).values(child=var[0], parent=parent))
    #op.bulk_insert(varInheritTable, insertIntoVarInherit)

def downgrade():
    meta = sa.MetaData(bind=op.get_bind())
    meta.reflect()

    varTable =  sa.Table('variety', meta)
    for var in varietals:
        op.execute(delete(varTable).where(varTable.c.name == var[0]))

    varInheritTable =  sa.Table('variety_inheritance', meta)
    for var in varietals:
        op.execute(delete(varInheritTable).where(varInheritTable.c.child == var[0]))
