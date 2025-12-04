# Individual Assessment Report Guide for Practice Leads

**Purpose**: This guide explains how to read, interpret, and use individual assessment reports for EOY performance reviews and scorecard completion.

**Audience**: Practice Leads, Department Leads, Team Leaders

**Version**: 1.0.0 | Last Updated: December 4, 2025

---

## Table of Contents

1. [Overview](#overview)
2. [Report Generation Process](#report-generation-process)
3. [Terminology Glossary](#terminology-glossary)
4. [Understanding Scores](#understanding-scores)
5. [Understanding Deltas (Self-Awareness)](#understanding-deltas-self-awareness)
6. [Statistical Metrics Explained](#statistical-metrics-explained)
7. [Tier Assignment System](#tier-assignment-system)
8. [Interpreting "Insufficient Data" Messages](#interpreting-insufficient-data-messages)
9. [Addressing Common Questions](#addressing-common-questions)
10. [FAQ](#faq)
11. [Best Practices for Using These Reports](#best-practices-for-using-these-reports)

---

## Overview

### What These Reports Are

Individual Assessment Reports are comprehensive performance analyses that combine:
- **Quantitative data**: Numerical scores from 10 behavioral questions based on Rise8's core values
- **Qualitative synthesis**: AI-analyzed feedback from peers on accomplishments, strengths, and development areas
- **Comparative analysis**: How the employee's performance compares to peers, team, department, and company

### How They're Generated

These reports are created through a three-phase automated process that combines Python statistical analysis with AI synthesis (see [Report Generation Process](#report-generation-process) for details).

### Who Should Read Them

- **Primary**: Practice Leads completing EOY scorecards
- **Secondary**: Department Leads, Team Leaders conducting performance discussions
- **Tertiary**: HR/People Ops for calibration and compensation planning

### How to Use Them

1. **EOY Scorecard Completion**: Use tier assignments and performance data as starting points
2. **Performance Discussions**: Reference specific questions, deltas, and qualitative feedback
3. **Development Planning**: Identify growth opportunities from START/STOP/KEEP recommendations
4. **Calibration Meetings**: Compare scores and tiers across practice/level

---

## Report Generation Process

**TL;DR**: Python calculates stats → AI synthesizes qualitative feedback → Report combines both with tier assignment

### Phase 1: Python Statistical Analysis

A Python script (`generate_individual_report.py`) analyzes raw assessment data to calculate:

- **Averages**: Peer average, self average, team average, level average, department average, project average, company average
- **Percentiles**: Where this employee ranks compared to all employees company-wide
- **Deltas**: Self-awareness gaps (difference between self-scores and comparison groups)
- **Standard Deviations**: Agreement/disagreement among reviewers
- **Score Ranges**: Highest and lowest scores received for each question

**Data Sources**:
- Individual assessment files (`assessments/[Department]/[Name].md`)
- Team mapping data (`team_map.json` with org structure)
- Comprehensive employee data (`riser_data_detailed.csv`)
- Company-wide tier assignments (`tier_assignments.csv`)

**Output**: A structured dataset with all quantitative metrics for each question

### Phase 2: AI Qualitative Synthesis

The `rise8-assessment-reviewer` agent (specialized AI trained on Rise8 values, manifesto, and A Player agreement) analyzes:

- **Question 13** (Self-Assessment): Employee's accomplishments
- **Question 11** (eNPS Comments): Why peers would/wouldn't rehire this person
- **Question 12** (START/STOP/KEEP): Development recommendations from peers

**What the AI Does**:
- Synthesizes recurring themes across multiple peer comments
- Identifies key accomplishments aligned with Rise8 values
- Highlights patterns in feedback (strengths, growth areas, blind spots)
- Generates actionable recommendations based on peer input

**What the AI Does NOT Do**:
- Override quantitative scores
- Make final tier decisions (algorithm-driven)
- Access level-specific competency matrices (known limitation)

### Phase 3: Report Assembly

The script combines Phase 1 (quantitative) and Phase 2 (qualitative) into a markdown report that includes:

- Overall scores and tier assignment
- Per-question breakdowns with statistical analysis
- Synthesized accomplishments review
- eNPS comments summary
- START/STOP/KEEP development recommendations

**Report Metadata**: Each report includes generation timestamp, script version, and data source file paths for traceability.

---

## Terminology Glossary

### Peers

**Definition**: All other Risers who submitted an assessment for this employee

**Example**: If 5 people reviewed Anthony Zubia, those 5 people are his peer reviewers

**Important Note**: "Peers" includes anyone who reviewed the employee, regardless of their role, level, or department. It's not limited to same-level colleagues.

### Team

**Definition**: The employee's assigned team in the organizational structure

**Examples**: "Beach", "OSIT", "Overhead", "Crypto", "ATTV"

**Data Source**: `team_map.json` (organizational team assignments)

### Project

**Definition**: The primary project or contract the employee is assigned to

**Examples**:
- "SPOC/S35F - Combat Enhancement Teams (AP IDIQ)"
- "Overhead" (internal work)
- "ATTV"
- "Multiple Projects" (cross-project contributors)

**Data Source**: `team_map.json` (project assignments)

### Department / Practice

**Definition**: The functional practice area or discipline

**Examples**: "Design", "Product-Management", "Software", "Platform-Cyber", "Enablement", "Directorate"

**Data Source**: Assessment file location (`assessments/[Department]/`)

### Level

**Definition**: Career level in the Rise8 organization

**Common Levels**:
- Junior Practitioner
- Practitioner
- Senior Practitioner
- Expert Practitioner
- Team Leader
- Senior Leader

**Data Source**: `team_map.json` (employee level data)

### Company

**Definition**: All employees across all departments, teams, levels, and projects

**Usage**: Company averages represent the baseline for all Rise8 employees

### Response Rate

**Definition**: The number of unique reviewers who answered a specific question divided by the total number of peer reviewers who submitted an assessment for this employee

**Example**:
- 5 people submitted assessments for Anthony Zubia
- 4 of them answered Question 1
- Response Rate: 4/5 (80%)

**Important**: Response rate varies by question. Some reviewers may skip questions if they don't have visibility into that specific behavior.

---

## Understanding Scores

### Score Scale

| Score | Meaning | Interpretation |
|-------|---------|----------------|
| **1.0** | Below Expectations | Significantly below A Player bar |
| **2.0** | Needs Improvement | Below A Player bar, requires development |
| **3.0** | Meets Expectations | A Player Baseline (meets bar) |
| **4.0** | Exceeds Expectations | Team Leader level performance |
| **5.0** | Best in Grade | Expert level, top performer |
| **6.0** | Haven't had opportunity to observe | Excluded from calculations |

**Important**: Score of 6.0 is NOT a rating—it's a "skip" indicator and is excluded from all averages, percentiles, and statistical calculations.

### Score Comparisons

Every report includes multiple comparison points to provide context:

#### Peers Average
**What it is**: Average score from all peer reviewers who rated this employee

**Example**: `Peers Average: 3.60 (based on 5 ratings)`

**Why it matters**: This is the most important baseline—how the people who work directly with this employee perceive their performance

#### Self Score
**What it is**: The score the employee gave themselves

**Example**: `Self Score: 3.0`

**Why it matters**: Combined with deltas, reveals self-awareness and calibration

#### Level Average
**What it is**: Average score for all employees at the same career level

**Example**: `Level Average: 4.09` (for Senior Practitioners)

**Why it matters**: Shows if the employee is performing above/below typical expectations for their level

#### Team Average
**What it is**: Average score for all employees on the same team

**Example**: `Team Average: 3.65` (for OSIT team)

**Why it matters**: Provides context for team-specific dynamics and performance norms

#### Department Average
**What it is**: Average score for all employees in the same practice/department

**Example**: `Department Average: 4.12` (for Design practice)

**Why it matters**: Shows how the employee compares to others in their functional area

#### Project Average
**What it is**: Average score for all employees on the same project/contract

**Example**: `Project Average: 3.69` (for SPOC/S35F project)

**Why it matters**: Provides context for project-specific challenges or dynamics

#### Company Average
**What it is**: Average score for all Rise8 employees across all departments, levels, teams

**Example**: `Company Average: 4.03`

**Why it matters**: The ultimate baseline—how this employee compares to the entire organization

---

## Understanding Deltas (Self-Awareness)

**TL;DR**: Deltas measure self-awareness by comparing self-scores to comparison groups. Negative = humble, near-zero = well-calibrated, positive = overconfident.

### What Are Deltas?

**Delta** = Self Score - Comparison Group Average

Deltas reveal whether an employee's self-assessment aligns with how others perceive them. This is a critical indicator of self-awareness and coachability.

### Delta Interpretation System

| Delta Value | Emoji | Label | Interpretation |
|-------------|-------|-------|----------------|
| **-0.10 or lower** | 🟢 | Humble | Rates self lower than comparison group (good self-awareness) |
| **-0.09 to +0.09** | 🟡 | Well-calibrated | Accurate self-assessment (excellent) |
| **+0.10 or higher** | 🔴 | Overconfident | Rates self higher than comparison group (potential blind spot) |

### Real Examples from Reports

#### Example 1: Humble Self-Assessment (Good)
```
Delta (Self - Peers): -0.15 🟢 (Humble)
```
**Translation**: Employee rated themselves 0.15 points lower than their peers rated them. This shows humility and realistic self-awareness.

#### Example 2: Well-Calibrated (Excellent)
```
Delta (Self - Team): +0.05 🟡 (Well-calibrated)
```
**Translation**: Employee's self-rating is nearly identical to their team average (within 0.09 points). This shows excellent self-awareness.

#### Example 3: Overconfident (Concern)
```
Delta (Self - Level): +0.33 🔴 (Overconfident)
```
**Translation**: Employee rated themselves 0.33 points higher than the average for their level. This may indicate a blind spot or inflated self-assessment.

### Answering the Key Question: "Is +0.33 a good thing or bad thing?"

**Answer**: +0.33 is a 🔴 **red flag** indicating overconfidence.

**Why it matters**:
- Suggests the employee may have blind spots about their performance
- May indicate difficulty receiving feedback or limited self-reflection
- Could signal misalignment with level expectations
- Often correlates with lower coachability

**What to do**:
- Discuss specific examples where self-perception differs from peer feedback
- Explore whether the employee understands expectations for their level
- Frame as a development opportunity (calibration conversations)
- Balance with qualitative feedback to understand context

### Pattern Analysis: Multiple Deltas

Each report shows 5 deltas per question:
1. Self - Peers
2. Self - Level
3. Self - Team
4. Self - Department
5. Self - Project

**Interpreting Patterns**:

| Pattern | What It Means | Action |
|---------|---------------|--------|
| **All 🟢 (negative)** | Very humble, may underestimate impact | Confidence coaching, highlight wins |
| **Mostly 🟡 (near-zero)** | Excellent self-awareness | Affirm, no action needed |
| **1-2 🔴 (positive)** | Isolated blind spots | Discuss specific areas, calibration |
| **3+ 🔴 (positive)** | Pattern of overconfidence | Structured feedback, development plan |
| **Mixed 🟢/🟡/🔴** | Context-dependent (normal) | Review specific dimensions |

### Why Deltas Matter for Leadership

Self-awareness is a leading indicator of:
- **Coachability**: Can they receive and act on feedback?
- **Growth potential**: Do they accurately assess development needs?
- **Team dynamics**: Do they understand their impact on others?
- **Promotion readiness**: Are they calibrated to next-level expectations?

**Best Practice**: Use deltas as conversation starters, not judgments. Explore the "why" behind the gap.

---

## Statistical Metrics Explained

**TL;DR**: Standard deviation = agreement level, percentile = company-wide ranking, median = typical reviewer perspective

### Standard Deviation (Reviewer Agreement)

**What it measures**: How much reviewers agree or disagree about this employee's performance

**Scale**:
- **0.0**: Perfect consensus (all identical scores) - rare
- **< 0.5**: High consensus (reviewers closely agree) - ideal
- **0.5-1.0**: Moderate variance (some disagreement) - common
- **> 1.0**: High variance (reviewers have very different perspectives) - investigate

**Examples**:

```
Standard Deviation: 0.40 (Moderate agreement)
```
**Translation**: Reviewers generally agree, with minor differences in perspective. Scores are clustered.

```
Standard Deviation: 0.80 (Mixed opinions)
```
**Translation**: Reviewers have noticeably different perspectives. Scores are more spread out.

```
Standard Deviation: 1.20 (High variance)
```
**Translation**: Reviewers have significantly different views. May indicate:
- Different contexts/projects with varied performance
- Role ambiguity (different people see different behaviors)
- Extreme performance (some see excellence, others see gaps)

**What to do with high variance (>1.0)**:
- Review score range to see extremes
- Check if reviewers are from different teams/projects
- Discuss with employee: "Different people see different things—why?"
- Look for context in qualitative feedback (Question 11 comments)

### Percentile Rank

**What it measures**: Where this employee ranks compared to ALL employees in the company on this specific question

**Scale**: 0th to 100th percentile
- **0th-25th**: Bottom quarter
- **25th-50th**: Below average
- **50th-75th**: Above average
- **75th-100th**: Top quarter

**Examples**:

```
Percentile Rank: 86.1th percentile
```
**Translation**: Scored higher than 86.1% of all employees company-wide on this question. Top 14%.

```
Percentile Rank: 22.7th percentile
```
**Translation**: Scored higher than only 22.7% of employees. Bottom 78%.

**Addressing the Question: "How does this get calculated with std dev of 0?"**

**Answer**: Percentile rank is calculated using ALL employees' peer averages company-wide, regardless of individual variance.

**Example**:
- Employee A: Peer average = 4.5 (all reviewers gave 5.0, std dev = 0)
- Company average: 3.67
- Even though Employee A has perfect consensus (std dev = 0), their 4.5 average is compared to the distribution of all 151 employees' averages
- If 130 employees scored below 4.5, Employee A ranks in the 86th percentile (130/151 = 86.1%)

**Key Point**: Standard deviation measures agreement among an individual's reviewers. Percentile rank measures where that individual's average falls in the company-wide distribution. They're independent metrics.

### Median Score

**What it measures**: The middle score when all peer scores for this question are sorted in order

**Addressing the Question: "Median score to what?"**

**Answer**: Median is the middle score from this employee's peer reviewers on this specific question.

**Example**:
```
Peer scores for Question 1: [3, 3, 4, 5, 5]
Median Score: 4.0
Peers Average: 4.0
```

**Why median matters**:
- **Less affected by outliers** than average
- **Shows typical reviewer perspective**
- **Useful when scores are spread out**

**Example with outlier**:
```
Peer scores: [2, 3, 3, 4, 5]
Median: 3.0 (middle value)
Average: 3.4 (influenced by the 2 and 5)
```

If median differs significantly from average, it suggests outlier scores are pulling the average up or down.

### Score Range & Spread

**What it measures**: Lowest and highest scores received, and the difference between them

**Examples**:

```
Score Range: 3.0 - 4.0 (spread: 1.0)
```
**Translation**: All reviewers scored between 3.0 and 4.0. Relatively tight range suggests consistency.

```
Score Range: 2.0 - 5.0 (spread: 3.0)
```
**Translation**: One reviewer gave 2.0, another gave 5.0. Large spread indicates very different perspectives.

**Interpreting Spread**:
- **Spread < 1.0**: High consistency
- **Spread 1.0-2.0**: Moderate variability (normal)
- **Spread > 2.0**: High variability (investigate context)

**When to investigate large spreads**:
- Check if reviewers are from different teams/projects
- Look for context clues in qualitative feedback
- Discuss with employee: "Some people see X, others see Y—why?"

---

## Tier Assignment System

**TL;DR**: Tier is 90% peer average + 10% self-awareness adjustment. It's algorithmic, not subjective, and should be treated as a starting point for discussion.

### Addressing the Question: "It would be helpful to know what went into this"

Here's the complete breakdown of how tiers are calculated.

### Data Inputs

**What IS Included**:
- ✅ **Quantitative**: Peer average scores across all 10 behavioral questions
- ✅ **Quantitative**: Self-awareness delta (calibration factor)
- ✅ **Qualitative**: AI synthesis of Questions 11 & 12 (accomplishments, feedback themes) - **informational only, does not affect tier calculation**

**What IS NOT Included**:
- ❌ Individual question breakdowns (only overall average matters)
- ❌ Project-specific context
- ❌ Level-specific competency matrices (known limitation - see [Addressing Common Questions](#addressing-common-questions))
- ❌ Subjective manager input
- ❌ Business outcomes or OKR achievement
- ❌ Tenure or longevity

### Tier Definitions

| Tier | Peer Average Range | Label | Description |
|------|-------------------|-------|-------------|
| **S** | 4.75+ | Supreme | Best in grade across all dimensions |
| **A+** | 4.25-4.74 | Exceptional | Consistently exceeds expectations |
| **A** | 3.75-4.24 | A Player | Solid A Player, reliable high performer |
| **A-** | 3.00-3.74 | A Player Baseline | Meets A Player bar, room to grow |
| **B** | 2.50-2.99 | B Player | Below A Player bar, needs improvement |
| **C** | < 2.50 | C Player | Significant performance concerns |

### Weighting Formula

**Primary Factor (90%)**: Peer Average Score
- Overall average of all 10 questions from peer reviewers
- Directly maps to tier range (e.g., 3.60 peer average = A- tier)

**Adjustment Factor (10%)**: Self-Awareness Delta
- Pattern of overconfidence (multiple 🔴 deltas) can lower tier by half-step
- Example: 4.25 peer average (A+ threshold) with 5+ red flags → adjusted to A tier
- Well-calibrated self-assessment (mostly 🟡) has no adjustment
- Humble self-assessment (mostly 🟢) has no adjustment

**Qualitative Synthesis**: Informational Only
- AI analysis of Questions 11-13 provides context and narrative
- Does NOT impact tier calculation
- Used for development planning and performance discussions
- Helps explain "why" behind the scores

### Example Tier Calculation

**Employee**: Anthony Zubia

**Step 1 - Calculate Peer Average**:
- Peer Average across 10 questions: 3.60

**Step 2 - Map to Tier Range**:
- 3.60 falls in 3.00-3.74 range → **A- (A Player Baseline)**

**Step 3 - Check Self-Awareness**:
- 5 questions with 🔴 (overconfident) deltas: +0.80, +0.20, +0.40, +0.80, +0.80
- Pattern of overconfidence detected
- Adjustment: None (3.60 is solidly within A- range; would need to be on threshold for adjustment)

**Step 4 - Final Tier**:
- **A- (A Player Baseline)**

**Step 5 - Qualitative Context** (informational):
- Accomplishments: Strong delivery, customer trust, contract renewal
- eNPS: 4.60 (above team/project average)
- Development: Pursue leadership roles, amplify voice in strategy

**Tier assignment reflects peer consensus (3.60), with qualitative synthesis providing the narrative for development planning.**

### Important Limitations

**Known Gap**: Level-Specific Competency Alignment

**The Question**: "I don't agree with this rating. The feedback focuses on likability and effort, not results expected at the Sr PM level."

**The Answer**: You're identifying a real limitation in the current system.

**What's Missing**:
- Integration with Lattice competency matrices for each role/level
- AI synthesis to map accomplishments to level-specific expectations
- Separate scoring dimension for "level-appropriate impact"
- Validation that accomplishments align with level requirements

**Current Reality**:
- Tier measures **overall performance** based on peer ratings
- Does NOT validate whether accomplishments align with **level expectations**
- Example: A Senior Practitioner could score 4.0 (A tier) based on effort and collaboration, but not demonstrate Senior-level strategic impact

**What This Means for Practice Leads**:
- **Tier is a starting point, not a final verdict**
- Manually review qualitative feedback (Questions 11-13) for level-appropriate contributions
- Ask: "Are the accomplishments/feedback aligned with what we expect from a [Level] in [Practice]?"
- Adjust final rating if tier doesn't reflect level-appropriate expectations
- Document your reasoning for any tier overrides in scorecard comments

**Future Roadmap** (not implemented):
- Integrate role/level competency matrices
- Add AI evaluation of accomplishments against level-specific criteria
- Create separate "level alignment" score dimension
- Weight tier calculation by level-appropriate impact, not just peer favorability

### Using Tiers Appropriately

**DO**:
- Use tier as a starting point for calibration discussions
- Cross-reference with qualitative feedback and accomplishments
- Consider level expectations when finalizing ratings
- Discuss tier with employee as part of performance conversation

**DON'T**:
- Treat tier as final, immutable verdict
- Ignore level-specific competency gaps
- Use tier as sole input for promotion/compensation decisions
- Assume all A-tier performers are equally ready for advancement

**Best Practice**: Tier + Qualitative Context + Level Expectations = Final Performance Rating

---

## Interpreting "Insufficient Data" Messages

**TL;DR**: Appears when < 3 peer responses for a question. Statistical significance requires minimum sample size. Focus on questions with sufficient data.

### When This Appears

You'll see "Insufficient Data" messages when:
- Fewer than 3 peer reviewers answered a specific question
- Response rate is too low for reliable statistical calculations

**Example**:
```
Question 5: Always Be Kind
Response Rate: 2/8 peer reviewers (25%)

⚠️ INSUFFICIENT DATA: This question has fewer than 3 responses.
Statistical metrics (percentile, standard deviation) are not reliable.
```

### Why This Matters

**Statistical Significance**:
- Percentiles, standard deviations, and averages require minimum sample size (n≥3)
- With 1-2 responses, a single outlier can skew results dramatically
- Example: 2 scores of [3, 5] → average 4.0, but highly unreliable

**Reliability**:
- Can't meaningfully calculate percentile rank with n<3
- Standard deviation is meaningless with n<3
- Comparisons to team/department/company are unreliable

### What Causes Insufficient Data

**Common Reasons**:
1. **Limited Peer Interaction**: Employee works in isolation or cross-functionally
2. **New Hire**: Recently joined, limited visibility
3. **Remote/Distributed Work**: Less direct observation by peers
4. **Specialized Role**: Few peers have context to evaluate specific dimensions
5. **Reviewers Skipping Questions**: Selecting "6 - Haven't had opportunity to observe"

### What to Do

**If you see frequent "Insufficient Data" messages**:

1. **Focus on Questions with Data**:
   - Prioritize questions with 3+ responses (higher reliability)
   - Look for patterns across questions that DO have data

2. **Investigate Root Cause**:
   - Why is peer visibility limited?
   - Is this a new hire? Cross-functional role?
   - Does the employee need more team integration?

3. **Gather Additional Context**:
   - Schedule 1-on-1s with employee and their closest collaborators
   - Review project work, deliverables, and outcomes directly
   - Seek input from managers/team leads who have direct visibility

4. **Consider Organizational Changes**:
   - Does employee need to be more integrated into team activities?
   - Are there opportunities for increased collaboration/visibility?
   - Is this a temporary state (new hire ramping up)?

### Example Scenario

**Employee**: New hire, 3 months tenure, 8 peer reviewers

**Results**:
- Questions 1-6: "Insufficient Data" (only 2 responses each)
- Questions 7-10: Sufficient data (5-6 responses)
- Question 11 (eNPS): 4 responses with positive comments

**Interpretation**:
- Early-stage assessment, limited behavioral visibility
- Focus on Questions 7-10 and qualitative feedback (Question 11)
- Revisit in 6 months when employee has more team integration
- Use this as baseline, not definitive performance assessment

**Action**:
- Note in performance discussion: "Early assessment, limited visibility"
- Set expectations for increased collaboration/visibility
- Reassess in next cycle with more complete data

---

## Addressing Common Questions

### Question 1: "Assuming ratings here are actually representing the number of questions responded to, not the number of assessor submissions, right?"

**Answer**: **Corrected in latest version.**

**What "Ratings" Means**:
- "Ratings" = number of unique peer reviewers who answered that specific question
- Example: "based on 5 ratings" = 5 unique people scored this question

**Important Clarification**:
- NOT the number of assessments submitted
- NOT the number of times the question was viewed
- It's the count of actual responses (excluding "6 - Haven't had opportunity to observe")

**Example**:
```
Response Rate: 5/8 peer reviewers (62.5%)
Peers Average: 3.60 (based on 5 ratings)
```
**Translation**: 8 people submitted assessments, but only 5 answered this question. The average (3.60) is based on those 5 responses.

### Question 2: "Is +0.33 a good thing or bad thing?"

**Answer**: +0.33 is a **🔴 red flag** indicating overconfidence.

**Why**:
- Self-score is 0.33 points higher than comparison group
- Threshold for overconfidence is +0.10
- Suggests potential blind spot or misalignment with expectations

**What to do**: See [Understanding Deltas](#understanding-deltas-self-awareness) section for detailed guidance.

### Question 3: "How does percentile get calculated with std dev of 0?"

**Answer**: Percentile and standard deviation measure different things.

**Standard Deviation**:
- Measures agreement among THIS employee's reviewers
- Example: All 5 reviewers gave 5.0 → average 5.0, std dev 0.0 (perfect consensus)

**Percentile Rank**:
- Compares THIS employee's average to ALL employees' averages company-wide
- Example: Employee average 5.0 ranks in 95th percentile if 95% of employees scored lower
- Calculated from distribution of 151 employees' averages, regardless of individual variance

**They're independent**: You can have perfect reviewer consensus (std dev 0) and still rank at any percentile.

### Question 4: "Median score to what?"

**Answer**: Median is the middle score from this employee's peer reviewers on this specific question.

**Example**:
- Peer scores: [3, 3, 4, 5, 5]
- Median: 4.0 (middle value when sorted)
- Average: 4.0

See [Statistical Metrics Explained](#statistical-metrics-explained) for detailed explanation.

### Question 5: "What does 'Insufficient Data' mean?"

**Answer**: Fewer than 3 peer responses for this question. Statistical metrics are unreliable with small sample sizes.

See [Interpreting "Insufficient Data" Messages](#interpreting-insufficient-data-messages) for detailed guidance.

### Question 6: "I don't agree with this rating. The feedback focuses on likability and effort, not results expected at the Sr PM level."

**Answer**: You're identifying a **known limitation** in the current system.

**The Problem**:
- Current tier system measures **overall performance** based on peer ratings
- Does NOT validate whether accomplishments align with **level-specific expectations**
- Does NOT incorporate competency matrices for each role/level

**What's Missing**:
- Integration with Lattice competency matrices
- AI synthesis to map accomplishments to level-specific criteria
- Separate scoring for "level-appropriate impact"
- Validation that work aligns with Senior Practitioner vs. Expert vs. Team Leader expectations

**What This Means for You**:
- Tier is a **starting point, not a final verdict**
- Manually review qualitative feedback (Questions 11-13) for level-appropriate contributions
- Ask: "Are the accomplishments aligned with what we expect from a [Level] in [Practice]?"
- Override tier if accomplishments don't match level expectations
- Document your reasoning in scorecard comments

**Example**:
- Employee scores 4.0 (A tier) based on collaboration and effort
- But accomplishments show execution work, not strategic impact expected at Senior level
- Practice Lead overrides to A- or B tier based on level misalignment
- Documents: "Strong peer ratings, but accomplishments not aligned with Senior PM expectations for strategic impact"

**Future Enhancement** (not implemented):
- Add level-specific competency evaluation
- Create separate "level alignment" score dimension
- Weight tier by level-appropriate impact, not just peer favorability

See [Tier Assignment System - Important Limitations](#tier-assignment-system) for more details.

---

## FAQ

### General Questions

**Q: How often should these reports be generated?**
A: EOY assessment cycle (annually), with potential mid-year check-ins if needed.

**Q: Can I share this report directly with the employee?**
A: Yes, but recommend discussing it in person first to provide context and answer questions. Reports contain sensitive peer feedback that should be framed constructively.

**Q: What if I disagree with the tier assignment?**
A: Tier is a starting point, not a mandate. You can override based on:
- Level-specific expectations (see Question 6 in Common Questions)
- Business outcomes not captured in peer ratings
- Context not visible in the data
- **Always document your reasoning** in scorecard comments.

**Q: How do I handle conflicting feedback (some peers love them, others have concerns)?**
A: Look at:
- Standard deviation (high = mixed opinions)
- Score range (wide = different perspectives)
- Qualitative feedback (Question 11 comments) for context
- Check if reviewers are from different projects/contexts
- Discuss with employee: "Different people see different things—why?"

### Score Interpretation Questions

**Q: What if peer average and self average differ significantly?**
A: This is what deltas measure. See [Understanding Deltas](#understanding-deltas-self-awareness) section. Large positive deltas (overconfidence) warrant calibration conversations. Large negative deltas (humility) may need confidence coaching.

**Q: Is a 3.0 average good or bad?**
A: 3.0 = "Meets Expectations" = A Player Baseline (A- tier). It's the minimum bar for A Player status. Not bad, but room to grow toward 3.75+ (A tier) or 4.25+ (A+ tier).

**Q: Why do some employees have low response rates?**
A: Common reasons:
- New hire (limited peer visibility)
- Cross-functional role (fewer direct collaborators)
- Remote/distributed work
- Specialized role (few peers qualified to evaluate)
- See [Interpreting "Insufficient Data" Messages](#interpreting-insufficient-data-messages)

**Q: What's a "good" percentile rank?**
A:
- **75th+**: Top quarter, strong performer
- **50th-75th**: Above average
- **25th-50th**: Below average, growth needed
- **<25th**: Bottom quarter, significant development required

**Q: Should I worry about high standard deviation (>1.0)?**
A: Yes, investigate:
- Review score range (extremes?)
- Check if reviewers from different teams/projects
- Look for context in qualitative feedback (Question 11)
- Discuss with employee: "Some people see X, others see Y—why?"
- High variance may indicate:
  - Context-dependent performance (great on some projects, struggles on others)
  - Role ambiguity (different people see different responsibilities)
  - Evolving performance (was struggling, now improving—or vice versa)

### Tier Questions

**Q: Can I override a tier assignment?**
A: Yes. Tier is algorithmic and serves as a starting point. Override if:
- Accomplishments don't align with level expectations
- Business outcomes warrant different rating
- Context not captured in peer ratings
- **Always document reasoning** in scorecard comments

**Q: What if tier doesn't align with my gut feeling?**
A: Investigate why:
- Read qualitative feedback (Questions 11-13) for context
- Check if level expectations are met (known gap)
- Review individual question scores (which dimensions are strong/weak?)
- Consider if your context differs from peer visibility
- Discuss with employee to understand their perspective

**Q: How often should tier assignments be reviewed?**
A: Annually (EOY cycle), with potential adjustments at:
- Mid-year check-ins (if significant performance change)
- Promotion discussions (level change = expectation change)
- Project transitions (context change may affect future ratings)

### Qualitative Feedback Questions

**Q: What if I disagree with the AI synthesis of Question 11/12?**
A:
- AI synthesis is a summary, not gospel
- Read raw comments (click "View Raw..." dropdowns)
- Trust your judgment if you have more context
- AI may miss nuances or overweight certain themes
- Use synthesis as starting point, raw feedback as source of truth

**Q: What if eNPS comments are overly positive but scores are low?**
A: Look for:
- **Likability vs. Performance**: Comments focus on personality, not results
- **Effort vs. Impact**: Comments praise effort, not outcomes
- **Potential vs. Delivery**: Comments note "promise" but not execution
- This pattern often indicates level misalignment (see Question 6)

**Q: What if START/STOP/KEEP recommendations conflict?**
A: Normal when reviewers have different contexts. Look for:
- Common themes across multiple reviewers
- Recommendations aligned with development goals
- Balance: Prioritize 1-2 START items, 1 STOP item, maintain KEEP behaviors

### Data Questions

**Q: What if I can't find the raw assessment file?**
A: File path shown in Report Metadata section:
- Location: `assessments/[Department]/[Employee_Name].md`
- Example: `assessments/Design/Anthony_Zubia.md`
- Contact admin if file is missing

**Q: How do I verify the tier calculation?**
A: Check:
- Peer average (Overall Scores section)
- Tier range (see [Tier Definitions](#tier-definitions) table)
- Self-awareness delta pattern (multiple 🔴 flags may adjust tier)
- Cross-reference with `tier_assignments.csv` (data source)

**Q: Can I request a report regeneration if data changes?**
A: Yes, contact admin. Script can be re-run if:
- Assessment data is corrected
- Team/project mapping is updated
- Employee level changes

---

## Best Practices for Using These Reports

### Before the Performance Discussion

1. **Read the Entire Report**
   - Don't just look at tier and overall scores
   - Review per-question breakdowns for patterns
   - Read all qualitative feedback (Questions 11-13)
   - Note questions with high variance or "Insufficient Data"

2. **Prepare Discussion Points**
   - Identify 2-3 key strengths from qualitative feedback
   - Identify 1-2 development areas from START/STOP recommendations
   - Prepare examples if you disagree with peer ratings
   - Draft questions about self-awareness deltas (if multiple 🔴)

3. **Check Level Alignment**
   - Ask: "Do accomplishments match what I expect from a [Level] in [Practice]?"
   - Compare to competency matrix for their role (manual step)
   - Note if tier needs adjustment based on level expectations

4. **Gather Additional Context**
   - Review project work, deliverables, OKRs
   - Talk to project leads/team members for additional perspective
   - Consider business outcomes not captured in peer ratings

### During the Performance Discussion

1. **Start with Strengths**
   - Share 2-3 key accomplishments from Question 13 synthesis
   - Highlight positive patterns in eNPS comments (Question 11)
   - Reinforce KEEP behaviors (Question 12)

2. **Present Scores as Data, Not Judgment**
   - "Here's how your peers rated you across 10 dimensions..."
   - "The data shows you're strong in X, with room to grow in Y..."
   - "Your self-assessment aligns closely with peers on A, B, C..."

3. **Explore Self-Awareness Deltas**
   - If multiple 🔴 (overconfident): "Let's talk about how you see yourself vs. how others see you..."
   - If multiple 🟢 (humble): "You're being harder on yourself than your peers are..."
   - If mostly 🟡 (well-calibrated): "You have excellent self-awareness..."

4. **Discuss Development Areas**
   - Focus on 1-2 START recommendations from peers
   - Explore 1 STOP behavior (if applicable)
   - Frame as growth opportunities, not failures

5. **Address Tier (If Appropriate)**
   - "Based on peer ratings, you're in the [Tier] range..."
   - "Here's what it would take to reach the next tier..."
   - If overriding tier: "I've adjusted your rating to [X] because [level expectations/business outcomes/context]..."

6. **Co-Create Development Plan**
   - Agree on 1-2 priority development goals
   - Reference specific START recommendations from peers
   - Set measurable outcomes for next cycle

### After the Performance Discussion

1. **Document Everything**
   - Scorecard comments should reference:
     - Key strengths (from report)
     - Development areas (from report)
     - Tier rationale (including any overrides)
     - Agreed-upon development goals

2. **Follow Up**
   - Schedule check-ins to track development progress
   - Revisit START/STOP/KEEP recommendations quarterly
   - Adjust goals if context changes

3. **Use for Calibration**
   - Share anonymized patterns with other Practice Leads
   - Discuss tier boundaries and level expectations
   - Ensure consistency across practice/department

### Common Pitfalls to Avoid

❌ **DON'T**:
- Rely solely on tier without reading qualitative feedback
- Ignore level expectations (see Question 6)
- Treat quantitative scores as absolute truth
- Share raw peer comments without context
- Make promotion/compensation decisions based on tier alone
- Dismiss employee's self-assessment as "wrong"

✅ **DO**:
- Use report as starting point for conversation
- Combine with your direct observations and context
- Consider level-appropriate expectations
- Frame feedback constructively
- Explore self-awareness gaps with curiosity
- Document your reasoning for any tier adjustments

### Using Reports for Calibration Meetings

**Before Calibration**:
1. Sort all reports by tier within your practice
2. Identify outliers (tier doesn't match your intuition)
3. Prepare to explain level-specific expectations
4. Bring examples of level-appropriate work

**During Calibration**:
1. Start with tier boundaries (A vs. A-, A+ vs. A)
2. Discuss outliers first (where tier doesn't align with expectations)
3. Share qualitative feedback patterns
4. Ensure consistency: "Is this A-tier Software Engineer comparable to that A-tier Software Engineer?"

**After Calibration**:
1. Document any tier adjustments and reasoning
2. Update scorecards with calibration notes
3. Communicate changes to affected employees

---

## Appendix: Quick Reference

### Tier Cheat Sheet

| Tier | Peer Average | Description |
|------|--------------|-------------|
| S | 4.75+ | Best in grade |
| A+ | 4.25-4.74 | Exceptional |
| A | 3.75-4.24 | Solid A Player |
| A- | 3.00-3.74 | A Player Baseline |
| B | 2.50-2.99 | Below A Player bar |
| C | <2.50 | Significant concerns |

### Delta Cheat Sheet

| Delta | Emoji | Label | Action |
|-------|-------|-------|--------|
| ≤-0.10 | 🟢 | Humble | Confidence coaching |
| -0.09 to +0.09 | 🟡 | Well-calibrated | Affirm |
| ≥+0.10 | 🔴 | Overconfident | Calibration discussion |

### Standard Deviation Cheat Sheet

| Std Dev | Label | Interpretation |
|---------|-------|----------------|
| <0.5 | High consensus | Reviewers agree |
| 0.5-1.0 | Moderate variance | Some disagreement (normal) |
| >1.0 | High variance | Investigate context |

### Response Rate Guidelines

| Response Rate | Interpretation | Action |
|---------------|----------------|--------|
| 80-100% | Excellent visibility | Trust the data |
| 50-79% | Good visibility | Use with confidence |
| 30-49% | Limited visibility | Supplement with 1-on-1s |
| <30% | Insufficient data | Focus on qualitative feedback |

---

## Document Metadata

- **Version**: 1.0.0
- **Last Updated**: December 4, 2025
- **Maintained By**: Assessment Analytics Team
- **Questions/Feedback**: Contact your Practice Lead or HR/People Ops

---

**End of Guide**
