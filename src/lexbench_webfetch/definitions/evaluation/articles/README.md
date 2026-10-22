# Article suite authoring

The registered `articles` suite (`articles-v11`) contains 100 qualified URLs: 95 fixed articles
and five changing post collections. `cohort.json` preserves candidate identities
and revision history; `rules.json` contains all 100 verified contracts. Public
tasks, the catalog and input manifest bind the complete executable dataset.
Full reference bodies and source observations remain external.

Candidate identities and source revisions are recorded in `cohort.json`; gaps in
case numbering preserve the original candidate IDs. Earlier authoring inputs
remain immutable. Pre-release version-1 runtime contracts are unsupported. Earlier frozen input
bytes are preserved; published results must identify their scorer version.

Four Weixin cases use user-supplied webarchives and an explicit initial-load, no-interaction attestation. The archives, source markup and full body references remain external and hash-bound. This provenance does not claim independent live browser access. They replace four singleton-platform cases without comment contracts.
Retained folded pages have explicit complete-displayed-excerpt scope; they do
not claim the hidden continuation of the original article.

## Existing contracts used as references

The [popular-site tasks](../popular-sites/tasks.json) separate stable site labels
from changing named links (for example, `global-homepage-013-yahoo-co-jp`). The
[dynamic-content tasks](../dynamic-content-100-moli-webfetch/tasks.json) add
independent source counts, same-record fields and full-body regions (for example,
`dynamic-062-zh-sspai-home` and `dynamic-023-en-mui-data-grid-pagination`). Follow
the [source-review guidance](../risk-control/rule-authoring-guide.md) for ordinary
visibility, complete scope and independent evidence.

Reuse those scoring contracts where applicable, but do not copy their current
items or counts. A named-link floor alone cannot establish article completeness:
a fixed-article case must also require the qualified full article text.
Changing collections use the separately disclosed post-coverage contract. Likewise,
an excerpt directory cannot become an article merely because a list contract
can count its links. Existing frozen suites and input versions remain unchanged.

## Required scope

Open the fixed URL and observe its first automatic load, including ordinary
already-loaded content below the viewport. Do not expand, switch tabs within
the page, log in, paginate, accept a wall or scroll to trigger loading.
Reference authors may close a login, subscription or similar
obstruction through its ordinary dismissal control. Preserve before/after
evidence and verify that the article was already loaded and its text did not
change; do not use dismissal to unlock or load additional content. This is a
reference-review exception only. Evaluated Web Fetch tasks still permit no
browser clicks, login, expansion or other content-loading interactions.
The historical reference must contain the complete qualified displayed article/post body, not a
selection of convenient paragraphs. Keep headings, paragraphs, textual lists,
table text, captions and ordinary body links within their declared scope.
Exclude image lettering, alt text, OCR, hidden markup and collapsed content.
For retained cases with folded prose, disclose a displayed-excerpt scope and
require all ordinarily displayed text within that scope. Preserve the visible
cutoff and expansion control as evidence; do not claim the full original article
or substitute hidden DOM text for the displayed excerpt. A clipping or fading
boundary needs rendered evidence, not an assumption based on accessible text.

For article feeds, require actual post text in addition to record identity,
same-record fields, real owned links where present, and independently observed
record counts. A bare directory or search-snippet list is not an article.
Use a separately reviewed `post_collection` contract for changing feeds; a
fixed-body contract cannot freeze their membership. Do not silently drop difficult platforms. Record authorized replacements or
removals in cohort history, with the original entries and review basis.

## Stable and changing regions

Review every relevant ordinary text region: title, attribution, navigation,
sidebar, footer, controls and the article itself. There is no phrase quota.
Each chosen group needs an original-language phrase, location and reason to
expect stability. Do not freeze current news recommendations, comments,
reaction counts, ranks, personalized account state or current copyright years.
Historical numbers inside a fixed article remain part of its complete body.
Consent prompts depend on session state and are not mandatory site text. Record
any obstruction and any permitted dismissal when reviewing the article scope;
do not accept binding terms or purchase access to obtain the reference.
A nonmodal notice alone does not establish a reading gate: inspect the article's
actual visibility, clipping, inert state and any modal backdrop. Already-loaded
ordinary document text below the viewport remains in scope; hidden or collapsed
body text does not.
Each declared stable group must have a matching review ID, source region,
stability basis and observation date. Repeated basis/date fields may be stored
in per-case `stable_text_review_defaults`; explicit row values take precedence.
IDs and source regions remain explicit, and empty overrides are invalid. Page-identity patterns are regular
expressions; escape punctuation when the intended identity is literal text.

