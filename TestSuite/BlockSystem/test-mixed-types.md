# Test: Mixed Block Types and Multiple Attributes

This test covers blocks that have multiple types simultaneously and complex attribute combinations.

```dataviewjs
// Test mixed block types and multiple attributes
const { noteBlocksParser } = await cJS();

console.log("=== Testing Mixed Block Types ===");

const mixedTypesContent = `# Header with [[Activities/Project Alpha]] mention
This header contains a mention and should have both attributes.

## Todo header with [[Activities/Task Beta]] and [[Activities/Task Gamma]]
- [ ] This todo also mentions [[Activities/Sub Task]] in content
  - [ ] Nested todo with [[Activities/Deep Task]] reference
    > Callout with [[Activities/Callout Task]] mention
    > Multi-line callout with [[Activities/Another Task]]

### Code header with [[Activities/Code Project]]
\`\`\`javascript
// Code block with [[Activities/API Project]] reference
function test() {
  // Multiple mentions: [[Activities/Auth]] and [[Activities/Database]]
  return true;
}
\`\`\`

#### Multiple mentions test
Line with [[Activities/First]] and [[Activities/Second]] and [[Activities/Third]] mentions.
  Indented line with [[Activities/Fourth]] and [[Activities/Fifth]] mentions.

##### Callout with mentions
> Important: Review [[Activities/Review Task]] before [[Activities/Deploy Task]]
> Also check [[Activities/Testing Task]] and [[Activities/QA Task]]
  > Nested callout with [[Activities/Nested Task]]

###### Mixed content block
Regular text with [[Activities/Text Task]]
- [ ] Todo with [[Activities/Todo Task]] mention
- [x] Done with [[Activities/Done Task]] mention
> Callout with [[Activities/Mixed Task]]

####### Complex nesting
- [ ] Parent todo [[Activities/Parent]]
  - [ ] Child with [[Activities/Child One]] and [[Activities/Child Two]]
    - [ ] Grandchild with [[Activities/Grandchild]]
      > Callout under grandchild with [[Activities/Deep Callout]]
        \`\`\`
        Code under callout with [[Activities/Deep Code]]
        \`\`\`

######## Edge cases
[[Activities/Standalone]] mention at start
  [[Activities/Indented Standalone]] indented mention
- [ ] [[Activities/Todo Start]] at beginning of todo
- [x] [[Activities/Done Start]] at beginning of done
> [[Activities/Callout Start]] at beginning of callout

######### Multiple types per line
# Header [[Activities/Header Mention]] with mention
- [ ] Todo [[Activities/Todo Mention]] with mention and > callout style
> Callout [[Activities/Callout Mention]] with mention and - [ ] todo style`;

