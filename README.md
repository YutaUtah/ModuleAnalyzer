# ![](../images/ga.png) Capstone Project, Part 3 - Extending & Testing

You've reached the final part of the project! Here, you'll extend the program in a significant way and test the added features.

## Part 3 Requirements

0. Include a README.md that:
    - Briefly describes the program
    - Explains the additional features added
    - Shows how to run the program
    - Shows how to test the program

1. Extend `pystats` to process directories/packages.
    - Instead of only processing one file, extend `pystats` to analyze Python packages (and their associated Python files).
        - Extend `Report` to list each package.
        - Extend `Statistic` to allow for package statistics. 
            - Include at least one package statistic.
        - Extend `PyStatsApp` (or make a new class) to discover files in each package, then analyze each using the existing methods.
    - There is no particular expected output, but we expect the final report to contain additional information about the package and files!

2. Create `pytest` test files that test any new functionalities added:
    - Test additions to `Statistic` using mocking.
    - Test `PyStatsApp` (or your new class) to ensure it properly discovers packages.
    - Write an end-to-end test that ensures it all works on an actual Python package.
        - Verify that the resulting report is as expected.
        - Please include the tested package inside your codebase.
    - Ensure that you test common cases and edge cases.

3. (BONUS) Verify that your script works on arbitrary Python packages from GitHub. This likely requires the existing functions to be more robust. For example, it will have to handle comments, multi-line strings, and signatures that extend across multiple lines.
    - Include an example package from GitHub in your repo along with the report showing it works.

4. (BONUS) Add additional enhancements and describe them in your README. For example:

Packaging:

    - Create a distributable using `setuptools` (as discussed in class).

Additional Stats/Warnings:

    - How many blank lines are there per class?
    - What is the largest indentation level in each class? function?
    - Warn if the module does not end with a newline.
    - Warn if there are too many blank lines between classes.

Parsing Enhancements:

    - Remove comments before parsing.
    - Trim any empty lines trailing a block.
    - Add an option to recursively look at all files in all subdirectories.
    - Add an option to examine only test files (e.g. `test_*.py` or `*_test.py`).
    - Add an option to remove private methods.

Additional Reports:

    - Add a new option to generate an HTML report, an email report, etc. (Note that a report can just be a small subset of the current one!)

## Project Alternatives

If you have an idea of similar complexity that involves testing, let us know! For example, you could use this program as inspiration and make reports about Markdown files in a project.
