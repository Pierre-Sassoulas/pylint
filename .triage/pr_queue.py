"""Render `pr-queue.html` from `pr_queue_data.json`.

The JSON holds only what the GitHub API said on the snapshot date: pull request
metadata, check-run outcomes, reviews, and the linked issues with their labels.
The lane each pull request sits in, and the two sentences next to it, are the
triage judgement and live in `V` below.

Refresh the JSON with `pr_queue_fetch.sh`, then re-run this file.
"""

from __future__ import annotations

import html
import json
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
DATA = json.loads((HERE / "pr_queue_data.json").read_text())
OUT = HERE / "pr-queue.html"

rows = {r["n"]: r for r in DATA["prs"]}
issues = {i["number"]: i for i in DATA["issues"]}

# lane key -> (label, stripe var, one-line rubric)
LANES = {
    "merge": (
        "Merge lane",
        "var(--good)",
        "Reviewed and green, or one green run away. Nothing left to decide.",
    ),
    "review": (
        "Review now",
        "var(--accent)",
        "Full CI green, no maintainer has looked, and the issue behind it is still open.",
    ),
    "approve": (
        "Approve the run",
        "var(--warn)",
        "Held in <code>action_required</code>: the test matrix has never run, so there is nothing to review yet. "
        "One click each.",
    ),
    "retrigger": (
        "Retrigger CI",
        "var(--warn)",
        "No test workflow at all — the queued run expired before anyone approved it. Needs a push or a "
        "close/reopen, not a click.",
    ),
    "author": (
        "Author's move",
        "var(--ink-faint)",
        "Red CI or requested changes. Waiting on the contributor, not on you.",
    ),
    "decide": (
        "Decide first",
        "var(--dup)",
        "The code is not the blocker — the behaviour it introduces has never been agreed.",
    ),
    "stale": (
        "Stale / take over",
        "var(--ink-faint)",
        "Author gone for a year or more. Take the branch over or close it.",
    ),
}

