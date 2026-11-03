# Lab 6: Code and Branch Coverage Analysis

Student: Atharv Mitt (PES1UG24CS091)  
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
coverage. Stage 2 will explicitly address that missing outcome and add
threshold and empty-input checks.

## Reproduction

From this `lab6` directory:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
bash reports/run_coverage.sh code
```

The script restricts measurement to `spam_scoring`, so coverage percentages
do not include test code. The original tests are preserved in
`reports/starter_tests.py`. The default `test_spam_scoring.py` entry point
collects the current stage's tests; explicitly named deliverable files can
also be passed to pytest. Local caches and coverage databases are ignored.
