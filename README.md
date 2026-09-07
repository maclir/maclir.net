# maclir.net

My personal site: the projects, and the story behind each one.

Hand-written HTML over one stylesheet. No build step, no framework, no
dependencies, no JavaScript — the same zero-idle-cost rule the projects it
lists are built on.

## Develop

```sh
make serve   # http://localhost:8080
make test    # every page parses, every local link and asset resolves
```

`make test` is the whole contract and runs on stock `python3`.

## Structure

```
index.html            homepage: hero, project cards
about.html            the longer version
stories/*.html        one story per project
assets/css/site.css   the only stylesheet
assets/logos/         each project's own mark, taken from its repo
scripts/check.py      make test
```

Each page sets `--accent` on `<body>` to that project's colour; the cards,
buttons, drop cap and focus rings all follow from it.

## Adding a project

1. Copy the closest story in `stories/`, change the copy, the mark and `--accent`.
2. Add a card to `index.html` in the right section.
3. Drop the project's icon into `assets/logos/` — 256px is plenty.
4. Add the page to `sitemap.xml`.
5. `make test`.

## Deploy

Push to `main`. GitHub Pages serves the branch root; `.nojekyll` keeps it from
running the content through Jekyll.