Declared stable groups are mandatory in the current fixed-article contracts.
They supplement distributed body coverage; title or navigation matches cannot
replace missing article text. Reviewers divide every source line into contiguous natural chapters,
paragraphs or quotations with readable labels and explicit one-based inclusive
ranges. Current segmentation version 3 allows at most five regions. Merge adjacent
reviewed components at their existing boundaries, preserving complete text and
order. Legacy segmentation versions remain readable for prior frozen inputs.
Automatic paragraph detection is insufficient for arbitrary DOM line breaks.
Each region must contain enough ordinary text to yield a six-character fragment;
merge shorter labels into their adjacent natural component.
The version-4 body contract requires every region to reach 80% fragment coverage
and independently requires 80% coverage of the reviewed `reference_scope.end`.
A missing or empty ending is invalid. The compiler adds this requirement only
to fixed articles; changing post collections retain their separate contracts.
The generic scorer retains legacy version-3 behavior for older frozen inputs.
These are fragment-coverage tolerances, not a guarantee of exact characters,
paragraph ordering or every small module. Middle omissions can remain within
tolerance; repeated wording elsewhere may also match. Ending coverage is not
proof of its position in the output. Do not describe this as exhaustive
semantic completeness or as a precise bound on the percentage of lost characters.
Test complete output in multiple formats, missing endings and substantial
truncation. Exactly 20% character deletion is not necessarily below an 80%
fragment threshold and is not universally required to fail.

Shared HTML visibility exposes only the first direct summary of a closed native
`details` element. Its hidden descendants cannot satisfy body, anchor or record
checks; an open element retains its visible content.

An independently observed visible input placeholder or button value may use an
anchor's `visible_control` selector and attribute. This opt-in applies only to
that anchor, never to body coverage. Hidden controls, passwords, accessibility
metadata and unobserved attributes are not visible text references. The same
visible label in Markdown can match; the selector is an additional HTML
extraction path, not a requirement to preserve original site markup.

## Titles and original body text

An independently observed actual title is a separate required component. Match
the visible source heading or a standalone Markdown/plain-text title, rather
than an HTML head title, image alt text, hidden heading or code block. Do not
invent titles for titleless short posts or infer image-only titles with OCR.
Preserve every original body sentence, including a first sentence that repeats
the title. A body repetition does not replace a missing title component.

## Initially displayed comments and replies

Only cases with evidenced initially displayed comment text receive a version 2
comment contract. Include comments and replies displayed after automatic initial
loading, including below-viewport content that needs no action to load. Exclude
anything requiring clicking, expansion, tab switching, pagination, login or
scroll-triggered loading. Closed disclosures, clipped continuations and inactive
panels do not count. An empty selector during loading is not evidence of absence.

A valid record contains its own nonempty author and actual nonempty comment text.
Reply relationships, exact names, historical wording and per-comment links are
not requirements. Ordinary comments and replies may be flattened. Image-only
records and hidden/deleted/spam placeholders do not establish text coverage.
Distinct source record IDs remain distinct even when their text matches. Without
record IDs, repeated identical author-and-text pairs count once. Source identity may serve
as the author for visible pingbacks. HTML uses the reviewed selectors; text and
Markdown need recognizable author-and-body records within the comment section.
Author headings, standalone linked or bold names are supported; colon-labelled
authors require an explicit Markdown comment-section heading or the reviewed body ending.
Current text contracts locate the comment component after that ending, or use an
explicit comment heading if the ending is absent. Reviewed standalone end labels
and equal-or-higher headings terminate the component. A navigation label alone
cannot establish it. These hints are not additional required output anchors;
they keep article text and subsequent recommendations from supplying comments. Bare names and
metadata-only text are ambiguous and are not guessed as valid comments.

