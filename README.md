# AI Agent System Templates

> **Comprehensive frameworks for AI agent orchestration and workflow-driven development**

This repository provides **two complete AI agent frameworks**:
- **🤖 GitHub Copilot Agent System** - Orchestrator-based workflow with task staging and specialist delegation
- **🎯 Claude Agent System** - PRD-driven development with specialized domain agents

Both systems can be used independently or together, depending on your AI tooling preferences.

## 🚀 Quick Setup

Choose your framework based on your AI tooling:

### GitHub Copilot Workflow System

**Step 1: Copy Framework Files**

```bash
# From solutions repository to your project
cp -r .copilot/ /path/to/your/project/
cp COPILOT.md /path/to/your/project/
```

**Step 2: Run Setup Script**

```bash
cd /path/to/your/project
./.copilot/setup.sh
```

This will:
- ✅ Create symlink: `.github/prompts` → `.copilot/prompts` (for auto-loading)
- ✅ Copy `copilot-instructions.md` to `.github/`

**Step 3: Run Workspace Setup**

Open GitHub Copilot Chat and run:

```
@workspace /setup-copilot-workspace
```

This will:
- ✅ Create initial `PROJECT_CONTEXT.md` with organization details
- ✅ Set up task lifecycle folders
- ✅ Initialize violation tracking

**Start Working**

```bash
# In GitHub Copilot Chat
!next          # Interactive task selection
!task          # Create new task
!improvement   # Capture enhancement ideas
```

### Claude Agent System

**Step 1: Copy System Files**

From the `solutions` repository:

```bash
# Copy the entire Claude Agent System
cp -r .claude/ /path/to/your/project/.claude/

# Copy the memory/instruction file
cp CLAUDE.md /path/to/your/project/
```

### Step 2: Initialize Workspace

In your new project, start Claude Code and run:

```bash
# Interactive mode - Claude suggests colors based on project name
/setup

# Single argument - Apply predefined theme
/setup red      # Red + Orange
/setup ocean    # Blue + Teal

# Two arguments - Custom color pairing
/setup red blue       # Red primary, Blue secondary
/setup purple orange  # Purple primary, Orange secondary
```

This command will:
- ✅ Create `.vscode/settings.json` from template
- ✅ Configure unique workspace colors for your project
- ✅ Generate audio completion notification (macOS)
- ✅ Set up all hooks and settings

### Step 3: Start Working

Tell Claude:
```
I'm setting up a new project with the Claude Agent System.
Please use the solutions-guide agent to help me get started.
```

That's it! The system auto-loads and all agents, hooks, and templates work immediately.

## 🎯 Purpose

This template provides a complete system for managing software development projects using specialized AI agents and Product Requirements Documents (PRDs). It eliminates project clutter through organized folder structures and enables knowledge transfer across projects.

**Core Philosophy**: The main Claude agent is an **orchestrator**, not an executor. It delegates 99% of work to specialized agents who have deep domain expertise. This ensures expert-level quality, efficient context usage, and consistent best practices across all work.

## ✨ What You Get

### GitHub Copilot System
- ✅ **Orchestrator-based delegation** (99% of work delegated to specialists)
- ✅ **Task staging workflow** (draft → ready → active → review → completed)
- ✅ **Permission protocol** (ask before acting, confirm before completing)
- ✅ **Hierarchical context** (PROJECT_CONTEXT.md + REPO_CONTEXT.md per repository)
- ✅ **Process violation tracking** (open/closed with metadata and recurrence detection)
- ✅ **Interrupt keywords** (!next, !task, !violation, !improvement, !status)
- ✅ **Specialist prompts** (software engineer, platform engineer, cybersecurity, CI/CD, SRE, product manager, UX/UI, data scientist)
- ✅ **Git worktree support** (automatic detection and enforcement for multi-branch workflows)

