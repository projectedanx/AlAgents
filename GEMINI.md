# ~/.gemini/GEMINI.md (Global Scope - Personas & Cross-Project Defaults)
# Development Guidelines:
- You must always adhere to a strict Test-Driven Development (TDD) cycle.
- If asked to fix a bug, you are strictly forbidden from modifying production code until you have written a failing reproduction script.

# ./my-project/GEMINI.md (Project Scope - Architecture & Testing Frameworks)
# Testing Standards:
- Tech Stack: Python unittest framework.
- Directory: All unit test cases must reside in the `tests/` directory.
- Workflows: Always run `PYTHONPATH=. python -m unittest discover tests` upon completion of a task.
- Error Handling: If any test fails, analyze the assertion logs, correct the target file, and rerun the test suite.
