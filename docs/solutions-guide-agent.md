# Solutions Guide Agent Documentation

The Solutions Guide is your dedicated coach for setting up and optimizing the Claude Agent System in any project.
```
I'm setting up a new project with the Claude Agent System. Please use the solutions-guide agent to help me get started step-by-step.
```

## Overview

The Solutions Guide agent serves as your proactive companion throughout the entire Claude Agent System journey - from initial project setup through daily productive usage. It acts as both a step-by-step setup wizard and an ongoing optimization coach.

## When to Use Solutions Guide

### Always Use For:
- ✅ **New Project Setup**: First-time Claude Agent System installation
- ✅ **System Optimization**: Improving existing Claude Agent configurations
- ✅ **Workflow Guidance**: Selecting and customizing workflow templates
- ✅ **Best Practices**: Learning effective patterns and conventions
- ✅ **Troubleshooting**: Resolving setup or configuration issues

### Don't Use For:
- ❌ **Project-Specific Questions**: Use `project-navigator` instead
- ❌ **Code Implementation**: Use `software-engineer` instead
- ❌ **Infrastructure Setup**: Use `platform-engineer` instead

## Key Capabilities

### 🚀 Proactive Coaching (80% of Interactions)
The Solutions Guide anticipates your needs and proactively suggests improvements:

```
☀️ DAILY COACHING CHECK-IN
How's your Claude Agent System experience going?

PROACTIVE OBSERVATIONS:
- I notice you've been using software-engineer frequently - here's how to optimize that pattern
- Your PROJECT_CONTEXT.md could benefit from adding performance requirements section
- Based on your recent tasks, consider trying the Feature Development Workflow

TODAY'S OPTIMIZATION SUGGESTION:
Add error handling patterns to your project context for better agent guidance
```

### 🔍 Reactive Support (20% of Interactions)
When you have specific questions or issues:

```
Q: "My agents don't seem to understand my project well"
A: Let me analyze your PROJECT_CONTEXT.md and provide specific improvements...

IMMEDIATE ACTIONS:
1. Review current PROJECT_CONTEXT.md completeness
2. Identify missing critical sections
3. Provide enhanced template with your project specifics
4. Test agent understanding with sample tasks
```

## Setup Workflows

### Phase 1: Initial Assessment
```
🔍 ASSESSMENT PHASE

Let me help you set up the Claude Agent System for your project!

DISCOVERY QUESTIONS:
1. What type of project are you working on? (web app, API, mobile, etc.)
2. What's your primary tech stack?
3. Are you working solo or with a team?
4. Have you used the Claude Agent System before?
5. What are your main development challenges?

Based on your answers, I'll create a personalized setup plan.
```

### Phase 2: Foundation Setup
```
🏗️ FOUNDATION PHASE

Perfect! Based on your [project type] project, here's your setup plan:

IMMEDIATE ACTIONS:
1. Create .claude directory structure
   └── Command: mkdir -p .claude/{tasks/{active,completed,templates},context,tests}

2. Copy agent templates to your project
   └── Command: cp .claude-agents/templates/* .claude/templates/

3. Set up initial PROJECT_CONTEXT.md
   └── I'll guide you through each section step-by-step

Let's start with step 1...
```

### Phase 3: Context Optimization
```
📝 CONTEXT OPTIMIZATION PHASE

Now let's create your PROJECT_CONTEXT.md - this is crucial for agent effectiveness!

SMART RECOMMENDATIONS FOR YOUR [PROJECT TYPE]:
✅ Focus on these critical sections:
   - Tech stack: [Detected: React, Node.js, PostgreSQL]
   - Architecture: [Recommended: Component patterns section]
   - Business domain: [Your e-commerce platform needs payment flow details]

❌ Skip these optional sections for now:
   - Compliance (add later if needed)
   - Advanced monitoring (start simple)

Let me help you fill out each section with project-specific guidance...
```

### Phase 4: Workflow Integration
```
🔄 WORKFLOW INTEGRATION PHASE

Excellent! Now let's establish your productive workflows:

RECOMMENDED STARTER WORKFLOW:
Based on your project, I suggest the "Feature Development Workflow":
1. Requirements (product-manager agent)
2. Technical design (software-engineer agent)
3. Implementation (software-engineer agent)
4. Testing (software-engineer agent)

FIRST TASK SUGGESTION:
"Implement user authentication using the Feature Development Workflow"

This will test your entire agent system and establish good patterns.
```

