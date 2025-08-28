# Test: Basic Hierarchy Structure

This test covers basic indentation-based hierarchy with different block types.

```dataviewjs
// Test basic hierarchy parsing
const { noteBlocksParser } = await cJS();
const { Block, BlockCollection } = await cJS();

console.log("=== Testing Basic Hierarchy ===");

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

try {
  const parser = new noteBlocksParser();
  const collection = parser.parse("test-basic.md", testContent);
  
  console.log("📊 Parsing Results:");
  console.log("Total blocks:", collection.blocks.length);
  console.log("Block types:", collection.getStats().types);
  console.log("Root blocks:", collection.getRootBlocks().length);
  console.log("Blocks with parents:", collection.blocks.length - collection.getRootBlocks().length);
  
  console.log("\n🌳 Hierarchy Structure:");
  const hierarchy = collection.getHierarchy();
  
  function printHierarchy(nodes, indent = "") {
    nodes.forEach((node, i) => {
      const block = node.block;
      const type = block.getAttribute("type");
      const level = block.getAttribute("level") || "";
      const indentLevel = block.getAttribute("indentLevel") || 0;
      const preview = block.content.substring(0, 50).replace(/\n/g, " ");
      
      console.log(`${indent}├─ ${type}${level ? `:${level}` : ""} (indent:${indentLevel}) "${preview}"`);
      
      if (node.children.length > 0) {
        printHierarchy(node.children, indent + "│  ");
      }
    });
  }
  
  printHierarchy(hierarchy);
  
  console.log("\n🔍 Query Tests:");
  console.log("Headers:", collection.findByType("header").length);
  console.log("Todos:", collection.findByType("todo").length);
  console.log("Done items:", collection.findByType("done").length);
  console.log("Level 1 headers:", collection.findByAttribute("level", 1).length);
  console.log("Level 2 headers:", collection.findByAttribute("level", 2).length);
  console.log("Indented items (level > 0):", collection.blocks.filter(b => (b.getAttribute("indentLevel") || 0) > 0).length);
  
  console.log("\n✅ Basic hierarchy test completed successfully!");
  
} catch (error) {
  console.error("❌ Test failed:", error);
  console.error(error.stack);
}
```

**Expected Results:**
- Headers should have child elements
- Indented todos should be children of their parents
- Separator (----) should break hierarchy
- All block types should be properly identified
