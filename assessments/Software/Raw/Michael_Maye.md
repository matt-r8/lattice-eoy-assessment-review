# Michael Maye - 2025 EOY Assessment

## Overall Scores

- **Peers Average**: 3.08 (based on 36 ratings)
- **Response Rate**: 36/41 peer reviewers (87%)
- **Self Average**: 4.45
- **Delta (Self - Peers)**: +1.37

---

## Michael Maye (Self)

### Question 1
**Be Bold: I have the courage to put our values in motion, even in the most intimidating and uncomfortable situations.**

**Rating**: 4 - Team Leader

### Question 2
**Do The Right Thing: I have integrity and do right by the customer, the team, and the company.**

**Rating**: 5 - Best in Class

### Question 3
**Do What Works: I work backwards from desired mission/business impact, creating alignment while rapidly testing hypotheses about outcomes and outputs.**

**Rating**: 4 - Team Leader

### Question 4
**Do What is Required: I do the hard things (activities > outputs) to create outcomes and impact.**

**Rating**: 4 - Team Leader

### Question 5
**Always Be Kind: I challenge directly and provide quality feedback without making others feel like they aren’t cared for.**

**Rating**: 5 - Best in Class

### Question 6
**Keep it Real: I keep it real with teammates and myself about not only impact and outcomes, but also the risks and opportunities along the way, leading indicators (pivots when needed), and take full ownership of the results without making excuses or shifting blame.**

**Rating**: 4 - Team Leader

### Question 7
**Outcomes in Production: I ship/support outcomes in production.**

**Rating**: 4 - Team Leader

### Question 8
**Grit: I am passionate about the mission and persevere like hell to see it through.**

**Rating**: 5 - Best in Class

### Question 9
**Growth Mindset: I am always looking to improve–when I come across a challenge I can’t solve I respond by developing my abilities and intelligence through dedication and hard work, viewing the challenges as opportunities to learn rather than to complain or give up.**

**Rating**: 5 - Best in Class

### Question 10
**No Unnecessary Rules: I am very comfortable in a high agency environment, and don’t seek or try to implement unnecessary rules.**

**Rating**: 4 - Team Leader

### Question 11
**I believe I would be enthusiastically rehired for my role on my team.**

**Rating**: 5 - Strongly Agree

**Comment**:
> My teammates can trust that when something mission-critical breaks or a delivery is at risk, I take ownership immediately and see it through to resolution. This year I stepped into unfamiliar territory—AWS, EKS, Kubernetes—and not only resurrected a down production environment, but rebuilt a more stable foundation that our teams and future applications can now build on. When stakes are high, I don’t wait for permission; I act with urgency, curiosity, and care.
I’m a teammate who creates clarity, not confusion. Whether it’s pairing with non-engineering partners to guide architectural decisions, helping peers understand new infrastructure, or communicating proactively about risks and progress, I try to make the team faster and more confident. My peers know I’m kind, honest, and deeply committed to outcomes over ego.
Ultimately, they would rehire me because I show up as someone who is reliable in the hard moments, generous with knowledge, grounded in the mission, and willing to take on difficult tasks with enthusiasm.

### Question 12
**For the next year, I plan to start/stop/keep doing the following things:**

**Rating**: None - Unknown

**Comment**:
> **Start**
- *Intentionally carving out time for architectural thinking.* Now that I’m owning significant infrastructure, I want to proactively design and document patterns that the team can follow, reducing ambiguity and onboarding friction.
- *Expanding cross-team visibility.* Sharing more interim designs, lessons learned, and “how it works” deep dives to multiply the impact of the knowledge I’ve gained.
**Stop**
- *Underestimating how much clarity I can drive.* I’ve seen how much value comes from voicing concerns early, framing trade-offs, and guiding others. I want to stop waiting for “perfect certainty” before raising ideas or feedback.
**Keep**
- *Running toward hard problems.* Troubleshooting production, decompiling undocumented systems, reverse-engineering behavior—these are strengths I want to continue leaning into.
- *Acting with high agency.* Writing my own tickets, leading investigations, removing blockers, and taking ownership before being asked.
• • *Showing kindness and partnership.* Continuing to help peers and cross-functional teammates succeed by meeting them where they are and supporting their growth.

### Question 13
**What are your top three accomplishments and their impact on Rise8’s mission that you want to highlight for the year?**

**Rating**: None - Unknown

**Comment**:
> **1. Resurrecting the EKS Production Environment & Building a New Foundation**
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

## Kevan Mordan (Peer)

### Question 1
**Be Bold: This Riser has the courage to put our values in motion, even in the most intimidating and uncomfortable situations.**

**Rating**: 2 - Developing Contributor

### Question 2
**Do The Right Thing: This Riser has integrity and does right by the customer, the team, and the company.**

**Rating**: 3 - Solid Performer

