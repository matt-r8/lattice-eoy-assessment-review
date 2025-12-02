# Setup Command
**Task**: Complete project setup workflow: configure workspace colors, optionally create product vision, and populate project context through guided discovery.

## Usage
/setup \[primary\] \[secondary\]

**Arguments**:
- `[primary]` (optional): Primary color or theme keyword
- `[secondary]` (optional): Secondary color (only used with primary color)

**Examples**:
- `/setup` - Interactive mode, prompts for color selection
- `/setup red` - Apply Red + Orange theme
- `/setup ocean` - Apply Blue + Teal theme
- `/setup red blue` - Apply Red primary + Blue secondary
- `/setup purple orange` - Apply Purple primary + Orange secondary

## Steps
1. **Parse Command Arguments**
   - Check if any color arguments were provided
   - **No arguments**: Proceed with interactive workflow
   - **One argument**: Match against theme keywords or single-color mappings
   - **Two arguments**: Use first as primary, second as secondary (custom pairing)

2. **Detect Project Context**
   - Get the current project directory name
   - Extract project name from git remote (if available)
   - Identify project type/purpose from README or package.json

3. **Initialize VS Code Workspace**
   - Check if `.vscode/settings.json` exists
   - If not, create `.vscode/` directory
   - Copy `.claude/templates/vscode-settings-template.json` to `.vscode/settings.json`

4. **Analyze Current Color Scheme**
   - Read `.vscode/settings.json`
   - Extract current primary and secondary colors
   - Check if colors are still default template (Green: `#22c55e`/`#166534`, Brown: `#78350f`/`#d97706`)

5. **Determine Theme to Apply**
   **If two color arguments provided** (e.g., `/setup red blue`):
   - Use first argument as primary color
   - Use second argument as secondary color
   - Look up hex codes from Color Hex Code Mapping
   - Calculate blended background color
   - Apply custom pairing immediately
   - Skip interactive prompts

   **If one color argument provided** (e.g., `/setup red`):
   - Match argument against theme keywords (see Theme Keyword Mapping below)
   - Apply matching predefined theme immediately
   - Skip interactive prompts

   **If no arguments (interactive mode)**:
   - Infer theme from project name using keyword matching
   - Present options to user:
     - A) Use inferred theme (if matched)
     - B) Choose from 10+ example color pairings
     - C) Keep current colors

6. **Apply Color Scheme**
   - If user selects a theme, update `.vscode/settings.json`
   - Replace all 7 color instances:
     - Primary bright (line 8)
     - Primary dark (line 9)
     - Secondary dark (line 12)
     - Secondary light (line 13)
     - Background tint (line 16)
     - Theme name comment (line 3)
   - Confirm completion with theme name and colors

