# 타닥타닥 문서·지원 사이트 개편 결과

작업일: 2026-10-21 · 저장소: `tadak-legal` · 브랜치: `redesign/2026-10`

`../common.md`, `../DESIGN_APP.md`와 기존 한·영 16개 페이지를 기준으로 작업했습니다. 기존 URL과 정책 본문을 유지하고 Paper 디자인, 문서 탐색, 검색 메타데이터를 정비했습니다. 푸시는 하지 않습니다.

## 페이지별 변경

| 페이지 | 변경 내용 |
| --- | --- |
| `index.html` + `en/index.html` | 큰 제목과 여백, 번호가 있는 문서 목록, 기존 문서별 시행·게시·수정일, 지원·계정 삭제 바로가기, 제품 소개와 스토어 링크를 정리했습니다. 사이트 업데이트 날짜는 정책 시행일과 구분했습니다. |
| `privacy.html` + `en/privacy.html` | 시행일·공고일을 보존하고 날짜에 `time`을 적용했습니다. 요약 카드, 본문 약 68ch, 데스크톱 고정 목차, 모바일 접이식 목차, 소제목·변경 이력 링크를 적용했습니다. |
| `terms.html` + `en/terms.html` | 개인정보처리방침과 같은 읽기 레이아웃을 적용했습니다. 기존 조항·날짜·과거 버전 링크를 보존하고 변경 이력을 12번 섹션으로 표시했습니다. |
| `support.html` + `en/support.html` | 공식 이메일을 큰 연락처 카드로 강조했습니다. 기존 문의 유형·운영 기준을 유지하고 계정 삭제, 구매 복원, 신고·제재, 답변 순서에 관한 FAQ 4개를 추가했습니다. 답변은 기존 안내에서 정리했습니다. |
| `account-deletion.html` + `en/account-deletion.html` | 앱 실행부터 최종 확인까지 기존 네 단계를 번호가 있는 절차로 표시했습니다. 삭제 대상, 예외 보관, 복구 불가 안내와 이메일 지원 경로를 보존했습니다. |
| `community-policy.html` + `en/community-policy.html` | 기존 정책 문구를 유지하면서 요약, 번호별 조항, 소제목 링크와 목차를 통일했습니다. |
| `download.html` + `en/download.html` | 새 앱 아이콘, 무료·지원 플랫폼 안내, 두 스토어 버튼, 기존 다운로드 QR, 지원 링크를 정리했습니다. 기존 기기별 자동 스토어 이동과 `?stay` 옵션을 보존했습니다. |
| `operator-info.html` + `en/operator-info.html` | 운영자 요약 카드와 기존 사업자 정보를 정리하고 관련 링크 제목을 `h2`로 바로잡았습니다. 사업자등록번호·대표자·이메일·전화번호는 보존했습니다. |

## 공통 디자인·접근성

- 공유 폴더가 비어 있어 `../shared/brand.css`에 Paper 색상·Pretendard·간격·읽기 폭·다크 모드 토큰을 작성했습니다. 랜딩 작업자가 같은 파일을 채택한 것을 파일 메모로 확인했고, 법률 사이트는 `assets/brand.css` 복사본으로 독립 배포합니다.
- 새 앱 아이콘 + `TADAK.` 로고, 공통 주 메뉴, 대응 페이지로 연결되는 KO/EN 전환을 적용했습니다.
- 푸터에는 모든 정책, 운영자 정보, 공식 제품 링크를 배치했습니다. 제품 링크는 한국어 `https://eastlooo.github.io/omilsoft-official-site/tadak/`, 영어 `https://eastlooo.github.io/omilsoft-official-site/en/tadak/`입니다.
- 데스크톱 목차는 스크롤에 따라 현재 위치를 표시합니다. 900px 이하에서는 기본적으로 접히며, 링크 선택 후 본문으로 포커스를 이동합니다. JavaScript를 끄면 기본 `details` 목차와 문서 링크가 작동합니다.
- 제목별 고유 앵커, 건너뛰기 링크, 키보드 포커스, 메뉴 Escape 닫기, 모션 감소 환경 설정, 시스템 다크 모드와 이미지 고정 크기를 적용했습니다.
- 페이지 하단에 맨 위로 이동과 인쇄 버튼을 배치했습니다. 인쇄 시 메뉴·목차·푸터를 제외하고 흰 배경으로 전환합니다. FAQ는 인쇄 전 펼치고 인쇄 후 원래 상태로 복원합니다.
- 표의 가로 스크롤·표 머리글·테두리·인쇄 스타일을 준비했습니다. 현재 정책 원문에는 HTML 표가 없어 새 표로 재작성하지 않았습니다.

## SEO 체크리스트

