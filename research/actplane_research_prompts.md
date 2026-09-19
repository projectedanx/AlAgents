# ActPlane Hierarchical Policy Research Report

## 1. Verifiable Zero-Trust Cross-Harness State Synchronization via SEMA-Merkle Trees

### Objective
Design a decentralized multi-agent system state synchronization mechanism over low-trust channels.

### SEMA-Merkle Tree Architecture
The agent state tuple $S(t) = (M_{\mathrm{epi}}, M_{\mathrm{sem}}, M_{\mathrm{work}}, \mathcal{K}, \mathrm{Ctxt}, \Psi)$ is encoded into a directed SEMA-Merkle Tree.
- Leaves are cryptographically hashed SEMA Pattern Cards (e.g., `BeliefTracking#c78f`, `Task#b290`).
- Branching represents contextual boundaries and hierarchical relationships.

### State-Transition Proofs ($P_{\Delta}$)
When $M_{\mathrm{work}}$ modifies to $M_{\mathrm{work}}'$:
- The agent generates a cryptographic proof (e.g., using zk-SNARKs or lightweight polynomial commitments) showing the transformation strictly adheres to parent constraint $\Phi \in \mathcal{K}$.
- Raw content is not disclosed; only the root hash change and the proof of compliance are broadcast.

### Decompression Reconstruction Protocol
Receiving harnesses:
1. Ingest the Merkle state diff.
2. Verify transition integrity by re-evaluating the leaf hashes against the root.
3. Use "lazy loading" (isomorphic to virtual memory page faults) to page in required context branches for immediate task execution.
- Conflict resolution uses decentralized consensus prioritizing constraints inherited from the highest sovereign domain.

---

## 2. ActPlane eBPF IFC DSL Synthesis for Dynamic Collaboration

### Objective
Dynamically compile natural-language instructions into OS kernel-enforced Information-Flow Control (IFC) policies.

### Context-Free Grammar (CFG) for IFC DSL
```ebnf
<rule> ::= <action> <target> [ "unless" <condition> ]
<action> ::= "block" | "allow"
<target> ::= <process_label> <operation> <resource_label>
<operation> ::= "write" | "exec" | "open" | "socket"
```

### Compilation Pipeline
- LLM acts as a Constrained Semantic Parser.
- Maps "Sub-agent C... can write to file F only if F has been validated" into DSL: `block C write F unless validated(F)`.
- Outputs JSON schemas for BPF loader.

### eBPF Kernel Enforcement Engine
- Intercepts `execve`, `openat`, and `socket` via BPF LSM hooks.
- Implements `Label_target = Label_target | Label_source`.
- Blocks operations where active labels match bitmasks restricted by inherited rules.

### Semantic Feedback Loop
- On block, uses `SECCOMP_RET_USER_NOTIF`.
- BPF relays the specific bitmask failure to userspace.
- The harness translates this back into a prompt-friendly warning (e.g., "Blocked: Missing validation label").

---

## 3. AgentSpawn Metacognitive Auto-Tuning

### Objective
Optimize agent spawning, memory compaction, and tool routing via RL from execution logs.

### Markov Decision Process (MDP) for Spawning
- State space $\Psi = \{I_f, C_c, F_c, O_c, U_c\}$ (context size, cyclomatic complexity, test failure density, file edit volume, uncertainty).
- Actions: Adjust memory slicing parameters, select specific sub-agent classes.

### Delta-Slicing Optimizer
- Parameterizes relevance function $r(m, T_{\text{child}})$.
- Goal: Maximize Critical Atom Recall (CAR) while minimizing token overload for the spawned child.

### Retrospective Harness Optimization (RHO)
- Offline learning on long trajectories.
- "Digester" isolated failure modes (semantic mutation, weakening) to create pairwise preference data (successful paths vs. failure paths).

### Reinforcement Learning Loop
- Uses DPO (Direct Preference Optimization).
- Reward function penalizes token spend, execution latency, and rule blocks (EPERM events from ActPlane).