## Optimization Guidance

### PROJECT_CONTEXT.md Optimization

#### Common Issues and Solutions
```
ISSUE: "Agents don't understand business logic"
SOLUTION: Enhance business context section
SPECIFIC ACTIONS:
- Add domain model explanation
- Include key business rules
- Document user journey flows
- Explain industry-specific terminology
```

```
ISSUE: "Agents suggest patterns that don't fit"
SOLUTION: Strengthen conventions section
SPECIFIC ACTIONS:
- Document coding standards with examples
- Specify preferred libraries and tools
- Include anti-patterns to avoid
- Add team decision history
```

```
ISSUE: "Tasks take too much context"
SOLUTION: Improve scope boundaries
SPECIFIC ACTIONS:
- Break down large features into smaller tasks
- Define clear component boundaries
- Establish interface contracts
- Document modular architecture
```

### Workflow Template Customization

#### Selecting the Right Template
```
PROJECT TYPE → RECOMMENDED WORKFLOWS

E-commerce Platform:
✅ Feature Development (new product features)
✅ Security Audit (payment processing)
✅ Performance Optimization (high traffic)

SaaS Application:
✅ Feature Development (user features)
✅ Data Analysis (usage analytics)
✅ Infrastructure Scaling (growth)

API Service:
✅ Bug Fix (service reliability)
✅ Security Audit (data protection)
✅ Performance Optimization (response times)
```

#### Template Customization Guide
```
CUSTOMIZATION CHECKLIST:

□ Adjust agent assignments based on your team skills
□ Modify task breakdown for your project complexity
□ Add project-specific quality gates
□ Include your testing requirements
□ Adapt to your deployment process
□ Align with your review procedures
```

## Daily Usage Patterns

### Morning Routine
```
🌅 DAILY STARTUP ROUTINE

1. "Good morning! Let's review yesterday's progress and plan today's work."

SMART CHECK-IN:
✅ Active tasks status
✅ Completed work review
✅ Today's priorities
✅ Potential blockers
✅ Agent system optimizations

2. "Based on your current work, here are today's recommendations..."
```

### Throughout the Day
```
🔄 CONTINUOUS GUIDANCE

PROACTIVE INTERVENTIONS:
- When you struggle with agent selection
- When tasks seem too complex for context limits
- When patterns could be optimized
- When new best practices emerge

GENTLE COACHING:
"I notice you're manually breaking down tasks. Would you like me to show you the task template that automates this?"
```

### End of Day
```
🌙 DAILY WRAP-UP

1. "Let's review today's accomplishments and prepare for tomorrow."

REFLECTION PROMPTS:
✅ What worked well with the agent system today?
✅ What could be improved?
✅ What new patterns emerged?
✅ What should be prioritized tomorrow?

2. "Here's what I learned about your project today that will help future sessions..."
```

## Troubleshooting Guide

### Common Setup Problems

#### Problem: Directory Structure Issues
```
SYMPTOMS:
- "Cannot find .claude directory"
- "Templates not loading"

DIAGNOSIS STEPS:
1. Check if .claude directory exists: ls -la .claude
2. Verify directory permissions: ls -la .claude/
3. Confirm template files: ls .claude/templates/

SOLUTION:
mkdir -p .claude/{tasks/{active,completed,templates},context,tests}
cp .claude-agents/templates/* .claude/templates/
```

#### Problem: PROJECT_CONTEXT.md Not Loading
```
SYMPTOMS:
- "Agents don't understand project"
- "Context seems generic"

DIAGNOSIS STEPS:
1. File exists: ls PROJECT_CONTEXT.md
2. File readable: head PROJECT_CONTEXT.md
3. Content complete: wc -l PROJECT_CONTEXT.md

SOLUTION:
- Use solutions-guide to review and enhance content
- Validate against project-context-template
- Test with sample agent interaction
```

#### Problem: Agent Selection Confusion
```
SYMPTOMS:
- "Don't know which agent to use"
- "Agents going out of scope"

DIAGNOSIS STEPS:
1. Review CLAUDE.md decision tree
2. Check task complexity assessment
3. Validate agent scope boundaries

SOLUTION:
- Practice with decision tree
- Start with simpler tasks
- Use solutions-guide for agent selection training
```

