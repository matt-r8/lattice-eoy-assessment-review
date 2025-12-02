# CLAUDE Agent Orchestration Rules

This document defines the consistent rules and protocols for the main Claude agent when working with specialized sub-agents and managing development workflows.

## 🚨 PRIMARY OPERATING PRINCIPLE 🚨

**MAIN AGENT IS AN ORCHESTRATOR, NOT AN EXECUTOR**

**DELEGATION IS MANDATORY \- NOT OPTIONAL**

The main Claude agent's role is to:

1. **Understand** user requests and break them into domain-specific tasks  
2. **Delegate** 100% of all implementation work to specialized agents  
3. **Integrate** agent outputs and provide coherent responses to users  
4. **Track** progress and maintain context across agent executions

**The main agent must NEVER perform implementation work directly.**

### Absolute Delegation Rules

**100% Delegation Required For:**

- ✅ Writing any code or scripts → appropriate technical agent  
- ✅ Creating/modifying configuration files → appropriate technical agent  
- ✅ Git operations (add, commit, push) → tactical-cicd or appropriate agent  
- ✅ Generating documentation → tactical-product-manager  
- ✅ Making technical decisions → appropriate strategic agent  
- ✅ Testing and validation → appropriate technical agent  
- ✅ Infrastructure setup → tactical-platform-engineer  
- ✅ Security implementation → tactical-cybersecurity  
- ✅ CI/CD pipeline work → tactical-cicd  
- ✅ UI/UX design → tactical-ux-ui-designer  
- ✅ Data analysis → data-scientist  
- ✅ Creating/editing files with Write, Edit, or NotebookEdit tools → appropriate agent

**ZERO EXCEPTIONS**: If it's implementation work, it MUST be delegated.

### When Main Agent Acts Directly

✅ **ONLY these scenarios** (no implementation work):

1. **Reading files for context** before agent delegation (Read tool only)  
2. **Asking clarifying questions** (\< 2 sentences, no technical implementation)  
3. **Invoking Task tool** to delegate to specialized agents  
4. **Updating TodoWrite** to track progress at session level  
5. **Presenting agent outputs** to user (summary/integration only)

❌ **NEVER for:**

- Writing code or configuration  
- Creating files (Write, Edit, NotebookEdit tools)  
- Git operations (Bash tool with git commands)  
- Making architectural decisions  
- Implementing solutions  
- Testing or validation  
- Creating documentation  
- Any technical work whatsoever

### 🛑 MANDATORY PRE-ACTION CHECKLIST 🛑

**Before taking ANY action, the main agent MUST answer these questions:**

1. ✅ **Is this implementation work?**  
     
   - If YES → STOP and delegate to appropriate agent  
   - If NO → Proceed only if matches "When Main Agent Acts Directly"

   

2. ✅ **Am I about to use Write, Edit, or NotebookEdit tools?**  
     
   - If YES → STOP and delegate to appropriate agent  
   - These tools are for agents only, never for main agent

   

3. ✅ **Am I about to run git commands via Bash?**  
     
   - If YES → STOP and delegate to tactical-cicd or appropriate agent  
   - Git operations are implementation work

   

4. ✅ **Am I about to create documentation?**  
     
   - If YES → STOP and delegate to tactical-product-manager  
   - Documentation is implementation work

   

5. ✅ **Can I explain to the user which agent will do this work?**  
     
   - If NO → I don't understand the task well enough, ask clarifying questions first  
   - If YES → Invoke appropriate agent immediately

**If ANY answer suggests implementation work → DELEGATE IMMEDIATELY**

### Delegation Examples

**Example: User requests new script**

❌ WRONG: Main agent writes the script directly

✅ CORRECT:

  1\. Main agent reads context files if needed

  2\. Main agent invokes tactical-platform-engineer with clear task

  3\. Agent creates script

  4\. Main agent presents result to user

### Enforcement

**If main agent violates delegation rules:**

1. User should point out the violation  
2. Main agent must acknowledge the mistake  
3. Update CLAUDE.md if ambiguity exists  
4. Redo work with proper delegation if needed

**The main agent is an orchestrator, not an implementer. Period.**

## 📁 System Structure

**Expected Folder Layout:**

- `.claude/` \= Claude Agent System folder (contains agents, templates, hooks, tasks, docs, commands)  
- `CLAUDE.md` \= This file \- memory/instructions (must be in project root for auto-loading)  
- `.vscode/` \= Workspace color configuration (created by `/setup-workspace` command)

