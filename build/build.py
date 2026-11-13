#!/usr/bin/env python3
"""Builds the Regius concept site into ../site as plain, self-contained HTML pages.

Spec mode: this is an unsolicited concept. Every page carries noindex, the staging
notice as its first element, and the footer disclosure. Nothing here is invented:
every fact traces to a source listed on about.html.
"""
import html
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import svgkit as k          # noqa: E402
from style import CSS       # noqa: E402

BASE = "https://regius.jakelabate.com/"
SITE = os.path.join(HERE, "..", "site")
OFFICIAL = "https://www.regiuscigars.com/"
COMPANIES_HOUSE = "https://find-and-update.company-information.service.gov.uk/company/06969408"

NAV = [("cigars.html", "Cigars"), ("house.html", "The house"),
       ("limited-editions.html", "Limited editions"), ("recognition.html", "Recognition"),
       ("stockists.html", "Stockists")]
FOOT = [("index.html", "Home"), ("cigars.html", "The cigars"), ("black-label.html", "Black Label"),
        ("exclusivo-usa.html", "Exclusivo U.S.A."), ("limited-editions.html", "Limited editions"),
        ("house.html", "The house"), ("recognition.html", "Recognition"),
        ("stockists.html", "Stockists"), ("about.html", "About this site")]
SECTION_OF = {"black-label.html": "cigars.html", "exclusivo-usa.html": "cigars.html"}


def esc(s):
    return html.escape(s, quote=True)


def url(page):
    return BASE if page == "index.html" else BASE + page


def og_slug(page):
    return page[:-5]


# ---------------------------------------------------------------- furniture

def head(page, title, desc, crumbs):
    u = url(page)
    og = f"{BASE}img/og/{og_slug(page)}.png"
    graph = [
        {"@type": "WebSite", "@id": BASE + "#website", "url": BASE,
         "name": "Regius Cigars concept site", "inLanguage": "en-GB",
         "description": "An unofficial concept site for Regius Cigars, the London cigar house.",
         "creator": {"@id": BASE + "#author"}, "about": {"@id": BASE + "#regius"}},
        {"@type": "Person", "@id": BASE + "#author", "name": "Jake Labate",
         "jobTitle": "SEO Consultant", "url": "https://jakelabate.com/"},
        {"@type": "Organization", "@id": BASE + "#regius", "name": "Regius Cigars",
         "legalName": "Regius Cigars Limited", "url": OFFICIAL, "foundingDate": "2010",
         "foundingLocation": {"@type": "Place", "name": "London, United Kingdom"},
         "founder": {"@type": "Person", "name": "Akhil Kapacee"},
         "slogan": "Arbiter Elegantiae", "sameAs": [COMPANIES_HOUSE]},
        {"@type": "WebPage", "@id": u + "#webpage", "url": u, "name": title, "description": desc,
         "inLanguage": "en-GB", "isPartOf": {"@id": BASE + "#website"},
         "about": {"@id": BASE + "#regius"}},
    ]
    if crumbs:
        items = [{"@type": "ListItem", "position": i + 1, "name": n, "item": url(p)}
                 for i, (p, n) in enumerate(crumbs)]
        graph[-1]["breadcrumb"] = {"@id": u + "#breadcrumb"}
        graph.append({"@type": "BreadcrumbList", "@id": u + "#breadcrumb", "itemListElement": items})
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=1)
    canonical = "" if page == "404.html" else f'<link rel="canonical" href="{u}">\n'
    base = f'<base href="{BASE}">\n' if page == "404.html" else ""
    return f"""<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
{base}<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
{canonical}<meta property="og:type" content="website">
<meta property="og:site_name" content="Regius Cigars concept site">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{u}">
<meta property="og:image" content="{og}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{esc(title)}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{og}">
<meta name="theme-color" content="#090807">
<link rel="icon" href="favicon.ico" sizes="any">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<link rel="stylesheet" href="fonts/fonts.css">
<link rel="preload" as="font" type="font/woff2" href="fonts/libre-caslon-display-latin-400-normal.woff2" crossorigin>
<link rel="preload" as="font" type="font/woff2" href="fonts/libre-caslon-text-latin-400-normal.woff2" crossorigin>
<style>{CSS}</style>
<script type="application/ld+json">
{ld}
</script>
</head>
"""


def header(page):
    here = SECTION_OF.get(page, page)
    items = []
    for href, label in NAV:
        attr = ""
        if href == page:
            attr = ' aria-current="page"'
        elif href == here:
            attr = ' class="here"'
        items.append(f'<li><a href="{href}"{attr}>{label}</a></li>')
    return f"""<body>
<div class="notice"><div class="wrap"><b>Staging site.</b><p>A proposal for Regius Cigars. <a href="about.html">About this site</a></p></div></div>
<a class="skip" href="#main">Skip to content</a>
{k.DEFS}
<header class="head lid"><div class="wrap">
<a class="wordmark" href="index.html" aria-label="Regius, home">REGIUS</a>
<nav class="nav" aria-label="Main"><ul>{''.join(items)}</ul></nav>
</div></header>
"""


def footer():
    links = "".join(f'<li><a href="{h}">{n}</a></li>' for h, n in FOOT)
    return f"""<footer class="lid"><div class="edge"></div><div class="wrap foot-wrap">
<div class="foot-grid">
<div>
<p class="foot-mark" aria-hidden="true">REGIUS</p>
<p class="quiet"><i lang="la">Arbiter elegantiae</i>, judge of elegance. A London cigar house whose cigars are rolled by hand in Estel&iacute;, Nicaragua.</p>
</div>
<nav aria-label="All pages"><ul class="foot-nav">{links}</ul></nav>
<div class="small">
<p class="disclaimer">Unofficial concept site. Not affiliated with or commissioned by Regius Cigars.</p>
<p class="quiet">For adults of legal smoking age only. Smoking tobacco harms your health.</p>
</div>
</div>
<div class="legal">
<p>Concept by <a href="https://jakelabate.com/">Jake Labate, SEO Consultant</a></p>
<p><a href="about.html">Sources and method</a></p>
</div>
</div></footer>
<dialog class="gate" id="gate" aria-labelledby="gate-h">
<p class="gate-mark" aria-hidden="true">REGIUS</p>
<h2 id="gate-h">Are you old enough to buy tobacco where you live?</h2>
<p>This site is about cigars and is meant for adults of legal smoking age.</p>
<div class="gate-actions" id="gate-actions">
<button class="btn btn-gold" id="gate-yes" type="button">Yes, I am of legal age</button>
<button class="btn btn-plain" id="gate-no" type="button">No, I am not</button>
</div>
<p class="gate-msg" id="gate-msg" hidden>This site is only for adults of legal smoking age.</p>
<p class="gate-note">Staging site. A proposal for Regius Cigars, not affiliated with or commissioned by them.</p>
</dialog>
<script>
(function(){{
  var d=document.getElementById('gate');
  if(!d||!d.showModal)return;
  var ok=false;
  try{{ok=localStorage.getItem('regius-age')==='yes'}}catch(e){{}}
  if(ok)return;
  d.showModal();
  d.addEventListener('cancel',function(e){{e.preventDefault()}});
  document.getElementById('gate-yes').addEventListener('click',function(){{
    try{{localStorage.setItem('regius-age','yes')}}catch(e){{}}
    d.close();
  }});
  document.getElementById('gate-no').addEventListener('click',function(){{
    document.getElementById('gate-actions').hidden=true;
    document.getElementById('gate-msg').hidden=false;
  }});
}})();
</script>
</body>
</html>
"""


def page_head(crumbs, h1, lede):
    trail = "".join(
        f'<li><a href="{p}">{n}</a></li>' if i < len(crumbs) - 1 else f'<li aria-current="page">{n}</li>'
        for i, (p, n) in enumerate(crumbs))
    return f"""<section class="page-head lid"><div class="wrap">
<nav class="crumbs" aria-label="Breadcrumb"><ol>{trail}</ol></nav>
<h1>{h1}</h1>
<p class="lede">{lede}</p>
</div></section>
<div class="edge"></div>
"""


