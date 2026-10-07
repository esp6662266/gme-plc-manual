# GME HMI와 PLC 매뉴얼 파일 안내

2026년 10월 7일 기준 기술 자료다. 원본 프로젝트와 실제 설비를 변경하지 않고 화면, 설정 파일, 백업 검색 색인, 알람 DB를 확인해 작성했다.

- [상세 매뉴얼 PDF](GME_HMI_PLC_manual.pdf): 목차와 페이지 번호가 있는 열람용 문서
- [검색 가능한 HTML](manual.html): 브라우저에서 검색하고 장별로 이동
- [Markdown 원본](manual.md): 이후 수정과 이력 관리에 사용
- [PLC 통신 장애 확인 기록](PLC_communication_check_20261007.md)
- [블록 목록](references/blocks.csv): 속성 문서 89개
- [네트워크 목록](references/networks.csv): 검색 색인 문서 457개
- [HMI PLC 태그 목록](references/hmi_plc_tags.csv): 설정 782개
- [HMI 화면 목록](references/hmi_windows.csv): 화면 메타데이터 17개
- [검증 대장](references/verification.csv): 추가 확인 16개

그림 PNG와 수정 가능한 SVG는 assets 폴더에 있다. HTML과 Markdown을 옮길 때는 전체 폴더를 함께 복사한다. PDF는 단독으로 읽을 수 있다. CSV는 Excel에서 열 수 있도록 UTF-8 BOM으로 저장했다.

현재 물리 PLC와 2월·6월 보관 프로젝트의 전체 일치 여부는 아직 확인되지 않았다. 백업의 검색 토큰은 다운로드 가능한 소스가 아니며 접점 연결을 완전히 보존하지 않는다. 현장 표시값은 관찰 시점의 값이다. 개선안은 아직 구현하거나 적용하지 않은 설계 제안이다.

홈페이지는 GitHub와 Netlify를 연결해 운영하도록 선택했다. [홈페이지 시작 화면](index.html)은 이 폴더에서 바로 열 수 있다. Netlify Identity와 Blobs를 사용하는 서버 자료실 소스도 준비했다. [배포 상태 안내](배포_상태_안내.md)에서 게시 및 GitHub 업로드의 실제 상태를 확인한다.

PLC 아카이브, HMI 실행 파일, SQL DB 백업, VM 디스크와 라이선스는 이 문서 묶음에 포함하지 않았다. 이 문서 묶음은 설비 전체를 복원하는 백업 파일이 아니다.
