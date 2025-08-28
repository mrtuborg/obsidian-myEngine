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
  const parser = new noteBlocksParser();
  const collection = parser.parse("test-edge-cases.md", edgeCaseContent);
  
  console.log("📊 Edge Case Results:");
  console.log("Total blocks:", collection.blocks.length);
  console.log("Block types:", collection.getStats().types);
  console.log("Root blocks:", collection.getRootBlocks().length);
  
  console.log("\n🔍 Specific Edge Case Tests:");
  
  // Test 1: Immediate content after header
  const immediateChildren = collection.blocks.filter(b => 
    b.getAttribute("type") === "header" && 
    b.content.includes("immediate content") &&
    b.children.length > 0
  );
  console.log("✓ Headers with immediate children:", immediateChildren.length);
  
  // Test 2: Content after empty lines should not be children
  const headersWithEmptyLines = collection.blocks.filter(b => 
    b.getAttribute("type") === "header" && 
    b.content.includes("empty lines")
  );
  if (headersWithEmptyLines.length > 0) {
    console.log("✓ Header with empty lines children count:", headersWithEmptyLines[0].children.length);
  }
  
  // Test 3: Deep nesting levels
  const deeplyNested = collection.blocks.filter(b => 
    (b.getAttribute("indentLevel") || 0) >= 8
  );
  console.log("✓ Deeply nested blocks (8+ spaces):", deeplyNested.length);
  
  // Test 4: Mixed content types
  const textBlocks = collection.findByType("text");
  console.log("✓ Text blocks found:", textBlocks.length);
  
  // Test 5: Hierarchy breaks
  const rootBlocks = collection.getRootBlocks();
  console.log("✓ Root blocks (hierarchy breaks):", rootBlocks.length);
  
  console.log("\n🌳 Detailed Hierarchy (first 10 levels):");
  const hierarchy = collection.getHierarchy();
  
  function printLimitedHierarchy(nodes, indent = "", maxDepth = 3, currentDepth = 0) {
    if (currentDepth >= maxDepth) return;
    
    nodes.slice(0, 5).forEach((node, i) => { // Limit to first 5 nodes per level
      const block = node.block;
      const type = block.getAttribute("type");
      const level = block.getAttribute("level") || "";
      const indentLevel = block.getAttribute("indentLevel") || 0;
      const preview = block.content.substring(0, 40).replace(/\n/g, " ");
      
      console.log(`${indent}├─ ${type}${level ? `:${level}` : ""} (i:${indentLevel}) "${preview}"`);
      
      if (node.children.length > 0 && currentDepth < maxDepth - 1) {
        printLimitedHierarchy(node.children, indent + "│  ", maxDepth, currentDepth + 1);
      }
    });
  }
  
  printLimitedHierarchy(hierarchy);
  
  console.log("\n🧪 Boundary Condition Tests:");
  
  // Test empty content
  const emptyBlocks = collection.blocks.filter(b => !b.content || b.content.trim() === "");
  console.log("Empty blocks:", emptyBlocks.length);
  
  // Test maximum indentation
  const maxIndent = Math.max(...collection.blocks.map(b => b.getAttribute("indentLevel") || 0));
  console.log("Maximum indentation level:", maxIndent);
  
  // Test parent-child consistency
  let consistencyErrors = 0;
  collection.blocks.forEach(block => {
    block.children.forEach(child => {
      if (child.parent !== block) {
        consistencyErrors++;
      }
    });
  });
  console.log("Parent-child consistency errors:", consistencyErrors);
  
  console.log("\n✅ Edge cases test completed!");
  
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