def write(page, title, desc, body, crumbs=None):
    out = head(page, title, desc, crumbs) + header(page) + f'<main id="main">\n{body}\n</main>\n' + footer()
    for bad in (chr(0x2014), chr(0x2013)):
        assert bad not in out, f"dash found in {page}"
    with open(os.path.join(SITE, page), "w", encoding="utf-8") as fh:
        fh.write(out)
    return out


# ---------------------------------------------------------------- pieces

def size_txt(length, ring, ring2=None):
    r = f"{ring} to {ring2}" if ring2 else f"{ring}"
    return f"{length} in &times; {r}"


def mm_txt(length, ring, ring2=None):
    d = f"{k.mm_dia(ring)} to {k.mm_dia(ring2)}" if ring2 else f"{k.mm_dia(ring)}"
    return f"{k.mm_len(length)} mm &times; {d} mm"


def vitola_table(caption, rows, leaf, band, second=None):
    """rows: dicts with name, length, ring and optional note, shape, ring2, leaf, band, culebra."""
    trs = []
    for r in rows:
        lf = r.get("leaf", leaf)
        label = f"{r['name']}, {r['length']} inches by {r['ring']} ring gauge, drawn to scale"
        if r.get("culebra"):
            art = k.culebra(r["length"], r["ring"], r["culebra"], label=label)
        else:
            art = k.cigar(r["length"], r["ring"], lf, shape=r.get("shape", "parejo"),
                          band=r.get("band", band), second=r.get("second", second),
                          ring2=r.get("ring2"), label=label)
        note = f'<span class="note">{r["note"]}</span>' if r.get("note") else ""
        trs.append(
            f'<tr><th scope="row">{r["name"]}{note}</th>'
            f'<td class="dim">{size_txt(r["length"], r["ring"], r.get("ring2"))}'
            f'<span class="note">{mm_txt(r["length"], r["ring"], r.get("ring2"))}</span></td>'
            f'<td class="draw">{art}</td></tr>')
    return f"""<table class="vitolas stack">
<caption class="sr">{caption}</caption>
<colgroup><col class="c-name"><col class="c-dim"><col class="c-draw"></colgroup>
<thead><tr><th scope="col">Size</th><th scope="col">Length by ring gauge</th><th scope="col">Drawn to scale</th></tr></thead>
<tbody>
{''.join(trs)}
</tbody>
<tfoot><tr><td colspan="2">One scale for every drawing. The ruler is in inches.</td><td class="draw">{k.ruler_svg()}</td></tr></tfoot>
</table>"""


def spec(pairs):
    return '<dl class="spec">' + "".join(f"<dt>{a}</dt><dd>{b}</dd>" for a, b in pairs) + "</dl>"


def ext(href, text):
    return f'<a href="{href}" rel="noopener">{text}</a>'


# ---------------------------------------------------------------- data

BLACK_ROWS = [
    {"name": "Chicos", "length": "4 3/8", "ring": 32, "note": "Tins of ten", "band": None},
    {"name": "Petit Robusto", "length": "4", "ring": 50, "note": "Boxes of ten. First listed as the Short Robusto."},
    {"name": "Robusto", "length": "4 7/8", "ring": 50, "note": "Boxes of 25, or ten in tubes"},
    {"name": "Corona", "length": "5 1/8", "ring": 42, "note": "Boxes of 25"},
    {"name": "Culebra", "length": "5 3/4", "ring": 39, "note": "Three cigars twisted together, each in a different wrapper. Boxes of three culebras.",
     "culebra": ["claro", "oscuro", "connecticut"]},
    {"name": "Lord Madsen", "length": "6", "ring": 38, "note": "Boxes of 25"},
    {"name": "Gran Toro", "length": "6 1/2", "ring": 56},
    {"name": "Grandido", "length": "7", "ring": 47, "note": "Boxes of 25"},
]

EXCL_ROWS = [
    {"name": "Robusto", "length": "4 1/2", "ring": 52},
    {"name": "Fat Perfecto", "length": "5 3/4", "ring": 54, "ring2": 60, "shape": "fatperfecto",
     "note": "The one size never box-pressed"},
    {"name": "Toro", "length": "6", "ring": 52},
    {"name": "Pressed Perfecto", "length": "6 1/2", "ring": 54, "shape": "perfecto",
     "note": "Closed at both ends. No. 21 in Cigar Aficionado's Top 25 of 2017."},
    {"name": "Toro Extra", "length": "6 1/2", "ring": 56},
    {"name": "Lancero Extra", "length": "7 1/2", "ring": 42},
]

CONN_ROWS = [
    {"name": "Robusto", "length": "4 7/8", "ring": 50},
    {"name": "Corona", "length": "5 1/8", "ring": 42},
    {"name": "Toro", "length": "6", "ring": 52},
    {"name": "Gran Toro", "length": "6 1/2", "ring": 52},
    {"name": "Grandido", "length": "7", "ring": 47},
]
SUN_ROWS = [
    {"name": "Corona", "length": "5 1/8", "ring": 42},
    {"name": "Toro", "length": "6", "ring": 50},
    {"name": "Gran Toro", "length": "6 1/2", "ring": 56},
]
MADURO_ROWS = [
    {"name": "Robusto", "length": "4 7/8", "ring": 50},
    {"name": "Corona", "length": "5 1/8", "ring": 42},
    {"name": "Toro", "length": "6", "ring": 50},
    {"name": "Gran Toro", "length": "6 1/2", "ring": 56},
    {"name": "Grandido", "length": "7", "ring": 47},
]
RESERVA_ROWS = [
    {"name": "Robusto Gordo", "length": "5 1/2", "ring": 55, "note": "2021 edition. Black lacquered boxes of 20."},
]

LINES = [
    ("black-label.html", "Black Label", "colorado", "black",
     "The first Regius cigar, sold in Britain since 2010. A medium-bodied Nicaraguan puro in eight sizes."),
    ("exclusivo-usa.html", "Exclusivo U.S.A.", "colorado", "red",
     "Three blends made for American smokers and sold only in the United States: Red, White and Blue Label."),
    ("cigars.html#connecticut", "Connecticut", "connecticut", "black",
     "A shade wrapper grown from Connecticut seed in the Talanga valley of Honduras, over Nicaraguan binder and filler."),
    ("cigars.html#sun-grown", "Sun Grown", "sungrown", "black",
     "A dark, higher-priming sun grown wrapper on an all-Nicaraguan blend, made as the fuller, bolder cigar in the range."),
    ("cigars.html#maduro", "Maduro", "maduro", "black",
     "The complexity of Black Label reworked around a maduro wrapper. Five sizes, in wide release since March 2018."),
    ("cigars.html#reserva", "Reserva", "colorado", "silver",
     "Small batches of all-Nicaraguan tobacco, aged after rolling and blended to recall the Cuban Bol&iacute;var."),
]


def lines_list():
    lis = []
    for href, name, leaf, band, what in LINES:
        lis.append(f'<li><span class="swatch sw-{leaf} bd-{band}" aria-hidden="true"></span>'
                   f'<span class="name"><a href="{href}">{name}</a></span>'
                   f'<p class="what">{what}</p></li>')
    return '<ul class="lines">' + "".join(lis) + "</ul>"


# ---------------------------------------------------------------- pages

