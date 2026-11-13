"""The one stylesheet, inlined into every page. Every colour is a :root token from palette.json."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
TOKENS = json.load(open(os.path.join(HERE, "..", "palette.json")))["tokens"]

ROOT = ":root{" + "".join(f"--{k}:{v};" for k, v in TOKENS.items()) + (
    "--display:'Libre Caslon Display','Libre Caslon Display Fallback',Georgia,serif;"
    "--text:'Libre Caslon Text','Libre Caslon Text Fallback',Georgia,serif;"
    "--roman:'Cinzel','Cinzel Fallback',Georgia,serif;"
    "--measure:36rem;--wrap:74rem;--gut:clamp(1.25rem,4.5vw,3.5rem)}"
)

CSS = ROOT + r"""
*,*::before,*::after{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--ink);color:var(--paper);font-family:var(--text);font-size:clamp(1.0625rem,.3vw + 1rem,1.1875rem);line-height:1.7;-webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility}
svg{display:block;max-width:100%}
.sr{position:absolute;width:1px;height:1px;margin:-1px;overflow:hidden;clip-path:inset(50%);white-space:nowrap}
.svg-defs{position:absolute;width:0;height:0}
.wrap{max-width:var(--wrap);margin-inline:auto;padding-inline:var(--gut)}

/* The box: a lacquer lid outside, a cedar tray inside. Each surface sets its own inks. */
.lid{--bg:var(--ink);--fg:var(--paper);--quiet:var(--muted);--link:var(--brand);--rule:var(--brand);--accent:var(--brand);--edge:var(--brand);background-color:var(--bg);color:var(--fg)}
.tray{--bg:var(--cedar);--fg:var(--ink);--quiet:var(--muted-ink);--link:var(--brand-text);--rule:var(--brand-text);--accent:var(--red);--edge:var(--leaf-edge);background-color:var(--bg);color:var(--fg);
  background-image:repeating-linear-gradient(90.6deg,color-mix(in srgb,var(--cedar-deep) 42%,transparent) 0 1px,transparent 1px 11px),repeating-linear-gradient(89.5deg,color-mix(in srgb,var(--cedar-deep) 26%,transparent) 0 3px,transparent 3px 47px)}
.band{padding-block:clamp(3.5rem,8vw,7.5rem)}
.band.tight{padding-block:clamp(2.5rem,5vw,4.5rem)}
.ruled{border-top:1px solid color-mix(in srgb,var(--rule) 45%,transparent)}
.edge{height:7px;border-block:1px solid var(--brand);background:var(--ink)}

h1,h2,h3{font-family:var(--display);font-weight:400;line-height:1.06;margin:0;text-wrap:balance}
h2{font-size:clamp(2.1rem,3.8vw,3.4rem);letter-spacing:-.005em}
h3{font-size:clamp(1.45rem,2vw,1.9rem);line-height:1.15}
p{margin:0 0 1.15em;max-width:var(--measure)}
p:last-child{margin-bottom:0}
a{color:var(--link);text-decoration-thickness:1px;text-underline-offset:.2em}
a:hover{text-decoration-thickness:2px}
:focus-visible{outline:2px solid var(--rule);outline-offset:3px;border-radius:2px}
.quiet{color:var(--quiet)}
.small{font-size:.9rem;line-height:1.6}
i,em,.latin{font-style:italic}
.skip{position:absolute;left:var(--gut);top:-4rem;background:var(--brand);color:var(--brand-ink);padding:.5rem .9rem;z-index:20}
.skip:focus{top:.5rem}

/* Staging notice: first thing on every page */
.notice{background:var(--ink-2);color:var(--paper);font-size:.82rem;line-height:1.45}
.notice .wrap{padding-block:8px;display:flex;gap:6px;align-items:baseline;flex-wrap:wrap}
.notice b{color:var(--brand);font-weight:700;white-space:nowrap}
.notice p{margin:0;max-width:none;color:var(--paper)}
.notice a{color:var(--brand)}

