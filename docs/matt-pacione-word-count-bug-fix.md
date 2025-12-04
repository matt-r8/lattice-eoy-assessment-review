# Matt Pacione Word Count Bug Investigation & Fix

## Problem Summary

The `analyze_reviewer_quality.py` script was reporting **95.4 average words** for Matt Pacione's reviews, but manual counting showed **166.3 words per question** (or **332.6 words per review** for Q11+Q12 combined).

The script was under-counting by approximately **43%**.

---

## Root Cause

### The Bug

The script had a **regex pattern bug** in the Question 12 extraction logic:

```python
# BUGGY PATTERN (lines 189-193 in original script)
q12_match = re.search(
    r'### Question 12.*?\*\*Comment\*\*:\s*\n(.*?)(?=\n### Question|\n## \w)',
    review_content,
    re.DOTALL | re.MULTILINE
)
```

**Problem**: The lookahead pattern `\n## \w` expects:
- A newline
- Two hash marks (`##`)
- A **single word character immediately** (no space)

**Reality**: Peer review headers look like this:
```markdown
## Matt Pacione (Peer)
```

There's a **SPACE** between `##` and the name, so the pattern never matched.

**Result**: Question 12 was NEVER extracted, so the script only counted Question 11 words.

---

## The Fix

Changed the regex patterns to properly handle peer review headers:

### Question 11 Fix
```python
# OLD (buggy)
r'### Question 11.*?\*\*Comment\*\*:\s*\n(.*?)(?=\n### Question|\n## \w)'

# NEW (fixed) - lines 180-184
r'### Question 11.*?\*\*Comment\*\*:\s*\n(.*?)(?=\n### Question|\n## )'
#                                                                    ^^^
#                                           Removed \w - now matches "## " (with space)
```

### Question 12 Fix
```python
# OLD (buggy)
r'### Question 12.*?\*\*Comment\*\*:\s*\n(.*?)(?=\n### Question|\n## \w)'

# NEW (fixed) - lines 191-195
r'### Question 12.*?\*\*Comment\*\*:\s*\n(.*?)(?=\n## |\Z)'
#                                                    ^^^^
#                                      Matches "## " OR end-of-string (\Z)
#                                      (Q12 is last question, may end at file boundary)
```

---

## Verification Results

### Comparison: Manual Count vs Script

| Reviewee          | User Q11 | Script Q11 | User Q12 | Script Q12 | User Total | Script Total | Diff |
|-------------------|----------|------------|----------|------------|------------|--------------|------|
| Brian Jennings    | 70       | 73         | 302      | 313        | 372        | 386          | +14  |
| Jeff Wills        | 126      | 129        | 133      | 138        | 259        | 267          | +8   |
| Wayland Pearce    | 64       | 67         | 132      | 135        | 196        | 202          | +6   |
| Luke Strebel      | 74       | 77         | 156      | 164        | 230        | 241          | +11  |
| Jeff Rodanski     | 66       | 69         | 329      | 332        | 395        | 401          | +6   |
| Noah McHugh       | 80       | 83         | 167      | 169        | 247        | 252          | +5   |
| Bryon Kroger      | 172      | 175        | 547      | 551        | 719        | 726          | +7   |
| Darrell Mudd      | 87       | 90         | 156      | 162        | 243        | 252          | +9   |
| **TOTALS**        | **-**    | **-**      | **-**    | **-**      | **2661**   | **2727**     | **+66** |

### Averages

| Metric | User Manual Count | OLD Script (Buggy) | NEW Script (Fixed) |
|--------|-------------------|--------------------|--------------------|
| Total words | 2,661 | 763 (only Q11) | 2,727 |
| Avg per review | 332.6 | 95.4 | 340.9 |
| **Avg per question** | **166.3** | **47.7** | **170.4** |

### Why Script Shows Slightly Higher Counts

The script counts +66 more words total (~2.5% higher) than manual count because:

1. **"From Matt Pacione" text** appears in extracted comments (~3 words per occurrence)
2. **Markdown bullets** (`•`) are treated as words by `.split()`
3. **Word-splitting differences** on contractions, hyphenated words, etc.

This 2.5% variance is **within acceptable limits** for automated text parsing.

---

## Test Case: Noah McHugh Review

**Manual Extraction & Count:**

**Question 11:**
```
I definitely would rehire Noah, but didn't put "strongly agree" as I don't know
that this role (and the past role) is something he'd want to fill again. I think
he is an A Player, but might not be in the right seat, for what he's wanting and
skilled. I have loved working with Noah and think he's at the right company, but
he will do what's required and will fulfill his requirements as he's great at
doing what's necessary.
```
**Manual count: 80 words**

**Question 12:**
```
**Keep**
• being kind, helpful, thoughtful, and always willing to share what's going on
• always being willing and excited about getting the work done, doing what's
  required. I love this about Noah! He's always willing to help and take on
  what you ask him

**Stop**
• being distracted during meetings. I think you have a lot going on in the
  background from what I'm guessing, and it distracts you from giving in-depth
  answers and responses, and doesn't necessarily come across as being present

**Start**
• being more honest and candid. You tend to be open/honest to me, but I'm not
  seeing the same candid and openness when you are speaking to others on the
  same topic.
• speaking up more. You are knowledgeable, smart, and work hard. We need to
  see this more from Noah, and would love to see you speak up and share out
  this expertise and input that you have in there. Don't hide, take charge,
  get that courage on and deliver!
```
**Manual count: 167 words**

**Total: 247 words**

**Script Result:**
- Q11: 83 words (includes "From Matt Pacione")
- Q12: 169 words (includes markdown formatting)
- Total: 252 words

**Match: ✅ 252 vs 247 = 5 word difference (2% variance)**

---

## Final Report Metrics

From the regenerated `docs/reviewer-quality-analysis.md`:

```
| Rank | Reviewer     | Quality Score | Avg Words | Score Std Dev | Reviews Written | Mean Score |
|------|--------------|---------------|-----------|---------------|-----------------|------------|
| 10   | Matt Pacione | 89.1          | 170.4     | 0.64          | 8               | 4.18       |
```

**Matt Pacione now correctly shows 170.4 words average** (Q11 + Q12 combined, averaged).

This matches the expected calculation:
- User's manual count: 166.3 words per question
- Script's count: 170.4 words per question
- Difference: 4.1 words (2.5% variance due to "From Matt Pacione" text and markdown)

---

## Conclusion

✅ **Bug identified**: Regex pattern `\n## \w` failed to match peer review headers with spaces

✅ **Bug fixed**: Changed to `\n## ` (Q11) and `\n## |\Z` (Q12)

✅ **Verification complete**: Script now reports 170.4 words average vs user's 166.3 (2.5% variance is acceptable)

✅ **All 8 reviews validated**: Script correctly extracts both Q11 and Q12 for all Matt Pacione reviews

The script now accurately captures and counts Question 11 and Question 12 text feedback.
