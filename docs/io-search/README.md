# GME 통합검색

PLC/HMI·기존 회로/신호와 공개 매뉴얼 HTML 본문, 원본 PDF3개330쪽을 검색합니다. 기능 설명/도면 시각대조6행과 단순 본문 문맥은 결과 배지로 구분합니다. 원본 텍스트층이 없는8.9/8.10은 실제 도면 PDF9쪽을 시각대조하여 전사했습니다. 미추출 표기의0건은 도면상 부재를 뜻하지 않습니다.

왼쪽 설비 검색창에서 Enter 또는 검색0건의 통합검색 버튼으로 진입할 수 있습니다. 선택한 설비의 문서/페이지 참조는 기존ID로 연결하고, 공통·미배정 문서는 전체 범위에서 검색합니다. 운영 localStorage·수리기록·MD초안은 색인하지 않습니다.

## 재생성

Python3.10+와 pypdf6.10.0을 사용할 수 있는 Python을 GME_PYTHON으로 지정합니다. 문서를 실행하지 않고 정적으로 읽습니다.

1. 버전/정적UI 변경 후 기존 정책에 따라 build-all-in-one.py를 실행합니다.
2. `npm run build:documents`로 PDF layout와 HTMLParser 본문을 압축 색인으로 저장합니다.
3. `npm run build:io-search`로7종 통합색인을 생성합니다.
4. `npm test`, 필수 패키지 검증, `NETLIFY=true npm run build`를 진행합니다.

Netlify는 커밋된 색인을 검증·복사하며 Python 추출기를 실행하지 않습니다. 모든 입력 문서의SHA256이 일치해야 빌드할 수 있습니다. 새 all-in-one 경로는 GME_NEW_PACKAGE_FILES에 기존 manifest 대비 정확한 목록으로 지정합니다. 이 저장소는 sparse checkout이므로 새/수정 파일을 `git add --sparse`로 검토하여 포함합니다.

시뮬레이터·PLC/현장·보호값·SEJIN 운영 자료는 실행하거나 변경하지 않습니다. 기존 철거/미사용 표시·도면상충 보류를 유지합니다.
