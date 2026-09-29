import pathlib, html, shutil, hashlib, datetime
SRC = pathlib.Path(__file__).resolve().parent      # src/
OUT = SRC.parent                                    # Repo-Wurzel = GitHub-Pages-Ausgabe
BASIS = 'https://p8y28vntm4-code.github.io/usm/'
VERSION = hashlib.md5((SRC / 'style.css').read_bytes()).hexdigest()[:8]  # Cache-Buster

PAGES = [
  # slug, title, description
  ('index', 'Haller-Wissen', 'Inoffizielle Wissensbasis zum USM Haller Systemmöbel: Aufbau, Demontage, Ersatzteile, Regal-Konfigurator und Praxiswissen.'),
  ('system', 'System & Technik · Haller-Wissen', 'Kugel, Rohr, Verbinder, Sonderrohre und Metallelemente verständlich erklärt.'),
  ('werkzeug', 'Werkzeug · Haller-Wissen', 'Welches Werkzeug du für Aufbau, Umbau und Demontage wirklich brauchst.'),
  ('aufbau', 'Aufbau-Guide · Haller-Wissen', 'Schritt für Schritt vom Querträger zum nivellierten Regal.'),
  ('konfigurator', 'Regal-Konfigurator · Haller-Wissen', 'Regal in 3D planen: Raster, Farben, Wände, Türen, Stückliste mit Artikelnummern.'),
  ('rechner', 'Teilerechner · Haller-Wissen', 'Stückliste für ein Regal aus Breite, Höhe und Tiefe berechnen.'),
  ('demontage', 'Demontage & Umzug · Haller-Wissen', 'Festsitzende Verbinder lösen, Vor-1990-Keile zerlegen, sicher umziehen.'),
  ('elemente', 'Tablare & Wände · Haller-Wissen', 'Metallelemente einsetzen, Rückwände ausbauen, Klemmhalter-Raster.'),
  ('tueren', 'Türen & Schlösser · Haller-Wissen', 'Klapptür, Einschubtür, Schiebetür und Glastür montieren und justieren.'),
  ('komponenten', 'Auszüge & Schubladen · Haller-Wissen', 'Auszugtablare, Schubladen, Hängeregister, Schrägablage und Inos.'),
  ('vitrine', 'Glasvitrine · Haller-Wissen', 'Glaselemente klemmen, Glastüren justieren, LED-Beleuchtung.'),
  ('sicherheit', 'Sicherheit & Wartung · Haller-Wissen', 'Wandverankerung, Gegengewichte, Traglasten und Wartung.'),
  ('ersatzteile', 'Ersatzteile · Haller-Wissen', 'Artikelnummern, Beispielpreise, Farbcodes und Bezugsquellen.'),
  ('praxis', 'Werkstatt-Notizen · Haller-Wissen', 'Erfahrungen aus Restaurierung, Gebrauchtkauf und Inventar.'),
  ('impressum', 'Impressum · Haller-Wissen', 'Anbieterkennzeichnung von Haller-Wissen.'),
  ('datenschutz', 'Datenschutz · Haller-Wissen', 'Datenschutzerklärung von Haller-Wissen.'),
  ('404', 'Seite nicht gefunden · Haller-Wissen', 'Diese Seite gibt es nicht.'),
]

# Navigation: Gruppen mit Unterseiten (slug, Name, Kurzbeschreibung)
NAV = [
  ('Grundlagen', [('system', 'System & Technik', 'Kugel, Rohr, Connie, Raster'),
                  ('werkzeug', 'Werkzeug', 'Was du wirklich brauchst'),
                  ('sicherheit', 'Sicherheit & Wartung', 'Verankerung, Traglasten')]),
  ('Anleitungen', [('aufbau', 'Aufbau-Guide', 'Vom Querträger zum Regal'),
                   ('demontage', 'Demontage & Umzug', 'Festsitzende Connies lösen'),
                   ('elemente', 'Tablare & Wände', 'Bleche, Klemmhalter-Raster'),
                   ('tueren', 'Türen & Schlösser', 'Klapp-, Einschub-, Glastür'),
                   ('komponenten', 'Auszüge & Schubladen', 'Auszüge, Register, Inos'),
                   ('vitrine', 'Glasvitrine', 'Glas klemmen, LED-Licht')]),
  ('Planen', [('konfigurator', 'Regal-Konfigurator', '3D, Türen, Stückliste'),
              ('rechner', 'Teilerechner', 'Nur die Mengen, schnell')]),
  (None, [('ersatzteile', 'Ersatzteile', '')]),
  (None, [('praxis', 'Praxis', '')]),
]

