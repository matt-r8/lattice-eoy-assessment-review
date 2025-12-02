# Claude Code Workflow System

A comprehensive task management system for feature development using Product Requirements Documents (PRDs) and structured task tracking.

## 📋 Overview

This workflow system guides feature development from initial concept through completion using a three-stage process:

1. **PRD Creation** - Document requirements and specifications
2. **Task Generation** - Break down features into actionable tasks with agent assignments
3. **Implementation Tracking** - Monitor progress through backlog → active → completed lifecycle

## 🗂️ Directory Structure

```
/.claude/tasks/
├── 1_backlog/          # Features ready for development
├── 2_active/           # Currently being developed
├── 3_completed/        # Finished features (numbered folders)
├── templates/          # Standardized templates
├── scripts/            # Validation and automation scripts
├── project-status.md   # Project dashboard and metrics
└── README.md          # This documentation
```

### Folder Numbering

Folders are numbered to show the natural workflow progression:
- **1_backlog** - Starting point for new features
- **2_active** - Work in progress
- **3_completed** - Final destination with chronological numbering

## 🚀 Getting Started

### 1. Create a New Feature

Start by creating a Product Requirements Document:

```bash
# Follow the structured PRD creation process
# This will ask clarifying questions and generate a complete PRD
```

Use the workflow defined in `1_create-prd.md` which includes:
- Clarifying questions to understand requirements
- Standardized PRD structure
- Clear functional requirements
- Success metrics definition

### 2. Generate Tasks

Convert your PRD into actionable tasks:

```bash
# Generate task breakdown with agent assignments
# This creates detailed subtasks for implementation
```

Follow `2_generate-tasks.md` process:
- Parent task identification (3-7 high-level tasks)
- Detailed subtask breakdown (max 8 subtasks per parent)
- Agent assignments for context efficiency
- File identification for implementation

### 3. Implement Features

Track progress through the implementation lifecycle:

```bash
# Move from backlog → active → completed
# Update task status as work progresses
```

Use `3_process-task-list.md` guidelines:
- One subtask at a time with user approval
- Immediate completion marking
- Quality gates and testing
- Proper commit and documentation

## 📁 File Naming Conventions

### PRD Files
- **Format**: `prd-[feature-name].md`
- **Example**: `prd-user-authentication.md`

### Task Files
- **Format**: `tasks-prd-[feature-name].md`
- **Example**: `tasks-prd-user-authentication.md`

### Completed Features
- **Format**: `XXX-[feature-name]/` (where XXX is sequential number)
- **Example**: `001-user-authentication/`

## 🤖 Agent Assignment System

Tasks are assigned to specialized agents to keep context windows small and leverage expertise:

### Available Agents

| Agent | Expertise | Use For |
|-------|-----------|---------|
| **software-engineer** | Code implementation, APIs, business logic | Core application features |
| **platform-engineer** | Infrastructure, databases, deployment | System architecture, DevOps |
| **cybersecurity-engineer** | Security, compliance, authentication | Security implementations |
| **data-scientist** | Analytics, metrics, data processing | Reporting and analytics |
| **product-manager** | Requirements, user stories, planning | Feature clarification |
| **ux-ui-designer** | UI/UX design, user experience | Frontend and design |
| **cicd-engineer** | CI/CD, build automation, testing | Deployment pipelines |
| **project-navigator** | Documentation, knowledge management | Cross-cutting concerns |
| **solutions-guide** | Claude system setup, orchestration | Workflow optimization |

### Assignment Principles

1. **Expertise Matching** - Match task domain to agent specialization
2. **Context Efficiency** - Use most specialized agent to minimize context
3. **Load Balancing** - Distribute tasks (max 8-10 per agent per feature)
4. **Single Responsibility** - Clear agent ownership per subtask

## 🔧 Validation and Automation

### Validation Scripts

Run these scripts to maintain workflow integrity:

