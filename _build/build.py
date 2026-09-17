#!/usr/bin/env python3
"""Dragon Digest — rebuild in "atlante naturalistico" layout.

Reads the pristine site (SRC), writes the restyled one (DST). Idempotent:
always starts from SRC, never from its own output.
"""
import html
import re
import subprocess
import sys
from pathlib import Path

SRC = Path("/home/web/daily-owl")
HERE = Path(__file__).resolve().parent
DST = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "site"
PLATES = HERE / "plates"

GA = """<script async src="https://www.googletagmanager.com/gtag/js?id=G-38HZZ4H6KR"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-38HZZ4H6KR');
</script>"""

FONTS = """<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500;1,600&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,500;0,8..60,600;1,8..60,400&display=swap" rel="stylesheet">"""

# slug, short nav label, species (latin), common name, crop (top%, bottom%)
GROUPS = [
    ("Mente e società", [
        ("bourdieu-gusto", "Bourdieu: il gusto", "Pavo cristatus", "pavone", (15, 82)),
        ("rehearsal-system", "Il Rehearsal System", "Bos taurus", "bovino che rumina", (8, 80)),
        ("sapolsky-1", "Sapolsky 1/3", "Papio anubis", "babbuino verde", (4, 87)),
        ("sapolsky-2", "Sapolsky 2/3", "Encephalon", "studio anatomico", (0, 91)),
        ("sapolsky-3", "Sapolsky 3/3", "Equus quagga", "zebra di pianura", (4, 89)),
        ("self-domestication", "Auto-domesticazione", "Vulpes vulpes", "volpe argentata", (4, 88)),
        ("tim-ferriss-fame", "Non diventare famosi", "Actias luna", "falena luna", None),
        ("existentially-starving", "You're Not Burnt Out", "Nepenthes", "pianta carnivora", (0, 90)),
        ("aiws-syndrome", "La sindrome di Alice", "Amanita muscaria", "ovolo malefico", (4, 86)),
    ]),
    ("Macchine", [
        ("leyline-protocol", "Il Protocollo Leyline", "Falco peregrinus", "falco pellegrino", (0, 90)),
        ("amanda-askell-ai-philosophy", "Askell on AI Philosophy", "Octopus vulgaris", "polpo comune", None),
        ("ai-agents-eating-saas", "Gli agent e il SaaS", "Locusta migratoria", "locusta", None),
        ("ai-energy-footprint", "Quanto consuma ChatGPT?", "Archilochus colubris", "colibrì", None),
        ("ai-newton", "AI-Newton", "Malus domestica", "melo", (8, 86)),
        ("microservices-to-monolith", "Addio microservices", "Physalia physalis", "caravella portoghese", (0, 90)),
        ("calm-tech-indieweb", "Calm Tech e l'Indieweb", "Cornu aspersum", "chiocciola", None),
    ]),
    ("Numeri e cosmo", [
        ("sfera-di-riemann", "La Sfera di Riemann", "Radiolaria", "radiolario", None),
        ("block-universe", "Il Block Universe", "Ammonoidea", "ammonite", None),
        ("decss-illegal-prime", "The Illegal Prime", "Magicicada", "cicala periodica", None),
    ]),
]
# inline plates: old filename stem -> (alt, crop)
INLINE = {
    "ai-agents-eating-saas-03": ("Formiche tagliafoglie in fila su un rametto", None),
    "ai-energy-footprint-03": ("Api su un frammento di favo", (6, 80)),
    "ai-newton-03": ("Sfinge dalla lunga spirotromba su un'orchidea bianca", (4, 82)),
    "aiws-syndrome-02": ("Camaleonte su un ramo", None),
    "aiws-syndrome-03": ("Libellula ad ali aperte, vista dorsale", (2, 88)),
    "amanda-askell-ai-philosophy-03": ("Pappagallo cenerino su un posatoio", (4, 79)),
    "block-universe-03": ("Libellula fossile in una lastra di calcare", None),
    "bourdieu-gusto-02": ("Uccello accanto al nido con uova azzurre", (8, 80)),
    "bourdieu-gusto-03": ("Un passeriforme imbecca un pulcino più grande di lui nel nido", (10, 76)),
    "calm-tech-indieweb-03": ("Felce con una fronda che si srotola", None),
    "decss-illegal-prime-03": ("Capolino di girasole con le spirali dei semi", None),
    "existentially-starving-03": ("Ghianda germogliata con radici e prime foglie di quercia", (4, 90)),
    "leyline-protocol-02": ("Pesce pagliaccio tra i tentacoli di un anemone", (6, 82)),
    "leyline-protocol-03": ("Funghi di bosco uniti sottoterra da micelio e radici", (2, 89)),
    "microservices-to-monolith-03": ("Ramo di corallo rosso", (6, 84)),
    "rehearsal-system-03": ("Biscia arrotolata su se stessa", None),
    "sapolsky-1-03": ("Madre babbuino con il piccolo", (2, 85)),
    "sapolsky-2-03": ("Neurone di Purkinje con i dendriti ramificati", (6, 84)),
    "sapolsky-3-03": ("Soffione di tarassaco con i semi che volano via", (4, 88)),
    "self-domestication-03": ("Crani di lupo e di cane a confronto", None),
    "sfera-di-riemann-03": ("Conchiglia a spirale logaritmica", (4, 81)),
    "tim-ferriss-fame-03": ("Paguro che si ritira nella conchiglia", (8, 75)),
}

