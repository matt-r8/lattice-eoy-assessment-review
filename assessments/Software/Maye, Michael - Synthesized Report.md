# Michael Maye - Individual Assessment Report

## Employee Information
- **Name**: Michael Maye
- **Department**: Software
- **Level**: Practitioner II
- **Team**: Beach
- **Project**: Overhead
- **Assessment Period**: 2025 EOY
- **Tier Assignment**: D (Needs Significant Improvement)

---

## Overall Scores

- **Peers Average**: 3.08 (based on 36 ratings)
- **Response Rate**: 4/4 peer reviewers (100%)
- **Self Average**: 4.45
- **Delta (Self - Peers)**: +1.37 🔴 (Overconfident)
- **Delta (Self - Level)**: +0.66 🔴 (Overconfident) (vs Level Average 3.79)
- **Delta (Self - Team)**: +0.83 🔴 (Overconfident) (vs Team Average 3.62)
- **Delta (Self - Department)**: +0.48 🔴 (Overconfident) (vs Department Average 3.97)
- **Delta (Self - Project)**: +0.32 🔴 (Overconfident) (vs Project Average 4.13)

---

## Accomplishments Review (Self-Assessment Question 13)

### Synthesized Summary

*[AI synthesis needed - invoke rise8-assessment-reviewer agent with accomplishments text]*

<details>
<summary>View Raw Accomplishments Text</summary>

**1. Resurrecting the EKS Production Environment & Building a New Foundation**
**Situation:** The internal employee site’s EKS cluster went down, impacting production access and threatening ongoing work. I had no prior AWS/Kubernetes experience, and platform had no bandwidth to respond.
**Task:** Diagnose and restore production service stability without existing Terraform/Helm configs, while minimizing impact on operations.
**Action:**
- Worked late nights for nearly a week to self-teach AWS, EKS, ECS, load balancers, and virtual networking.
- Traced obscure target group registration failures to deprecated instance types after days of deep investigation.
- Validated a fix in staging, updated instance type configurations, and restored the cluster.
- Implemented a circuit-breaker fallback in GitHub Actions to prevent repeat outages.
- Began leading the migration from EKS Self-Managed to ECS to eliminate root causes entirely.
**Result:**
- Full restoration of production with **zero data loss**.
- **Reduced operational burden** on the platform team by owning the migration.
- **Improved future time-to-restore** through workflow improvements.
- Established a stable ECS foundation that other applications can now deploy on with minimal setup.




**2. Unblocking the WinTAK Prototype Through Deep Technical Investigation**
**Situation:** A core KMZ export feature was producing geographically misaligned output, threatening the success of the building-detection prototype.
**Task:** Fix an issue that had no documentation, no examples, and no clear root cause—under a tight delivery window.
**Action:**
- Decompiled and traced WinTAK code paths to understand undocumented projection logic.
- Validated MapGL’s projection functions and reverse-projection accuracy.
- Diagnosed subtle pixel-coordinate misalignment between MapGL and GL capture systems.
- Implemented a corrective transformation that made outputs accurate enough for the AI SDK to function reliably.
**Result:**
- **Unblocked core feature of prototype**, enabling an on-time delivery with accurate building detections.
- Prevented a likely failed customer review of WinTak and potential loss of confidence.
- Demonstrated significant growth in autonomy, technical depth, and problem-solving under ambiguity.