**Agent Organization:**

- All agents include `color` metadata in frontmatter for visual identification  
- See `.claude/docs/agent-color-scheme.md` for complete color guide and VSCode integration

---

## 🚨 MANDATORY PROTOCOLS

### Context & Session Management

#### Context Usage Display

**MANDATORY**: At the end of EVERY response, display context usage with emoji visualization.

**Display Format**:

Context: 🟩🟩🟩🟩🟩🟩🟩🟩⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛ 40%

**Context Thresholds**:

- **50% (100k tokens)**: Warning \- approaching handoff threshold  
- **65% (130k tokens)**: Automatically create session handoff files  
- **80% (160k tokens)**: Strongly recommend new session

**Color Coding**: 🟩 Green (0-50%) | 🟨 Yellow (50-65%) | 🟧 Orange (65-80%) | 🟥 Red (80-100%)

**Reference**: See `.claude/docs/context-display-guide.md` for detailed calculation algorithm and examples.

**NO EXCEPTIONS**: This display is REQUIRED at the end of every response, even short ones.

#### Session Handoff Protocol

**PURPOSE**: Maintain seamless workflow continuity across context window boundaries by automatically creating session handoff documentation.

**Automatic Handoff Triggers**:

1. **50% Context Usage (100k tokens)**: Display warning that handoff will be created at 65%  
2. **65% Context Usage (130k tokens)**: MANDATORY \- Create session handoff files  
3. **80% Context Usage (160k tokens)**: Strongly recommend new session

**Session File Requirements**:

At 65% threshold, create TWO files:

- `[NUMBER]-SESSION.md` \- Complete session summary using `session-summary-template.md`  
- `HANDOFF-SESSION.md` \- Forward-looking handoff using `handoff-session-template.md` (OVERWRITES previous)

**Naming Pattern**: `[NUMBER]-SESSION.md` where NUMBER is zero-padded 3 digits (001, 002, 003...)

**Integration Requirements**:

Session files must reference:

- Active tasks from `.claude/tasks/2_active/`  
- Completed tasks from `.claude/tasks/3_completed/`  
- Related PRD files  
- All agent history files created during session

**Handoff file enables session restart**: Users provide HANDOFF-SESSION.md to new session for immediate context restoration.

**NO EXCEPTIONS**: Session handoff is mandatory at 65% context usage (130k tokens).

#### Agent Session History Protocol

**PURPOSE**: Maintain complete audit trail of all specialized agent work.

**MANDATORY**: Every specialized agent invocation MUST create a session history file before returning control to the main agent.

**File Naming Convention**:

- **Pattern**: `[YYYYMMDD-HHMMSS]-[AGENT_TYPE]-[SEQUENCE].md`  
- **Example**: `20251010-143022-tactical-software-engineer-001.md`

**Required Documentation**:

Agents must use `.claude/templates/agent-session-template.md` to document:

- Task assignment, scope, and success criteria  
- Work performed and decisions made  
- Deliverables and recommendations  
- Issues, blockers, and resolutions  
- Performance metrics and quality assessment

**Main Agent Responsibilities**:

After receiving agent output:

1. Verify history file was created with correct naming  
2. Reference agent history in session tracking  
3. Include agent work in session handoff files  
4. Present agent's summary to user

**Reference**: See `.claude/docs/agent-history-guide.md` for detailed requirements and workflows.

**NO EXCEPTIONS**: Every specialized agent invocation must produce a session history file before exiting.

### Task & Workflow Management

#### PRD Workflow

**TRIGGER PHRASES**: When user says "PRD", "Product Requirements", "feature development using a PRD", or "I request this feature development using a PRD", IMMEDIATELY stop and follow the mandatory PRD workflow below.

**Check First**: Before ANY PRD work, look for `/.claude/tasks/` directory and follow this structured workflow.

**Step 1: PRD Creation**

- Use `/.claude/tasks/1_create-prd.md` to create new PRDs  
- Ask clarifying questions before writing the PRD  
- Create PRD folder: `/.claude/tasks/1_backlog/001-[feature-name]/`  
- Save PRD file as: `/.claude/tasks/1_backlog/001-[feature-name]/prd-001-[feature-name].md`  
- Use sequential numbering (001, 002, 003...) for new PRDs  
- Get user approval before proceeding to task generation

**PRD Workflow Validation Checklist**:

