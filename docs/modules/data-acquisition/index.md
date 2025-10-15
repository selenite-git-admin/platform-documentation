# Data Acquisition

The Data Acquisition family connects DataJetty to external enterprise systems and executes ingestion pipelines that extract, transform, and load data into the platform’s landing zones.  
It serves as the entry point for data movement, standardizing how external datasets are connected, transferred, and made available for processing.

This family abstracts the complexity of heterogeneous source systems—ERP, CRM, APIs, and files—into reusable connectors and controlled runtimes.  
Pipelines orchestrate these components to ensure that every dataset entering the platform is validated, logged, and compliant with the registered contracts and schemas maintained by Platform Control.

### Functional Coverage

- Connects to structured and unstructured data sources through configurable connectors.  
- Defines runners that govern batch and stream ingestion frequency, volume, and parallelism.  
- Manages execution contexts, environment isolation, and runtime orchestration for ingestion tasks.  
- Provides pipeline orchestration and transformation logic with lineage and contract registration.  
- Enables synthetic data generation for sandbox testing, validation, and demo environments.  
- Produces metadata and logs consumed by Data Store, Quality, and Control families for traceability.

### Modules

[Connectors](connectors/index.md)  
Defines integrations with source systems such as ERP, CRM, file, and API-based inputs, managing authentication and schema discovery.

[Runners](runners/index.md)  
Implements batch and stream runner configurations, handling scheduling, parallelism, and checkpoint control.

[Runtime](runtime/index.md)  
Manages execution environments, resource allocation, and lifecycle tracking for ingestion and transformation jobs.

[Pipelines](pipelines/index.md)  
Orchestrates extraction, transformation, and loading workflows that register schemas and lineage before persisting data.

[Synthetic Data](synthetic-data/index.md)  
Generates representative datasets for testing and validation, supporting pipeline and model verification without production data.
