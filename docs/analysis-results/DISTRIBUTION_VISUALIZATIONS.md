# Rise8 EOY Assessment - Distribution Visualizations
## Visual Representations of Statistical Data

**Dataset:** 143 Risers across 13 departments
**Analysis Date:** 2025-12-03

---

## 1. Peer Score Distribution Histogram

```
Score Range | Count | Percentage | Distribution
------------|-------|------------|----------------------------------------------------
4.70-4.91   |   3   |   2.1%     | ███ [S-Tier]
4.60-4.69   |   7   |   4.9%     | ███████ [A+ Tier]
4.50-4.59   |  12   |   8.4%     | ████████████ [A+ Tier]
4.40-4.49   |  13   |   9.1%     | █████████████ [A Tier]
4.30-4.39   |  15   |  10.5%     | ███████████████ [A Tier]
4.20-4.29   |  17   |  11.9%     | █████████████████ [A Tier]
4.10-4.19   |  16   |  11.2%     | ████████████████ [A- Tier]
4.00-4.09   |  17   |  11.9%     | █████████████████ [A- Tier]
3.90-3.99   |  11   |   7.7%     | ███████████ [A- Tier]
3.80-3.89   |  10   |   7.0%     | ██████████ [A- Tier]
3.70-3.79   |   6   |   4.2%     | ██████ [A- Tier]
3.60-3.69   |   5   |   3.5%     | █████ [A- Tier]
3.50-3.59   |   3   |   2.1%     | ███ [A- Tier]
3.40-3.49   |   2   |   1.4%     | ██ [A- Tier]
3.30-3.39   |   1   |   0.7%     | █ [A- Tier]
3.20-3.29   |   2   |   1.4%     | ██ [A- Tier]
3.10-3.19   |   1   |   0.7%     | █ [A- Tier]
3.00-3.09   |   1   |   0.7%     | █ [A- Tier]
2.90-2.99   |   0   |   0.0%     | [None]
2.80-2.89   |   1   |   0.7%     | █ [B Tier]
2.70-2.79   |   0   |   0.0%     | [None]
2.60-2.69   |   0   |   0.0%     | [None]
2.50-2.59   |   0   |   0.0%     | [None]
2.40-2.49   |   1   |   0.7%     | █ [B Tier]

Total:      | 143   | 100.0%

Mean:        4.100
Median:      4.170
Std Dev:     0.425
```

**Key Observations:**
- **Normal-ish distribution** with slight positive skew (median > mean)
- **Peak at 4.00-4.29 range** (40.6% of Risers)
- **Long left tail** down to 2.44 (minimal but present)
- **No ceiling effect** - top performer at 4.91 shows room for excellence recognition

---

## 2. Tier Distribution (Pie Chart Representation)

```
         S-Tier (2.1%)
              ╭─╮
         A+ (8.4%)
        ╭─────────╮
    A (31.5%)     │
  ╭──────────────╮│
  │              ││
  │   A- Tier    ││
  │   (56.6%)    ││
  │              ││
  ╰──────────────╯│
   B (1.4%)       │
   ╰───────────────╯

Tier Breakdown:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
S  (4.75+):   3 Risers   █  2.1%  [Supreme]
A+ (4.58+):  12 Risers   ████  8.4%  [Exceptional]
A  (4.25+):  45 Risers   ████████████████  31.5%  [Solid]
A- (3.00+):  81 Risers   ████████████████████████████  56.6%  [Baseline]
B  (2.00+):   2 Risers   █  1.4%  [Developing]
C  (<2.00):   0 Risers     0.0%  [Critical]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Interpretation:**
- **98.6% of Risers** meet A Player baseline (3.0+)
- **42.0% of Risers** exceed solid performer threshold (4.25+)
- **10.5% of Risers** in top tier (S + A+) drive exceptional impact
- **1.4% of Risers** require development focus (B tier)

---

## 3. Department Comparison Box Plot

```
Department Performance Distribution (Mean ± 1 StdDev)

