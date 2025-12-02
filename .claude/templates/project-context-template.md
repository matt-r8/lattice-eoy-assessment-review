# Project Context Template

This file should be created as `PROJECT_CONTEXT.md` in the root of each repository to provide agents with essential project information.

## Project Overview

### Basic Information
- **Project Name**: [Project name]
- **Description**: [Brief project description]
- **Repository**: [Repository URL]
- **Primary Language(s)**: [Main programming languages]
- **Framework(s)**: [Key frameworks and libraries]
- **Last Updated**: [Date of last context update]

### Architecture
- **Type**: [Web app, API, microservices, CLI tool, etc.]
- **Architecture Pattern**: [MVC, microservices, serverless, etc.]
- **Database**: [Database type and version]
- **Infrastructure**: [Cloud provider, deployment method]
- **Key Services**: [List of main services/components]

## Development Environment

### Prerequisites
- **Node/Python/etc Version**: [Required versions]
- **Package Manager**: [npm, yarn, pip, etc.]
- **Required Tools**: [Docker, specific CLIs, etc.]
- **Environment Variables**: [Key env vars needed]

### Setup Commands
```bash
# Installation
[Installation commands]

# Development server
[Dev server start command]

# Build process
[Build commands]

# Test execution
[Test commands]
```

## Project Conventions

### Code Standards
- **Linting**: [ESLint, Prettier, etc. with config location]
- **Testing**: [Jest, PyTest, etc. with patterns]
- **Documentation**: [JSDoc, docstrings, etc.]
- **Git Flow**: [Branch naming, commit patterns]

### File Structure
```
project-root/
├── [Key directories and their purposes]
├── [Important config files]
└── [Documentation locations]
```

### Naming Conventions
- **Files**: [kebab-case, camelCase, etc.]
- **Functions**: [Naming patterns]
- **Variables**: [Naming patterns]
- **Components**: [Naming patterns]

## Business Context

### Domain
- **Industry**: [Healthcare, fintech, e-commerce, etc.]
- **Target Users**: [Who uses this system]
- **Core Business Logic**: [Key business rules]
- **Compliance Requirements**: [GDPR, HIPAA, SOX, etc.]

### Key Features
- [Feature 1]: [Brief description]
- [Feature 2]: [Brief description]
- [Feature 3]: [Brief description]

### Critical Paths
- [Critical user journey 1]
- [Critical user journey 2]
- [Performance-sensitive areas]

## Technical Constraints

### Performance Requirements
- **Response Time**: [Target response times]
- **Throughput**: [Expected load]
- **Availability**: [Uptime requirements]
- **Scalability**: [Growth expectations]

### Security Requirements
- **Authentication**: [Method used]
- **Authorization**: [RBAC, ABAC, etc.]
- **Data Protection**: [Encryption, PII handling]
- **Audit Requirements**: [Logging, compliance]

### Integration Points
- **External APIs**: [List of external services]
- **Internal Services**: [Other internal systems]
- **Webhooks**: [Incoming/outgoing webhooks]
- **Message Queues**: [Event systems]

## Operational Context

### Deployment
- **Environments**: [dev, staging, prod specifics]
- **CI/CD Pipeline**: [Build/deploy process]
- **Infrastructure**: [Servers, containers, cloud resources]
- **Monitoring**: [APM, logging, alerting tools]

### Team Structure
- **Team Size**: [Number of developers]
- **Roles**: [Frontend, backend, DevOps, etc.]
- **Communication**: [Slack channels, meeting patterns]
- **Decision Making**: [Who approves changes]

### Known Issues
- **Technical Debt**: [Key areas needing refactoring]
- **Performance Bottlenecks**: [Known slow areas]
- **Browser/Platform Limitations**: [Compatibility issues]
- **External Dependencies**: [Risky third-party services]

## Agent-Specific Guidance

### Common Tasks
- [Frequent development tasks and their patterns]
- [Typical debugging approaches]
- [Standard deployment procedures]

### Gotchas and Pitfalls
- [Common mistakes to avoid]
- [Areas requiring special attention]
- [Historical problems and solutions]

### Success Patterns
- [Proven approaches that work well]
- [Preferred libraries/tools for specific tasks]
- [Effective debugging strategies]

## Auto-Discovery Hints

### Framework Detection
- **Package Files**: [package.json, requirements.txt, etc.]
- **Config Files**: [Key configuration files to check]
- **Directory Patterns**: [Typical project structure indicators]

### Tool Integration
- **Linting Config**: [.eslintrc, .pylintrc locations]
- **Test Config**: [jest.config.js, pytest.ini locations]
- **Build Config**: [webpack.config.js, Dockerfile locations]
- **CI/CD Config**: [.github/workflows, .gitlab-ci.yml locations]

---

## Usage Instructions

1. **Initial Setup**: Copy this template to `PROJECT_CONTEXT.md` in your repository root
2. **Customize**: Fill in all sections relevant to your project
3. **Maintain**: Update as the project evolves
4. **Agent Integration**: Agents will automatically read this file for context
5. **Validation**: Use the provided validation scripts to ensure completeness