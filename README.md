# 📘 German A1 — Complete Guide (Roman Urdu)

Pakistan mein German seekhne walon ke liye aik **muft, mukammal A1 kitab** — har cheez
Roman Urdu mein samjhai gayi, talaffuz ke saath, aur har chapter mein practice.

- **Target**: Goethe-Zertifikat A1 / Start Deutsch 1
- **Zaban**: German content + Roman Urdu explanation aur pronunciation
- **Size**: A4, exactly 100 safhaat, colourful — magar poori tarah **black & white print safe**
  (gender M/F/N badge se aata hai, colour se nahi; har box ka apna border style hai)

## Build kaise karein

```bash
python3 build.py
```

Ye `content/*.html` ke tamam pages jorr kar `build/book.html` banata hai aur
headless Chromium se `output/German_A1_Complete_Guide_Roman_Urdu.pdf` print karta hai.

Build har dafa teen cheezein karta hai:

1. **Fehrist khud banata hai** — har page apna `toc=` / `part=` elaan karta hai, page number
   khud-ba-khud sahi lagta hai.
2. **Overflow check** — kisi page ka content A4 se bahar to nahi ja raha (page number bata deta hai).
3. **Page count check** — PDF ke pages aur likhe gaye pages barabar hain ya nahi.

## Kitab ka naqsha

| Safhaat | Kya hai |
|---|---|
| 1–5 | Cover, "kaise parhein", 3 safhon ki fehrist |
| 6–7 | German zaban aur A1 exam ka taaruf |
| 8–11 | Ch 1 — Alphabet aur awaazein |
| 12–19 | Ch 2 — Salaam dua aur apna taaruf |
| 20–27 | Ch 3 — Ginti, waqt aur tareekh |
| 28–34 | Ch 4 — Ism, article aur plural |
| 35–42 | Ch 5 — Verbs aur zamana-e-haal |
| 43–47 | Ch 6 — Jumla banane ka tareeqa |
| 48–55 | Ch 7 — Nominativ, Akkusativ aur nafi |
| 56–62 | Ch 8 — Modalverben, trennbare Verben, Imperativ |
| 63–68 | Ch 9 — Dativ aur prepositions |
| 69–74 | Ch 10 — Perfekt (guzra hua waqt) |
| 75–84 | Ch 11 — Themes ki vocabulary (10 topics) |
| 85–90 | Ch 12 — Likhna, bolna aur exam ki tayyari |
| 91–92 | 300 zaroori alfaaz ki quick sheet |
| 93–98 | 39 mashqon ke jawabat + 15 aam ghaltiyan |
| 99–100 | 60-din ka plan aur aage ka safar |

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

Marker attributes: `cls="cover"` (extra CSS class), `nofoot="1"` (footer chhupayein),
`part="…"` (fehrist mein naya chapter), `toc="…"` (fehrist mein aik line),
`tocpage="1"` (is page par fehrist khud ban jaye).