def home():
    plates = [
        ("corona", "Corona", "5 1/8", 42),
        ("robusto", "Robusto", "4 7/8", 50),
        ("madsen", "Lord Madsen", "6", 38),
        ("grandido", "Grandido", "7", 47),
    ]
    radios = "".join(
        f'<input class="sr" type="radio" name="vitola" id="v-{key}"{" checked" if key == "robusto" else ""}>'
        for key, *_ in plates)
    tabs = "".join(f'<label for="v-{key}">{name}</label>' for key, name, *_ in plates)
    figs = []
    for key, name, length, ring in plates:
        label = f"A Regius Black Label {name}, {length} inches long and {ring} ring gauge, drawn to scale above an inch ruler"
        figs.append(
            f'<figure class="plate" data-v="{key}">{k.plate(length, ring, "colorado", label)}'
            f'<figcaption><strong>{name}.</strong> {length} inches long, {ring} ring gauge. '
            f'In metric, {k.mm_len(length)} mm by {k.mm_dia(ring)} mm. The circle at the right is the cigar seen end on.</figcaption></figure>')
    frieze = "".join('<span class="gap"></span>' if c == " " else f"<span>{c}</span>" for c in "ARBITER ELEGANTIAE")
    body = f"""<section class="hero lid"><div class="wrap">
<h1>Regius Cigars of London</h1>
<div class="hero-grid">
<dl class="facts">
<dt>Founded</dt><dd>London, 2010</dd>
<dt>Rolled in</dt><dd>Estel&iacute;, Nicaragua</dd>
<dt>Made by</dt><dd>Plasencia Cigars S.A.</dd>
<dt>Motto</dt><dd><i lang="la">Arbiter elegantiae</i></dd>
</dl>
<div>
<p class="lede">Regius is a London cigar house, founded in 2010. Its cigars are rolled by hand in Estel&iacute;, Nicaragua, by the Plasencia family, and were first blended for smokers raised on Cuban cigars. The motto on the band asks one thing of whoever is holding it: be the judge of elegance.</p>
<p class="hero-links"><a href="cigars.html">See every cigar and size</a><a href="house.html">Read about the house</a></p>
</div>
</div>
<p class="frieze" role="img" aria-label="Arbiter elegantiae">{frieze}</p>
</div></section>
<div class="edge"></div>

<section class="band tray"><div class="wrap">
<h2>Four sizes to begin with</h2>
<fieldset class="bench">
<legend class="sr">Choose a Black Label size to see it drawn to scale</legend>
{radios}
<div class="bench-tabs">{tabs}</div>
<div class="plates">{''.join(figs)}</div>
</fieldset>
<p class="more">Black Label, the first Regius blend, came to market in these four sizes. <a href="black-label.html">Black Label now runs to eight</a>.</p>
</div></section>

<section class="band lid"><div class="wrap cols">
<div class="side">
<h2>Six lines, one band</h2>
<p class="quiet">All are handmade, long-filler cigars. The swatch beside each name shows the shade of its wrapper leaf.</p>
</div>
<div>
{lines_list()}
<p class="more"><a href="cigars.html">Every blend and size, drawn to scale</a></p>
</div>
</div></section>

<section class="band tray"><div class="wrap cols">
<div class="side"><h2>The name and the motto</h2></div>
<div>
<p><i lang="la">Regius</i> is Latin for royal: of a king. The motto on the band, <i lang="la">arbiter elegantiae</i>, means judge of elegance.</p>
<p>It was the standing of Gaius Petronius at the court of Nero. Petronius gave his life to pleasure, yet Rome remembered him as a connoisseur, and the emperor took his word as final on any question of taste. Regius was named in his memory.</p>
<p>The motto hands his office to the smoker. The cigar is made; the verdict is yours.</p>
<p class="more"><a href="house.html">The house, its makers and its history</a></p>
</div>
</div></section>

<section class="band lid"><div class="wrap cols">
<div class="side">
<h2>Recognition</h2>
<p class="quiet">Results published by the cigar press, each checked at its source.</p>
</div>
<div>
<table class="ledger stack">
<caption class="sr">Selected published ratings for Regius cigars</caption>
<thead><tr><th scope="col">Year</th><th scope="col">Publication</th><th scope="col">Cigar and result</th></tr></thead>
<tbody>
<tr><th scope="row">2017</th><td data-l="Publication">Cigar Aficionado, Top 25 Cigars of the Year</td><td>Exclusivo U.S.A. Pressed Perfecto. No. 21, with 92 points.</td></tr>
<tr><th scope="row">2016</th><td data-l="Publication">Cigar Coop, Cigar of the Year Countdown</td><td>Exclusivo U.S.A. Oscuro Especial Robusto. No. 27.</td></tr>
<tr><th scope="row">2014</th><td data-l="Publication">Cigar Coop, Cigar of the Year Countdown</td><td>Exclusivo U.S.A. Claro Especial. No. 22.</td></tr>
<tr><th scope="row">2013</th><td data-l="Publication">Cigar Aficionado</td><td>White Label Royal Robusto. 90 points.</td></tr>
</tbody>
</table>
<p class="more"><a href="recognition.html">All ratings, with sources</a></p>
</div>
</div></section>

<section class="band tray"><div class="wrap cols">
<div class="side"><h2>Rolled in Estel&iacute;</h2></div>
<div>
<p>The core Regius blends are made at Plasencia Cigars S.A. in Estel&iacute;, in the mountains of northern Nicaragua. Regius describes its partners as cigar makers of Cuban descent with more than 500 rollers at the bench.</p>
<p>The tobacco is Nicaraguan, some of it aged for years before it is rolled. Regius says every cigar is checked by hand for draw and construction before it leaves the factory.</p>
<p class="more"><a href="stockists.html">Where to find Regius cigars</a></p>
</div>
</div></section>"""
    write("index.html", "Regius Cigars | London cigar house, rolled in Estelí",
          "Regius is a London cigar house founded in 2010. Its cigars are rolled by hand at Plasencia Cigars in Estelí, Nicaragua. See every blend and size.",
          body)


