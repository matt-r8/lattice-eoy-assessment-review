# Project Context

## Project Overview

### Basic Information
- **Project Name**: Lattice EOY Assessment Review System
- **Description**: Automated system to gather end-of-year peer assessment reviews from Lattice platform, organize feedback for Practice Leads to review, and use Claude Code agents to summarize and synthesize A Player rankings and peer ratings for EOY scorecards
- **Repository**: Local repository at /workspaces/lattice-eoy-assessment-review
- **Primary Language(s)**: Python
- **Framework(s)**: LatticeAPI client library (custom), python-dotenv, requests, pytest, python-docx
- **Last Updated**: 2025-12-01

### Architecture
- **Type**: CLI automation tool / Data extraction and processing system
- **Architecture Pattern**: Modular Python library with API client components
- **Database**: None (file-based output: markdown documents)
- **Infrastructure**: Local execution via devcontainer, outputs to Google Drive for distribution
- **Key Services**:
  - LatticeAPI client (authentication, reviews, updates, users, managers modules)
  - Data extraction from Lattice API
  - Markdown document generation (one per employee)
  - Claude Code agent integration for synthesis

## Development Environment

### Prerequisites
- **Python Version**: Python 3.x (specified in devcontainer)
- **Package Manager**: pip
- **Required Tools**: Docker (for devcontainer), Google Drive access (for output distribution)
- **Environment Variables**:
  - Lattice API credentials (stored in .env file)
  - API keys for authentication

### Setup Commands
```bash
# Installation
pip install -r requirements.txt

# Environment setup
# Create .env file with Lattice API credentials

# Test execution
pytest

# Run data extraction
python [main script to be determined]
```

## Project Conventions

### Code Standards
- **Linting**: To be determined
- **Testing**: pytest for unit tests
- **Documentation**: Python docstrings
- **Git Flow**: Standard branch naming conventions

### File Structure
```
lattice-eoy-assessment-review/
├── knowledge-base/          # Rise8 knowledge-base material for agent creation
├── LatticeAPI/              # API client modules
│   ├── authentication.py
│   ├── reviews.py
│   ├── updates.py
│   ├── users.py
│   └── managers.py
├── .env                     # API credentials (not committed)
├── .devcontainer/           # Development container configuration
├── requirements.txt         # Python dependencies
└── [output directory]/      # Generated markdown files
```

### Naming Conventions
- **Files**: snake_case for Python modules
- **Functions**: snake_case
- **Variables**: snake_case
- **Classes**: PascalCase

## Business Context

### Domain
- **Industry**: Human Resources / Performance Management
- **Target Users**:
  - Primary: Practice Leads (Software, Platform/Cyber, Design, Product Management)
  - Secondary: HR/People Ops team for company-wide assessment processing
  - Future: Leadership, Finance, Growth, Customer Success, IT, Marketing departments
- **Core Business Logic**:
  - Extract peer assessment reviews from Lattice platform
  - Organize feedback by employee and Practice
  - Generate markdown summaries for Practice Lead review
  - Synthesize A Player rankings and peer ratings using Claude agents
  - Support EOY scorecard completion process