# n: (lane, verdict-chip-text, chip-class, finding, action)
V = {
    # ---- merge lane -------------------------------------------------------
    11640: (
        "author",
        "approved",
        "confirmed",
        "Issue 9237 (pyreverse bug): an empty module still wrote a <code>classes</code> diagram "
        "holding only the header. You approved on 11 October and asked DudeNr33 to confirm. 53 green, "
        "one cancelled job. Waiting on DudeNr33, not on you.",
        "Wait for DudeNr33's review.",
    ),
    # ---- review now -------------------------------------------------------
    11711: (
        "author",
        "changes",
        "confirmed",
        'New, 144 lines by fly1d for issue 22 (pyreverse bug, Minor, 1 reaction): <code>pyreverse --class Target a.py b.py</code> dies with <code>ValueError</code> instead of asking for a qualified class name; unknown modules/classes also gave tracebacks. Now an error on stderr, exit 1. Green, primer clean. You requested changes on 22 October: a target resolving to a non-class still warns, writes an empty diagram and exits 0; keep the warning only for Uninferable.',
        'Wait for the author.',
    ),
    11663: (
        "review",
        "ready",
        "confirmed",
        "219 lines by wesleybl for issue 11651 (FP): <code>no-self-argument</code>, "
        "<code>no-method-argument</code> and others on <code>zope.interface.Interface</code> "
        "subclasses, whose base type is not a subclass of <code>type</code>. Green, full coverage, "
        "primer only pandas noise. Triage on 13 October said the fix belongs in an astroid brain, "
        "not in the checkers.",
        "Review with that in mind: checker-side special case or astroid brain.",
    ),
    11698: (
        "review",
        "ready",
        "confirmed",
        "96 lines by mehdimirzafaruk for issue 3484 (FP, 3 reactions): <code>using-constant-test</code> "
        "on <code>if self.cached:</code> when the method has an unknown or class decorator "
        "(third-party <code>cached_property</code>). 43/43 green, full coverage. Primer removes 5 real "
        "FPs (django <code>views/generic/base.py</code> x3, home-assistant x2); rest is noise.",
        "Review.",
    ),
    11644: (
        "review",
        "ready",
        "confirmed",
        "Issue 3732 (FP, 16 reactions, High priority): <code>too-few-public-methods</code> on "
        "<code>attr.s</code> / <code>attr.dataclass</code> classes. Rebased onto "
        "<code>is_module_member</code> with a <code>level</code> check (touches your helper). 43/43 "
        "green, full coverage; primer removes 7 ansible + several home-assistant FPs.",
        "Re-review the <code>level</code> change to <code>is_module_member</code>, then merge.",
    ),
    11615: (
        "review",
        "ready",
        "confirmed",
        "Issue 10137 (bug, 3 reactions, milestone 4.1.4): <code>__Init__.py</code> with different "
        "capitalization is linted as a module on Windows. Now carries the whole-path fix from the "
        "closed #11668. 43/43 green; primer only the usual astropy/django/music21 noise.",
        "Re-review (your changes requested still standing); backport.",
    ),
    11417: (
        "review",
        "ready",
        "confirmed",
        "For and With checkers did not run on <code>async for</code> / <code>async with</code>. "
        "Milestone 4.1.4, backport label. 43/43 green; primer adds 3 home-assistant "
        "<code>too-many-nested-blocks</code> on <code>async for</code>, the intended new hits.",
        "Re-review (your changes requested still standing); backport.",
    ),
    11690: (
        "review",
        "ready",
        "confirmed",
        "New, 24 lines by agustin18 for issue 9986 (Regression FP): "
        "<code>unbalanced-dict-unpacking</code> on <code>.items()</code> of a dict held in an "
        "instance attribute or defined in another scope. Green, full coverage, primer clean.",
        "Review; backport candidate (regression).",
    ),
    11693: (
        "review",
        "ready",
        "confirmed",
        "New, 63 lines by agustin18 for issue 8567 (Regression FP): <code>unreachable</code> after "
        "<code>signal.signal(..., lambda s, f: [print(), sys.exit(1)])</code>; the lambda guard only "
        "looked at the direct parent. Green, unit + functional tests. Primer: 5 django "
        "<code>invalid-name</code> on <code>settings.X = ...</code>, unrelated to the change (the "
        "case #11691 targets).",
        "Review.",
    ),
    11683: (
        "review",
        "ready",
        "confirmed",
        "New, 18 lines by udsy19 for issue 3808 (FP): <code>unnecessary-lambda</code> on "
        "<code>lambda: (datetime.utcnow() + delta).isoformat()</code>, where the call sits inside "
        "the receiver. Green, full coverage, primer only astropy noise.",
        "Review.",
    ),
    11694: (
        "review",
        "ready",
        "confirmed",
        "New, 25 lines by agustin18 for issue 8145 (FP, 2 reactions): <code>undefined-variable</code> "
        "on <code>def meth(self) -&gt; Foo</code> in a class defined inside a function, with "
        "postponed annotations. Green, primer only astropy noise.",
        "Review.",
    ),
    11695: (
        "review",
        "ready",
        "confirmed",
        "New, 30 lines by agustin18 for issue 4993 (FP, 2 reactions): <code>unused-import</code> on "
        "<code>import gettext</code> used in a method annotation when the class later defines a "
        "<code>gettext</code> property. Green, primer only astropy noise. Uses "
        "<code>getattr(n, \"fromlineno\")</code> (AGENTS.md) and a module-wide <code>lookup</code> "
        "heuristic.",
        "Review; ask for isinstance and a narrower condition.",
    ),
    11660: (
        "review",
        "ready",
        "confirmed",
        "281 lines by agustin18 for issue 9642 (FN): <code>possibly-used-before-assignment</code> "
        "missed a name defined only in a loop body that may never run. Pushed 18 October: full "
        "patch coverage now, 43/43 green, primer clean.",
        "Review.",
    ),
    11461: (
        "review",
        "ready",
        "confirmed",
        "136 lines by agustin18 (FP): <code>invalid-overridden-method</code> when a property "
        "overrides <code>Enum.value</code>. The run was released; 48/48 green, full coverage, "
        "primer only astropy noise.",
        "Review.",
    ),
    11661: (
        "review",
        "ready",
        "confirmed",
        "85 lines by shan3520 for issue 7538 (FP): <code>used-before-assignment</code> when a branch "
        "of a nested conditional expression uses a name its test binds with a walrus. 43/43 green.",
        "Review.",
    ),
    11205: (
        "review",
        "ready",
        "confirmed",
        "Issue 7572 (enhancement, Good first issue): pyreverse <code>--theme</code> option for "
        "dark-mode diagrams, 971 lines. The author fixed the R0801 duplicate-code on 13 October; 52 "
        "green, one cancelled. Last changes requested by you on 7 October.",
        "Re-review (large); DudeNr33 also requested changes before.",
    ),
    11621: (
        "review",
        "ready",
        "confirmed",
        "Python 3.14 FN: <code>break</code>/<code>continue</code> nested deeper inside "
        "<code>finally</code> was not reported. The author fixed the three problems your tests "
        "exposed (loop <code>else</code> handling) on 12 October; 43/43 green.",
        "Review.",
    ),
    11654: (
        "review",
        "ready",
        "confirmed",
        "New, 18 lines by agustin18 for issue 5270 (FN): <code>signature-differs</code> missed "
        "keyword-only argument changes. 43/43 green.",
        "Review.",
    ),
    11645: (
        "review",
        "ready",
        "confirmed",
        "Issue 9641 (FP): <code>used-before-assignment</code> for a walrus bound in one decorator and "
        "used in a later stacked decorator. Functional test now, 43/43 green.",
        "Review.",
    ),
    11624: (
        "review",
        "ready",
        "confirmed",
        "New, 33 lines by kdelay for issue 3945 (bug): a <code># pylint: disable</code> pragma that is "
        "not the first statement of its block re-enabled every earlier line of the block, overriding "
        "<code>--disable</code> on the command line. 48/48 green.",
        "Review; backport candidate.",
    ),
    11576: (
        "review",
        "approach",
        "confirmed",
        "48/48 green, 153 lines for issue 10602. Works around astroid's "
        "<code>ClassDef.ancestors()</code> skipping a subscripted generic base "
        "(<code>GenericModel[int]</code>) inside pylint. The primer removes home-assistant "
        "<code>too-few-public-methods</code> false positives.",
        "Decide whether the fix belongs in astroid's <code>ancestors()</code> instead, then review.",
    ),
    11545: (
        "review",
        "CI running",
        "confirmed",
        "Run released on 4 October, 42 checks green so far. 41 lines, progress on issue 10423 "
        "(subscription checks look at every inferred class).",
        "Review when CI and the primer finish.",
    ),
    11396: (
        "review",
        "primer check",
        "confirmed",
        "Released and green (49/49), 50 lines. The primer reports about 190 changed or new lines on "
        "ansible, django and astropy, far more than a <code>pass</code> exemption should move.",
        "Read the primer comment before the diff: check the new messages are base drift, not the change.",
    ),
    11428: (
        "review",
        "primer check",
        "confirmed",
        "48/48 green, 114 lines, no review. The primer changes 12 astropy messages and adds 3 on astropy "
        "and music21.",
        "Review with the primer comment open; the 3 new messages decide it.",
    ),
    11480: (
        "review",
        "ready",
        "confirmed",
        "48/48 green, 113 lines. The primer drops 4 django <code>method-hidden</code> false positives, "
        "the exact case of the issue.",
        "Review. Clean primer, confirmed issue.",
    ),
    11664: (
        "review",
        "tests",
        "feature",
        "New, 426 lines by Julfried: directory-based pyreverse functional tests (regular and "
        "namespace packages), sharing the config parsing with the single-file tests. Only the "
        "changelog check is red.",
        "Add skip news, then review with DudeNr33.",
    ),
    # ---- approve the workflow run ----------------------------------------
    11714: (
        "review",
        "ready",
        "confirmed",
        'New, 23 lines by nk-batman21 for their issue 11713 (FP, reproduced on 4.1.3): <code>bad-string-format-type</code> on <code>"%-*s %d" % (width, name, count)</code>: a <code>*</code> width takes its own argument, so every later argument was checked against the wrong type. Also catches the real mismatches it used to miss. Run released 22 October: green, primer only noise.',
        'Review.',
    ),
    11717: (
        "approve",
        "held",
        "feature",
        "New, 224 lines by anyingiit (AI-generated, \"requested by winshyon\") for issue 7534 "
        "(enhancement, Help wanted, 0 reactions): optional extension "
        "<code>non-standard-exit-argument-names</code> (C3801) for <code>__exit__</code> / "
        "<code>__aexit__</code> parameters not named <code>exc_type, exc_value, traceback</code>.",
        "Low priority.",
    ),
    11697: (
        "approve",
        "held",
        "confirmed",
        "New, 43 lines by mehdimirzafaruk for issue 8628 (FP): <code>missing-param-doc</code> on "
        "Sphinx <code>:param Union[str, int] name:</code>; the regex refused a space after a comma.",
        "Approve the run.",
    ),
    11708: (
        "approve",
        "held",
        "confirmed",
        "New, 152 lines by ykakade for issue 9745 (Proposal, 0 reactions): "
        "<code>invalid-overridden-method</code> accepts a sync override that directly returns a "
        "coroutine call (<code>return sleep(0)</code>) of an async parent, and the reverse. Return "
        "annotations alone do not count.",
        "Low priority: approve with the next batch.",
    ),
    11704: (
        "approve",
        "held",
        "confirmed",
        "New, 32 lines by mehdimirzafaruk for issue 6856 (FN, 0 reactions): "
        "<code>repeated-keyword</code> skipped built-ins like <code>print(end=\"!\", "
        "**{\"end\": \"?\"})</code>, because the check came after the early return for callees "
        "without argument information. Moves the check up.",
        "Low priority: approve with the next batch.",
    ),
    11680: (
        "review",
        "ready",
        "confirmed",
        'New, 93 lines by soodoku for issue 11679 (bug, filed the same minute): <code>duplicate-code</code> reports a block copied into three files as one pair; the third copy never appears. Run released 22 October: green, primer only noise.',
        'Review.',
    ),
    11667: (
        "review",
        "ready",
        "confirmed",
        'New, 142 lines by summeriver13 for issue 7470 (FP, 1 reaction, re-confirmed by a user on 14 October): <code>function-redefined</code> for a function defined in two <code>case</code> branches of one <code>match</code>. Run released 22 October: green, primer clean.',
        'Review.',
    ),
    11666: (
        "approve",
        "held",
        "confirmed",
        "New, 54 lines by summeriver13 for issue 10827 (FP): <code>unused-wildcard-import</code> "
        "for names the module's <code>__all__</code> excludes, and <code>from . import *</code> "
        "reported as an unused <code>*</code>.",
        "Approve the run, then review.",
    ),
    11670: (
        "approve",
        "held",
        "confirmed",
        "New, 77 lines by abdull-ah-med for issue 2589 (FP): <code>redefined-outer-name</code> on a "
        "local <code>import xml.etree</code> when <code>import xml</code> is already at module "
        "level.",
        "Approve the run, then review.",
    ),
    11691: (
        "approve",
        "held",
        "confirmed",
        "New this morning, 49 lines by b84330808 for issue 9666 (FP): <code>invalid-name</code> "
        "ignores a module-level disable when <code>self._srv_status.field = ...</code> is assigned "
        "on a ctypes <code>Structure</code> defined in another module (astroid adds the attribute "
        "there, so the message lands in the other file).",
        "Approve the run, then review.",
    ),
    11692: (
        "approve",
        "held",
        "confirmed",
        "New this morning, 101 lines by b84330808 for issue 9424 (FP): "
        "<code>arguments-differ</code> when an override fills in a <code>ParamSpec</code> "
        "(<code>*args: P.args, **kwargs: P.kwargs</code>) with concrete parameters, as mypy "
        "accepts.",
        "Approve the run, then review.",
    ),
    11673: (
        "approve",
        "held",
        "confirmed",
        "New, 59 lines by mehdimirzafaruk for issue 8680 (FN, 1 reaction): "
        "<code>missing-parentheses-for-call-in-test</code> missed methods, as in <code>if "
        "self.is_on:</code>.",
        "Approve the run, then review.",
    ),
    11687: (
        "approve",
        "held",
        "confirmed",
        "New, 193 lines by ybai08 for issue 8968 (FN, 1 reaction, labelled Needs astroid update): "
        "<code>implicit-str-concat</code> missed f-strings and t-strings (<code>JoinedStr</code>, "
        "<code>TemplateStr</code>); done in pylint without the astroid change.",
        "Approve the run; decide whether the pylint-side fix is enough.",
    ),
    10953: (
        "approve",
        "held",
        "confirmed",
        "pytest-remaster for the functional suite, mchris86 branch you rebased on 17 October (10 "
        "commits); 10961 closed in its favour the same day. Run waits for approval.",
        "Approve the run; it unblocks the autofix branch stacked on it.",
    ),
    11657: (
        "review",
        "ready",
        "confirmed",
        'New, 26 lines by adityasinha-ghub for issue 11656 (FP): <code>useless-suppression</code> on disabled <code>deprecated-*</code> messages, because the exemption list still holds their pre-#6693 ids (W0402, W1505, W1511-W1513) instead of W4901-W4905. Run waits for approval. Run released 22 October: green; primer removes 20 astropy useless-suppression hits on deprecated-* disables, the intended fix.',
        'Review.',
    ),
    11659: (
        "approve",
        "held",
        "confirmed",
        "New, 70 lines by devanshranjan10 (FP+FN): <code>return-in-finally</code> flagged a "
        "<code>return</code> inside a function defined in the <code>finally</code> clause, and missed "
        "nested <code>finally</code> clauses. Same author and walk as #11621 (break/continue in "
        "finally). Run waits for approval.",
        "Approve the run; review together with #11621.",
    ),
    11230: (
        "approve",
        "held",
        "confirmed",
        "Issue 9943 (output depends on file order). New push on 12 October for the failing "
        "<code>test_package_expansion_order</code>; the run waits for approval. Astroid #3384 (cache "
        "of budget-truncated inference) targets the inference side of the same symptom (11582).",
        "Approve the run; compare with astroid #3384.",
    ),
    11655: (
        "review",
        "ready",
        "confirmed",
        'New, 44 lines by Cherith1222 for issue 9624 (FP, 1 reaction): <code>unsupported-binary-operation</code> on PEP 604 unions like <code>int | None</code> in <code>.pyi</code> stubs, which never run. Run released 22 October: green, primer only noise.',
        'Review.',
    ),
    11646: (
        "approve",
        "held",
        "confirmed",
        "Issue 5471 (enhancement, 1 reaction): new <code>misplaced-module-dunder</code> check for "
        "module dunders like <code>__all__</code> below imports (PEP 8). Grew to 201 lines on 11 "
        "October; the new run waits for approval.",
        "Approve the run; decide whether the check is wanted.",
    ),
    11631: (
        "approve",
        "held",
        "confirmed",
        "New, 49 lines by DariusHQ for issue 5363 (FP, 0 reactions, Minor): "
        "<code>subprocess-run-check</code> when <code>check</code> comes from <code>**kwargs</code> "
        "unpacking a dict that always defines it. Inference over every possible dict.",
        "Approve the run, then review.",
    ),
    11630: (
        "review",
        "ready",
        "confirmed",
        'New, 38 lines by DariusHQ for issue 7351 (FP, 1 reaction): <code>unnecessary-dunder-call</code> on <code>mock.call.method.__setitem__(1, 2)</code>, which describes an expected mock call. Walks the attribute/call chain looking for <code>unittest.mock._Call</code>. Run released 22 October: green, primer clean.',
        'Review.',
    ),
    11629: (
        "approve",
        "held",
        "confirmed",
        "New, 56 lines by DariusHQ (one of 3 PRs opened within 8 minutes) for issue 7548 (FP, 0 "
        "reactions): <code>unused-import</code> on names used only in the string type argument of "
        "<code>typing.cast(\"set[Path]\", x)</code>. Treats the first argument (or <code>typ=</code>) "
        "of <code>cast</code> as an annotation.",
        "Approve the run, then review.",
    ),
    11617: (
        "approve",
        "held",
        "confirmed",
        "New, 57 lines for issue 8577: <code>unnecessary-comprehension</code> suggests "
        "<code>list(a)</code> for <code>[(x, y) for x, y in a]</code>, which is only equivalent when "
        "the items of <code>a</code> already are tuples (for a list of lists it changes the result).",
        "Approve the run; false positive with a wrong suggestion.",
    ),
    11616: (
        "approve",
        "held",
        "confirmed",
        "New, 101 lines for issue 9517: <code>missing-timeout</code> only knew the module-level "
        "<code>requests.get()</code> and friends; it now also reports "
        "<code>requests.Session().get()</code> and the other session methods, which hang the same way "
        "without a timeout.",
        "Approve the run; false negative.",
    ),
    11614: (
        "approve",
        "held",
        "confirmed",
        "New, 36 lines, no linked issue: an <code>await</code> inside a generator expression makes it "
        "an async generator expression, which Python accepts outside an async function, so "
        "<code>await-outside-async</code> is a false positive there.",
        "Approve the run.",
    ),
    11430: (
        "approve",
        "held",
        "feature",
        "The author pushed an attrs abstract-property fix on 3 October, so a run is now waiting for "
        "approval. 57 lines teaching <code>abstract-class-instantiated</code> about attrs fields; the "
        "issue was classed as library-specific.",
        "Decide whether attrs support belongs in core, then approve the run.",
    ),
    11525: (
        "approve",
        "held",
        "feature",
        "364 lines for issue 8900, an issue never specified: an <code>isinstance</code> guard narrows a "
        "variant so <code>attribute-defined-outside-init</code> stays quiet.",
        "Approve the run, but read the narrowing rules before the tests; big for a false positive.",
    ),
    11416: (
        "approve",
        "held",
        "confirmed",
        "51 lines, <code>no-member</code> on an annotated enum value. Second PR from this contributor this month.",
        "Approve the run.",
    ),
    # ---- retrigger --------------------------------------------------------
    11581: (
        "retrigger",
        "rerun",
        "feature",
        "47 lines for issue 9818: report <code>from __future__ import annotations</code> as a syntax "
        "error below Python 3.7. 41 checks green; the primer failed on a GitHub artifact HTTP 503 "
        "(ServerBusy) before running, and fail-fast cancelled the other shards.",
        "Re-run the failed primer jobs, then review.",
    ),
    11377: (
        "retrigger",
        "no ci",
        "unrepro",
        "15 lines, the smallest open PR here, and it has sat since 3 September with no test workflow at all.",
        "Push the button that starts CI, then review — it should be a ten-minute read.",
    ),
    11376: (
        "retrigger",
        "mis-linked",
        "duplicate",
        "<b>Links an issue closed as completed in June 2024</b>, and the titles do not match: the PR is about "
        "<code>invalid-name</code> parameter kinds, the issue about <code>duplicate-argument-name</code>.",
        "Ask which behaviour is actually being fixed before spending CI on it.",
    ),
    11308: (
        "retrigger",
        "no ci",
        "confirmed",
        "31 lines, stdin line endings on Windows. Open since 19 August with no run and no comment.",
        "Retrigger, then review. Nobody has said a word to this contributor.",
    ),
    11233: (
        "retrigger",
        "no ci",
        "confirmed",
        "313 lines against a duplicate-code false positive. You reviewed it once in August; CI has never run.",
        "Retrigger before the next review round, otherwise you are reading untested code.",
    ),
    11190: (
        "retrigger",
        "no ci",
        "confirmed",
        "39 lines, <code>superfluous-parens</code> false negative. Author's last comment is a month old and "
        "unanswered.",
        "Retrigger and answer.",
    ),
    11111: (
        "retrigger",
        "no ci",
        "crash",
        "23 lines against a crash on a non-UTF-8 bytes format string. Carries <em>Blocked</em>, but the "
        "blocker is not recorded on the PR.",
        "Retrigger, and write down what it is blocked on — nobody else can tell.",
    ),
    10904: (
        "retrigger",
        "no ci",
        "feature",
        "110 lines adding a <code>:pylint:</code> Sphinx role. <b>Overlaps your own doc-linking series</b> — same "
        "target, different mechanism.",
        "Decide which mechanism wins before reviewing. Yours is further along; say so on the PR either way.",
    ),
    10950: (
        "retrigger",
        "no ci",
        "confirmed",
        "61 lines protecting versioned functional-test output from <code>--update-functional-output</code>. Small "
        "and squarely a maintainer concern.",
        "Retrigger and review — this is test-harness hygiene you benefit from directly.",
    ),
    11421: (
        "retrigger",
        "no ci",
        "confirmed",
        "141 lines, <code>no-member</code> on a contextmanager's generator return type. No test workflow "
        "ever ran.",
        "Retrigger. Same author as the next row: one close/reopen each.",
    ),
    11422: (
        "retrigger",
        "no ci",
        "confirmed",
        "233 lines on the confirmed isinstance-narrowing false positive in chained <code>and</code>. No "
        "test workflow ever ran.",
        "Retrigger. The size needs a primer run before review.",
    ),
    # ---- author's move ----------------------------------------------------
    11672: (
        "author",
        "changes",
        "crash",
        "Crash 9277 (2 reactions): <code>UnicodeEncodeError</code> when stdout cannot encode a "
        "message. Green, chrikrah approved, but you requested changes on 22 October: the 9277 "
        "traceback goes through colorama's <code>AnsiToWin32</code> wrapper in "
        "<code>ColorizedTextReporter</code>, which this PR may not fix; plus a fragment rewording.",
        "Wait for the author's answer on the colorama path.",
    ),
    11682: (
        "author",
        "red",
        "confirmed",
        "72 lines by soodoku for issue 11681 (bug): <code>ignore-comments</code> of "
        "<code>duplicate-code</code> cut lines at a <code>#</code> inside a string; now uses "
        "<code>tokenize</code>. Run released 22 October: the spelling check fails on "
        "<code>Tokenizing</code> / <code>tokenized</code>; tests still running.",
        "Wait for the spelling fix (or add the words to the dictionary).",
    ),
    11715: (
        "author",
        "red",
        "confirmed",
        "New, 127 lines by fly1d for issue 9160 (FP, 0 reactions): <code>import-private-name</code> on "
        "<code>from _sibling import Public</code> when <code>_sibling.py</code> sits next to the file. "
        "Only the spelling check fails (<code>initializers</code> in a comment); primer only noise.",
        "Wait for the one-word fix, then review.",
    ),
    11675: (
        "author",
        "changes",
        "crash",
        "Crash 11674: <code>--jobs</code> above 1 crashes with <code>PermissionError</code> when "
        "<code>ProcessPoolExecutor</code> cannot be created (sandbox). Green. You requested changes "
        "on 22 October: check more before trying the pool so a one-CPU machine does not create an "
        "executor for nothing (+15 to +40 ms).",
        "Wait for the author.",
    ),
    11641: (
        "author",
        "red",
        "confirmed",
        "Issue 10025 (FP): <code>import-self</code> when an extensionless script has the same "
        "basename as an importable module. 42/43: only the spelling check fails on "
        "<code>extensionless</code> in a docstring. Primer only noise.",
        "Ask for the one-word fix; then re-review.",
    ),
    11579: (
        "author",
        "blocked",
        "feature",
        "Enhancement: flag calls in default arguments, extending "
        "<code>dangerous-default-value</code>. chrikrah blocked on 16 October: the docs still name "
        "the deleted <code>allowed-default-calls</code> option, and <code>object()</code>, "
        "<code>complex()</code>, <code>range()</code> now raise W0102.",
        "Waiting on the author.",
    ),
    11662: (
        "author",
        "astroid",
        "confirmed",
        "New, 120 lines by Anandb71 for issue 9192 (FN): <code>modified-iterating-list</code> missed "
        "lists astroid cannot infer. You requested on 14 October that astroid infers better instead "
        "of pylint accepting inference failure; labelled Blocked / Needs astroid update.",
        "Waiting on an astroid fix.",
    ),
    11424: (
        "author",
        "astroid",
        "confirmed",
        "Issue 10091 (FP): <code>no-member</code> on <code>__value__</code> of a PEP 695 "
        "<code>type</code> alias. The author is writing the astroid change (alias name infers to a "
        "<code>typing.TypeAliasType</code> instance); you want to keep this PR for its regression "
        "tests.",
        "Wait for the astroid PR, then trim this one to tests.",
    ),
    11618: (
        "author",
        "waiting",
        "feature",
        "You requested changes on 10 October. Docs for issue 8196 (<code>too-many-locals</code> "
        "rationale).",
        "Waiting on the author.",
    ),
    11409: (
        "author",
        "astroid",
        "confirmed",
        "The author opened astroid #3371 on 9 October as you asked (bind the class to a metaclass "
        "method; the typing brain rebuilt its <code>Meta</code> template on every inference, which "
        "broke an identity check). This PR waits for that. Issue 10042 (<code>not-callable</code> when "
        "inheriting from <code>typing.IO</code>).",
        "Review astroid #3371; this PR becomes a test or closes.",
    ),
    11432: (
        "author",
        "waiting",
        "confirmed",
        "You requested changes on 4 October (much shorter "
        "<code>_unused_sibling_submodule_imports</code>, sketched in the review). Only "
        "<code>codecov/project</code> red. Your local review: the 4 primer hits are true positives; an "
        "<code>__all__</code> false positive and a one-line <code>import a.x, a.y</code> false negative "
        "remain.",
        "Waiting on the author.",
    ),
    11469: (
        "author",
        "waiting",
        "confirmed",
        "The one PR kept for issue 8460 (#10903 and #11540 closed in its favour, 4 October). Milestone "
        "4.2.0. You asked for an error on a non-boolean value (<code>exit-zero = \"maybe\"</code>), an "
        "INI test, an <code>errors-only = false</code> test, and to reuse #10903's functional config "
        "tests with a Co-authored-by trailer.",
        "Waiting on the author.",
    ),
    11370: (
        "author",
        "waiting",
        "confirmed",
        "One red check. Reviewed once by a maintainer, no follow-up from the author since August.",
        "Ping.",
    ),
    11171: (
        "author",
        "waiting",
        "confirmed",
        "49/49 green but changes requested and untouched since mid-July.",
        "Ping — green CI with an open request is easy to forget.",
    ),
    11241: (
        "author",
        "waiting",
        "confirmed",
        "Conflicting, no CI, four reviews deep. Author replied end of August.",
        "Needs a rebase from the author before anything else.",
    ),
    11255: (
        "author",
        "waiting",
        "confirmed",
        "Changes requested, no CI run, author's last reply in mid-August.",
        "Waiting on the author.",
    ),
    11132: (
        "author",
        "waiting",
        "confirmed",
        "<em>Waiting on author</em> since July, backport label set, no CI.",
        "Waiting on the author.",
    ),
    11177: (
        "author",
        "waiting",
        "feature",
        "Optional pytest-random-order for isolation hunting; one red check, one maintainer review.",
        "Low stakes, decide yes or no rather than letting it age.",
    ),
    11194: (
        "author",
        "waiting",
        "feature",
        "636 lines adding a whole new docparams message, conflicting, three red checks, zero reviews.",
        "Say up front whether a new W9022 is wanted; do not read 636 lines first.",
    ),
    10749: (
        "author",
        "waiting",
        "feature",
        "891 lines over 17 files for a type-annotations checker. Green, changes requested, silent since June.",
        "Too big to land as-is. Ask for a split or close it.",
    ),
    11398: (
        "author",
        "waiting",
        "confirmed",
        "Released: one check red out of 49. 23 lines on the confirmed "
        "<code>consider-using-f-string</code> false positive.",
        "Point the author at the red check.",
    ),
    11411: (
        "author",
        "waiting",
        "confirmed",
        "Released: 2 checks red out of 48, patch coverage 85%, and no changelog fragment.",
        "Waiting on the author.",
    ),
    11450: (
        "author",
        "waiting",
        "feature",
        "You asked on 25 September whether the regex approach extends to other names, like pylint's own "
        "message names.",
        "Waiting on the author's answer.",
    ),
    11475: (
        "author",
        "waiting",
        "feature",
        "Green, but you asked on 26 September to cover two related issues too: 123 lines for a message "
        "that only fires next to an import error.",
        "Waiting on the author.",
    ),
    11223: (
        "author",
        "rebase",
        "confirmed",
        "Conflicts with main since #11011 landed the ignore-paths pruning and the sorted walk on 27 "
        "September. The package-root discovery part is still its own.",
        "Ask for a rebase onto #11011, keeping only the package-root fix.",
    ),
    # ---- decide first -----------------------------------------------------
    11650: (
        "decide",
        "approved",
        "crash",
        "Crash 10278: <code>ImportError: Unable to find module</code> when an implicit namespace "
        "package also exists in site-packages or shadows a stdlib package. 41/41 green, primer "
        "clean, chrikrah approved, milestone 4.1.4. On 20 October the author corrected their answer "
        "to your astroid question: a path-aware <code>is_namespace(modname, path=None)</code> is "
        "about six lines in astroid, keeps the 1756 guard and fixes 10278. Asks which you prefer: "
        "astroid PR, or this pylint fix shipped in a patch release meanwhile.",
        "Answer: both (merge this for 4.1.4, astroid PR for the real fix, revert here once pinned), "
        "or astroid only.",
    ),
    11678: (
        "decide",
        "design",
        "feature",
        "New, 513 lines by soodoku for issue 11677 (filed the same minute): an "
        "<code>ignore-local-names</code> option so <code>duplicate-code</code> matches blocks that "
        "differ only by renamed locals. One of 3 issue+PR pairs this account opened within 9 "
        "minutes on 18 October; the issue carries measurements.",
        "Decide whether the option is wanted before reading 513 lines.",
    ),
    11648: (
        "decide",
        "dup",
        "confirmed",
        "New, 104 lines by agustin18 for issue 11647 (FP): <code>undefined-variable</code> on a "
        "walrus in a comprehension condition after a bare <code>x: int</code> annotation. Duplicates "
        "your #11649 (opened 4 hours later, written earlier). This one rewrites the line-order test "
        "for every comparison inside a comprehension; yours only exempts a <code>NamedExpr</code> in "
        "the condition and keeps the self-referencing TP.",
        "Close in favour of #11649, or credit the author.",
    ),
    11601: (
        "decide",
        "design",
        "feature",
        "New, 145 lines for issue 10731: report <code>no-value-for-parameter</code> on a method call when the "
        "receiver is Uninferable but annotated, by inferring the instance from the annotation. Pylint does not "
        "infer from annotations elsewhere, so this is a design shift. Same author as astroid #3359 (closed as a "
        "duplicate).",
        "Decide whether annotation-based inference belongs in pylint (or astroid) before running CI.",
    ),
    11587: (
        "decide",
        "lib-specific",
        "feature",
        "New, 237 lines for issue 9090 (1 reaction, <em>Lib specific</em>): teach "
        "<code>unexpected-keyword-arg</code> about Pydantic field aliases (<code>Field(alias=)</code>, "
        "<code>validation_alias</code>, <code>AliasChoices</code>). Pydantic-specific knowledge in core "
        "pylint; astroid synthesizes the dataclass <code>__init__</code>.",
        "Decide whether this belongs in pylint, an astroid brain, or a pydantic plugin before running "
        "CI.",
    ),
    11502: (
        "decide",
        "design",
        "feature",
        "Issue 8912: render the real <code>--enable</code>/<code>--disable</code> defaults in "
        "all-options. You objected to the long list; the author answered on 30 September (ruff and "
        "eslint use rule prefixes and presets) and reworked it. The CI run is held.",
        "Settle what the page should list, then approve the run.",
    ),
    11539: (
        "decide",
        "close?",
        "feature",
        "227 lines of annotation changes across 8 files for issue 11524 (no runtime defect). Part of a "
        "burst of 4 PRs from the same new account in one day.",
        "Decide whether issue 11524 is wanted at all before reviewing 227 lines.",
    ),
    10600: (
        "decide",
        "needs decision",
        "feature",
        "A maintainer's own PR for a new CodeStyle check, one red check, <em>Needs decision</em> since 2025.",
        "This is a maintainer-to-maintainer decision, not a review. Settle it.",
    ),
    10658: (
        "decide",
        "needs decision",
        "feature",
        "Six red checks; the issue carries <em>Needs decision</em>. Overlaps 10962 exactly.",
        "Decide the <code>len()</code>-versus-zero question once and close whichever PR loses.",
    ),
    10962: (
        "decide",
        "needs decision",
        "feature",
        "Eleven red checks, marked <em>Blocked</em>, targeting the same issue as 10658.",
        "Same decision as 10658. Two contributors are waiting on one call.",
    ),
    10793: (
        "decide",
        "needs decision",
        "feature",
        "Eight red checks, no reviews, <em>Needs decision</em> on the issue since 2025.",
        "Decide whether the message is wanted before anyone rebases it.",
    ),
    10759: (
        "decide",
        "blocked",
        "feature",
        "SARIF reporter, 16 reviews, one red check, <em>Blocked</em>. The author is still responsive.",
        "The blocker needs naming. Sixteen rounds without one is a process failure, not the author's.",
    ),
    10619: (
        "decide",
        "wip",
        "feature",
        "A maintainer's own WIP draft for a default message set; the issue needs a specification first.",
        "Specification before code. Related to your own preset work — keep them in one place.",
    ),
    9967: (
        "decide",
        "needs decision",
        "feature",
        "Source-roots fallback, conflicting, no CI, no reviews; the issue carries <em>Needs decision</em>.",
        "Decide the fallback semantics, then ask for a rebase — not the other way round.",
    ),
    11393: (
        "decide",
        "close?",
        "feature",
        "Rebased and released again, but it is 12 lines of test that <b>pins the current false positive "
        "as expected output</b>. The author confirmed it fixes nothing.",
        "Decide whether a reproducer that expects the bug is worth merging; otherwise close it.",
    ),
    11439: (
        "decide",
        "needs decision",
        "feature",
        "97 lines on generic Protocol subscription. The issue was classed as needing a spec first.",
        "Agree on the expected behaviour in the issue before approving a run.",
    ),
    # ---- stale ------------------------------------------------------------
    11277: (
        "stale",
        "close?",
        "duplicate",
        "Draft with no CI and no comment; <b>the issue it closes was closed as a duplicate today</b>.",
        "Close it, pointing at the surviving issue.",
    ),
    10333: (
        "stale",
        "abandoned",
        "duplicate",
        "Changes requested in April 2025, no reply since. One of the two issues it claims is already closed.",
        "Take over or close.",
    ),
    10190: (
        "stale",
        "abandoned",
        "unrepro",
        "Marked <em>Work in progress</em>, no CI, no reviews, last touched by a maintainer in March 2025.",
        "Close with thanks; the issue stays open.",
    ),
    9806: (
        "stale",
        "abandoned",
        "unrepro",
        "31 lines of pyreverse docs, two maintainer reviews, author gone since 2024.",
        "Rewrite the 31 lines yourself — faster than another ping.",
    ),
    9721: (
        "stale",
        "abandoned",
        "unrepro",
        "Out-of-source linting, no reviews in two years, conflicting, <em>Needs take over</em>.",
        "Take over or close.",
    ),
    9693: (
        "stale",
        "abandoned",
        "unrepro",
        "A test that documents a pyreverse gap. Mergeable, no CI, author gone since 2024.",
        "The test alone has value — take it over.",
    ),
    9690: (
        "stale",
        "abandoned",
        "unrepro",
        "34 lines fixing functional-test ref updating; changes requested in 2024, never answered.",
        "Take over — it is one file and you know the harness.",
    ),
    9550: (
        "stale",
        "abandoned",
        "duplicate",
        "Preliminary per-directory-config work, conflicting, 14 reviews, silent since 2024. Pairs with 9395.",
        "Decide the per-directory-config story once, then close both or take both.",
    ),
    9395: (
        "stale",
        "abandoned",
        "duplicate",
        "The larger half of the same per-directory-config attempt. Conflicting, changes requested, <em>High "
        "priority</em> on the issue.",
        "High priority and abandoned is a bad combination — either own it or say it is not happening.",
    ),
    5401: (
        "stale",
        "abandoned",
        "feature",
        "The pylintd daemon, opened in 2021, conflicting, no CI.",
        "Close it. Four years is an answer.",
    ),
}