def cigars():
    crumbs = [("index.html", "Regius"), ("cigars.html", "The cigars")]
    robusto = k.cigar("4 7/8", 50, "colorado", label="A Black Label Robusto, 4 7/8 inches by 50 ring gauge, drawn to scale")
    pressed = k.cigar("6 1/2", 54, "colorado", shape="perfecto", band="red",
                      label="An Exclusivo U.S.A. Pressed Perfecto, 6 1/2 inches by 54 ring gauge, drawn to scale")
    body = page_head(crumbs, "The cigars",
                     "Six lines carry the Regius band. Sizes are given as length in inches by ring gauge, where one ring is 1/64 of an inch. Every drawing on this page is to one scale, so a Corona and a Gran Toro can be judged side by side.") + f"""
<section class="band tray" id="black-label"><div class="wrap stack-gap">
<div class="cols">
<div class="side"><h2>Black Label</h2></div>
<div>
<p>The original. Black Label reached British tobacconists in 2010 and is the cigar the rest of the range is measured against: a medium-bodied Nicaraguan puro, blended to give smokers of Cuban cigars something they would recognise.</p>
{spec([("Wrapper", "Nicaragua, shade grown"), ("Binder and filler", "Nicaragua"), ("Body", "Medium"), ("Sizes", "Eight, from the 4 inch Petit Robusto to the 7 inch Grandido")])}
<p class="more"><a href="black-label.html">Black Label: blend, tasting notes and all eight sizes</a></p>
</div>
</div>
<div class="draw">{robusto}{k.ruler_svg()}</div>
</div></section>

<section class="band tray ruled" id="exclusivo-usa"><div class="wrap stack-gap">
<div class="cols">
<div class="side"><h2>Exclusivo U.S.A.</h2></div>
<div>
<p>A series of three blends made for the American market and sold only there. The Red Label and the White Label, or Claro Especial, arrived in 2014. The Blue Label, or Oscuro Especial, closed the series in February 2016. All three share six sizes, two of them perfectos.</p>
{spec([("Red Label", "All Nicaraguan, with a Jalapa wrapper"), ("White Label", "All Nicaraguan, with a double binder"), ("Blue Label", "Mexican San Andr&eacute;s wrapper over Nicaraguan binder and filler"), ("Sold in", "The United States only")])}
<p class="more"><a href="exclusivo-usa.html">Exclusivo U.S.A.: the three blends and six sizes</a></p>
</div>
</div>
<div class="draw">{pressed}{k.ruler_svg()}</div>
</div></section>

<section class="band tray ruled" id="connecticut"><div class="wrap stack-gap">
<div class="cols">
<div class="side"><h2>Connecticut</h2></div>
<div>
<p>Regius showed its Connecticut at the IPCPR trade show in July 2017. The wrapper is shade grown from Connecticut seed in the Talanga valley of Honduras, and sits over Nicaraguan binder and filler.</p>
<p>Most Connecticut-seed wrapper is grown in Ecuador. Regius chose Talanga leaf instead, and its own product notes say the choice was made for flavour.</p>
{spec([("Wrapper", "Connecticut seed, shade grown, Talanga valley, Honduras"), ("Binder and filler", "Nicaragua"), ("First shown", "July 2017")])}
</div>
</div>
{vitola_table("Regius Connecticut sizes", CONN_ROWS, "connecticut", "black")}
</div></section>

<section class="band tray ruled" id="sun-grown"><div class="wrap stack-gap">
<div class="cols">
<div class="side"><h2>Sun Grown</h2></div>
<div>
<p>Shown beside the Connecticut in 2017, the Sun Grown sits at the other end of the range. It wears a dark sun grown wrapper taken from the higher primings of the plant, over Nicaraguan binder and filler, and it was made to be the fuller, bolder cigar in the range.</p>
{spec([("Wrapper", "Nicaragua, sun grown, higher priming"), ("Binder and filler", "Nicaragua"), ("Body", "Full"), ("First shown", "July 2017")])}
<p class="small quiet">Three sizes could be confirmed with dimensions. A Robusto is also made.</p>
</div>
</div>
{vitola_table("Regius Sun Grown sizes", SUN_ROWS, "sungrown", "black")}
</div></section>

<section class="band tray ruled" id="maduro"><div class="wrap stack-gap">
<div class="cols">
<div class="side"><h2>Maduro</h2></div>
<div>
<p>The Regius Maduro went into wide release in March 2018, after a spell in which only a few retailers had it. Regius describes it as the complexity of Black Label with the blend adjusted to suit a rich maduro wrapper. The details of that blend have not been published.</p>
<p>Akhil Kapacee has traced the idea to Spanish jam&oacute;n: if what a pig eats in its last weeks decides the ham, then what a tobacco plant is fed should decide the leaf.</p>
{spec([("Wrapper", "Maduro"), ("Blend", "Not disclosed"), ("Wide release", "March 2018"), ("Packed", "Boxes of 25")])}
</div>
</div>
{vitola_table("Regius Maduro sizes", MADURO_ROWS, "maduro", "black")}
</div></section>

<section class="band tray ruled" id="reserva"><div class="wrap stack-gap">
<div class="cols">
<div class="side"><h2>Reserva</h2></div>
<div>
<p>Reserva is made in small batches from Nicaraguan tobacco and aged after rolling. Kapacee has said these medium to medium-plus cigars were blended to recall the Cuban Bol&iacute;var of the years when it was most sought after.</p>
<p>The 2021 edition came as a Robusto Gordo in black lacquered boxes of twenty. British stockists have also carried a 50 ring Robusto in boxes of ten.</p>
{spec([("Wrapper", "Nicaragua, Habano"), ("Binder and filler", "Nicaragua"), ("Body", "Medium to medium-plus"), ("Made", "In small batches, aged after rolling")])}
</div>
</div>
{vitola_table("Regius Reserva sizes", RESERVA_ROWS, "colorado", "reserva", second="silver")}
</div></section>

<section class="band tight lid"><div class="wrap">
<p class="quiet">What is on the shelf varies by country and by year. <a href="stockists.html">Ask a stockist</a>, or see the <a href="limited-editions.html">limited editions</a> for the cigars made once and not again.</p>
</div></section>"""
    write("cigars.html", "Regius cigars | Every blend and size, drawn to scale",
          "Black Label, Exclusivo U.S.A., Connecticut, Sun Grown, Maduro and Reserva: the six Regius lines, with wrapper, origin and every size drawn to one scale.",
          body, crumbs)


def black_label():
    crumbs = [("index.html", "Regius"), ("cigars.html", "The cigars"), ("black-label.html", "Black Label")]
    body = page_head(crumbs, "Black Label",
                     "The cigar Regius began with. Black Label reached British tobacconists in 2010 and American ones late in 2011, where it was also sold as Regius of London.") + f"""
<section class="band tray"><div class="wrap cols">
<div class="side"><h2>The blend</h2></div>
<div>
<p>Black Label is a Nicaraguan puro: wrapper, binder and filler all come from Nicaragua. It is rolled at Plasencia Cigars S.A. in Estel&iacute; and was blended by Akhil Kapacee, who built his first Regius cigars for the European palate, which is to say for people who mostly smoke Cuban cigars.</p>
<p>An early halfwheel review reported that the blend draws on leaf from every part of the plant, some of it aged for as long as 15 years, under a shade-grown wrapper. The result is medium in body.</p>
{spec([("Wrapper", "Nicaragua, shade-grown Habano"), ("Binder", "Nicaragua"), ("Filler", "Nicaragua"), ("Factory", "Plasencia Cigars S.A., Estel&iacute;"), ("Body", "Medium"), ("First sold", "United Kingdom, 2010")])}
</div>
</div></section>

<section class="band lid"><div class="wrap cols">
<div class="side"><h2>What reviewers found</h2></div>
<div>
<ul class="plain">
<li>Creamy leather, sweet wood and a touch of something floral, with a little spice on the tongue. <span class="where">halfwheel, on the Robusto</span></li>
<li>Espresso cream, vanilla pod and earth. <span class="where">Mitchells Wine Merchants, on the Robusto</span></li>
<li>A light to medium body, a sweet aroma and a creamy texture that suits a cup of coffee. <span class="where">C.Gars Ltd, on the Corona</span></li>
</ul>
<p class="more">The band carries a detail worth looking for. halfwheel noted that it bears the initials of everyone who helped bring the brand into being.</p>
</div>
</div></section>

<section class="band tray"><div class="wrap stack-gap">
<div class="cols">
<div class="side"><h2>Eight sizes</h2></div>
<div>
<p>Black Label launched as a Corona, a Robusto, the slim Lord Madsen and the Grandido. The short robusto, the tubed Robusto, the Chicos in their tins and the Gran Toro followed. The Culebra is three cigars twisted together, a form first rolled for the makers themselves.</p>
</div>
</div>
{vitola_table("Regius Black Label sizes", BLACK_ROWS, "colorado", "black")}
</div></section>

<section class="band lid"><div class="wrap cols">
<div class="side"><h2>How it has been rated</h2></div>
<div>
<p>Cigar Coop reviewed the Black Label Corona and placed it in its 94 to 96 band. British stockists publish a longer list of ratings for the line, led by a 95 from Cigar Journal.</p>
<p class="more"><a href="recognition.html">Ratings for every Regius cigar, with sources</a></p>
</div>
</div></section>"""
    write("black-label.html", "Regius Black Label | The original Nicaraguan puro",
          "Black Label is the cigar Regius began with in 2010: a medium-bodied Nicaraguan puro rolled at Plasencia in Estelí. Blend, tasting notes and all eight sizes.",
          body, crumbs)


