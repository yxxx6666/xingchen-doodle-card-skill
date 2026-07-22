# Typography Consistency Rules v0.8.10

## Goal

Make all pages look lettered by the same person with the same pen. Separate pages may vary in size and weight, but not in character construction or lettering family.

## One-family contract

Choose one explicit family token before generation and copy it unchanged into every page prompt. Default:

```text
rounded bold handwritten Chinese marker lettering, upright characters, softly squared structure, rounded stroke ends, stable medium-to-heavy stroke, compact but readable spacing, no brush-calligraphy modulation, no serif, no printed-song type, no bubble-outline lettering
```

Do not shorten, paraphrase or replace this token on later pages.

## Three-level system

1. Cover title: same family, extra-bold, largest size; maximum 1.6 times the content-page title stroke presence.
2. Content-page title: same family, bold, medium-large.
3. Body, chart labels and small labels: same family, regular, high legibility.

Maximum one family and three levels. Size and weight may change; character skeleton, stroke ends, upright angle and spacing rhythm must not.

## Exact locks

- Keep the same numeral construction across all pages, including `0`, `1`, `2`, `%`, `+`, `/` and decimal points.
- Keep punctuation shape, baseline and spacing consistent.
- Keep title alignment according to one manifest rule; allow only one explicitly declared cover exception.
- Use one emphasis treatment across the series: either a rough underline or a pale marker strip. Do not alternate randomly.
- Body text must never become decorative brush lettering, outlined display lettering or a different thin handwriting style.
- Chart labels and icon labels use the body token, not a separate technical font.
- Do not rotate ordinary text. Only a predefined decorative label component may rotate.

## Anchor-reference rule

The selected anchor page must contain normal title and body text whenever possible. When reference images are supported, use the approved anchor on every later generation and explicitly request matching:

- Chinese character skeleton;
- stroke thickness and rounded terminals;
- numeral shapes;
- title/body weight relationship;
- line spacing and character density.

## Failures requiring regeneration

- thick rounded marker title on one page and thin brush calligraphy on another;
- body text looks printed on one page and handwritten on another;
- numerals or percent signs use a visibly different family;
- title stroke thickness or character roundness drifts strongly;
- chart labels introduce a technical sans-serif look;
- a page appears lettered by a different designer.
