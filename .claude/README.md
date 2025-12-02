# Solutions - Claude Agent Orchestration System

This folder contains the complete Claude Agent Orchestration system that can be copied to any project to enable powerful AI-assisted development workflows.

## 🚀 Quick Start (One Command Setup)

To use this system in a new project:

```bash
# From solutions repository root
cp -r .claude/ /path/to/your/project/.claude/
cp CLAUDE.md /path/to/your/project/
```

Then in your new project, run:
```bash
/setup
```

That's it! Claude Code will automatically:
- ✅ Load `CLAUDE.md` as persistent memory/instructions
- ✅ Use agents from `.claude/agents/` for specialized tasks
- ✅ Apply hooks from `.claude/hooks/` for context tracking
- ✅ Use templates from `.claude/templates/` for PRDs, tasks, sessions
- ✅ Follow task workflows from `.claude/tasks/`
- ✅ Create and customize workspace color theme

## 📁 Folder Structure

```
.claude/                             # Active system folder (in your projects)
├── agents/                          # Specialized AI agent prompts
│   ├── cicd-engineer.md            # CI/CD pipeline specialist
│   ├── cybersecurity-engineer.md   # Security analysis expert
│   ├── data-scientist.md           # Data analysis & ML specialist
│   ├── solutions-guide.md          # System setup assistant
│   ├── platform-engineer.md        # Infrastructure specialist
│   ├── product-manager.md          # Feature planning expert
│   ├── project-navigator.md        # Project knowledge expert
│   ├── software-engineer.md        # Code implementation expert
│   └── ux-ui-designer.md          # UI/UX design specialist
├── commands/                        # Custom slash commands
│   └── setup.md                    # Project setup & workspace customization
├── docs/                           # Documentation & guides
│   ├── README.md                   # System documentation
│   ├── agent-invocation-examples.md
│   ├── code-quality-examples.md
│   ├── task-management-examples.md
│   └── testing-and-implementation.md
├── hooks/                          # Automated behavior hooks
│   └── post-prompt-context.sh     # Context usage tracking
├── tasks/                          # Task workflow directories
│   ├── 0_obe/                     # Overtaken by Events (cancelled)
│   ├── 1_backlog/                 # Planned features/tasks
│   ├── 2_active/                  # Currently in progress
│   ├── 3_completed/               # Finished tasks
│   ├── templates/                 # Task-specific templates
│   ├── 1_create-prd.md           # PRD creation workflow
│   ├── 2_generate-tasks.md       # Task generation workflow
│   ├── 3_process-task-list.md    # Task execution workflow
│   ├── project-status.md         # Overall project status
│   └── README.md                 # Task system documentation
├── templates/                      # Reusable templates
│   ├── agent-template.md          # For creating new agents
│   ├── handoff-session-template.md # Session continuity
│   ├── session-summary-template.md # Session summaries
│   ├── simple-task-template.md    # Basic task structure
│   ├── vscode-settings-template.json # Workspace color template
│   └── README.md                  # Template documentation
├── context/                        # Runtime session tracking
│   └── session-history/           # Session handoff files (created at runtime)
├── audio/                          # Optional completion audio
│   └── completion.wav             # "Project name is finished" audio
├── settings.json                   # Claude Code configuration
├── settings.local.json            # Local overrides (gitignored)
└── README.md                      # This file
```

## 🎯 What This System Provides

### 1. **Specialized AI Agents**
Invoke domain experts for specific tasks:
- **Software Engineer**: Code implementation & architecture
- **Platform Engineer**: Infrastructure & deployment
- **Cybersecurity Engineer**: Security analysis & hardening
- **CI/CD Engineer**: Pipeline automation & testing
- **Data Scientist**: Data analysis & ML workflows
- **Product Manager**: Feature planning & requirements
- **UX/UI Designer**: User experience & interface design
- **Solutions Guide**: System setup & configuration
- **Project Navigator**: Project knowledge & context

