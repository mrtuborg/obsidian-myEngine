# Test: Real-World Daily Notes Scenario

This test simulates a real daily note with complex hierarchy and mixed content types.

```dataviewjs
// Test real-world daily notes scenario
const { noteBlocksParser } = await cJS();

console.log("=== Testing Real-World Daily Notes Scenario ===");

const realWorldContent = `---
date: 2025-08-28
---

# 28 August 2025

## Morning Planning
- [ ] Review [[Activities/Project Alpha]] status
  - [ ] Check milestone progress
  - [ ] Update timeline estimates
    - [ ] Backend development: 2 weeks remaining
    - [ ] Frontend integration: 1 week remaining
  - [ ] Schedule team meeting
- [ ] Process [[Activities/Client Beta]] feedback
  - [ ] Address UI concerns
    > Client mentioned: "Navigation feels confusing"
    > Priority: High
  - [ ] Update documentation
- [x] Complete [[Activities/Daily Standup]] preparation

## Work Sessions

### Session 1: Development Work
Started: 09:00
- [ ] Implement user authentication
  - [x] Set up JWT tokens
  - [ ] Add password validation
    - [ ] Minimum 8 characters
      - [ ] Check length validation
      - [ ] Test edge cases
    - [ ] Special character requirement
      - [ ] Require at least one symbol
      - [ ] Test various symbols
    - [ ] Uppercase/lowercase mix
      - [ ] Require both cases
      - [ ] Validate mixed case
  - [ ] Test login flow
- [ ] Code review for [[Activities/Feature X]]
  > Review notes:
  > - Good error handling
  > - Need more unit tests
  > - Consider edge cases

\`\`\`javascript
// Authentication implementation
function validatePassword(password) {
  // Implementation for [[Activities/Security Audit]]
  return password.length >= 8;
}
\`\`\`

### Session 2: Meetings
- [x] Daily standup with team
  - [x] Discussed [[Activities/Sprint Planning]]
  - [x] Reviewed blockers
    - [x] Database migration issue resolved
    - [ ] API rate limiting still pending
- [ ] Client call about [[Activities/Project Gamma]]
  - [ ] Present mockups
    - [ ] Homepage design
    - [ ] User dashboard
    - [ ] Settings page
  - [ ] Discuss timeline
  - [ ] Get approval for next phase

## Afternoon Tasks

### Bug Fixes
- [x] Fixed critical bug in [[Activities/Payment System]]
  - [x] Issue: Transaction timeout
  - [x] Solution: Increased timeout to 30s
  - [x] Testing: All payment flows working
- [ ] Investigate [[Activities/Performance Issues]]
  - [ ] Database query optimization
    - [ ] Add indexes to user table
    - [ ] Optimize JOIN operations
    - [ ] Cache frequently accessed data
  - [ ] Frontend performance
    - [ ] Lazy load components
    - [ ] Optimize bundle size

### Documentation
- [ ] Update [[Activities/API Documentation]]
  - [ ] New authentication endpoints
    - [ ] POST /auth/login
    - [ ] POST /auth/refresh
    - [ ] DELETE /auth/logout
  - [ ] Error response formats
- [ ] Write deployment guide for [[Activities/DevOps Setup]]

## Evening Reflection

### Completed Today
- [x] Authentication system foundation
- [x] Critical payment bug fix
- [x] Team standup and planning
- [x] Client feedback processing

### Tomorrow's Priorities
- [ ] Finish password validation
- [ ] Complete API documentation
- [ ] Client presentation for [[Activities/Project Gamma]]
- [ ] Performance optimization sprint

### Notes and Ideas
> Idea: Consider implementing 2FA for [[Activities/Security Audit]]
> 
> Research: Look into Redis caching for [[Activities/Performance Issues]]
> 
> Follow-up: Schedule architecture review meeting

## Links and References
[[Activities/Project Alpha]] - Main development project
  [[Activities/Feature X]] - Specific feature branch
    [[Activities/Security Audit]] - Security requirements
[[Activities/Client Beta]] - Client feedback project
[[Activities/Project Gamma]] - New client project
  [[Activities/Sprint Planning]] - Agile planning
[[Activities/Payment System]] - E-commerce integration
[[Activities/Performance Issues]] - Optimization tasks
[[Activities/API Documentation]] - Technical docs
[[Activities/DevOps Setup]] - Infrastructure

----

## Personal Notes
Had a productive day overall. The authentication system is coming together well.
Need to focus more on testing tomorrow.

Weather: Sunny, 22°C
Mood: Productive
Energy: 8/10`;