def exclusivo():
    crumbs = [("index.html", "Regius"), ("cigars.html", "The cigars"), ("exclusivo-usa.html", "Exclusivo U.S.A.")]
    def blend(name, alt, leaf, band, when, text, pairs):
        return f"""<div class="edition">
<div>
<p class="when">{when}</p>
<h3>{name}</h3>
<span class="swatch sw-{leaf} bd-{band}" aria-hidden="true"></span>
<p class="dims">{alt}</p>
</div>
<div>
<p>{text}</p>
{spec(pairs)}
</div>
</div>"""
    body = page_head(crumbs, "Exclusivo U.S.A.",
                     "Three blends made for American smokers and sold only in the United States. Red, then White, then Blue.") + f"""
<section class="band tray"><div class="wrap cols">
<div class="side"><h2>Why America got its own</h2></div>
<div>
<p>Regius had been built for British and European tastes. In 2014 Akhil Kapacee turned to the United States, telling Cigar Aficionado he wanted a line that kept traditional flavours but came in the modern, inventive sizes the American market asks for.</p>
<p>The series debuted that May at Casa de Montecristo and went national soon after, first in four sizes and then in six. Regius has said each blend is adjusted for each size, so a Robusto and a Lancero Extra of the same colour are not the same recipe cut to different lengths.</p>
<p>All three were rolled at Plasencia Cigars S.A. in Nicaragua.</p>
</div>
</div></section>

<section class="band lid"><div class="wrap">
<h2>The three blends</h2>
<div class="more">
{blend("Red Label", "Exclusivo U.S.A.", "colorado", "red", "2014",
       "A Nicaraguan puro with a wrapper grown in the Jalapa valley and filler that includes tobacco from the island of Ometepe. Cigar Aficionado tasted cocoa and earth with a nutty, pistachio edge in the Pressed Perfecto, gave it 92 points and ranked it no. 21 among its Top 25 cigars of 2017.",
       [("Wrapper", "Nicaragua, Jalapa valley"), ("Binder", "Nicaragua"), ("Filler", "Nicaragua, including Ometepe")])}
{blend("White Label", "Exclusivo U.S.A. Claro Especial", "claro", "white", "2014",
       "The second release, later the same year. It is also Nicaraguan throughout and is built on a double binder. Cigar Coop tasted cream, mixed fruit, natural tobacco and pepper across the sizes and placed it no. 22 in its 2014 Cigar of the Year Countdown.",
       [("Wrapper", "Nicaragua"), ("Binder", "Nicaragua, double binder"), ("Filler", "Nicaragua")])}
{blend("Blue Label", "Exclusivo U.S.A. Oscuro Especial", "oscuro", "blue", "2016",
       "The last of the three, shipped in February 2016 and the strongest. Kapacee chose a dark Mexican San Andr&eacute;s wrapper for its sweetness and clean finish, and five of the six sizes are box-pressed. Cigar Coop scored the Robusto 92 and placed it no. 27 in its 2016 Countdown.",
       [("Wrapper", "Mexico, San Andr&eacute;s"), ("Binder", "Nicaragua"), ("Filler", "Nicaragua")])}
</div>
</div></section>

<section class="band tray"><div class="wrap stack-gap">
<div class="cols">
<div class="side"><h2>Six sizes</h2></div>
<div>
<p>The series shares one set of sizes across all three blends. Two are perfectos, tapered at both ends, and none of them is small. They are drawn here with the Red Label's wrapper.</p>
</div>
</div>
{vitola_table("Regius Exclusivo U.S.A. sizes", EXCL_ROWS, "colorado", "red")}
</div></section>"""
    write("exclusivo-usa.html", "Regius Exclusivo U.S.A. | Red, White and Blue Label",
          "Three Regius blends made for American smokers and sold only in the United States. The Red Label Pressed Perfecto made Cigar Aficionado's Top 25 of 2017.",
          body, crumbs)


def editions():
    crumbs = [("index.html", "Regius"), ("limited-editions.html", "Limited editions")]

    def ed(when, name, text, art, dims):
        return f"""<article class="edition">
<div>
<p class="when">{when}</p>
<h2>{name}</h2>
</div>
<div>
{text}
<div class="draw">{art}</div>
<p class="dims">{dims}</p>
</div>
</article>"""

    orchant = k.cigar("4 3/4", 52, "colorado", band="black", second="gold",
                      label="The Selección Orchant Robusto, 4 3/4 inches by 52 ring gauge, drawn to scale")
    cule = k.culebra("5 3/4", 39, ["claro", "oscuro", "connecticut"],
                     label="A culebra of three cigars with three different wrappers, 5 3/4 inches by 39 ring gauge, drawn to scale")
    winston = k.culebra("5 3/4", 39, ["colorado", "oscuro", "connecticut"],
                        label="A culebra of three twisted cigars in three wrappers, 5 3/4 inches long, drawn to scale")
    gorda = k.cigar("5 5/8", 46, "colorado", label="The Limited Edition Corona Gorda, 5 5/8 inches by 46 ring gauge, drawn to scale")
    white = "".join([
        k.cigar("5 5/8", 54, "colorado", band="white", label="White Label Royal Robusto, 5 5/8 inches by 54 ring gauge, drawn to scale"),
        k.cigar("6", 50, "colorado", band="white", label="White Label Toro, 6 inches by 50 ring gauge, drawn to scale"),
        k.cigar("6 1/8", 52, "colorado", shape="torpedo", band="white", label="White Label Torpedo, 6 1/8 inches by 52 ring gauge, drawn to scale"),
    ])
    double = k.cigar("7 5/8", 49, "colorado", label="The Double Corona sold in 2013, 7 5/8 inches by 49 ring gauge, drawn to scale")
    body = page_head(crumbs, "Limited editions",
                     "Cigars Regius made in small numbers, for particular shops, or only once. All are drawn to the same scale as the regular range.") + f"""
<section class="band tray"><div class="wrap">
{ed("2013, then yearly", "Selecci&oacute;n Orchant",
    '<p>Mitchell Orchant of C.Gars Ltd and Alfie Turmeaus Tobacconist is one of the largest sellers of Cuban cigars in Britain, and lends his name to the Havanas he selects. In 2013 he and Akhil Kapacee made a Regius to the same standard: a Robusto modelled on the Partag&aacute;s Serie D No. 4, which Kapacee described to halfwheel as &ldquo;classically Cuban&rdquo;.</p>'
    '<p>Four hundred boxes of ten were made, half for Britain and half for the United States. The cigar wears a second, golden band. It came back in 2014 with a new size, and C.Gars now lists the Orchant Selecci&oacute;n as a yearly release blended for British palates.</p>',
    orchant, "Robusto, 2013. 4 3/4 in &times; 52. Nicaraguan wrapper, binder and filler. Plasencia Cigars S.A.")}
{ed("2013", "The three-wrapper Culebra",
    '<p>A culebra is three slim cigars twisted together while still supple. Regius made this one for Alfie Turmeaus with a different wrapper on each cigar: a Cuban-seed claro, a Cuban-seed oscuro and the Talanga Connecticut.</p>'
    '<p>Binder and filler are the same in all three, so the smoker can untwist them and taste exactly what a wrapper does. They were sold in boxes of three culebras, nine cigars in all.</p>',
    cule, "5 3/4 in &times; 39 each. Boxes of three culebras.")}
{ed("2012", "Winston's Humidor Third Anniversary Culebra",
    "<p>Winston's Humidor of Midlothian, Virginia, was one of the first American shops to stock Regius. For its third anniversary in 2012 Regius made it a culebra with a different wrapper on each cigar. halfwheel reviewed the Rosado and the Oscuro from it separately.</p>"
    "<p>The culebra made for Turmeaus a year later has the same size and the same mix of wrappers. Kapacee has said the blend inside is different.</p>",
    winston, "5 3/4 in &times; 39 each. Nicaraguan Jalapa Rosado wrapper on the Rosado. Plasencia Cigars S.A.")}
{ed("2014", "Damaris",
    "<p>A very small release made with Jim Thomas of That Cigar Place. It wore a Mexican San Andr&eacute;s wrapper two years before the Oscuro Especial made that leaf a regular part of the range.</p>",
    "", "No dimensions were published in the sources used here, so it is not drawn.")}
{ed("2015", "Limited Edition Corona Gorda",
    "<p>An offshoot of Black Label in a Cuban-style box press. It wears the Black Label band, but Kapacee told Cigar Coop the blend is slightly different, and the cigars were aged for two years before release.</p>",
    gorda, "5 5/8 in &times; 46, box-pressed. Nicaraguan wrapper, binder and filler.")}
{ed("Limited production", "Serie Limitada",
    "<p>The one Regius made entirely of Peruvian tobacco. Wrapper, binder and filler all come from Tabacalera del Oriente in Tarapoto, and the cigars are matured for more than a year. C.Gars, which announced the line, says the Peruvian leaf gives the cigar a layer of sweetness.</p>",
    "", "Made as a Corona, Petit Royales, Robusto and Wide Churchill. Dimensions were not confirmed, so none is drawn.")}
{ed("2012", "White Label",
    "<p>The first Regius made outside Nicaragua. When SAG Imports took on American distribution in 2012, its sister factory MATASA in the Dominican Republic began rolling a Dominican puro under the Regius name. Cigar Aficionado gave the Royal Robusto 90 points in December 2013.</p>"
    "<p>When Regius and Quesada parted in 2017, Quesada said it was no longer making the line. It should not be confused with the White Label of the Exclusivo U.S.A. series, which is Nicaraguan.</p>",
    white, "Royal Robusto 5 5/8 in &times; 54, Toro 6 in &times; 50, Torpedo 6 1/8 in &times; 52. Dominican wrapper, binder and filler.")}
{ed("2013", "The &pound;40,000 Double Corona",
    "<p>In 2013 a single boxed Regius Double Corona was sold at Alfie Turmeaus Tobacconist in Shepherd Market, Mayfair, for &pound;40,000. The trade press reported it as the most expensive cigar ever sold, and it still appears on lists of the costliest cigars in the world.</p>"
    "<p>The price bought more than the cigar. Regius flew the buyer to Nicaragua to see the factory, then blended and rolled a thousand cigars to his own taste in flavour, size and strength. Kapacee cut and lit the Double Corona himself.</p>",
    double, "7 5/8 in &times; 49. Handmade in Nicaragua.")}
</div></section>"""
    body = body.replace('<div class="draw"></div>\n', '')
    write("limited-editions.html", "Regius limited editions | Selección Orchant and more",
          "Selección Orchant, the three-wrapper Culebra, a Peruvian Serie Limitada, the Dominican White Label and the £40,000 Double Corona sold in Mayfair in 2013.",
          body, crumbs)


