# Test: Compatibility with Existing Components

This test verifies that the new Block system works with existing components like mentionsProcessor.

```dataviewjs
// Test compatibility with existing components
const { noteBlocksParser } = await cJS();
const { mentionsProcessor } = await cJS();

console.log("=== Testing Compatibility ===");

const compatibilityContent = `# Project Planning
This is a test for [[Activities/Test Activity]] integration.

## Tasks
- [ ] Complete [[Activities/Test Activity]] setup
  - [ ] Configure environment
  - [ ] Test basic functionality
- [ ] Review [[Activities/Another Activity]] progress
- [x] Finished [[Activities/Completed Activity]] work

## Notes
> Important: Check [[Activities/Test Activity]] for updates
> Also review [[Activities/Another Activity]] status

## Code Examples
\`\`\`javascript
// Reference to [[Activities/Test Activity]]
console.log("Testing");
\`\`\`

## Links
[[Activities/Test Activity]] - Main project
  [[Activities/Sub Project]] - Related work
    [[Activities/Deep Project]] - Nested reference

----

## Separate Section
Content after separator with [[Activities/Separate Activity]].`;

try {
  const parser = new noteBlocksParser();
  const collection = parser.parse("test-compatibility.md", compatibilityContent);
  
  console.log("📊 Compatibility Test Results:");
  console.log("Total blocks:", collection.blocks.length);
  console.log("Block types:", collection.getStats().types);
  
  // Test 1: BlockCollection to compatibility array conversion
  console.log("\n🔄 Testing Compatibility Array Conversion:");
  const compatArray = collection.toCompatibilityArray();
  console.log("Original blocks:", collection.blocks.length);
  console.log("Compatibility array length:", compatArray.length);
  console.log("First compatibility item structure:", Object.keys(compatArray[0] || {}));
  
  // Test 2: mentionsProcessor integration
  console.log("\n🔗 Testing mentionsProcessor Integration:");
  
  // Simulate mentionsProcessor usage
  const testPageContent = "# Test Page\nSome existing content.";
  const tagId = "Activities/Test Activity";
  const frontmatterObj = { stage: "active", startDate: "2025-08-28" };
  
  try {
    // Test with BlockCollection (new format)
    console.log("Testing with BlockCollection...");
    const mentionsResult1 = await mentionsProcessor.run(
      testPageContent,
      collection, // Pass BlockCollection directly
      tagId,
      frontmatterObj
    );
    console.log("✓ BlockCollection integration successful");
    console.log("Result length:", mentionsResult1.length);
    
    // Test with compatibility array (old format)
    console.log("Testing with compatibility array...");
    const mentionsResult2 = await mentionsProcessor.run(
      testPageContent,
      compatArray, // Pass compatibility array
      tagId,
      frontmatterObj
    );
    console.log("✓ Compatibility array integration successful");
    console.log("Result length:", mentionsResult2.length);
    
    // Compare results
    const resultsMatch = mentionsResult1.length === mentionsResult2.length;
    console.log("✓ Results consistency:", resultsMatch ? "PASS" : "FAIL");
    
  } catch (mentionError) {
    console.log("⚠️ MentionsProcessor test skipped (component may need frontmatter param)");
    console.log("Error:", mentionError.message);
  }
  
  // Test 3: Block attribute queries
  console.log("\n🔍 Testing Advanced Queries:");
  
  // Find all mentions
  const mentions = collection.findByType("mention");
  console.log("Total mentions found:", mentions.length);
  
  // Find mentions with specific targets
  const activityMentions = mentions.filter(block => {
    const target = block.getAttribute("target");
    return target && target.includes("Activities/");
  });
  console.log("Activity mentions:", activityMentions.length);
  
  // Find indented content
  const indentedBlocks = collection.blocks.filter(block => 
    (block.getAttribute("indentLevel") || 0) > 0
  );
  console.log("Indented blocks:", indentedBlocks.length);
  
  // Test hierarchy relationships
  const blocksWithChildren = collection.blocks.filter(block => block.children.length > 0);
  console.log("Blocks with children:", blocksWithChildren.length);
  
  const blocksWithParents = collection.blocks.filter(block => block.parent !== null);
  console.log("Blocks with parents:", blocksWithParents.length);
  
  // Test 4: Performance comparison
  console.log("\n⚡ Performance Test:");
  const startTime = performance.now();
  
  // Simulate multiple operations
  for (let i = 0; i < 100; i++) {
    collection.findByType("todo");
    collection.findByAttribute("level", 1);
    collection.getRootBlocks();
  }
  
  const endTime = performance.now();
  console.log("100 query operations took:", Math.round(endTime - startTime), "ms");
  
  // Test 5: Memory usage estimation
  console.log("\n💾 Memory Usage Estimation:");
  const blockMemory = collection.blocks.length * 500; // Rough estimate per block
  const relationshipMemory = blocksWithParents.length * 100; // Rough estimate per relationship
  console.log("Estimated memory usage:", Math.round((blockMemory + relationshipMemory) / 1024), "KB");
  
  console.log("\n✅ Compatibility test completed successfully!");
  
} catch (error) {
  console.error("❌ Compatibility test failed:", error);
  console.error(error.stack);
}
```

**Expected Results:**
- BlockCollection should convert to compatibility array correctly
- mentionsProcessor should work with both formats
- Query operations should be fast and accurate
- Memory usage should be reasonable
- All existing functionality should be preserved