# source url -> (lead, title, (author, venue))
SOURCES = {
    "https://neilthanedar.com/youre-not-burnt-out-youre-existentially-starving/": (
        "Questo saggio nasce dalle riflessioni su",
        "You’re Not Burnt Out. You’re Existentially Starving.",
        ("Neil Thanedar", "<em>neilthanedar.com</em> &middot; 21 dicembre 2025 &middot; in inglese")),
    "https://tim.blog/2020/02/02/reasons-to-not-become-famous/": (
        "Questo saggio nasce dalle riflessioni su",
        "11 Reasons Not to Become Famous (or “A Few Lessons Learned Since 2007”)",
        ("Tim Ferriss", "<em>The Blog of Author Tim Ferriss</em> &middot; 2 febbraio 2020 &middot; in inglese")),
    "https://alexsci.com/blog/calm-tech-discover/": (
        "Questo saggio nasce dalle riflessioni su",
        "Discovering the indieweb with calm tech",
        ("Robert Alexander", "<em>Built on Shards of Silicon</em>, alexsci.com &middot; in inglese")),
    "https://arxiv.org/abs/2504.01538": (
        "Questo saggio nasce dalle riflessioni su",
        "AI-Newton: A Concept-Driven Physical Law Discovery System without Prior Physical Knowledge",
        ("You-Le Fang, Dong-Shan Jian, Xiang Li, Yan-Qing Ma", "<em>arXiv</em> 2504.01538 &middot; 2 aprile 2025 &middot; in inglese")),
    "https://www.youtube.com/watch?v=BKO8ePwqWm8": (
        "Questa seconda parte nasce da",
        "La coevoluzione di umani e intelligenza artificiale",
        ("Telmo Pievani", "editoriale per <em>Lucy sui mondi</em> &middot; video su YouTube")),
}


def source_block(m):
    url = m.group(1)
    lead, title, (author, venue) = SOURCES[url]
    return f"""<aside class="sources">
              <span class="sources-label">Fonte</span>
              <p class="sources-lead">{lead}</p>
              <p class="sources-title"><a href="{url}" rel="noopener">{title}</a></p>
              <p class="sources-by"><span class="sources-author">{author}</span>{venue}</p>
            </aside>"""


def inline_plate(m):
    stem = m.group(1)
    alt, crop = INLINE[stem]
    make_plate(stem, crop, DST / "assets" / "plates" / f"{stem}.webp", width=1100)
    return (f'<figure class="essay-image plate-frame">\n            '
            f'<img src="../../assets/plates/{stem}.webp" alt="Tavola naturalistica: {alt}." loading="lazy">\n'
            f'        </figure>')


DEFAULT_CROP = (6, 86)
ROMAN = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII",
         "XIII", "XIV", "XV", "XVI", "XVII", "XVIII", "XIX", "XX"]


