# Static analysis issue table

Line numbers refer to the original `movie_reviews.py` in the baseline commit.
Reports are preserved in `reports/before/`. The baseline Pylint score is
**5.47/10**; Bandit reports four findings and Flake8 reports four findings.

| Issue | Type | Line(s) | Description | Fix Approach |
|-------|------|---------|-------------|--------------|
| Bandit B324: MD5 | Security / High | 46 | Review identifiers use MD5, which Bandit flags as a weak cryptographic hash. | Bandit stage: use SHA-256 while preserving the ten-character display ID. The short ID is a label, not a credential or guaranteed unique identifier. |
| Bandit B104: all interfaces | Security / Medium | 4 | The advertised stream address uses `0.0.0.0`, which would expose all interfaces if used as a bind address. This demo only prints the address; it does not start a server. | Bandit stage: default to loopback (`127.0.0.1`). |
| Bandit B105: hardcoded password | Security / Low | 6 | An unused moderator password is stored in source code. | Bandit stage: remove the unused credential; the demo has no authentication feature. |
| Bandit B311: ordinary randomness | Security / Low | 41 | Bandit flags `random.choice` as unsuitable for security-sensitive randomness. Featured movie selection itself is not security-sensitive. | Bandit stage: use `secrets.choice` to clear the finding while preserving random selection. |
| Pylint W0603: global statement | Maintainability / Warning | 8, 40–42 | Featured selection writes redundant module-level state. | Pylint stage: return the chosen title directly and remove the unused `featured` variable. |
| Pylint C0114, C0116: missing documentation | Documentation / Convention | 1, 11, 16, 26, 34, 39, 45, 48, 54, 58 | The module and its functions have no docstrings. | Pylint stage: document the module and every function. |
| Pylint C0103: naming | Style / Convention | 8, 11, 16, 26, 34, 39, 45, 48, 54 | Functions and review parameters use camelCase; `featured` also violates module naming conventions. | Pylint stage: use snake_case names, update all callers, and remove redundant featured state. |
| Pylint R1705: unnecessary else | Maintainability / Refactor | 28–31 | The average calculation uses an `else` after a branch that already returns. | Pylint stage: return `0.0` after the conditional. |
| Pylint C0200: indexed iteration | Maintainability / Convention | 49–51 | Review printing builds a list and indexes it using `range(len(...))`. | Pylint stage: iterate over titles with `enumerate(movies, start=1)`. |
| Flake8 E225: operator spacing | Formatting | 35 | Assignment lacks spaces around `=`. | Flake8 stage: add the required spaces. |
| Flake8 E302: blank lines | Formatting | 48 | Only one blank line separates top-level functions. | Flake8 stage: separate functions with two blank lines. |
| Flake8 E261: inline comment spacing | Formatting | 70 | Only one space precedes the inline comment. | Flake8 stage: use two spaces before the comment. |
| Flake8 E231: comma spacing | Formatting | 72 | A comma in the genres print statement lacks a following space. | Flake8 stage: add a space after the comma. |

## Stage completion

- Baseline: ran the demo and all three tools, saved original reports, and
  documented all findings in severity order.
- Bandit fixes: completed all four findings without suppressions. Bandit exits
  successfully with no issues. The SHA-256 display ID changes from `52e343ca87` to
  `b8fc2faf6d`, and the printed host changes to `127.0.0.1`. Rating averages,
  ordering, review storage, and genre output retain their original behavior.
- Pylint fixes: completed all findings without suppressions, reaching
  **10.00/10**. Functions and review parameters use snake_case, all functions
  have docstrings, featured selection returns its result without a global
  assignment, average calculation no longer has a redundant `else`, and review
  printing uses `enumerate`. Reran the demo and all three tools; current reports
  are in `reports/after/`.
- Flake8 fixes: corrected all four formatting findings. Reran the demo and all
  three analysis tools: Pylint **10.00/10**, Bandit **no issues**, and Flake8
  **no findings**, all exiting successfully. Final reports and demo output are
  in `reports/after/`; original reports remain in `reports/before/`.