try {
  dv.header(2, "🧪 Real-World Daily Notes Test");
  dv.paragraph("**Testing:** Complex daily note with realistic content, deep nesting, and multiple content types");
  
  // Load CustomJS factories
  const cjsResult = await cJS();
  const noteBlocksParser = cjsResult.createnoteBlocksParserInstance;
  
  if (!noteBlocksParser) {
    throw new Error("noteBlocksParser factory not found in CustomJS");
  }
  
  const parser = noteBlocksParser();
  const collection = await parser.parse("2025-08-28.md", realWorldContent);
  
  // Basic Results
  dv.header(3, "📊 Parsing Results");
  const stats = collection.getStats();
  const rootBlocks = collection.getRootBlocks().length;
  const blocksWithParents = collection.blocks.filter(b => b.parent).length;
  
  dv.paragraph(`✅ **Total blocks parsed:** ${collection.blocks.length}`);
  dv.paragraph(`✅ **Root blocks:** ${rootBlocks}`);
  dv.paragraph(`✅ **Child blocks:** ${blocksWithParents}`);
  dv.paragraph(`✅ **Block types:** ${Object.keys(stats.types).join(", ")}`);
  
  // Task Analysis
  dv.header(3, "🎯 Task Analysis");
  const todos = collection.findByType("todo");
  const done = collection.findByType("done");
  const totalTasks = todos.length + done.length;
  const completionRate = totalTasks > 0 ? Math.round((done.length / totalTasks) * 100) : 0;
  
  dv.paragraph(`✅ **Todo items:** ${todos.length}`);
  dv.paragraph(`✅ **Completed tasks:** ${done.length}`);
  dv.paragraph(`✅ **Completion rate:** ${completionRate}%`);
  
  // Hierarchy Analysis
  dv.header(3, "🏗️ Hierarchy Analysis");
  const indentLevels = collection.blocks.map(b => b.getAttribute("indentLevel") || 0);
  const maxDepth = Math.max(...indentLevels);
  const avgDepth = indentLevels.reduce((a, b) => a + b, 0) / indentLevels.length;
  
  dv.paragraph(`✅ **Maximum nesting depth:** ${maxDepth} levels`);
  dv.paragraph(`✅ **Average nesting depth:** ${Math.round(avgDepth * 100) / 100} levels`);
  
  // Content Type Analysis
  dv.header(3, "📝 Content Type Analysis");
  const headers = collection.findByType("header");
  const mentions = collection.findByType("mention");
  const callouts = collection.findByType("callout");
  const codeBlocks = collection.findByType("code");
  
  dv.paragraph(`✅ **Headers:** ${headers.length}`);
  dv.paragraph(`✅ **Mentions:** ${mentions.length}`);
  dv.paragraph(`✅ **Callouts:** ${callouts.length}`);
  dv.paragraph(`✅ **Code blocks:** ${codeBlocks.length}`);
  
  // Activity References
  dv.header(3, "🔗 Activity References");
  const activityMentions = mentions.filter(block => {
    const target = block.getAttribute("target");
    return target && target.startsWith("Activities/");
  });
  
  dv.paragraph(`✅ **Activity mentions found:** ${activityMentions.length}`);
  
  // Group by activity and show top 5
  const activityGroups = {};
  activityMentions.forEach(block => {
    const target = block.getAttribute("target");
    if (!activityGroups[target]) {
      activityGroups[target] = 0;
    }
    activityGroups[target]++;
  });
  
  const topActivities = Object.entries(activityGroups)
    .sort(([,a], [,b]) => b - a)
    .slice(0, 5);
  
  if (topActivities.length > 0) {
    dv.paragraph("**Most referenced activities:**");
    topActivities.forEach(([activity, count]) => {
      dv.paragraph(`• **${activity}:** ${count} references`);
    });
  }
  
  // Productivity Metrics
  dv.header(3, "📈 Productivity Metrics");
  const sectionTasks = {};
  headers.forEach(header => {
    const sectionName = header.content.replace(/^#+\s*/, "");
    const sectionTodos = header.children.filter(child => 
      child.getAttribute("type") === "todo" || child.getAttribute("type") === "done"
    );
    if (sectionTodos.length > 0) {
      sectionTasks[sectionName] = sectionTodos.length;
    }
  });
  
  if (Object.keys(sectionTasks).length > 0) {
    dv.paragraph("**Tasks by section:**");
    Object.entries(sectionTasks).forEach(([section, count]) => {
      dv.paragraph(`• **${section}:** ${count} tasks`);
    });
  }
  
  // Time References
  const timeReferences = collection.blocks.filter(block => 
    /\d{2}:\d{2}/.test(block.content)
  );
  dv.paragraph(`✅ **Time references found:** ${timeReferences.length}`);
  
  // Test Validation
  dv.header(3, "✅ Test Validation");
  let allTestsPassed = true;
  let testResults = [];
  
  // Test 1: Should parse many blocks (realistic daily note)
  if (collection.blocks.length >= 40) {
    testResults.push("✅ **Complex parsing:** Large number of blocks parsed successfully");
  } else {
    testResults.push("❌ **Complex parsing:** Fewer blocks than expected for complex content");
    allTestsPassed = false;
  }
  
  // Test 2: Should have deep hierarchy
  if (maxDepth >= 6) {
    testResults.push("✅ **Deep nesting:** Complex hierarchy structure preserved");
  } else {
    testResults.push("❌ **Deep nesting:** Hierarchy depth insufficient");
    allTestsPassed = false;
  }
  
  // Test 3: Should find activity mentions
  if (activityMentions.length >= 10) {
    testResults.push("✅ **Activity tracking:** Multiple activity references found");
  } else {
    testResults.push("❌ **Activity tracking:** Too few activity references");
    allTestsPassed = false;
  }
  
  // Test 4: Should have mixed content types
  if (Object.keys(stats.types).length >= 5) {
    testResults.push("✅ **Content variety:** Multiple content types recognized");
  } else {
    testResults.push("❌ **Content variety:** Insufficient content type diversity");
    allTestsPassed = false;
  }
  
  // Test 5: Should calculate productivity metrics
  if (totalTasks > 0 && Object.keys(sectionTasks).length > 0) {
    testResults.push("✅ **Productivity metrics:** Task analysis working correctly");
  } else {
    testResults.push("❌ **Productivity metrics:** Unable to calculate task metrics");
    allTestsPassed = false;
  }
  
  testResults.forEach(result => dv.paragraph(result));
  
  if (allTestsPassed) {
    dv.paragraph("🎉 **ALL TESTS PASSED!** Real-world scenario handling is working perfectly.");
    dv.paragraph("The Block system successfully handles complex daily notes with deep nesting, multiple content types, and realistic productivity tracking.");
  } else {
    dv.paragraph("⚠️ **SOME TESTS FAILED.** Check the results above for details.");
  }
  
} catch (error) {
  console.error("❌ Real-world scenario test failed:", error);
  console.error(error.stack);
}
```

**Expected Results:**
- Complex nested todo structure should be preserved
- Activity mentions should be properly linked
- Multiple content types should coexist in hierarchy
- Performance should remain good with realistic content volume
- Productivity metrics should be calculable from the structure