LANE_ORDER = ["merge", "review", "approve", "retrigger", "author", "decide", "stale"]

missing = sorted(
    n for n, r in rows.items() if n not in V and not r["a"].startswith("app/")
)
extra = sorted(n for n in V if n not in rows)
assert not missing, f"no verdict for {missing}"
assert not extra, f"verdict for a closed PR: {extra}"


# A PR labelled "Needs review" waits on another maintainer: nothing you can
# do about it, so it sits with the ones waiting on their author.
WAITING_ON_SOMEONE_ELSE = "Needs review"


def lane_of(n: int) -> str | None:
    lane = V.get(n, (None,))[0]
    if lane in ("merge", "review", "approve") and any(
        label.startswith(WAITING_ON_SOMEONE_ELSE) for label in rows[n]["labels"]
    ):
        return "author"
    return lane


E = html.escape


def issue_cell(links: list) -> str:
    if not links:
        return '<span class="repro na">no linked issue</span>'
    out = []
    for number, _state, _labels in links:
        info = issues.get(number, {})
        state = info.get("state", "?")
        reason = info.get("state_reason") or ""
        labels = info.get("labels", [])
        kinds = ("Crash", "False Positive", "False Negative", "Bug", "Enhancement")
        sought = ("Help wanted", "Good first issue", "Hacktoberfest", "High priority")
        kind = next((name for name in labels if name.startswith(kinds)), "")
        wanted = [name for name in labels if name.startswith(sought)]
        cls = "no" if state == "closed" else "yes"
        tail = f" — {E(reason)}" if state == "closed" and reason else ""
        bits = [f'<span class="repro {cls}">#{number} {E(state)}{tail}</span>']
        if kind:
            bits.append(f'<span class="lab">{E(kind)}</span>')
        for w in wanted:
            bits.append(f'<span class="lab">{E(w)}</span>')
        out.append("".join(bits))
    return "".join(out)