def make_plate(slug, crop, out, width=1400):
    # crop away the fake captions Flux prints along the bottom edge of the sheet
    top, bottom = crop or DEFAULT_CROP
    src = PLATES / f"{slug}.png"
    w, h = map(int, subprocess.check_output(
        ["identify", "-format", "%w %h", str(src)]).split())
    box = f"{int(w * .96)}x{int(h * (bottom - top) / 100)}+{int(w * .02)}+{int(h * top / 100)}"
    subprocess.run(["convert", str(src), "-crop", box, "+repage",
                    "-resize", f"{width}x", "-quality", "82", str(out)], check=True)


def nav(active, prefix):
    out = ['<details class="taxon-nav" id="taxon-nav">',
           '  <summary class="taxon-nav-title">' + MARK + 'Dragon Digest</summary>',
           f'  <a href="{prefix}" class="taxon-index-link{" active" if active is None else ""}">&larr; Indice delle tavole</a>']
    for label, items in GROUPS:
        out.append(f'  <div class="taxon-group">\n    <p class="taxon-group-label">{label}</p>')
        for slug, short, *_ in items:
            cls = "taxon-link active" if slug == active else "taxon-link"
            out.append(f'    <a href="{prefix}{slug}/" class="{cls}">{html.escape(short, quote=False)}</a>')
        out.append("  </div>")
    out.append("</details>")
    return "\n".join(out)


MARK = ('<svg class="mark" xmlns="http://www.w3.org/2000/svg" viewBox="12 5 34 38" aria-hidden="true">'
        '<g fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round">'
        '<path d="M35 40 C20 39, 17 31, 24 25 C31 19, 29 11, 18 9" stroke-width="3"/>'
        '<path d="M24 25 C27 15, 34 10, 42 10" stroke-width="2"/>'
        '<path d="M42 10 C42 17, 38 23, 30 27" stroke-width="2.6" stroke-dasharray="0.2 4.4"/></g></svg>')

NAV_JS = """<script>
  (function(){var n=document.getElementById('taxon-nav');
  if(n&&window.matchMedia('(min-width: 861px)').matches){n.open=true;}})();
</script>"""


def head(title, desc, css):
    return f"""<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="alternate" type="application/rss+xml" title="Dragon Digest" href="/feed.xml">
{FONTS}
<link rel="stylesheet" href="{css}">
{GA}
</head>"""


def build_essay(slug, short, species, common, crop, number):
    src = (SRC / "it" / slug / "index.html").read_text()
    title = re.search(r"<title>(.*?)</title>", src, re.S).group(1).strip()
    desc = re.search(r'<meta name="description" content="(.*?)"', src, re.S).group(1)
    h1 = re.search(r"<h1>(.*?)</h1>", src, re.S).group(1).strip()
    body = src.split("</header>", 1)[1].split('<footer class="site-footer">', 1)[0]
    disclosure = re.search(r'<div class="ai-disclosure">(.*?)</div>', src, re.S).group(1).strip()

    # the opening figure becomes the naturalist plate; the others stay, framed
    body = re.sub(r'\s*<figure class="essay-image">.*?</figure>', "", body, count=1, flags=re.S)
    body = re.sub(r'<figure class="essay-image">\s*<img src="[^"]*/([^"/]+)\.webp"[^>]*>\s*</figure>',
                  inline_plate, body)
    body = re.sub(r'<p><a href="(https?://[^"]+)">[^<]*</a></p>',
                  lambda m: source_block(m) if m.group(1) in SOURCES else m.group(0), body)

    make_plate(slug, crop, DST / "assets" / "plates" / f"{slug}.webp")

    page = f"""{head(title, desc, "../../style.css")}
<body>
<div class="page">

{nav(slug, "../")}

  <main class="leaf">

    <div class="running-head">
      <span>Dragon Digest</span>
      <span>Tavola {number} &middot; saggio</span>
    </div>

    <figure class="plate-frame">
      <img src="../../assets/plates/{slug}.webp" alt="Tavola naturalistica: {species}, {common}." width="1400">
    </figure>

    <p class="plate-number">Tavola {number} &middot; <em>{species}</em>, {common}</p>
    <h1>{h1}</h1>

    <div class="rule"></div>
{body.rstrip()}

    <div class="callout">
      <span class="callout-label">Trasparenza</span>
      <p>{disclosure}</p>
    </div>

    <footer>
      <span><a href="../">Dragon Digest</a> &middot; <a href="https://giobi.com">giobi.com</a></span>
      <span>it/{slug}</span>
    </footer>

  </main>
</div>
{NAV_JS}
<script src="../../assets/lightbox.js" defer></script>
</body>
</html>
"""
    (DST / "it" / slug / "index.html").write_text(page)


