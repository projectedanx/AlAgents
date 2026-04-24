🧹 [Narrow exception handling for file IO operations]

🎯 What: Replaced broad `except Exception:` blocks with `except OSError:` in the `_log_symbolic_scar` methods across `epistemic_cartographer.py`, `lexis_sovereign_agent.py`, `axiom_agent.py`, and `vulcan_agent.py`. Additionally, updated `lexis_sovereign_agent.py` to use `logging.error` instead of `print`.

💡 Why: Catching the base `Exception` class is considered a bad practice as it can silently swallow critical errors like `MemoryError` or `ValueError`. Since these `try` blocks specifically wrap file write operations, catching `OSError` accurately targets the potential failures (e.g., permissions, disk space) without masking unrelated bugs.

✅ Verification: Validated the changes by inspecting the git diff and running the unit test suite (`python -m unittest discover tests`). All tests pass.

✨ Result: More resilient error handling, preventing unintended bugs from being silently ignored, and ensuring consistent error reporting via the standard `logging` module.