**3. Sustaining High Performance Through a 7-Month Active Duty Training Period and Seamless Reintegration**
**Situation:**
I was required to transition to a 7-month active-duty training cycle as part of my military service, attending full-time cybersecurity analyst instruction: 8 hours of high-intensity classroom work daily, combined with military duties and performance expectations.
**Task:**
Remain a contributing member of Rise8, support ongoing internal initiatives, and ensure a smooth return to full-time engineering work—without letting either commitment slip in quality.
**Action:**
- Maintained part-time contributions to an internal project during the entire training period, staying engaged with the team and continuing to ship meaningful work.
- Balanced full-time military academic load with professional responsibilities, continuously communicating status, delivering work asynchronously, and remaining available for key discussions.
- Graduated **top of my class**, demonstrating mastery of new cybersecurity knowledge while upholding Rise8 quality and reliability.
- Immediately reintegrated into full-time engineering upon return, joining the WinTAK project and quickly delivering high-complexity contributions that helped the team achieve a successful final prototype.
**Result:**
- Demonstrated **exceptional grit and consistency**, maintaining performance in two high-demand environments simultaneously.
- Preserved team continuity and momentum during an extended part-time period.
- Returned to Rise8 at full speed, with **zero ramp-up time**, contributing immediately to mission-critical work.
- Strengthened the company’s cybersecurity posture with newly acquired, formally trained expertise.
This accomplishment shows that even under extreme external demands, I remained aligned with the mission, upheld Rise8 standards, and continued delivering high-impact outcomes without compromise.

</details>

---

## Per-Question Breakdown

### Question 1: Be Bold

**Basic Scores:**
- **Peers Average**: 3.33 (based on 3 ratings)
- **Response Rate**: 3/4 peer reviewers (75%)
- **Self Score**: 4.0
- **Median Score**: 3.00

**Self-Awareness Deltas:**
- **Delta (Self - Peers)**: +0.67 🔴 (Overconfident)
- **Delta (Self - Level)**: +0.25 🔴 (Overconfident)
- **Delta (Self - Team)**: +0.14 🔴 (Overconfident)
- **Delta (Self - Department)**: +0.16 🔴 (Overconfident)
- **Delta (Self - Project)**: -0.07 🟡 (Well-calibrated)

**Performance Comparisons (Peer Avg vs Groups):**
- **vs Team Average**: -0.53 (Team avg: 3.86) - Below team
- **vs Project Average**: -0.74 (Project avg: 4.07) - Below project
- **vs Department Average**: -0.51 (Department avg: 3.84) - Below department
- **vs Company Average**: -0.69 (Company avg: 4.03) - Below company

**Statistical Analysis:**
- **Standard Deviation**: 0.47 (Moderate agreement)
- **Percentile Rank**: 9.2th percentile
- **Score Range**: 3.0 - 4.0 (spread: 1.0)

**Interpretation:**
- Scores in the **bottom 91%** on Be Bold company-wide (top 9%)
- Peer average (3.33) is **-0.74 below project average**
- **Moderate agreement** among reviewers (SD: 0.47)
- Score range (3.0-4.0) shows reasonable consistency in reviewer perceptions

### Question 2: Do The Right Thing

**Basic Scores:**
- **Peers Average**: 3.33 (based on 3 ratings)
- **Response Rate**: 3/4 peer reviewers (75%)
- **Self Score**: 5.0
- **Median Score**: 3.00

**Self-Awareness Deltas:**
- **Delta (Self - Peers)**: +1.67 🔴 (Overconfident)
- **Delta (Self - Level)**: +1.15 🔴 (Overconfident)
- **Delta (Self - Team)**: +1.05 🔴 (Overconfident)
- **Delta (Self - Department)**: +0.98 🔴 (Overconfident)
- **Delta (Self - Project)**: +0.68 🔴 (Overconfident)

**Performance Comparisons (Peer Avg vs Groups):**
- **vs Team Average**: -0.61 (Team avg: 3.95) - Below team
- **vs Project Average**: -0.99 (Project avg: 4.32) - Below project
- **vs Department Average**: -0.69 (Department avg: 4.02) - Below department
- **vs Company Average**: -0.89 (Company avg: 4.22) - Below company

**Statistical Analysis:**
- **Standard Deviation**: 0.47 (Moderate agreement)
- **Percentile Rank**: 3.8th percentile
- **Score Range**: 3.0 - 4.0 (spread: 1.0)

