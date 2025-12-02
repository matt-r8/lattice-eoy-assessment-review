# Generating a Task List from a PRD

## Goal

To guide an AI assistant in creating a detailed, step-by-step task list in Markdown format based on an existing Product Requirements Document (PRD). The task list should guide a developer through implementation.

## Output

- **Format:** Markdown (`.md`)
- **Location:** `/.claude/tasks/1_backlog/001-[feature-name]/` (within the same PRD folder)
- **Filename:** `tasks-prd-001-[feature-name].md` (matching the PRD numbering)

## Process

1.  **Receive PRD Reference:** The user points the AI to a specific PRD file
2.  **Analyze PRD:** The AI reads and analyzes the functional requirements, user stories, and other sections of the specified PRD.
3.  **Assess Current State:** Review the existing codebase to understand existing infrastructure, architectural patterns and conventions. Also, identify any existing components or features that already exist and could be relevant to the PRD requirements. Then, identify existing related files, components, and utilities that can be leveraged or need modification.
4.  **Phase 1: Generate Parent Tasks:** Based on the PRD analysis and current state assessment, create the file and generate the main, high-level tasks required to implement the feature. Use your judgement on how many high-level tasks to use. It's likely to be about 3-7 high-level tasks. 
5. **Inform the user:** Present these tasks to the user in the specified format (without sub-tasks yet) For example, say "I have generated the high-level tasks based on the PRD. Ready to generate the sub-tasks? Respond with 'Go' to proceed." . 
6.  **Wait for Confirmation:** Pause and wait for the user to respond with "Go".
7.  **Phase 2: Generate Sub-Tasks:** Once the user confirms, break down each parent task into smaller, actionable sub-tasks necessary to complete the parent task. Ensure sub-tasks logically follow from the parent task, cover the implementation details implied by the PRD, and consider existing codebase patterns where relevant without being constrained by them.
8.  **Assign Agents:** For each parent task and subtask, assign the most appropriate agent based on the task domain (see Agent Assignment Guidelines below). This keeps context windows small by routing tasks to specialized agents.
9.  **Identify Relevant Files:** Based on the tasks and PRD, identify potential files that will need to be created or modified. List these under the `Relevant Files` section, including corresponding test files if applicable.
10. **Generate Final Output:** Combine the parent tasks, sub-tasks, agent assignments, relevant files, and notes into the final Markdown structure.
11.  **Save Task List:** Save the generated document in the same PRD folder `/.claude/tasks/1_backlog/001-[feature-name]/` with the filename `tasks-prd-001-[feature-name].md`, matching the PRD numbering scheme.
12.  **Update Project Status:** Update `/.claude/tasks/project-status.md` to reflect the new feature in backlog.

## Output Format

The generated task list _must_ follow this structure:

```markdown
## Relevant Files

- `path/to/potential/file1.ts` - Brief description of why this file is relevant (e.g., Contains the main component for this feature).
- `path/to/file1.test.ts` - Unit tests for `file1.ts`.
- `path/to/another/file.tsx` - Brief description (e.g., API route handler for data submission).
- `path/to/another/file.test.tsx` - Unit tests for `another/file.tsx`.
- `lib/utils/helpers.ts` - Brief description (e.g., Utility functions needed for calculations).
- `lib/utils/helpers.test.ts` - Unit tests for `helpers.ts`.

### Notes

- Unit tests should typically be placed alongside the code files they are testing (e.g., `MyComponent.tsx` and `MyComponent.test.tsx` in the same directory).
- Use `npx jest [optional/path/to/test/file]` to run tests. Running without a path executes all tests found by the Jest configuration.

## Tasks

- [ ] 1.0 Parent Task Title
  - **Assigned Agent**: [agent-name]
  - **Context**: [Brief explanation of why this agent]
  - [ ] 1.1 [Sub-task description 1.1]
    - **Assigned Agent**: [agent-name]
    - **Context**: [Brief context]
  - [ ] 1.2 [Sub-task description 1.2]
    - **Assigned Agent**: [agent-name]
    - **Context**: [Brief context]
- [ ] 2.0 Parent Task Title
  - **Assigned Agent**: [agent-name]
  - **Context**: [Brief explanation]
  - [ ] 2.1 [Sub-task description 2.1]
    - **Assigned Agent**: [agent-name]
    - **Context**: [Brief context]
- [ ] 3.0 Parent Task Title
  - **Assigned Agent**: [agent-name]
  - **Context**: [Brief explanation]
```

## Agent Assignment Guidelines

### Available Agents

Based on the agents available in `/.claude/agents/`, assign tasks to the most appropriate specialist:

- **software-engineer**: Code implementation, APIs, business logic, application features
- **platform-engineer**: Infrastructure, databases, deployment, DevOps, system architecture
- **cybersecurity-engineer**: Security implementation, audits, compliance, authentication, authorization
- **data-scientist**: Analytics, metrics collection, data processing, reporting, ML features
- **product-manager**: Requirements clarification, user stories, acceptance criteria, feature planning
- **ux-ui-designer**: User interface design, user experience flows, design systems, frontend styling
- **cicd-engineer**: Build pipelines, deployment automation, testing infrastructure, CI/CD workflows
- **project-navigator**: Project understanding, documentation, knowledge management, cross-cutting concerns
- **solutions-guide**: Claude system setup, agent orchestration guidance, workflow optimization

### Assignment Principles

1. **Expertise Matching**: Match task complexity and domain to agent specialization
2. **Context Efficiency**: Assign to most specialized agent to keep context windows small
3. **Single Responsibility**: Each subtask should have clear agent ownership
4. **Logical Grouping**: Related subtasks can share the same agent when appropriate
5. **Avoid Overloading**: Distribute tasks across agents (max 8-10 tasks per agent per feature)

### Assignment Examples

- **Database schema design** → platform-engineer
- **API endpoint implementation** → software-engineer
- **Security audit requirements** → cybersecurity-engineer
- **User interface components** → ux-ui-designer
- **Analytics dashboard** → data-scientist
- **Deployment pipeline** → cicd-engineer
- **Feature requirements review** → product-manager

## Interaction Model

The process explicitly requires a pause after generating parent tasks to get user confirmation ("Go") before proceeding to generate the detailed sub-tasks. This ensures the high-level plan aligns with user expectations before diving into details.

## Target Audience

Assume the primary reader of the task list is a **junior developer** who will implement the feature with awareness of the existing codebase context.