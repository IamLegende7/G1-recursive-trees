# G1 - Rekursive Figuren / Bäume

![titel_bild](assets/image.png)


Dieses Programm erstellt rekursive Figuren und speichert sie in einer SVG datei ab.

Ihr könnt ruhig selbst mit dem Programm rumspielen.
Dafür müsst ihr nur das Programm runterladen und die konstanten Variablen in dem ```## SETTINGS ##``` Abschnitt nach belieben verändern.

## Einstellungen

*Note*: Nur ein kurzer Überblick!  
*Note*: Einige Erklärungen machen möglicheweise keinen Sinn, wenn ihr das Programm nicht versteht

| Einstellung        | mögliche Werte | Erklärung                              |
| :----------------- | :------------- | :------------------------------------- |
| **General**                                                                  |
| ```mode```         | "line", "quad" | Die Formen, die erstellt werden sollen |
| **Board**                                                                    |
| ```heigth```       | any pos. float | Die Höhe des SVGs                      |
| ```width```        | any pos. float | Die Breite des SVGs                    |
| **Size**                                                                     |
| ```initial_size``` | any pos. float | die Größe der ersten Generation        |
| ```dropoff```      | any float      | wie schnell die Größe & Linienbreite sich verändert |
| ```exponential_dropoff``` | bool | ob die Größe exponentiell kleiner werden soll |
| ```line_width```   | any pos. float | die Linienbreite, abhänging von der Länge |


## Kurzer Überblick des Programmes

Importieren des "math" modules für sinus, cosinus, pi, etc:

```python
import math
```