### Claude Agent System
- ✅ **8 specialized agents** (project-navigator, prompt-optimizer, solutions-guide, task-analyze, task-document, task-enhance, task-generate, task-validate)
- ✅ **15+ templates** (PRDs, tasks, sessions, agents, architecture)
- ✅ **Automatic hooks** (context tracking, session handoff)
- ✅ **Task workflows** (backlog → active → completed → OBE)
- ✅ **Session continuity** (auto-handoff at 65% context)
- ✅ **Unique workspace colors** (visual project identity)
- ✅ **Custom commands** (extensible slash command system)

### Combined Usage
Both systems can coexist in the same project. The Copilot system focuses on workflow orchestration and task management, while Claude agents provide specialized domain expertise.

## 🏗️ Repository Structure

### GitHub Copilot Framework
```
solutions/
├── .copilot/                        # Copilot workflow system (copy this folder)
│   ├── prompts/                     # Specialist agent prompts
│   │   ├── software-engineer.md     # Software development specialist
│   │   ├── platform-engineer.md     # Infrastructure/Terraform specialist
│   │   ├── cybersecurity-engineer.md # Security/compliance specialist
│   │   ├── cicd-engineer.md         # CI/CD pipeline specialist
│   │   ├── sre-engineer.md          # Reliability engineering specialist
│   │   ├── product-manager.md       # Product strategy specialist
│   │   ├── ux-ui-designer.md        # Design systems specialist
│   │   ├── data-scientist.md        # Data/analytics/ML specialist
│   │   ├── common-instructions.md   # Shared instructions for all prompts
│   │   └── orchestrator.md          # Explicit orchestrator mode
│   ├── templates/                   # Workflow templates
│   │   ├── copilot-instructions.md  # Auto-loading rules (copy to .github/)
│   │   ├── PROJECT_CONTEXT.md       # Organization context template
│   │   ├── REPO_CONTEXT.md          # Repository context template
│   │   ├── REPO_CONTEXT-worktree-terraform.md # Terraform/worktree variant
│   │   └── project-status.md        # Task dashboard template
│   ├── docs/                        # Documentation
│   │   ├── git-worktree-guide.md    # Complete worktree workflow guide
│   │   ├── tool-limitations.md      # Known issues and workarounds
│   │   └── session-handoff-guide.md # Session continuity guide
│   ├── tasks/                       # Task lifecycle folders (created at runtime)
│   │   ├── 0_canceled/              # Canceled tasks
│   │   ├── 1_draft/                 # Draft tasks needing refinement
│   │   ├── 2_ready/                 # Ready for work
│   │   ├── 3_active/                # Currently working
│   │   ├── 4_review/                # Completed, awaiting approval
│   │   ├── 5_completed/             # Approved and finished
│   │   └── 6_blocked/               # Blocked by dependencies
│   └── violations/                  # Process violation tracking (created at runtime)
│       ├── open/                    # Active violations
│       └── closed/                  # Resolved violations
├── COPILOT.md                       # Complete orchestration rules (~4000 lines)
└── README.md                        # This file
```

### Claude Agent Framework
**Solutions (Template Repository):**
```
solutions/
├── .claude/                         # Claude Agent System (copy this entire folder)
│   ├── agents/                      # 9 specialized agent prompts
│   ├── commands/                    # Custom slash commands
│   ├── templates/                   # 15+ workflow templates
│   ├── tasks/                       # PRD workflow directories (0_obe, 1_backlog, 2_active, 3_completed)
│   ├── docs/                        # Agent documentation & examples
│   ├── hooks/                       # Automation hooks (context tracking)
│   ├── settings.json                # Claude Code configuration
│   ├── context/                     # Session history (not copied - created at runtime)
│   └── README.md                    # System documentation
├── CLAUDE.md                        # Agent orchestration rules (copy to project root)
└── README.md                        # This file
```

### After Setup - Copilot in Your Project
```
your-project/
├── .copilot/                        # (copied from solutions/.copilot/)
│   ├── prompts/                     # Auto-loaded specialist prompts
│   ├── templates/                   # Available templates
│   ├── docs/                        # Documentation
│   ├── tasks/                       # Task lifecycle folders (orchestrator creates)
│   │   └── project-status.md        # Generated dashboard (orchestrator maintains)
│   └── violations/                  # Violation tracking (orchestrator creates)
├── .github/
│   └── copilot-instructions.md      # Auto-loads orchestrator rules
├── COPILOT.md                       # Orchestrator rules (auto-loaded)
├── PROJECT_CONTEXT.md               # Generated by orchestrator on first use
└── [your project files...]
```

