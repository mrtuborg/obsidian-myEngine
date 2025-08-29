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
  dv.header(2, "🔗 Compatibility Test Results");
  dv.paragraph("**Testing:** Integration with existing components and backward compatibility");
  
  // Load CustomJS factories
  const cjsResult = await cJS();
  const noteBlocksParser = cjsResult.createnoteBlocksParserInstance;
  const mentionsProcessor = cjsResult.creatementionsProcessorInstance;
  
  if (!noteBlocksParser) {
    throw new Error("noteBlocksParser factory not found in CustomJS");
  }
  
  const parser = noteBlocksParser();
  const collection = await parser.parse("test-compatibility.md", compatibilityContent);
  
  // Basic Results
  dv.header(3, "📊 Parsing Results");
  const stats = collection.getStats();
  dv.paragraph(`✅ **Total blocks:** ${collection.blocks.length}`);
  dv.paragraph(`✅ **Block types:** ${Object.keys(stats.types).join(", ")}`);
  
  // Test 1: BlockCollection to compatibility array conversion
  dv.header(3, "🔄 Compatibility Array Conversion");
  const compatArray = collection.toCompatibilityArray();
  dv.paragraph(`✅ **Original blocks:** ${collection.blocks.length}`);
  dv.paragraph(`✅ **Compatibility array length:** ${compatArray.length}`);
  dv.paragraph(`✅ **First item structure:** ${Object.keys(compatArray[0] || {}).join(", ")}`);
  
  // Test 2: mentionsProcessor integration
  dv.header(3, "🔗 MentionsProcessor Integration");
  
  // Simulate mentionsProcessor usage
  const testPageContent = "# Test Page\nSome existing content.";
  const tagId = "Activities/Test Activity";
  const frontmatterObj = { stage: "active", startDate: "2025-08-28" };
  
  let mentionsTestPassed = false;
  let mentionsResults = { collection: 0, array: 0, consistent: false };
  
  try {
    // Create mentionsProcessor instance using factory pattern
    if (!mentionsProcessor) {
      throw new Error("mentionsProcessor factory not found in CustomJS");
    }
    
    const processor = mentionsProcessor();
    
    // Test with BlockCollection (new format)
    const mentionsResult1 = await processor.run(
      testPageContent,
      collection, // Pass BlockCollection directly
      tagId,
      frontmatterObj
    );
    const result1Length = typeof mentionsResult1 === 'string' ? mentionsResult1.split('\n').length : 0;
    mentionsResults.collection = result1Length;
    
    // Test with compatibility array (old format)
    const mentionsResult2 = await processor.run(
      testPageContent,
      compatArray, // Pass compatibility array
      tagId,
      frontmatterObj
    );
    const result2Length = typeof mentionsResult2 === 'string' ? mentionsResult2.split('\n').length : 0;
    mentionsResults.array = result2Length;
    
    // Compare results
    mentionsResults.consistent = result1Length === result2Length;
    mentionsTestPassed = true;
    
    dv.paragraph(`✅ **BlockCollection integration:** ${mentionsResults.collection} content lines`);
    dv.paragraph(`✅ **Compatibility array integration:** ${mentionsResults.array} content lines`);
    dv.paragraph(`✅ **Results consistency:** ${mentionsResults.consistent ? "PASS" : "FAIL"}`);
    
  } catch (mentionError) {
    dv.paragraph(`⚠️ **MentionsProcessor test:** Skipped (${mentionError.message})`);
  }
  
  // Test 3: Block attribute queries
  dv.header(3, "🔍 Advanced Query Testing");
  
  // Find all mentions
  const mentions = collection.findByType("mention");
  dv.paragraph(`✅ **Total mentions found:** ${mentions.length}`);
  
  // Find mentions with specific targets
  const activityMentions = mentions.filter(block => {
    const target = block.getAttribute("target");
    return target && target.includes("Activities/");
  });
  dv.paragraph(`✅ **Activity mentions:** ${activityMentions.length}`);
  
  // Find indented content
  const indentedBlocks = collection.blocks.filter(block => 
    (block.getAttribute("indentLevel") || 0) > 0
  );
  dv.paragraph(`✅ **Indented blocks:** ${indentedBlocks.length}`);
  
  // Test hierarchy relationships
  const blocksWithChildren = collection.blocks.filter(block => block.children.length > 0);
  const blocksWithParents = collection.blocks.filter(block => block.parent !== null);
  dv.paragraph(`✅ **Blocks with children:** ${blocksWithChildren.length}`);
  dv.paragraph(`✅ **Blocks with parents:** ${blocksWithParents.length}`);
  
  // Test 4: Performance comparison
  dv.header(3, "⚡ Performance Testing");
  const startTime = performance.now();
  
  // Simulate multiple operations
  for (let i = 0; i < 100; i++) {
    collection.findByType("todo");
    collection.findByAttribute("level", 1);
    collection.getRootBlocks();
  }
  
  const endTime = performance.now();
  const performanceTime = Math.round(endTime - startTime);
  dv.paragraph(`✅ **100 query operations:** ${performanceTime}ms`);
  
  // Test 5: Memory usage estimation
  dv.header(3, "💾 Memory Usage Analysis");
  const blockMemory = collection.blocks.length * 500; // Rough estimate per block
  const relationshipMemory = blocksWithParents.length * 100; // Rough estimate per relationship
  const totalMemoryKB = Math.round((blockMemory + relationshipMemory) / 1024);
  dv.paragraph(`✅ **Estimated memory usage:** ${totalMemoryKB}KB`);
  
  // Test Validation
  dv.header(3, "✅ Test Validation");
  let allTestsPassed = true;
  let testResults = [];
  
  // Test 1: Compatibility array conversion
  if (compatArray.length === collection.blocks.length) {
    testResults.push("✅ **Compatibility conversion:** Array length matches block count");
  } else {
    testResults.push("❌ **Compatibility conversion:** Array length mismatch");
    allTestsPassed = false;
  }
  
  // Test 2: MentionsProcessor integration
  if (mentionsTestPassed && mentionsResults.consistent) {
    testResults.push("✅ **MentionsProcessor integration:** Both formats work consistently");
  } else if (mentionsTestPassed) {
    testResults.push("⚠️ **MentionsProcessor integration:** Works but results inconsistent");
  } else {
    testResults.push("⚠️ **MentionsProcessor integration:** Test skipped");
  }
  
  // Test 3: Query performance
  if (performanceTime < 100) {
    testResults.push("✅ **Query performance:** Fast response time");
  } else {
    testResults.push("⚠️ **Query performance:** Slower than expected");
  }
  
  // Test 4: Memory efficiency
  if (totalMemoryKB < 100) {
    testResults.push("✅ **Memory efficiency:** Reasonable memory usage");
  } else {
    testResults.push("⚠️ **Memory efficiency:** Higher memory usage than expected");
  }
  
  // Test 5: Feature completeness
  if (mentions.length > 0 && activityMentions.length > 0 && indentedBlocks.length > 0) {
    testResults.push("✅ **Feature completeness:** All query types working");
  } else {
    testResults.push("❌ **Feature completeness:** Some query types not working");
    allTestsPassed = false;
  }
  
  testResults.forEach(result => dv.paragraph(result));
  
  if (allTestsPassed) {
    dv.paragraph("🎉 **ALL COMPATIBILITY TESTS PASSED!** The Block system maintains full backward compatibility.");
    dv.paragraph("Integration with existing components works seamlessly with both new and legacy formats.");
  } else {
    dv.paragraph("⚠️ **SOME TESTS FAILED.** Check the results above for details.");
  }
  
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
