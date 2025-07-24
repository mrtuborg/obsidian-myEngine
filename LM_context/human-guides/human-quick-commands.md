# Human Quick Commands & Shortcuts

## 🚀 One-Line Session Commands

### Enhanced Session Start with Validation (Copy-Paste)
```
Start session with validation: Check context health, validate files exist, read context with freshness check (session-handoff, current-iteration, environment, failed-solutions), ask 3-5 specific questions with understanding validation, confirm readiness before proceeding.
```

### Project Type-Specific Session Start (Copy-Paste)

#### Technical Projects
```
Start technical session: Read context (session-handoff, current-iteration, environment, working-solutions), ask about programming language/platform/frameworks, focus on implementation and integration, summarize technical status and next development actions.
```

#### Research Projects  
```
Start research session: Read context (session-handoff, current-iteration, assumptions-log, validation), ask about research question/methodology/hypothesis, focus on evidence collection and validation, summarize research status and next investigation actions.
```

#### Documentation Projects
```
Start documentation session: Read context (session-handoff, current-iteration, project-plan, external-resources), ask about audience/scope/format requirements, focus on content creation and organization, summarize documentation status and next writing actions.
```

#### Collaborative Projects
```
Start collaborative session: Read context (session-handoff, current-iteration, assumptions-log, working-solutions), ask about team members/decision process/communication channels, focus on coordination and knowledge sharing, summarize team status and next collaboration actions.
```

### Enhanced Session End with Verification (Copy-Paste)  
```
End session with verification: Create backup, compile knowledge with quality checks (update working-solutions.md, failed-solutions/, create daily log in archive/daily-logs/), update files with verification (session-handoff.md, current-iteration.md, knowledge-base/), ask closure questions with completeness check, confirm proper closure.
```

### Emergency Reset (Copy-Paste)
```
System reset: Run assumption-validator.py, read working-solutions.md, update session-handoff.md with current technical state.
```

### Agile Schedule Adaptation (Copy-Paste)

#### Schedule Pressure (Deadline Moved Up)
```
Schedule update: Deadline moved to [new date]. Analyze current iteration, identify minimum viable deliverables, rebalance priorities to fit timeline, update current-iteration.md with revised plan.
```

#### Extended Timeline (More Time Available)
```
Schedule update: Timeline extended to [new date]. Analyze current iteration, identify enhancement opportunities, add valuable features to scope, update current-iteration.md with expanded plan.
```

#### Scope Change (Requirements Updated)
```
Scope update: Requirements changed - [describe changes]. Analyze impact on current iteration, adjust priorities and timeline, update current-iteration.md with revised scope and schedule.
```

#### Agile Plan Adaptation (General Changes)
```
Agile adaptation: Analyze current iteration progress, assess schedule constraints, rebalance priorities for maximum value delivery, update current-iteration.md with optimized plan that fits available time and resources.
```

## ⚡ Quick Status Checks

### Before Starting Session
```bash
# Quick system health check (30 seconds)
cd /path/to/your/project/LM_context
python3 dynamic/assumption-validator.py --stability-hours 0.1 && echo "✅ System Ready"
```

### After Session (Verify LLM Updates)
```bash
# Check if files were actually updated (10 seconds)
ls -la dynamic/session-handoff.md dynamic/current-iteration.md
grep -i "$(date +%Y-%m-%d)" dynamic/session-handoff.md || echo "⚠️ Session handoff not updated"
```

### Weekly Maintenance (5 minutes)
```bash
# Clean up and verify system health
find . -name "*.md" -size +10k -exec echo "Large file: {}" \;
python3 dynamic/assumption-validator.py --stability-hours 1
```

## 📋 Human Decision Templates

### When LLM Asks About Priorities
**Quick Responses:**
- `"Continue current iteration - focus on [specific task]"`
- `"Pivot to [new area] - current work is blocked"`  
- `"Run validation first - need to verify current state"`
- `"Emergency: fix [specific issue] immediately"`

### When LLM Asks About Time/Scope
**Quick Responses:**
- `"30 min session - quick progress only"`
- `"2 hour session - can tackle major tasks"`
- `"Just validation - run tests and update status"`
- `"Planning session - prepare next iteration"`

### When LLM Asks About Environment
**Quick Responses:**
- `"Environment unchanged - proceed as documented"`
- `"Network issue: target device IP changed to [new IP]"`
- `"Hardware problem: camera not accessible"`
- `"All systems normal - continue with current setup"`

## 🎯 Cost-Saving Shortcuts

### Avoid Re-Reading Large Files
**Instead of:** "Read the entire environment.md file"
**Say:** "Environment unchanged since last session - use cached context"

### Use Validation Script Results
**Instead of:** Describing manual tests
**Say:** "Run assumption-validator.py and use those results"

### Reference Previous Sessions
**Instead of:** Re-explaining context
**Say:** "Continue from session-handoff.md - no additional context needed"

### Batch Updates
**Instead of:** Multiple file updates
**Say:** "Update all context files at session end - batch the changes"

## 🔧 Emergency Procedures

### If LLM Seems Confused
```
Reset context: Read session-handoff.md only, ask one specific question about current priority, proceed with that task.
```

### If Session Goes Off-Track
```
Refocus: What's the #1 priority from session-handoff.md? Work on that only.
```

### If Files Seem Inconsistent
```
Validate system: Run assumption-validator.py, update session-handoff.md with actual current state.
```

## 📊 Success Metrics (Quick Check)

### Good Session Indicators
- [ ] LLM asked specific questions (not generic)
- [ ] Work focused on session-handoff priorities  
- [ ] Files updated with concrete progress
- [ ] Next session has clear direction

### Poor Session Indicators  
- [ ] LLM asked generic questions
- [ ] Work scattered across multiple areas
- [ ] Vague progress updates
- [ ] Unclear next steps

## 💡 Pro Tips

### Save Tokens
- Use short, specific responses to LLM questions
- Reference file names instead of describing content
- Say "continue as planned" when no changes needed
- Use validation script results instead of manual descriptions

### Save Time
- Keep session-handoff.md under 2KB for fast reading
- Use the one-line session commands above
- Batch all file updates at session end
- Run quick status checks before starting

### Maintain Quality
- Always verify LLM actually updated files
- Check that next actions are specific and actionable
- Ensure progress percentages reflect reality
- Keep failed-solutions updated when things don't work

---

**Last Updated:** July 23, 2025  
**Purpose:** Streamline human interaction with the LLM context system
