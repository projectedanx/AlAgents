# ADR-24: BFF and Gateway Automated Falsification

## Status
Accepted

## Context
Following the principles set forth in ADR-18 (Strategic Integration Project Manager Persona Metrology) and ADR-23 (Dynamic PCS and Zachman Framework Extrusion), the execution capability of the `StrategicIntegrationProjectManagerAgent` is expanding to include automated testing harnesses for API Gateways and Backends for Frontends (BFFs).

At a macro-architectural scale, both the Backend for Frontend (BFF) and the Standard API Gateway patterns partition system responsibilities differently. The system requires an automated AI testing harness to enforce structural rigor across network boundaries where contract drift, business logic bleed, and performance degradation can occur without explicit structural enforcement.

Three advanced research prompts have been identified for this harness:
1. **Automated Verification of Client Payload Minimization and Schema Drift**: Validating schema compliance and payload efficiency at the BFF boundary by intercepting OpenAPI contracts and generating mutation tests.
2. **Synthesizing Adaptive Rate-Limiting and Backpressure at the API Gateway Boundary**: Implementing an intelligent, adaptive rate-limiting engine based on real-time downstream system telemetry (e.g., database connection queue lengths).
3. **Continuous Detection of Business Logic Bleed and SRP Violations in BFF Architectures**: Identifying state-changing calculations within polyglot BFF repositories using AST parsers to prevent Single Responsibility Principle (SRP) violations.

## Decision
1. **Integration of Advanced Research Prompts into the MoE Context**: The StrategicIntegrationProjectManagerAgent will utilize its `execute_petzold_loop` to process vectors associated with these architectural challenges. The prompts serve as the input context to extrude operational workflows, specifically mapping the Gateway Sinkhole and Shared Persistence traps.
2. **Zachman Framework Enforcement**: The output specification for these testing harnesses must strictly conform to the `zachman_framework_schema.json` mapping.
    - **Entities**: 'BFF_Gateway', 'Standard_API_Gateway', 'Downstream_Services', 'OpenAPI_Contracts', 'Client_Payloads', 'Telemetry_Data'
    - **Capabilities**: 'Payload_Minimization_Verification', 'Adaptive_Rate_Limiting', 'Business_Logic_Bleed_Detection', 'Schema_Drift_Analysis', 'Circuit_Breaker_Isolation'
    - **Events**: 'Continuous_Falsification', 'Edge_Case_Stress_Testing', 'Schema_Evolution', 'Traffic_Spike_Handling'
3. **Continuous Falsification Pipeline**: These workflows are bound by the Epsilon-Tolerance Paraconsistency mechanism to manage technical debt across distributed boundaries, avoiding binary failure categorizations.

## Consequences
- **Positive**: Eradicates ambiguity in testing network boundaries by formalizing them into a Prompt Dimensioning & Tolerancing (PD&T) YAML block. Ensures the system explicitly models the structural patterns of BFFs and Standard Gateways.
- **Negative**: Increased complexity in synthesizing mock telemetry data and AST parsers for business logic detection within the simulation environment.