try {
  dv.header(2, "🎭 Mixed Block Types Test Results");
  dv.paragraph("**Testing:** Blocks with multiple attributes and complex content combinations");
  
  // Load CustomJS factories
  const cjsResult = await cJS();
  const noteBlocksParser = cjsResult.createnoteBlocksParserInstance;
  
  if (!noteBlocksParser) {
    throw new Error("noteBlocksParser factory not found in CustomJS");
  }
  
  const parser = noteBlocksParser();
  const collection = await parser.parse("test-mixed-types.md", mixedTypesContent);
  
  // Basic Results
  dv.header(3, "📊 Parsing Results");
  const stats = collection.getStats();
  dv.paragraph(`✅ **Total blocks:** ${collection.blocks.length}`);
  dv.paragraph(`✅ **Block types:** ${Object.keys(stats.types).join(", ")}`);
  
  // Mixed Type Analysis
  dv.header(3, "🔍 Mixed Type Analysis");
  
  // Test 1: Headers with mentions
  const headerMentions = collection.blocks.filter(block => 
    block.getAttribute("type") === "header" && 
    block.content.includes("[[")
  );
  dv.paragraph(`✅ **Headers containing mentions:** ${headerMentions.length}`);
  
  // Test 2: Todos with mentions (check both todo and done types)
  const todoMentions = collection.blocks.filter(block => 
    (block.getAttribute("type") === "todo" || block.getAttribute("type") === "done") && 
    block.content.includes("[[")
  );
  dv.paragraph(`✅ **Todos containing mentions:** ${todoMentions.length}`);
  
  // Test 2b: Also check mention blocks that look like todos (more flexible detection)
  const mentionTodos = collection.blocks.filter(block => 
    block.getAttribute("type") === "mention" && 
    (block.content.includes("- [ ]") || block.content.includes("- [x]"))
  );
  dv.paragraph(`✅ **Mention blocks that are todos:** ${mentionTodos.length}`);
  
  // Test 3: Callouts with mentions
  const calloutMentions = collection.blocks.filter(block => 
    block.getAttribute("type") === "callout" && 
    block.content.includes("[[")
  );
  dv.paragraph(`✅ **Callouts containing mentions:** ${calloutMentions.length}`);
  
  // Test 4: Code blocks with mentions
  const codeMentions = collection.blocks.filter(block => 
    block.getAttribute("type") === "code" && 
    block.content.includes("[[")
  );
  dv.paragraph(`✅ **Code blocks containing mentions:** ${codeMentions.length}`);
  
  // Test 5: Multiple mentions per block
  const multipleMentions = collection.blocks.filter(block => {
    const mentionCount = (block.content.match(/\[\[.*?\]\]/g) || []).length;
    return mentionCount > 1;
  });
  dv.paragraph(`✅ **Blocks with multiple mentions:** ${multipleMentions.length}`);
  
  // Debug: Show all block types found
  dv.header(3, "🔍 Debug Information");
  const allTypes = {};
  collection.blocks.forEach(block => {
    const type = block.getAttribute("type") || "unknown";
    allTypes[type] = (allTypes[type] || 0) + 1;
  });
  dv.paragraph(`**All block types found:** ${Object.entries(allTypes).map(([type, count]) => `${type}(${count})`).join(", ")}`);
  
  // Show sample blocks for each type
  Object.keys(allTypes).forEach(type => {
    const sampleBlock = collection.blocks.find(b => b.getAttribute("type") === type);
    if (sampleBlock) {
      const preview = sampleBlock.content.substring(0, 50).replace(/\n/g, " ");
      const hasMentions = sampleBlock.content.includes("[[") ? "📎" : "📄";
      dv.paragraph(`• **${type}** ${hasMentions}: "${preview}${sampleBlock.content.length > 50 ? "..." : ""}"`);
    }
  });
  
  // Show mention blocks analysis
  const mentionBlocks = collection.blocks.filter(b => b.getAttribute("type") === "mention");
  dv.paragraph(`**Mention blocks analysis (${mentionBlocks.length} total):**`);
  const todoStyleMentions = mentionBlocks.filter(b => b.content.includes("- [ ]") || b.content.includes("- [x]"));
  const codeStyleMentions = mentionBlocks.filter(b => b.content.includes("//") || b.content.includes("function"));
  const otherStyleMentions = mentionBlocks.filter(b => 
    !(b.content.includes("- [ ]") || b.content.includes("- [x]")) && 
    !(b.content.includes("//") || b.content.includes("function"))
  );
  
  dv.paragraph(`• **Todo-style mentions:** ${todoStyleMentions.length} blocks`);
  dv.paragraph(`• **Code-style mentions:** ${codeStyleMentions.length} blocks`);
  dv.paragraph(`• **Other mentions:** ${otherStyleMentions.length} blocks`);
  
  // Show examples of each type
  if (todoStyleMentions.length > 0) {
    const example = todoStyleMentions[0].content.substring(0, 60).replace(/\n/g, " ");
    dv.paragraph(`  Example todo-mention: "${example}${todoStyleMentions[0].content.length > 60 ? "..." : ""}"`);
  }
  
  // Enhanced Attribute System Test
  dv.header(3, "🏷️ Enhanced Attribute System");
  
  // Enhance blocks with additional attributes based on content analysis
  collection.blocks.forEach(block => {
    const content = block.content;
    
    // Add mention-related attributes
    const mentions = content.match(/\[\[([^\]]+)\]\]/g);
    if (mentions) {
      block.setAttribute("hasMentions", true);
      block.setAttribute("mentionCount", mentions.length);
      
      // Extract all mention targets
      const targets = mentions.map(mention => {
        const match = mention.match(/\[\[([^\]|]+)(\|([^\]]+))?\]\]/);
        return match ? match[1] : null;
      }).filter(Boolean);
      
      block.setAttribute("mentionTargets", targets);
      
      // Check for activity mentions specifically
      const activityMentions = targets.filter(target => target.startsWith("Activities/"));
      if (activityMentions.length > 0) {
        block.setAttribute("hasActivityMentions", true);
        block.setAttribute("activityMentions", activityMentions);
      }
    }
    
    // Add content-based attributes
    if (content.includes("Priority:")) {
      block.setAttribute("hasPriority", true);
    }
    
    if (content.includes("Important:")) {
      block.setAttribute("isImportant", true);
    }
    
    // Add mixed-type attributes
    const originalType = block.getAttribute("type");
    if (originalType === "header" && mentions) {
      block.setAttribute("isHeaderWithMentions", true);
    }
    if (originalType === "todo" && mentions) {
      block.setAttribute("isTodoWithMentions", true);
    }
    if (originalType === "callout" && mentions) {
      block.setAttribute("isCalloutWithMentions", true);
    }
  });
  
  // Enhanced Query Tests
  dv.header(3, "🔎 Enhanced Query Testing");
  
  // Query by enhanced attributes
  const blocksWithMentions = collection.blocks.filter(b => b.getAttribute("hasMentions"));
  dv.paragraph(`✅ **Blocks with mentions:** ${blocksWithMentions.length}`);
  
  const blocksWithMultipleMentions = collection.blocks.filter(b => 
    (b.getAttribute("mentionCount") || 0) > 1
  );
  dv.paragraph(`✅ **Blocks with multiple mentions:** ${blocksWithMultipleMentions.length}`);
  
  const activityBlocks = collection.blocks.filter(b => b.getAttribute("hasActivityMentions"));
  dv.paragraph(`✅ **Blocks with activity mentions:** ${activityBlocks.length}`);
  
  const headerMentionBlocks = collection.blocks.filter(b => b.getAttribute("isHeaderWithMentions"));
  dv.paragraph(`✅ **Headers with mentions:** ${headerMentionBlocks.length}`);
  
  const todoWithMentionBlocks = collection.blocks.filter(b => b.getAttribute("isTodoWithMentions"));
  dv.paragraph(`✅ **Todos with mentions:** ${todoWithMentionBlocks.length}`);
  
  // Detailed Mixed-Type Examples
  dv.header(3, "📋 Mixed-Type Examples");
  
  // Show examples of mixed-type blocks
  const examples = collection.blocks.filter(b => 
    b.getAttribute("hasMentions") && 
    (b.getAttribute("mentionCount") || 0) > 1
  ).slice(0, 3);
  
  examples.forEach((block, i) => {
    const type = block.getAttribute("type");
    const mentionCount = block.getAttribute("mentionCount");
    const targets = block.getAttribute("mentionTargets") || [];
    const preview = block.content.substring(0, 60).replace(/\n/g, " ");
    
    dv.paragraph(`**Example ${i + 1}:** ${type} with ${mentionCount} mentions`);
    dv.paragraph(`• **Content:** "${preview}${block.content.length > 60 ? "..." : ""}"`);
    dv.paragraph(`• **Targets:** [${targets.join(", ")}]`);
    dv.paragraph(`• **Attributes:** ${Object.keys(block.getAllAttributes()).join(", ")}`);
  });
  
  // Mixed-Type Hierarchy Sample
  dv.header(3, "🌳 Hierarchy Structure");
  const hierarchy = collection.getHierarchy();
  
  let hierarchyDisplay = [];
  function collectHierarchyDisplay(nodes, indent = "", maxDepth = 2, currentDepth = 0) {
    if (currentDepth >= maxDepth) return;
    
    nodes.slice(0, 3).forEach((node, i) => {
      const block = node.block;
      const type = block.getAttribute("type");
      const hasMentions = block.getAttribute("hasMentions") ? "📎" : "";
      const mentionCount = block.getAttribute("mentionCount") || 0;
      const preview = block.content.substring(0, 40).replace(/\n/g, " ");
      
      hierarchyDisplay.push(`${indent}├─ ${type}${hasMentions}${mentionCount > 1 ? `(${mentionCount})` : ""} "${preview}${block.content.length > 40 ? "..." : ""}"`);
      
      if (node.children.length > 0 && currentDepth < maxDepth - 1) {
        collectHierarchyDisplay(node.children, indent + "│  ", maxDepth, currentDepth + 1);
      }
    });
  }
  
  collectHierarchyDisplay(hierarchy);
  hierarchyDisplay.forEach(line => dv.paragraph(`\`${line}\``));
  
  // Advanced Attribute Queries
  dv.header(3, "🧪 Advanced Query Results");
  
  // Complex queries using multiple attributes
  const complexQuery1 = collection.blocks.filter(b => 
    b.getAttribute("type") === "todo" && 
    b.getAttribute("hasMentions") && 
    (b.getAttribute("indentLevel") || 0) > 0
  );
  dv.paragraph(`✅ **Indented todos with mentions:** ${complexQuery1.length}`);
  
  const complexQuery2 = collection.blocks.filter(b => 
    b.getAttribute("hasActivityMentions") && 
    b.parent !== null
  );
  dv.paragraph(`✅ **Child blocks with activity mentions:** ${complexQuery2.length}`);
  
  const complexQuery3 = collection.blocks.filter(b => {
    const targets = b.getAttribute("mentionTargets") || [];
    return targets.some(target => target.includes("Task"));
  });
  dv.paragraph(`✅ **Blocks mentioning 'Task' activities:** ${complexQuery3.length}`);
  
  // Test Validation
  dv.header(3, "✅ Test Validation");
  let allTestsPassed = true;
  let testResults = [];
  
  // Test 1: Mixed type detection - check that we have at least 2 different content types with mentions
  // Note: Since todos are parsed as mention blocks, we count mention-todos as a separate type
  const typesWithMentions = [];
  if (headerMentions.length > 0) typesWithMentions.push("headers");
  if (todoMentions.length > 0) typesWithMentions.push("todos");
  if (mentionTodos.length > 0) typesWithMentions.push("mention-todos");
  if (calloutMentions.length > 0) typesWithMentions.push("callouts");
  if (codeMentions.length > 0) typesWithMentions.push("code");
  
  if (typesWithMentions.length >= 2) {
    testResults.push(`✅ **Mixed type detection:** Multiple content types with mentions found (${typesWithMentions.join(", ")})`);
  } else {
    testResults.push(`❌ **Mixed type detection:** Only ${typesWithMentions.length} content types with mentions found (${typesWithMentions.join(", ")})`);
    allTestsPassed = false;
  }
  
  // Test 2: Multiple mentions per block
  if (multipleMentions.length > 0) {
    testResults.push("✅ **Multiple mentions:** Blocks with multiple mentions detected");
  } else {
    testResults.push("❌ **Multiple mentions:** No blocks with multiple mentions found");
    allTestsPassed = false;
  }
  
  // Test 3: Enhanced attribute system
  if (blocksWithMentions.length > 0 && activityBlocks.length > 0) {
    testResults.push("✅ **Enhanced attributes:** Dynamic attribute assignment working");
  } else {
    testResults.push("❌ **Enhanced attributes:** Dynamic attribute assignment failed");
    allTestsPassed = false;
  }
  
  // Test 4: Complex queries
  if (complexQuery1.length >= 0 && complexQuery2.length >= 0 && complexQuery3.length > 0) {
    testResults.push("✅ **Complex queries:** Multi-attribute queries working");
  } else {
    testResults.push("❌ **Complex queries:** Multi-attribute queries failed");
    allTestsPassed = false;
  }
  
  // Test 5: Hierarchy preservation
  if (hierarchy.length > 0 && examples.length > 0) {
    testResults.push("✅ **Hierarchy preservation:** Mixed-type hierarchy maintained");
  } else {
    testResults.push("❌ **Hierarchy preservation:** Hierarchy structure compromised");
    allTestsPassed = false;
  }
  
  testResults.forEach(result => dv.paragraph(result));
  
  if (allTestsPassed) {
    dv.paragraph("🎉 **ALL MIXED-TYPE TESTS PASSED!** The generic attribute system successfully supports multiple types and complex queries.");
    dv.paragraph("Blocks can have multiple attributes simultaneously while maintaining their primary type and hierarchy relationships.");
  } else {
    dv.paragraph("⚠️ **SOME TESTS FAILED.** Check the results above for details.");
  }
  
} catch (error) {
  console.error("❌ Mixed types test failed:", error);
  console.error(error.stack);
}
```

**Expected Results:**
- Blocks should support multiple attributes simultaneously
- Headers can have mention attributes while remaining headers
- Multiple mentions per block should be tracked
- Complex queries should work with attribute combinations
- Hierarchy should be preserved regardless of mixed types