| 항목 | 상태 |
| --- | --- |
| 16개 페이지별 고유 title ≤60자, description ≤155자 | 정적 검사 통과 |
| canonical, ko/en/x-default hreflang 및 역방향 연결 | 정적 검사 통과 |
| 한국어·영어 `html lang`, 페이지당 h1 하나, 제목 계층 | 정적 검사 통과 |
| Open Graph, Twitter, 1200×630 한·영 공유 이미지 | 적용·이미지 크기 검사 통과 |
| 밝은/어두운 theme-color, 새 favicon과 apple-touch-icon | 적용·규격 검사 통과 |
| 모든 페이지 BreadcrumbList, Organization, WebSite | JSON 파싱·구조 검사 통과 |
| 다운로드 MobileApplication, 가격 0 및 iOS/iPadOS/Android | 적용 |
| 지원 FAQPage와 실제 FAQ 4개 | 적용·개수 검사 통과 |
| `sitemap.xml` 16개 canonical + lastmod + 언어 대체 링크 | 정적 검사 통과 |
| `robots.txt` 사이트맵 참조, 검색 색인 허용 | 적용. 모든 페이지 `index, follow`; noindex 없음 |
| 기존 Search Console 인증 메타 | 원본 16개 페이지에 인증 메타가 없음을 확인. 임의 인증값은 추가하지 않음 |
| 이미지 대체 텍스트·크기·WebP 및 PNG 대체·QR lazy loading | 정적 검사 통과 |
| Pretendard 동적 서브셋과 CDN preconnect, 공통 최소 JS | 적용 |
| Lighthouse SEO·접근성·Best Practices·모바일 성능 목표 | 실행 환경 제한으로 미측정. 점수 통과를 주장하지 않음 |

문서 허브의 루트와 `/en/`를 canonical로 사용하며 `index.html`, `en/index.html` 파일도 그대로 유지합니다. 별점·리뷰 수 등 법률 페이지에 불필요한 홍보 수치는 추가하지 않았습니다.

## 생성·갱신한 자산

- `assets/app/favicon-32.png`, `favicon-64.png`, `apple-touch-icon.png` — `../refs/app_icon_1024.png`에서 생성.
- `assets/app/icon.webp`, `icon.png` — 같은 원본의 192×192 웹용 이미지와 대체 PNG.
- `assets/tadak-legal-og.png`, `tadak-legal-og-en.png` — 새 아이콘과 Paper 디자인으로 구성한 1200×630 공유 이미지. 각 약 48KB이며 두 언어의 편집 원본 SVG도 갱신했습니다. 한·영 PNG를 이미지 도구로 열어 확인했습니다.
- `assets/brand.css`, `assets/site.css`, `assets/site.js` — 공유 토큰, 법률 문서 레이아웃, 메뉴·목차·인쇄 향상 기능.
- 기존 다운로드 QR 두 개는 유지했습니다.

## 검증 결과와 남은 확인

다음 검사를 통과했습니다.

```sh
python3 scripts/check_site.py --compare-ref a28a315
node --check assets/site.js
git diff --check
```

검사 스크립트는 메타데이터·언어 쌍·JSON-LD·파일 링크·앵커·이미지 규격·사이트맵·공유 토큰 일치를 확인합니다. 개편 전 커밋 `a28a315`과 비교해 기존 법률 문단·목록·표 셀·앵커 보존도 확인했습니다. 정책 본문의 오탈자 수정은 **없습니다**. 백틱을 실제 `code` 마크업으로 바꾸고 목차·요약·날짜 레이블 등 화면 안내를 한국어로 통일했습니다.

실제 브라우저 검수와 Lighthouse는 완료하지 못했습니다. 이 세션의 샌드박스가 Python 서버와 browse 데몬의 localhost 바인딩을 거부했고, 브라우저 도구는 로컬 `file:` URL을 정책상 차단했습니다. 이 제한을 우회하지 않았습니다. 따라서 320/390/768/1440px 레이아웃, 다크 모드, 키보드 메뉴·목차 이동, 인쇄 미리보기와 Lighthouse 점수는 허용된 로컬 환경에서 최종 확인해야 합니다.

다음 기존 내용은 운영자가 확인할 항목입니다. 커뮤니티 정책은 2026-03-06 기준 키워드 차단·신고 3건 기준을 유지하지만, 2026-10-25 시행 개인정보처리방침·약관에는 AI 검사와 가중 신고가 반영되어 있습니다. 원문 유지 요청에 따라 임의로 정책 내용을 맞추지 않았습니다.

영문 제품 랜딩 `/en/tadak/`는 다른 작업자가 새로 만드는 페이지이므로 두 저장소 배포 후 연결을 확인해 주세요. 기존 다운로드 자동 이동은 실제 iPhone/iPad/Android에서도 확인해야 합니다.

## 로컬 미리보기

이 저장소에서 다음 명령을 실행합니다.

```sh
python3 -m http.server 8000
```

- 허브: `http://localhost:8000/`
- 개인정보처리방침: `http://localhost:8000/privacy.html`
- 지원·FAQ: `http://localhost:8000/support.html`
- 자동 이동 없이 다운로드 확인: `http://localhost:8000/download.html?stay`
- 영문: `http://localhost:8000/en/`

한·영 법률 문서의 날짜와 본문을 확인한 뒤 모바일 화면·인쇄·Lighthouse를 검수하면 됩니다.

## 커밋 상태

최근 이력의 한국어 Conventional Commit 형식을 확인하고 커밋을 준비했으나, 샌드박스가 `.git/index.lock` 생성을 거부해 스테이징·커밋을 만들지 못했습니다. 변경 파일은 작업 트리에 남겨 두었으며 지정된 공동 작성자 표기를 포함한 메시지는 `/tmp/tadak-legal-commit.txt`에 저장했습니다. 푸시하지 않았습니다.