# Category first, then High priority, then reactions on the open linked
# issues, then the most recently updated. Read from the PR labels, falling
# back to the labels of its linked issues.
CATEGORIES = ("Crash", "performance", "Bug", "False Positive", "False Negative", "Enhancement")


def priority(n: int) -> tuple:
    r = rows[n]
    linked = [issues.get(number, {}) for number, _state, _labels in r["links"]]
    labels = list(r["labels"])
    for info in linked:
        labels.extend(info.get("labels", []))
    found = {c for c in CATEGORIES for name in labels if name.startswith(c)}
    # Many false-positive issues also carry "Bug": the FP/FN label is the
    # more precise kind, so "Bug" only counts when neither is present.
    if found & {"False Positive", "False Negative"}:
        found.discard("Bug")
    category = min((CATEGORIES.index(c) for c in found), default=len(CATEGORIES))
    # Crash and performance share the top rank.
    category = max(category - 1, 0)
    high = any(name.startswith("High priority") for name in labels)
    reactions = sum(
        info.get("reactions", 0) for info in linked if info.get("state") == "open"
    )
    return (category, not high, -reactions, "".join(chr(0x10FFFF - ord(c)) for c in r["updated"]))


# PRs whose new tests were run with the source files reset to main (they must
# fail) and with the PR merged into main (they must pass): n -> date checked.
TESTED = {
    n: "2026-10-22"
    for n in (
        11648, 11654, 11655, 11657, 11659, 11660, 11661, 11666, 11667, 11670,
        11672, 11673, 11675, 11676, 11678, 11680, 11682, 11683, 11687, 11690,
        11691, 11692, 11693, 11694, 11695, 11697, 11698, 11703, 11704, 11708,
    )
}


