# Article coverage review decisions

This records the response to the [100-case review](https://github.com/lexmount/lexbench-webfetch/pull/5#issuecomment-6336835161) against `4dd9a95` and the approved `articles-v10`/`articles-v11` revisions.

- **Missing profile content in 038/041: accepted and corrected.** Both saved accessibility observations contain the bio, category, location, website and joined date. The rules now require these fields using the existing shared stable-text matcher. Paired public-scorer controls accept complete profiles and reject each missing field. No site-specific scoring branch was added.
- **Dynamic records with a one-character body: reproduced, not claimed fixed.** All five collection contracts accept distinct attributed links with nonempty text, including `x`. This is a real limit of structural coverage. The user explicitly chose reusable fixed floors without per-run source acquisition and excluded reply relationships. Reintroducing contemporary references or reply matching would change that approved contract. A minimum character count would reject legitimate short posts while accepting unrelated padding. No such patch is applied, and the suite must not be presented as proving semantic or exhaustive dynamic-body completeness.
- **Static coverage: adopt the user-approved minimal scheme 2 from the v7 review.** Version 4 requires every existing body region and the separately bound ending to reach 80%. No new module layer or website branch is published. The experimental module layer was withdrawn: 24 of 25 omission controls failed as intended, but repeated text still allowed one omission. Scheme 2 addresses the weaker 60% region allowance and unprotected tail; it does not solve every middle-module omission, ordering, table-cell or speaker association. Those stronger proposals are not claimed implemented. Exact 20% character deletion need not fail an 80% fragment rule. Format and truncation controls must substantiate the narrower contract.
- **Repeated review prose: accepted.** Per-case defaults deduplicate basis/date fields; every row retains its ID, source region and explicit exceptions. Expanded reviews and acceptance/title/comment/post contracts are unchanged by this storage change. Input version 11 preserves the already published v10 Weixin revision.
- **Retrievable evidence: valid reproducibility requirement, external distribution still outstanding.** Full input and capture bundles exist in local external storage and are hash-bound. Local paths are not a public download service. Do not commit third-party captures or claim a public bundle exists. Public rules plus a hash alone do not let a reviewer reconstruct the frozen bodies. A separately provisioned evidence location remains necessary for external reproduction.

## Weixin revision

Four user-approved articles replace 001, 002, 003 and 077, each previously the only case from its platform and without a comment contract. The population stays at 100: 95 single articles/posts and five collections; all 20 existing comment contracts remain unchanged. The new population covers 72 platform names and 75 URL hosts.

The evidence consists of four user-supplied webarchives and the user's confirmation that they were saved after normal automatic loading without interaction. It is not an independently successful live browser visit. Source captures remain external. Main-body boundaries exclude attribution, promotional cards and related-article lists; source links remain. Ordinary stable attribution/profile/control text is declared separately with per-region rationale. Hidden comment dialogs do not become visible comment requirements. The existing compiler, qualifier and scorer are reused unchanged.

## Version 11 scope

The four approved Weixin cases and all 100 URLs are preserved. Body compilation changes for 95 fixed articles; five changing collections retain their contracts. Review metadata storage changes do not relax any acceptance threshold. Prior frozen bytes remain unchanged. The v7 proposal referenced v9/v10; current publication instead advances v10 to v11 to avoid reusing the already bound version.

## Version 11 validation and limits

All 95 fixed reference bodies passed body-only checks in plain text, Markdown
blockquote and HTML-derived text (285 positive controls). Truncating the last
24% of characters failed for all 95. Removing only the declared ending failed
for 93/95; 069 and 100 still passed because matching fragments occur elsewhere.
Removing the last four blank-line-delimited paragraphs failed for 94/95; 069
still passed. These are source-based body-layer controls, not provider runs or
a claim that all 100 cases are fixed articles. No special exception was added
for these cases. Scheme 2 is a stricter coverage contract, not an ordered
end-position or semantic completeness guarantee.

Deduplication removes 7,671 repeated review fields: rules.json decreases from
3,078,113 to 2,211,902 bytes. Expanding defaults reproduces every prior review
row; acceptance, title, comment and collection contracts remain unchanged.

## Follow-up at f38bccb

The [follow-up review](https://github.com/lexmount/lexbench-webfetch/pull/5#issuecomment-6340008998) correctly distinguishes coverage limits from newly introduced bugs. Reproduction through the public scorer again accepts attributed distinct records with body `x` for all five collections, while removing their records fails. The main READMEs now disclose the structural scope directly rather than requiring readers to find it in the detailed contract. No score, floor or case is changed by that clarification.

The user explicitly retained the five changing collections; replacing them with fixed articles/posts is no longer proposed. Retention does not establish acceptance of a stronger content-completeness claim. Per-run independent reference acquisition would change the previously requested reusable-reference workflow and has not been authorized. The user has now confirmed retaining the structural contract for this PR. [Issue #9](https://github.com/lexmount/lexbench-webfetch/issues/9) tracks investigation of stronger dynamic-body coverage; it does not claim that coverage is implemented or that the reviewer approved the scope. The user has explicitly retained the five-region/80%-plus-ending fixed-body scope rather than adding per-module checks.

A private handoff package has been prepared outside Git: it contains the frozen v11 scoring input for all 100 cases, the four original Weixin webarchives, their qualified extracts and scope evidence, and a checksum manifest. All 17 data files were checked after packaging. It does not contain the remaining 96 historical browser captures. It is not yet delivered to the reviewer or hosted at a shared location. Raw archives can contain session-bearing resource URLs; preparing a local package is not authorization to publish them.


## Public reproduction follow-up

Private delivery to one reviewer would not provide public reproducibility. The
required scoring input and the original captures serve different purposes:
`dataset.json` supplies the frozen scoring references; captures support auditing
what the source displayed. A verified local scoring package exists separately
from the larger capture package, but neither is currently publicly distributed.

The v11 input passes `verify-inputs` for all 100 cases. A preliminary scan found
no token/ticket/session/authentication parameter names in its extracted URLs;
this is not a complete privacy audit or distribution clearance. The input does
not include a per-source redistribution permission manifest.

A source-policy check on 2026-10-22 found materially different conditions:
[Our World in Data](https://ourworldindata.org/faqs),
[PLOS](https://plos.org/terms-of-use/) and
[Distill](https://distill.pub/journal/) provide reuse terms that require checking
the specific content and attribution. [Quanta](https://www.quantamagazine.org/terms-conditions/)
and [Pew](https://www.pewresearch.org/about/terms-and-conditions/) do not provide
blanket permission for the proposed full-text bundle in the reviewed terms.
No separate permission for that distribution is recorded. This is not a legal
determination of statutory exceptions, and the remaining sources have not all
been reviewed. The code license does not resolve these differences.

Public distribution therefore remains open. A release must have a documented
distribution basis, appropriate notices, a stable download location and matching
hashes before it can be advertised as a reproducible public input package. Moving
the same files to Release assets does not itself supply that basis. Publishing a
permitted subset would not reproduce the complete 100-case v11 suite. Do not
silently remove cases, replace references, alter frozen bytes, or present private
delivery as completion of this requirement. No scoring changes are justified by
this distribution gap.