### 2. **PRD-Driven Development**
Structured workflow for feature development:
1. Create PRD (Product Requirements Document)
2. Generate detailed task breakdown
3. Implement with agent assistance
4. Track progress through lifecycle stages

### 3. **Session Continuity**
Automatic handoff system for long sessions:
- **50% context**: Warning phase
- **65% context**: Auto-create handoff files
- **80% context**: Critical - new session recommended

### 4. **Task Management**
Complete task tracking system:
- Task templates for different scenarios
- Lifecycle management (backlog → active → completed)
- OBE (Overtaken by Events) for cancelled work
- Integration with TodoWrite tool

### 5. **Context Awareness**
Automatic context usage tracking:
- Visual emoji-based meter (🟩🟨🟧🟥)
- Calculated against 155k usable tokens (excludes autocompact buffer)
- Displayed at end of every response

### 6. **Custom Commands**
Slash commands for common operations:
- `/setup`: Complete project setup with workspace colors, product vision, and project context

## 🔧 Configuration Files

### `settings.json`
Configures hooks and project-level settings:
```json
{
  "hooks": {
    "UserPromptSubmit": {
      "command": "./.claude/hooks/post-prompt-context.sh"
    }
  }
}
```

### `settings.local.json`
Local overrides (gitignored, project-specific):
```json
{
  "hooks": {
    "Stop": {
      "command": "afplay .claude/audio/completion.wav 2>/dev/null || true"
    }
  }
}
```

### `hooks/post-prompt-context.sh`
Reminds Claude to display context usage after each prompt.

## 📚 Key Concepts

### Agent Orchestration
Main Claude delegates specialized tasks to domain experts for:
- ✅ Expert-level quality on domain-specific work
- ✅ Context efficiency (agents work within their scope)
- ✅ Parallel execution of independent tasks
- ✅ Clear separation of concerns

### PRD Workflow
Structured approach to feature development:
```
.claude/tasks/1_backlog/001-feature-name/
├── prd-001-feature-name.md          # Requirements document
├── tasks-prd-001-feature-name.md    # Generated task breakdown
└── [implementation files...]         # Code, configs, etc.
```

### Session Handoff
Maintains workflow continuity across context boundaries:
```
.claude/context/session-history/
├── 001-SESSION.md                   # Completed session record
├── 002-SESSION.md                   # Next completed session
└── HANDOFF-SESSION.md               # Always current handoff
```

## 🎨 Workspace Color Customization

Each project can have a **unique two-color theme** for easy visual identification across multiple VS Code windows.

### How It Works

When you start a new project from solutions template:
1. Run `/setup` command
2. The `.vscode/settings.json` file is created from template
3. Default theme is **Green + Brown** ("Solutions")
4. Claude detects this and **offers to customize** workspace colors
5. Claude can **auto-infer** themes from project names (e.g., "ocean-api" → Blue + Teal)
6. Or you can **choose any two-color pairing** manually

### Setup Process

**Automatic (Recommended):**
```
User: "I'm setting up my new project called 'ocean-api'"
Claude: "I notice the default colors. The name 'ocean-api' suggests
         Blue + Teal (Ocean theme). Use this? (Yes/No/Choose different)"
```

**Manual:**
```
User: "Set up workspace colors with purple and blue"
Claude: [Applies Purple + Blue theme immediately]
```

### Available Themes

**Nature:** Green + Brown, Teal + Sage
**Ocean:** Blue + Teal, Cyan + Navy
**Fire:** Red + Orange, Orange + Yellow
**Royal:** Purple + Blue, Magenta + Purple
**Sunset:** Pink + Orange, Rose + Gold
**Energy:** Orange + Yellow
**Tech:** Cyan + Navy
**Earth:** Teal + Sage

### What Gets Colored

✅ **Primary color** (most visible): Title bar, status bar, section headers
✅ **Secondary color** (accents): Borders, tab underlines, activity bar border
✅ **Background tint**: Sidebar (subtle blend of both colors)
❌ **Stays default**: Editor, terminal content, syntax highlighting