**Interpretation:**
- Scores in the **bottom 97%** on Do The Right Thing company-wide (top 4%)
- Peer average (3.33) is **-0.99 below project average**
- **Moderate agreement** among reviewers (SD: 0.47)
- Score range (3.0-4.0) shows reasonable consistency in reviewer perceptions

### Question 3: Do What Works

**Basic Scores:**
- **Peers Average**: 3.00 (based on 3 ratings)
- **Response Rate**: 3/4 peer reviewers (75%)
- **Self Score**: 4.0
- **Median Score**: 3.00

**Self-Awareness Deltas:**
- **Delta (Self - Peers)**: +1.00 🔴 (Overconfident)
- **Delta (Self - Level)**: +0.18 🔴 (Overconfident)
- **Delta (Self - Team)**: +0.08 🟡 (Well-calibrated)
- **Delta (Self - Department)**: +0.26 🔴 (Overconfident)
- **Delta (Self - Project)**: -0.00 🟡 (Well-calibrated)

**Performance Comparisons (Peer Avg vs Groups):**
- **vs Team Average**: -0.92 (Team avg: 3.92) - Below team
- **vs Project Average**: -1.00 (Project avg: 4.00) - Below project
- **vs Department Average**: -0.74 (Department avg: 3.74) - Below department
- **vs Company Average**: -0.97 (Company avg: 3.97) - Below company

**Statistical Analysis:**
- **Standard Deviation**: 0.00 (High consensus)
- **Percentile Rank**: 2.1th percentile
- **Score Range**: 3.0 - 3.0 (spread: 0.0)

*Perfect consensus - all reviewers gave identical scores*

### Question 4: Do What is Required

**Basic Scores:**
- **Peers Average**: 3.33 (based on 3 ratings)
- **Response Rate**: 3/4 peer reviewers (75%)
- **Self Score**: 4.0
- **Median Score**: 3.00

**Self-Awareness Deltas:**
- **Delta (Self - Peers)**: +0.67 🔴 (Overconfident)
- **Delta (Self - Level)**: +0.27 🔴 (Overconfident)
- **Delta (Self - Team)**: +0.33 🔴 (Overconfident)
- **Delta (Self - Department)**: +0.05 🟡 (Well-calibrated)
- **Delta (Self - Project)**: -0.15 🟢 (Humble)

**Performance Comparisons (Peer Avg vs Groups):**
- **vs Team Average**: -0.34 (Team avg: 3.67) - Below team
- **vs Project Average**: -0.81 (Project avg: 4.15) - Below project
- **vs Department Average**: -0.61 (Department avg: 3.95) - Below department
- **vs Company Average**: -0.77 (Company avg: 4.10) - Below company

**Statistical Analysis:**
- **Standard Deviation**: 0.47 (Moderate agreement)
- **Percentile Rank**: 7.4th percentile
- **Score Range**: 3.0 - 4.0 (spread: 1.0)

**Interpretation:**
- Scores in the **bottom 93%** on Do What is Required company-wide (top 7%)
- Peer average (3.33) is **-0.81 below project average**
- **Moderate agreement** among reviewers (SD: 0.47)
- Score range (3.0-4.0) shows reasonable consistency in reviewer perceptions

### Question 5: Always Be Kind

**Basic Scores:**
- **Peers Average**: 3.50 (based on 2 ratings)
- **Response Rate**: 2/4 peer reviewers (50%)
- **Self Score**: 5.0
- **Median Score**: 3.50

**Self-Awareness Deltas:**
- **Delta (Self - Peers)**: +1.50 🔴 (Overconfident)
- **Delta (Self - Level)**: +1.08 🔴 (Overconfident)
- **Delta (Self - Team)**: +0.92 🔴 (Overconfident)
- **Delta (Self - Department)**: +1.06 🔴 (Overconfident)
- **Delta (Self - Project)**: +0.77 🔴 (Overconfident)

**Performance Comparisons (Peer Avg vs Groups):**
- **vs Team Average**: -0.58 (Team avg: 4.08) - Below team
- **vs Project Average**: -0.73 (Project avg: 4.23) - Below project
- **vs Department Average**: -0.44 (Department avg: 3.94) - Below department
- **vs Company Average**: -0.64 (Company avg: 4.14) - Below company

