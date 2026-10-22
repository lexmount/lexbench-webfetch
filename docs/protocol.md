# Evaluation protocol

A sample is one declared method–task logical result. Choose the complete task population, methods, versions, repetitions, timeout, concurrency and retry policy before calls. Keep the four suites separate unless a combined population and deduplication policy were declared in advance.

## Inputs and delivery

Use the original dataset verified by the suite's `source-inputs.json`. The public `tasks.json` exposes task requirements for inspection and integration; it omits complete reference text and capture metadata and cannot replace the executable frozen dataset. The original catalog binds complete task definitions through SHA-256.

A method receives the task URL and prompt. Follow the declared task kind: return body text, structured records with the required identities and links, discover the specified resources, or deliver the requested file. A successful HTTP request or nonempty response alone is insufficient. Method-specific alternate task requirements are not allowed.

Task requirements are data: expected markers, fact groups, forbidden output, minimum length, body coverage, structure and resource/file contracts are selected by the task. Missing reference coverage is unavailable, not zero or a perfect score. Binary task acceptance and text-quality diagnostics are separate. LexBench owns `score_attempt`, the shared `task_passed` predicate and file-byte acceptance. Browser Eval calls the same installed implementations. Other harnesses can use `lexbench_webfetch.evaluation.evaluate_response` or the `score` command without Browser Eval; disclose the benchmark/scorer revision when comparing scores.

Execution harnesses own acquisition provenance: validate every selected body, metadata, file, title and final-URL field against retained native evidence before calling the scorer. `score_attempt`, `evaluate_response` and CLI inputs are the submitted answer itself. `score_attempt(delivered_files=...)` accepts actual file bytes and recomputes file acceptance rather than trusting previous metrics. Native API envelopes, diagnostic log decoding, and pre-call selection policies belong to the execution harness, not the scoring package.

## Live sources and frozen evidence

Input validation proves that supplied bytes match the frozen version. It does not prove that a live website still matches that version. A publishable live-site cohort must independently verify task-relevant reference scope before calls and again after the complete declared scope. If source content changes, preserve the attempt and investigate the shared cause; do not silently refresh references or omit failed cases.

Retain the benchmark commit, suite and dataset hashes, every physical call, raw output, delivered files, exact acceptance result, error, method version and evaluator revision. Hash-bind any auxiliary evidence. Keep credentials, cookies, private page captures and internal execution logs out of public packages. The benchmark code license grants no redistribution rights to third-party content.

## Scores and timing

Report task acceptance as passed/evaluated with the declared denominator and unavailable count. Give each metric its unit and population. Report mean, P50 and P95 over the same population. Retain failed calls in the declared cohort; report all-call timing separately from each method's conditional successful-call distribution. A success-only latency distribution does not describe all attempted tasks.

Declare the score-bearing call and timing boundary before execution. If retries are allowed, retain every call, select the final response rather than the best response, and report total retry execution cost separately from any final-call latency. One retried task remains one logical sample. Record warm/cold start, local/remote execution, conversion and network differences.

## Results and corrections

A result submission must identify the immutable input and code revisions, full declared method–task matrix, saved output hashes, verdicts and denominators, errors, timing boundaries, missing results, source verification and review scope. Keep measured artifacts in a separately licensed evidence release with a stable location and integrity manifest. No leaderboard or automatic submission service is maintained here.

A requirement correction creates a new benchmark revision, with accepted and rejected scenario controls. A scoring implementation correction must fix the shared cause and rescore the complete affected scope without overwriting prior evidence. Changes to execution inputs require new calls. Independent result review is a separate operation; machine checks do not imply human review.

## Native projection and text boundaries

Projection schema 2 keeps `title` and `final_url` optional for replay of retained declarations: an absent result field yields `None` unless a declared request-URL fallback applies. An explicit default is still checked and must be empty, just as for answer fields. New declarations should state `default: null` when missing context is allowed. File projections accept only their declared byte/base64 shapes and report malformed declarations or payloads as validation errors.

Historical `fetch_log_final_url` and `video_values` formats remain replay readers for retained native declarations; they do not choose a provider interface or add a scored answer. The execution harness owns native acquisition, format selection and evidence persistence. Changing a retained declaration requires a new binding and must not rewrite historical evidence.

A flattened link label establishes multiple record fields only when its visible text retains field separators, such as line breaks or spaced vertical bars. URL slugs, English ticket-action labels and US city/state spelling cannot establish missing field boundaries. Ambiguous labels remain unqualified even when a reader can guess their intended layout. Named table columns with duplicate matching headers remain ambiguous; a navigation line without a table structure is not a column header.

A named-link group may declare `markdown_label_pattern` with a named `label` capture when a card places metadata before its visible name. The capture selects text already present in that link; it cannot supply a name from the URL. `record_start_pattern` bounds cards whose fields precede their title link. Fields before a later card start or another target link cannot complete the current record.

Text field patterns consume their matched spans, so distinct declared fields may share a physical line. Matching one field cannot reuse its value for a second requirement. Unlabeled text still needs its own evidence; relative-date controls such as “Today” do not establish a venue or source.

Required facts use body text by default. An information task may declare `match_scope: "body_or_title"` for a fact that explicitly requests a page title. This permits the delivered title field, an HTML document title, or a scalar top-level Markdown front-matter title. Keywords and descriptions cannot supply the title, and title metadata cannot supply other facts.

Contract-declared field aliases support Unicode labels. The built-in English metadata-role recognition is a limited legacy fallback, not an automatic translation dictionary. Declare the language-specific labels needed by a task rather than treating every colon in prose as a metadata separator. Body matching treats unfenced table tags as HTML, including in mixed prose. Literal code needs an explicit code fence or escape; a standalone table tag cannot disable HTML visibility rules for hidden elements or attributes.

### Reference controls for annotation revisions

A revision export runs the frozen reference through the public scorer and task
predicate, then checks that an error page fails. The resulting
`annotation-review.json` records the source and answer hashes, outcomes and scorer
identity. Resource references use URLs retained by an independent source capture,
serialized in the requested answer format; they are not generated from expected
URLs. A known reference that fails the revised contract blocks export.

Some historical input bundles retain observation hashes without the original
page bytes or an executable reference answer. Their control is `unavailable`,
never passed, and the review's `complete` flag remains false. Exporting these
frozen inputs preserves their historical definition; it does not certify the
missing evidence or create a new independent source observation.
