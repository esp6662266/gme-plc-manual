"""Selected visible rows of the 2024 construction drawing, not a field cable list.

Page+row is the key: cable identifiers can repeat. Masked rows are excluded.
Core/size/type/LEN are verbatim drawing values, not installation recommendations.
"""
SOURCE='sources/Electrical_Can_Decoating_20241118.pdf'
SHA256='3963f137b7a1a5a8ab6525c9e002046f8aa5ebbdee4799f41b0a0bad664a4dbd'
VISUAL_PAGES=[1,2,3,4,5,6,19,21,24,33,48,50,51,52,53,55,56,57,58,59,64]
MASKED={52:['2_5'],53:['3_5'],56:['6_7','6_8','6_9','6_10'],58:['8_5','8_7','8_8']}

def power(id,row,code,motor,current,spec,size,route,length,note=''):
    return dict(key='P'+str(50+int(row.split('_')[0]))+':'+row, equipment=id,
        page=50+int(row.split('_')[0]),row=row,cable=code,from_='CR',to=motor,
        current_type=current,spec=spec,core='4',size=size,spare='0',
        route=route,len_original=str(length),note=note,visible=True,field_verified=False)

POWER=[
    power('BC01','1_1','=ENT+BC01-M02A','BC-01 / M02','DAC','PVC-S','2.5SB',['CR','E100'],22),
    power('FN03','1_3','=ENT+FN03-M25A','FN-03 / M25','DAC','PVC-S','25SB',['100','RA','E200'],36),
    power('FN06','1_4','=ENT+FN06-M26A','FN-06 / M26','GAC','CV','1.5',['100','RB','E100'],43,'PDF21 배관도에는 100RBD1의 분기 표기도 있습니다. 배관 경로 단계와 케이블 목록의 열을 함께 확인합니다.'),
    power('RD01','1_5','=ROT+RD01-M03A','RD-01 / M03','DAC','PVC-S','25SB',['100','RC','E100'],39,'PDF24 같은 케이블의 SIZE16과 차이. C04 검토 전 규격을 선택하지 않습니다.'),
    power('RD01-FAN','1_6','=ROT+RD01-M04A','RD-01 / M04','GAC','CV','1.5',['100','RC','E200'],39,'RD01 주 구동 M03과 냉각팬 M04를 별도로 기록합니다.'),
    power('MV03','1_9','=FLA+MV03-M17A','MV-03 / M17','GAC','CV','1.5',['100','LCD1','E100'],46),
    power('FN02','1_10','=FLA+FN02-M19A','FN-02 / M19','DAC','PVC-S','50SB',['100','110','LAD1','E100'],50),
    power('MV01','1_11','=FLA+MV01-M20A','MV-01 / M20','GAC','CV','1.5',['100','110','LAD1','E200'],49),
    power('FN01','1_12','=FLB+FN01-M22A','FN-01 / M22','DAC','PVC-S','95SB',['100','120','RB','E1200'],65),
    power('FN01-FAN','1_13','=FLB+FN01-M29A','FN-01 / M29','GAC','CV','1.5',['100','120','RB','E1300'],65,'기존 OEM FG54는 냉각팬 SPARE 표기입니다. 시공도면 목록에 있다고 실제 설치·사용으로 확정하지 않습니다.'),
    power('MV06','1_14','=FLB+MV06-M14A','MV-06 / M14','DAC','PVC-S','1.5SB',['100','120','RB','E900'],59),
    power('MC04','1_18','=EXI+MC04-M09A','MC-04 / M09','DAC','PVC-S','16SB',['100','120','121','122','EXI1TB1','E100'],87),
    power('VS01','1_20','=EXI+VS01-M06A','VS-01 / M06','DAC','PVC-S','6SB',['100','120','121','122','EXI1TB1','E300'],88),
    power('VS01','1_21','=EXI+VS01-M07A','VS-01 / M07','DAC','PVC-S','6SB',['100','120','121','122','EXI1TB1','E400'],88,'두 모터 분기를 별도로 기록합니다.'),
    power('SC01','1_22','=DUS+SC01-M28A','SC-01 / M28','GAC','CV','1.5',['100','200','210','211','RC','E100'],110,'FN04와 연관된 분진 스크루이며 동일 설비로 병합하지 않습니다.'),
    power('FN04','2_3','=DUS+FN04-M31A','FN-04 / M31','DAC','PVC-S','50SB',['100','200','230','231','RA','E100'],106,'PDF48 모터 그림·TAG 표기의 혼재는 C05에서 확인 대기로 관리합니다.'),
    power('FN04','2_4','=DUS+FN04-M36A','FN-04 / M36','DAC','PVC-S','50SB',['100','200','230','231','RB','E100'],109,'공통 인버터와 두 모터 분기를 구분합니다. M34·M38로 자동 치환하지 않습니다.'),
]

