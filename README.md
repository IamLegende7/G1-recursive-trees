*Note*: nicht in dieser reinfolge

*Note*: Nur ein kleiner überklick; **Ausbauen!**

## Kurzer Überblick Program

```py
from svg import SVGWriter
import math
```

* importieren von math --> sinus, cosinus & ceil (aufrunden)
* importieren von svg.py (siehe [hier](docs/svg.md))

```python
debug = False # Debug infos
```

```python
## SETTINGS ##
# Board
height = 1000
width = 1000

# Size
initial_size = 200
dropoff = 0.5

# Generations & Children
max_generations = 5
initial_children_count = 2
line_width = 4

# Spread
spread = 90
spread_dropoff = 1
do_spread_dropoff = False
keep_rotation = False
```

Einstellungen des svg schreibers, mit 'image.svg' als ausgabedatei (TODO: mehr erklärungen!):

```python
# Init
svg_writer = SVGWriter('image.svg')
svg_writer.write(svg_writer.rect(width, height, "#FFFFFF"))
```

Neue instanz der klasse SVGWriter (siehe svg.py) & ausfüllen des Hintergrunds --> weiß

```python
def node(startx: float, starty: float, generation: int, child_num: int, children_count_parent: int, rotation = None):
```

Node funktion, die wir rekursiv aufrufen werden.

Argumente:

* ```startx```, ```starty```: die position des knotenpunktes; linie, die von dieser node gemalt wird geht von P¹(startx | starty) zu P²(endx | endy)
* ```generation```: die generation dieser node; startet bei 0 --> erste node, ausgeführt von uns in zeile 78
* ```child_num```: das wievielte child der parent node dieses ist (wichtig für winkel-berechnungen)
* ```children_count_parent```: wieviele children die parent node hatte (wichtig für winkel-berechnungen)
* ```rotation```: wenn ```keep_rotation``` = true; enthält die rotation der parent node, damit die child node eine rotation dazu relativ haben kann (mach ein paar sachen einfacher; geht auch ohne diese variable)

### Mathe

![skizze_mathe](assets/bild_dreieck.png)

(Schlecht formatiert, ich weiß)

wir haben also P¹ gegeben, brauchen aber auch P²

da wir auch spread haben, können wir erstmal alpha ausrechnen: (TODO: ausfürlicher erklären)

```python
## Mathe
child_multi = child_num - math.ceil(children_count_parent / 2)
if ((children_count_parent % 2) == 0):
  if child_num <= (children_count_parent / 2): child_multi -= 1
  if child_multi < 0: child_multi += 0.5
  else: child_multi -= 0.5

if generation == 0:
  alpha = 0
else:
  if do_spread_dropoff: spread_full = (spread / (generation / (1 / spread_dropoff)))
else: 
  spread_full = spread

if (rotation is None) or (not keep_rotation):
  alpha = (            spread_full * child_multi)
else:
  alpha = (rotation + (spread_full * child_multi))
```

Nun müssen wir alpha von Degress in Radial umwandeln: (also statt 1 mal komplett rum = 360; 1 mal komplett rum = 2pi) (TODO: besser ausdrücken)

```python
alpha_rad = alpha * (math.pi / 180)
```

Daraus mit umformen:

sin(alpha) = x_offset / length --> x_offset = sin(alpha) * length
cos(alpha) = y_offset / length --> y_offset = cos(alpha) * length

in python: (sinus & cosinus von python's "math" module)

```python
x_offset = math.sin(alpha_rad) * (initial_size / (dropoff * (generation + 1)))
y_offset = math.cos(alpha_rad) * (initial_size / (dropoff * (generation + 1)))
```

Und dann P²:

```python
endx = startx + x_offset
endy = starty + y_offset
```

Malen der linie dieser node:

```python
## Drawing
svg_writer.write(svg_writer.line(startx, starty, endx, endy, (line_width / (generation + 1)), "#000000"))
```

Setzen der Anzahl der children (eintweder von der globalen variable ```initial_children_count``` oder vom parent)
und das alles nartürlich nur, wenn die derzeitige generation unter dem generationslimit liegt:

```python
if generation < max_generations:
  ## Get child count
  if generation == 0:
    children_count = initial_children_count
  else:
    children_count = children_count_parent
```

Und zu guter letzt die generation von children (immer noch in der ```if generation < max_generations:``` verzweigung):

```python
  ## Generate Children
  for i in range(children_count):
    node(endx, endy, generation+1, i+1, children_count, rotation=alpha)
```

### Zurück zum program

Entlich sind wir nun mit den deklarierungen fertig, und können die mother node aufrufen:

```python
# Generating Tree
node(startx=(width / 2), starty=0, generation=0, child_num=1, children_count_parent=1)
```

Nachdem alles fertig ist, müssen wir noch den svg footer ranhängen und den prozess mit SVGWriter abschießen:

```python
# Cleanup
svg_writer.close()
```

**und wir sind fertig!**