def build_index():
    src = (SRC / "it" / "index.html").read_text()
    excerpts, dates = {}, {}
    for sec in re.findall(r'<section class="date-section">(.*?)</section>', src, re.S):
        date = re.search(r'date-header">(.*?)</h2>', sec).group(1)
        for slug, _t, ex in re.findall(
                r'<a href="([^"/]+)/">(.*?)</a></h3>\s*<p class="essay-excerpt">(.*?)</p>', sec, re.S):
            excerpts[slug], dates[slug] = ex.strip(), date
    titles = dict(re.findall(r'<a href="([^"/]+)/">(.*?)</a></h3>', src))

    make_plate("dragon", (8, 84), DST / "assets" / "plates" / "dragon.webp")

    sections, n = [], 0
    for label, items in GROUPS:
        cards = []
        for slug, _short, species, common, _crop in items:
            cards.append(f"""      <a href="{slug}/" class="index-card">
        <div class="thumb-frame"><div class="sheet"><img src="../assets/plates/{slug}.webp" alt="{species}, {common}"></div></div>
        <p class="card-plate-no">Tavola {ROMAN[n]} &middot; <em>{species}</em></p>
        <h3>{titles[slug]}</h3>
        <p class="card-blurb">{excerpts[slug]}</p>
      </a>""")
            n += 1
        sections.append(f'    <p class="index-section-label">{label}</p>\n    <div class="index-grid">\n'
                        + "\n".join(cards) + "\n    </div>")

    page = f"""{head("Dragon Digest", "Essays by Giobi × AI. Riflessioni, framework, idee.", "../style.css")}
<body>
<div class="page">

{nav(None, "./")}

  <main class="leaf">

    <div class="running-head">
      <span>Dragon Digest</span>
      <span>Indice delle tavole</span>
    </div>

    <figure class="plate-frame frontispiece hung">
      <img src="../assets/plates/dragon.webp" alt="Tavola naturalistica: Draco volans, il drago volante." width="1400">
    </figure>

    <p class="plate-number">Frontespizio &middot; <em>Draco volans</em></p>
    <div class="masthead-mark">{MARK}</div>
    <h1>Dragon Digest</h1>
    <p class="common-name">essays by Giobi &times; AI</p>

    <div class="index-intro">
      <p>Diciannove saggi su mente, macchine e numeri, ordinati come le tavole di un
      atlante naturalistico: a ogni saggio il suo esemplare.</p>
    </div>

{chr(10).join(sections)}

    <div class="callout">
      <span class="callout-label">Trasparenza</span>
      <p>Tutti i saggi sono scritti in collaborazione con AI. Ogni articolo indica il modello usato.</p>
    </div>

    <footer>
      <span>by <a href="https://giobi.com">giobi.com</a> &middot; <a href="/feed.xml">RSS</a></span>
      <span>it/</span>
    </footer>

  </main>
</div>
{NAV_JS}
<script src="../assets/lightbox.js" defer></script>
</body>
</html>
"""
    (DST / "it" / "index.html").write_text(page)


def main():
    (DST / "assets" / "plates").mkdir(parents=True, exist_ok=True)
    (DST / "style.css").write_text((HERE / "style.css").read_text())
    for i in (1, 2, 3):
        subprocess.run(["convert", str(PLATES / f"paper-{i}.png"), "-resize", "900x", "-quality", "80",
                        str(DST / "assets" / "plates" / f"paper-{i}.webp")], check=True)
    (DST / "favicon.svg").write_text((HERE / "logo.svg").read_text())
    (DST / "assets" / "lightbox.js").write_text((HERE / "lightbox.js").read_text())
    n = 0
    for _label, items in GROUPS:
        for slug, short, species, common, crop in items:
            build_essay(slug, short, species, common, crop, ROMAN[n])
            n += 1
    build_index()
    print(f"built {n} essays + index -> {DST}")


if __name__ == "__main__":
    main()