**Statistical Analysis:**
- **Standard Deviation**: 0.50 (Moderate agreement)
- **Percentile Rank**: 8.4th percentile
- **Score Range**: 3.0 - 4.0 (spread: 1.0)

*Insufficient data for interpretation (minimum 3 responses needed)*

### Question 6: Keep it Real

**Basic Scores:**
- **Peers Average**: 3.50 (based on 2 ratings)
- **Response Rate**: 2/4 peer reviewers (50%)
- **Self Score**: 4.0
- **Median Score**: 3.50

**Self-Awareness Deltas:**
- **Delta (Self - Peers)**: +0.50 🔴 (Overconfident)
- **Delta (Self - Level)**: +0.22 🔴 (Overconfident)
- **Delta (Self - Team)**: -0.09 🟡 (Well-calibrated)
- **Delta (Self - Department)**: +0.03 🟡 (Well-calibrated)
- **Delta (Self - Project)**: -0.20 🟢 (Humble)

**Performance Comparisons (Peer Avg vs Groups):**
- **vs Team Average**: -0.59 (Team avg: 4.09) - Below team
- **vs Project Average**: -0.70 (Project avg: 4.20) - Below project
- **vs Department Average**: -0.47 (Department avg: 3.97) - Below department
- **vs Company Average**: -0.67 (Company avg: 4.17) - Below company

**Statistical Analysis:**
- **Standard Deviation**: 0.50 (Moderate agreement)
- **Percentile Rank**: 8.4th percentile
- **Score Range**: 3.0 - 4.0 (spread: 1.0)

*Insufficient data for interpretation (minimum 3 responses needed)*

### Question 7: Outcomes in Production

**Basic Scores:**
- **Peers Average**: 3.00 (based on 1 ratings)
- **Response Rate**: 1/4 peer reviewers (25%)
- **Self Score**: 4.0
- **Median Score**: 3.00

**Self-Awareness Deltas:**
- **Delta (Self - Peers)**: +1.00 🔴 (Overconfident)
- **Delta (Self - Level)**: +0.33 🔴 (Overconfident)
- **Delta (Self - Team)**: +0.13 🔴 (Overconfident)
- **Delta (Self - Department)**: +0.08 🟡 (Well-calibrated)
- **Delta (Self - Project)**: +0.00 🟡 (Well-calibrated)

**Performance Comparisons (Peer Avg vs Groups):**
- **vs Team Average**: -0.87 (Team avg: 3.87) - Below team
- **vs Project Average**: -1.00 (Project avg: 4.00) - Below project
- **vs Department Average**: -0.92 (Department avg: 3.92) - Below department
- **vs Company Average**: -0.98 (Company avg: 3.98) - Below company

**Statistical Analysis:**
- **Standard Deviation**: 0.00 (High consensus)
- **Percentile Rank**: 2.1th percentile
- **Score Range**: 3.0 - 3.0 (spread: 0.0)

*Insufficient data for interpretation (minimum 3 responses needed)*

### Question 8: Grit

**Basic Scores:**
- **Peers Average**: 4.00 (based on 2 ratings)
- **Response Rate**: 2/4 peer reviewers (50%)
- **Self Score**: 5.0
- **Median Score**: 4.00

**Self-Awareness Deltas:**
- **Delta (Self - Peers)**: +1.00 🔴 (Overconfident)
- **Delta (Self - Level)**: +1.09 🔴 (Overconfident)
- **Delta (Self - Team)**: +1.18 🔴 (Overconfident)
- **Delta (Self - Department)**: +0.95 🔴 (Overconfident)
- **Delta (Self - Project)**: +0.73 🔴 (Overconfident)