Cleaned HTML may use the structured text parser only when reviewed native record
containers are absent. This projection preserves headings and links and excludes
navigation, sidebars and footers; a failed native ownership check cannot be
rescued by selecting a larger fallback count. Without explicit section boundaries,
mixed author formats, unknown author headings and repeated body endings can be
indistinguishable from body subheadings, links or quoted text. The scorer does not
promise to resolve those ambiguous representations. An explicit comment heading
allows repeated body endings before that heading to be disambiguated.

Each comment/post contract requires explicit `ignored_labels` and
`unavailable_notices` lists. Post contracts also require `non_author_labels` for
permalink captions that cannot identify an author. Empty lists are valid; omitted
fields and normalized duplicates are rejected. Rules and observations share whole
label normalization for Unicode width, whitespace, case and emphasis decoration.
`rules.json` is the sole authoring source; compiled tasks carry these lists without
runtime defaults or another policy file. Earlier authoring inputs are retained as
provenance, not a supported compatibility promise; they may lack fields required
by the current scorer. Syntax recognition (HTML/Markdown, timestamps and
count decorations) remains parser code.

The minimum equals the independently reviewed valid record count when that count
is at most five; otherwise it equals 80% of that count, rounded up. The baseline
is frozen at authoring time, not refreshed for each test. This tests comment coverage:
missing the whole section or returning fewer valid records fails, while names,
wording and totals may change. It cannot prove every visible comment was captured,
or detect omissions above the minimum. Do not describe it as exhaustive comment
completeness. A site that later stops displaying comments requires a dataset
revision; historical presence does not establish permanent presence.

No fresh comment reference is acquired or required at scoring time. Historical
qualification still binds the complete independent source files by SHA-256 and
supports the presence/absence decision. Absent pages retain that evidence but
have no runtime comment contract. A date-only historical observation does not
invent a precise timestamp. Historical qualification validates saved evidence without imposing runtime
freshness or reply matching requirements.

## Changing post collections

Version 2 post contracts count distinct owned post-detail links with a nonempty
attributed author and visible post text. A genuinely empty outer post can qualify
through its attributed nonempty quoted text. A link and author alone do not count.
Duplicate links count once; quote-only links are not separate outer records.
HTML uses the reviewed selectors; ordinary linked-author Markdown is supported.
Keep the declared page-identity and stable-text checks. Do not freeze current
post identities, author names or wording.

Qualify scope from at least two independent direct initial loads. Preserve
historical qualification records and hash-bound source files outside Git.
The minimum equals the observed valid record count for baselines up to five,
or 80% rounded up above five. Only automatically displayed records qualify;
clicking, expansion, switching, login, pagination and scroll-triggered loading
remain out of scope. A displayed quote excerpt represents that excerpt only.

No runtime post reference or reference context is required for version 2.
These fixed floors detect missing fields and insufficient post coverage. They
do not prove complete per-post text, current membership, source identity beyond
the checked fields, or freshness. A website changing its initial display or
structure requires review and a dataset revision, not an automatic conclusion
that an extraction method failed.

## References and validation

Keep complete references, DOM captures, screenshots and review results outside
Git. Bind each body by UTF-8 byte hash, character count, exact opening/ending
and the complete-scope declaration. Independently inspect article boundaries,
overlays, lazy embeds and link ownership. Text extraction alone does not prove
ordinary visibility. Tool-policy or connection failures do not establish that
an evaluated method cannot fetch the article.

`lexbench_webfetch.article_dataset.compile_case` builds one verified fixed
article or post collection against an external evidence directory. `compile_dataset` requires the
entire approved inventory to be verified and refuses missing, reordered or
unresolved rules. No partial population is silently published as the suite.
The current version binds all 100 cases together. Future revisions must resolve
their whole declared population before publishing new dataset, task, catalog
and manifest bindings.