def nav(cur, pfx=''):
    teile = []
    for gi, (gruppe, eintraege) in enumerate(NAV):
        if gruppe is None:
            s, name, _ = eintraege[0]
            cur_attr = ' aria-current="page"' if s == cur else ''
            teile.append(f'<li><a href="{pfx}{s}.html"{cur_attr}>{name}</a></li>')
            continue
        aktiv = any(s == cur for s, _, _ in eintraege)
        ac = ' aria-current="page"'
        links = ''.join(
            f'<li><a href="{pfx}{s}.html"{ac if s == cur else ""}>{n}<small>{d}</small></a></li>'
            for s, n, d in eintraege)
        teile.append(f'<li class="grp{" aktiv" if aktiv else ""}"><button type="button" class="grp-btn" aria-expanded="false" aria-controls="grp-{gi}">{gruppe}</button>'
                     f'<ul class="grp-list" id="grp-{gi}">{links}</ul></li>')
    return f'''<script>document.documentElement.classList.add('js')</script>
<header class="kopf"><div class="nav-inner">
<a class="logo" href="{pfx}index.html"><span class="dot" aria-hidden="true"></span>Haller-Wissen</a>
<button type="button" class="nav-toggle" aria-expanded="false" aria-controls="hauptnav">Menü</button>
<nav id="hauptnav" aria-label="Hauptnavigation"><ul class="nav-top">{''.join(teile)}</ul></nav>
<a class="btn btn-primary btn-sm nav-cta" href="{pfx}konfigurator.html">Regal planen</a>
</div></header>
<main id="top">
'''

NAV_JS = '''<script>
(function(){
  var kopf = document.querySelector('.kopf'), tog = document.querySelector('.nav-toggle');
  var grps = [].slice.call(document.querySelectorAll('.kopf .grp'));
  function zu(ausser){ grps.forEach(function(g){ if (g !== ausser){ g.classList.remove('open'); g.querySelector('.grp-btn').setAttribute('aria-expanded','false'); } }); }
  grps.forEach(function(g){
    var b = g.querySelector('.grp-btn');
    b.addEventListener('click', function(e){ e.stopPropagation(); var auf = !g.classList.contains('open'); zu(g); g.classList.toggle('open', auf); b.setAttribute('aria-expanded', auf ? 'true' : 'false'); });
  });
  document.addEventListener('click', function(e){ if (!e.target.closest('.kopf .grp')) zu(null); });
  document.addEventListener('keydown', function(e){ if (e.key === 'Escape'){ zu(null); if (kopf.classList.contains('nav-open')){ kopf.classList.remove('nav-open'); tog.setAttribute('aria-expanded','false'); tog.focus(); } } });
  tog.addEventListener('click', function(){ var auf = !kopf.classList.contains('nav-open'); kopf.classList.toggle('nav-open', auf); tog.setAttribute('aria-expanded', auf ? 'true' : 'false'); tog.textContent = auf ? 'Schließen' : 'Menü'; });
})();
</script>
'''

