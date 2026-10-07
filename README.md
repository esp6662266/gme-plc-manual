# GME HMI와 PLC 매뉴얼 홈페이지

GME 설비의 운전 화면과 Siemens PLC 구성, PV01 센서 진단, 알람 이력, 백업 및 구조 개선을 설명하는 한국어 홈페이지다. 매뉴얼은 22개 장이며 검색, 그림 확대, PDF·Markdown·CSV 다운로드를 제공한다.

- 홈페이지: https://gme-plc-manual.netlify.app/
- 공개 저장소: https://github.com/esp6662266/gme-plc-manual

## 운영 구성

- GitHub: 홈페이지 코드와 공개 기술 문서의 변경 이력
- Netlify: HTTPS 홈페이지 게시와 GitHub 변경 시 자동 배포
- Netlify Identity: 서버 자료실 로그인과 이메일 확인
- Netlify Blobs: 계정별 파일, 목록, 개정 이력 저장. 재배포 후에도 보관한다.

자료실 업로드는 파일당 최대 4MB다. Netlify Functions의 바이너리 요청 한도보다 낮게 제한했다. 중요한 대용량 PLC 프로젝트와 VM 이미지는 별도 백업 저장소에 보관한다. 로그인한 사용자의 자료만 조회할 수 있고, 개정본을 올려도 이전 버전을 보존한다. 동시 개정은 조건부 쓰기로 충돌을 표시한다.

## 배포

Node.js 24를 사용한다. `npm ci`, `npm test`, `npm run build`를 실행한다. Netlify에서 이 저장소를 연결하면 `netlify.toml`의 설정에 따라 게시한다. 첫 게시 후 Netlify 프로젝트의 **Identity → Enable Identity**에서 로그인 서비스를 활성화한다. 가입 시 이메일 확인을 유지한다. 자료실 주소는 `/library/`다.

`manual/`에 PDF, Markdown, HTML, PNG·SVG 그림, CSV 참조 자료가 있다. `scripts/build.mjs`가 `dist/`로 복사하고 자료실 브라우저 스크립트를 묶는다. `netlify/functions/documents.mjs`가 인증된 요청을 처리한다. 자동 배포의 게시 폴더는 `dist`, 함수 폴더는 `netlify/functions`다.

홈페이지 파일의 롤백은 서버 자료실에 올린 파일을 되돌리지 않는다. 자료실 데이터는 GitHub 소스 백업에 포함되지 않으므로 다운로드해 별도 보관해야 한다.

## 확인 범위

본 홈페이지는 기술 자료이며 실제 PLC의 운전 상태를 표시하거나 설비를 제어하지 않는다. 매뉴얼의 실제 PLC와 보관 프로젝트의 전체 일치 여부는 추가 확인 대상이다. 홈페이지 빌드는 `manual/`의 기술 문서와 자료실 화면을 `dist/`에 생성하며, 저장소 루트의 별도 프로젝트·백업 자료는 홈페이지 게시 폴더에 복사하지 않는다.

자료실 테스트는 로그인 요구, 계정별 자료 격리, 이전 버전 보존, 동시 개정 충돌, 저장 실패 정리와 파일 검증을 포함한다. 실제 자료실 계정으로 로그인한 뒤 파일을 저장하는 운영 시험은 추가 확인 대상이다. 게시 주소 접속과 문서 다운로드, GitHub 자동 배포, 이메일 발송을 확인했으며 실제 상태는 [배포 상태 안내](manual/배포_상태_안내.md)에 기록한다.
