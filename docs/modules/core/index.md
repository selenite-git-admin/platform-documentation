# Core

The Core family forms the foundation of the DataJetty platform. It provides the essential building blocks that make all higher-level services secure, consistent, and interoperable. Core modules establish the baseline for authentication, authorization, encryption, identity, and error management without depending on business or transactional data.

These services operate independently of domain logic and can be used by any other family through lightweight APIs or shared libraries. Together, they ensure that every request, secret, and identifier within the platform adheres to a single, verifiable standard.

### Functional Coverage

- Defines uniform authentication and authorization mechanisms for users and services.  
- Provides cryptographic services including encryption, signing, and key lifecycle management.  
- Manages secure secret storage and retrieval for runtime and build-time contexts.  
- Generates deterministic and collision-resistant identifiers for data entities.  
- Establishes consistent network policy and validation models used across modules.  
- Standardizes error handling and diagnostic responses for service interoperability.  
- Acts as a shared dependency layer for all other families, ensuring security and reliability from the ground up.

### Modules

[Authentication](authentication/index.md)  
Manages user and service authentication, token issuance, and identity federation with external providers.

[Authorization](authorization/index.md)  
Evaluates and enforces access control policies, integrating with tenant and role metadata from Platform Subscription.

[Encryption](encryption/index.md)  
Implements encryption, decryption, and signing utilities with integrated key lifecycle handling.

[Secrets](secrets/index.md)  
Stores and retrieves configuration secrets, credentials, and tokens securely through managed key references.

[Network Security](network-security/index.md)  
Defines network policy schemas and validation for allowed CIDR ranges, port profiles, and trust levels.

[UUID](uuid/index.md)  
Generates globally unique identifiers and maintains consistency across distributed data sources.

[Error Handling](error-handling/index.md)  
Provides a unified error model, code taxonomy, and structured diagnostic output for all platform modules.