### After Setup - Claude in Your Project:
```
solutions/
├── .claude/                         # Claude Agent System (copy this entire folder)
│   ├── agents/                      # 9 specialized agent prompts
│   ├── commands/                    # Custom slash commands
│   ├── templates/                   # 15+ workflow templates
│   ├── tasks/                       # PRD workflow directories (0_obe, 1_backlog, 2_active, 3_completed)
│   ├── docs/                        # Agent documentation & examples
│   ├── hooks/                       # Automation hooks (context tracking)
│   ├── settings.json                # Claude Code configuration
│   ├── context/                     # Session history (not copied - created at runtime)
│   └── README.md                    # System documentation
├── CLAUDE.md                        # Agent orchestration rules (copy to project root)
└── README.md                        # This file
```

**After Setup in Your Project:**
```
your-project/
├── .claude/                         # (copied from solutions/.claude/)
│   ├── agents/                      # Auto-loaded specialized agents
│   ├── commands/                    # Custom slash commands
│   ├── templates/                   # Available templates
│   ├── tasks/                       # PRD lifecycle folders
│   ├── docs/                        # Documentation
│   ├── hooks/                       # Active hooks
│   ├── settings.json                # Active configuration
│   ├── settings.local.json          # Local overrides (created by /setup)
│   ├── audio/                       # Completion audio (created by /setup)
│   └── context/                     # Runtime session history
├── .vscode/                         # Workspace colors (created by /setup)
│   └── settings.json                # Auto-generated from template
├── CLAUDE.md                        # Agent rules (auto-loaded)
└── [your project files...]
```

**Key Points:**
- **Copilot**: `.copilot/` folder + `COPILOT.md` + copy `copilot-instructions.md` to `.github/`
- **Claude**: `.claude/` folder + `CLAUDE.md`
- Both systems auto-load their respective configuration files
- `PROJECT_CONTEXT.md` (Copilot) is orchestrator-generated, not committed
- `.vscode/` (Claude) is created by `/setup` command

---

## 📋 Copilot Workflow System

### Core Philosophy

The **orchestrator delegates 99% of work** to specialist prompts. It never implements directly - it coordinates, enforces protocols, and maintains workflow state.

### Permission Protocol ⚠️

**Present → Ask → Wait → Act**

Before starting work:
1. Present what will be done
2. Ask: "Should I proceed?"
3. **WAIT** for explicit approval
4. Then begin work

After completing work:
1. Move to `4_review/` automatically
2. Report what was done
3. Ask: "Should I mark this as completed?"
4. **WAIT** for user confirmation
5. Then move to `5_completed/`

### Task Staging Lifecycle

```
1_draft/ → 2_ready/ → 3_active/ → 4_review/ → 5_completed/
         ↘ 6_blocked/ ↗
         ↘ 0_canceled/
```

**Critical Rules**:
- ✅ ALL new tasks start in `1_draft/`
- ✅ Move to `2_ready/` when fully defined
- ✅ Move to `3_active/` with user permission
- ✅ Move to `4_review/` automatically when work complete
- ✅ Move to `5_completed/` ONLY after user approves

### Specialist Delegation

| Task Type | Delegate To |
|-----------|-------------|
| Code/Architecture/Refactoring | `/software-engineer` |
| Infrastructure/Platform/Terraform | `/platform-engineer` |
| Security/Compliance/Audits | `/cybersecurity-engineer` |
| CI/CD/Pipelines/GitHub Actions | `/cicd-engineer` |
| Reliability/SRE/Monitoring | `/sre-engineer` |
| Product/Planning/Requirements | `/product-manager` |
| UI/UX/Design Systems | `/ux-ui-designer` |
| Data/Analytics/ML | `/data-scientist` |