def category_name(n: int) -> str:
    rank = priority(n)[0]
    return ("crash / perf", "bug", "false positive", "false negative", "enhancement", "other")[rank]


CI_WORDS = {
    "green": ("all green", "no"),
    "failing": ("red", "yes"),
    "running": ("running", "na"),
    "not-run": ("never ran", "yes"),
    "awaiting-approval": ("held for approval", "yes"),
}

body = []
for lane in LANE_ORDER:
    label, stripe, rubric = LANES[lane]
    members = [n for n in rows if lane_of(n) == lane]
    members.sort(key=priority)
    body.append(
        f'<section class="lane" data-lane="{lane}">'
        f'<h2 style="--stripe: {stripe}">{E(label)} <span class="count">{len(members)}</span></h2>'
        f'<p class="rubric">{rubric}</p>'
        f'<div class="scroll"><table><thead><tr>'
        f"<th>PR</th><th>What</th><th>State</th><th>Why it sits here</th><th>Next move</th>"
        f"</tr></thead><tbody>"
    )
    for n in members:
        r = rows[n]
        _lane, chip, chip_cls, finding, action = V[n]
        ci_word, ci_dot = CI_WORDS[r["ci"]]
        fails = f" ({r['cifail']} failing)" if r["cifail"] else ""
        conflict = (
            '<span class="lab">conflicting</span>'
            if r["merge"] == "CONFLICTING"
            else ""
        )
        draft = '<span class="lab">draft</span>' if r["draft"] else ""
        tested = (
            f'<span class="repro no">tests fail on main, pass with PR ({TESTED[n]})</span>'
            if n in TESTED
            else ""
        )
        reviewers = ", ".join(r["mrev"]) if r["mrev"] else "none"
        body.append(
            "<tr>"
            f'<td class="id"><a href="https://github.com/pylint-dev/pylint/pull/{n}">#{n}</a>'
            f'<span class="date">{E(r["a"])}</span>'
            f'<span class="date">{E(r["created"])} → {E(r["updated"])}</span></td>'
            f'<td class="what"><span class="t">{E(r["t"])}</span>'
            f'<span class="msg">{r["size"]} lines · {r["files"]} files</span>{draft}{conflict}'
            f'<span class="lab">{E(category_name(n))}</span></td>'
            f'<td class="verdict"><span class="chip {chip_cls}">{E(chip)}</span>'
            f"{tested}"
            f'<span class="repro {ci_dot}">CI {ci_word}{fails}</span>'
            f'<span class="repro na">reviewed by {E(reviewers)}</span>'
            f'{issue_cell(r["links"])}</td>'
            f'<td class="finding">{finding}</td>'
            f'<td class="action">{action}</td>'
            "</tr>"
        )
    body.append("</tbody></table></div></section>")

