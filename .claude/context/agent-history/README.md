# Agent Session History

This directory contains session history files created by specialized agents when they are invoked to complete tasks.

## Purpose

Agent session histories serve several critical functions:

1. **Institutional Memory**: Preserve decision rationale and technical context
2. **Learning & Patterns**: Enable pattern recognition across similar tasks
3. **Audit Trail**: Provide debugging information for troubleshooting
4. **Knowledge Transfer**: Help future agents understand project history
5. **Session Continuity**: Maintain context across session boundaries

## File Naming Convention

```
[AGENT-TYPE]-[TIMESTAMP].md
```

**Examples**:
- `tactical-software-engineer-2025-10-16-1430.md`
- `strategic-platform-engineering-2025-10-16-1535.md`
- `data-scientist-2025-10-17-0900.md`

**Format**:
- **Agent Type**: Full agent name (kebab-case)
- **Timestamp**: ISO format YYYY-MM-DD-HHMM
- **Extension**: Always `.md` (Markdown)

## Template

Use the standard template located at:
```
.claude/templates/agent-session-history-template.md
```

## Required Content

Every agent session history must include:

### Essential Sections
- ✅ **Task Summary**: What was requested and why
- ✅ **Approach & Decisions**: Key decisions with rationale
- ✅ **Deliverables**: Files created/modified with descriptions
- ✅ **Outcomes & Validation**: Success criteria verification
- ✅ **Challenges & Solutions**: Issues and resolutions
- ✅ **Recommendations**: Next steps and improvements
- ✅ **Knowledge Transfer**: Learnings and patterns

### Metadata
- Agent name and type
- Date and duration
- Context usage metrics
- Related resources (task files, PRDs, etc.)

## When to Create

**MANDATORY**: Every specialized agent invocation must create a session history file upon task completion.

This applies to all agent types:
- Tactical agents (software-engineer, platform-engineering, etc.)
- Strategic agents (architecture, planning, etc.)
- Domain specialists (data-scientist, cybersecurity, etc.)
- Task agents (generate, analyze, validate, etc.)

## Main Agent Responsibilities

The main orchestrator agent must:

1. **Include requirement in agent briefing**
2. **Verify documentation upon completion**
3. **Reference agent histories in main session summaries**
4. **Link to agent sessions in handoff documentation**

## Benefits

- **Debugging**: Quickly trace back through agent decisions
- **Onboarding**: New sessions can review past approaches
- **Consistency**: Maintain consistent patterns across tasks
- **Quality**: Learn from successful and unsuccessful approaches
- **Efficiency**: Avoid repeating mistakes or research

## Directory Structure

```
.claude/context/agent-history/
├── README.md (this file)
├── tactical-software-engineer-2025-10-16-1430.md
├── tactical-software-engineer-2025-10-16-1645.md
├── strategic-platform-engineering-2025-10-17-0900.md
└── data-scientist-2025-10-17-1100.md
```

## Maintenance

- Keep all agent session histories indefinitely
- Review periodically for patterns and learnings
- Reference when similar tasks arise
- Use for retrospectives and process improvements

## See Also

- Main session histories: `.claude/context/session-history/`
- Agent invocation examples: `.claude/docs/agent-invocation-examples.md`
- Agent orchestration rules: `CLAUDE.md` (Agent Session History Documentation section)
