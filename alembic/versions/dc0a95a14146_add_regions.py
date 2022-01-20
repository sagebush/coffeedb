"""Add regions

Revision ID: dc0a95a14146
Revises: cc716f6a7d94
Create Date: 2022-01-19 23:29:19.167649

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.expression import insert, delete


# revision identifiers, used by Alembic.
revision = 'dc0a95a14146'
down_revision = 'cc716f6a7d94'
branch_labels = None
depends_on = None

regions = (
    ('brazil', 'other', ''),
    ('brazil', 'cerrado', ''),
    ('brazil', 'mogiana', ''),
    ('brazil', 'matas_de_minas', ''),
    ('brazil', 'sul_de_minas', ''),
    ('brazil', 'chapadas_de_minas', ''),
    ('brazil', 'sao_paulo', ''),
    ('brazil', 'espirito_santo', ''),
    ('brazil', 'bahia', ''),
    ('brazil', 'parana', ''),
    ('vietnam', 'other', ''),
    ('vietnam', 'dak_lak', ''),
    ('vietnam', 'gia_lai', ''),
    ('vietnam', 'dak_nong', ''),
    ('vietnam', 'lam_dong', ''),
    ('vietnam', 'kontum', ''),
    ('colombia', 'other', ''),
    ('colombia', 'antioquia', ''),
    ('colombia', 'arauca', ''),
    ('colombia', 'boyaca', ''),
    ('colombia', 'caldas', ''),
    ('colombia', 'casanare', ''),
    ('colombia', 'caqueta', ''),
    ('colombia', 'cauca', ''),
    ('colombia', 'cesar', ''),
    ('colombia', 'choco', ''),
    ('colombia', 'cundinamarca', ''),
    ('colombia', 'huila', ''),
    ('colombia', 'la_guajira', ''),
    ('colombia', 'magdalena', ''),
    ('colombia', 'meta', ''),
    ('colombia', 'narino', ''),
    ('colombia', 'quindio', ''),
    ('colombia', 'risaralda', ''),
    ('colombia', 'santander', ''),
    ('colombia', 'tolima', ''),
    ('colombia', 'valle_del_cauca', ''),
    ('indonesia', 'other', ''),
    ('indonesia', 'bali', ''),
    ('indonesia', 'sumatra', ''),
    ('indonesia', 'sulawesi', ''),
    ('indonesia', 'java', ''),
    ('indonesia', 'timor', ''),
    ('indonesia', 'papua', ''),
    ('ethiopia', 'other', ''),
    ('ethiopia', 'yirgacheffe', ''),
    ('ethiopia', 'sidamo', ''),
    ('ethiopia', 'harrar', ''),
    ('ethiopia', 'bebeka', ''),
    ('ethiopia', 'teppi', ''),
    ('ethiopia', 'limu', ''),
    ('ethiopia', 'djimma', ''),
    ('ethiopia', 'illubabor', ''),
    ('ethiopia', 'lekempti', ''),
    ('ethiopia', 'wellega', ''),
    ('ethiopia', 'gimbi', ''),
    ('ethiopia', 'guji', ''),
    ('ethiopia', 'illubabor', ''),
    ('ethiopia', 'amaro', ''),
    ('ethiopia', 'kaffa', ''),
    ('ethiopia', 'tepi', ''),
    ('ethiopia', 'welayta', ''),
    ('ethiopia', 'bebeka', ''),
    ('ethiopia', 'borena', ''),
    ('ethiopia', 'arsi', ''),
    ('ethiopia', 'bale', ''),
    ('honduras', 'other', ''),
    ('honduras', 'copan', ''),
    ('honduras', 'opalaca', ''),
    ('honduras', 'montecillos', ''),
    ('honduras', 'comayugua', ''),
    ('honduras', 'el_paraiso', ''),
    ('honduras', 'agalta', ''),
    ('india', 'other', ''),
    ('india', 'wayanad', ''),
    ('india', 'travancore', ''),
    ('india', 'chikmagalur', ''),
    ('india', 'coorg', ''),
    ('india', 'biligiris', ''),
    ('india', 'bababudangiris', ''),
    ('india', 'shevaroys', ''),
    ('india', 'pulneys', ''),
    ('india', 'nilgiris', ''),
    ('india', 'manjarabad', ''),
    ('india', 'brahmaputra', ''),
    ('india', 'bababudangiris', ''),
    ('india', 'arak_valley', ''),
    ('india', 'anamalais', ''),
    ('uganda', 'other', ''),
    ('uganda', 'okoro', ''),
    ('uganda', 'lira', ''),
    ('uganda', 'gulu', ''),
    ('uganda', 'mbale', ''),
    ('uganda', 'bugisu', ''),
    ('uganda', 'jinja', ''),
    ('uganda', 'mukono', ''),
    ('uganda', 'kampala', ''),
    ('uganda', 'masaka', ''),
    ('uganda', 'kasese', ''),
    ('uganda', 'mbarara', ''),
    ('mexico', 'ther', ''),
    ('mexico', 'eracruz', ''),
    ('mexico', 'hiapas', ''),
    ('mexico', 'axaca', ''),
    ('mexico', 'uebla', ''),
    ('guatemala', 'other', ''),
    ('guatemala', 'antigua', ''),
    ('guatemala', 'acatenango_valley', ''),
    ('guatemala', 'huehuetenango', ''),
    ('guatemala', 'coban', ''),
    ('guatemala', 'nueva_oriente', ''),
    ('guatemala', 'fraijanes_plateau', ''),
    ('guatemala', 'atitlan', ''),
    ('guatemala', 'san_marcos', ''),
    ('peru', 'other', ''),
    ('peru', 'piura', ''),
    ('peru', 'cajamarca', ''),
    ('peru', 'cutervo', ''),
    ('peru', 'amazonas', ''),
    ('peru', 'san_martin', ''),
    ('peru', 'huánuco', ''),
    ('peru', 'pasco', ''),
    ('peru', 'junin', ''),
    ('peru', 'cuzco', ''),
    ('peru', 'ayacucho', ''),
    ('peru', 'puno', ''),
    ('nicaragua', 'other', ''),
    ('nicaragua', 'matagalpa', ''),
    ('nicaragua', 'jinotega', ''),
    ('nicaragua', 'estelí ', ''),
    ('nicaragua', 'madriz', ''),
    ('nicaragua', 'nueva_segovia', ''),
    ('china', 'other', ''),
    ('china', 'yunnan', ''),
    ('china', 'fujian', ''),
    ('china', 'hainan_island', ''),
    ('ivory_coast', 'other', ''),
    ('ivory_coast', 'dimbokro', ''),
    ('ivory_coast', 'abengourou', ''),
    ('ivory_coast', 'bongouanou', ''),
    ('ivory_coast', 'gagnoa', ''),
    ('ivory_coast', 'aboisso', ''),
    ('ivory_coast', 'man', ''),
    ('ivory_coast', 'danané', ''),
    ('ivory_coast', 'agboville', ''),
    ('ivory_coast', 'daloa', ''),
    ('ivory_coast', 'san_pedro', ''),
    ('ivory_coast', 'divo', ''),
    ('ivory_coast', 'soubré', ''),
    ('ivory_coast', 'sassandra', ''),
    ('costa_rica', 'other', ''),
    ('costa_rica', 'central_valley ', ''),
    ('costa_rica', 'tres_ríos', ''),
    ('costa_rica', 'turrialba', ''),
    ('costa_rica', 'brunca', ''),
    ('costa_rica', 'guanacaste', ''),
    ('costa_rica', 'tarrazú', ''),
    ('costa_rica', 'orosi', ''),
    ('costa_rica', 'west_valley', ''),
    ('kenya', 'other', ''),
    ('kenya', 'kiambu', ''),
    ('kenya', 'nyeri', ''),
    ('kenya', 'kirinyaga', ''),
    ('kenya', 'muranga', ''),
    ('kenya', 'thika', ''),
    ('kenya', 'meru_entral', ''),
    ('kenya', 'embu', ''),
    ('kenya', 'machakos', ''),
    ('kenya', 'tharaka-nithi', ''),
    ('kenya', 'makueni', ''),
    ('kenya', 'nakuru', ''),
    ('kenya', 'nandi', ''),
    ('kenya', 'kipkelion', ''),
    ('kenya', 'trans_zoia', ''),
    ('kenya', 'baringo', ''),
    ('kenya', 'bungoma', ''),
    ('kenya', 'vihiga', ''),
    ('kenya', 'kakamega', ''),
    ('kenya', 'kisii', ''),
    ('kenya', 'nyamira', ''),
    ('kenya', 'migori', ''),
    ('kenya', 'kisumu', ''),
    ('papua_new_guinea', 'other', ''),
    ('papua_new_guinea', 'western_highlands', ''),
    ('papua_new_guinea', 'eastern_highlands', ''),
    ('papua_new_guinea', 'jiwaka', ''),
    ('papua_new_guinea', 'chimbu', ''),
    ('papua_new_guinea', 'morobe', ''),
    ('papua_new_guinea', 'east_sepik ', ''),
    ('tanzania', 'other', ''),
    ('tanzania', 'arusha', ''),
    ('tanzania', 'moshi', ''),
    ('tanzania', 'pare', ''),
    ('tanzania', 'songea', ''),
    ('tanzania', 'mbinga', ''),
    ('tanzania', 'ruvuma', ''),
    ('tanzania', 'iringa', ''),
    ('tanzania', 'mara', ''),
    ('tanzania', 'morogoro', ''),
    ('tanzania', 'mbeya', ''),
    ('tanzania', 'tanga', ''),
    ('tanzania', 'manyara', ''),
    ('tanzania', 'rukwa', ''),
    ('tanzania', 'kigoma', ''),
    ('tanzania', 'kagera', ''),
    ('tanzania', 'bukoba', ''),
    ('tanzania', 'mwanza', ''),
    ('el_salvador', 'other', ''),
    ('el_salvador', 'apaneca-ilamatepec', ''),
    ('el_salvador', 'el_básalmo-quezaltepec', ''),
    ('el_salvador', 'tecapa-chichontepec', ''),
    ('el_salvador', 'cacahuatique', ''),
    ('el_salvador', 'nahuaterique', ''),
    ('el_salvador', 'alotepeque-metapan', ''),
    ('el_salvador', 'chinchontepec', ''),
    ('ecuador', 'other', ''),
    ('ecuador', 'manabi', ''),
    ('ecuador', 'guayaquil', ''),
    ('ecuador', 'el_oro', ''),
    ('ecuador', 'loja', ''),
    ('ecuador', 'guayas', ''),
    ('ecuador', 'zamora_chinchipe', ''),
    ('ecuador', 'los_rios', ''),
    ('ecuador', 'pichincha', ''),
    ('ecuador', 'orellana', ''),
    ('ecuador', 'sucumbios', ''),
    ('ecuador', 'napo', ''),
    ('cameroon', 'other', ''),
    ('cameroon', 'boyo', ''),
    ('cameroon', 'victoria', ''),
    ('cameroon', 'nkongsamba', ''),
    ('cameroon', 'ebolowa', ''),
    ('cameroon', 'dschang', ''),
    ('cameroon', 'bamileke', ''),
    ('cameroon', 'bamaoun', ''),
    ('laos', 'other', ''),
    ('laos', 'bolaven', ''),
    ('madagascar', 'other', ''),
    ('madagascar', 'vatovavy', ''),
    ('madagascar', 'fitovivany', ''),
    ('madagascar', 'antalaha', ''),
    ('madagascar', 'tamatave', ''),
    ('madagascar', 'nosy_be', ''),
    ('gabon', 'other', ''),
    ('thailand', 'other', ''),
    ('thailand', 'chumphon', ''),
    ('thailand', 'surat_thani', ''),
    ('thailand', 'nakhon_si_thammarat', ''),
    ('thailand', 'krabi', ''),
    ('thailand', 'phang_nga', ''),
    ('thailand', 'ranong', ''),
    ('venezuela', 'other', ''),
    ('venezuela', 'llanos', ''),
    ('venezuela', 'orinoco_river_delta', ''),
    ('venezuela', 'guayana', ''),
    ('venezuela', 'tachira', ''),
    ('venezuela', 'merida', ''),
    ('venezuela', 'trujilo', ''),
    ('venezuela', 'duaca', ''),
    ('dominican_republic', 'other', ''),
    ('dominican_republic', 'cibao', ''),
    ('dominican_republic', 'bani', ''),
    ('dominican_republic', 'azua', ''),
    ('dominican_republic', 'ocoa', ''),
    ('dominican_republic', 'barahona', ''),
    ('dominican_republic', 'juncalito', ''),
    ('haiti', 'other	', ''),
    ('haiti', 'massif_de_la_selle', ''),
    ('haiti', 'massif_du_nord', ''),
    ('haiti', 'massif_de_la_hotte', ''),
    ('haiti', 'montagnes_du_trou_deau', ''),
    ('haiti', 'montagnes_noires', ''),
    ('haiti', 'chaîne_des_matheux', ''),
    ('congo', 'other', ''),
    ('congo', 'maniema', ''),
    ('congo', 'kivu', ''),
    ('congo', 'ubangi', ''),
    ('congo', 'uele', ''),
    ('congo', 'kasai', ''),
    ('congo', 'bas-congo', ''),
    ('congo', 'ituri', ''),
    ('rwanda', 'other', ''),
    ('rwanda', 'virunga', ''),
    ('rwanda', 'akagera', ''),
    ('rwanda', 'kivu', ''),
    ('rwanda', 'muhazi', ''),
    ('rwanda', 'kizi', ''),
    ('rwanda', 'maraba', ''),
    ('burundi', 'other', ''),
    ('burundi', 'buyenzi', ''),
    ('burundi', 'kirimiro', ''),
    ('burundi', 'mumirwa', ''),
    ('burundi', 'bweru', ''),
    ('burundi', 'bugesera', ''),
    ('philippines', 'other', ''),
    ('philippines', 'cordillera ', ''),
    ('philippines', 'northern_luzon', ''),
    ('philippines', 'calabarzon', ''),
    ('philippines', 'mimaropa', ''),
    ('philippines', 'visayas', ''),
    ('philippines', 'mindanao', ''),
    ('togo', 'other', ''),
    ('guinea', 'other', ''),
    ('yemen', 'other', ''),
    ('yemen', 'matari', ''),
    ('yemen', 'haraaz', ''),
    ('yemen', 'hayma', ''),
    ('yemen', 'sanani', ''),
    ('yemen', 'ismaeli', ''),
    ('cuba', 'other', ''),
    ('cuba', 'sierra_maestra', ''),
    ('panama', 'other', ''),
    ('panama', 'boquete', ''),
    ('panama', 'volcan', ''),
    ('panama', 'renacimiento', ''),
    ('panama', 'chiriqui', ''),
    ('bolivia', 'other', ''),
    ('bolivia', 'caranavi', ''),
    ('bolivia', 'coroico', ''),
    ('bolivia', 'nor_yungas', ''),
    ('bolivia', 'sud_yungas', ''),
    ('bolivia', 'inquisivi', ''),
    ('bolivia', 'ichilo', ''),
    ('bolivia', 'samaipata', ''),
    ('bolivia', 'mairana', ''),
    ('central_african_republic', 'other', ''),
    ('nigeria', 'other', ''),
    ('nigeria', 'bauchi', ''),
    ('nigeria', 'kogi', ''),
    ('nigeria', 'ogun', ''),
    ('nigeria', 'oyo', ''),
    ('nigeria', 'taraba', ''),
    ('nigeria', 'ondo', ''),
    ('nigeria', 'ekiti', ''),
    ('nigeria', 'kwara', ''),
    ('nigeria', 'delta', ''),
    ('nigeria', 'edo', ''),
    ('nigeria', 'abia', ''),
    ('nigeria', 'akwa-ibom', ''),
    ('ghana', 'other', ''),
    ('ghana', 'ashanti', ''),
    ('ghana', 'brong', ''),
    ('ghana', 'ahafo', ''),
    ('ghana', 'eastern_volta', ''),
    ('ghana', 'central_volta', ''),
    ('ghana', 'western_volta', ''),
    ('sierra_leone', 'other', ''),
    ('sierra_leone', 'moyumba', ''),
    ('sierra_leone', 'bo', ''),
    ('sierra_leone', 'kenema', ''),
    ('sierra_leone', 'pujuhem', ''),
    ('sierra_leone', 'kono', ''),
    ('sierra_leone', 'kailhahun', ''),
    ('sierra_leone', 'koindugu', ''),
    ('sierra_leone', 'tonkolili', ''),
    ('jamaica', 'other', ''),
    ('jamaica', 'blue_mountain', ''),
    ('paraguay', 'other', ''),
    ('paraguay', 'altos', ''),
    ('paraguay', 'asuncion', ''),
    ('paraguay', 'limpio', ''),
    ('malawi', 'other', ''),
    ('malawi', 'misuku_hills', ''),
    ('malawi', 'phoka_hills', ''),
    ('malawi', 'viphya_north', ''),
    ('malawi', 'nkhatabay_highlands', ''),
    ('malawi', 'south_east_mzimba', ''),
    ('malawi', 'ntchisi_east', ''),
    ('trinidad_tobago', 'other', ''),
    ('zimbabwe', 'other', ''),
    ('zimbabwe', 'chipinge', ''),
    ('zimbabwe', 'chimanimani', ''),
    ('zimbabwe', 'mutasa', ''),
    ('zimbabwe', 'mutare', ''),
    ('zimbabwe', 'honde_valley', ''),
    ('liberia', 'other', ''),
    ('zambia', 'other', ''),
    ('zambia', 'mazabuka', ''),
    ('zambia', 'lusaka', ''),
    ('zambia', 'serenje', ''),
    ('zambia', 'kasama', ''),
    ('zambia', 'mbala', '')
)

def upgrade():
    meta = sa.MetaData(bind=op.get_bind())
    meta.reflect()

    regionTable = sa.Table('region', meta)
    for r in regions:
        op.execute(insert(regionTable).values(name=r[1]), country_name=r[0], display_name=r[2])


def downgrade():
    meta = sa.MetaData(bind=op.get_bind())
    meta.reflect()

    regionTable = sa.Table('region', meta)
    for r in regions:
        op.execute(delete(regionTable).where(name=r[1]))