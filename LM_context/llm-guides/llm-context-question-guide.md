# LLM Context-Driven Question Generation Guide

## 🎯 Purpose
This guide helps LLMs generate appropriate clarifying questions based on the specific context they discover when reading the session files.

---

## 📋 Question Generation Framework

### Step 1: Analyze Context Files
After reading the essential context files, identify:

1. **Current Status Indicators**
   - Iteration progress percentage
   - Hypothesis validation status
   - Blockers or risks mentioned
   - Time since last session

2. **Environmental Context**
   - Hardware setup status
   - Network configuration
   - Any constraint changes
   - Resource availability

3. **Priority Signals**
   - Immediate next actions listed
   - Urgency indicators
   - Completion criteria status
   - Validation requirements

4. **Knowledge Base Context**
   - Are there any new or relevant guides in the `knowledge/` directory?
   - Do any existing knowledge articles apply to the current task?
   - Is there an opportunity to create a new knowledge article from the current work?

### Step 2: Generate Context-Specific Questions

#### Based on Session Handoff Status

**If Progress is Blocked:**
- "I see there's a blocker with [specific issue from handoff]. Has this been resolved or should we focus on unblocking it?"
- "The session handoff mentions [specific risk]. What's the current status of this issue?"

**If Iteration is Near Completion:**
- "The current iteration shows [X%] completion. Should we focus on finishing it or start planning the next iteration?"
- "I notice [specific completion criteria] are still pending. Are these still relevant priorities?"

**If Validation is Overdue:**
- "The assumptions log shows H[X] hasn't been validated recently. Should we prioritize running validation tests?"
- "I see the stability testing for H7 is pending. Do you want to start the 24-hour validation now?"

#### Based on Environment Context

**If Hardware Setup Questions:**
- "The environment shows target device at [TARGET_IP]. Is this still the correct IP for this session?"
- "Are there any changes to the hardware setup or network configuration I should know about?"

**If Resource Constraints:**
- "I notice the system targets <40% CPU usage. Are there any new performance requirements?"
- "The environment mentions specific Yocto layers. Have there been any build system changes?"

#### Based on Current Iteration Context

**If Hypothesis Testing in Progress:**
- "The current iteration is testing [specific hypothesis]. Should we continue with this or pivot to something else?"
- "I see [specific experiment] is active. What's the current status of this test?"

#### Based on Knowledge Base Context

**If a Relevant Guide Exists:**
- "I found a `plugin-development-guide.md` in the knowledge base. Should we follow this guide for the task of creating the new GStreamer plugin?"
- "The `performance-tuning-guide.md` seems relevant to our goal of reducing latency. Shall I apply the principles from that guide?"

**If Multiple Priorities Listed:**
- "The session handoff lists several next actions. Which should be the top priority for this session?"
- "There are both development and validation tasks pending. What should we focus on given the time available?"

### Step 3: Include Session Scope Questions

**Always Ask About:**
- **Time Available:** "How much time do you have for this session? This will help me prioritize the work appropriately."
- **Scope Preference:** "Should we focus on [specific area based on context] or is there something else more urgent?"
- **Validation Needs:** "Do you want me to run validation tests first, or should we proceed with development work?"

---

## 🔍 Context Analysis Patterns

### High-Priority Signals
- **"BLOCKED"** status in session handoff → Focus on unblocking
- **Validation overdue** (>48 hours) → Prioritize validation
- **Iteration >90% complete** → Focus on completion
- **New hypothesis added** → Understand validation requirements

### Medium-Priority Signals
- **Multiple next actions** → Clarify priorities
- **Environment changes mentioned** → Verify current setup
- **Performance issues noted** → Understand constraints
- **Resource updates needed** → Clarify scope

### Low-Priority Signals
- **Documentation updates** → Can be deferred
- **Archive maintenance** → Not session-critical
- **Future planning** → Only if current work is complete

---

## 📝 Question Templates