### Question 3
**Do What Works: This Riser works backwards from desired mission/business impact, creating alignment while rapidly testing hypotheses about outcomes and outputs.**

**Rating**: 3 - Solid Performer

### Question 4
**Do What is Required: This Riser does the hard things (activities > outputs) to create outcomes and impact.**

**Rating**: 2 - Developing Contributor

### Question 5
**Always Be Kind: This Riser challenges directly and provides quality feedback without making others feel like they aren’t cared for.**

**Rating**: 3 - Solid Performer

### Question 6
**Keep it Real: This Riser keeps it real with teammates and themselves about not only impact and outcomes, but also the risks and opportunities along the way, leading indicators (pivots when needed), and takes full ownership of the results without making excuses or shifting blame.**

**Rating**: 3 - Solid Performer

### Question 7
**Outcomes in Production: This Riser ships/supports outcomes in production.**

**Rating**: 2 - Developing Contributor

### Question 8
**Grit: This Riser is passionate about the mission and perseveres like hell to see it through.**

**Rating**: 2 - Developing Contributor

### Question 9
**Growth Mindset: This is always looking to improve–when they come across a challenge they can’t solve they respond by developing their abilities and intelligence through dedication and hard work, viewing the challenges as opportunities to learn rather than to complain or give up.**

**Rating**: 3 - Solid Performer

### Question 10
**No Unnecessary Rules: This Riser is very comfortable in a high agency environment, and doesn’t seek or try to implement unnecessary rules.**

**Rating**: 3 - Solid Performer

### Question 11
**I would enthusiastically rehire this Riser for their role on my team.**

**Rating**: 6 - Haven't had the opportunity to observe

**Comment**:
> Michael needs to step it up with communication and involvement, or more transparent with the reality of his situation. I can't provide much feedback on his core SWE fundamentals, but would have liked to see more.

### Question 12
**For the next year, I would recommend that you start/stop/keep doing the following things:**

**Rating**: None - Unknown

**Comment**:
> Start - Communicating availability and status more
Stop - Spinning your tires before asking for help or clarity, be noisier sooner
Keep - Having a positive attitude

## Thomas Reynolds (Peer)

### Question 1
**Be Bold: This Riser has the courage to put our values in motion, even in the most intimidating and uncomfortable situations.**

**Rating**: 3 - Solid Performer

### Question 2
**Do The Right Thing: This Riser has integrity and does right by the customer, the team, and the company.**

**Rating**: 2 - Developing Contributor

### Question 3
**Do What Works: This Riser works backwards from desired mission/business impact, creating alignment while rapidly testing hypotheses about outcomes and outputs.**

**Rating**: 3 - Solid Performer

### Question 4
**Do What is Required: This Riser does the hard things (activities > outputs) to create outcomes and impact.**

**Rating**: 3 - Solid Performer

### Question 5
**Always Be Kind: This Riser challenges directly and provides quality feedback without making others feel like they aren’t cared for.**

**Rating**: 2 - Developing Contributor

### Question 6
**Keep it Real: This Riser keeps it real with teammates and themselves about not only impact and outcomes, but also the risks and opportunities along the way, leading indicators (pivots when needed), and takes full ownership of the results without making excuses or shifting blame.**

**Rating**: 2 - Developing Contributor

### Question 7
**Outcomes in Production: This Riser ships/supports outcomes in production.**

**Rating**: 3 - Solid Performer

### Question 8
**Grit: This Riser is passionate about the mission and perseveres like hell to see it through.**

**Rating**: 2 - Developing Contributor

### Question 9
**Growth Mindset: This is always looking to improve–when they come across a challenge they can’t solve they respond by developing their abilities and intelligence through dedication and hard work, viewing the challenges as opportunities to learn rather than to complain or give up.**

**Rating**: 3 - Solid Performer

### Question 10
**No Unnecessary Rules: This Riser is very comfortable in a high agency environment, and doesn’t seek or try to implement unnecessary rules.**

**Rating**: 3 - Solid Performer

### Question 11
**I would enthusiastically rehire this Riser for their role on my team.**

**Rating**: 4 - Agree

**Comment**:
> Michael does the work he is assigned regardless of complexity or difficulty. I would like to see him be more open and honest about timelines and his understanding of how to solve the problems he encounters. I would be happy to rehire him for his role with an understanding that he is still growing as an engineer.

### Question 12
**For the next year, I would recommend that you start/stop/keep doing the following things:**

**Rating**: None - Unknown

**Comment**:
> - Start: Being more open, communicating and sharing more. Come up with ideas for improvement or refactoring and bring them up with your teams. Even if they aren't accepted, it can generate more ideas and lead to a better product and will help you think more critically about the work you're doing.
- Stop: Not asking for help. If you get stuck on something for a long time, reach out and ask for help.
- Keep: Looking for opportunities to grow and improve your skillset. Sometimes just stepping back to look at a problem without jumping straight to the "best practice" solution can help you think critically and grow through trying new solutions.

