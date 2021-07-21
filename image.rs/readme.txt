Wenn das Bild sich im gleichen Verzeichnis wie ecvb_bildverarbeitung.exe befindet, wird nur der Name der Datei (inklusive Dateityp) und kein Pfad benötigt.
Das eingegebene Bild muss größer als 200x200 Pixel groß sein.
Die eingegebenen Farbwerte sind im u8 RGB Farbraum und müssen somit zwischen 0 und 255 liegen.
Ob die folgende Rotationsmatrix normalisiert werden soll, um das Bild nicht zu skalieren, muss mit y = ja oder n = nein angegeben werden.
Die Werte der Rotationsmatrix sind im f32 Zahlenraum und werden in der Reihenfolge x1,y1,x2,y2 angegeben.
Das veränderte Bild wird dann als output.png im gleichen Verzeichnis wie ecvb_bildverarbeitung.exe gespeichert.

Der Sourcecode Befindet sich in src/main.rs.