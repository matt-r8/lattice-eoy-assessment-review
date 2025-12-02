# Claude Templates

This directory contains templates used by the Claude Agent System.

## Templates

### `vscode-settings-template.json`

**Purpose**: Template for VS Code workspace color customization

**Usage**:
- Automatically copied to `.vscode/settings.json` by `/setup` command
- Contains default "Solutions" theme (Green + Brown)
- Includes example color pairings for other themes

**Do not edit directly in new projects** - use `/setup` to customize colors.

### `handoff-session-template.md`

**Purpose**: Template for session handoff documentation

**Usage**:
- Auto-generated at 65% context usage
- Provides forward-looking information for next session
- Overwrites previous handoff file each time

### `session-summary-template.md`

**Purpose**: Template for session summaries

**Usage**:
- Auto-generated at 65% context usage
- Creates numbered session files (001-SESSION.md, 002-SESSION.md, etc.)
- Archives completed work and decisions

### `agent-session-history-template.md`

**Purpose**: Template for specialized agent session documentation

**Usage**:
- Created by specialized sub-agents upon task completion
- Documents task summary, decisions, deliverables, and learnings
- Stored in `.claude/context/agent-history/[AGENT-TYPE]-[TIMESTAMP].md`
- Provides institutional memory and knowledge transfer

**Required for**:
- All tactical agents (software-engineer, platform-engineering, etc.)
- All strategic agents (architecture, planning, etc.)
- All domain specialists (data-scientist, cybersecurity, etc.)
- All task agents (generate, analyze, validate, etc.)

## Template Management

**Source of Truth**: `solutions` repository contains master templates
**Distribution**: Copy `claude/` folder to `.claude/` in new projects
**Customization**: Templates are meant to be copied and customized per project