/* Header */
.head .wrap{display:flex;align-items:baseline;justify-content:space-between;gap:1rem 2.5rem;padding-block:1.5rem;flex-wrap:wrap}
.wordmark{font-family:var(--roman);font-weight:500;font-size:1.55rem;letter-spacing:.36em;color:var(--brand);text-decoration:none;line-height:1}
.nav ul{list-style:none;display:flex;gap:.4rem clamp(1.1rem,2.4vw,2.2rem);margin:0;padding:0;flex-wrap:wrap}
.nav a{color:var(--paper);text-decoration:none;display:inline-block;padding-block:.3rem;border-bottom:1px solid transparent}
.nav a:hover{border-bottom-color:var(--brand)}
.nav a[aria-current],.nav a.here{color:var(--brand);border-bottom-color:var(--brand)}

/* Home hero */
.hero{padding-block:clamp(2.5rem,6vw,5.5rem) 0}
.hero h1{font-size:clamp(3.3rem,11.2vw,10.25rem);line-height:1;letter-spacing:-.018em;margin-left:-.04em}
.hero-grid{display:grid;gap:2.5rem;margin-top:clamp(2.2rem,5vw,4.5rem)}
.lede{font-size:clamp(1.2rem,1vw + 1rem,1.5rem);line-height:1.5}
.facts{margin:0;display:grid;grid-template-columns:auto 1fr;gap:.3rem 1.4rem;align-content:start;font-size:.98rem}
.facts dt{color:var(--quiet)}
.facts dd{margin:0}
.hero-links{display:flex;gap:1.8rem;flex-wrap:wrap;margin-top:1.6rem}
@media (min-width:58rem){.hero-grid{grid-template-columns:minmax(0,4fr) minmax(0,7fr);align-items:start;gap:4rem}}
.frieze{display:flex;justify-content:space-between;align-items:baseline;max-width:none;margin:clamp(2.6rem,6vw,5rem) 0 0;padding-bottom:clamp(1.1rem,2.4vw,1.9rem);font-family:var(--roman);font-weight:500;font-size:clamp(.78rem,2.25vw,1.7rem);line-height:1;color:var(--brand)}
.frieze .gap{flex:0 0 1.2em}

/* Inner page head */
.page-head{padding-block:clamp(2.2rem,5vw,4rem) clamp(2.6rem,6vw,5rem)}
.page-head h1{font-size:clamp(2.9rem,7.6vw,6.6rem);line-height:1.02;letter-spacing:-.014em;max-width:14ch;margin-left:-.03em}
.page-head .lede{margin-top:clamp(1.4rem,3vw,2.4rem);max-width:40rem}
.crumbs{font-size:.9rem;margin-bottom:clamp(1.6rem,4vw,3rem);color:var(--quiet)}
.crumbs ol{list-style:none;display:flex;flex-wrap:wrap;gap:.5rem;margin:0;padding:0}
.crumbs li+li::before{content:"/";margin-right:.5rem;color:var(--quiet)}
.crumbs a{color:var(--quiet)}

/* Two column prose: heading left, matter right */
.cols{display:grid;gap:1.6rem 4rem}
@media (min-width:58rem){.cols{grid-template-columns:minmax(0,4fr) minmax(0,7fr)}.cols>.side{position:sticky;top:2rem;align-self:start}}
.side p{margin-top:1.2rem}
.stack-gap>*+*{margin-top:clamp(2.2rem,4vw,3.4rem)}