Operations      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━●━━━━━━━ [4.56]
Enablement      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━●━━━━━━━━━━━━ [4.47 ± 0.17]
Delivery        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━●━━━━━━━━━━━━ [4.37 ± 0.13]
Executive       ━━━━━━━━━━━━━━━━━━━━━━━━━━━●━━━━━━━━━━━━━ [4.34 ± 0.25]
Platform-Cyber  ━━━━━━━━━━━━━━━━━━━━━━━━━●━━━━━━━━━━━━━━━ [4.16 ± 0.42]
Growth          ━━━━━━━━━━━━━━━━━━━━━━━━━●━━━━━━━━━━━━━━━ [4.16 ± 0.12]
Product-Mgmt    ━━━━━━━━━━━━━━━━━━━━━━━━━●━━━━━━━━━━━━━━━ [4.13 ± 0.41]
Design          ━━━━━━━━━━━━━━━━━━━━━━━━━●━━━━━━━━━━━━━━━ [4.07 ± 0.30]
Marketing       ━━━━━━━━━━━━━━━━━━━━━━━━●━━━━━━━━━━━━━━━━ [3.98 ± 0.28]
Software        ━━━━━━━━━━━━━━━━━━━━━━━●━━━━━━━━━━━━━━━━━ [3.96 ± 0.45]
IT              ━━━━━━━━━━━━━━━━━━━━━━━●━━━━━━━━━━━━━━━━━ [3.80 ± 0.76]
Customer-Success━━━━━━━━━━━━━━━━━━━━━━●━━━━━━━━━━━━━━━━━━ [3.74 ± 1.14]
PeopleOps       ━━━━━━━━━━━━━━━━━━━━━●━━━━━━━━━━━━━━━━━━━ [3.66]

            2.5  3.0  3.5  4.0  4.5  5.0
                 ↑
            A Player Baseline (3.0)
```

**Department Size Context:**
- Large (30+): Platform-Cyber (38), Software (36)
- Medium (15-30): Product-Management (21), Design (16)
- Small (5-15): Executive (9), Enablement (6), Marketing (6)
- Tiny (1-4): Customer-Success (3), Growth (2), Delivery (2), IT (2), Operations (1), PeopleOps (1)

**Key Findings:**
- **Most consistent:** Enablement (σ=0.166), Growth (σ=0.120), Delivery (σ=0.127)
- **Most variable:** Customer-Success (σ=1.141), IT (σ=0.764), Software (σ=0.447)
- **All departments above 3.0 mean** - Strong company-wide performance

---

## 4. Self vs Peer Delta Scatter Plot

```
Self-Assessment vs Peer Average (with Delta indication)

5.0 │
    │                                      ●  Ryan Tuck (Δ=+1.64)
4.8 │                               ●  Michael Maye (Δ=+1.37)
    │
4.6 │                        ╱
    │                    ╱  ●
4.4 │                ╱     ●●●
    │            ╱      ●●●●●
4.2 │        ╱       ●●●●●●●
    │    ╱        ●●●●●●●●●●
4.0 │ ╱         ●●●●●●●●●●●●●
    │╱        ●●●●●●●●●●●●●●●
3.8 │       ●●●●●●●●●●●●●●●●
    │     ●●●●●●●●●●●●●●●
3.6 │   ●●●●●●●●●●●●●●
    │  ●●●●●●●●●●●●●
3.4 │ ●●●●●●●●●●●●
    │●●●●●●●●●
3.2 │●●●●●
    │●●  Ainsilie Hibbard (Δ=-1.92)
3.0 │●
    │● Jordan Dilworth (Δ=-1.42)
2.8 │● Vanessa Ten-Kate (Δ=-1.42)
    │
2.6 │
    │
2.4 └──────────────────────────────────────────────────
    2.4 2.8 3.2 3.6 4.0 4.4 4.8 5.0
                 Peer Average Score

    ╱ = Perfect self-awareness line (Self = Peer)
    Above line = Overconfident (Self > Peer)
    Below line = Humble/Growth Mindset (Self < Peer)
```

**Delta Distribution:**
```
Overconfident      Accurate       Humble/Growth
  (Δ > 0.3)      (-0.3 ≤ Δ ≤ 0.3)   (Δ < -0.3)
    19.6%           41.3%            39.2%
  28 Risers       59 Risers        56 Risers
     ▲               ▲                ▲
     └───────────────┴────────────────┘
              Mean Δ = -0.170
          (Company leans humble)
```

**Correlation Pattern:**
- **High Performers (≥4.0):** Tend to be humble (avg Δ = -0.334)
- **Lower Performers (<3.5):** Tend to be overconfident (avg Δ = +0.547)
- **Inverse correlation:** Better performers underestimate themselves more

---

## 5. Response Rate Impact Analysis

```
Response Rate Distribution (111 Risers with data)

100% │ ████████████████████████████████ (51 Risers, 45.9%)
 95% │ ███████████████ (23 Risers, 20.7%)
 90% │ ████████ (15 Risers, 13.5%)
 85% │ ████ (8 Risers, 7.2%)
 80% │ ██ (3 Risers, 2.7%)
 75% │ █ (2 Risers, 1.8%)
 70% │ █ (2 Risers, 1.8%)
 65% │ █ (2 Risers, 1.8%)
 60% │ █ (1 Riser, 0.9%)
 55% │ █ (1 Riser, 0.9%)
 50% │ █ (2 Risers, 1.8%)
 45% │ █ (1 Riser, 0.9%)

