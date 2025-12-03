# Rise8 EOY Assessment Analysis Results

**Analysis Date:** 2025-12-03
**Dataset:** 143 of 147 Risers (97.3% capture rate)
**Coverage:** All 13 departments across Rise8

---

## Quick Start

**For Executives:**
- Read: [EXECUTIVE_SUMMARY.md](./EXECUTIVE_SUMMARY.md) (10 min)
- Review: [TIER_SYSTEM_GUIDE.md](./TIER_SYSTEM_GUIDE.md) - Tier definitions section
- Action: [ACTIONABLE_INSIGHTS.md](./ACTIONABLE_INSIGHTS.md) - Immediate actions section

**For Department Leads:**
- Read: [EXECUTIVE_SUMMARY.md](./EXECUTIVE_SUMMARY.md) - Department comparison section
- Review: [tier_assignments.csv](./tier_assignments.csv) - Your team's tier distribution
- Reference: [TIER_SYSTEM_GUIDE.md](./TIER_SYSTEM_GUIDE.md) - How to use tiers in 1:1s

**For HR/People Ops:**
- Read: [ACTIONABLE_INSIGHTS.md](./ACTIONABLE_INSIGHTS.md) (full document)
- Review: [DISTRIBUTION_VISUALIZATIONS.md](./DISTRIBUTION_VISUALIZATIONS.md) - Statistical distributions
- Data: [riser_data_detailed.csv](./riser_data_detailed.csv) - Full dataset for HRIS integration

**For Data/Analytics:**
- Script: `/workspaces/lattice-eoy-assessment-review/scripts/comprehensive_analysis.py`
- Data: [riser_data_detailed.csv](./riser_data_detailed.csv)
- Visualizations: [DISTRIBUTION_VISUALIZATIONS.md](./DISTRIBUTION_VISUALIZATIONS.md)

---

## File Guide

### Primary Documents (Start Here)

#### 1. EXECUTIVE_SUMMARY.md
**Purpose:** High-level overview of company-wide performance
**Length:** 12 KB, ~15 min read
**Key Sections:**
- Overall performance distribution (mean: 4.100)
- Recommended tier system (S, A+, A, A-, B, C)
- Statistical insights (self-awareness, department comparison)
- Top performers and bottom performers
- Actionable recommendations

**Who Should Read:** Everyone (executives, leads, managers)

---

#### 2. TIER_SYSTEM_GUIDE.md
**Purpose:** Complete reference for tier definitions and usage
**Length:** 19 KB, ~25 min read
**Key Sections:**
- Tier definitions with examples (S through C)
- Who qualifies for each tier
- Department-specific tier distributions
- Self-awareness patterns by tier
- Usage guidelines for performance reviews
- FAQs

**Who Should Read:** Managers, HR, anyone conducting performance reviews

---

#### 3. ACTIONABLE_INSIGHTS.md
**Purpose:** Specific actions with timelines and success metrics
**Length:** 21 KB, ~30 min read
**Key Sections:**
- Immediate actions (30 days): B-tier development, overconfidence coaching, S-tier recognition
- Strategic initiatives (90 days): Tier rollout, department calibration, self-awareness program
- Continuous monitoring: Quarterly tracking, response quality maintenance
- Risk mitigation: Flight risk, performance risk
- Communication guidelines

**Who Should Read:** HR, People Ops, Department Leads, Executives

---

#### 4. DISTRIBUTION_VISUALIZATIONS.md
**Purpose:** Visual representations of statistical data
**Length:** 20 KB, ~20 min read
**Key Sections:**
- Score distribution histogram (ASCII visualization)
- Tier distribution pie chart
- Department comparison box plots
- Self vs peer delta scatter plots
- Response rate impact analysis
- Percentile reference charts

**Who Should Read:** Data-oriented stakeholders, those wanting deeper statistical understanding

---

### Data Files

#### 5. riser_data_detailed.csv
**Purpose:** Complete dataset with all metrics
**Size:** 7.9 KB, 143 rows + header
**Columns:**
- Name, Department
- Peer_Average, Self_Average, Delta
- Response_Count, Response_Total, Response_Pct
- Total_Ratings

**Use Cases:**
- HRIS integration
- Custom analysis
- Trend tracking over time
- Department-level reports

---

#### 6. tier_assignments.csv
**Purpose:** Tier assignments for each Riser
**Size:** 7.2 KB, 143 rows + header
**Columns:**
- Name, Department, Peer_Average, Tier, Tier_Name

**Use Cases:**
- Distribution to department leads
- Performance review preparation
- Compensation/promotion decisions
- Tracking tier movement over time

---

#### 7. analysis_summary.txt
**Purpose:** Plain-text summary of analysis output
**Size:** 358 bytes
**Contents:** Basic statistical summary from analysis script

**Use Cases:** Quick reference, script validation

---

## Key Findings Summary

### Company Performance
- **Mean Score:** 4.100 (Strong A Player performance)
- **Median Score:** 4.170 (Positive skew toward high performance)
- **A Player Baseline (3.0) Validation:** 98.6% of Risers meet or exceed
- **Below Baseline:** Only 2 Risers (1.4%) - Kyle Smart, Shawn Kilroy

