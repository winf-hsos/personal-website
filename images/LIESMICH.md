# Favicon

Monogramm **NM** in Weiß auf einem Kreis in Hochschulblau (`#009ee3`).
Von Nicolas am 2026-09-21 aus vier Entwürfen gewählt.

| Datei | Zweck |
|---|---|
| `favicon.svg` | **Die Quelle.** Eingebunden über `favicon:` im `_quarto.yml` |
| `favicon-32.png` | Rückfall für Browser ohne SVG-Favicon (Safari vor 17) |
| `apple-touch-icon.png` | 180 px, Symbol auf dem iOS-Startbildschirm |
| `icon-512.png` | große Fassung, etwa als Profilbild auf anderen Kanälen |
| `favicon-erzeugen.py` | erzeugt die drei PNG aus denselben Koordinaten |

## Wenn sich etwas ändert

Die Buchstaben stehen **zweimal** im Bestand: als `polyline` im SVG und als
Koordinatenliste im Python-Skript. Wer eins ändert, ändert das andere mit —
sonst zeigen SVG- und PNG-Fassung verschiedene Zeichen.

```
python images/favicon-erzeugen.py
```

Zwei Dinge, die beim Bauen aufgefallen sind:

- **`stroke-miterlimit="2"`** ist kein Detail. Der Scheitel des N ist so spitz,
  dass eine unbegrenzte Gehrung eine lange Nadel weit über den Kreis hinaus
  zieht. Die Grenze schneidet sie ab — im SVG wie im Skript.
- **Ein einzelnes Polygon für einen Buchstaben füllt Pillow falsch**, weil der
  Umriss sich selbst schneidet. Das Skript füllt deshalb je Strichsegment ein
  Rechteck und schließt die Ecken mit einem Keil.
