# Agent History Guidance

## Purpose

Agent history files provide institutional memory and knowledge continuity across agent sessions. They capture what was done, why decisions were made, and what should happen next. This enables:

- **Knowledge Transfer:** Future agents and humans can understand past work
- **Decision Tracking:** Preserve the rationale behind important choices
- **Progress Continuity:** Pick up where previous agents left off
- **Pattern Recognition:** Identify recurring issues or successful approaches
- **Quality Assurance:** Review agent performance and outcomes

---

## Mandatory Exit Protocol

Every agent **MUST** complete the exit protocol before ending their session. This is non-negotiable and critical for maintaining system intelligence.

### When to Execute Exit Protocol

Execute the exit protocol when:
1. Your primary task is complete
2. You're handing off to another agent
3. You're blocked and cannot proceed
4. Context window is approaching limits (>80%)
5. User explicitly ends the session
6. Maximum session time is reached

### Exit Protocol Steps

1. **Assess Completion Status**
   - Review your original objectives
   - Determine what was completed vs. pending
   - Identify any blockers or risks

2. **Generate History File**
   - Use the template at `.claude/context/agent-history/TEMPLATE-agent-history.md`
   - Create filename: `YYYYMMDD-HHMMSS-AGENT_NAME-###.md`
   - Fill out ALL sections (no placeholders or TODOs)

3. **Write History File**
   - Save to `.claude/context/agent-history/`
   - Use Write tool to create the file
   - Verify file was written successfully

4. **Notify User**
   - Provide brief summary of work completed
   - Reference the history file location
   - Highlight any urgent follow-ups needed

5. **Exit Cleanly**
   - No partial work left in progress
   - No uncommitted changes (unless intentional)
   - Clear handoff of next steps

---

## Filename Convention

### Format
```
YYYYMMDD-HHMMSS-AGENT_NAME-###.md
```

### Components
- **YYYYMMDD:** Date (e.g., 20241021)
- **HHMMSS:** Time in 24-hour format (e.g., 143022)
- **AGENT_NAME:** Short agent identifier (kebab-case)
- **###:** Sequential number for same agent on same day (001, 002, etc.)

### Examples
```
20241021-143022-pws-software-engineer-001.md
20241021-150315-pws-platform-engineer-001.md
20241021-161245-pws-software-engineer-002.md
20241022-090000-pws-product-manager-001.md
```

---

## Template Sections Guide

### Executive Summary
**Purpose:** Quick overview for humans scanning history files

**Content:**
- 1-2 paragraphs maximum
- What was the main task?
- What was accomplished?
- What are the key takeaways?

**Good Example:**
> "Evaluated the PWS document for the USAF Cloud Migration project from a software engineering perspective. The assessment found strong DevOps practices and modern delivery expectations (4/5 rating). However, identified concerns about unrealistic timeline for database migration and lack of clarity on testing environments. Recommended negotiating for 2-week buffer and clarifying environment provisioning timeline."

**Poor Example:**
> "Worked on stuff. Did some analysis. Found some things."

### Task Context
**Purpose:** Capture the "why" behind the work

**Content:**
- Original user request (verbatim if possible)
- Business context or problem being solved
- Constraints, deadlines, or requirements
- Why this agent was chosen for the task

**Tips:**
- Quote the user request exactly
- Include context that might not be obvious later
- Note any assumptions made

### Work Performed
**Purpose:** Document what actually happened

**Content:**
- Analysis steps taken
- Tools used (Read, Grep, WebFetch, etc.)
- Files examined or created
- Decisions made and alternatives considered

**Tips:**
- Be specific with file paths and line numbers
- Explain decision rationale
- Note any dead ends or failed approaches

### Key Findings
**Purpose:** Capture insights and learning

**Content:**
- Important discoveries or insights
- Risks, concerns, or red flags
- Opportunities identified
- Recommendations with rationale

**Tips:**
- Distinguish facts from opinions
- Prioritize findings by importance
- Make recommendations actionable

### Outcomes & Metrics
**Purpose:** Measure success objectively

**Content:**
- What success criteria were met?
- What quality indicators validate the work?
- What measurable impact was created?

**Tips:**
- Use checkboxes for success criteria (✓ or ○)
- Be honest about partial completions
- Include quantitative metrics where possible

### Handoff Information
**Purpose:** Enable seamless continuation

**Content:**
- What's ready for the next person?
- What's still pending?
- What blockers exist?
- Specific next steps (prioritized)

**Tips:**
- Make next steps actionable (not vague)
- Identify who should do what
- Call out urgent items clearly

### Knowledge Artifacts
**Purpose:** Make work reusable

**Content:**
- Files created or modified (with paths)
- Reusable code patterns or templates
- Documentation that was or should be created

**Tips:**
- Use relative paths from project root
- Describe why files are important
- Link to key code locations (file:line)

### Lessons Learned
**Purpose:** Improve future performance

**Content:**
- What worked well (to repeat)
- What could be improved (to change)
- Knowledge gaps identified (to fill)

**Tips:**
- Be specific, not generic
- Focus on actionable improvements
- Admit mistakes or missteps

### Context Window Usage
**Purpose:** Track efficiency and identify optimization needs

**Content:**
- Final context usage (tokens and percentage)
- Peak usage during session
- Notes on efficiency or waste

**Tips:**
- Check context usage before writing history
- Note if you hit limits or had to be careful
- Suggest optimizations for future agents

---

## Quality Standards

### Completeness
- **All sections must be filled out** (no "N/A" or "TODO" placeholders)
- If a section doesn't apply, explain why briefly
- Err on the side of more detail rather than less

### Clarity
- Write for someone who wasn't in the session
- Define acronyms and jargon
- Use concrete examples and specifics