### Tier Distribution
- **S-Tier (4.75+):** 3 Risers (2.1%) - Andrew Knife, Peter Duong, Luke Strebel
- **A+ Tier (4.58-4.75):** 12 Risers (8.4%) - Top 10% of company
- **A Tier (4.25-4.58):** 45 Risers (31.5%) - Solid performers
- **A- Tier (3.00-4.25):** 81 Risers (56.6%) - Meeting baseline
- **B Tier (2.00-3.00):** 2 Risers (1.4%) - Needs development
- **C Tier (<2.00):** 0 Risers (0.0%) - None

### Self-Awareness Patterns
- **Humble/Growth Mindset (Δ < -0.3):** 39.2% of Risers
- **Accurate Self-Assessment (-0.3 ≤ Δ ≤ 0.3):** 41.3% of Risers
- **Overconfident (Δ > 0.3):** 19.6% of Risers
- **Key Pattern:** High performers are humble (avg Δ: -0.334), low performers overconfident (avg Δ: +0.547)

### Department Performance
- **Highest:** Enablement (4.47), Delivery (4.37), Executive (4.34)
- **Lowest:** Customer-Success (3.74), IT (3.80), Software (3.96)
- **Most Consistent:** Enablement (σ=0.166), Growth (σ=0.120)
- **Most Variable:** Customer-Success (σ=1.141), IT (σ=0.764)

### Response Rates
- **Mean Response Rate:** 92.5%
- **Median Response Rate:** 96.0%
- **Mean Response Count:** 60.9 responses per Riser
- **High Confidence:** 97.3% of Risers have ≥20 responses

---

## Immediate Action Items

### Priority 1: B-Tier Development (CRITICAL)
- **Who:** Kyle Smart (Software, 2.83), Shawn Kilroy (Customer-Success, 2.44)
- **Timeline:** 90-day development plans, weekly check-ins
- **Goal:** Movement to 3.0+ range or separation decision

### Priority 2: Overconfidence Coaching (HIGH)
- **Who:** Ryan Tuck (Δ=+1.64), Michael Maye (Δ=+1.37), Samuel McQueen (Δ=+1.00)
- **Timeline:** Immediate 1:1s, monthly progress reviews
- **Goal:** Reduce delta to ±0.5 range, improve self-awareness

### Priority 3: S-Tier Recognition (RETENTION)
- **Who:** Andrew Knife (4.91), Peter Duong (4.76), Luke Strebel (4.75)
- **Timeline:** Week 1 company-wide recognition, Week 2 executive 1:1s
- **Goal:** Maximum retention, career trajectory discussions

### Priority 4: Humble High Performer Celebration (CULTURE)
- **Who:** Ainsilie Hibbard (Δ=-1.92), Jordan Dilworth (Δ=-1.42), Vanessa Ten-Kate (Δ=-1.42), et al
- **Timeline:** Month 1 feature in communications, ongoing encouragement
- **Goal:** Reinforce growth mindset culture, build confidence

---

## How to Use This Analysis

### For Performance Reviews
1. Look up Riser in [tier_assignments.csv](./tier_assignments.csv)
2. Reference tier definition in [TIER_SYSTEM_GUIDE.md](./TIER_SYSTEM_GUIDE.md)
3. Use language from Communication Guidelines section
4. Focus on behaviors/outcomes, not tier labels
5. Set goals for tier advancement if applicable

### For Compensation Decisions
1. Review tier and percentile placement
2. Consider tenure, trajectory, market conditions
3. Use tier as **one input**, not sole determinant
4. Reference compensation guidelines in [ACTIONABLE_INSIGHTS.md](./ACTIONABLE_INSIGHTS.md)

### For Promotion Decisions
1. Check current tier and trajectory over time
2. Assess readiness beyond just tier placement
3. S/A+ tier = strong candidates
4. A tier = ready if 12+ months + trajectory
5. A-/B tier = improve first, then reassess

### For Project Assignments
1. Match project complexity to tier
2. S/A+ = highest impact, most complex
3. A = important projects, growth opportunities
4. A- = standard projects, development focus
5. B = lower-risk projects, close oversight

---

## Reproducing the Analysis

### Run the Analysis Script
```bash
cd /workspaces/lattice-eoy-assessment-review
python3 scripts/comprehensive_analysis.py
```

**Output Location:** `/workspaces/lattice-eoy-assessment-review/docs/analysis-results/`

### Script Capabilities
- Parses all 147 assessment markdown files
- Calculates company-wide statistics (mean, median, std dev, percentiles)
- Analyzes response rates and confidence levels
- Compares department performance
- Identifies self vs peer delta patterns
- Recommends tier definitions based on distribution
- Generates CSV files and text summaries

### Customization Options
Edit `/workspaces/lattice-eoy-assessment-review/scripts/comprehensive_analysis.py`:
- Adjust tier boundaries (lines 450-500)
- Modify statistical calculations (lines 100-150)
- Add new analyses (extend methods)
- Change output formats (lines 550-650)

---

## Data Quality Notes

