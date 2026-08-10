from pathlib import Path


ROOT = Path(__file__).parents[1]


def test_light_and_dark_theme_contract_is_present():
    html = (ROOT / "public" / "index.html").read_text(encoding="utf-8")
    css = (ROOT / "public" / "theme.css").read_text(encoding="utf-8")
    javascript = (ROOT / "public" / "theme.js").read_text(encoding="utf-8")

    assert 'meta name="theme-color"' in html
    assert 'id="theme-toggle"' in html
    assert 'href="/theme.css"' in html
    assert 'src="/theme.js"' in html
    assert 'html[data-theme="light"]' in css
    assert 'html[data-theme="dark"]' in css
    assert ".theme-toggle:focus-visible" in css
    assert "prefers-color-scheme: dark" in javascript
    assert "aixcel-color-theme" in javascript
    assert "localStorage.setItem" in javascript