def house():
    crumbs = [("index.html", "Regius"), ("house.html", "The house")]
    years = [
        ("2009", "Regius Cigars Limited is incorporated in London on 22 July, under its first name, Trinity Cigars Limited."),
        ("2010", "The company takes the name Regius on 1 July. The first cigars reach British tobacconists."),
        ("2011", "Late in the year Regius is sold in the United States for the first time, through Sacred Cigars of Dallas. Three of its four sizes make the crossing."),
        ("2012", "SAG Imports, the distribution arm of Quesada Cigars, becomes the exclusive American distributor. The Dominican-made White Label follows, and Winston's Humidor in Virginia receives an anniversary culebra."),
        ("2013", "The Selecci&oacute;n Orchant Robusto and a three-wrapper Culebra are made with Mitchell Orchant. A single Double Corona is sold in Mayfair for &pound;40,000."),
        ("2014", "Exclusivo U.S.A. launches: the Red Label in May, the Claro Especial later in the year. Damaris is made in very small numbers."),
        ("2015", "A box-pressed Limited Edition Corona Gorda appears, aged for two years."),
        ("2016", "The Oscuro Especial ships in February and completes the Exclusivo U.S.A. series."),
        ("2017", "The agreement with Quesada ends on 30 April, and Oscar Valladares Tobacco &amp; Co. of Houston takes over on 1 May. Connecticut and Sun Grown are shown at the IPCPR trade show in July. In December the Pressed Perfecto is named no. 21 in Cigar Aficionado's Top 25."),
        ("2018", "The Maduro goes into wide release in March."),
        ("2021", "The 2021 edition of Reserva arrives in black lacquered boxes."),
    ]
    tl = "".join(f'<li><span class="year">{y}</span><p>{t}</p></li>' for y, t in years)
    body = page_head(crumbs, "The house",
                     "Regius Cigars Ltd is a London company. Its cigars are designed in England and rolled in Nicaragua, and its name and motto are Roman.") + f"""
<section class="band tray"><div class="wrap cols">
<div class="side"><h2>A Latin name</h2></div>
<div>
<p><i lang="la">Regius</i> means royal, or belonging to a king. The house uses it plainly: a hand-made king of cigars.</p>
<p>The motto on the band is <i lang="la">arbiter elegantiae</i>, judge of elegance. It belongs to Gaius Petronius, a Roman writer born around AD 27 and a courtier to the emperor Nero. Petronius devoted himself to pleasure, but he was known as a connoisseur and not a wastrel. Tacitus records that Nero came to think nothing charming or refined unless Petronius had approved it.</p>
<p>Regius was created in his memory, and the motto is an invitation. The makers cultivate, age and blend the tobacco for taste, an even burn and a good aroma. Whether they have succeeded is for the smoker to judge.</p>
</div>
</div></section>

<section class="band lid"><div class="wrap cols">
<div class="side"><h2>Founded in London</h2></div>
<div>
<p>Regius was founded in 2010 by a small group of cigar enthusiasts in London. It is led by Akhil Kapacee, who was born in the city and worked as an investment banker at Barclays Capital before he made cigars.</p>
<p>Kapacee blended his first cigars for the European palate. In practice that meant people who mostly smoked Havanas, and the aim was a Nicaraguan cigar with a character they would recognise. The American market came later, and with it a second idea of what a Regius could be.</p>
{spec([("Company", "Regius Cigars Limited"), ("Based in", "London, United Kingdom"), ("Founded", "2010"), ("Led by", "Akhil Kapacee"), ("First market", "United Kingdom")])}
</div>
</div></section>

<section class="band tray"><div class="wrap cols">
<div class="side"><h2>Made by the Plasencias</h2></div>
<div>
<p>To make the cigars, the founders went to Nestor Plasencia, whose family has grown tobacco for five generations and whose roots are in Cuban cigar making. The core Regius blends are rolled at Plasencia Cigars S.A. in Estel&iacute;, in the mountains of northern Nicaragua.</p>
<p>Regius describes a factory of more than 500 rollers making cigars the old-fashioned way with modern technology behind them. Every cigar is checked individually for draw and construction before it leaves.</p>
<p>Two cigars were made elsewhere. The first White Label was rolled at MATASA in the Dominican Republic, and the Serie Limitada uses only Peruvian tobacco. Both are on the <a href="limited-editions.html">limited editions</a> page.</p>
</div>
</div></section>

<section class="band lid"><div class="wrap cols">
<div class="side"><h2>Year by year</h2></div>
<div><ol class="timeline">{tl}</ol></div>
</div></section>"""
    write("house.html", "The house of Regius | Name, makers and timeline",
          "Why a London cigar house took a Latin name and a Roman courtier's motto, who founded it, who rolls its cigars in Nicaragua, and what happened year by year.",
          body, crumbs)