# "To do now": the few items worth acting on today, in priority order. A held
# run is only worth approving for a crash, a bug, a High priority item or an
# issue with at least two reactions; the rest of the approve lane can wait.
TODO_REVIEW = 8
TODO_APPROVE = 8
APPROVE_LOOP = (
    'for pr in {numbers}; do sha=$(gh pr view "$pr" --repo pylint-dev/pylint --json headRefOid '
    "--jq .headRefOid); gh api \"repos/pylint-dev/pylint/actions/runs?head_sha=$sha&amp;"
    "status=action_required\" --jq '.workflow_runs[].id' | xargs -I{{}} gh api -X POST "
    '"repos/pylint-dev/pylint/actions/runs/{{}}/approve"; done'
)


def lane_members(lane: str) -> list:
    return sorted((n for n in rows if lane_of(n) == lane), key=priority)


def worth_a_run(n: int) -> bool:
    category, not_high, minus_reactions, _ = priority(n)
    return category <= 1 or not not_high or minus_reactions <= -2


KIND_NAMES = ("crash / perf", "bug", "false positive", "false negative", "enhancement", "other")


def why(category: int, high: bool, reactions: int, refs: list, ci: str, extra: list) -> str:
    """The reasons behind an item's place, in the order the ranking uses them."""
    parts = [KIND_NAMES[category]]
    if high:
        parts.append("High priority")
    if reactions:
        parts.append(f"{reactions} reaction{'s' * (reactions > 1)} on {', '.join(refs)}")
    parts.append(f"CI {CI_WORDS[ci][0]}")
    parts.extend(extra)
    return " · ".join(parts)


