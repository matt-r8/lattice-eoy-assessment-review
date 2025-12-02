---
description: Prepare handoff summary for next agent (project, gitignored)
---


You MUST create ACTUAL session handoff documentation FILES according to the AUTOMATIC SESSION HANDOFF PROTOCOL in CLAUDE.md.


**CRITICAL**: This command creates FILES using Write tool, not just chat summaries.


**Follow these steps exactly:**


1. **Determine Session Number**:
  - Check `.claude/context/session-history/` for existing session files
  - Find highest session number (e.g., if 011-SESSION.md exists, next is 012)
  - Use zero-padded 3-digit format (001, 002, 003, etc.)


2. **Create Session Summary File** (USING WRITE TOOL):
  - Read template: `.claude/templates/session-summary-template.md`
  - Create file: `.claude/context/session-history/[NUMBER]-SESSION.md`
  - Fill in ALL required sections with actual session data:
    * Date and duration
    * Context usage at handoff
    * Completed tasks with outcomes
    * Decisions made with rationale
    * Issues encountered (resolved and unresolved)
    * Files created/modified
    * Commands executed
    * Session statistics


3. **Create/Update Handoff File** (USING WRITE TOOL):
  - Read existing `.claude/context/session-history/HANDOFF-SESSION.md` first
  - Read template: `.claude/templates/handoff-session-template.md`
  - Overwrite: `.claude/context/session-history/HANDOFF-SESSION.md`
  - Fill in ALL required sections with forward-looking information:
    * Current status and progress
    * Prioritized next steps with context
    * Active blockers and issues
    * Important decisions and context
    * Working files and git state
    * Quick start guide for next session
    * Reference to the session file you just created


4. **Quality Validation**:
  - Ensure DELEGATION MANDATE section is included in HANDOFF-SESSION.md
  - Verify all template sections are filled (not placeholder text)
  - Check that next steps are prioritized and actionable
  - Confirm git status and branch information is accurate
  - Validate file paths and references are correct


5. **Confirm Files Created**:
  - Tell user: "Created `.claude/context/session-history/[NUMBER]-SESSION.md`"
  - Tell user: "Updated `.claude/context/session-history/HANDOFF-SESSION.md`"
  - Show file paths so user can verify


**MANDATORY**: You MUST use the Write tool to create these files. Providing a summary in chat is NOT SUFFICIENT. The files must exist on disk for the next session to read them.


**Example of CORRECT behavior**:
```
1. Read .claude/templates/session-summary-template.md
2. Use Write tool to create .claude/context/session-history/012-SESSION.md
3. Read .claude/context/session-history/HANDOFF-SESSION.md (existing)
4. Use Write tool to overwrite .claude/context/session-history/HANDOFF-SESSION.md
5. Tell user: "✅ Created 012-SESSION.md and updated HANDOFF-SESSION.md"
```


**Example of INCORRECT behavior** (DO NOT DO THIS):
```
"Here's a handoff summary for the next session: [long text in chat]"
```
