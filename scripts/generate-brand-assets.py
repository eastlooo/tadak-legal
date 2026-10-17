#!/usr/bin/env python3
"""Build Paper icons and social cards from the current app icon (Pillow required).

Usage: /usr/local/bin/python3 scripts/generate-brand-assets.py [_src/tadak-icon.png]
The source directory is intentionally excluded from Git.
"""
import base64
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / '_src/tadak-icon.png'
ASSETS = ROOT / 'assets'
PAPER, INK, MUTED, LINE, COBALT = '#fafaf8', '#242524', '#62645f', '#d9d9d2', '#3d7bea'
icon = Image.open(SOURCE).convert('RGB')
icon.save(ASSETS / 'app/icon.webp', quality=95)
for size, name in [(32, 'favicon-32.png'), (64, 'favicon-64.png'), (180, 'apple-touch-icon.png')]:
    icon.resize((size, size), Image.Resampling.LANCZOS).save(ASSETS / 'app' / name)

# Apple SD Gothic Neo is the local Korean fallback used for the PNG rendering.
# The editable SVG prefers the site's Pretendard / Noto Sans KR stack.
font_path = '/System/Library/Fonts/AppleSDGothicNeo.ttc'
fonts = {}
for index in range(20):
    try:
        font = ImageFont.truetype(font_path, 16, index=index)
        fonts[font.getname()[1].lower()] = index
    except OSError:
        break


def font(size, bold=False):
    return ImageFont.truetype(font_path, size, index=fonts.get('bold' if bold else 'regular', 0))


icon_data = base64.b64encode((ASSETS / 'app/icon.webp').read_bytes()).decode()
for en in [False, True]:
    name = 'tadak-legal-og-en' if en else 'tadak-legal-og'
    title = 'Documents & support' if en else '타닥타닥 문서와 지원'
    subtitle = 'Privacy · Terms · Support · Account deletion' if en else '개인정보처리방침 · 이용약관 · 지원 · 계정 삭제'
    image = Image.new('RGB', (1200, 630), PAPER)
    draw = ImageDraw.Draw(image)
    for y in [122, 490]:
        draw.line((72, y, 1128, y), fill=LINE)
    for text, x, y, size, fill, bold in [
        ('OMILSOFT', 72, 90, 23, INK, True),
        ('TADAK / DOCUMENTS', 72, 216, 16, MUTED, False),
        (title, 72, 314, 66, INK, True),
        (subtitle, 75, 380, 25, MUTED, False),
        ('eastlooo.github.io/tadak-legal/', 72, 553, 18, MUTED, False),
    ]:
        face = font(size, bold)
        draw.text((x, y), text, fill=fill, font=face, anchor='ls')
        if text in ['OMILSOFT', title]:
            draw.text((x + draw.textlength(text, font=face), y), '.', fill=COBALT, font=face, anchor='ls')
    image.paste(icon.resize((48, 48), Image.Resampling.LANCZOS), (1064, 520))
    image.save(ASSETS / f'{name}.png', optimize=True)
    svg_title = title.replace('&', '&amp;')
    (ASSETS / f'{name}.svg').write_text(f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630">
  <rect width="1200" height="630" fill="{PAPER}"/>
  <g font-family="Pretendard, Noto Sans KR, Apple SD Gothic Neo, sans-serif" fill="{INK}">
    <text x="72" y="90" font-size="23" font-weight="800">OMILSOFT<tspan fill="{COBALT}">.</tspan></text>
    <path d="M72 122H1128 M72 490H1128" stroke="{LINE}"/>
    <text x="72" y="216" font-size="16" fill="{MUTED}">TADAK / DOCUMENTS</text>
    <text x="72" y="314" font-size="66" font-weight="700">{svg_title}<tspan fill="{COBALT}">.</tspan></text>
    <text x="75" y="380" font-size="25" fill="{MUTED}">{subtitle}</text>
    <text x="72" y="553" font-size="18" fill="{MUTED}">eastlooo.github.io/tadak-legal/</text>
    <image x="1064" y="520" width="48" height="48" href="data:image/webp;base64,{icon_data}"/>
  </g>
</svg>\n''')
    print('Generated', name)
