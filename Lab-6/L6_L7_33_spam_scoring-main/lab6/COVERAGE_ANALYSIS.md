# Lab 6: Code and Branch Coverage Analysis

Student: Atharv Mittal (PES1UG24CS091)

Git identity: AtharvMitt <atharvmitt@gmail.com>

Application: `spam_scoring.py` (supplied source, unchanged)

## Initial measurements

The two supplied tests pass. Measuring only the application gives 16/39
statements (41%) and 9/26 branch destinations (34.62%). Coverage's combined
statement-and-branch percentage is 38%: (16 + 9) / (39 + 26).
The initial reports are saved as text in `reports/initial_*`; no screenshots
of results below 90% are submitted.

## Stage 1: code coverage

`CodeCoverageTest_PES1UG24CS091_spam_scoring.py` contains 12 passing cases.
They exercise spam keywords, uppercase words, each link scoring block, the
known sender clamp, all classifications, inbox counting, and all statuses.
All 39 statements execute: **100% line coverage**.

Evidence: `reports/code_coverage.png`, `reports/code_terminal.txt`, and
`reports/code_coverage.json`. The PNG is an unedited capture of the laptop's
eDP-1 display using `grim`, showing the actual terminal test run and report.

Line coverage alone does not prove both outcomes of a decision were taken.
A diagnostic branch run of this suite leaves `17 -> 19` untested: a known
sender whose score after subtracting three is nonnegative, so the clamp is
skipped. All lines still execute because another test takes the clamp.
The suite covers 25/26 branch destinations (96.15%), with 98% combined
coverage. Stage 2 explicitly addresses that missing outcome and adds
threshold and empty-input checks.

## Stage 2: branch coverage

`BranchCoverageTest_PES1UG24CS091_spam_scoring.py` is an independent suite of
50 passing cases. It retains the Stage 1 scenarios and adds the following:

| Decision or behavior | Cases exercised |
| --- | --- |
| Word loop | Empty text, whitespace only, one word, multiple words |
| Spam word match | Each keyword, mixed case, punctuation, repetitions |
| Uppercase fallback | Ordinary/mixed-case text, uppercase lengths 3 and 4, digits |
| Link thresholds | 0, 1, 3 and 4 links |
| Known sender | Both sender flags; adjusted score negative, zero and positive |
| Classification | 0, 1, 3, 4, 5, 7, 8 and 9 |
| Inbox loop | Empty inbox, single items, mixed labels, repeated messages |
| Status total | Zero and nonzero totals |
| Spam ratio | Below, at and above 0.2 and 0.5, plus zero and one |

The known-sender tests with pre-deduction scores of three and four exercise
the previously missed `17 -> 19` branch. Exact ratio tests verify the strict
`>` comparisons: 20% spam is healthy and 50% spam is noisy.
Integration also verifies filtering followed by status calculation, and
inbox tests check counts and that the input collections are unchanged.

The final result is **39/39 statements (100%) and 26/26 branch destinations
(100%)**, with zero missing statements, zero partial branches, and 100%
combined coverage. Evidence: `reports/branch_coverage.png`,
`reports/branch_terminal.txt`, and `reports/branch_coverage.json`.
The branch screenshot is also an unedited `grim` capture of the laptop's
eDP-1 display, after running the branch suite in a real Kitty terminal.

## Interpretation

Line coverage counts executable statements reached. Branch coverage counts
the alternate control-flow destinations taken; the line suite's missing
clamp-skip outcome demonstrates the difference. Coverage.py's `Cover`
column with `--branch` combines statement and branch counts; the separate
branch percentages above use covered branches divided by all branches.
All four application functions are invoked. Path coverage concerns entire
execution sequences; 100% branch coverage does not establish all possible
paths through loops or all combinations of conditions, nor prove the
application is free of defects. The assertions check expected behavior
in addition to exercising code.

## Reproduction

From this `lab6` directory:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
bash reports/run_coverage.sh code
bash reports/run_coverage.sh branch
python -m pytest -q
```

The script restricts measurement to `spam_scoring`, so coverage percentages
do not include test code. The original tests are preserved in
`reports/starter_tests.py`. The default `test_spam_scoring.py` entry point
collects the current stage's tests; explicitly named deliverable files can
also be passed to pytest. Local caches and coverage databases are ignored.

The first commit (`ec88202`) contains the line suite and its screenshot.
The following branch coverage commit adds the branch suite, its screenshot,
and this completed analysis. Both use AtharvMitt <atharvmitt@gmail.com>.
