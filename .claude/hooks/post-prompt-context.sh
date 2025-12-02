#!/bin/bash
# Post-prompt hook to remind Claude to display context usage
# This hook runs after every user message submission

# Configuration
TOTAL_TOKENS=200000   # Total context window
AUTOCOMPACT_BUFFER=45000  # Reserved for autocompact (22.5%)
WARNING_THRESHOLD=$((TOTAL_TOKENS * 65 / 100))   # 130k
HANDOFF_THRESHOLD=$((TOTAL_TOKENS * 80 / 100))   # 160k
CRITICAL_THRESHOLD=$((TOTAL_TOKENS * 90 / 100))  # 180k

# IMPORTANT: System warnings show MESSAGE tokens only
# Actual context usage = message_tokens + base_overhead (~35-40k)
# Base overhead includes: system prompt, tools, memory files (CLAUDE.md), agents
# Use formula: actual_usage ≈ message_tokens + 35000

# Output reminder for Claude to display context
echo "📊 CONTEXT REMINDER: Display context usage visualization at end of response."
echo ""
echo "⚠️  CRITICAL: System warnings show MESSAGE tokens only."
echo "    Add ~35-40k for base overhead (system prompt + tools + memory + agents)"
echo "    Formula: actual_usage ≈ message_tokens + 35000"
echo ""
echo "Thresholds (based on ${TOTAL_TOKENS} total tokens, ${AUTOCOMPACT_BUFFER} autocompact buffer):"
echo "  • 65% (${WARNING_THRESHOLD}): Warning phase"
echo "  • 80% (${HANDOFF_THRESHOLD}): Create handoff files"
echo "  • 90% (${CRITICAL_THRESHOLD}): Critical - new session"