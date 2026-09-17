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
           '  <summary class="taxon-nav-title">Dragon Digest</summary>',
           f'  <a href="{prefix}" class="taxon-index-link{" active" if active is None else ""}">&larr; Indice delle tavole</a>']
    for label, items in GROUPS:
        out.append(f'  <div class="taxon-group">\n    <p class="taxon-group-label">{label}</p>')
        for slug, short, *_ in items:
            cls = "taxon-link active" if slug == active else "taxon-link"
            out.append(f'    <a href="{prefix}{slug}/" class="{cls}">{html.escape(short, quote=False)}</a>')
        out.append("  </div>")
    out.append("</details>")
    return "\n".join(out)


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
    body = body.replace('<figure class="essay-image">', '<figure class="essay-image plate-frame">')

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
        <div class="thumb-frame"><img src="../assets/plates/{slug}.webp" alt="{species}, {common}"></div>
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

    <figure class="plate-frame frontispiece">
      <img src="../assets/plates/dragon.webp" alt="Tavola naturalistica: Draco volans, il drago volante." width="1400">
    </figure>

    <p class="plate-number">Frontespizio &middot; <em>Draco volans</em></p>
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
</body>
</html>
"""
    (DST / "it" / "index.html").write_text(page)


def main():
    (DST / "assets" / "plates").mkdir(parents=True, exist_ok=True)
    (DST / "style.css").write_text((HERE / "style.css").read_text())
    n = 0
    for _label, items in GROUPS:
        for slug, short, species, common, crop in items:
            build_essay(slug, short, species, common, crop, ROMAN[n])
            n += 1
    build_index()
    print(f"built {n} essays + index -> {DST}")


if __name__ == "__main__":
    main()