Mean: 92.5% | Median: 96.0%
```

**Response Count Distribution:**
```
Responses | Confidence | Count | Percentage
----------|------------|-------|------------
100+      | VERY HIGH  |   9   |   8.1%
80-99     | HIGH       |  20   |  18.0%
60-79     | HIGH       |  24   |  21.6%
40-59     | HIGH       |  36   |  32.4%
20-39     | MEDIUM     |  20   |  18.0%
10-19     | MEDIUM     |   2   |   1.8%
5-9       | LOW        |   0   |   0.0%
<5        | VERY LOW   |   0   |   0.0%

Mean: 60.9 responses | Median: 55.0 responses
```

**Key Finding:**
- 97.3% of Risers (with data) received ≥20 responses
- High statistical confidence in peer averages
- Minimal correlation between response rate and performance

---

## 6. Percentile Reference Chart

```
Percentile Mapping (What score represents what percentile?)

Percentile | Score  | Interpretation
-----------|--------|--------------------------------------------------
99th       | 4.760  | Top 1% - S-Tier boundary
98th       | 4.750  | Top 2%
95th       | 4.640  | Top 5%
90th       | 4.580  | Top 10% - A+ Tier boundary
75th (Q3)  | 4.410  | Top 25%
60th       | 4.250  | Top 40% - A Tier boundary
50th (Med) | 4.170  | Median performer
40th       | 4.050  | Above average
25th (Q1)  | 3.850  | First quartile
10th       | 3.450  | Bottom 10% (but still A- tier)
5th        | 3.220  | Bottom 5%
1st        | 2.440  | Bottom 1% - B Tier

3.00 = A Player Baseline (98.6% of company above this)
```

---

## 7. Score Distribution by Tier (Violin Plot)

```
           S-Tier          A+ Tier         A Tier       A- Tier     B Tier
          (4.75+)        (4.58-4.75)    (4.25-4.58)   (3.00-4.25)  (2.00-3.00)

5.0 ─      ●─4.91
          ┌─┐
4.8 ─      │ │
          │ │
4.6 ─      └─┘─4.76          ●─4.72
                           ┌───┐
4.4 ─                      │   │          ●─4.56
                          │   │        ┌─────┐
4.2 ─      (3)            └───┘       │     │         ●─4.23
                                      │     │       ┌───────┐
4.0 ─                       (12)      └─────┘      │       │
                                                   │       │
3.8 ─                                  (45)       │       │
                                                  │       │
3.6 ─                                             │       │
                                                 │       │
3.4 ─                                            │       │
                                                │       │
3.2 ─                                           └───────┘
                                                          ●─2.83
3.0 ─                                            (81)     ┌─┐
                                                         │ │
2.8 ─                                                    │ │
                                                        └─┘─2.44
2.6 ─                                                    (2)

     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
     2.1%            8.4%           31.5%         56.6%        1.4%
```

**Interpretation:**
- **S-Tier:** Tightly clustered at top (4.75-4.91)
- **A+ Tier:** Narrow band (4.58-4.72)
- **A Tier:** Widest distribution, largest absolute group
- **A- Tier:** Largest group by percentage, spans widest range (3.00-4.23)
- **B Tier:** Only 2 outliers, very small group

---

## 8. Department-Level Tier Distribution

```
Department         | S | A+ | A | A- | B | Total | Top 10% (S+A+)
-------------------|---|----|----|-------|---|-------|---------------
Platform-Cyber     | 2 |  6 | 11 |  19   | 0 |  38   | 21.1%
Software           | 1 |  1 | 11 |  21   | 2 |  36   |  5.6%
Product-Management | 1 |  2 |  9 |   9   | 0 |  21   | 14.3%
Design             | 0 |  1 |  4 |  11   | 0 |  16   |  6.3%
Executive          | 0 |  1 |  5 |   3   | 0 |   9   | 11.1%
Enablement         | 0 |  3 |  2 |   1   | 0 |   6   | 50.0%
Marketing          | 0 |  0 |  1 |   5   | 0 |   6   |  0.0%
Customer-Success   | 0 |  0 |  1 |   1   | 1 |   3   |  0.0%
Growth             | 0 |  0 |  1 |   1   | 0 |   2   |  0.0%
Delivery           | 0 |  0 |  1 |   1   | 0 |   2   |  0.0%
IT                 | 0 |  0 |  0 |   2   | 0 |   2   |  0.0%
Operations         | 0 |  0 |  1 |   0   | 0 |   1   |  0.0%
PeopleOps          | 0 |  0 |  0 |   1   | 0 |   1   |  0.0%
-------------------|---|----|----|-------|---|-------|---------------
TOTAL              | 3 | 12 | 45 |  81   | 2 | 143   | 10.5%
```

**Key Insights:**
- **Enablement dominates top performers** (50% in S+A+ tier)
- **Platform-Cyber has most S-tier** (2 of 3 total)
- **Software has widest distribution** (includes both S-tier and B-tier)
- **Marketing/Customer-Success/Growth** have no top 10% performers

---

## 9. Self-Peer Delta by Performance Level

```
Performance Band | Mean Delta | Interpretation
-----------------|------------|------------------------------------------
Top 10% (≥4.58)  |   -0.485   | Very humble - underestimate significantly
High (4.00-4.58) |   -0.334   | Humble - growth mindset culture
Mid (3.50-3.99)  |   -0.106   | Slightly humble - realistic self-view
Low (3.00-3.49)  |   +0.253   | Slightly overconfident
Bottom (<3.00)   |   +0.785   | Very overconfident - needs calibration

                 Humble ←─────────────────→ Overconfident
                      -1.0      0.0      +1.0
