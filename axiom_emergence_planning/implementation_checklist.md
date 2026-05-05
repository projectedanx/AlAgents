# Implementation Checklist: Axiom Agent

## 1. Core Agent Mechanics (`axiom_agent.py`)
- [ ] Verify `DCCD` (Draft-Conditioned Constrained Decoding) pipeline is correctly implemented in `execute_petzold_loop`.
- [ ] Confirm `EpistemicEscrow` correctly halts execution when CFDI > 0.15.
- [ ] Confirm `SagaRecovery` correctly flushes context when SSI > 0.04.
- [ ] Ensure `SymbolicScar` logs are correctly generated and formatted in `SymbolicScar.jsonl`.
- [ ] Ensure `AutonymicIsolate` successfully flags/masks forbidden lexicon items.

## 2. Testing & Verification
- [ ] Implement `test_axiom_agent.py` to cover CFDI thresholds, SSI triggers, schema validation, and forbidden word usage.
- [ ] Ensure tests use `sys.modules` mocking for NLTK to prevent timeout/dependency issues in isolated environments.

## 3. Documentation Updates
- [ ] Update `README.md` to reference the Axiom agent's role and the new `axiom_emergence_planning` directory.
- [ ] Update `DOMAIN_GLOSSARY.md` if any new terms from Axiom's frontmatter need explicit definitions.