def control(id,page,row,cable,from_,to,current,spec,core,size='1.0',note='',spare=None):
    return dict(key='P'+str(page)+':'+row,equipment=id,page=page,row=row,cable=cable,
        from_=from_,to=to,current_type=current,spec=spec,core=core,size=size,
        spare=spare,note=note,visible=True,field_verified=False)

CONTROL=[
    control('BC01',53,'3_18','=ENT+BC01-SS01A','BC-01 / ENT1TB1','BC-01 / SS-01','DC','CVV','5G',note='기존 FG19의 직렬 허가 접점과 PLC 감시 접점은 별도 회로입니다.'),
    control('BC01',53,'3_19','=ENT+BC01-SSL01A','BC-01 / ENT1TB2','BC-01 / SSL-01','DC','CVV','2C',note='OEM FG19 SPARE. 설치 여부·입력 사용은 미확인입니다.'),
    control('PV01',53,'3_8','=ENT+PV01-ENT2TB2A','CC-01 / ENT2TB1','PV-01 / ENT2TB2 · LS01/02/03/04','DC','CVV','12G',spare='3'),
    control('PV01',53,'3_9','=ENT+PV01-ENT2TB2B','CC-01 / ENT2TB1','PV-01 / ENT2TB2 · EV01','AC','CVV','3G',spare='0'),
    control('PV01',53,'3_10','=ENT+PV01-ENT2TB3A','CC-01 / ENT2TB1','PV-01 / ENT2TB3 · LS05/06/07/08','DC','CVV','12G',spare='3'),
    control('PV01',53,'3_11','=ENT+PV01-ENT2TB3B','CC-01 / ENT2TB1','PV-01 / ENT2TB3 · EV02','AC','CVV','3G',spare='0'),
    control('PV02',55,'5_1','=ROT+UC01-ROT1TB1A','CR','UC-01 / ROT1TB1 · LS25–32, PB16','DC','CVV','25G',spare='5',note='공유 접속함의 간선입니다. PV02 전용 PLC 입력 수를 의미하지 않습니다.'),
    control('PV02',55,'5_2','=ROT+UC01-ROT1TB1B','CR','UC-01 / ROT1TB1 · EV03/04/05','AC','CVV','12G',spare='5',note='EV03은 RD01 윤활 밸브 회로와 구분해 추적합니다.'),
    control('PV02',55,'5_4','=ROT+PV02-LS25A','UC-01 / ROT1TB1','PV-02 / LS-25','DC','CVV','2C',note='배관도 PDF24의 짧은 No. 표기는 다릅니다. 전체 식별자와 페이지로 찾습니다.'),
    control('PV02',55,'5_8','=ROT+PV02-EV04A','UC-01 / ROT1TB1','PV-02 / EV-04','AC','CVV','3G'),
    control('EV03',55,'5_3','=ROT+RD01-ROT1TB2A','UC-01 / ROT1TB1','RD-01 / ROT1TB2 · EV03','AC','CVV','3G',note='공유 간선 다음의 RD01 접속함 분기. 원본 FG21/PDF22의 밸브 회로와 대조합니다.'),
    control('EV03',55,'5_15','=ROT+RD01-EV03A','RD-01 / ROT1TB2','RD-01 / EV-03','AC','CVV','3G'),
    control('MV03',56,'6_15','=FLA+MV03-LS19A','MV-03 / FLO1TB1','MV-03 / LS-19','DC','CVV','2C'),
    control('MV03',56,'6_16','=FLA+MV03-LS20A','MV-03 / FLO1TB1','MV-03 / LS-20','DC','CVV','2C'),
    control('MV03',56,'6_17','=FLA+MV03-ZT04A','MV-03 / FLO1TB1','MV-03 / ZT-04','TM','CVV-S','4S',note='도면 TM 표기는 원문으로 유지합니다. 전기 신호 규격·PLC 환산은 별도 확인입니다.'),
    control('MV01',57,'7_8','=FLA+MV01-LS23A','HE-01 / FLO2TB1','MV-01 / LS-23','DC','CVV','2C'),
    control('MV01',57,'7_9','=FLA+MV01-LS24A','HE-01 / FLO2TB1','MV-01 / LS-24','DC','CVV','2C'),
    control('MV01',57,'7_10','=FLA+MV01-ZT02A','HE-01 / FLO2TB1','MV-01 / ZT-02','AI','CVV-S','4S'),
    control('MV06',58,'8_6','=FLB+MV06-FLO4TB2A','CR','MV-06 / FLO4TB2 · ZT06','TM','CVV-S','4S',note='8_17과 같은 식별자지만 시작점·신호·규격이 다릅니다. C01 확인 전 한 케이블로 합치지 않습니다.',spare='0'),
    control('MV06',58,'8_17','=FLB+MV06-FLO4TB2A','UC-01 / FLO4TB1','MV-06 / FLO4TB2 · LS34/35','DC','CVV','7G',note='8_6과 같은 식별자. 페이지+행을 별도 키로 보존합니다.',spare='2'),
    control('MV06',58,'8_19','=FLB+MV06-LS34A','MV-06 / FLO4TB2','MV-06 / LS-34','DC','CVV','2C'),
    control('MV06',58,'8_20','=FLB+MV06-LS35A','MV-06 / FLO4TB2','MV-06 / LS-35','DC','CVV','2C'),
    control('MV06',58,'8_21','=FLB+MV06-ZT06A','MV-06 / FLO4TB2','MV-06 / ZT-06','TM','CVV-S','4S'),
    control('MC04',59,'9_7','=EXI+MC04-SS10A','MC-05 / EXI1TB2','MC-04 / SS-10','DC','CVV','2C',note='OEM FG25의 SS10 SPARE 표기와 현재 설치·사용을 대조합니다.'),
    control('MC04',59,'9_8','=EXI+MC04-SS11A','MC-05 / EXI1TB2','MC-05 / SS-11','DC','CVV','2C',note='식별자의 MC04와 TO의 MC05가 다릅니다. C07 대기. MC04·MC05·SS11을 병합하지 않습니다.'),
    control('FN01',58,'8_22','=FLB+FN01-TC04A','CR','FN-01 / TC-04','TC','KX','2S',note='8_7의 가려진 NO/NO 행을 배선으로 채택하지 않습니다.'),
    control('FN01',58,'8_23','=FLB+FN01-TC05A','CR','FN-01 / TC-05','TC','KX','2S',note='8_8의 가려진 NO/NO 행을 배선으로 채택하지 않습니다.'),
]
for row,suffix,current,spec,core,size,spare in [
    ('14_12','A','DC','CVV','25G','1.0','8'),('14_13','B','AC','CVV','4G','4.0','3'),
    ('14_14','C','AC','CVV','16G','1.0','15'),('14_15','D','AIO','CVV-S','4S','1.0','3'),
    ('14_16','E','AIO','CVV-S','4S','1.0','3'),('14_17','F','AI','CVV-S','4S','1.0','3'),
    ('14_18','F','AI','CVV-S','4S','1.0','3')]:
    CONTROL.append(control('BR01',64,row,'=ENT+CC01-BR01'+suffix,'CR','CC-01 / BR-01',current,spec,core,size,spare=spare,note='버너 간선 묶음. 개별 핀·연소 안전 기능은 미식별입니다.'+(' F가 두 행에 반복되어 C02 확인 전 별도 기록합니다.' if suffix=='F' else '')))

