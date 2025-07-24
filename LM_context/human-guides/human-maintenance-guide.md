# Human Maintenance Guide

## Overview
This guide provides comprehensive maintenance procedures for humans managing the LLM Context Management System. It covers routine maintenance, troubleshooting, and system optimization tasks.

## 🚀 Quick Start Commands

### Starting a New Session
```
I need you to help me continue with my [PROJECT NAME] learning project. Please start by:

1. Reading the session context files (session-handoff.md, current-iteration.md, environment.md)
2. Checking failed-solutions/ directory to avoid suggesting previously failed approaches
3. Running the validation script to assess current system state
4. Asking me 3-5 specific questions based on what you find in the context
5. Summarizing the current status and recommending next actions
```

### Emergency System Reset
```
System appears to be in an inconsistent state. Please:

1. Run the assumption-validator.py script to assess current technical state
2. Read working-solutions.md to understand what's currently proven to work
3. Update session-handoff.md with the actual current state based on validation results
4. Provide a clear summary of system status and immediate next steps
```

## 🔧 Daily Maintenance Tasks

### Before Each Session (2 minutes)
```bash
# Navigate to your project context directory
cd /path/to/your/project/LM_context

# Quick system health check
python3 dynamic/assumption-validator.py --stability-hours 0.1 && echo "✅ System Ready"

# Check for large files that might slow down LLM sessions
find . -name "*.md" -size +10k -exec echo "Large file: {}" \;

# Verify critical files exist and are recent
ls -la dynamic/session-handoff.md dynamic/current-iteration.md
```

### After Each Session (3 minutes)
```bash
# Verify LLM actually updated the session handoff
grep -i "$(date +%Y-%m-%d)" dynamic/session-handoff.md || echo "⚠️ Session handoff not updated"

# Check that progress was documented
ls -la dynamic/current-iteration.md

# Ensure working solutions were updated if new solutions were found
ls -la dynamic/working-solutions.md
```

## 📊 Weekly Maintenance (15 minutes)

### File Size Management
```bash
# Find files that are getting too large
find . -name "*.md" -size +10k -exec ls -lh {} \;

# Check total context size (should be under 50KB for efficiency)
find . -name "*.md" -exec wc -c {} + | tail -1

# Archive old daily logs if they exist
find archive/daily-logs/ -name "*.md" -mtime +30 -exec echo "Archive candidate: {}" \;
```

### System Health Validation
```bash
# Run comprehensive validation
python3 dynamic/assumption-validator.py --stability-hours 1

# Check for inconsistencies in context files
grep -r "TODO\|FIXME\|TBD" . --include="*.md"

# Verify all failed solutions are properly documented
find dynamic/failed-solutions/ -name "*.md" -exec echo "Checking: {}" \;
```

### Knowledge Base Maintenance
```bash
# Check for duplicate solutions
grep -r "## " dynamic/working-solutions.md | sort | uniq -d

# Verify cross-references are still valid
grep -r "see.*\.md" . --include="*.md"

# Update knowledge base timestamps
find static/knowledge-base/ -name "*.md" -mtime +7 -exec echo "Knowledge base needs update: {}" \;
```

## 🎯 Monthly Maintenance (30 minutes)

### 1. Context System Audit
**Goal:** Ensure the context management system is working effectively

**Tasks:**
```bash
# Analyze session effectiveness over the past month
find archive/daily-logs/ -name "*.md" -mtime -30 -exec grep -l "✅" {} \;

# Check for repeated failures (indicates system issues)
find dynamic/failed-solutions/ -name "*.md" -exec grep -c "Date:" {} \;

# Verify validation script is being used regularly
grep -r "assumption-validator" archive/daily-logs/ | wc -l
```

### 2. Performance Analysis
**Goal:** Optimize system performance and token usage

**Tasks:**
- **File Size Analysis:** Identify files that have grown too large
- **Content Duplication:** Find and consolidate duplicate information
- **Access Patterns:** Review which files are read most frequently
- **Token Usage:** Estimate token consumption and optimization opportunities

### 3. Knowledge Base Consolidation
**Goal:** Organize and optimize accumulated knowledge

**Tasks:**
```bash
# Consolidate similar working solutions
# Review static/knowledge-base/ for outdated information
# Update quick reference guides
# Archive completed iterations and old experiments
```

## 🚨 Troubleshooting Common Issues

### Issue: LLM Sessions Are Unfocused
**Symptoms:**
- LLM asks generic questions like "What would you like to work on?"
- No reference to specific project context
- Repeated questions across sessions

**Diagnosis:**
```bash
# Check session handoff quality
wc -l dynamic/session-handoff.md  # Should be 50-100 lines
grep -i "priority\|next\|action" dynamic/session-handoff.md
grep -c "TODO\|TBD\|unclear" dynamic/session-handoff.md  # Should be 0
```

