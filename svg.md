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
```XML
<?xml version="1.0" encoding="UTF-8"?>\n<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="1000">
```
### Linie:
```XML
<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{width}" />
```
### Recheck:
```XML
<rect width="{width}" height="{height}" fill="{colour}" />
```
### Verschieben:
```XML
<g transform="translate({x},{y})">
```
### Drehen:
```XML
<g transform="rotate({rot},{x},{y})">
```

### Sonstiges:
Kreis, Elipse, Polygon, Text, ...


## Einbettung
### Deklaration:
```PYTHON
def __init__(self, file: str):
    self.svg_header = '<?xml version="1.0" encoding="UTF-8"?>\n<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="1000">'
    self.svg_footer = '</svg>'
```

### Linie:
```PYTHON
def line(self, x1: float, y1: float, x2: float, y2: float, width: float, colour: str):
    return f'<line x1="{str(x1)}" y1="{str(y1)}" x2="{str(x2)}" y2="{str(y2)}" stroke="{colour}" stroke-width="{str(width)}" />'
```

### Rechteck:
```PYTHON
def rect(self, width: float, height: str, colour: str):
    return f'<rect width="{str(width)}" height="{str(height)}" fill="{colour}" />'
```
