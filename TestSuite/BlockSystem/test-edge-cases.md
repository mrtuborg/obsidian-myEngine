# Test: Edge Cases and Corner Cases

This test covers edge cases like empty lines, mixed indentation, and boundary conditions.

```dataviewjs
// Test edge cases and corner cases
const { noteBlocksParser } = await cJS();

console.log("=== Testing Edge Cases ===");

const edgeCaseContent = `# Header with immediate content
- [ ] Todo right after header
  - [ ] Nested immediately

## Header with empty lines


- [ ] Todo after empty lines (should NOT be child)

### Header with separator
----
Content after separator

#### Mixed indentation test
- [ ] Level 0
  - [ ] Level 2 spaces
    - [ ] Level 4 spaces
      - [ ] Level 6 spaces
        - [ ] Level 8 spaces
- [ ] Back to level 0

##### Empty content test
- [ ] 
  - [ ] Empty parent above

###### Callout nesting
> Callout level 0
  > Indented callout (should be child)
    > Double indented callout

####### Code block test
\`\`\`
Code at root level
\`\`\`
  \`\`\`
  Indented code block
  \`\`\`

######## Mention test
[[Root Level Link]]
  [[Indented Link]] should be child
    [[Double Indented Link]]

######### Mixed content
Text content
  Indented text
- [ ] Todo mixed with text
  Text under todo
  - [ ] Nested todo
    More text under nested todo

########## Two empty lines test
Content before


Content after two empty lines (hierarchy should break)

########### Horizontal rules test
Content before first rule
----
Content after first rule
- [ ] Todo after rule
  - [ ] Nested todo
----
Content after second rule (hierarchy broken again)`;

