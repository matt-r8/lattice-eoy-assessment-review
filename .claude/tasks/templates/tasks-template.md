# Task List: [Feature Name]

## 🛑 MANDATORY EXECUTION RULES
- **ZERO DEVIATIONS** without explicit user confirmation
- **TECHNOLOGY STACK LOCKED** as specified below
- **STOP AND ESCALATE** if plan cannot be executed exactly as written

## Technology Stack (IMMUTABLE)
```yaml
primary_technology: "[Exact technology/version - NO SUBSTITUTIONS]"
runtime: "[Exact runtime - NO ALTERNATIVES]"
architecture: "[Exact architecture approach - LOCKED]"
networking: "[Exact networking configuration - FIXED]"
deployment_method: "[Exact deployment approach - MANDATORY]"
```

## Plan Adherence Checklist
Before starting, Claude must verify:
- [ ] All specified technologies are available and functional
- [ ] No port conflicts or missing prerequisites
- [ ] Architecture can be implemented exactly as specified
- [ ] User explicitly confirms plan understanding is correct

Generated from: `prd-[feature-name].md`

## Relevant Files

- `path/to/file1.ts` - Brief description of why this file is relevant
- `path/to/file1.test.ts` - Unit tests for `file1.ts`
- `path/to/file2.tsx` - Brief description
- `path/to/file2.test.tsx` - Unit tests for `file2.tsx`

### Notes

- Unit tests should be placed alongside the code files they are testing
- Use appropriate test command for the project (e.g., `npm test`, `pytest`, etc.)
- Follow existing project patterns and conventions

## Tasks

- [ ] 1.0 [Parent Task Title]
  - **Assigned Agent**: [agent-name]
  - **Context**: [Brief context for why this agent]
  - [ ] 1.1 [Sub-task description]
    - **Assigned Agent**: [agent-name]
    - **Context**: [Brief context]
  - [ ] 1.2 [Sub-task description]
    - **Assigned Agent**: [agent-name]
    - **Context**: [Brief context]

- [ ] 2.0 [Parent Task Title]
  - **Assigned Agent**: [agent-name]
  - **Context**: [Brief context for why this agent]
  - [ ] 2.1 [Sub-task description]
    - **Assigned Agent**: [agent-name]
    - **Context**: [Brief context]
  - [ ] 2.2 [Sub-task description]
    - **Assigned Agent**: [agent-name]
    - **Context**: [Brief context]

- [ ] 3.0 [Parent Task Title]
  - **Assigned Agent**: [agent-name]
  - **Context**: [Brief context for why this agent]
  - [ ] 3.1 [Sub-task description]
    - **Assigned Agent**: [agent-name]
    - **Context**: [Brief context]

## Agent Assignment Guidelines

### Available Agents
- **software-engineer**: Code implementation, APIs, business logic
- **platform-engineer**: Infrastructure, databases, deployment, DevOps
- **cybersecurity-engineer**: Security implementation, audits, compliance
- **data-scientist**: Analytics, metrics, data processing, ML features
- **product-manager**: Requirements clarification, user stories, acceptance criteria
- **ux-ui-designer**: User interface, user experience, design systems
- **cicd-engineer**: Build pipelines, deployment automation, testing infrastructure
- **project-navigator**: Project understanding, documentation, knowledge management
- **solutions-guide**: Claude system setup, agent orchestration guidance

### Assignment Principles
- **Keep context small**: Assign tasks to most specialized agent
- **Single responsibility**: Each subtask should have clear agent ownership
- **Logical grouping**: Related subtasks can share the same agent
- **Expertise matching**: Match task complexity to agent specialization

## Progress Tracking

- Mark subtasks complete `[x]` immediately upon finishing
- Mark parent tasks complete only when ALL subtasks are `[x]`
- Add new subtasks as discovered during implementation
- Update agent assignments if task scope changes

---

**Created**: [Date]
**Status**: [Backlog/Active/Completed]
**Total Parent Tasks**: [Number]
**Total Subtasks**: [Number]