def todo_item(n: int) -> str:
    r = rows[n]
    category, not_high, minus_reactions, _ = priority(n)
    refs = [
        f"#{number}"
        for number, _s, _l in r["links"]
        if issues.get(number, {}).get("state") == "open"
        and issues.get(number, {}).get("reactions")
    ]
    extra = [f"reviewed by {', '.join(r['mrev'])}"] if r["mrev"] else []
    if n in TESTED:
        extra.append("tests fail on main, pass with the PR")
    return (
        f'<li><a href="https://github.com/pylint-dev/pylint/pull/{n}">#{n}</a> '
        f'<span class="k">{E(category_name(n))}</span>{E(r["t"])} '
        f'<span class="do">— {V[n][4]}</span>'
        f'<span class="why">Why here: {why(category, not not_high, -minus_reactions, refs, r["ci"], extra)}</span>'
        "</li>"
    )


todo_approve = [
    n
    for n in lane_members("approve")
    if rows[n]["ci"] == "awaiting-approval" and worth_a_run(n)
][:TODO_APPROVE]
todo = [
    '<section class="todo"><h2>To do now</h2>'
    '<p class="rubric">Ordered by what unblocks a release or a user first: merges cost one click and ship '
    "fixes, reviews of green pull requests come next, then runs worth releasing, then decisions. Inside "
    "each step the order is the lanes' ranking: crash or performance, bug, false positive, false "
    "negative, enhancement; then High priority; then reactions on the open linked issues. A held run "
    "is only listed for a crash, a bug, High priority or two reactions.</p>"
]
for title, items in (
    ("1. Merge", lane_members("merge")),
    ("2. Review", lane_members("review")[:TODO_REVIEW]),
    ("3. Approve the run", todo_approve),
    ("4. Decide (crash or bug)", [n for n in lane_members("decide") if priority(n)[0] <= 1]),
):
    if not items:
        if items is todo_approve:
            todo.append(
                f"<h3>{title}</h3><p class=\"rubric\">Nothing worth a run today: every held pull "
                "request is a false positive, false negative or enhancement with fewer than two "
                "reactions.</p>"
            )
        continue
    todo.append(f"<h3>{title}</h3><ol>")
    todo.extend(todo_item(n) for n in items)
    todo.append("</ol>")
    if items is todo_approve:
        todo.append(f"<pre>{APPROVE_LOOP.format(numbers=' '.join(map(str, items)))}</pre>")

