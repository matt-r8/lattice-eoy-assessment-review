# Task List Management

Guidelines for managing task lists in markdown files to track progress on completing a PRD

## Task Lifecycle

Tasks flow through four possible stages:
1. **Backlog** (`/.claude/tasks/1_backlog/001-[feature-name]/`) - Generated PRD folders ready to be worked
2. **Active** (`/.claude/tasks/2_active/001-[feature-name]/`) - Currently being worked on
3. **Completed** (`/.claude/tasks/3_completed/001-[feature-name]/`) - Finished features maintaining original numbering
4. **OBE** (`/.claude/tasks/0_obe/001-[feature-name]/`) - Overtaken by Events (cancelled, superseded, deprioritized)

### Starting Work
- When beginning a feature, move the entire PRD folder `001-[feature-name]/` from `1_backlog/` to `2_active/`
- This keeps all PRD-related files (PRD, tasks, implementation files) together
- Update `/.claude/tasks/project-status.md` to reflect the status change

### OBE (Overtaken by Events) Process
- For PRDs that won't be implemented, move entire folder to `/.claude/tasks/0_obe/001-[feature-name]/`
- Add `obe-reason.md` file explaining the decision:
  ```markdown
  # OBE Reason: [Feature Name]

  **Date**: [Date moved to OBE]
  **Reason**: [cancelled/superseded/deprioritized/requirements changed]
  **Details**: [Explanation of why this PRD was not implemented]
  **Decision Made By**: [Team/Person who made the decision]

  ## Alternative Solution
  [If applicable, describe what replaced this PRD or alternative approach taken]
  ```
- Update `/.claude/tasks/project-status.md` to reflect OBE status

## Task Implementation
- **One sub-task at a time:** Do **NOT** start the next sub‑task until you ask the user for permission and they say "yes" or "y"
- **Completion protocol:**  
  1. When you finish a **sub‑task**, immediately mark it as completed by changing `[ ]` to `[x]`.
  2. If **all** subtasks underneath a parent task are now `[x]`, follow this sequence:
    - **First**: Run the full test suite (`pytest`, `npm test`, `bin/rails test`, etc.)
    - **If tests fail**: Address issues before proceeding, do not commit failing code
    - **Only if all tests pass**: Stage changes (`git add .`)
    - **Clean up**: Remove any temporary files and temporary code before committing
    - **Commit**: Use a descriptive commit message that:
      - Uses conventional commit format (`feat:`, `fix:`, `refactor:`, etc.)
      - Summarizes what was accomplished in the parent task
      - Lists key changes and additions
      - References the task number and PRD context (format: "Related to Task X.Y from prd-feature-name.md")
      - **Formats the message as a single-line command using `-m` flags**, e.g.:

        ```
        git commit -m "feat: add payment validation logic" -m "- Validates card type and expiry" -m "- Adds unit tests for edge cases" -m "Related to Task 2.3 from prd-payment-system.md"
        ```
  3. Once all the subtasks are marked completed and changes have been committed, mark the **parent task** as completed.
  4. When **all parent tasks** are completed for a feature:
    - Move the entire PRD folder `001-[feature-name]/` from `2_active/` to `3_completed/`
    - All implementation files, PRD, and task files stay together in the completed folder
    - Create optional files in the completed folder:
      - `implementation-notes.md` - Technical decisions made during development
      - `retrospective.md` - What went well/poorly for future reference
    - Update `/.claude/tasks/project-status.md` to reflect completion
- Stop after each sub‑task and wait for the user's go‑ahead.

## Task List Maintenance

1. **Update the task list as you work:**
   - Mark tasks and subtasks as completed (`[x]`) per the protocol above.
   - Add new tasks as they emerge.

2. **Maintain the "Relevant Files" section:**
   - List every file created or modified.
   - Give each file a one‑line description of its purpose.

## AI Instructions

When working with task lists, the AI must:

1. **File Movement Management:**
   - Move entire PRD folders (maintaining original numbering) between 1_backlog/2_active/3_completed/0_obe
   - Preserve folder structure: `001-[feature-name]/` stays consistent across all stages
   - Keep all related files (PRD, tasks, implementation) together in the same folder
   - For OBE: Add `obe-reason.md` file when moving to 0_obe folder

2. **Status Tracking:**
   - Update `project-status.md` whenever moving files between backlog/2_active/completed/0_obe
   - Maintain accurate counts and progress metrics including OBE count
   - Add completion dates and duration tracking
   - For OBE: Record date moved and reason category

3. **Task List Maintenance:**
   - Regularly update the task list file after finishing any significant work
   - Follow the completion protocol:
     - Mark each finished **sub‑task** `[x]`
     - Mark the **parent task** `[x]` once **all** its subtasks are `[x]`
   - Add newly discovered tasks
   - Keep "Relevant Files" accurate and up to date

4. **Workflow Enforcement:**
   - Before starting work, check which sub‑task is next
   - After implementing a sub‑task, update the file and then pause for user approval
   - Ensure proper folder structure is maintained throughout the process