**Performance Comparisons (Peer Avg vs Groups):**
- **vs Team Average**: +0.18 (Team avg: 3.82) - Above team
- **vs Project Average**: -0.27 (Project avg: 4.27) - Below project
- **vs Department Average**: -0.05 (Department avg: 4.05) - At department
- **vs Company Average**: -0.16 (Company avg: 4.16) - Below company

**Statistical Analysis:**
- **Standard Deviation**: 1.00 (Mixed opinions)
- **Percentile Rank**: 35.7th percentile
- **Score Range**: 3.0 - 5.0 (spread: 2.0)

*Insufficient data for interpretation (minimum 3 responses needed)*

### Question 9: Growth Mindset

**Basic Scores:**
- **Peers Average**: 3.33 (based on 3 ratings)
- **Response Rate**: 3/4 peer reviewers (75%)
- **Self Score**: 5.0
- **Median Score**: 3.00

**Self-Awareness Deltas:**
- **Delta (Self - Peers)**: +1.67 🔴 (Overconfident)
- **Delta (Self - Level)**: +1.15 🔴 (Overconfident)
- **Delta (Self - Team)**: +1.29 🔴 (Overconfident)
- **Delta (Self - Department)**: +0.93 🔴 (Overconfident)
- **Delta (Self - Project)**: +0.76 🔴 (Overconfident)

**Performance Comparisons (Peer Avg vs Groups):**
- **vs Team Average**: -0.38 (Team avg: 3.71) - Below team
- **vs Project Average**: -0.90 (Project avg: 4.24) - Below project
- **vs Department Average**: -0.74 (Department avg: 4.07) - Below department
- **vs Company Average**: -0.86 (Company avg: 4.19) - Below company

**Statistical Analysis:**
- **Standard Deviation**: 0.47 (Moderate agreement)
- **Percentile Rank**: 2.4th percentile
- **Score Range**: 3.0 - 4.0 (spread: 1.0)

**Interpretation:**
- Scores in the **bottom 98%** on Growth Mindset company-wide (top 2%)
- Peer average (3.33) is **-0.90 below project average**
- **Moderate agreement** among reviewers (SD: 0.47)
- Score range (3.0-4.0) shows reasonable consistency in reviewer perceptions

### Question 10: No Unnecessary Rules

**Basic Scores:**
- **Peers Average**: 3.33 (based on 3 ratings)
- **Response Rate**: 3/4 peer reviewers (75%)
- **Self Score**: 4.0
- **Median Score**: 3.00

**Self-Awareness Deltas:**
- **Delta (Self - Peers)**: +0.67 🔴 (Overconfident)
- **Delta (Self - Level)**: +0.14 🔴 (Overconfident)
- **Delta (Self - Team)**: +0.06 🟡 (Well-calibrated)
- **Delta (Self - Department)**: +0.02 🟡 (Well-calibrated)
- **Delta (Self - Project)**: -0.16 🟢 (Humble)

**Performance Comparisons (Peer Avg vs Groups):**
- **vs Team Average**: -0.61 (Team avg: 3.94) - Below team
- **vs Project Average**: -0.82 (Project avg: 4.16) - Below project
- **vs Department Average**: -0.65 (Department avg: 3.98) - Below department
- **vs Company Average**: -0.78 (Company avg: 4.11) - Below company

**Statistical Analysis:**
- **Standard Deviation**: 0.47 (Moderate agreement)
- **Percentile Rank**: 3.5th percentile
- **Score Range**: 3.0 - 4.0 (spread: 1.0)

**Interpretation:**
- Scores in the **bottom 97%** on No Unnecessary Rules company-wide (top 4%)
- Peer average (3.33) is **-0.82 below project average**
- **Moderate agreement** among reviewers (SD: 0.47)
- Score range (3.0-4.0) shows reasonable consistency in reviewer perceptions

### Question 11: eNPS (Employee Net Promoter Score)

**Basic Scores:**
- **Peers Average**: 4.50 (based on 2 ratings)
- **Response Rate**: 2/4 peer reviewers (50%)
- **Self Score**: 5.0
- **Median Score**: 4.50