REVIEWS=[
    dict(id='C01',equipment=['MV06'],pages=[58],rows=['8_6','8_17'],observation='=FLB+MV06-FLO4TB2A가 TM/CVV-S/4S/CR 시작 행과 DC/CVV/7G/UC01 시작 행에 반복됩니다.',impact='식별자만 키로 쓰면 서로 다른 신호·시작점이 합쳐집니다.',validation='제작사 수정본, 양단 케이블 표찰·접속함 단자 기록을 대조해 두 간선을 식별합니다.'),
    dict(id='C02',equipment=['BR01','CC01'],pages=[64],rows=['14_17','14_18'],observation='=ENT+CC01-BR01F가 같은 FROM/TO·AI·4S 규격으로 두 행에 반복됩니다.',impact='중복 기재인지 실제 두 간선인지 확정할 수 없습니다.',validation='버너 전용 배선도와 양단 표찰·케이블 수를 확인합니다. 자동 중복 제거를 하지 않습니다.'),
    dict(id='C03',equipment=['MV05','MV06'],pages=[56],rows=['6_6','6_20'],observation='MV05 FLO1TB2 간선 설명은 ZT06, 같은 접속함에서 나가는 직접 케이블·TO는 ZT05입니다.',impact='MV06의 ZT06 또는 다른 센서로 잘못 연결될 수 있습니다.',validation='MV05·MV06 실물 센서 표찰과 단자, 원본 회로도·PLC 심볼을 각각 확인합니다.'),
    dict(id='C04',equipment=['RD01'],pages=[24,51],rows=['1_5'],observation='=ROT+RD01-M03A: PDF24 배관표 SIZE16, PDF51 케이블 목록 SIZE25SB입니다.',impact='도면만으로 케이블 단면·사양을 선택할 수 없습니다.',validation='승인된 개정본과 실제 케이블·보호기기·모터 명판을 대조합니다. 이 매뉴얼에서 임의 규격을 확정하지 않습니다.'),
    dict(id='C05',equipment=['FN04'],pages=[48,52],rows=['2_3','2_4'],observation='PDF48 DUST14의 모터 그림은 M34/M38, 표의 TAG는 M31/M34, 케이블 접미사·PDF52 TO는 M31/M36입니다.',impact='FN04 두 분기를 SC10 M34·VR04 M38과 잘못 병합할 수 있습니다.',validation='OEM FG59의 M31/M36, 배치도, 양단 표찰·모터 명판을 별도로 대조합니다. PDF48 표기를 현장 ID로 채택하지 않습니다.'),
    dict(id='C06',equipment=['PV02','EV03'],pages=[24,55],rows=['5_3','5_4','5_5'],observation='배관도 PDF24의 LS25·LS26 No.는 5_3·5_4, 케이블 목록 PDF55에서는 5_4·5_5입니다. PDF55의 5_3은 RD01 ROT1TB2 간선입니다.',impact='짧은 No.만 따라가면 센서와 밸브 간선이 바뀝니다.',validation='전체 케이블 식별자+페이지+FROM/TO로 대조하고 제작사 개정본에서 참조 순번을 확인합니다.'),
    dict(id='C07',equipment=['MC04','MC05'],pages=[59],rows=['9_8'],observation='케이블 식별자는 =EXI+MC04-SS11A지만 TO는 MC05 / SS11입니다.',impact='MC04·MC05의 감시 신호와 정비 이력이 섞일 수 있습니다.',validation='SS10·SS11 실물 위치, EXI1TB2 양단 단자와 OEM 회로도를 확인합니다. 이름만으로 소유 설비를 지정하지 않습니다.'),
]
for review in REVIEWS:review.update(status='확인 대기',resolved=False,field_verified=False)

