🔒 [Security] Replace non-cryptographic hash() with SHA-256 for persistent integrity

🎯 **What:** The vulnerability fixed
The `EpistemicCartographerAgent._synthesize()` method previously used Python's built-in `hash()` function to generate the `smm_hash` field for the `DASL` object.

⚠️ **Risk:** The potential impact if left unfixed
Python's built-in `hash()` function incorporates a randomized salt per-process for strings and bytes to prevent hash collision denial-of-service (DOS) attacks. This means `hash(str(smm))` will yield different results for identical inputs across different runs or processes. Because this hash is used for persistent verification and integrity mapping in the Dynamic Affordance Sync Ledger (DASL), its non-deterministic nature across sessions undermines the reliability of state tracking and allows potential spoofing of validation trails, posing both a data-integrity and security risk.

🛡️ **Solution:** How the fix addresses the vulnerability
Replaced the built-in `hash()` function with a cryptographically secure and deterministic algorithm `hashlib.sha256()`. By using `hashlib.sha256(str(smm).encode('utf-8')).hexdigest()`, the resulting `smm_hash` is now strictly deterministic and provides strong cryptographic collision resistance, ensuring the generated DASL maintains persistent, verifiable integrity across all executions.