/* The range, listed */
.lines{list-style:none;margin:0;padding:0}
.lines li{display:grid;grid-template-columns:4.8rem 1fr;gap:.25rem 1.6rem;padding-block:1.3rem;border-top:1px solid color-mix(in srgb,var(--rule) 45%,transparent);align-items:baseline}
.lines li:last-child{border-bottom:1px solid color-mix(in srgb,var(--rule) 45%,transparent)}
.lines .name{font-family:var(--display);font-size:clamp(1.5rem,2.2vw,2rem);line-height:1.15}
.lines .name a{color:var(--fg);text-decoration-color:color-mix(in srgb,var(--rule) 70%,transparent)}
.lines .what{grid-column:2;color:var(--quiet);margin:0;max-width:44rem}
.swatch{display:block;width:4.8rem;height:1rem;border-radius:.5rem 2px 2px .5rem;border:1px solid var(--edge);align-self:center;--band:var(--leaf);background:linear-gradient(90deg,var(--leaf) 0 22%,var(--band) 22% 40%,var(--leaf) 40%)}
.sw-connecticut{--leaf:var(--leaf-connecticut)}.sw-claro{--leaf:var(--leaf-claro)}.sw-colorado{--leaf:var(--leaf-colorado)}
.sw-sungrown{--leaf:var(--leaf-sungrown)}.sw-maduro{--leaf:var(--leaf-maduro)}.sw-oscuro{--leaf:var(--leaf-oscuro)}
.bd-black{--band:var(--ink)}.bd-red{--band:var(--red)}.bd-white{--band:var(--band-white)}.bd-blue{--band:var(--band-blue)}.bd-silver{--band:var(--band-silver)}
.edition .swatch{margin-top:.9rem}

/* Specification list */
.spec{margin:0;display:grid;grid-template-columns:minmax(6.5rem,9rem) 1fr;font-size:.98rem}
.spec dt,.spec dd{padding-block:.6rem;border-top:1px solid color-mix(in srgb,var(--rule) 45%,transparent);margin:0}
.spec dt{color:var(--quiet);padding-right:1rem}

/* Tables */
table{border-collapse:collapse;width:100%}
caption{text-align:left}
th,td{text-align:left;vertical-align:middle;padding:.9rem 1.2rem .9rem 0;border-top:1px solid color-mix(in srgb,var(--rule) 45%,transparent);font-weight:400}
thead th{border-top:0;color:var(--quiet);font-size:.9rem;padding-block:.4rem}
tbody th{font-family:var(--display);font-size:1.6rem;line-height:1.15}
.note{display:block;font-family:var(--text);font-size:.88rem;color:var(--quiet);line-height:1.45;margin-top:.2rem}
.vitolas{table-layout:fixed}
.c-name{width:27%}.c-dim{width:21%}.c-draw{width:52%}
.vitolas .draw{padding-right:0}
.vitolas tfoot td{border-top:1px solid color-mix(in srgb,var(--rule) 45%,transparent);font-size:.9rem;color:var(--quiet);vertical-align:top}
.ledger td,.ledger th{vertical-align:top}
.ledger tbody th{font-family:var(--display);font-size:1.5rem;color:var(--accent);white-space:nowrap}
@media (max-width:46rem){
  .stack thead{position:absolute;width:1px;height:1px;overflow:hidden;clip-path:inset(50%)}
  .stack tr{display:block;padding-block:1rem;border-top:1px solid color-mix(in srgb,var(--rule) 45%,transparent)}
  .stack th,.stack td{display:block;border:0;padding:.1rem 0;width:auto}
  .stack td[data-l]::before{content:attr(data-l) ": ";color:var(--quiet)}
  .vitolas{table-layout:auto}
  .vitolas .draw{padding-top:.7rem}
  .stack tfoot tr{padding-block:.6rem}
}