```bash
# Check workflow structure and file consistency
/.claude/scripts/validate-workflow.sh

# Analyze task dependencies and agent workload
/.claude/scripts/check-dependencies.sh

# Update project metrics and statistics
/.claude/scripts/generate-metrics.sh
```

### What They Check

- **File naming conventions** and consistency
- **Task completion logic** (parent/subtask relationships)
- **Agent availability** and workload distribution
- **Project statistics** and progress metrics
- **Folder structure** integrity

## 📊 Project Status Dashboard

The `project-status.md` file provides:

- **Current statistics** (completed, active, backlog counts)
- **Progress metrics** (weekly, monthly, quarterly completion rates)
- **Development velocity** (average feature duration)
- **Workflow commands** for file management

## 🔄 Workflow Commands

### Move to Active Phase
```bash
mv /.claude/tasks/1_backlog/prd-[feature].md /.claude/tasks/2_active/
mv /.claude/tasks/1_backlog/tasks-prd-[feature].md /.claude/tasks/2_active/
```

### Complete Feature
```bash
mkdir /.claude/tasks/3_completed/XXX-[feature-name]/
mv /.claude/tasks/2_active/prd-[feature].md /.claude/tasks/3_completed/XXX-[feature-name]/
mv /.claude/tasks/2_active/tasks-prd-[feature].md /.claude/tasks/3_completed/XXX-[feature-name]/
```

### Generate Metrics
```bash
/.claude/scripts/generate-metrics.sh
```

## 📝 Templates

Standardized templates ensure consistency:

- **`prd-template.md`** - Complete PRD structure with all required sections
- **`tasks-template.md`** - Task format with agent assignments and context
- **`implementation-notes-template.md`** - Technical decision documentation

### Using Templates

```bash
# Copy template to start new feature
cp /.claude/tasks/templates/prd-template.md /.claude/tasks/1_backlog/prd-new-feature.md

# Edit template content
# Follow workflow process for completion
```

## 🎯 Best Practices

### Task Management
- **Keep subtasks small** (1-4 hours of work each)
- **Limit parent tasks** (max 3-7 per feature)
- **Assign appropriate agents** based on expertise
- **Update status immediately** upon completion

### Quality Assurance
- **Run tests** before marking tasks complete
- **Update documentation** as features are implemented
- **Follow security guidelines** for sensitive implementations
- **Validate integration points** with existing systems

### Documentation
- **Create implementation notes** for technical decisions
- **Document architectural choices** and rationale
- **Maintain clear commit messages** with task references
- **Update project status** regularly

## 🔍 Troubleshooting

### Common Issues

**Missing agent assignments**
```bash
# Check task files for agent assignments
grep -r "Assigned Agent" /.claude/tasks/2_active/
```

**Inconsistent task completion**
```bash
# Run dependency checker
/.claude/scripts/check-dependencies.sh
```

**Outdated project statistics**
```bash
# Regenerate metrics
/.claude/scripts/generate-metrics.sh
```

### File Structure Problems

**Wrong folder locations**
```bash
# Validate entire workflow
/.claude/scripts/validate-workflow.sh
```

**Missing templates**
```bash
# Check template availability
ls -la /.claude/tasks/templates/
```

## 🎉 Success Metrics

This workflow system provides:

- **Structured approach** to feature development
- **Context-efficient** agent utilization
- **Comprehensive tracking** from concept to completion
- **Quality assurance** through validation scripts
- **Clear documentation** of technical decisions
- **Measurable progress** through project metrics

## 📚 Additional Resources

- `1_create-prd.md` - Detailed PRD creation process
- `2_generate-tasks.md` - Task generation guidelines
- `3_process-task-list.md` - Implementation workflow
- `project-status.md` - Current project dashboard
- Templates folder - Standardized starting points

---

**Last Updated**: 2025-09-18
**Version**: 1.0
**Workflow System**: Production Ready