### Interrupt Keywords

- `!next` - Interactive task selection (shows options, waits for choice)
- `!task` - Quick task creation
- `!violation` - Capture process violation
- `!improvement` - Capture enhancement idea
- `!status` - Check active work status
- `!previous` - Resume previous work

### Hierarchical Context System

**PROJECT_CONTEXT.md** (Workspace root - orchestrator creates):
- Organization overview (team, mission)
- Standards & compliance requirements
- Cross-repository patterns
- Repository inventory

**REPO_CONTEXT.md** (Each repository - orchestrator creates):
- Technical architecture & tech stack
- Repository-specific patterns
- Deployment procedures
- Current work status

**Update Triggers**:
- Org changes → Update `PROJECT_CONTEXT.md`
- Architecture/infra changes → Update `REPO_CONTEXT.md`
- Workflow changes → Update `COPILOT.md` (not context files)

### Git Worktree Support

Automatic detection and enforcement for repositories requiring parallel branch work:
- Detects worktree requirements from `PROJECT_CONTEXT.md`
- Blocks operations in non-worktree clones when required
- Complete guide: `.copilot/docs/git-worktree-guide.md`

### Process Violation Tracking

Violations captured in `.copilot/violations/{open,closed}` with:
- YAML metadata (severity, recurrence, related improvements)
- Descriptive filenames (`violation-YYYYMMDD-NNN-description.md`)
- Resolution tracking and pattern detection

---

## 📋 Claude PRD Organization System (Legacy)

Features are organized using a **numbered folder system** that eliminates project-level clutter:

Each project can have a **unique two-color theme** for easy visual identification across multiple VS Code windows.

### How It Works

When you run `/setup`:
1. Creates `.vscode/settings.json` from template
2. Default theme is **Green + Brown** ("Solutions")
3. Claude detects project name and suggests appropriate colors
4. You can choose from suggested themes or pick custom colors

### Available Themes

**Nature:**
- Green + Brown (default "Solutions" theme)
- Teal + Sage

**Ocean:**
- Blue + Teal
- Cyan + Navy

**Fire:**
- Red + Orange
- Orange + Yellow

**Royal:**
- Purple + Blue
- Magenta + Purple

**Sunset:**
- Pink + Orange
- Rose + Gold

**Energy:**
- Orange + Yellow

**Tech:**
- Cyan + Navy

**Earth:**
- Teal + Sage

### Theme Selection

Claude will **automatically infer** themes based on project name keywords:

- **solutions, systems, platform, framework** → Green + Brown
- **ocean, sea, water, aqua** → Blue + Teal
- **fire, flame, heat, burn** → Red + Orange
- **royal, king, crown, purple** → Purple + Blue
- **sunset, dusk, dawn, pink** → Pink + Orange
- **tech, cyber, digital, code** → Cyan + Navy

Or you can **manually choose** any color pairing from the list above.

### What Gets Colored

✅ **Primary color** (bright): Title bar, status bar, major UI elements
✅ **Secondary color** (accent): Borders, tab underlines, icons
✅ **Background tint**: Sidebar (subtle blend of both colors)
❌ **Stays default**: Editor, terminal content, syntax highlighting

This keeps code **fully readable** while making workspaces **instantly recognizable**!

### Quick Color Change

**Predefined themes** (single argument):
```bash
/setup red      # Red + Orange
/setup ocean    # Blue + Teal
/setup purple   # Purple + Blue
/setup tech     # Cyan + Navy
```

**Custom pairings** (two arguments):
```bash
/setup red blue       # Red primary + Blue secondary
/setup purple orange  # Purple primary + Orange secondary
/setup green cyan     # Green primary + Cyan secondary
/setup magenta yellow # Magenta primary + Yellow secondary
```

**Supported color keywords**:
- Single colors: `red`, `orange`, `yellow`, `green`, `teal`, `blue`, `cyan`, `purple`, `magenta`, `pink`, `brown`, `navy`, `sage`
- Neutral colors: `gray`, `white`, `silver`, `black`
- Theme names: `ocean`, `fire`, `royal`, `sunset`, `tech`, `nature`, `earth`, `energy`

