# 굿파트너모빌리티

대리운전 · 차량탁송 · 퀵서비스 | 1555-1103

## Cloudflare Pages 설정
- Production branch: main
- Framework preset: None
- Build command: 비워두기
- Build output directory: dist

홈페이지 파일은 dist 폴더에 있습니다. 별도 빌드나 API 키가 필요하지 않습니다.

이 소스는 공개 서비스·회사 안내 6개 페이지의 검색 수집을 허용합니다. 정규 주소는 https://gpmobility.kr/이며, Cloudflare Pages의 기본 HTML 확장자 제거 리다이렉트에 맞춰 내부 링크·canonical·사이트맵을 통일했습니다. 404 페이지는 noindex를 유지하고 사이트맵에서 제외합니다. Cloudflare Pages 미리보기 배포의 기본 X-Robots-Tag: noindex는 변경하지 않습니다.

온라인 접수와 이메일 수신 서버는 연결하지 않았으며 문의 버튼은 대표번호로 연결됩니다. 이미지는 서비스 연출 이미지입니다.

## 검색 설정 검사
저장소 루트에서 다음 명령을 실행합니다. Python 3 표준 라이브러리만 사용합니다.

```sh
python -m unittest discover -s tests -v
```

검색 설정 변경을 main에 병합하거나 실제 운영에 배포하려면 별도 승인이 필요합니다. Git 연동이 설정돼 있다면 main 변경 시 자동 배포될 수 있습니다. 소스 수정 자체는 검색엔진 색인·순위 상승을 보장하지 않습니다.

운영 반영 후에는 메인과 5개 서비스/소개 경로, robots.txt, sitemap.xml의 실제 HTTP 응답과 noindex 헤더 여부를 확인해야 합니다. .html 주소는 확장자 없는 정규 주소로 이동해야 합니다. 현재 소스는 별도 서버·DB·외부 추적 스크립트·유료 서비스를 추가하지 않습니다. 실제 계정 사용량/요금은 별도 확인 대상입니다.