# Astroid: the same ranking over astroid_queue_data.json (astroid_queue_fetch.py).
# Kinds come from the PR labels plus those of the astroid issues it closes and
# the pylint issues it names; reactions count on all of those.
ASTROID_FILE = HERE / "astroid_queue_data.json"
if ASTROID_FILE.exists():
    ASTROID = json.loads(ASTROID_FILE.read_text())
    ASTROID_NOTES = {
        # n: (step, action, note) for what the data cannot tell; step is one of
        # "merge", "review", "approve", "ping", "skip".
    }

    def astroid_priority(p: dict) -> tuple:
        labels = list(p["labels"])
        for linked in p["links"]:
            labels.extend(linked["labels"])
        names = [name.lower() for name in labels]
        found = set()
        for rank, keys in enumerate(
            (("crash", "performance"), ("bug",), ("false positive",), ("false negative",), ("enhancement", "brain"))
        ):
            if any(key in name for key in keys for name in names):
                found.add(rank)
        if found & {2, 3}:
            found.discard(1)
        category = min(found, default=5)
        high = any(name.startswith("high priority") for name in names)
        reactions = sum(linked["reactions"] for linked in p["links"] if linked["state"] == "open")
        return (category, not high, -reactions, "".join(chr(0x10FFFF - ord(c)) for c in p["updated"]))

    def astroid_item(p: dict, action: str) -> str:
        category, not_high, minus_reactions, _ = astroid_priority(p)
        refs = [
            linked["ref"].replace("pylint-dev/", "")
            for linked in p["links"]
            if linked["state"] == "open" and linked["reactions"]
        ]
        extra = []
        if p["milestone"]:
            extra.append(f"milestone {p['milestone']}")
        if p["rd"] == "APPROVED":
            extra.append("approved")
        elif p["rd"] == "CHANGES_REQUESTED":
            extra.append("changes requested")
        extra.append(f"{p['size']} lines")
        note = ASTROID_NOTES.get(p["n"], (None, None, ""))[2]
        if note:
            extra.append(note)
        return (
            f'<li><a href="https://github.com/pylint-dev/astroid/pull/{p["n"]}">astroid #{p["n"]}</a> '
            f'<span class="k">{E(KIND_NAMES[category])}</span>{E(p["t"])} '
            f'<span class="do">— {action}</span>'
            f'<span class="why">Why here: {why(category, not not_high, -minus_reactions, refs, p["ci"], extra)}</span>'
            "</li>"
        )

    def astroid_step(p: dict) -> str:
        if p["n"] in ASTROID_NOTES:
            return ASTROID_NOTES[p["n"]][0]
        if p["draft"]:
            return "skip"
        category, not_high, minus_reactions, _ = astroid_priority(p)
        worth = category <= 1 or not not_high or minus_reactions <= -2
        if p["a"] == OWNER:
            # Your own: only worth a reviewer ping when it unblocks something.
            return "ping" if worth or p["milestone"] else "skip"
        if p["ci"] == "green" and p["rd"] == "APPROVED":
            return "merge"
        if p["ci"] == "green" and p["rd"] != "CHANGES_REQUESTED":
            return "review" if worth else "skip"
        if p["ci"] == "awaiting-approval":
            return "approve" if worth else "skip"
        return "skip"

    OWNER = DATA["owner"]
    steps: dict = {"merge": [], "review": [], "approve": [], "ping": []}
    for p in sorted(ASTROID["prs"], key=astroid_priority):
        step = astroid_step(p)
        if step in steps:
            steps[step].append(p)
    default_action = {
        "merge": "Merge.",
        "review": "Review.",
        "approve": "Approve the run, then review.",
        "ping": "Ask another maintainer for a review.",
    }
    todo.append(
        f'<h3>5. Astroid <span class="count">snapshot {E(ASTROID["snapshot"])}</span></h3>'
        '<p class="rubric">Same ranking. A fix in astroid reaches pylint users only after an astroid '
        "release and a bump of pylint's minimum astroid version, so a crash or bug fix there weighs as "
        "much as one in pylint. Your own pull requests are listed when they unblock something "
        "(crash, bug, performance, reactions or a milestone) and only need a second maintainer.</p>"
    )
    for step, title, limit in (
        ("merge", "Merge", 8),
        ("review", "Review (contributors, green)", 8),
        ("approve", "Approve the run", 8),
        ("ping", "Yours, waiting on a reviewer", 10),
    ):
        if not steps[step]:
            continue
        todo.append(f"<h4>{title}</h4><ol>")
        for p in steps[step][:limit]:
            action = ASTROID_NOTES.get(p["n"], (None, default_action[step]))[1] or default_action[step]
            todo.append(astroid_item(p, action))
        todo.append("</ol>")
        if step == "approve":
            numbers = " ".join(str(p["n"]) for p in steps[step][:limit])
            todo.append(
                "<pre>"
                + APPROVE_LOOP.format(numbers=numbers).replace("pylint-dev/pylint", "pylint-dev/astroid")
                + "</pre>"
            )
todo.append("</section>")

n_open = DATA["open_total"]
n_own = DATA["open_own"]
n_bot = sum(1 for r in rows.values() if r["a"].startswith("app/"))
counts = {
    lane: sum(1 for n in rows if lane_of(n) == lane) for lane in LANE_ORDER
}
n_silent = sum(1 for n, r in rows.items() if n in V and r["lastcom"][0] == "-")
n_conflict = sum(1 for n, r in rows.items() if n in V and r["merge"] == "CONFLICTING")
total = sum(counts.values())
held = counts["approve"] + counts["retrigger"]

page = (
    (HERE / "pr_queue_template.html")
    .read_text()
    .format(
        n_open=n_open,
        n_own=n_own,
        n_bot=n_bot,
        total=total,
        held=held,
        counts=counts,
        n_silent=n_silent,
        n_conflict=n_conflict,
        snapshot=DATA["snapshot"],
        snapshot_long=__import__("datetime").date.fromisoformat(DATA["snapshot"]).strftime("%-d %B %Y"),
        todo="".join(todo),
        body="".join(body),
    )
)
OUT.write_text(page)
print(f"wrote {OUT} — {total} PRs")
for lane in LANE_ORDER:
    print(f"  {lane:10s} {counts[lane]}")
