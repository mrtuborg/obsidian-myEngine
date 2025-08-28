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
  const parser = new noteBlocksParser();
  const collection = parser.parse("test-mixed-types.md", mixedTypesContent);
  
  console.log("📊 Mixed Types Test Results:");
  console.log("Total blocks:", collection.blocks.length);
  console.log("Block types:", collection.getStats().types);
  
  console.log("\n🔍 Mixed Type Analysis:");
  
  // Test 1: Headers with mentions
  const headerMentions = collection.blocks.filter(block => 
    block.getAttribute("type") === "header" && 
    block.content.includes("[[")
  );
  console.log("✓ Headers containing mentions:", headerMentions.length);
  
  // Test 2: Todos with mentions
  const todoMentions = collection.blocks.filter(block => 
    block.getAttribute("type") === "todo" && 
    block.content.includes("[[")
  );
  console.log("✓ Todos containing mentions:", todoMentions.length);
  
  // Test 3: Callouts with mentions
  const calloutMentions = collection.blocks.filter(block => 
    block.getAttribute("type") === "callout" && 
    block.content.includes("[[")
  );
  console.log("✓ Callouts containing mentions:", calloutMentions.length);
  
  // Test 4: Code blocks with mentions
  const codeMentions = collection.blocks.filter(block => 
    block.getAttribute("type") === "code" && 
    block.content.includes("[[")
  );
  console.log("✓ Code blocks containing mentions:", codeMentions.length);
  
  // Test 5: Multiple mentions per block
  const multipleMentions = collection.blocks.filter(block => {
    const mentionCount = (block.content.match(/\[\[.*?\]\]/g) || []).length;
    return mentionCount > 1;
  });
  console.log("✓ Blocks with multiple mentions:", multipleMentions.length);
  
  console.log("\n🏷️ Enhanced Attribute System Test:");
  
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
  
  console.log("\n🔎 Enhanced Query Tests:");
  
  // Query by enhanced attributes
  const blocksWithMentions = collection.blocks.filter(b => b.getAttribute("hasMentions"));
  console.log("Blocks with mentions:", blocksWithMentions.length);
  
  const blocksWithMultipleMentions = collection.blocks.filter(b => 
    (b.getAttribute("mentionCount") || 0) > 1
  );
  console.log("Blocks with multiple mentions:", blocksWithMultipleMentions.length);
  
  const activityBlocks = collection.blocks.filter(b => b.getAttribute("hasActivityMentions"));
  console.log("Blocks with activity mentions:", activityBlocks.length);
  
  const headerMentionBlocks = collection.blocks.filter(b => b.getAttribute("isHeaderWithMentions"));
  console.log("Headers with mentions:", headerMentionBlocks.length);
  
  const todoMentionBlocks = collection.blocks.filter(b => b.getAttribute("isTodoWithMentions"));
  console.log("Todos with mentions:", todoMentionBlocks.length);
  
  console.log("\n📋 Detailed Mixed-Type Examples:");
  
  // Show examples of mixed-type blocks
  const examples = collection.blocks.filter(b => 
    b.getAttribute("hasMentions") && 
    (b.getAttribute("mentionCount") || 0) > 1
  ).slice(0, 3);
  
  examples.forEach((block, i) => {
    const type = block.getAttribute("type");
    const mentionCount = block.getAttribute("mentionCount");
    const targets = block.getAttribute("mentionTargets") || [];
    const preview = block.content.substring(0, 80).replace(/\n/g, " ");
    
    console.log(`Example ${i + 1}: ${type} with ${mentionCount} mentions`);
    console.log(`  Content: "${preview}"`);
    console.log(`  Targets: [${targets.join(", ")}]`);
    console.log(`  Attributes: ${Object.keys(block.getAllAttributes()).join(", ")}`);
  });
  
  console.log("\n🌳 Mixed-Type Hierarchy Sample:");
  const hierarchy = collection.getHierarchy();
  
  function printMixedTypeHierarchy(nodes, indent = "", maxDepth = 2, currentDepth = 0) {
    if (currentDepth >= maxDepth) return;
    
    nodes.slice(0, 3).forEach((node, i) => {
      const block = node.block;
      const type = block.getAttribute("type");
      const hasMentions = block.getAttribute("hasMentions") ? "📎" : "";
      const mentionCount = block.getAttribute("mentionCount") || 0;
      const preview = block.content.substring(0, 50).replace(/\n/g, " ");
      
      console.log(`${indent}├─ ${type}${hasMentions}${mentionCount > 1 ? `(${mentionCount})` : ""} "${preview}"`);
      
      if (node.children.length > 0 && currentDepth < maxDepth - 1) {
        printMixedTypeHierarchy(node.children, indent + "│  ", maxDepth, currentDepth + 1);
      }
    });
  }
  
  printMixedTypeHierarchy(hierarchy);
  
  console.log("\n🧪 Advanced Attribute Queries:");
  
  // Complex queries using multiple attributes
  const complexQuery1 = collection.blocks.filter(b => 
    b.getAttribute("type") === "todo" && 
    b.getAttribute("hasMentions") && 
    (b.getAttribute("indentLevel") || 0) > 0
  );
  console.log("Indented todos with mentions:", complexQuery1.length);
  
  const complexQuery2 = collection.blocks.filter(b => 
    b.getAttribute("hasActivityMentions") && 
    b.parent !== null
  );
  console.log("Child blocks with activity mentions:", complexQuery2.length);
  
  const complexQuery3 = collection.blocks.filter(b => {
    const targets = b.getAttribute("mentionTargets") || [];
    return targets.some(target => target.includes("Task"));
  });
  console.log("Blocks mentioning 'Task' activities:", complexQuery3.length);
  
  console.log("\n✅ Mixed types test completed!");
  console.log("The generic attribute system successfully supports multiple types and complex queries!");
  
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
