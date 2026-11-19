# NECA Lab. · Website design preview

This is the bilingual review site at [GitHub Pages](https://ohseongwoog.github.io/necalab/preview/). The [existing lab website](https://sites.google.com/view/necalab/home) remains separate.

Public lab news is the first section below the compact hero. Its research section links to five areas: Radar & Physical AI, AI for RF Design, 3D Chip Interconnects, RF for Fusion Plasmas, and Evidence-Grounded AI. Each area has an original, editable SVG concept diagram. The two groups in Recent research outputs are peer-reviewed journal articles and confirmed international conference presentations. They use separate inclusion checks; news items do not appear as publications.

The public catalog contains 23 journals, nine international conference contributions, seven people and four lab announcements. Source records and links stay with the entries. The lab’s [news](https://sites.google.com/view/necalab/news), [publications](https://sites.google.com/view/necalab/Journal), [faculty](https://sites.google.com/view/necalab/professor) and [members](https://sites.google.com/view/necalab/members) pages are the main public references. The illustrations are explanatory, not measured data. The hero now opens two replayable, one-minute puzzles. AI Detective pairs fictional records with a supported conclusion; Signal Builder explores transmit/receive block order and an ideal single-frequency impedance match. All six rounds work without an external service, log-in, or game-state storage.

The original lab logo and seven public portraits are preserved; the optional EM/AI logo study remains separate. Institutional colors follow the [University of Seoul visual identity](https://www.uos.ac.kr/eng/web/contents/UOS_About_04_02_03). The university emblem is not redrawn.

To rebuild, use Python 3 in this directory: `python3 build.py`, then `python3 validate.py`. The six HTML pages, their relative assets and bilingual catalog do not require a server-side application. The draft is public, with noindex metadata. No private project records are distributed.

## Interaction design

The home and Research pages share an image-first, swipeable research card deck, with native scroll snap, labelled previous/next buttons, visible position, keyboard support, and no autoplay. The five theme anchors remain directly addressable. Editorial references included [MIT Media Lab](https://www.media.mit.edu/) for concrete question-led entry points, [Google Research](https://research.google/research-areas/) for topic navigation, [Apple](https://www.apple.com/airpods-pro/) for visual highlights, and the [W3C ARIA carousel pattern](https://www.w3.org/WAI/ARIA/apg/patterns/carousel/) for accessible controls. All puzzle graphics, copy and implementations are original.
