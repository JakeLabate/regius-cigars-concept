# Regius Cigars staging site

A proposed website for Regius Cigars, live at https://regius.jakelabate.com/

It is presented as a gift to Regius from Demian and Mike at Cigar and Lounge, Watertown, MA:
free build, free hosting if useful, and the code transferable if Regius prefers.

Built in spec mode: Regius did not commission it. Every page carries `noindex, nofollow`,
the staging notice as its first element, and the footer disclosure. `robots.txt` disallows
everything. No Regius logo, band artwork or photography is used.

## Layout

- `main` holds the source: `build/` (generator), `palette.json`, `brand.json`, and `site/` (the built output).
- `gh-pages` holds the built site only. GitHub Pages serves this branch. The custom domain comes from the `CNAME` file.

## Rebuild

```bash
cd regius-cigars-concept
python3 build/build.py
```

`build/build.py` writes the pages into `site/`. Copy and facts live in `build/build.py`,
the drawings in `build/svgkit.py`, the stylesheet in `build/style.py`. Colours come only from
`palette.json`, which must pass the contrast gate before any change ships.

After a rebuild, rerun the gates from the auto-site-builder skill (share cards, spec SEO gate,
contrast scan, font check, card check), then publish.

## Publish

```bash
cd regius-cigars-concept
git checkout gh-pages
git checkout main -- site
cp -a site/. . && git rm -r -q --cached site && rm -rf site
git add -A && git commit -m "Republish" && git push origin gh-pages
git checkout main
```

## Sources

Every fact on the site traces to a source listed on the About page (`site/about.html`).
