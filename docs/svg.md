# Erklärung des .svg Formats

**s** = scaleable

**v** = vector

**g** = grafic

## Funktion

Punkte können Kommazahlen sein,

Bild wird an Pfaden je nach Auflösung generiert

## Vorteile

nur xml (text)    ->  einfach zu generieren

vector basiert    ->  Scallierung egal

## Nutzung / Beispiele
### Init:

```xml
<?xml version="1.0" encoding="UTF-8"?>\n<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="1000">
```

### Linie:

```xml
<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{breite}" />
```

### Rechteck:

```xml
<rect x="0" y="0" width="{width}" height="{height}" fill="{colour}" />
```
*Note:* bei Rechtecken müssen x & y nicht gegeben werden; wenn nicht definiert werden sie automatisch auf 0|0 gesetzt

### Verschieben:

```xml
<g transform="translate({x},{y})">
```

### Drehen:

```xml
<g transform="rotate({rot},{x},{y})">
```

### Andere Formen:

SVG unterstüzt auch noch andere Formen:
 - Kreis, 
 - Elipse,
 - Polygon,
 - Text,
 - ...


## Nutzung in dem Projekt
### Setzen des Headers:
```python
svg_header = '<?xml version="1.0" encoding="UTF-8"?>\n<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="1000">'

to_file(svg_header)
```

### Hintergrund weiß ausfüllen:
```python
to_file(f'<rect width="{str(width)}" height="{str(height)}" fill="#FFFFFF" />')
```

### Linie:
```python
def line(self, x1: float, y1: float, x2: float, y2: float, width: float, colour: str):
    line_str = f'<line x1="{str(x1)}" y1="{str(y1)}" x2="{str(x2)}" y2="{str(y2)}" stroke="{colour}" stroke-width="{str(width)}" />'
    to_file(line_str)
```

### Setzen des Footers
```python
svg_footer = '</svg>'

to_file(svg_footer)
```

## Beispiel

Das Folgende Beispiel kann in [beispiel.svg](beispiel.svg) und als Text in [beispiel.xml](beispiel.xml) angezeigt werden.

Header mit der Größe des SVGs= 1000x1000:

```xml
<?xml version="1.0" encoding="UTF-8"?>                              <!-- xml header -->
<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="1000"> <!-- svg header -->
```
*Note*: wie zu sehen ist, erschaffen wir **hier** kein Rechteck als Hintergrund: der Hintergrund ist transparent.


Eine pinke Line von 0|0 (links oben) zu 1000|1000 (rechts unten):

```xml
<line x1="0" y1="0" x2="1000" y2="1000" stroke="#FF00FF" stroke-width="7" />
```

Ein weißes Rechteck mit w=30 h=50, mit der linken, oberen Ecke bei 10|10:

```xml
<rect x="10" y="10" width="30" height="50" fill="#FFFFFF" />
```

Ein grünes Rechteck mit w,h=100, mit der linken, oberen Ecke bei 450|450 (also mitte rechteck = mitte svg).  
Dieses drehen wir dann um 45° um 500|500

```xml
<g transform="rotate(45,500,500)"> <!-- Drehen -->
    <rect x="450" y="450" width="100" height="100" fill="#00FF00" /> <!-- Rechteck -->
</g> <!-- Drehen footer -->
```