This keeps code **fully readable** while making workspaces **instantly recognizable**!

## 🔊 Audio Completion Notifications

Optional macOS feature that plays "[Project Name] is finished" after each prompt completion.

### Enable Audio Notifications

Add this to `.claude/settings.local.json`:
```json
{
  "hooks": {
    "Stop": {
      "command": "afplay .claude/audio/completion.wav 2>/dev/null || true"
    }
  }
}
```

Note: Audio notifications are not available when running in devcontainer environments.

### Disable Audio Notifications

Remove the `"Stop"` hook from `.claude/settings.local.json` or delete the file.

## 🎯 Customization

### Adding New Agents
1. Create `.claude/agents/your-agent.md`
2. Use `agent-template.md` as starting point
3. Define expertise, capabilities, and protocols
4. Reference in `CLAUDE.md` orchestration rules

### Adding New Templates
1. Create template in `.claude/templates/`
2. Use existing templates as reference
3. Include clear placeholder syntax
4. Document in templates README

### Adding Custom Commands
1. Create `.claude/commands/your-command.md`
2. Define task, steps, and success criteria
3. Use existing commands as reference
4. Test thoroughly before distribution

### Modifying Workflows
1. Edit task workflow files in `.claude/tasks/`
2. Update `CLAUDE.md` with new protocols
3. Test in this repo before distributing

## 🚨 Important Notes

### What Gets Copied
When you run `cp -r .claude/ /path/to/project/.claude/`:
- ✅ All agents, templates, hooks, settings, commands
- ✅ Empty task directories (0_obe, 1_backlog, 2_active, 3_completed)
- ✅ Documentation and guides
- ❌ NOT session history (created at runtime)
- ❌ NOT active tasks (project-specific)
- ❌ NOT .vscode/ (created by /setup)

### What Stays in Projects
Each project's `.claude/` folder will contain:
- Project-specific task files
- Session history for that project
- Runtime state and context
- Local settings overrides

### Updating the System
To update a project with new templates/agents:
```bash
# Backup existing .claude if you have project-specific customizations
cp -r /path/to/project/.claude/ /path/to/project/.claude.backup/

# Copy new version from solutions
cp -r .claude/ /path/to/project/.claude/

# Restore project-specific files if needed
cp -r /path/to/project/.claude.backup/tasks/ /path/to/project/.claude/tasks/
cp -r /path/to/project/.claude.backup/context/ /path/to/project/.claude/context/
cp /path/to/project/.claude.backup/settings.local.json /path/to/project/.claude/
```

## 📖 Further Reading

- See `docs/` folder for detailed guides and examples
- Review `CLAUDE.md` for complete orchestration rules
- Check individual agent files in `agents/` for capabilities
- Explore templates in `templates/` for different scenarios
- Read task system docs in `tasks/README.md`

## 🤝 Contributing

To improve this system:
1. Make changes in `solutions` repository
2. Test thoroughly with real projects
3. Update documentation
4. Distribute updated `.claude/` folder to projects

## 📋 Directory Details

### `/agents/`
Domain-expert AI agent prompts for specialized tasks. Each agent has defined expertise areas, invocation patterns, and quality standards.

### `/commands/`
Custom slash commands that extend Claude Code functionality. Commands are markdown files defining task workflows.

### `/context/`
Runtime session tracking and handoff files. Created automatically at 65% context usage for session continuity.

### `/docs/`
Comprehensive documentation for system usage, best practices, and examples.

### `/hooks/`
Shell scripts that run in response to Claude Code events (prompt submit, stop, etc.).

### `/tasks/`
Complete task management system with PRD workflows, task templates, and lifecycle tracking.

### `/templates/`
Reusable markdown templates for agents, tasks, sessions, PRDs, and workspace configuration.

### `/audio/`
Optional completion notification audio files (macOS only).

### `/tests/`
Test files for validating system behavior and agent responses.

---

**Version**: 3.0 (Consolidated Single .claude/ Folder)
**Last Updated**: 2025-10-08
**Maintained by**: Solutions Project
