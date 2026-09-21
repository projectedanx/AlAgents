import ast
import json
import difflib

class SEPAOEnvironmentScanner:
    """
    Scanner that parses Python code into an AST and computes Semantic Drift Deltas.
    """
    def parse_code(self, code: str) -> set:
        """Extracts function and class names as a basic structural representation."""
        try:
            tree = ast.parse(code)
            nodes = set()
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    nodes.add(f"Func:{node.name}")
                elif isinstance(node, ast.ClassDef):
                    nodes.add(f"Class:{node.name}")
            return nodes
        except SyntaxError:
            return set()

    def compute_delta(self, old_nodes: set, new_nodes: set) -> float:
        """Computes a simple Jaccard distance representing Semantic Drift Delta."""
        intersection = len(old_nodes.intersection(new_nodes))
        union = len(old_nodes.union(new_nodes))
        if union == 0:
            return 0.0
        jaccard_similarity = intersection / union
        return 1.0 - jaccard_similarity

class FIPIGenerator:
    """
    Failure-Informed Prompt Inversion generator.
    Translates failure traces into Symbolic Scars and mutates the constitution.
    """
    def generate_scar(self, error_trace: str, context: str) -> dict:
        return {
            "error_signature": error_trace.splitlines()[-1] if error_trace else "Unknown Error",
            "context": context,
            "constraint_type": "FORBID"
        }

    def apply_fipi(self, scar: dict, constitution: str) -> str:
        """Applies a Negative Constraint to the constitution based on the scar."""
        new_constraint = f"\n- **{scar['constraint_type']}**: Avoid pattern leading to `{scar['error_signature']}` in context `{scar['context']}`."
        return constitution + new_constraint

if __name__ == "__main__":
    scanner = SEPAOEnvironmentScanner()
    fipi = FIPIGenerator()

    # Simulate Code Change
    old_code = "def fetch_data(): pass\nclass DataModel: pass"
    new_code = "def fetch_data_v2(): pass\nclass AdvancedDataModel: pass"

    old_nodes = scanner.parse_code(old_code)
    new_nodes = scanner.parse_code(new_code)

    delta = scanner.compute_delta(old_nodes, new_nodes)
    print(f"Semantic Drift Delta: {delta:.2f}")

    if delta > 0.5:
        print("Ontological Conflict Detected. Triggering F-IPI.")
        trace = "AttributeError: 'DataModel' object has no attribute 'v2_field'"
        scar = fipi.generate_scar(trace, "Data Fetching Module")
        print("Generated Scar:", json.dumps(scar, indent=2))

        mock_constitution = "# System Constitution\n- Be factual."
        updated_constitution = fipi.apply_fipi(scar, mock_constitution)
        print("\nUpdated Constitution:\n", updated_constitution)
