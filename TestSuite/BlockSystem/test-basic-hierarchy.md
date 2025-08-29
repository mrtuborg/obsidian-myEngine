# Test: Basic Hierarchy Structure

This test covers basic indentation-based hierarchy with different block types.

```dataviewjs
try {
  dv.header(2, "🧪 Basic Hierarchy Test");
  dv.paragraph("**Testing:** Indentation-based hierarchy with different block types");
  
  const testContent = `# Main Header
This is some text under the header.

## Sub Header
- [ ] Todo item 1
  - [ ] Nested todo 1.1
  - [ ] Nested todo 1.2
    - [ ] Deep nested 1.2.1
- [ ] Todo item 2
- [x] Completed todo

> This is a callout
> Multi-line callout

\`\`\`javascript
console.log("Code block");
\`\`\`

[[Some Link]] with mention

### Another Header
More content here.

----

Content after separator (should break hierarchy).`;

  // Load CustomJS factories
  const cjsResult = await cJS();
  const noteBlocksParser = cjsResult.createnoteBlocksParserInstance;
  
  if (!noteBlocksParser) {
    throw new Error("noteBlocksParser factory not found in CustomJS");
  }
  
  const parser = noteBlocksParser();
  const collection = await parser.parse("test-basic.md", testContent);
  
  // Test Results
  dv.header(3, "📊 Parsing Results");
  const stats = collection.getStats();
  const rootBlocks = collection.getRootBlocks().length;
  const blocksWithParents = collection.blocks.length - rootBlocks;
  
  dv.paragraph(`✅ **Total blocks parsed:** ${collection.blocks.length}`);
  dv.paragraph(`✅ **Block types found:** ${Object.keys(stats.types).join(", ")}`);
  dv.paragraph(`✅ **Root blocks:** ${rootBlocks}`);
  dv.paragraph(`✅ **Child blocks:** ${blocksWithParents}`);
  
  // Debug: Show what the root blocks actually are
  const actualRootBlocks = collection.getRootBlocks();
  dv.paragraph("**Debug - Root blocks:**");
  actualRootBlocks.forEach((block, i) => {
    const type = block.getAttribute("type");
    const preview = block.content.substring(0, 30).replace(/\n/g, " ");
    dv.paragraph(`${i + 1}. **${type}**: "${preview}"`);
  });
  
  // Hierarchy Structure
  dv.header(3, "🌳 Hierarchy Structure");
  const hierarchy = collection.getHierarchy();
  
  let hierarchyText = "";
  function buildHierarchyText(nodes, indent = "") {
    nodes.forEach((node, i) => {
      const block = node.block;
      const type = block.getAttribute("type");
      const level = block.getAttribute("level") || "";
      const indentLevel = block.getAttribute("indentLevel") || 0;
      const preview = block.content.substring(0, 40).replace(/\n/g, " ");
      
      hierarchyText += `${indent}├─ **${type}${level ? `:${level}` : ""}** (indent:${indentLevel}) "${preview}"\n`;
      
      if (node.children.length > 0) {
        buildHierarchyText(node.children, indent + "│  ");
      }
    });
  }
  
  buildHierarchyText(hierarchy);
  dv.paragraph("```\n" + hierarchyText + "```");
  
  // Query Tests
  dv.header(3, "🔍 Query Test Results");
  const headers = collection.findByType("header").length;
  const todos = collection.findByType("todo").length;
  const done = collection.findByType("done").length;
  const level1Headers = collection.findByAttribute("level", 1).length;
  const level2Headers = collection.findByAttribute("level", 2).length;
  const indentedItems = collection.blocks.filter(b => (b.getAttribute("indentLevel") || 0) > 0).length;
  
  dv.paragraph(`✅ **Headers found:** ${headers}`);
  dv.paragraph(`✅ **Todo items:** ${todos}`);
  dv.paragraph(`✅ **Completed items:** ${done}`);
  dv.paragraph(`✅ **Level 1 headers:** ${level1Headers}`);
  dv.paragraph(`✅ **Level 2 headers:** ${level2Headers}`);
  dv.paragraph(`✅ **Indented items:** ${indentedItems}`);
  
  // Test Validation
  dv.header(3, "✅ Test Validation");
  let allTestsPassed = true;
  let testResults = [];
  
  // Test 1: Should have parsed multiple blocks
  if (collection.blocks.length >= 10) {
    testResults.push("✅ **Block parsing:** Multiple blocks parsed successfully");
  } else {
    testResults.push("❌ **Block parsing:** Too few blocks parsed");
    allTestsPassed = false;
  }
  
  // Test 2: Should have hierarchy
  if (blocksWithParents > 0) {
    testResults.push("✅ **Hierarchy:** Parent-child relationships established");
  } else {
    testResults.push("❌ **Hierarchy:** No parent-child relationships found");
    allTestsPassed = false;
  }
  
  // Test 3: Should recognize different types
  if (Object.keys(stats.types).length >= 5) {
    testResults.push("✅ **Block types:** Multiple content types recognized");
  } else {
    testResults.push("❌ **Block types:** Insufficient content type recognition");
    allTestsPassed = false;
  }
  
  // Test 4: Should handle separator breaks
  // The test content should have: Main Header (root), separator (root), content after separator (root)
  // Plus potentially Sub Header and Another Header as roots if hierarchy is properly broken
  if (rootBlocks >= 3) {
    testResults.push("✅ **Separator handling:** Hierarchy breaks working correctly");
  } else {
    testResults.push(`❌ **Separator handling:** Expected ≥3 root blocks, got ${rootBlocks}`);
    allTestsPassed = false;
  }
  
  testResults.forEach(result => dv.paragraph(result));
  
  if (allTestsPassed) {
    dv.paragraph("🎉 **ALL TESTS PASSED!** Basic hierarchy system is working correctly.");
  } else {
    dv.paragraph("⚠️ **SOME TESTS FAILED.** Check the results above for details.");
  }
  
} catch (error) {
  dv.paragraph(`❌ **Test Error:** ${error.message}`);
  console.error("Basic hierarchy test failed:", error);
}
```

**Expected Results:**
- Headers should have child elements
- Indented todos should be children of their parents
- Separator (----) should break hierarchy
- All block types should be properly identified