# Only visually reviewed source pages. Broad text mentions and legend examples
# are deliberately not converted into equipment identities or control models.
PROFILES={
 'BC01':([4,5,6,21,51,53],'ENT1TB1/2 → SS01·SSL01. 기동 직렬 회로와 PLC 감시 회로를 구분합니다.'),
 'FN04':([4,6,48,52],'M31·M36 두 동력 분기와 공통 인버터. PDF48의 혼재 표기는 C05 확인 대기입니다.'),
 'PV01':([5,6,21,53],'ENT2TB1 → ENT2TB2/3 → LS01–08·EV01/02. LS 여덟 표기를 PLC 입력 여덟 개로 확정하지 않습니다. 기존 백업 입력6개·예비 및 도면 차이는 계속 확인합니다.'),
 'PV02':([5,6,24,55],'ROT1TB1 → LS25–32·EV04/05, PB16. 공유 간선에 포함된 EV03은 별도 RD01 윤활 회로입니다.'),
 'RD01':([4,6,24,51,55],'킬른 본체 대응은 후보입니다. M03 주 구동·M04 냉각팬·EV03 윤활 밸브를 별도 추적합니다.'),
 'MC04':([4,5,6,51,59],'M09 동력과 EXI1TB2의 SS10 감시를 분리합니다. SS11은 MC05 TO 표기와 차이가 있어 대기합니다.'),
 'VS01':([4,6,51],'M06·M07 두 모터 케이블입니다. 공통 제어 신호로 개별 모터의 정상 회전을 보증하지 않습니다.'),
 'CC01':([5,6,21,53,64],'본체 후보와 ENT2TB1 공유 접속함, BR01 간선을 구분합니다. 접속함 표기가 본체 전용 제어를 증명하지 않습니다.'),
 'BR01':([6,64],'CR → CC01 / BR01 간선 묶음. 버너 개별 핀·연소 안전·기동 순서는 전용 도면·원본 로직 확인 전입니다.'),
 'AB01':([3,6,64],'재연소로 본체 대응은 후보입니다. 6SB2 케이블 표기는 전체 비상정지 기능·안전 등급을 증명하지 않습니다.'),
 'HE01':([5,6,56,57],'열교환기 본체 후보와 FLO1/FLO2 공유 접속함, 주변 댐퍼·센서의 소유를 구분합니다. 가려진 6_7–10은 채택하지 않습니다.'),
 'FN01':([4,5,6,33,51,58],'M22 주 팬, M29 냉각팬 예비 여부, TC04/05를 구분합니다. PDF58의 가려진 8_7/8과 실제 보이는 8_22/23을 혼용하지 않습니다.'),
 'FN02':([4,6,51],'M19 동력 케이블과 OEM FG42/43의 기동·응답 경로를 함께 확인합니다.'),
 'FN03':([4,6,21,51],'M25 동력과 소프트스타터 TOR 응답은 별도 경로입니다. 시공도면 DAC 표기는 OEM FG51의 장치 종류를 대신 확정하지 않습니다.'),
 'FN06':([4,6,21,51],'M26 동력과 OEM FG52 허가·응답을 함께 확인합니다. 경로의 분기 표기를 실제 배관과 대조합니다.'),
 'MV01':([4,5,6,51,57],'M20 동력, FLO2TB1 → LS23/24·ZT02를 구분합니다. 위치 정상값·환산은 현장 및 원본 확인 전입니다.'),
 'MV03':([4,5,6,51,56],'M17 동력, FLO1TB1 → LS19/20·ZT04. 공유 접속함의 다른 댐퍼·센서를 자동 귀속하지 않습니다.'),
 'MV06':([4,5,6,33,51,58],'M14 동력, FLO4TB2 → LS34/35·ZT06. 중복 간선 식별자 C01은 페이지·행으로 분리합니다.'),
 'RD01-FAN':([4,24,51],'M04 냉각팬을 RD01 M03 주 구동과 별도로 유지합니다.'),
 'FN01-FAN':([4,33,51],'M29 냉각팬 케이블 기록과 OEM FG54 SPARE를 함께 확인합니다. 설치·사용 확정 전입니다.'),
 'EV03':([6,24,55],'ROT1TB1 → RD01 ROT1TB2 → EV03. PV02 밸브 EV04/05와 별도 회로입니다.'),
 'SC01':([4,6,51],'M28 분진 스크루. FN04 인터록 관련 여부는 PLC 원본으로 확인하고 별도 설비 ID를 유지합니다.'),
}