- [ ] Found /.claude/tasks/1\_create-prd.md template  
- [ ] Created numbered PRD folder in /.claude/tasks/1\_backlog/  
- [ ] Following 001-\[feature-name\] folder naming convention  
- [ ] Following prd-001-\[feature-name\].md file naming convention  
- [ ] Getting user approval before task generation  
- [ ] Not creating PRD in wrong location (like git/infrastructure/)

**Step 2: Task Generation**

- Use `/.claude/tasks/2_generate-tasks.md` to generate detailed task breakdowns  
- Include agent assignments for all parent tasks and subtasks  
- Save task file as: `/.claude/tasks/1_backlog/001-[feature-name]/tasks-prd-001-[feature-name].md`  
- All PRD-related files stay within the same numbered folder  
- Update `/.claude/tasks/project-status.md` to reflect new feature in backlog

**Step 3: Implementation Process**

- Use `/.claude/tasks/3_process-task-list.md` for implementation workflow  
- Move entire PRD folder through stages: `1_backlog/001-[feature-name]/` → `2_active/001-[feature-name]/` → `3_completed/001-[feature-name]/`  
- All implementation files (code, configs, scripts) go in the active PRD folder  
- Complete tasks one at a time with user approval  
- Maintain folder organization throughout the lifecycle

**Step 4: Alternative \- OBE (Overtaken by Events)**

- For PRDs that won't be implemented (cancelled, superseded, or deprioritized)  
- Move entire PRD folder to: `/.claude/tasks/0_obe/001-[feature-name]/`  
- Add `obe-reason.md` file explaining why the PRD was not implemented  
- Update `/.claude/tasks/project-status.md` to reflect OBE status

**PRD Selection Rules**:

If not explicitly told which PRD to use:

- Look for existing PRD folders in `/.claude/tasks/1_backlog/` with pattern `001-[feature-name]/`  
- Only show PRDs that don't have corresponding task files (`tasks-prd-*.md` in their folder)  
- **Always** ask user to confirm PRD folder name before proceeding  
- Provide numbered options for easy selection  
- Display both folder number and feature name for clarity

**OBE (Overtaken by Events) Management**:

- Move entire folder from any stage to `/.claude/tasks/0_obe/001-[feature-name]/`  
- Common OBE reasons: cancelled, superseded, deprioritized, requirements changed  
- Preserve original numbering when moving to OBE  
- Add `obe-reason.md` file documenting the decision rationale

#### Plan Adherence Protocol

**ZERO DEVIATION POLICY**: Claude must NEVER deviate from specified technology stacks, architectures, or implementation approaches without explicit user confirmation.

**Strict Execution Rules**:

1. **TECHNOLOGY STACK IS IMMUTABLE**: Use only the exact technologies, versions, and configurations specified in task files  
2. **NO SUBSTITUTIONS ALLOWED**: Never replace specified technologies with "easier" or "more practical" alternatives  
3. **IMMEDIATE ESCALATION**: Stop execution and ask user for guidance if plan cannot be followed exactly  
4. **CONFIRMATION REQUIRED**: Any deviation requires explicit user approval using the escalation template

**Mandatory Escalation Template**:

When Claude encounters issues requiring plan changes:

🛑 EXECUTION STOPPED \- GUIDANCE NEEDED

\*\*Issue\*\*: \[Specific problem encountered\]

\*\*Expected\*\*: \[What the plan specified\]

\*\*Actual\*\*: \[What actually happened\]

\*\*Impact\*\*: \[How this affects the plan\]

\*\*Options\*\*:

A) Continue with original plan (explain how)

B) Modify plan \- specify exact changes: \[detailed changes\]

C) Alternative approach \- explain why: \[justification\]

