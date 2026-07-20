# Figure 6 v2 QA

## Scientific and visual checks

- Core claim: current density and oxidized-carrier diffusivity provide the
  largest simulated leverage on the positive-electrode averaged saturation
  point over the declared ranges.
- Architecture: panels a and b form the solved-response row; panel c spans the
  complete lower row and is the quantitative hero. The former explanatory
  lever/node/consequence panel is absent.
- Figure-internal language was checked for internal-review phrasing. The labels
  use natural scientific terms: `Averaged saturation point`, `full simulations`,
  `continuum simulation`, `analytical scenario` and `MD-informed range`.
- `J = 80 mA cm^-2` is unambiguously right-censored: open triangle at the
  available endpoint, upward arrow, `Q_s > 40` text and `right-censored` label.
  It is not joined to either neighboring current point.
- The current line and panel-c range remain restricted to 20–40 mA cm^-2.
- Final-size color preview inspected at 180 mm: pass; labels are not clipped and
  panel c reads as the visual anchor.
- Grayscale preview inspected: pass. Evidence classes remain distinguishable by
  circles/diamonds/triangles and solid/dashed/dotted lines.

## Dimensions and raster outputs

- PDF page: `510.236 x 325.984 pt`, corresponding to `180 x 115 mm`; one page.
- SVG root: `510.23622 x 325.984252 pt`.
- Publication PNG: `2834 x 1811 px`, opaque RGB, 400 dpi.
- Publication TIFF: `4251 x 2716 px`, opaque RGB, LZW-compressed, 600 dpi.
- Final-size color preview: `2125 x 1358 px`, RGB, 300 dpi.
- Grayscale QA preview: `2125 x 1358 px`, RGB grayscale, 300 dpi.

## Typography and vector integrity

- Exact family: TeX Gyre Termes OpenType for ordinary text and mathtext.
- Base size: 7.2 pt; minimum size: 6.5 pt; panel labels: 8.0 pt bold.
- PDF contains only embedded subset TeXGyreTermes Regular, Italic and Bold CID
  OpenType fonts. `pdffonts` reports no Type 3 font.
- SVG contains 57 editable text nodes, 77 TeX Gyre Termes declarations and zero
  raster `<image>` elements.
- SVG contains no Arial, Helvetica, DejaVu, Times New Roman or Liberation font
  reference.

Exact font hashes:

| font file | SHA-256 |
|---|---|
| `texgyretermes-regular.otf` | `CC3FE7C707B81428D23D54DF3EADD9228A2BF6A4D43125D94DF56F5F63134659` |
| `texgyretermes-bold.otf` | `2FB3E952065FA153C7E4E64E04B98B9D79225739B6025AA3F0F0782D299FF61E` |
| `texgyretermes-italic.otf` | `6DD103A1672E50568CD2F8A706CCD48443D44D7D073A59D2286F4E6F746575D6` |
| `texgyretermes-bolditalic.otf` | `1BF6AF99CB0E26C12951317032D79B96AE009551E59CCF02A5B24F325ECFEC87` |

## Determinism

Two consecutive executions produced byte-identical figure and preview files:

| output | SHA-256 |
|---|---|
| PDF | `459C497BA4C1EE7FBD02121DE01601793618D4E79BFD7B3208B8776EDD28D256` |
| SVG | `133092B436B3DC9E69F219B054791A512CE57337DDD7C2A3142ECB0CBDCE0467` |
| PNG | `44034ADC46A66D28F44DC9F3EEF62655B74B8938D2DA27F8FC0C92F0993A5C9A` |
| TIFF | `FC3AE09E38C4F42A92771FBD28BC78444231F6EC6B7B699349A2370642364464` |
| 180-mm color preview | `1D97940F3DE37FB4CE05A09623B6E846D9530B57570CDAB1F448F2D6CFF790B4` |
| grayscale preview | `C5A6239549FD6FF3A6F5B41E7FAA099EBF2C2B495F2C715A0280E032732244AE` |

Fixed PDF metadata dates and a fixed SVG hash salt are used. The builder validates
the source tables through the read-only v1 evidence module before drawing.

## Preservation check

The four v1 publication outputs retain their pre-v2 hashes:

- PDF: `6E600C7DD489C2F966D1C490925B3C7AF883452E5FCEAFB714DB525A18EC3D1E`.
- SVG: `35AAE5DB1F76A05FEFD7D33F83EDC55D6033A16D55667E391A615624BD59AD8E`.
- PNG: `718C524DB4F40CD77C336D365DC6928A7E68692D74725F891C3AB69C8DAEEED3`.
- TIFF: `30396E5AD07237A5AE907904A51EF55AD5A8AF521C880C7546318E1C60FE9471`.