Validate through `evaluate_response`: complete independent body plus required
stable groups, actual title and sufficient valid initially displayed comment records should pass,
including reasonable Markdown/whitespace changes.
Title-only, navigation-only, wrong article, repeated opening, omitted body
regions, missing titles/comments and absent mandatory groups must fail. Keep controls synthetic in CI;
real reference validation results stay outside Git. Do not call evaluated
products while authoring. Run `make check` and submit a feature-branch PR.

To compile all verified cases from an independently acquired evidence directory:

```sh
uv run --frozen lexbench-webfetch compile-articles \
  --evidence-home /absolute/path/evidence --output /absolute/path/new-dataset.json
```

Compilation requires the exact hash-bound source files declared in the rules.
It does not download pages or call providers. Runtime scoring needs the compiled
input and response, not the historical source bundle. Compilation refuses to
overwrite existing outputs or pinned reference inputs. Source-capture controls
are supplementary external evidence; repository tests use reproducible synthetic
accepted and rejected responses.

### Updating the public bindings

`compile-articles` creates only the external dataset; it does not publish a suite
revision. Before compiling a revision, update `cohort.json` and `rules.json`
together, including the dataset ID, inventory, revision and prior-input provenance.
Keep the previous external input directory unchanged. Place the new output in a
new external directory as `dataset.json`; never commit its reference bodies.

Generate the public bindings in this order under `definitions/evaluation/articles`
(relative to `src/lexbench_webfetch`). Preserve case order from the compiled dataset.
Use UTF-8 JSON with `ensure_ascii=False`, `indent=2` and one trailing newline for
these generated files; compute file hashes from the final bytes, not parsed JSON.

1. **`dataset-catalog.json`:** retain `schema_version: 1` and
   `kind: frozen_dataset_catalog`. Copy `id`, `name` and `case_count` from the
   dataset, set `dataset` to `dataset.json`, and hash that file into
   `dataset_sha256`. For each case copy `id`, `name`, `url`, `category`, `track`
   and `task_prompt`. Set `definition_sha256` to SHA-256 of the complete case
   serialized with `json.dumps(case, ensure_ascii=False, sort_keys=True,
   separators=(",", ":")).encode("utf-8")`. Set `reference_sha256` to SHA-256 of
   `ground_truth_main_content.encode("utf-8")`, or JSON `null` for an empty body.
2. **`tasks.json`:** copy the dataset's top-level fields, replacing `cases` with
   `[lexbench_webfetch.benchmark.public_task(case) for case in dataset["cases"]]`.
   Use that projection rather than copying full cases: it removes external source
   evidence and replaces full reference text with bindings.
3. **`source-inputs.json`:** retain `schema_version: 2` and
   `kind: frozen_reference_inputs`; set `id` to the new dataset ID plus `-` and
   the first 12 dataset-hash characters. Set `catalog` to `dataset-catalog.json`
   and `catalog_sha256` to its final file hash. Set `dataset` to `dataset.json`,
   `dataset_sha256` to the dataset hash, `files` to `{"dataset.json": <dataset hash>}`
   and `trees` to `{}`. No captures belong in this bundle.
4. **`definitions/registry.json`:** change only the `articles` entry. Copy the
   new `dataset_id` and `case_count`; update its `files` hashes for `tasks.json`,
   `dataset-catalog.json` and `source-inputs.json`. Keep its directory unchanged.
5. Update the version in the top-level English/Chinese READMEs and this guide.
   Run the checks below against the new external directory, then review all
   generated changes together in the feature-branch PR. A hash match alone does
   not replace independent evidence review or accepted/rejected scoring controls.

```sh
uv run --frozen lexbench-webfetch validate --suite articles
uv run --frozen lexbench-webfetch verify-inputs --suite articles \
  --source /absolute/path/new-input-directory
make check
```

Markdown fenced and indented code blocks cannot provide article titles, comment
authors or post records. Code inside an already attributed comment remains its
body text. Post author validation applies after every extraction route, including
preceding-line attribution, native HTML and quoted posts: task-declared metadata
labels, standalone timestamps and invisible-only names cannot supply attribution.
