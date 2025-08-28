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
    - [ ] Special character requirement
    - [ ] Uppercase/lowercase mix
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
  const parser = new noteBlocksParser();
  const collection = parser.parse("2025-08-28.md", realWorldContent);
  
  console.log("📊 Real-World Scenario Results:");
  console.log("Total blocks:", collection.blocks.length);
  console.log("Block types:", collection.getStats().types);
  console.log("Root blocks:", collection.getRootBlocks().length);
  console.log("Blocks with parents:", collection.blocks.filter(b => b.parent).length);
  
  console.log("\n🎯 Daily Notes Analysis:");
  
  // Analyze task structure
  const todos = collection.findByType("todo");
  const done = collection.findByType("done");
  console.log("Total todos:", todos.length);
  console.log("Completed tasks:", done.length);
  console.log("Completion rate:", Math.round((done.length / (todos.length + done.length)) * 100) + "%");
  
  // Analyze hierarchy depth
  const indentLevels = collection.blocks.map(b => b.getAttribute("indentLevel") || 0);
  const maxDepth = Math.max(...indentLevels);
  const avgDepth = indentLevels.reduce((a, b) => a + b, 0) / indentLevels.length;
  console.log("Maximum nesting depth:", maxDepth);
  console.log("Average nesting depth:", Math.round(avgDepth * 100) / 100);
  
  // Analyze content types
  const headers = collection.findByType("header");
  const mentions = collection.findByType("mention");
  const callouts = collection.findByType("callout");
  const codeBlocks = collection.findByType("code");
  
  console.log("Headers:", headers.length);
  console.log("Mentions:", mentions.length);
  console.log("Callouts:", callouts.length);
  console.log("Code blocks:", codeBlocks.length);
  
  console.log("\n🔗 Activity References Analysis:");
  const activityMentions = mentions.filter(block => {
    const target = block.getAttribute("target");
    return target && target.startsWith("Activities/");
  });
  console.log("Activity mentions:", activityMentions.length);
  
  // Group by activity
  const activityGroups = {};
  activityMentions.forEach(block => {
    const target = block.getAttribute("target");
    if (!activityGroups[target]) {
      activityGroups[target] = 0;
    }
    activityGroups[target]++;
  });
  
  console.log("Most referenced activities:");
  Object.entries(activityGroups)
    .sort(([,a], [,b]) => b - a)
    .slice(0, 5)
    .forEach(([activity, count]) => {
      console.log(`  ${activity}: ${count} references`);
    });
  
  console.log("\n🌳 Hierarchy Structure Sample:");
  const hierarchy = collection.getHierarchy();
  
  function printRealWorldHierarchy(nodes, indent = "", maxNodes = 3, maxDepth = 3, currentDepth = 0) {
    if (currentDepth >= maxDepth) return;
    
    nodes.slice(0, maxNodes).forEach((node, i) => {
      const block = node.block;
      const type = block.getAttribute("type");
      const level = block.getAttribute("level") || "";
      const indentLevel = block.getAttribute("indentLevel") || 0;
      const preview = block.content.substring(0, 60).replace(/\n/g, " ");
      
      console.log(`${indent}├─ ${type}${level ? `:${level}` : ""} (i:${indentLevel}) "${preview}"`);
      
      if (node.children.length > 0 && currentDepth < maxDepth - 1) {
        const childCount = node.children.length;
        if (childCount > maxNodes) {
          console.log(`${indent}│  ├─ ... (${childCount - maxNodes} more children)`);
        }
        printRealWorldHierarchy(node.children, indent + "│  ", maxNodes, maxDepth, currentDepth + 1);
      }
    });
  }
  
  printRealWorldHierarchy(hierarchy);
  
  console.log("\n📈 Productivity Metrics:");
  
  // Calculate task distribution by section
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
  
  console.log("Tasks by section:");
  Object.entries(sectionTasks).forEach(([section, count]) => {
    console.log(`  ${section}: ${count} tasks`);
  });
  
  // Time-based analysis (if timestamps present)
  const timeReferences = collection.blocks.filter(block => 
    /\d{2}:\d{2}/.test(block.content)
  );
  console.log("Time references found:", timeReferences.length);
  
  console.log("\n✅ Real-world scenario test completed!");
  console.log("This daily note structure demonstrates complex hierarchy with practical content.");
  
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
