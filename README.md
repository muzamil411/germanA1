# 📘 German A1 — Complete Guide (Roman Urdu)

Pakistan mein German seekhne walon ke liye aik **muft, mukammal A1 kitab** — har cheez
Roman Urdu mein samjhai gayi, talaffuz ke saath, aur har chapter mein practice.

- **Target**: Goethe-Zertifikat A1 / Start Deutsch 1
- **Zaban**: German content + Roman Urdu explanation aur pronunciation
- **Size**: A4, ~100 safhaat, colourful (print bhi ho sakti hai)

## Build kaise karein

```bash
python3 build.py
```

Ye `content/*.html` ke tamam pages jorr kar `build/book.html` banata hai aur
headless Chromium se `output/German_A1_Complete_Guide_Roman_Urdu.pdf` print karta hai.

Build har dafa do cheezein check karta hai:

1. **Overflow** — kisi page ka content A4 se bahar to nahi ja raha (page ka number bata deta hai).
2. **Page count** — PDF ke pages aur content pages barabar hain ya nahi.

## Structure

| Path | Kya hai |
|---|---|
| `content/*.html` | Kitab ka content, file order = page order |
| `assets/style.css` | Poori kitab ka design system (colors, boxes, tables) |
| `build.py` | HTML jorrna + PDF print + validation |
| `output/` | Final PDF |

Naya page banane ke liye content file mein ye marker likhein:

```html
<!--PAGE ch="Chapter 3 · Ginti" -->
...page ka content...
```

`cls="cover"` aur `nofoot="1"` cover-type pages ke liye hain.