7. **Success Confirmation**
   ✅ Workspace colors updated to [Theme Name]!
   - Primary: [Color Name] (#hexcode)
   - Secondary: [Color Name] (#hexcode)

   Reload VS Code to see the new theme.

8. **Product Vision Discovery (Optional)**
   Determine if the project needs a product vision document.

   1. **Ask User About Project Scope**
      Present clear question to user:

      🎯 Would you like to create a product vision document?
      A product vision defines high-level objectives, target users, and strategic
      themes before diving into technical implementation.
      **Recommended for**: Full applications, multi-phase projects, products with
      multiple features or stakeholders
      **Skip for**: Single scripts, utilities, one-off tools, simple features
      Would you like to create a product vision? (Y/N)  

   2. **If User Selects Yes (Y)**
      a. **Check for PRODUCT_VISION.md**:
      - Look in project root for `PRODUCT_VISION.md`
      - If doesn't exist, copy template: `cp .claude/templates/product-vision-template.md PRODUCT_VISION.md`

      b. **Detect Template Status**:
      - Read PRODUCT_VISION.md
      - Check if it contains template placeholder text like:
        - `[Project Name]`
        - `[Date]`
        - `[Name/Team]`
        - Or if file is mostly empty (< 1000 characters of actual content)

      c. **Invoke Product Visionary Agent**:
      If PRODUCT_VISION.md is template/empty:

      📋 Let's define your product vision!
      I'm going to have our product-visionary agent conduct a discovery
      interview to understand your product goals and populate the vision document.

      Then invoke the product-visionary agent with this task:

      Task: Conduct product vision discovery interview and populate PRODUCT_VISION.md
      Context: User has just completed workspace setup and wants to define product
      vision. The PRODUCT_VISION.md file exists but is still in template form.

      Constraints:
      - Use conversational, exploratory tone for discovery
      - Ask strategic questions about users, problems, and value proposition
      - Build understanding of high-level objectives and themes
      - Help user articulate vision clearly

      Expected Deliverables:
      1. Complete discovery interview covering vision, users, value prop, themes
      2. Fully populated PRODUCT_VISION.md with strategic themes defined
      3. Clear roadmap themes that can drive PRD creation

      Success Criteria:
      - All template placeholders replaced with actual vision content
      - User has clarity on high-level objectives
      - Strategic themes are defined for roadmap planning
      - PRODUCT_VISION.md is ready to guide technical PRD development

      d. **Completion Message**: After product-visionary completes:
      ✅ Product vision captured successfully!
      Your PRODUCT_VISION.md defines strategic themes that will guide
      feature development and PRD creation.
      Next: Let's set up your technical project context.

      e. **If PRODUCT_VISION.md Already Populated**: Skip product-visionary invocation and show:
      ✅ Product vision already defined!
      Moving to technical project setup...


   3. **If User Selects No (N)**
      Skip product vision creation:
      ⏭️ Skipping product vision.
      Moving to technical project setup...

   4. **Proceed to Step 9** (Project Context Discovery)

9. **Project Context Discovery**
   Check if PROJECT_CONTEXT.md needs to be populated:

   1. **Check for PROJECT_CONTEXT.md**
      - Look in project root for `PROJECT_CONTEXT.md`
      - If file doesn't exist, skip this step (user hasn't set up the system yet)

   2. **Detect Template/Empty Status**
      - Read the PROJECT_CONTEXT.md file
      - Check if it contains template placeholder text like:
        - `[Project Name]`
        - `[Brief Description]`
        - `<!-- Replace this template...`
        - Or if the file is mostly empty (< 500 characters of actual content)

   3. **Invoke Solutions Guide Agent**
      If PROJECT_CONTEXT.md is template/empty:

      📋 I notice your PROJECT_CONTEXT.md is still a template. Let me help you fill it out!
      I'm going to have our solutions-guide agent walk you through a discovery interview
      to understand your project and populate the context file.

      Then invoke the solutions-guide agent with this task:

      Task: Conduct project discovery interview and populate PROJECT_CONTEXT.md
      Context: User has just completed workspace setup. The PROJECT_CONTEXT.md file
      exists but is still in template form and needs to be populated with actual
      project information.

      Constraints:
      - Use conversational, friendly tone for discovery questions
      - Ask questions one at a time or in small groups
      - Reference the project discovery question checklist
      - Build rapport while gathering information

      Expected Deliverables:
      1. Complete discovery interview covering all essential areas
      2. Fully populated PROJECT_CONTEXT.md file with user's project information
      3. Confirmation that the file has been saved

      Success Criteria:
      - All template placeholders replaced with actual project info
      - User feels their project context is accurately captured
      - PROJECT_CONTEXT.md is ready for use by other agents

   4. **Completion Message** After solutions-guide completes:
      ✅ Project context captured successfully!
      Your PROJECT_CONTEXT.md is now populated and will help all agents
      understand your project better.
      🎉 Onboarding complete! You're ready to start working.

   5. **If PROJECT_CONTEXT.md Already Populated** Skip solutions-guide invocation and show:
      ✅ Project context already configured!
      🎉 Onboarding complete! Your workspace is ready.

## How to Change Settings

### Workspace Colors

**To Change Colors**: Run `/setup` command again and select a new theme

**To Revert to Defaults**: Manually edit `.vscode/settings.json` and restore:
- Primary: `#22c55e` (bright), `#166534` (dark)
- Secondary: `#78350f` (dark), `#d97706` (light)
- Background: `#1f2617`

## Color Hex Code Mapping

**For custom two-color pairings**, use these base colors:
- `red`: Bright `#ef4444`, Dark `#991b1b`
- `orange`: Bright `#f97316`, Dark `#9a3412`
- `yellow`: Bright `#fde047`, Dark `#854d0e`
- `green`: Bright `#22c55e`, Dark `#166534`
- `teal`: Bright `#14b8a6`, Dark `#0f766e`
- `blue`: Bright `#3b82f6`, Dark `#1e40af`
- `cyan`: Bright `#06b6d4`, Dark `#0e7490`
- `purple`: Bright `#a855f7`, Dark `#6b21a8`
- `magenta`: Bright `#ec4899`, Dark `#9f1239`
- `pink`: Bright `#ec4899`, Dark `#9f1239`
- `brown`: Bright `#d97706`, Dark `#78350f`
- `navy`: Bright `#93c5fd`, Dark `#1e3a8a`
- `sage`: Bright `#84cc16`, Dark `#365314`
- `gray`: Bright `#9ca3af`, Dark `#4b5563`
- `white`: Bright `#f3f4f6`, Dark `#d1d5db`
- `silver`: Bright `#e5e7eb`, Dark `#9ca3af`
- `black`: Bright `#6b7280`, Dark `#1f2937`

## Theme Keyword Mapping

**Single-color keywords** (apply predefined theme):
- `red` → Red + Orange
- `orange` → Orange + Yellow
- `yellow` → Orange + Yellow
- `green` → Green + Brown
- `teal` → Teal + Sage
- `blue` → Blue + Teal
- `cyan` → Cyan + Navy
- `purple` → Purple + Blue
- `magenta` → Magenta + Purple
- `pink` → Pink + Orange
- `brown` → Green + Brown

**Multi-color keywords** (specific pairings):
- `ocean` → Blue + Teal
- `fire` → Red + Orange
- `royal` → Purple + Blue
- `sunset` → Pink + Orange
- `tech` → Cyan + Navy
- `nature` → Green + Brown
- `earth` → Teal + Sage
- `energy` → Orange + Yellow

## Color Pairings with Hex Codes

**Nature:**
- Green + Brown: `#22c55e`, `#166534`, `#78350f`, `#d97706`, `#1f2617`
- Teal + Sage: `#14b8a6`, `#0f766e`, `#365314`, `#84cc16`, `#1a2617`

**Ocean:**
- Blue + Teal: `#3b82f6`, `#1e40af`, `#0f766e`, `#5eead4`, `#1a2e3e`
- Cyan + Navy: `#06b6d4`, `#0e7490`, `#1e3a8a`, `#93c5fd`, `#1a2d3e`

**Fire:**
- Red + Orange: `#ef4444`, `#991b1b`, `#9a3412`, `#fdba74`, `#2e1a1a`
- Orange + Yellow: `#f97316`, `#9a3412`, `#854d0e`, `#fde047`, `#2e1f1a`

**Royal:**
- Purple + Blue: `#a855f7`, `#6b21a8`, `#1e40af`, `#93c5fd`, `#2a1e3e`
- Magenta + Purple: `#ec4899`, `#9f1239`, `#6b21a8`, `#d8b4fe`, `#2e1a2e`

**Sunset:**
- Pink + Orange: `#ec4899`, `#9f1239`, `#9a3412`, `#fdba74`, `#2e1a1e`
- Rose + Gold: `#f43f5e`, `#9f1239`, `#854d0e`, `#fde047`, `#2e1a17`

**Energy:**
- Orange + Yellow: `#f97316`, `#9a3412`, `#854d0e`, `#fde047`, `#2e1f1a`

**Tech:**
- Cyan + Navy: `#06b6d4`, `#0e7490`, `#1e3a8a`, `#93c5fd`, `#1a2d3e`

**Earth:**
- Teal + Sage: `#14b8a6`, `#0f766e`, `#365314`, `#84cc16`, `#1a2617`

## Success Criteria

- Project name detected correctly
- Current color scheme analyzed
- Appropriate theme suggested (if keywords match)
- User presented with clear options
- Colors applied correctly if user selects a theme
- Confirmation message displays new theme details
- Product vision scope assessed with user
- PRODUCT\_VISION.md created and populated if requested
- Product-visionary agent invoked successfully (if vision requested)
- Strategic themes defined in vision document (if vision requested)
- PROJECT\_CONTEXT.md status detected correctly
- Solutions-guide invoked if context is template/empty
- Project discovery interview conducted successfully (if needed)
- PROJECT\_CONTEXT.md populated with actual project information (if needed)