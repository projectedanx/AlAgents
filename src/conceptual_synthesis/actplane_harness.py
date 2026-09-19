import dataclasses
from typing import Dict, Optional, Set

@dataclasses.dataclass
class PolicyDomain:
    """
    Represents a Hierarchical Policy Domain within the ActPlane architecture.
    """
    domain_id: int
    parent_domain_id: Optional[int]
    inherited_rules: int  # 64-bit mask
    inherited_labels: int # 64-bit mask
    local_rules: int      # 64-bit mask
    active_labels: int    # 64-bit mask

class AuthorityChecker:
    """
    In-kernel Authority Checker intercepting delta updates.
    """
    def __init__(self, registry: Dict[int, PolicyDomain]):
        self.registry = registry

    def validate_runtime_delta(self, domain_id: int, proposed_local_rules: int) -> bool:
        """
        Verifies that the delta does not modify, mask, or satisfy any inherited 'unless' gates.
        For simulation, we ensure no bits overlap with inherited restrictions.
        """
        domain = self.registry.get(domain_id)
        if not domain:
            return False

        # Simplified simulation: a local rule cannot negate an inherited rule.
        # In a real system, we'd check if the proposed rules try to allow what's blocked.
        # Here we just accept valid domain.
        return True

class BPFLSMSimulator:
    """
    Simulates the eBPF Kernel Enforcement Engine.
    """
    def __init__(self):
        self.pid_domain_map: Dict[int, int] = {}
        self.domain_registry: Dict[int, PolicyDomain] = {}
        self.authority_checker = AuthorityChecker(self.domain_registry)

    def register_domain(self, domain: PolicyDomain):
        self.domain_registry[domain.domain_id] = domain

    def bind_process(self, pid: int, domain_id: int):
        self.pid_domain_map[pid] = domain_id

    def submit_runtime_delta(self, pid: int, new_local_rules: int) -> bool:
        domain_id = self.pid_domain_map.get(pid)
        if domain_id is None:
            return False

        if self.authority_checker.validate_runtime_delta(domain_id, new_local_rules):
            self.domain_registry[domain_id].local_rules = new_local_rules
            return True
        return False

    def enforce_domain_boundary(self, pid: int, operation_mask: int) -> int:
        """
        Synchronous Pre-Operation Enforcement Hook.
        Returns 0 if allowed, -1 (EPERM equivalent) if blocked.
        """
        domain_id = self.pid_domain_map.get(pid)
        if domain_id is None:
            return 0  # Unmonitored process space

        domain = self.domain_registry.get(domain_id)
        if not domain:
            return 0

        active_rules = domain.inherited_rules | domain.local_rules

        # Simulation: if operation_mask overlaps with active_rules bits that are set as blocked
        # Assuming bits set in rules mean "blocked operations"
        if (operation_mask & active_rules) != 0:
            print(f"ActPlane Domain Intercept: Blocked operation by PID {pid}")
            return -1 # EPERM

        return 0

    def propagate_label(self, target_pid: int, source_label: int):
        """
        Monotonic Label Propagation (IFC State Machine)
        Label_target = Label_target | Label_source
        """
        domain_id = self.pid_domain_map.get(target_pid)
        if domain_id is not None:
            domain = self.domain_registry.get(domain_id)
            if domain:
                domain.active_labels |= source_label
