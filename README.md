# See Colors palette patch

Copy `palette.py` into the same folder as `app.py` and `chromium_daltonize.py`.
Replace `app.py` with the provided version (which retains `chromium_daltonize` and severity handling).
Update `requirements.txt` to include `pycolornames==1.1.0`.
Install with `pip install -r requirements.txt` and restart the Flask server.

The existing `/daltonize` endpoint still returns a JPEG body. It now also includes an
`X-Color-Palettes` HTTP response header containing JSON with `original` and `daltonized`
arrays. Each entry has `hex`, `name`, and `percentage`.

`palette.py` downscales, quantizes to 32 candidate colours, and merges near shades in
OKLab space. Adjust `merge_distance=0.08` (higher merges more, lower merges less).

The percentages refer to *all pixels of the image*, not just the displayed top five.
Consequently, their sum may be less than 100%. Colors are approximate due to sampling and quantization.

Example frontend:

```ts
const header = response.headers.get('X-Color-Palettes');
const palettes = header ? JSON.parse(header) : null;
const visibleColors = tab === 'original'
  ? palettes?.original ?? []
  : palettes?.daltonized ?? [];
```

The header remains small (10 colors total); a full-image palette would require a different
response format. Keep the existing JPEG decoding and saving logic unchanged.