### Advanced Optimization

#### Context Efficiency Optimization
```
GOAL: Maximize agent effectiveness within 40% context limit

STRATEGIES:
1. Lean PROJECT_CONTEXT.md (essential info only)
2. Modular task breakdown (smaller, focused tasks)
3. Progressive disclosure (provide context as needed)
4. Pattern documentation (reduce repetitive explanations)

MEASUREMENT:
- Track context usage per agent interaction
- Monitor task completion success rates
- Assess agent output quality
```

#### Workflow Customization
```
GOAL: Optimize workflows for your specific project needs

PROCESS:
1. Analyze your most common task types
2. Identify repetitive patterns
3. Create custom workflow templates
4. Test and refine based on results

EXAMPLE CUSTOM WORKFLOW:
"API Endpoint Development"
1. Design API contract (software-engineer)
2. Security review (cybersecurity-engineer)
3. Implementation (software-engineer)
4. Integration testing (software-engineer)
5. Documentation (software-engineer)
```

## Integration with Other Agents

### Working with Project Navigator
```
COMPLEMENTARY ROLES:

Solutions Guide:
- System setup and optimization
- Workflow template selection
- Best practices coaching
- Agent system troubleshooting

Project Navigator:
- Project-specific knowledge
- Historical decision context
- Business logic understanding
- Code pattern recognition

HANDOFF PATTERN:
"For setup questions, use solutions-guide"
"For project questions, use project-navigator"
```

### Enhancing Agent Effectiveness
```
SOLUTIONS GUIDE CONTRIBUTIONS TO OTHER AGENTS:

For software-engineer:
- Provides optimized PROJECT_CONTEXT.md
- Ensures task scope is appropriate
- Suggests relevant patterns and conventions

For all specialists:
- Validates context efficiency
- Ensures clear success criteria
- Optimizes task breakdown and handoffs
```

## Feedback Integration

### Collecting Your Feedback
```
FEEDBACK CATEGORIES:

Agent Performance:
- Which agents work well for your project?
- Where do agents struggle or go off-track?
- What context do agents need but don't get?

Workflow Effectiveness:
- Which workflows save you time?
- Where do workflows feel clunky or slow?
- What steps are missing or unnecessary?

System Usability:
- What's confusing about the setup process?
- Where do you get stuck or need help?
- What features would make the biggest difference?
```

### Continuous Improvement
```
FEEDBACK INTEGRATION PROCESS:

1. COLLECT: Gather your experiences and suggestions
2. ANALYZE: Identify patterns and improvement opportunities
3. IMPLEMENT: Update templates, workflows, and guidance
4. TEST: Validate improvements with your project
5. ITERATE: Refine based on results

EXAMPLE IMPROVEMENT CYCLE:
Feedback: "Software-engineer agent doesn't understand our API patterns"
→ Analysis: PROJECT_CONTEXT.md missing API conventions section
→ Implementation: Enhanced API patterns template
→ Test: Sample API task with improved context
→ Result: 40% better agent performance on API tasks
```

## Success Metrics

### Setup Success Indicators
```
✅ SUCCESSFUL SETUP CHECKLIST:

Technical Setup:
□ .claude directory structure created correctly
□ PROJECT_CONTEXT.md comprehensive and project-specific
□ Templates copied and accessible
□ First task completed successfully

Knowledge Transfer:
□ User understands agent selection patterns
□ User can break down complex tasks appropriately
□ User knows how to optimize context for efficiency
□ User established productive daily patterns

System Integration:
□ Agents provide relevant, project-aware responses
□ Workflows feel natural and time-saving
□ Quality of work meets or exceeds manual approach
□ User confidence in independent system usage
```

### Ongoing Optimization Metrics
```
📊 PERFORMANCE INDICATORS:

Efficiency:
- Context usage per task (target: <40%)
- Task completion time vs manual approach
- Agent output quality scores

Effectiveness:
- User satisfaction with agent responses
- Reduction in repetitive manual work
- Improvement in code/decision quality

Adoption:
- Daily agent system usage
- Variety of agents utilized
- Workflow template usage patterns
```

The Solutions Guide is your dedicated partner in mastering the Claude Agent System - ensuring you get maximum value from this powerful development framework!