**Interactive mode**: Run `/setup` without arguments for guided setup

**To revert to defaults**: Run `/setup nature` or manually edit `.vscode/settings.json`

## 📁 PRD Organization System

Features are organized using a **numbered folder system** that eliminates project-level clutter:

### Folder Lifecycle
```
1_backlog/001-feature-name/    →    2_active/001-feature-name/    →    3_completed/001-feature-name/
                              ↘                                   ↗
                                0_obe/001-feature-name/ (if cancelled)
```

### Folder Contents
Each PRD folder contains:
- `prd-001-feature-name.md` - Product Requirements Document
- `tasks-prd-001-feature-name.md` - Implementation task breakdown
- Implementation files (code, configs, tests)
- `implementation-notes.md` - Technical decisions and notes
- `retrospective.md` - Lessons learned (completed features)
- `obe-reason.md` - Cancellation reasoning (OBE features)

### Enhanced Workflow (Optional)
For projects requiring knowledge transfer and pattern reusability:
- `PROJECT_IMPLEMENTATION_GUIDE.md` - Standalone replication guide
- `SOLUTION_PATTERNS.md` - Reusable architectural patterns
- `TECHNOLOGY_DECISION_LOG.md` - Decision rationale documentation

## 🤖 Available Agents

This repository includes specialized agents for Claude Agent System management and engineering practice framework operations.

| Agent | Specialization | Use Cases |
|-------|---------------|-----------|
| **🧭 Project Navigator** | Knowledge management | Project understanding, historical decisions, pattern documentation |
| **💡 Prompt Optimizer** | AI prompt engineering | Prompt improvement, refinement, creation for complex tasks |
| **🌱 Solutions Guide** | System setup & coaching | Project initialization, workflow guidance, context optimization |
| **📊 Task Analyze** | Framework analysis | Competency evaluation, pattern identification, gap analysis, quality assessment |
| **📝 Task Document** | Documentation creation | User guides, implementation docs, reference materials, training content |
| **✨ Task Enhance** | Content improvement | Quality enhancement, clarity improvements, modernization, customization |
| **🔧 Task Generate** | Content generation | Practice frameworks, role definitions, agent prompts, competency matrices |
| **✅ Task Validate** | Quality assurance | Template compliance, structural validation, consistency checking |

**Agent Selection**: Main Claude agent automatically selects the appropriate specialized agent based on the task type and scope. Users rarely need to request specific agents.