try {
  // Load CustomJS factories
  const cjsResult = await cJS();
  const noteBlocksParser = cjsResult.createnoteBlocksParserInstance;
  
  if (!noteBlocksParser) {
    throw new Error("noteBlocksParser factory not found in CustomJS");
  }
  
  const parser = noteBlocksParser();
  const collection = await parser.parse("test-edge-cases.md", edgeCaseContent);
  
  dv.header(2, "🧪 Edge Cases & Boundary Conditions Test");
  dv.paragraph("**Testing:** Empty lines, mixed indentation, deep nesting, and boundary conditions");
  
  // Basic Results
  dv.header(3, "📊 Parsing Results");
  const stats = collection.getStats();
  const rootBlocks = collection.getRootBlocks();
  
  dv.paragraph(`✅ **Total blocks parsed:** ${collection.blocks.length}`);
  dv.paragraph(`✅ **Block types:** ${Object.keys(stats.types).join(", ")}`);
  dv.paragraph(`✅ **Root blocks:** ${rootBlocks.length}`);
  
  // Specific Edge Case Tests
  dv.header(3, "🔍 Edge Case Analysis");
  
  // Test 1: Immediate content after header
  const immediateChildren = collection.blocks.filter(b => 
    b.getAttribute("type") === "header" && 
    b.content.includes("immediate content") &&
    b.children.length > 0
  );
  dv.paragraph(`✅ **Headers with immediate children:** ${immediateChildren.length}`);
  
  // Test 2: Content after empty lines should not be children
  const headersWithEmptyLines = collection.blocks.filter(b => 
    b.getAttribute("type") === "header" && 
    b.content.includes("empty lines")
  );
  const emptyLineChildCount = headersWithEmptyLines.length > 0 ? headersWithEmptyLines[0].children.length : 0;
  dv.paragraph(`✅ **Empty line handling:** Header after empty lines has ${emptyLineChildCount} children`);
  
  // Test 3: Deep nesting levels
  const deeplyNested = collection.blocks.filter(b => 
    (b.getAttribute("indentLevel") || 0) >= 8
  );
  dv.paragraph(`✅ **Deep nesting:** ${deeplyNested.length} blocks at 8+ indent levels`);
  
  // Test 4: Mixed content types
  const textBlocks = collection.findByType("text");
  dv.paragraph(`✅ **Text blocks found:** ${textBlocks.length}`);
  
  // Boundary Condition Tests
  dv.header(3, "🧪 Boundary Condition Results");
  
  // Test empty content
  const emptyBlocks = collection.blocks.filter(b => !b.content || b.content.trim() === "");
  dv.paragraph(`✅ **Empty blocks handled:** ${emptyBlocks.length}`);
  
  // Test maximum indentation
  const maxIndent = Math.max(...collection.blocks.map(b => b.getAttribute("indentLevel") || 0));
  dv.paragraph(`✅ **Maximum indentation level:** ${maxIndent}`);
  
  // Test parent-child consistency
  let consistencyErrors = 0;
  collection.blocks.forEach(block => {
    block.children.forEach(child => {
      if (child.parent !== block) {
        consistencyErrors++;
      }
    });
  });
  dv.paragraph(`✅ **Parent-child consistency errors:** ${consistencyErrors}`);
  
  // Hierarchy Sample
  dv.header(3, "🌳 Hierarchy Structure Sample");
  const hierarchy = collection.getHierarchy();
  
  let hierarchyText = "";
  function buildLimitedHierarchy(nodes, indent = "", maxDepth = 3, currentDepth = 0) {
    if (currentDepth >= maxDepth) return;
    
    nodes.slice(0, 3).forEach((node, i) => {
      const block = node.block;
      const type = block.getAttribute("type");
      const level = block.getAttribute("level") || "";
      const indentLevel = block.getAttribute("indentLevel") || 0;
      const preview = block.content.substring(0, 35).replace(/\n/g, " ");
      
      hierarchyText += `${indent}├─ **${type}${level ? `:${level}` : ""}** (i:${indentLevel}) "${preview}"\n`;
      
      if (node.children.length > 0 && currentDepth < maxDepth - 1) {
        buildLimitedHierarchy(node.children, indent + "│  ", maxDepth, currentDepth + 1);
      }
    });
  }
  
  buildLimitedHierarchy(hierarchy);
  dv.paragraph("```\n" + hierarchyText + "```");
  
  // Test Validation
  dv.header(3, "✅ Test Validation");
  let allTestsPassed = true;
  let testResults = [];
  
  // Test 1: Should handle immediate content correctly
  if (immediateChildren.length > 0) {
    testResults.push("✅ **Immediate content:** Headers with immediate children handled correctly");
  } else {
    testResults.push("❌ **Immediate content:** No headers with immediate children found");
    allTestsPassed = false;
  }
  
  // Test 2: Should respect empty line breaks
  if (emptyLineChildCount === 0) {
    testResults.push("✅ **Empty line breaks:** Content after empty lines correctly not children");
  } else {
    testResults.push("❌ **Empty line breaks:** Content after empty lines incorrectly became children");
    allTestsPassed = false;
  }
  
  // Test 3: Should handle deep nesting
  if (deeplyNested.length > 0) {
    testResults.push("✅ **Deep nesting:** 8+ level indentation handled successfully");
  } else {
    testResults.push("❌ **Deep nesting:** Deep indentation not working");
    allTestsPassed = false;
  }
  
  // Test 4: Should maintain consistency
  if (consistencyErrors === 0) {
    testResults.push("✅ **Consistency:** All parent-child relationships are consistent");
  } else {
    testResults.push(`❌ **Consistency:** ${consistencyErrors} parent-child relationship errors`);
    allTestsPassed = false;
  }
  
  // Test 5: Should handle multiple root blocks (separators)
  if (rootBlocks.length >= 3) {
    testResults.push("✅ **Hierarchy breaks:** Multiple root blocks from separators");
  } else {
    testResults.push("❌ **Hierarchy breaks:** Insufficient hierarchy breaking");
    allTestsPassed = false;
  }
  
  testResults.forEach(result => dv.paragraph(result));
  
  if (allTestsPassed) {
    dv.paragraph("🎉 **ALL EDGE CASE TESTS PASSED!** The system handles boundary conditions robustly.");
    dv.paragraph("Empty lines, deep nesting, mixed indentation, and hierarchy breaks all work correctly.");
  } else {
    dv.paragraph("⚠️ **SOME EDGE CASE TESTS FAILED.** Check the results above for details.");
  }
  
} catch (error) {
  console.error("❌ Edge cases test failed:", error);
  console.error(error.stack);
}
```

**Expected Results:**
- Content immediately after headers should be children
- Content after 2+ empty lines should NOT be children
- Deep nesting (8+ levels) should work correctly
- Horizontal rules should break hierarchy
- Parent-child relationships should be consistent