/* Drawings */
.cigar{width:100%;height:auto;overflow:visible}
.shadowed{filter:drop-shadow(0 5px 4px color-mix(in srgb,var(--ink) 34%,transparent))}
.leaf-connecticut{fill:var(--leaf-connecticut)}.leaf-claro{fill:var(--leaf-claro)}.leaf-colorado{fill:var(--leaf-colorado)}
.leaf-sungrown{fill:var(--leaf-sungrown)}.leaf-maduro{fill:var(--leaf-maduro)}.leaf-oscuro{fill:var(--leaf-oscuro)}
.strand,.strand-edge{fill:none;stroke-linecap:round;stroke-linejoin:round}
.strand-edge{stroke:var(--leaf-edge)}
.st-connecticut{stroke:var(--leaf-connecticut)}.st-claro{stroke:var(--leaf-claro)}.st-colorado{stroke:var(--leaf-colorado)}.st-oscuro{stroke:var(--leaf-oscuro)}
.vein{fill:none;stroke:var(--leaf-edge);stroke-width:1.1;opacity:.2}
.shade{fill:url(#cyl)}
.outline{fill:none;stroke:var(--leaf-edge);stroke-width:1.2;opacity:.65}
.ringedge{stroke:var(--leaf-edge);stroke-width:1.2}
.foot{fill:var(--leaf-edge);opacity:.5}
.foot-in{fill:var(--leaf-edge);opacity:.3}
.b-black,.b-reserva{fill:var(--ink)}.b-red{fill:var(--red)}.b-white{fill:var(--band-white)}.b-blue{fill:var(--band-blue)}.b-gold{fill:var(--brand)}.b-silver{fill:var(--band-silver)}
.r-black,.r-white{fill:var(--brand)}.r-red,.r-blue{fill:var(--band-white)}.r-reserva{fill:var(--band-silver)}
.s-hi{stop-color:var(--paper)}.s-lo{stop-color:var(--ink)}
.tick{stroke:var(--fg);stroke-width:1.3;opacity:.75}
.num{font-family:var(--text);font-size:17px;fill:var(--quiet)}
.ruler{width:100%;height:auto}

/* The bench: pick a size, lay it against the ruler */
.bench{border:0;margin:0;padding:0;min-width:0}
.bench-tabs{display:flex;flex-wrap:wrap;gap:.4rem 2rem;margin:clamp(1.6rem,3vw,2.4rem) 0 clamp(1.4rem,3vw,2.4rem)}
.bench-tabs label{cursor:pointer;font-family:var(--display);font-size:clamp(1.3rem,2.1vw,1.8rem);line-height:1.2;color:var(--quiet);padding-bottom:.2rem;border-bottom:2px solid transparent}
.bench-tabs label:hover{color:var(--fg)}
.plate{display:none;margin:0}
.plate figcaption{margin-top:1.1rem;max-width:var(--measure)}
#v-corona:checked~.plates [data-v=corona],#v-robusto:checked~.plates [data-v=robusto],#v-madsen:checked~.plates [data-v=madsen],#v-grandido:checked~.plates [data-v=grandido]{display:block}
#v-corona:checked~.bench-tabs [for=v-corona],#v-robusto:checked~.bench-tabs [for=v-robusto],#v-madsen:checked~.bench-tabs [for=v-madsen],#v-grandido:checked~.bench-tabs [for=v-grandido]{color:var(--fg);border-bottom-color:var(--accent)}
#v-corona:focus-visible~.bench-tabs [for=v-corona],#v-robusto:focus-visible~.bench-tabs [for=v-robusto],#v-madsen:focus-visible~.bench-tabs [for=v-madsen],#v-grandido:focus-visible~.bench-tabs [for=v-grandido]{outline:2px solid var(--rule);outline-offset:4px}
@media (prefers-reduced-motion:no-preference){
  .plate .cigar{animation:unsheathe 1s cubic-bezier(.2,.7,.2,1) both}
  @keyframes unsheathe{from{clip-path:inset(-20% 100% -20% 0)}to{clip-path:inset(-20% -5% -20% 0)}}
}
@media (max-width:40rem){.plate .num{display:none}}

/* Timeline */
.timeline{list-style:none;margin:0;padding:0}
.timeline li{display:grid;grid-template-columns:minmax(4.2rem,7.5rem) 1fr;gap:1.2rem;padding-block:1.35rem;border-top:1px solid color-mix(in srgb,var(--rule) 45%,transparent)}
.timeline .year{font-family:var(--display);font-size:clamp(1.7rem,3vw,2.5rem);line-height:1;color:var(--accent)}
.timeline p{margin:0;max-width:40rem}

/* Editions */
.edition{display:grid;gap:1.4rem 4rem;padding-block:clamp(2.2rem,4.5vw,3.6rem);border-top:1px solid color-mix(in srgb,var(--rule) 45%,transparent)}
.edition:first-of-type{border-top:0;padding-top:0}
.edition .when{color:var(--accent);font-family:var(--display);font-size:1.25rem;margin:0 0 .35rem}
.edition .draw{margin-top:.4rem}
.edition .dims{font-size:.92rem;color:var(--quiet);margin-top:.6rem}
@media (min-width:58rem){.edition{grid-template-columns:minmax(0,5fr) minmax(0,7fr);align-items:start}}

/* Plain lists */
.plain{list-style:none;margin:0;padding:0}
.plain li{padding-block:.75rem;border-top:1px solid color-mix(in srgb,var(--rule) 45%,transparent);max-width:46rem}
.plain li:last-child{border-bottom:1px solid color-mix(in srgb,var(--rule) 45%,transparent)}
.plain .where{color:var(--quiet);font-size:.92rem;display:block}
.source-group+.source-group{margin-top:2.6rem}
.source-group h3{margin-bottom:.9rem}
.twoup{display:grid;gap:2.5rem 4rem}
@media (min-width:52rem){.twoup{grid-template-columns:1fr 1fr}}
.more{margin-top:1.8rem}

/* Footer */
.foot-wrap{padding-block:clamp(3rem,6vw,5rem) 2.2rem}
.foot-grid{display:grid;gap:2.2rem 3rem}
@media (min-width:52rem){.foot-grid{grid-template-columns:minmax(0,4fr) minmax(0,4fr) minmax(0,4fr)}}
.foot-mark{font-family:var(--roman);font-weight:500;letter-spacing:.36em;font-size:1.3rem;color:var(--brand);margin:0 0 .5rem}
.foot-nav{list-style:none;margin:0;padding:0;columns:2;column-gap:2rem}
.foot-nav li{padding-block:.18rem;break-inside:avoid}
.foot-nav a{color:var(--paper);text-decoration:none;white-space:nowrap}
.foot-nav a:hover{text-decoration:underline}
.disclaimer{color:var(--paper)}
.legal{margin-top:2.6rem;padding-top:1.3rem;border-top:1px solid color-mix(in srgb,var(--brand) 45%,transparent);display:flex;flex-wrap:wrap;gap:.4rem 2rem;justify-content:space-between;font-size:.85rem;color:var(--muted)}
.legal p{margin:0;max-width:none}
.legal a{color:var(--muted)}

/* Age question */
.gate{border:1px solid var(--brand);background:var(--paper);color:var(--ink);max-width:min(31rem,calc(100vw - 2.5rem));padding:clamp(1.6rem,4vw,2.6rem);--rule:var(--brand-text);--link:var(--brand-text)}
.gate::backdrop{background:color-mix(in srgb,var(--ink) 90%,transparent);backdrop-filter:blur(8px)}
.gate-mark{font-family:var(--roman);font-weight:500;letter-spacing:.36em;font-size:1rem;color:var(--brand-text);margin:0 0 1.2rem}
.gate h2{font-size:clamp(1.8rem,5vw,2.4rem);margin-bottom:.8rem}
.gate p{color:var(--muted-ink)}
.gate-actions{display:flex;flex-wrap:wrap;gap:.8rem;margin-top:1.5rem}
.btn{font:inherit;cursor:pointer;padding:.7rem 1.3rem;border-radius:2px;border:1px solid var(--ink)}
.btn-gold{background:var(--brand);color:var(--brand-ink);border-color:var(--brand)}
.btn-plain{background:var(--paper);color:var(--ink)}
.btn:hover{border-color:var(--ink)}
.gate-msg{margin-top:1.3rem;color:var(--ink)}
.gate .gate-note{margin-top:1.6rem;padding-top:1rem;border-top:1px solid color-mix(in srgb,var(--brand-text) 45%,transparent);font-size:.82rem;color:var(--muted-ink)}
"""