### Successfully Parsed
- **143 of 147 Risers** (97.3%)
- **All 13 departments** represented
- **111 Risers** (77.6%) have complete response rate data

### Missing Data
**4 Risers missing peer or self-assessment:**
- Lakshmi Sadasiv (Enablement) - No peer average
- Kenny Kay (Finance) - No peer average
- Ron Golan (Product-Management) - No self average
- Yechiel Kalmenson (Software) - No self average

**32 Risers missing response rate metadata:**
- Still have valid peer average scores
- Response rate data not required for tier assignment
- Primarily affects statistical confidence analysis

### Data Integrity
- All scores validated within 1-5 scale
- Delta calculations verified (Self - Peer)
- Department assignments confirmed
- No duplicate entries detected

---

## Comparison to Previous Analysis

**Session 002 (110 Risers) → Session 003 (143 Risers)**

| Metric | Session 002 | Session 003 | Change |
|--------|-------------|-------------|--------|
| Sample Size | 110 | 143 | +33 (+30.0%) |
| Mean Score | 4.082 | 4.100 | +0.018 |
| Median Score | 4.090 | 4.170 | +0.080 |
| Std Dev | 0.415 | 0.425 | +0.010 |
| Below 3.0 | 1 (0.9%) | 2 (1.4%) | +1 (+0.5%) |
| P90 (A+ boundary) | 4.580 | 4.580 | No change |
| P99 (S boundary) | 4.760 | 4.760 | No change |

**Key Insights:**
- Adding 33 Risers slightly raised mean and median (higher performing additions)
- 3.0 baseline remains valid (98.6% above threshold)
- Tier boundaries stable and well-calibrated
- Second low performer identified (Shawn Kilroy, 2.44)

---

## Statistical Methodology

### Distribution Analysis
- **Measures of Central Tendency:** Mean, median, mode
- **Measures of Dispersion:** Range, variance, standard deviation, IQR
- **Percentiles:** Q1 (25th), Q2 (50th), Q3 (75th), P90, P95, P99
- **Shape:** Skewness (positive), kurtosis (platykurtic)

### Response Rate Analysis
- **Confidence Intervals:** Based on sample size and standard error
- **Margin of Error:** 1.96 × (σ / √n) for 95% confidence
- **Statistical Validity:** Minimum 20 responses recommended for HIGH confidence

### Self-Awareness Analysis
- **Delta Calculation:** Self Average - Peer Average
- **Categorization:** Humble (Δ < -0.3), Accurate (-0.3 ≤ Δ ≤ 0.3), Overconfident (Δ > 0.3)
- **Correlation:** Inverse relationship between performance and delta

### Tier Calibration
- **Method:** Percentile-based with statistical validation
- **S-Tier:** 99th percentile (top 1-2%)
- **A+ Tier:** 90-98th percentile (top 10%)
- **A Tier:** 60-90th percentile (solid performers)
- **A- Tier:** 3.0 baseline to 60th percentile
- **B Tier:** 2.0 to 3.0 (below baseline)
- **C Tier:** <2.0 (critical)

---

## Future Analysis Recommendations

### Next Assessment Cycle
1. **Maintain data format consistency** (especially response rate metadata)
2. **Track tier movement** (who moved up/down and why)
3. **Monitor self-awareness trends** (delta changes over time)
4. **Assess department calibration** (variance reduction)
5. **Validate tier boundaries** (adjust if distribution shifts significantly)

### Additional Analyses to Consider
1. **Tenure Analysis:** Performance vs time at Rise8
2. **Role Analysis:** Performance by role (engineer, PM, designer, etc.)
3. **Project Performance:** Correlation with delivery outcomes
4. **Customer Feedback:** Alignment with peer assessments
5. **Compensation Equity:** Ensure tier alignment with pay

### Continuous Improvement
1. **Quarterly Pulse Checks:** Mini-assessments to track trends
2. **Development Tracking:** Monitor B-tier and lower A- tier progress
3. **Retention Monitoring:** Track S/A+ tier turnover closely
4. **Culture Metrics:** Maintain growth mindset (humble self-assessments)

---

## Questions or Issues?

**Analysis Questions:** Review detailed methodology in each document
**Data Questions:** Check [riser_data_detailed.csv](./riser_data_detailed.csv) for source data
**Interpretation Questions:** See [TIER_SYSTEM_GUIDE.md](./TIER_SYSTEM_GUIDE.md) FAQs
**Technical Questions:** Review `/workspaces/lattice-eoy-assessment-review/scripts/comprehensive_analysis.py`

---

## Document Change Log

**2025-12-03:** Initial analysis complete
- 143 Risers analyzed
- Tier system recommendations finalized
- All documentation generated
- Data files exported

---

**Analysis Complete**
**Total Analysis Time:** ~2 hours
**Output Files:** 7 files (4 markdown documents, 3 data files)
**Total Size:** 72 KB documentation + analysis script

For questions or to re-run analysis, reference:
- Analysis script: `/workspaces/lattice-eoy-assessment-review/scripts/comprehensive_analysis.py`
- Source data: `/workspaces/lattice-eoy-assessment-review/assessments/`