Top Performers:   ─────●────────|──────────────────
High Performers:  ──────────●───|──────────────────
Mid Performers:   ─────────────●|──────────────────
Low Performers:   ──────────────|──●───────────────
Bottom 2%:        ──────────────|──────────●───────

```

**Critical Pattern:**
- **Inverse correlation** between performance and self-rating
- **High performers undervalue** themselves (growth mindset)
- **Low performers overvalue** themselves (Dunning-Kruger effect)
- **Coaching opportunity:** Help low performers develop accurate self-assessment

---

## 10. Tier Transition Boundaries (Score Bands)

```
Visual representation of where Risers fall relative to tier boundaries

5.0 ┤
    │  S-TIER BEGINS (4.75) ─────────────────────────────────
4.9 │  ● Andrew Knife (4.91)
    │
4.8 │
    │  ● Peter Duong (4.76) ● Luke Strebel (4.75)
4.7 │
    │  A+ TIER BEGINS (4.58) ────────────────────────────────
4.6 │  ●●● (9 Risers in 4.60-4.69)
    │
4.5 │  ●●●●●●●●●●●● (12 Risers in 4.50-4.59)
    │
4.4 │  A TIER BEGINS (4.25) ──────────────────────────────────
    │  ●●●●●●●●●●●●●●●●●●●●●●●●●●●●● (45 Risers in 4.25-4.49)
4.3 │
    │
4.2 │  A- TIER BEGINS (3.00) ─────────────────────────────────
    │  ●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●
4.1 │  ●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●
    │  ●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●
4.0 │  ●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●
    │  ●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●
3.9 │  ●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●
    │  ●●●●●●●●●●●●●●●●●●●●●●●●●●●
3.8 │  ●●●●●●●●●●●●●●●●●●●●●●●
    │  ●●●●●●●●●●●●●●●●●●
3.7 │  ●●●●●●●●●●●●
    │  ●●●●●●●●
3.6 │  ●●●●●●
    │  ●●●●
3.5 │  ●●●
    │  ●●
3.4 │  ●●
    │  ●
3.3 │  ●
    │  ●●
3.2 │  ●
    │  ●
3.1 │  ●
    │
3.0 │  B TIER BEGINS (2.00) ──────────────────────────────────
    │
2.9 │  ● Kyle Smart (2.83)
    │
2.8 │
    │
2.7 │
    │
2.6 │
    │
2.5 │  ● Shawn Kilroy (2.44)
    │
2.4 │  C TIER BEGINS (<2.00) ─────────────────────────────────
    │  [No Risers in C-Tier]
    └──────────────────────────────────────────────────────────

    │◄──────── 81 Risers (56.6%) ────────►│
                  A- Tier Range
```

---

## Summary Statistics Reference

### Central Tendency
- **Mean:** 4.100
- **Median:** 4.170
- **Mode:** 4.20-4.29 (most common range)

### Dispersion
- **Range:** 2.470 (2.44 to 4.91)
- **Variance:** 0.181
- **Standard Deviation:** 0.425
- **Coefficient of Variation:** 10.4% (moderate variability)

### Shape
- **Skewness:** Slightly positive (median > mean indicates left-skewed)
- **Kurtosis:** Platykurtic (flatter than normal distribution)

### Quartiles
- **Q1 (25th):** 3.850
- **Q2 (50th):** 4.170
- **Q3 (75th):** 4.410
- **IQR:** 0.560

### Percentiles
- **P10:** 3.450
- **P25:** 3.850
- **P50:** 4.170
- **P75:** 4.410
- **P90:** 4.580
- **P95:** 4.640
- **P99:** 4.760

---

**For detailed data:**
- Full dataset: `/workspaces/lattice-eoy-assessment-review/docs/analysis-results/riser_data_detailed.csv`
- Tier assignments: `/workspaces/lattice-eoy-assessment-review/docs/analysis-results/tier_assignments.csv`
- Executive summary: `/workspaces/lattice-eoy-assessment-review/docs/analysis-results/EXECUTIVE_SUMMARY.md`
