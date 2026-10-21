# tadak-legal

Public legal documents for the Tadak app.

- Korean Terms: `terms.html`
- Korean Privacy: `privacy.html`
- English Terms: `en/terms.html`
- English Privacy: `en/privacy.html`
- Contact: `omilsoft@gmail.com`

디자인 변경·SEO·검증 결과와 미리보기 방법: [REDESIGN_REPORT.md](REDESIGN_REPORT.md)

```sh
python3 -m http.server 8000
python3 scripts/check_site.py
```

공통 디자인 토큰은 `assets/brand.css`이며, 두 사이트 작업 시 `../shared/brand.css`와 동기화합니다. 서버 없이도 각 HTML 파일을 열 수 있으며, 다운로드 페이지의 자동 이동은 `?stay`로 멈출 수 있습니다.