### Environment Verification
```
"I see the environment configuration shows [specific detail]. Is this still current for today's session?"
```

### Priority Clarification
```
"Based on the session handoff, I see [X] and [Y] are both listed as priorities. Which should we tackle first given the time available?"
```

### Blocker Resolution
```
"The context shows [specific blocker]. Has this been resolved, or should we focus on addressing it in this session?"
```

### Validation Status
```
"I notice [specific hypothesis] validation is [status]. Should we run the validation tests or continue with development?"
```

### Scope Definition
```
"Given that [context observation], should we focus on [option A] or [option B] for this session?"
```

---

## ⚠️ Question Generation Rules

### DO Generate Questions About:
- **Specific blockers or risks** mentioned in session handoff
- **Validation status** when tests are overdue
- **Priority conflicts** when multiple urgent items exist
- **Environment changes** that might affect the session
- **Time/scope constraints** for the current session

### DON'T Generate Questions About:
- **Generic preferences** not related to current context
- **Obvious information** clearly stated in context files
- **Historical details** that don't affect current work
- **Theoretical scenarios** not relevant to immediate tasks

### Question Quality Guidelines:
- **Be Specific:** Reference exact details from context files
- **Be Actionable:** Focus on decisions that affect the session
- **Be Contextual:** Base questions on what you actually read
- **Be Concise:** Ask 3-5 focused questions, not a long list
- **Be Relevant:** Only ask what's needed to proceed effectively

---

## 🎯 Example Question Sets

### Scenario 1: Blocked Iteration
*Context: Session handoff shows "BLOCKED - H7 validation failing"*

**Generated Questions:**
1. "I see H7 validation is failing and blocking progress. Have you identified the root cause, or should we focus on debugging this issue?"
2. "Should we try to fix the H7 validation problem, or would you prefer to work on other hypotheses while this is being resolved?"
3. "How much time do you have for this session? Debugging validation issues can be time-consuming."

### Scenario 2: Near Iteration Completion
*Context: Current iteration shows 85% complete, only documentation tasks remaining*

**Generated Questions:**
1. "The current iteration is 85% complete with mainly documentation tasks left. Should we finish this iteration or start the next one?"
2. "Are the remaining documentation tasks critical, or can we move forward with the next hypothesis?"
3. "Do you want to run a final validation before marking this iteration complete?"

### Scenario 3: Multiple Priorities
*Context: Session handoff lists both H8 development and H7 stability testing as priorities*

**Generated Questions:**
1. "I see both H8 development and H7 stability testing are listed as priorities. Which should we tackle first?"
2. "The H7 stability test takes 24 hours to complete. Should we start that running in the background while working on H8?"
3. "Given the time available, should we focus on one priority or try to advance both?"

### Scenario 4: Environment Changes
*Context: Environment file shows recent updates, session handoff mentions network issues*

**Generated Questions:**
1. "I notice the environment file was recently updated and there were network issues mentioned. Are the current IP addresses ([TARGET_IP]/[DEV_IP]) still correct?"
2. "Have the network issues been resolved, or do we need to work around them in this session?"
3. "Are there any other environment changes I should be aware of before we start?"

---

## 🚀 Implementation Checklist

### For LLMs Using This Guide:
- [ ] Read all essential context files first
- [ ] Identify specific status indicators and signals
- [ ] Generate 3-5 context-specific questions
- [ ] Reference exact details from the context files
- [ ] Focus on actionable decisions for the current session
- [ ] Wait for human responses before proceeding with work

### For Humans Receiving Questions:
- [ ] Answer questions briefly and specifically
- [ ] Provide any additional context not captured in files
- [ ] Clarify priorities and time constraints
- [ ] Mention any urgent issues not reflected in context
- [ ] Give the LLM clear direction to proceed

---

**Last Updated:** July 23, 2025  
**Purpose:** Enable LLMs to generate intelligent, context-driven questions for optimal session initialization
