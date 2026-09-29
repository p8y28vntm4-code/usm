# Haller-Wissen

Inoffizielle deutschsprachige Wissensbasis zum USM Haller Systemmöbel: Aufbau, Demontage, Ersatzteile, Praxis-Notizen und ein Regal-Konfigurator mit 3D-Ansicht.

Live: https://p8y28vntm4-code.github.io/usm/

## Aufbau

- `src/seiten/` – Inhalt jeder Seite (nur der Hauptteil, ohne Kopf und Fuß)
- `src/style.css` – gemeinsames Stylesheet
- `src/assets/` – Favicon und Bilder
- `src/build.py` – erzeugt daraus alle fertigen Seiten, `style.css`, `sitemap.xml` und `robots.txt` im Hauptordner
- Hauptordner – fertige Website, wird von GitHub Pages (Branch `main`, Ordner `/`) ausgeliefert

## Seite ändern

1. Datei in `src/seiten/` oder `src/style.css` bearbeiten
2. `python3 src/build.py` ausführen (Python 3, keine weiteren Pakete nötig)
3. Änderungen committen und pushen, nach 1–2 Minuten ist die Seite aktualisiert

Navigation, Seitentitel und Footer stehen in `src/build.py`.

Keine Verbindung zur USM U. Schärer Söhne AG. „USM“ und „USM Haller“ sind Marken ihrer jeweiligen Inhaber.