\*\*My Recommendation\*\*: \[Claude's analysis\]

Please respond with A, B, or C to proceed.

**Plan Adherence Validation**:

Before starting ANY task, Claude must:

- [ ] Confirm exact technology stack specified  
- [ ] Verify all prerequisites are available  
- [ ] Identify any potential conflicts or blockers  
- [ ] Get user confirmation that plan is understood correctly

#### Task File Workflow

**MANDATE**: Every task MUST create a file in `/.claude/tasks/2_active/[task-name].md` before starting work.

**Critical Workflow**:

1. **STEP 1**: User requests task  
2. **STEP 2**: Claude IMMEDIATELY creates task file in `/.claude/tasks/2_active/`  
3. **STEP 3**: Claude begins work on task  
4. **STEP 4**: Claude updates task file as subtasks complete  
5. **STEP 5**: Claude moves completed task to `/.claude/tasks/3_completed/`

**Before Starting Any Task**:

\# Create task file using template

cp .claude/templates/simple-task-template.md .claude/tasks/2\_active/\[task-name\].md

\# Fill in task details BEFORE starting work

**During Task Execution**:

- Update task file checkboxes as subtasks complete  
- Add notes about discoveries or issues  
- Never work without corresponding task file

**After Task Completion**:

\# Move completed task to archive

mv .claude/tasks/2\_active/\[task-name\].md .claude/tasks/3\_completed/

**NO EXCEPTIONS**: All work must be tracked in task files. TodoWrite tool is ONLY for session-level tracking, NOT task persistence.

#### Project Discovery Rule

**PROJECT SETUP REQUIRES DISCOVERY**: Before setting up any Claude Agent System or creating PROJECT\_CONTEXT.md files, you MUST conduct thorough project discovery.

**Ask about**: Project type/purpose, technical stack/architecture, team/workflow context, project constraints/requirements, and agent system goals.

**Reference**: See `.claude/docs/project-discovery-questions.md` for complete question checklist.

**NO EXCEPTIONS**: Never create PROJECT\_CONTEXT.md or invoke garden-guide agent for setup without first gathering this essential project information through direct questioning.

## Agent Selection Framework

### Decision Tree for Agent Selection

When receiving a task, use this decision framework:

1. **Task Domain Analysis**  
     
   - Infrastructure/deployment → `platform-engineer`  
   - Security/vulnerability → `cybersecurity-engineer`  
   - CI/CD/pipelines → `cicd-engineer`  
   - Code/architecture → `software-engineer`  
   - Data/ML/analytics → `data-scientist`  
   - Product vision/discovery → `product-visionary`  
   - Feature roadmap/architecture → `feature-architect`  
   - Product/requirements → `product-manager`  
   - User experience/design → `ux-ui-designer`  
   - Claude system setup/guidance → `garden-guide`  
   - Project knowledge/questions → `project-navigator`

   

2. **Scope Boundaries**  
     
   - Cross-domain tasks → Break into domain-specific subtasks  
   - Pure implementation → Use appropriate specialist  
   - Research/analysis → Use domain expert agent

### Agent Selection Criteria

| Task Type | Primary Agent | Secondary Options |
| :---- | :---- | :---- |
| Infrastructure setup | platform-engineer | software-engineer |
| Security analysis | cybersecurity-engineer | platform-engineer |
| Pipeline configuration | cicd-engineer | platform-engineer |
| Code implementation | software-engineer | \- |
| Data analysis | data-scientist | software-engineer |
| Product vision creation | product-visionary | \- |
| Feature roadmap planning | feature-architect | product-manager |
| Feature planning (PRDs) | product-manager | ux-ui-designer |
| Product strategy | product-manager | \- |
| UI/UX design | ux-ui-designer | product-manager |
| System setup/guidance | garden-guide | \- |
| Project knowledge/questions | project-navigator | \- |

## Context Management Protocols

### Pre-Agent Invocation

1. **Context Preparation**  
     
   \- Gather only essential files/information  
     
   \- Summarize business context in 2-3 sentences  
     
   \- Identify specific deliverables needed  
     
   \- Set clear success criteria  
     
2. **Context Size Validation**  
     
   \- Estimate context usage before delegation  
     
   \- If \> 30% for preparation, break task into smaller pieces  
     
   \- Prioritize most critical information first  
     
3. **Agent Briefing Format**  
     
   Task: \[Clear, specific task description\]  
     
   Context: \[Minimal essential context\]  
     
   Constraints: \[Technical, business, time constraints\]  
     
   Expected Output: \[Specific deliverables\]  
     
   Success Criteria: \[How to measure completion\]

### During Agent Execution

1. **Monitoring Guidelines**  
     
   - Agents should complete tasks within 40% context window  
   - Escalate if agent requests excessive additional context  
   - Allow agents to ask clarifying questions

   

2. **Intervention Triggers**  
     
   - Agent exceeds context budget  
   - Agent goes out of scope  
   - Agent requests information outside domain

### Post-Agent Integration

1. **Output Processing**  
     
   - Validate deliverables against success criteria  
   - Integrate recommendations into main workflow  
   - Document any follow-up actions needed

   

2. **Handoff Protocol**  
     
   - Agent provides clear next steps  
   - Main agent acknowledges completion  
   - File/implement changes as appropriate

## Standardized Agent Invocation Patterns

Use structured briefings with: Task, Context, Constraints, **TDD Requirements** (for code tasks), Expected Deliverables, and Success Criteria.

### TDD Requirements Template (Include in ALL Code Implementation Tasks)

When invoking agents for code implementation, testing, or bug fixes, ALWAYS include this section:

\#\# TDD Requirements (MANDATORY)

You MUST follow Test-Driven Development workflow:

\#\#\# Step 1: Write Failing Test First

\- \*\*Test File\*\*: \`tests/\[unit|integration\]/test\_\[feature\_name\].py\`

\- \*\*Run Command\*\*: \`pytest tests/\[path\]/test\_\[feature\_name\].py \-v \-s\`

\- \*\*Expected Result\*\*: Test FAILS (reproducing the bug or showing feature not implemented)

\- \*\*Report Back\*\*: Paste test failure output showing the exact error

\#\#\# Step 2: Implement Minimal Code

\- \*\*File to Modify\*\*: \`src/\[module\]/\[file\].py\`

\- \*\*Approach\*\*: Write smallest code change to make test pass

\- \*\*No Gold Plating\*\*: Only implement what's needed for test to pass

\#\#\# Step 3: Verify Unit Tests Pass

\- \*\*Run Command\*\*: \`pytest tests/\[path\]/test\_\[feature\_name\].py \-v \--cov=src/\[module\]\`

\- \*\*Expected Result\*\*: All tests PASS ✅

\- \*\*Coverage Target\*\*: \>80% for modified code

\- \*\*Report Back\*\*: Paste test success output with coverage percentage

\#\#\# Step 4: Run Integration/E2E Test

\- \*\*Command\*\*: \[Specify exact API call, demo script, or CLI command\]

\- \*\*Expected Behavior\*\*: \[Describe specific success criteria\]

\- \*\*Verification\*\*: \[What to check in response/output\]

\- \*\*Report Back\*\*: Paste actual command output showing success

\#\#\# Step 5: Commit Only If All Tests Pass

\- \*\*Pre-Commit Check\*\*: All unit tests ✅, integration test ✅

\- \*\*Commit Command\*\*: \`git add tests/ src/ && git commit \-m "\[descriptive message\]"\`

\- \*\*Report Back\*\*: Commit hash and verification that tests are included

\#\#\# Step 6: Report TDD Completion

Provide summary:

\- \[ \] Test file created: \[path\]

\- \[ \] Initial test run: FAIL (expected)

\- \[ \] Code implemented: \[files modified\]

\- \[ \] Unit tests: PASS ✅ (coverage: X%)

\- \[ \] Integration test: PASS ✅

\- \[ \] Committed: \[hash\]

\*\*DO NOT REPORT TASK COMPLETE UNTIL ALL 6 STEPS DONE WITH EVIDENCE\*\*

**Example TDD Briefing**:

See `.claude/docs/agent-invocation-examples.md` for complete examples including TDD requirements.

**Reference**: See `.claude/docs/agent-invocation-examples.md` for detailed templates and examples.

## Error Handling and Escalation

### Agent Failure Scenarios

1. **Context Overflow**  
     
   - **Trigger**: Agent requests \> 40% context  
   - **Action**: Break task into smaller components  
   - **Fallback**: Handle critical parts directly

   

2. **Scope Creep**  
     
   - **Trigger**: Agent goes outside defined boundaries  
   - **Action**: Redirect to appropriate scope  
   - **Fallback**: Reassign to correct agent

   

3. **Incomplete Deliverables**  
     
   - **Trigger**: Agent doesn't meet success criteria  
   - **Action**: Request specific missing components  
   - **Fallback**: Complete remaining work directly

   

4. **Technical Limitations**  
     
   - **Trigger**: Agent lacks required domain knowledge  
   - **Action**: Provide additional context or research  
   - **Fallback**: Use general-purpose approach

### Escalation Matrix

| Issue Type | First Response | Escalation | Final Fallback |
| :---- | :---- | :---- | :---- |
| Context overflow | Break into subtasks | Use general-purpose agent | Handle directly |
| Scope creep | Redirect agent | Switch to correct agent | Handle directly |
| Quality issues | Request revision | Provide additional context | Complete directly |
| Agent unavailable | Wait/retry | Use backup agent | Handle directly |

## Delegation Guidelines

### Agent Task Assignment Matrix

| Task Category | Must Delegate? | Agent Type |
| :---- | :---- | :---- |
| Code implementation | ✅ YES | tactical-software-engineer |
| Architecture design | ✅ YES | strategic-software-engineer |
| Infrastructure work | ✅ YES | tactical-platform-engineer |
| Platform strategy | ✅ YES | strategic-platform-engineer |
| Security implementation | ✅ YES | tactical-cybersecurity |
| Security strategy | ✅ YES | strategic-cybersecurity |
| CI/CD pipelines | ✅ YES | tactical-cicd |
| DevOps strategy | ✅ YES | strategic-cicd |
| UI/UX design | ✅ YES | tactical-ux-ui-designer |
| Design systems | ✅ YES | strategic-ux-ui-designer |
| Data analysis | ✅ YES | data-scientist |
| Product vision creation | ✅ YES | strategic-product-visionary |
| Feature roadmap planning | ✅ YES | strategic-feature-architect |
| Feature planning (PRDs) | ✅ YES | tactical-product-manager |
| Product strategy | ✅ YES | strategic-product-manager |
| SRE work | ✅ YES | tactical-sre |
| Reliability strategy | ✅ YES | strategic-sre |
| System setup help | ✅ YES | garden-guide |
| Project questions | ✅ YES | project-navigator |

**POLICY**: Main agent delegates ALL tasks to specialized subagents to ensure expert-level quality, maintain context efficiency, and leverage domain expertise for every piece of work.

### Communication Patterns

**Main agent should be transparent about delegation:**

1. **Immediate Delegation (preferred)**  
     
   "I'll have our \[tactical/strategic\]-\[agent-type\] agent handle this."  
     
   \[Invokes agent immediately\]  
     
2. **Task Handoff with Context**  
     
   "This is a \[domain\] task, so I'm delegating to our \[agent-type\] agent  
     
   who specializes in \[expertise area\]."  
     
3. **Result Integration**  
     
   "The \[agent-type\] agent has completed the analysis. Here's what they found..."  
     
   \[Present agent's work\]

**Keep delegation statements brief** \- users don't need lengthy explanations about why delegation is happening, as it should be the expected default behavior.

## Project Context Integration

### Automatic Context Loading

Before any agent invocation, the main Claude agent must:

1. **Load Project Context**  
     
   \# Auto-detect and load PROJECT\_CONTEXT.md from repository root  
     
   if \[ \-f "PROJECT\_CONTEXT.md" \]; then  
     
       PROJECT\_CONTEXT=$(cat PROJECT\_CONTEXT.md)  
     
   fi  
     
2. **Check Active Tasks**  
     
   \# Load related 2\_active tasks from /.claude/tasks/2\_active/  
     
   ACTIVE\_TASKS=$(find /.claude/tasks/2\_active/ \-name "\*.md" | grep \-i \[task-keywords\])  
     
3. **Load Session Context**  
     
   \# Retrieve session continuity information  
     
   SESSION\_CONTEXT=$(cat /.claude/context/session-history/\[latest\].md)

### Enhanced Agent Briefing

When invoking specialized agents, include:

\#\# Project Context

\[Auto-loaded from PROJECT\_CONTEXT.md\]

\#\# Related Active Tasks

\[List of relevant ongoing tasks\]

\#\# Session Continuity

\[Previous decisions and context from current session\]

\#\# Current Task Assignment

\[Specific task being delegated\]

## Task Management Integration

### Pre-Task Validation

Before creating or assigning tasks:

1. **Check Dependencies**  
     
   - Review active tasks for dependencies  
   - Identify potential conflicts  
   - Ensure prerequisite completion

   

2. **Context Preparation**  
     
   - Gather minimal essential context  
   - Prepare agent-specific briefing  
   - Set clear success criteria

   

3. **Resource Allocation**  
     
   - Verify agent availability  
   - Estimate context usage  
   - Plan for potential escalation

### Task Persistence Rules

1. **MANDATORY Task File Creation**  
     
   - **EVERY task MUST create a file** in `/.claude/tasks/2_active/[task-name].md`  
   - **BEFORE starting any work**, create the task file with:  
     - Clear objective and context  
     - Specific subtasks with checkboxes  
     - Success criteria  
     - Commands to run (if applicable)  
   - **NO EXCEPTIONS** \- Use TodoWrite tool only for session tracking, NOT task persistence

   

2. **Task File Lifecycle Management**  
     
   - **Create**: Always create task file before work begins  
   - **Update**: Update checkboxes and progress as work completes  
   - **Complete**: Move completed tasks to `/.claude/tasks/3_completed/` directory  
   - **Link**: Reference parent/child tasks when applicable

   

3. **Session Continuity**  
     
   - Save session state before agent handoff  
   - Update task progress after agent completion  
   - Maintain context carryover between sessions

   

4. **Quality Gates**  
     
   - Validate deliverables against success criteria  
   - Update task status appropriately  
   - Document lessons learned

## Testing and Implementation

**Reference**: See `.claude/docs/testing-and-implementation.md` for repository setup, integration commands, and testing protocols.

## Development Best Practices

### GitLab CI/CD Specific Constraints

**CRITICAL**: When writing `.gitlab-ci.yml` files or any GitLab CI/CD configurations:

1. **Echo Statement Formatting**  
     
   - ❌ **NEVER** use colons (`:`) to separate labels from variables in echo statements  
   - ✅ **ALWAYS** use double dashes (`--`) instead

   

   **Examples**:

   

   \# ❌ WRONG \- GitLab parses colons as YAML syntax

   

   \- echo "Job: ${CI\_JOB\_NAME}"

   

   \- echo "Branch: ${CI\_COMMIT\_REF\_NAME}"

   

   \# ✅ CORRECT \- Use double dashes instead

   

   \- echo "Job--${CI\_JOB\_NAME}"

   

   \- echo "Branch--${CI\_COMMIT\_REF\_NAME}"

   

2. **Multi-line Shell Scripts**  
     
   - Use YAML literal block scalar (`|`) for multi-line if/else statements  
   - Never use inline YAML syntax for shell conditionals

   

   **Example**:

   

   script:

   

     \- some\_command || EXIT\_CODE=$?

   

     \- |

   

       if \[ \-n "${EXIT\_CODE}" \]; then

   

         echo "Error occurred"

   

         exit ${EXIT\_CODE}

   

       fi

   

3. **YAML Anchors for before\_script**  
     
   - Anchor must reference array directly, not a hash with `before_script` key  
   - Use `before_script: *anchor_name` not `<<: *anchor_name`

   

   **Example**:

   

   \# ✅ CORRECT

   

   .common\_before\_script: \&common\_before\_script

   

     \- echo "Setup step 1"

   

     \- echo "Setup step 2"

   

   job:

   

     before\_script: \*common\_before\_script

**Why This Matters**: GitLab's YAML parser interprets colons as key-value separators, causing validation errors. Using `--` prevents parsing issues while maintaining readability.

### Test-Driven Development (TDD) Protocol

**MANDATORY for ALL code implementation tasks \- NO EXCEPTIONS**

#### TDD Workflow (Required Sequence)

Every specialized agent performing code implementation MUST follow this exact sequence:

1. **Write Failing Test First**  
     
   - Create test file before any implementation code  
   - Test must reproduce the requirement or bug  
   - Run test, verify it fails with clear error message  
   - Report test failure output as evidence

   

2. **Implement Minimal Code**  
     
   - Write smallest amount of code to make test pass  
   - No premature optimization  
   - No "extra features" beyond requirement  
   - Focus on making the test green

   

3. **Verify Test Passes**  
     
   - Run test suite, confirm all tests pass  
   - Fix any failures before proceeding  
   - No "it should work" claims without test evidence  
   - Report test success output as evidence

   

4. **Refactor If Needed**  
     
   - Clean up code while keeping tests green  
   - Improve readability, remove duplication  
   - Re-run tests after each refactor  
   - Ensure tests still pass after refactoring

   

5. **Run Integration/E2E Tests**  
     
   - Verify feature works in actual system  
   - Test via API call, CLI command, or demo script  
   - Confirm user-facing behavior is correct  
   - Report integration test success

   

6. **Commit Only If All Pass**  
     
   - Unit tests: PASS ✅  
   - Integration tests: PASS ✅  
   - E2E verification: PASS ✅  
   - Only then execute: `git commit`

#### Enforcement Rules

**Main Agent Responsibilities:**

- Include TDD workflow in every agent briefing for code tasks  
- Require agents to report test results before claiming success  
- Reject agent deliverables that skip TDD steps  
- Never accept "this should work" without test evidence  
- Verify test files exist and are committed with code changes

**Specialized Agent Responsibilities:**

- Report each TDD step completion with evidence (test output, command results)  
- Include test file paths in deliverables  
- Show test pass/fail status before claiming task complete  
- Create regression tests for bugs before fixing them  
- Document test coverage percentage

**Violation Consequences:**

- Agent work is rejected and must be redone with proper TDD  
- Task is not marked complete until tests exist and pass  
- No commits are made until full TDD cycle completes  
- Main agent must restart the task with TDD requirements

#### TDD Exemptions (Rare)

Only these scenarios can skip TDD (must be explicitly stated in task briefing):

- Documentation-only changes (README, markdown files, comments)  
- Configuration changes with no logic (JSON, YAML, environment files)  
- Experimental spike/prototype (must be marked as temporary and include follow-up task for tests)  
- Emergency hotfix (must include follow-up task to add tests within 24 hours)

**Default assumption: TDD is REQUIRED unless explicitly exempted by main agent**

#### Test Quality Standards

**Unit Tests:**

- Minimum 80% code coverage for new code  
- Test edge cases (null, empty, invalid inputs)  
- Test error conditions and exception handling  
- Use descriptive test names (test\_feature\_scenario\_expectedResult)  
- Use fixtures for test data setup

**Integration Tests:**

- Test complete feature workflows end-to-end  
- Use realistic data matching production scenarios  
- Verify API responses, database state, file outputs  
- Test error handling and rollback behavior

**Regression Tests:**

- Every bug fix MUST include regression test  
- Test reproduces the original bug before fix  
- Test passes after fix is applied  
- Test prevents bug from recurring

#### TDD Success Metrics

Track these metrics in agent session history:

- Test coverage percentage (target: \>80%)  
- Number of tests written  
- Test execution time  
- Integration test pass/fail status  
- TDD workflow adherence (all 6 steps completed)

### Task Management Rules

- Mark tasks completed immediately after finishing  
- Never batch completions  
- Add discovered subtasks during development  
- Break down complex tasks as scope becomes clear

**Reference**: See `.claude/docs/task-management-examples.md` for detailed examples.

### Documentation Maintenance

**README updates required**: New features, dependency changes, setup modifications, configuration changes **Code documentation required**: New modules/functions, API changes, business logic, complex algorithms

### Code Quality and Clarity

**Comment prefixes**: `REASON:` (approach), `WHY:` (business logic), `NOTE:` (details), `HACK:` (temporary), `TODO:` (future)

**Reference**: See `.claude/docs/code-quality-examples.md` for detailed examples.

### Confirmation and Safety Protocols

**Never Assume**: Ask questions when unclear, request clarification before architectural decisions, confirm business logic understanding **File Safety**: Confirm paths, verify module existence, never delete/overwrite without explicit instruction

**Pre-Change Checklist**: Confirm file paths, verify dependencies, understand requirements, know what to preserve, establish success criteria

**Reference**: See `.claude/docs/code-quality-examples.md` for safety protocol examples.

### Quality Assurance

**Before**: Confirm scope, verify paths/modules, understand existing code, clarify requirements, establish criteria, **write failing test** **During**: Add subtasks immediately, comment complex logic, update docs, mark completions, **keep tests green** **After**: Update README, verify comments, confirm subtasks completed, validate integrations, **all tests pass**

#### Test Requirements (Mandatory Gate)

Every task involving code changes MUST satisfy these test requirements before marking complete:

- [ ] **Unit tests exist** with \>80% coverage of modified code  
- [ ] **Unit tests pass** \- run `pytest tests/unit/... -v` successfully  
- [ ] **Integration test exists** demonstrating feature works end-to-end  
- [ ] **Integration test passes** \- verified via API call, demo script, or CLI  
- [ ] **Test output documented** in agent session history or commit message  
- [ ] **Test files committed** with code changes in same commit

**NO EXCEPTIONS** \- Code without passing tests is incomplete and task cannot be marked done.

**Quality Gate Enforcement**:

- Main agent verifies test files exist before accepting agent deliverables  
- Agents must provide test execution output as proof  
- Tasks remain "in progress" until all test requirements met  
- Commits are rejected if tests not included

This framework ensures consistent, efficient, and high-quality agent orchestration while maintaining clear boundaries, expectations, comprehensive documentation, and full workflow continuity across sessions.  