**Self-Awareness Deltas:**
- **Delta (Self - Peers)**: +0.50 🔴 (Overconfident)
- **Delta (Self - Level)**: +0.46 🔴 (Overconfident)
- **Delta (Self - Team)**: +0.81 🔴 (Overconfident)
- **Delta (Self - Department)**: +0.38 🔴 (Overconfident)
- **Delta (Self - Project)**: +0.36 🔴 (Overconfident)

**Performance Comparisons (Peer Avg vs Groups):**
- **vs Team Average**: +0.31 (Team avg: 4.19) - Above team
- **vs Project Average**: -0.14 (Project avg: 4.64) - Below project
- **vs Department Average**: -0.12 (Department avg: 4.62) - Below department
- **vs Company Average**: -0.17 (Company avg: 4.67) - Below company

**Statistical Analysis:**
- **Standard Deviation**: 0.50 (Moderate agreement)
- **Percentile Rank**: 21.2th percentile
- **Score Range**: 4.0 - 5.0 (spread: 1.0)

*Insufficient data for interpretation (minimum 3 responses needed)*

---

## Question 11: eNPS - Peer Comments Summary

### Synthesized Summary

*[AI synthesis needed - invoke rise8-assessment-reviewer agent with eNPS comments]*

<details>
<summary>View Raw eNPS Comments</summary>

**Kevan Mordan:**
Michael needs to step it up with communication and involvement, or more transparent with the reality of his situation. I can't provide much feedback on his core SWE fundamentals, but would have liked to see more.

**Thomas Reynolds:**
Michael does the work he is assigned regardless of complexity or difficulty. I would like to see him be more open and honest about timelines and his understanding of how to solve the problems he encounters. I would be happy to rehire him for his role with an understanding that he is still growing as an engineer.

**Alden Davidson:**
Michael takes on challenging, open-ended tasks cooly and with determination. He is honest about his skillsets and limitations, but doesn't let that hold him back from learning and growing eagerly. Michael's a fun teammate to work with in these challenging situations, and he really puts in the legwork to get the tough tasks done.


</details>

---

## Question 12: Start/Stop/Keep Recommendations

### Synthesized Summary

**START:**
*[AI synthesis needed - invoke rise8-assessment-reviewer agent with START feedback]*

**STOP:**
*[AI synthesis needed - invoke rise8-assessment-reviewer agent with STOP feedback]*

**KEEP:**
*[AI synthesis needed - invoke rise8-assessment-reviewer agent with KEEP feedback]*

<details>
<summary>View Raw Start/Stop/Keep Feedback</summary>

**Kevan Mordan:**
Start - Communicating availability and status more
Stop - Spinning your tires before asking for help or clarity, be noisier sooner
Keep - Having a positive attitude

**Thomas Reynolds:**
- Start: Being more open, communicating and sharing more. Come up with ideas for improvement or refactoring and bring them up with your teams. Even if they aren't accepted, it can generate more ideas and lead to a better product and will help you think more critically about the work you're doing.
- Stop: Not asking for help. If you get stuck on something for a long time, reach out and ask for help.
- Keep: Looking for opportunities to grow and improve your skillset. Sometimes just stepping back to look at a problem without jumping straight to the "best practice" solution can help you think critically and grow through trying new solutions.

**Alden Davidson:**
- Keep demonstrating that fearless attitude in the face of uncertainty; despite being handed a major complicated, unfamiliar migration of Rise8 infrastructure from EKS to ECS, you worked tirelessly to understand the situation and implement an effective solution


</details>

---

## Report Metadata

- **Generated**: 2025-12-04 17:48:04
- **Script Version**: 1.0.0
- **Data Sources**:
  - Assessment File: `assessments/Software/Michael_Maye.md`
  - Team Mapping: `LatticeAPI/lattice_api_client/team_map.json`
  - Comprehensive Data: `docs/analysis-results/riser_data_detailed.csv`
  - Tier Assignments: `docs/analysis-results/tier_assignments.csv`