**Solutions:**
1. **Update session handoff** with specific, actionable priorities
2. **Add concrete next steps** with exact commands or tasks
3. **Include specific questions** the LLM should ask
4. **Reference specific files** and line numbers when possible

### Issue: Context Files Are Too Large
**Symptoms:**
- LLM sessions slow to start
- Token usage warnings
- Files over 10KB in size

**Diagnosis:**
```bash
# Find large files
find . -name "*.md" -size +10k -exec ls -lh {} \;

# Check for repetitive content
find . -name "*.md" -exec grep -c "repeated pattern" {} \;
```

**Solutions:**
1. **Archive completed work** to archive/ directory
2. **Consolidate similar content** across files
3. **Use references** instead of duplicating information
4. **Split large files** into focused, smaller files

### Issue: Validation Script Failures
**Symptoms:**
- Script exits with errors
- No validation results generated
- Environment setup problems

**Diagnosis:**
```bash
# Check script syntax
python3 -m py_compile dynamic/assumption-validator.py

# Verify dependencies
python3 -c "import sys; print(sys.version)"

# Check file permissions
ls -la dynamic/assumption-validator.py
```

**Solutions:**
1. **Fix syntax errors** using Python linter
2. **Install missing dependencies** for your project domain
3. **Update script permissions** to executable
4. **Customize validation methods** for your specific project

### Issue: Knowledge Not Being Preserved
**Symptoms:**
- Repeated work across sessions
- Lost insights and solutions
- No learning accumulation

**Diagnosis:**
```bash
# Check knowledge base updates
ls -la static/knowledge-base/

# Verify working solutions tracking
wc -l dynamic/working-solutions.md

# Check daily logs creation
ls -la archive/daily-logs/
```

**Solutions:**
1. **Update knowledge base** after each session
2. **Document working solutions** with exact commands
3. **Create daily logs** with session summaries
4. **Cross-reference** related solutions and insights

## 🔄 System Recovery Procedures

### Complete Context Reset
**When to use:** System state is completely unclear or inconsistent

**Procedure:**
```bash
# 1. Backup current state
cp -r . ../backup-$(date +%Y%m%d)

# 2. Run validation to assess actual technical state
python3 dynamic/assumption-validator.py --save-results

# 3. Reset session handoff to minimal context
echo "System reset - starting fresh with basic project context" > dynamic/session-handoff.md

# 4. Update current iteration with reset status
# Edit dynamic/current-iteration.md to reflect reset state

# 5. Preserve working solutions
# Keep dynamic/working-solutions.md intact - this is valuable

# 6. Start fresh session with clear priorities
```

### Partial Context Recovery
**When to use:** Some context files are inconsistent but core system is working

**Procedure:**
1. **Identify problematic files** using validation script
2. **Restore from backup** if available
3. **Rebuild from working solutions** and validation results
4. **Update session handoff** with current actual state
5. **Test system** with a short LLM session

## 📋 Quality Assurance Checklists

### Before Starting LLM Session
- [ ] Session handoff file updated within 24 hours
- [ ] Current iteration has specific, measurable goals
- [ ] Validation script runs without errors
- [ ] No files over 10KB without justification
- [ ] Failed solutions documented for current work area

### After LLM Session
- [ ] Session handoff updated with concrete next steps
- [ ] Working solutions documented with exact commands
- [ ] Knowledge base updated with new insights
- [ ] Daily log created in archive/ (if applicable)
- [ ] Current iteration progress updated with evidence

### Weekly System Health
- [ ] All files under size limits
- [ ] No stale content over 1 week old
- [ ] Validation script health verified
- [ ] Knowledge base consolidated and organized
- [ ] Archive cleaned of old, irrelevant content

## 💡 Optimization Tips

### Token Usage Optimization
- **Keep session-handoff.md under 2KB** for fast reading
- **Use references** instead of duplicating content
- **Archive completed work** regularly
- **Consolidate similar solutions** to reduce redundancy

### Session Efficiency
- **Use one-line session commands** from this guide
- **Batch file updates** at session end
- **Run quick status checks** before starting
- **Prepare specific questions** for the LLM

### Knowledge Management
- **Document as you go** during sessions
- **Use consistent formats** for all documentation
- **Cross-reference related content** for easy navigation
- **Validate solutions** before documenting them

## 🎯 Success Metrics

### Good System Health Indicators
- [ ] LLM sessions start quickly with clear context
- [ ] Specific, actionable questions from LLM
- [ ] Consistent progress on project goals
- [ ] Knowledge accumulation over time
- [ ] Reduced repetition of solved problems

### System Performance Metrics
- **Average session startup time:** < 30 seconds
- **Context file sizes:** < 10KB each
- **Token usage per session:** < 5,000 tokens
- **Knowledge reuse rate:** > 50% of solutions referenced
- **Problem resolution time:** Decreasing over time

---

**Last Updated:** July 23, 2025  
**Purpose:** Human maintenance procedures for LLM Context Management System  
**Scope:** Generic procedures applicable to any project domain
