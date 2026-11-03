#!/usr/bin/env bash
# Run from lab6 with the Python environment activated.
set -euo pipefail
case "${1:-}" in
    code)
        test_file=CodeCoverageTest_PES1UG24CS091_spam_scoring.py
        export COVERAGE_FILE=reports/.coverage.code
        options=()
        ;;
    branch)
        test_file=BranchCoverageTest_PES1UG24CS091_spam_scoring.py
        export COVERAGE_FILE=reports/.coverage.branch
        options=(--branch)
        ;;
    *) echo "Usage: bash reports/run_coverage.sh code|branch"; exit 2 ;;
esac
printf 'Lab 6 | AtharvMitt | PES1UG24CS091 | %s coverage\n' "$1"
PS4='$ '
set -x
date --iso-8601=seconds
pwd
git var GIT_AUTHOR_IDENT
python -m coverage run "${options[@]}" --source=spam_scoring -m pytest -q "$test_file"
python -m coverage report -m --fail-under=90
python -m coverage json -o "reports/${1}_coverage.json"
