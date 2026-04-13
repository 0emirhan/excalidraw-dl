# Excalidraw DL

> Download any read-only Excalidraw+ presentation as a fully editable `.excalidraw` file — directly from your browser. No server. No account. No install.

**[→ excalidraw-dl.github.io](https://0emirhan.github.io/excalidraw-dl)**

---

## Features

- One-click download of any `link.excalidraw.com/p/readonly/…` presentation
- Preserves all elements, frames, and app state
- File is named after the presentation title automatically
- Runs 100% client-side — your data never leaves your browser
- Works on Chrome, Firefox, Edge, Brave, Safari

## Usage

### Bookmarklet (recommended)

1. Visit **[the tool page](https://0emirhan.github.io/excalidraw-dl)**
2. Drag the **Excalidraw DL** button to your bookmarks bar
3. Open any read-only Excalidraw+ link
4. Click the bookmark → `.excalidraw` file downloads instantly

### Batch download (Python CLI)

For downloading multiple files at once from the command line:

```bash
pip install requests
python excalidraw_dl.py \
  https://link.excalidraw.com/p/readonly/XXXXXX \
  https://link.excalidraw.com/p/readonly/YYYYYY \
  -o ./output
```

## How it works

Excalidraw+ read-only pages are server-side rendered with Next.js. The full scene JSON is embedded in the page's RSC payload (`window.__next_f`). The bookmarklet reads this payload directly from the already-loaded page, extracts the `sceneContents` object, and triggers a browser download — no network request needed.

## Compatibility

| Platform | Status |
|----------|--------|
| `link.excalidraw.com/p/readonly/…` | ✅ Supported |
| `excalidraw.com/#json=…` | ✅ Supported (use built-in export) |
| Password-protected rooms | ❌ Not supported |

## License

[MIT](LICENSE) © 2026 [0emirhan](https://github.com/0emirhan)