def foot(pfx=''):
    spalten = []
    for gruppe, eintraege in NAV[:3]:
        spalten.append(f'<div><h4>{gruppe}</h4><ul>' + ''.join(f'<li><a href="{pfx}{s}.html">{n}</a></li>' for s, n, _ in eintraege) +
                       ('<li><a href="' + pfx + 'ersatzteile.html">Ersatzteile</a></li><li><a href="' + pfx + 'praxis.html">Werkstatt-Notizen</a></li>' if gruppe == 'Planen' else '') + '</ul></div>')
    return f'''</main>
<footer><div class="footer-inner">
<div><div class="footer-logo"><span class="dot" style="width:14px;height:14px;border-radius:50%;background:radial-gradient(circle at 35% 30%,#fff 0%,#d8dbde 45%,#8d9298 100%)"></span>Haller-Wissen</div>
<p>Private, nicht-kommerzielle Wissensplattform für alle, die Haller-Möbel selbst aufbauen, umbauen, restaurieren oder Ersatzteile suchen. Alle Texte sind eigenständig formuliert, alle Angaben ohne Gewähr. Arbeiten am Möbel erfolgen auf eigene Verantwortung.</p>
<p style="margin-top:.7rem">Keine Verbindung zur USM U. Schärer Söhne AG. „USM“ und „USM Haller“ sind Marken ihrer jeweiligen Inhaber. Preise sind Beispielwerte aus Bestellungen 2024/25.</p></div>
{''.join(spalten)}
</div>
<div class="footer-bottom"><span>Inoffizielles Community-Projekt · Stand September 2026</span><span><a href="{pfx}impressum.html">Impressum</a> · <a href="{pfx}datenschutz.html">Datenschutz</a></span></div>
</footer>
{NAV_JS}'''

def kopfdaten(slug, title, desc, pfx=''):
    url = BASIS + ('' if slug == 'index' else f'{slug}.html')
    robots = '<meta name="robots" content="noindex">\n' if slug in ('404',) else ''
    return (f'<title>{html.escape(title)}</title>\n<meta name="description" content="{html.escape(desc)}">\n{robots}'
            f'<link rel="icon" href="{pfx}favicon.svg" type="image/svg+xml">\n'
            f'<meta name="theme-color" content="#24272a">\n'
            f'<meta property="og:type" content="website">\n<meta property="og:site_name" content="Haller-Wissen">\n'
            f'<meta property="og:title" content="{html.escape(title)}">\n<meta property="og:description" content="{html.escape(desc)}">\n'
            f'<meta property="og:url" content="{url}">\n<meta property="og:image" content="{BASIS}og.jpg">\n'
            f'<meta property="og:image:width" content="1200">\n<meta property="og:image:height" content="630">\n'
            f'<meta name="twitter:card" content="summary_large_image">\n'
            f'<link rel="canonical" href="{url}">\n'
            f'<link rel="stylesheet" href="{pfx}style.css?v={VERSION}">\n')

for slug, title, desc in PAGES:
    body = (SRC / 'seiten' / f'{slug}.html').read_text()
    pfx = '/usm/' if slug == '404' else ''
    head = kopfdaten(slug, title, desc, pfx)
    inhalt = nav(slug, pfx) + body + foot(pfx)
    page = ('<!doctype html>\n<html lang="de">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
            + head + '</head>\n<body>\n' + inhalt + '</body>\n</html>\n')
    (OUT / f'{slug}.html').write_text(page)
print('built', len(PAGES))


# Stylesheet und Bilder kopieren
shutil.copy(SRC / 'style.css', OUT / 'style.css')
for f in (SRC / 'assets').iterdir():
    shutil.copy(f, OUT / f.name)
(OUT / '.nojekyll').write_text('')

# Sitemap und robots.txt
heute = datetime.date.today().isoformat()
urls = ''.join(f'  <url><loc>{BASIS}{"" if s == "index" else s + ".html"}</loc><lastmod>{heute}</lastmod></url>\n'
               for s, _, _ in PAGES if s != '404')
(OUT / 'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + urls + '</urlset>\n')
(OUT / 'robots.txt').write_text(f'User-agent: *\nAllow: /\n\nSitemap: {BASIS}sitemap.xml\n')
print('fertig:', len(PAGES), 'Seiten, Sitemap, robots.txt')