## Alexandra Brierton (Peer)

### Question 1
**Be Bold: This Riser has the courage to put our values in motion, even in the most intimidating and uncomfortable situations.**

**Rating**: 3 - Solid Performer

### Question 2
**Do The Right Thing: This Riser has integrity and does right by the customer, the team, and the company.**

**Rating**: 3 - Solid Performer

### Question 3
**Do What Works: This Riser works backwards from desired mission/business impact, creating alignment while rapidly testing hypotheses about outcomes and outputs.**

**Rating**: 3 - Solid Performer

### Question 4
**Do What is Required: This Riser does the hard things (activities > outputs) to create outcomes and impact.**

**Rating**: 3 - Solid Performer

### Question 5
**Always Be Kind: This Riser challenges directly and provides quality feedback without making others feel like they aren’t cared for.**

**Rating**: 4 - Team Leader

### Question 6
**Keep it Real: This Riser keeps it real with teammates and themselves about not only impact and outcomes, but also the risks and opportunities along the way, leading indicators (pivots when needed), and takes full ownership of the results without making excuses or shifting blame.**

**Rating**: 4 - Team Leader

### Question 7
**Outcomes in Production: This Riser ships/supports outcomes in production.**

**Rating**: 2 - Developing Contributor

### Question 8
**Grit: This Riser is passionate about the mission and perseveres like hell to see it through.**

**Rating**: 3 - Solid Performer

### Question 9
**Growth Mindset: This is always looking to improve–when they come across a challenge they can’t solve they respond by developing their abilities and intelligence through dedication and hard work, viewing the challenges as opportunities to learn rather than to complain or give up.**

**Rating**: N/A - Unknown

### Question 10
**No Unnecessary Rules: This Riser is very comfortable in a high agency environment, and doesn’t seek or try to implement unnecessary rules.**

**Rating**: N/A - Unknown

### Question 11
**I would enthusiastically rehire this Riser for their role on my team.**

**Rating**: N/A - Unknown

### Question 12
**For the next year, I would recommend that you start/stop/keep doing the following things:**

**Rating**: N/A - Unknown

## Alden Davidson (Peer)

### Question 1
**Be Bold: This Riser has the courage to put our values in motion, even in the most intimidating and uncomfortable situations.**

**Rating**: 4 - Team Leader

### Question 2
**Do The Right Thing: This Riser has integrity and does right by the customer, the team, and the company.**

**Rating**: 4 - Team Leader

### Question 3
**Do What Works: This Riser works backwards from desired mission/business impact, creating alignment while rapidly testing hypotheses about outcomes and outputs.**

**Rating**: 6 - Haven't had the opportunity to observe

### Question 4
**Do What is Required: This Riser does the hard things (activities > outputs) to create outcomes and impact.**

**Rating**: 4 - Team Leader

### Question 5
**Always Be Kind: This Riser challenges directly and provides quality feedback without making others feel like they aren’t cared for.**

**Rating**: 6 - Haven't had the opportunity to observe

### Question 6
**Keep it Real: This Riser keeps it real with teammates and themselves about not only impact and outcomes, but also the risks and opportunities along the way, leading indicators (pivots when needed), and takes full ownership of the results without making excuses or shifting blame.**

**Rating**: 6 - Haven't had the opportunity to observe

### Question 7
**Outcomes in Production: This Riser ships/supports outcomes in production.**

**Rating**: 6 - Haven't had the opportunity to observe

### Question 8
**Grit: This Riser is passionate about the mission and perseveres like hell to see it through.**

**Rating**: 5 - Best in Grade

### Question 9
**Growth Mindset: This is always looking to improve–when they come across a challenge they can’t solve they respond by developing their abilities and intelligence through dedication and hard work, viewing the challenges as opportunities to learn rather than to complain or give up.**

**Rating**: 4 - Team Leader

### Question 10
**No Unnecessary Rules: This Riser is very comfortable in a high agency environment, and doesn’t seek or try to implement unnecessary rules.**

**Rating**: 4 - Team Leader

### Question 11
**I would enthusiastically rehire this Riser for their role on my team.**

**Rating**: 5 - Strongly Agree

**Comment**:
> Michael takes on challenging, open-ended tasks cooly and with determination. He is honest about his skillsets and limitations, but doesn't let that hold him back from learning and growing eagerly. Michael's a fun teammate to work with in these challenging situations, and he really puts in the legwork to get the tough tasks done.

### Question 12
**For the next year, I would recommend that you start/stop/keep doing the following things:**

**Rating**: None - Unknown

**Comment**:
> - Keep demonstrating that fearless attitude in the face of uncertainty; despite being handed a major complicated, unfamiliar migration of Rise8 infrastructure from EKS to ECS, you worked tirelessly to understand the situation and implement an effective solution