def recognition():
    crumbs = [("index.html", "Regius"), ("recognition.html", "Recognition")]
    body = page_head(crumbs, "Recognition",
                     "What the cigar press has published about Regius, with the year, the cigar and where each result comes from.") + f"""
<section class="band tray"><div class="wrap cols">
<div class="side">
<h2>Checked at the source</h2>
<p class="quiet">Each of these was read on the publication's own pages while this site was being made.</p>
</div>
<div>
<table class="ledger stack">
<caption class="sr">Regius ratings confirmed on the publisher's own pages</caption>
<thead><tr><th scope="col">Year</th><th scope="col">Publication</th><th scope="col">Cigar</th><th scope="col">Result</th></tr></thead>
<tbody>
<tr><th scope="row">2017</th><td data-l="Publication">{ext("https://www.cigaraficionado.com/top25/2017", "Cigar Aficionado, Top 25 Cigars of 2017")}</td><td data-l="Cigar">Exclusivo U.S.A. Pressed Perfecto</td><td data-l="Result">No. 21, 92 points</td></tr>
<tr><th scope="row">2016</th><td data-l="Publication">{ext("https://cigar-coop.com/2016/12/2016-cigar-of-the-year-countdown-27-regius-exclusivo-u-s-a-oscuro-especial-robusto.html", "Cigar Coop, Cigar of the Year Countdown")}</td><td data-l="Cigar">Exclusivo U.S.A. Oscuro Especial Robusto</td><td data-l="Result">No. 27. Review score 92</td></tr>
<tr><th scope="row">2014</th><td data-l="Publication">{ext("https://www.cigar-coop.com/2014/12/aged-selects-2014-cigar-of-year_9.html", "Cigar Coop, Cigar of the Year Countdown")}</td><td data-l="Cigar">Exclusivo U.S.A. Claro Especial</td><td data-l="Result">No. 22</td></tr>
<tr><th scope="row">2013</th><td data-l="Publication">{ext("https://www.cigaraficionado.com/ratings/16769/name/regius-white-label-royal-robusto-toro", "Cigar Aficionado")}</td><td data-l="Cigar">White Label Royal Robusto</td><td data-l="Result">90 points</td></tr>
</tbody>
</table>
</div>
</div></section>

<section class="band lid"><div class="wrap cols">
<div class="side"><h2>Other published scores</h2></div>
<div>
<ul class="plain">
<li>Reserva Robusto Gordo, 2021 edition: 93. <span class="where">{ext("https://thecigarauthority.com/?p=52070", "The Cigar Authority")}</span></li>
<li>Exclusivo U.S.A. Red Label Toro: 93. <span class="where">{ext("https://thecigarauthority.com/?p=44927", "The Cigar Authority")}</span></li>
<li>Black Label Corona: placed in the 94 to 96 band. <span class="where">{ext("https://cigar-coop.com/tag/regius/page/3", "Cigar Coop")}</span></li>
<li>Exclusivo U.S.A. Oscuro Especial Toro Extra: 89. <span class="where">{ext("https://www.cigaraficionado.com/ratings/19929/name/regius-exclusivo-u-s-a-oscuro-especial-toro-extra-toro", "Cigar Aficionado")}</span></li>
</ul>
</div>
</div></section>

<section class="band tray"><div class="wrap cols">
<div class="side">
<h2>As listed by stockists</h2>
<p class="quiet">Not checked against the original publications for this site.</p>
</div>
<div>
<p>British stockists {ext("https://www.cgarsltd.co.uk/cigar-library/Regius_Cigars.html", "C.Gars Ltd")} and {ext("https://www.simplycigars.co.uk/nicaraguan-cigars-regius-cigars-c-267_65_248.html", "Simply Cigars")} publish this list of ratings for Black Label:</p>
<ul class="plain">
<li>Cigar Journal: 95</li>
<li>Cigar Aficionado: 91</li>
<li>Wall Street Journal: Top 12</li>
<li>Cigar Coop: 94</li>
<li>Stogie Rate: 91</li>
<li>Leaf Enthusiast: 9.5 out of 10</li>
<li>A Cigar Smoker: 91</li>
<li>Blind Man's Puff: 89</li>
</ul>
<p class="more">The same listings say Cigar Aficionado has rated Regius among the top 25 cigar brands on sale in the United States.</p>
</div>
</div></section>

<section class="band tight lid"><div class="wrap">
<p>One record is of a different kind. In 2013 a single Regius Double Corona sold in Mayfair for &pound;40,000. <a href="limited-editions.html">Read about it among the limited editions</a>.</p>
</div></section>"""
    write("recognition.html", "Regius Cigars ratings | Top 25 lists and review scores",
          "Published ratings for Regius cigars from Cigar Aficionado, Cigar Coop and The Cigar Authority, each with its year, its cigar and its source.",
          body, crumbs)


def stockists():
    crumbs = [("index.html", "Regius"), ("stockists.html", "Stockists")]
    uk = [
        ("C.Gars Ltd", "Online and in its Turmeaus shops", "https://www.cgarsltd.co.uk/cigar-library/Regius_Cigars.html"),
        ("Turmeaus", "Tobacconist, established 1817", "https://www.turmeaus.co.uk/regius-robusto-cigar-single-p-16554.html"),
        ("Simply Cigars", "Online", "https://www.simplycigars.co.uk/nicaraguan-cigars-regius-cigars-c-267_65_248.html"),
        ("Mitchells Wine Merchants", "Black Label and Connecticut", "https://www.mitchellswine.co.uk/shop/cigars_and_tobacco/regius/"),
        ("GQ Tobaccos", "Online", "https://www.gqtobaccos.com/cigars/regius-robusto-single-cigar-4"),
    ]
    us = [
        ("Smokingpipes", "Black Label, Maduro, Sun Grown and Connecticut", "https://www.smokingpipes.com/cigars/regius/"),
        ("TobaccoPipes", "Maduro and Sun Grown", "https://tobaccopipes.com/regius-cigars"),
        ("Hiland's Cigars", "Online", "https://www.hilandscigars.com/shop/cigars/regius/"),
        ("Atlantic Cigar", "Exclusivo U.S.A.", "https://atlanticcigar.com/regius-exclusivo-usa-red-fat-perfecto-1"),
        ("Blacksburg Pipe and Tobacco", "Blacksburg, Virginia", "https://www.blacksburgtobacco.com/services/regius-cigars/"),
    ]

    def lst(rows):
        return '<ul class="plain">' + "".join(
            f'<li>{ext(u, "Regius at " + n)}<span class="where">{w}</span></li>' for n, w, u in rows) + "</ul>"

    body = page_head(crumbs, "Where to find Regius",
                     "Regius sells through tobacconists. These retailers listed Regius cigars online in November 2026.") + f"""
<section class="band tray"><div class="wrap twoup">
<div>
<h2>United Kingdom</h2>
<div class="more">{lst(uk)}</div>
</div>
<div>
<h2>United States</h2>
<div class="more">{lst(us)}</div>
</div>
</div></section>

<section class="band lid"><div class="wrap cols">
<div class="side"><h2>How Regius reached America</h2></div>
<div>
<p>For its first years Regius could be bought only in Britain. It crossed the Atlantic late in 2011 through one shop, Sacred Cigars of Dallas.</p>
<p>In August 2012 SAG Imports, the distribution company of Quesada Cigars, became the exclusive American distributor. That agreement ended on 30 April 2017, and from 1 May Oscar Valladares Tobacco &amp; Co. of Houston stored and shipped Regius cigars in the United States.</p>
<p>The <a href="exclusivo-usa.html">Exclusivo U.S.A.</a> series was made for that market and is sold nowhere else. In Britain, C.Gars Ltd also carries the <a href="limited-editions.html">Selecci&oacute;n Orchant</a>, chosen by Mitchell Orchant.</p>
</div>
</div></section>

<section class="band tight tray"><div class="wrap">
<p>Listings change, so confirm stock with the retailer before you travel or order. You must be of legal age to buy tobacco where you live.</p>
</div></section>"""
    write("stockists.html", "Where to buy Regius cigars | UK and US stockists",
          "Tobacconists in the United Kingdom and United States that list Regius cigars online, and how the brand has been distributed in America since 2011.",
          body, crumbs)


