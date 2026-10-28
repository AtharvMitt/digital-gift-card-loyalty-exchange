# Lab 5: Static Code Analysis — Movie Review & Rating System

**Your file:** `movie_reviews.py`

Follow the lab handout for the full instructions.

## About the program

A movie rating board. It adds movies, accepts 1-5 star ratings with optional reviews, works out average ratings, ranks the top movies, picks a featured movie and generates review ids.

The supplied code had quality, style and security problems identified by Pylint, Flake8 and Bandit. The documented findings have been fixed in three separate tool-specific commits.

## What to do

1. **Run it first** and read the output carefully:

   ```
   python movie_reviews.py
   ```

   It runs a short demonstration and needs no input. Note what it prints, so you can check that it still behaves the same after your fixes.

2. **Install the tools:**

   ```
   python -m venv .venv
   source .venv/bin/activate
   python -m pip install pylint bandit flake8
   ```

3. **Run the analysis and save the reports:**

   ```
   mkdir -p reports/after
   python -m pylint --persistent=n movie_reviews.py > reports/after/pylint_report.txt 2>&1
   python -m bandit -r movie_reviews.py > reports/after/bandit_report.txt 2>&1
   python -m flake8 movie_reviews.py > reports/after/flake8_report.txt 2>&1
   ```

   Original reports and demo output are preserved in `reports/before/`; final reports and demo output are in `reports/after/`. An empty Flake8 report means no findings.

4. **Document the issues** in `issues.md` using this table (at least 4 rows, high and medium severity first):

   | Issue | Type | Line(s) | Description | Fix Approach |
   |-------|------|---------|-------------|--------------|
   | ...   | ...  | ...     | ...         | ...          |

5. **Fix the code.** Fix at least 4 of the issues you documented, then rerun all three tools to confirm they are gone. Repeat until you are satisfied. The program should still do its job when you are done.

## Deliverables

- `movie_reviews.py`: your cleaned version, with at least 4 issues fixed.
- `issues.md`: the completed issue table.
- `reports/before/` and `reports/after/`: the three analysis reports and demo output before and after the fixes.

**Final results:** Pylint **10.00/10**, Bandit **no findings**, and Flake8 **no findings**. Verified with Python 3.14.8, Pylint 4.1.3, Bandit 1.9.4, and Flake8 7.4.1.

The demo preserves its ratings and rankings. The SHA-256 review ID is now `b8fc2faf6d`, the stream address is `127.0.0.1:8000`, and the featured movie varies between runs. `reflection.md` is omitted as requested.

Be ready to explain the bugs you found and how you fixed them. You may be called on to present.
