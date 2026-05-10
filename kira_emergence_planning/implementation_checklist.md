# KIRA-7 Implementation Checklist

- [ ] Create `kira_agent.py` in `src/conceptual_synthesis/`.
- [ ] Implement `KiraAgent` inheriting from `BaseAgent`.
- [ ] Add `execute_petzold_loop()` that strictly enforces `THINK`, `WRITE`, `CODE`, `IMMUNE_REVIEW`.
- [ ] Implement `DCCDSchemaGuard` method for validating Feishu Card JSON v2.0.
- [ ] Implement `_scope_isolation_gate` to demand required info if missing.
- [ ] Implement `_generate_webhook_ingress` to produce signature-verified route code.
- [ ] Add explicit personality suspension logging in the `CODE` phase.
- [ ] Log Symbolic Scars (SCAR-001 to SCAR-007) in `scars.yaml`.
- [ ] Write `test_kira_agent.py` to ensure the logic and constraints hold.
- [ ] Update `README.md` with KIRA-7 Architecture summary.
