# Setup Guide - Solutions Claude Agent System

## 🚀 Quick Start for New Projects

### 1. Copy System Files

From the `solutions` repository:

```bash
# Copy the entire Claude Agent System
cp -r .claude/ /path/to/your/project/.claude/

# Copy the memory/instruction file
cp CLAUDE.md /path/to/your/project/
```

### 2. Initialize Workspace

In your new project, start Claude Code and run:

```bash
# Interactive mode - Claude suggests colors based on project name
/setup

# Single argument - Apply predefined theme
/setup red      # Red + Orange
/setup ocean    # Blue + Teal

# Two arguments - Custom color pairing
/setup red blue       # Red primary, Blue secondary
/setup purple orange  # Purple primary, Orange secondary
```

This command will:
- ✅ Create `.vscode/settings.json` from template
- ✅ Configure unique workspace colors for your project
- ✅ Generate audio completion notification (macOS)
- ✅ Set up all hooks and settings

**Supported color keywords**: `red`, `orange`, `yellow`, `green`, `teal`, `blue`, `cyan`, `purple`, `magenta`, `pink`, `brown`, `navy`, `sage`, `gray`, `white`, `silver`, `black`

**Supported theme keywords**: `ocean`, `fire`, `royal`, `sunset`, `tech`, `nature`, `earth`, `energy`

### 3. Start Working

Tell Claude:
```
I'm setting up a new project with the Claude Agent System.
Please use the solutions-guide agent to help me get started.
```

## 📁 What You Get

After setup, your project will have:

```
your-project/
├── .claude/                    # Complete agent system
│   ├── agents/                 # 9 specialized AI agents
│   ├── commands/               # Custom slash commands
│   ├── templates/              # 15+ workflow templates
│   ├── tasks/                  # PRD lifecycle folders
│   ├── docs/                   # Documentation
│   ├── hooks/                  # Automation hooks
│   ├── settings.json           # Base configuration
│   ├── settings.local.json     # Local overrides
│   ├── audio/                  # Completion audio
│   └── context/                # Session history
├── .vscode/                    # Workspace customization
│   └── settings.json           # Unique color theme
├── CLAUDE.md                   # Agent orchestration rules
└── [your project files...]
```

## 🎨 Workspace Colors

Each project gets a unique two-color theme:

**Default**: Green + Brown ("Solutions")

**Other themes**: Ocean (Blue + Teal), Fire (Red + Orange), Royal (Purple + Blue), etc.

Claude will detect your project name and suggest appropriate colors, or you can choose manually.

## 🔊 Audio Notifications (Optional)

macOS users get audio completion notifications by default ("Project name is finished" after each prompt).

**To disable**: Remove the `"Stop"` hook from `.claude/settings.local.json`

## 📚 Learn More

- `.claude/README.md` - Complete system documentation
- `CLAUDE.md` - Agent orchestration rules
- `.claude/docs/` - Detailed guides and examples
- `.claude/agents/` - Individual agent capabilities

## 🔄 Updating the System

To update a project with new system features:

```bash
# Backup project-specific files
cp -r /path/to/project/.claude/tasks/ /tmp/tasks-backup/
cp -r /path/to/project/.claude/context/ /tmp/context-backup/
cp /path/to/project/.claude/settings.local.json /tmp/

# Copy new system version
cp -r .claude/ /path/to/project/.claude/

# Restore project-specific files
cp -r /tmp/tasks-backup/ /path/to/project/.claude/tasks/
cp -r /tmp/context-backup/ /path/to/project/.claude/context/
cp /tmp/settings.local.json /path/to/project/.claude/
```

## ✨ Key Features

- **9 Specialized Agents**: Domain experts for infrastructure, security, CI/CD, data, product, design, etc.
- **PRD-Driven Development**: Structured workflow from requirements to implementation
- **Session Continuity**: Auto-handoff at 65% context usage
- **Context Tracking**: Visual meter showing usage (🟩🟨🟧🟥)
- **Task Management**: Complete lifecycle (backlog → active → completed → OBE)
- **Visual Identity**: Unique workspace colors per project
- **Custom Commands**: Extensible slash command system

---

**Version**: 3.0 (Consolidated Single .claude/ Folder)
**Last Updated**: 2025-10-08