**Note**: For full engineering practice agents (Platform Engineering, Cybersecurity, CI/CD, Software Engineering, UX/UI Design, SRE, Product Management, Data Science, etc.), visit the [Rise8 Agents repository](https://github.com/rise8-us/8gents).

## 🔄 Workflow Overview

### Standard PRD Workflow
1. **Create PRD** → Use `1_create-prd.md` template
2. **Generate Tasks** → Use `2_generate-tasks.md` template
3. **Implement** → Use `3_process-task-list.md` workflow
4. **Complete** → Move to `3_completed/` with retrospective

### Enhanced PRD Workflow (Knowledge Transfer)
Standard workflow **plus** mandatory deliverables:
- **Task 3.4**: Create implementation guide for replication
- **Task 3.5**: Extract reusable solution patterns
- **Task 3.6**: Document technology decisions and rationale

## 🎯 Enhanced Features for Knowledge Transfer

### Implementation Guides
Create standalone guides that enable anyone to replicate your solution independently:
```markdown
PROJECT_IMPLEMENTATION_GUIDE.md
├── Environment Setup
├── Step-by-Step Implementation
├── Configuration Details
├── Testing & Validation
├── Troubleshooting Guide
└── Adaptation Instructions
```

### Solution Patterns
Extract technology-agnostic patterns for future reuse:
```markdown
SOLUTION_PATTERNS.md
├── Architectural Patterns
├── Design Decisions
├── Scaling Strategies
├── Integration Approaches
└── Adaptation Guidelines
```

### Decision Logs
Capture the "why" behind technology choices:
```markdown
TECHNOLOGY_DECISION_LOG.md
├── Decision Context
├── Options Considered
├── Selection Rationale
├── Trade-offs Made
└── Migration Paths
```

## 📋 Quality Gates

### Standard Projects
- [ ] All functional requirements implemented
- [ ] Tests passing and code reviewed
- [ ] Documentation updated

### Enhanced Projects (Knowledge Transfer)
- [ ] Implementation guide enables independent replication
- [ ] Solution patterns are technology-agnostic and reusable
- [ ] Decision log captures rationale for all major choices
- [ ] All deliverables support knowledge transfer

## 🚀 Expected Benefits

### For Standard Workflow
- **Organized Development**: No scattered files across project
- **Clear Progress Tracking**: Visual folder-based lifecycle
- **Agent Efficiency**: Context-optimized specialized agents
- **Decision Preservation**: OBE folder maintains cancelled work

### For Enhanced Workflow
- **60-80% Faster Similar Projects**: Implementation guides accelerate future work
- **Better Architecture Decisions**: Pattern library improves choices
- **Reduced Decision Overhead**: Decision logs prevent re-solving problems
- **Team Scalability**: New members can understand and replicate solutions
- **Cross-Project Learning**: Patterns improve decisions across projects

## 🛠️ Usage Examples

### Starting a New Feature
```bash
# Tell Claude:
"I want to create a PRD for user authentication system"

# Claude will:
1. Use 1_create-prd.md to ask clarifying questions
2. Create 001-user-authentication/ folder in 1_backlog/
3. Generate prd-001-user-authentication.md
4. Ask for approval before task generation
```

### Implementation Phase
```bash
# Tell Claude:
"Let's start implementing the user authentication PRD"

# Claude will:
1. Move 001-user-authentication/ to 2_active/
2. Follow 3_process-task-list.md workflow
3. Complete tasks one by one with approval
4. Create implementation files within the folder
```

### Knowledge Transfer (Enhanced)
```bash
# For enhanced workflow, Claude will also create:
- PROJECT_IMPLEMENTATION_GUIDE.md
- SOLUTION_PATTERNS.md
- TECHNOLOGY_DECISION_LOG.md
```

## 📖 Documentation

- **[CLAUDE.md](CLAUDE.md)** - Complete agent orchestration rules
- **[docs/](docs/)** - Detailed agent documentation
- **[templates/](templates/)** - All workflow and development templates

## 🎯 Next Steps

### After Setup
1. **Customize** `PROJECT_CONTEXT.md` with your project details
2. **Train team** on PRD workflow if working with others
3. **Start** with a simple feature to learn the system

### For Enhanced Workflow
1. **Use enhanced templates** for all new PRDs
2. **Build pattern library** from multiple projects
3. **Measure** acceleration in similar projects

## 🤝 Team Integration

Add to your project README:
```markdown
## Claude Agent Integration
This project uses the Claude Agent System for development workflow management.
- Project context: `PROJECT_CONTEXT.md`
- Active tasks: `.claude/tasks/2_active/`
- Workflow templates: `.claude/templates/`

### PRD Organization
Features are organized in numbered folders that move through workflow stages:
- **Backlog**: `.claude/tasks/1_backlog/001-feature-name/`
- **Active**: `.claude/tasks/2_active/001-feature-name/`
- **Completed**: `.claude/tasks/3_completed/001-feature-name/`
- **OBE**: `.claude/tasks/0_obe/001-feature-name/` (Overtaken by Events)
```

## 🌟 More Agents

If you'd like more project or practice specific Rise8 Agents (8gents), visit the official repository:
**https://github.com/rise8-us/8gents**

## 📄 License

This repository is designed for internal use in AI agent orchestration systems. Adapt and modify as needed for your specific use cases.

---

**Status**: ✅ Ready for use in any project
**Templates Available**: 13 total (including enhanced workflow templates)
**Last Updated**: September 2024