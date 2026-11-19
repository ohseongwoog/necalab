# NECA Lab · Design preview

Six native HTML pages in Korean and English. No dependencies or server are needed to open the site. The public academic records live in `data/catalog.json`, and all six pages are rendered from `build.py`. To rebuild, run `python3 build.py`. Open `index.html`.

## Scope and sources

- Current lab pages: [Home](https://sites.google.com/view/necalab/home), [Faculty](https://sites.google.com/view/necalab/professor), [Members](https://sites.google.com/view/necalab/members), [Publications](https://sites.google.com/view/necalab/Journal), [News](https://sites.google.com/view/necalab/news).
- The catalog includes 23 journal papers, nine international conference contributions, seven publicly listed people, five research areas, and four public lab news items. Author ordering and source links stay with each record. No student e-mails are included.
- Research illustrations are optimized from the five owner-published PNGs at `ohseongwoog/necalab`, main snapshot `da182b89ce956e63ca3ab7431dcca1763d92e27b`. They are topic illustrations, not laboratory photographs.
- [University of Seoul identity colors](https://www.uos.ac.kr/eng/web/contents/UOS_About_04_02_03): UOS Blue RGB 0/57/135 and UOS Green RGB 0/114/58. Neutral and lighter tones are layout colors. The original NECA mark is preserved byte-for-byte (SHA-256: 407b8241e7e28f8a449700ae4a8138b619a564742a648ec43f31092598fc48e5). The seven portraits came from the existing public faculty and member pages. The official university mark has not been repurposed or redrawn for this site.
- `assets/em-ai-study.svg` is an optional brand study, not the existing mark or an official university emblem. Orthogonal field axes are differentiated from a propagation line and circuit nodes. No waveguide mode is asserted.
- The home-page polar plot is a calculated, normalized principal-plane array-factor cut for an ideal uniformly excited 8×8 planar array of half-wavelength spacing, with selectable scan angles. It is not a measurement.
- The static site has no accounts, data collection or backend. Language preference is the only persistent value saved to browser local storage; no private organizational data, network addresses or connection information are distributed.

## GitHub Pages handoff

The generated assets can be placed unchanged under `preview/` on a **new independent Pages source branch**. The supplied Pages package includes a simple root landing that clearly identifies the existing lab website and the draft; it does not redirect or overwrite it. No custom domain is required, and the Google Site and repository main branch need no changes. All links and scripts are relative to the preview folder. The HTML contains noindex, nofollow, noarchive metadata; this is a discoverability signal, not access protection.

The design remains a draft until reviewed. The build intentionally requires neither a database nor a third-party font, map, analytics or script.