def about():
    crumbs = [("index.html", "Regius"), ("about.html", "About this site")]
    groups = [
        ("Trade press and reviews", [
            ("halfwheel: Regius Robusto review", "https://halfwheel.com/regius-robusto/21696/"),
            ("halfwheel: Regius Selección Orchant Robusto LE", "https://halfwheel.com/review-regius-seleccion-orchant-robusto-le-prerelease/40156/"),
            ("halfwheel: Dominican-made White Label and two new sizes", "https://halfwheel.com/regius-cigars-introduced-dominican-made-white-labels-vitolas/30151/"),
            ("halfwheel: SAG Imports distribution press release", "https://halfwheel.com/press-release-regius-london-cigars-exclusively-distributed-usa-sag-imports/"),
            ("halfwheel: Exclusivo U.S.A. Oscuro Especial Pressed Perfecto", "https://halfwheel.com/regius-exclusivo-u-s-a-oscuro-especial-pressed-perfecto/112212/"),
            ("halfwheel: Regius and Quesada end distribution agreement", "https://halfwheel.com/regius-quesada-end-distribution-agreement/145099"),
            ("halfwheel: Regius Maduro Corona", "https://halfwheel.com/regius-maduro-corona/269995/"),
            ("Cigar Aficionado: Top 25 Cigars of 2017", "https://www.cigaraficionado.com/top25/2017"),
            ("Cigar Aficionado: Exclusivo U.S.A. Pressed Perfecto rating", "https://www.cigaraficionado.com/ratings/20155/name/regius-exclusivo-u-s-a-pressed-perfecto-figurado"),
            ("Cigar Aficionado: Final Regius Cigar Made Just For The U.S.A.", "https://www.cigaraficionado.com/article/final-regius-cigar-made-just-for-the-usa-18533"),
            ("Cigar Aficionado: Quesada and Regius Cigars Part Ways", "https://www.cigaraficionado.com/article/quesada-and-regius-cigars-part-ways-19314"),
            ("Cigar Aficionado: White Label Royal Robusto rating", "https://www.cigaraficionado.com/ratings/16769/name/regius-white-label-royal-robusto-toro"),
            ("Cigar Coop: Regius archive", "https://cigar-coop.com/tag/regius"),
            ("Cigar Coop: Oscuro Especial coming in February", "https://cigar-coop.com/2016/01/cigar-news-regius-exclusivo-u-s-a-oscuro-especial-coming-in-february.html"),
            ("Cigar Coop: Oscuro Especial Robusto review", "https://cigar-coop.com/2016/11/cigar-review-regius-exclusivo-u-s-a-oscuro-especial-robusto.html"),
            ("Cigar Coop: 2016 Countdown, no. 27", "https://cigar-coop.com/2016/12/2016-cigar-of-the-year-countdown-27-regius-exclusivo-u-s-a-oscuro-especial-robusto.html"),
            ("Cigar Coop: 2014 Countdown, no. 22", "https://www.cigar-coop.com/2014/12/aged-selects-2014-cigar-of-year_9.html"),
            ("Cigar Coop: Limited Edition Corona Gorda review", "https://cigar-coop.com/2015/11/cigar-review-regius-limited-edition-corona-gorda-cuban-box-press.html"),
            ("Cigar Coop: Oscar Valladares to distribute Regius", "https://cigar-coop.com/2017/04/cigar-news-regius-cigars-to-be-distributed-by-oscar-valladares-tobacco-co.html"),
            ("The Cigar Authority: Regius Reserva Robusto Gordo", "https://thecigarauthority.com/?p=52070"),
            ("The Cigar Authority: Black Label Petit Robusto", "https://thecigarauthority.com/?p=42545"),
            ("The Cigar Authority: Exclusivo U.S.A. Red Toro", "https://thecigarauthority.com/?p=44927"),
            ("Tobacco Business: Regius taps Oscar Valladares for distribution", "https://tobaccobusiness.com/regius-cigars-oscar-valladares-distribution"),
            ("Blind Man's Puff: Black Label Corona", "https://blindmanspuff.com/?p=33049"),
            ("Casas Fumando: Exclusivo U.S.A. Red Label", "https://www.casasfumando.com/regius-cigars-exclusivo-usa-red-label/"),
        ]),
        ("Stockists and their libraries", [
            ("C.Gars Ltd: Regius in the Cigar Library", "https://www.cgarsltd.co.uk/cigar-library/Regius_Cigars.html"),
            ("C.Gars Ltd: World's most costly cigar sold at Alfie Turmeaus", "https://www.cgarsltd.co.uk/worlds-most-costly-cigar-sold-londons-alfie-turmeaus-a-669.html"),
            ("C.Gars Ltd: Regius adds a limited Culebra and Robusto", "https://www.cgarsltd.co.uk/regius-add-limited-culebra-robusto-a-676.html"),
            ("C.Gars Ltd: New Regius Limitada cigars", "https://www.cgarsltd.co.uk/new-regius-limitada-cigars-a-622.html"),
            ("C.Gars Ltd: Regius Orchant Seleccion", "https://www.cgarsltd.co.uk/regius-orchant-seleccion-a-166.html"),
            ("Simply Cigars: Regius", "https://www.simplycigars.co.uk/nicaraguan-cigars-regius-cigars-c-267_65_248.html"),
            ("Mitchells Wine Merchants: Regius", "https://www.mitchellswine.co.uk/shop/cigars_and_tobacco/regius/"),
            ("Gauntleys: Regius, cigar of the month", "https://cigars.gauntleys.com/uk/offer/cigar-of-the-month-regius-cigars-of-nicaragua"),
            ("Smokingpipes: Regius", "https://www.smokingpipes.com/cigars/regius/"),
            ("TobaccoPipes: Regius", "https://tobaccopipes.com/regius-cigars"),
        ]),
        ("Public records", [
            ("Companies House: Regius Cigars Limited, company 06969408", COMPANIES_HOUSE),
        ]),
    ]
    src = "".join(
        f'<div class="source-group"><h3>{g}</h3><ul class="plain">'
        + "".join(f"<li>{ext(u, esc(n))}</li>" for n, u in items) + "</ul></div>"
        for g, items in groups)
    body = page_head(crumbs, "About this site",
                     "This is an unofficial concept site. Regius Cigars did not commission it, has not reviewed it and is not affiliated with it.") + f"""
<section class="band tray"><div class="wrap cols">
<div class="side"><h2>What it is</h2></div>
<div>
<p>This site was designed and written in November 2026 by Jake Labate, SEO Consultant, as a proposal for Regius Cigars: a picture of what the house's website could be.</p>
<p>When it was made, the official address, <span class="quiet">regiuscigars.com</span>, showed a holding page saying a new site was being prepared.</p>
<p>If Regius would like anything here changed, or the whole site taken down, it will be done the same day. Write to Jake through <a href="https://jakelabate.com/">jakelabate.com</a>.</p>
</div>
</div></section>

<section class="band lid"><div class="wrap cols">
<div class="side"><h2>How it was made</h2></div>
<div>
<ul class="plain">
<li>Every fact comes from a published source listed below. Where sources disagreed, the more direct one was used. Where a detail could not be confirmed, it was left out.</li>
<li>No Regius logo, band artwork or photography appears. The name is set in type, and the cigars are original drawings made from published dimensions.</li>
<li>The copy is written in the third person. It describes Regius and does not speak for it.</li>
<li>Prices are left out because they change. Customer reviews are left out because they belong to the people who wrote them.</li>
<li>Every page is marked noindex, so this concept does not compete with Regius in search.</li>
</ul>
</div>
</div></section>

<section class="band tray"><div class="wrap cols">
<div class="side"><h2>Sources</h2></div>
<div>{src}</div>
</div></section>"""
    write("about.html", "About this site | Regius Cigars concept and sources",
          "This is an unofficial concept site for Regius Cigars by Jake Labate, SEO Consultant. How it was researched, what was left out, and every source used.",
          body, crumbs)


def notfound():
    body = """<section class="page-head lid"><div class="wrap">
<h1>That page is not in the box</h1>
<p class="lede">The address may have changed, or the page may never have existed. These will get you back.</p>
<p class="hero-links"><a href="index.html">Home</a><a href="cigars.html">The cigars</a><a href="house.html">The house</a></p>
</div></section>"""
    write("404.html", "Page not found | Regius Cigars concept site",
          "The page you were looking for is not here. Go back to the Regius Cigars concept site home page or see the cigars.",
          body)


if __name__ == "__main__":
    os.makedirs(SITE, exist_ok=True)
    home(); cigars(); black_label(); exclusivo(); editions(); house(); recognition(); stockists(); about(); notfound()
    print("built", sorted(f for f in os.listdir(SITE) if f.endswith(".html")))