- **Compliance Requirements**:
  - Employee data privacy
  - Cross-department access controls (Practice Leads only see their Practice's reviews)
  - Secure handling of performance review data

### Key Features
- **Lattice API Integration**: Automated extraction of end-of-year peer assessment reviews
- **Markdown Generation**: One document per employee with organized feedback
- **Claude Agent Synthesis**: AI-powered summarization and synthesis of peer ratings and A Player rankings
- **Practice-Based Organization**: Filtering and grouping by 4 core Practices (Software, Platform/Cyber, Design, Product Management)
- **Google Drive Distribution**: Secure file sharing with role-based access control

### Critical Paths
- **Data Extraction**: Successfully authenticate and retrieve all review data from Lattice API
- **Document Generation**: Create accurate, complete markdown files for each employee
- **Access Control**: Ensure Practice Leads only access reviews for their Practice
- **Agent Processing**: Claude Code agents accurately synthesize rankings and ratings

## Technical Constraints

### Performance Requirements
- **Execution Frequency**: One-time annually (end-of-year process)
- **Processing Scale**: 15-42 employees per Practice across 4 Practices (60-168 total employees initially)
- **Response Time**: Not time-critical; batch processing acceptable
- **Availability**: Local execution, no uptime requirements

### Security Requirements
- **Authentication**: Lattice API key authentication (stored in .env)
- **Authorization**: Cross-department access controlled via Google Drive permissions
- **Data Protection**:
  - API credentials in .env (gitignored)
  - Employee performance data handled locally
  - Google Drive folder permissions limit Practice Lead access to their Practice only
- **Audit Requirements**: Review data handling follows company HR policies

### Integration Points
- **External APIs**:
  - Lattice API (primary)
    - Authentication endpoint
    - Reviews endpoint (primary)
    - Updates endpoint
    - Users endpoint
    - Managers endpoint
  - Google Drive (for output distribution)
- **Internal Services**: None
- **Claude Integration**: Claude Code agents via agent chat interface (not Claude API)

## Operational Context

### Deployment
- **Environments**: Local development only
- **CI/CD Pipeline**: None (one-time annual script execution)
- **Infrastructure**:
  - Local execution via Python/devcontainer
  - Output files stored locally then uploaded to Google Drive
- **Monitoring**: Manual verification of generated markdown files

### Team Structure
- **Team Size**: Single user/developer initially
- **Roles**:
  - Developer: Runs extraction scripts
  - Practice Leads: Review generated documents (Software, Platform/Cyber, Design, Product Management)
  - HR/People Ops: Oversee process
- **Communication**: Direct user interaction with Claude Code agents
- **Decision Making**:
  - Practice Leads: Review and score employees in their Practice
  - HR/People Ops: Overall process ownership

### Target Scale by Practice
- **Software Practice**: 15-42 Risers
- **Platform Practice** (includes Cyber): 15-42 Risers
- **Design Practice**: 15-42 Risers
- **Product Management Practice**: 15-42 Risers
- **Future Expansion**: Leadership, Finance, Growth, HR, Customer Success, IT, Marketing departments

### Known Issues
- **Technical Debt**: None identified yet (new project)
- **Performance Bottlenecks**: None expected for annual batch processing
- **API Limitations**: Dependent on Lattice API rate limits and availability
- **External Dependencies**:
  - Lattice API availability and stability
  - Google Drive access for distribution

## Agent-Specific Guidance

### Common Tasks
- **Data Extraction**: Use LatticeAPI client modules to retrieve review data
- **Document Generation**: Create one markdown file per employee with structured feedback
- **Agent Synthesis**: Use Claude Code agents (not API) to summarize peer ratings and A Player rankings
- **Rise8 Knowledge Integration**: Reference ./knowledge-base directory when creating new agents

### Gotchas and Pitfalls
- **API Authentication**: Ensure .env file is properly configured before running
- **Cross-Practice Data Leakage**: Verify Google Drive permissions prevent cross-department access
- **Scale Considerations**: 4 Practices with 15-42 employees each = significant data volume
- **Agent Creation**: Must use Rise8 knowledge-base material from ./knowledge-base directory

### Success Patterns
- **Modular API Client**: Existing LatticeAPI structure with separate modules (authentication, reviews, users, managers, updates)
- **Semi-Automated Workflow**: User generates files → uploads to Drive → Practice Leads access
- **Claude Code Agents**: Agent chat interface for synthesis (not programmatic API calls)
- **Practice-Based Organization**: Clear separation by department for access control

### Claude Agent Integration Strategy
- **Agent Type**: Claude Code agents (interactive chat interface)
- **Automation Level**: Semi-automated (user initiates agent interactions)
- **Knowledge Base**: Rise8 material in ./knowledge-base directory
- **Use Cases**:
  - Summarization of peer assessment feedback
  - Synthesis of A Player rankings
  - Analysis of peer ratings
  - EOY scorecard data preparation

## Auto-Discovery Hints

### Framework Detection
- **Package Files**: requirements.txt (python-dotenv, requests, pytest, python-docx)
- **Config Files**: .env (API credentials), .devcontainer/ (dev environment)
- **Directory Patterns**: LatticeAPI/ (API client modules), knowledge-base/ (Rise8 materials)

### Tool Integration
- **Linting Config**: To be determined
- **Test Config**: pytest (standard configuration)
- **Build Config**: None (Python script execution)
- **CI/CD Config**: None (local execution only)

---

## Workflow Summary

1. **Data Extraction**: Run Python scripts to retrieve EOY peer assessment reviews from Lattice API
2. **Document Generation**: Create markdown file for each employee with organized feedback
3. **Agent Synthesis**: Use Claude Code agents to summarize A Player rankings and peer ratings
4. **Distribution**: Upload generated markdown files to Google Drive
5. **Review Process**: Practice Leads access their Practice's reviews via Drive and complete EOY scorecards
6. **Access Control**: Google Drive folder permissions ensure Practice Leads only see their Practice's data

## Distribution Approach

**Output Format**: Markdown documents (one per employee)
**Distribution Method**: Google Drive with folder-level permissions
**Access Control**: Practice Leads only access their Practice's reviews
**Security Model**: Cross-department data separation via Drive permissions
