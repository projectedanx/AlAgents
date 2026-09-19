# ADR 27: ActPlane Hierarchical Policy Domains and the Sovereignty-Enforcement Split

## Status
Accepted

## Context
As the complexity of multi-agent cognitive systems increases, the traditional model-centric development paradigm is no longer sufficient. LLMs, as probabilistic next-token generators, lack the intrinsic capability to securely execute sequential operations or maintain durable state. Currently, our system relies on prompt engineering and userspace tool-call gateways to enforce safety and architectural constraints. These methods are susceptible to "Gate-Bypassing" (prompt injection overriding rules) and "Laid-back" declassification attempts. We need a fundamental division of control—a "Sovereignty-Enforcement Split"—where rules defined by the parent orchestrator cannot be weakened, bypassed, or disabled by any downstream sub-agent or generated script.

## Decision
We will implement **ActPlane Hierarchical Policy Domains**, establishing a strict boundary between the probabilistic intelligence of the agent and the deterministic enforcement of the runtime harness.

The implementation consists of four pillars:
1. **Automated Discovery and Constraint Mining:**
   - Static invariants (e.g., "never push directly to main") are established at the parent domain.
   - Child domains monotonically inherit all parent rules, which are marked as read-only and immutable.
2. **Isomorphic Formalization (Kernel-Space Domains):**
   - Policy domains will be formalized as in-kernel eBPF maps mapping PIDs to their domain.
   - Constraints will be represented as bitmasks (`inherited_rules`, `local_rules`).
   - We will enforce monotonic Information-Flow Control (IFC) label propagation along OS data-flow edges.
3. **Parametric Trade-off Modeling:**
   - Using BPF-LSM and tracepoint hooks adds only microsecond-level overhead (~1.9%), avoiding the high latency of hardware virtualization (e.g., Firecracker) while remaining completely out of userspace bypass scope.
   - Spawning fresh subprocesses within child domains bounds "taint accumulation" (label creep), pruning inherited file-read labels for transient worker processes.
4. **Continuous Falsification and Edge-Case Testing:**
   - An in-kernel **Authority Checker** will intercept runtime delta submissions, rejecting any attempt by a child process to mask or satisfy inherited gates.
   - Declassification of safety labels is bound strictly to the domain that authored them; children lack cryptographic privilege to clear parent-imposed labels.

## Consequences

### Positive
* **Zero-Trust Resilience:** Downstream agents cannot bypass safety rules through prompt injection or shell escapes.
* **Low Overhead:** eBPF-LSM provides near-native performance compared to heavy containerization.
* **Deterministic Verification:** Converts probabilistic safety into deterministic, OS-level constraints.

### Negative
* **Increased Harness Complexity:** Requires maintaining BPF programs and simulating them for testing.
* **Label Creep Management:** We must rigorously prune long-running subprocesses to prevent them from becoming over-tainted and blocking legitimate operations.