### Objectivity
- Separate facts from opinions
- Admit uncertainties or limitations
- Don't oversell accomplishments

### Actionability
- Make recommendations specific and actionable
- Include enough detail to execute next steps
- Prioritize and sequence recommendations

### Searchability
- Use consistent terminology
- Include relevant keywords
- Reference files with full paths

---

## Anti-Patterns to Avoid

### ❌ Vague History
```markdown
## Work Performed
- Looked at some files
- Made some changes
- Found some issues
```

### ✓ Specific History
```markdown
## Work Performed
- Analyzed deployment configuration in `infrastructure/terraform/main.tf:45-120`
- Modified database connection pooling settings from 10 to 50 connections
- Identified security vulnerability in API authentication (CVE-2024-12345)
```

### ❌ Missing Context
```markdown
## Task Context
User wanted me to fix the bug.
```

### ✓ Rich Context
```markdown
## Task Context
User reported that customers were unable to complete checkout on the e-commerce site during high-traffic periods (>1000 concurrent users). Investigation needed to determine if this was a database connection issue, API rate limiting, or frontend timeout problem. Critical issue affecting $50K+ in daily revenue.
```

### ❌ No Handoff Information
```markdown
## Handoff Information
Everything is done.
```

### ✓ Clear Handoff
```markdown
## Handoff Information

### Completed Items
- Database connection pooling configured
- Load testing completed with 2000 concurrent users
- Monitoring alerts configured for connection pool exhaustion

### Pending Items
- Need to deploy to production (requires change approval)
- Documentation update for runbook needed

### Recommended Next Steps
1. Submit change request for production deployment (use template in docs/change-request.md)
2. Schedule deployment for low-traffic window (Sunday 2-4am EST)
3. Update runbook with new connection pool settings (docs/runbooks/database.md:45)
4. Monitor for 48 hours post-deployment
```

---

## Agent-Specific Considerations

### PWS Evaluation Agents
- Include scores with rationale
- Reference specific PWS sections (page numbers, section titles)
- Highlight deal-breakers clearly
- Provide competitive positioning insights

### Development Agents
- Include code snippets or file diffs
- Reference specific functions/classes with file:line notation
- Document test coverage and quality metrics
- Note technical debt created or resolved

### Research Agents
- Cite sources and references
- Document search strategies used
- Note information gaps or uncertainties
- Provide confidence levels for findings

### Strategic Agents
- Frame recommendations in business terms
- Include ROI or impact estimates
- Consider stakeholder perspectives
- Note political or organizational considerations

---

## Using History Files

### For Future Agents
When resuming work in a related area:
1. Search agent-history folder for relevant sessions
2. Read executive summaries to find related work
3. Review key findings and lessons learned
4. Check handoff information for next steps
5. Build upon previous insights (don't duplicate work)

### For Humans
When reviewing agent work:
1. Start with executive summary
2. Verify outcomes against success criteria
3. Review decisions and rationale
4. Check for risks or concerns flagged
5. Execute recommended next steps

### For System Improvement
When improving the agent system:
1. Analyze patterns across history files
2. Identify recurring issues or successes
3. Extract reusable patterns and templates
4. Update agent prompts based on lessons learned
5. Improve tools or workflows based on feedback

---

## Technical Implementation

### Generating the Filename
```python
from datetime import datetime

def generate_history_filename(agent_name, sequence_number=1):
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = f"{timestamp}-{agent_name}-{sequence_number:03d}.md"
    return f".claude/context/agent-history/{filename}"

# Example usage
filename = generate_history_filename("pws-software-engineer", 1)
# Output: .claude/context/agent-history/20241021-143022-pws-software-engineer-001.md
```

### Checking for Existing Files
Before writing, check if a file with the same timestamp already exists:
```bash
ls .claude/context/agent-history/20241021-143022-pws-software-engineer-*.md
```

If exists, increment the sequence number.

### Writing the File
Use the Write tool to create the history file:
```
Write tool:
- file_path: /absolute/path/to/.claude/context/agent-history/[filename].md
- content: [filled out template]
```

---

## Quality Checklist

Before exiting, verify:
- [ ] All template sections are completed
- [ ] Filename follows convention (YYYYMMDD-HHMMSS-AGENT_NAME-###.md)
- [ ] File saved to correct location (.claude/context/agent-history/)
- [ ] Executive summary is clear and concise
- [ ] Work performed is detailed and specific
- [ ] Key findings include actionable recommendations
- [ ] Handoff information specifies next steps
- [ ] Lessons learned capture improvement opportunities
- [ ] Context usage is documented
- [ ] No placeholder text remains (no TODO, TBD, N/A without explanation)
- [ ] User has been notified of history file location

---

## Examples

### Good History File
See: `.claude/context/agent-history/TEMPLATE-agent-history.md` (with all sections filled)

### Finding History Files
```bash
# Find all histories for a specific agent
ls .claude/context/agent-history/*pws-software-engineer*.md

# Find all histories from a specific date
ls .claude/context/agent-history/20241021-*.md

# Find all histories from the last 7 days
find .claude/context/agent-history -name "*.md" -mtime -7

# Search history content for specific topics
grep -r "database migration" .claude/context/agent-history/
```

---

## Support & Questions

If you encounter issues with the exit protocol:
1. Check this guidance document for clarification
2. Review the template file for structure
3. Look at existing history files for examples
4. When in doubt, include more detail rather than less
5. Notify the user if you cannot complete the protocol

Remember: **The exit protocol is mandatory and non-negotiable.** Agent history is the institutional memory of the system.

---

*Last Updated: 2024-10-21*
*Version: 1.0*
