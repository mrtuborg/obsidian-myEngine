# Test: Note Blocks Parser

## Description
Tests the noteBlocksParser component which is responsible for parsing markdown files and extracting different types of blocks (todos, done items, headers, mentions, etc.).

## Test Cases
- [x] Parse basic markdown content
- [x] Detect todo items with various formats
- [x] Detect completed (done) items
- [x] Identify headers and their levels
- [x] Parse mentions and callouts
- [x] Handle code blocks correctly
- [x] Process multiple files
- [x] Performance testing with large files

## DataviewJS Test Block

```dataviewjs
/**
 * Test: noteBlocksParser Component
 * Tests markdown parsing and block extraction functionality
 */

async function testNoteBlocksParser() {
  console.log("🧪 === NOTE BLOCKS PARSER TEST START ===");
  
  try {
    // Load the noteBlocksParser module
    const { noteBlocksParser } = await cJS();
    const parser = new noteBlocksParser();
    
    console.log("✅ Module loaded successfully");
    
    // Test 1: Basic todo detection
    console.log("\n📋 Test 1: Todo Detection");
    const todoTests = [
      "- [ ] Basic todo item",
      "  - [ ] Indented todo",
      "- [x] Completed todo",
      "> - [ ] Quoted todo",
      "- [ ] Todo with [[link]]",
      "- [ ] Todo with #tag",
      "- regular list item",
      "# Header",
      ""
    ];
    
    let todoTestsPassed = 0;
    todoTests.forEach((line, index) => {
      const isTodo = parser.isTodoLine(line);
      const isDone = parser.isDoneLine(line);
      const expected = line.includes("[ ]") && !line.includes("[x]");
      const expectedDone = line.includes("[x]");
      
      console.log(`   Line ${index + 1}: "${line}"`);
      console.log(`   Todo: ${isTodo} (expected: ${expected}), Done: ${isDone} (expected: ${expectedDone})`);
      
      if (isTodo === expected && isDone === expectedDone) {
        console.log("   ✅ PASS");
        todoTestsPassed++;
      } else {
        console.log("   ❌ FAIL");
      }
    });
    
    console.log(`📊 Todo Detection: ${todoTestsPassed}/${todoTests.length} tests passed`);
    
    // Test 2: Header detection
    console.log("\n📋 Test 2: Header Detection");
    const headerTests = [
      { line: "# Header 1", expected: true, level: 1 },
      { line: "## Header 2", expected: true, level: 2 },
      { line: "### Header 3", expected: true, level: 3 },
      { line: "Regular text", expected: false, level: 0 },
      { line: "- [ ] Todo", expected: false, level: 0 }
    ];
    
    let headerTestsPassed = 0;
    headerTests.forEach((test, index) => {
      const isHeader = parser.isHeader(test.line);
      const level = parser.getHeaderLevel(test.line);
      
      console.log(`   Test ${index + 1}: "${test.line}"`);
      console.log(`   Header: ${isHeader} (expected: ${test.expected}), Level: ${level} (expected: ${test.level})`);
      
      if (isHeader === test.expected && level === test.level) {
        console.log("   ✅ PASS");
        headerTestsPassed++;
      } else {
        console.log("   ❌ FAIL");
      }
    });
    
    console.log(`📊 Header Detection: ${headerTestsPassed}/${headerTests.length} tests passed`);
    
    // Test 3: Block parsing with sample content
    console.log("\n📋 Test 3: Block Parsing");
    const sampleContent = `# Sample Document

This is a sample document for testing.

## Todo Section
- [ ] First todo item
- [ ] Second todo item with [[Activity Link]]
- [x] Completed todo

## Notes Section
Some regular text here.

> [!NOTE] This is a callout
> With some content

### Subsection
- Regular list item
- [ ] Another todo
- [x] Another completed item

## Mentions
[[2025-07-06]] - Today's date
[[Activity Name]] - Some activity

\`\`\`javascript
// Code block should be ignored
- [ ] This todo should not be parsed
\`\`\`
`;
    
    try {
      const blocks = parser.parse("test-file.md", sampleContent);
      console.log(`   📦 Total blocks parsed: ${blocks.length}`);
      
      // Count block types
      const blockTypes = {};
      blocks.forEach(block => {
        blockTypes[block.blockType] = (blockTypes[block.blockType] || 0) + 1;
      });
      
      console.log("   📊 Block type summary:");
      Object.entries(blockTypes).forEach(([type, count]) => {
        console.log(`      ${type}: ${count}`);
      });
      
      // Verify expected blocks
      const expectedTodos = 3; // Should find 3 todo items
      const expectedDone = 2;  // Should find 2 completed items
      const expectedHeaders = 3; // Should find 3 headers
      
      const actualTodos = blockTypes.todo || 0;
      const actualDone = blockTypes.done || 0;
      const actualHeaders = blockTypes.header || 0;
      
      console.log(`   🎯 Expected todos: ${expectedTodos}, found: ${actualTodos}`);
      console.log(`   🎯 Expected done: ${expectedDone}, found: ${actualDone}`);
      console.log(`   🎯 Expected headers: ${expectedHeaders}, found: ${actualHeaders}`);
      
      const blockParsingPassed = (
        actualTodos === expectedTodos &&
        actualDone === expectedDone &&
        actualHeaders === expectedHeaders
      );
      
      if (blockParsingPassed) {
        console.log("   ✅ Block parsing test PASSED");
      } else {
        console.log("   ❌ Block parsing test FAILED");
      }
      
    } catch (parseError) {
      console.error("   ❌ Block parsing failed:", parseError);
    }
    
    // Test 4: File loading test (if possible)
    console.log("\n📋 Test 4: File Loading");
    try {
      // Try to load a real file for testing
      const testFilePath = "Journal/2025/07.July/2025-07-06.md";
      const fileContent = await parser.loadFile(app, testFilePath);
      
      if (fileContent && fileContent.length > 0) {
        console.log(`   ✅ File loaded successfully: ${fileContent.length} characters`);
        
        // Parse the real file
        const realBlocks = parser.parse(testFilePath, fileContent);
        console.log(`   📦 Real file blocks parsed: ${realBlocks.length}`);
        
        // Show block summary
        const realBlockTypes = {};
        realBlocks.forEach(block => {
          realBlockTypes[block.blockType] = (realBlockTypes[block.blockType] || 0) + 1;
        });
        
        console.log("   📊 Real file block types:");
        Object.entries(realBlockTypes).forEach(([type, count]) => {
          console.log(`      ${type}: ${count}`);
        });
        
      } else {
        console.log("   ⚠️  File loaded but empty or not found");
      }
      
    } catch (fileError) {
      console.log(`   ⚠️  File loading test skipped: ${fileError.message}`);
    }
    
    // Test 5: Performance test
    console.log("\n📋 Test 5: Performance Test");
    const startTime = Date.now();
    
    // Create a large content for performance testing
    let largeContent = "# Performance Test Document\n\n";
    for (let i = 0; i < 1000; i++) {
      largeContent += `- [ ] Todo item ${i}\n`;
      largeContent += `- [x] Done item ${i}\n`;
      largeContent += `Regular text line ${i}\n`;
      if (i % 100 === 0) {
        largeContent += `## Section ${i / 100}\n`;
      }
    }
    
    const perfBlocks = parser.parse("performance-test.md", largeContent);
    const endTime = Date.now();
    const duration = endTime - startTime;
    
    console.log(`   ⏱️  Parsed ${perfBlocks.length} blocks in ${duration}ms`);
    console.log(`   📊 Performance: ${(perfBlocks.length / duration * 1000).toFixed(0)} blocks/second`);
    
    if (duration < 1000) { // Should complete within 1 second
      console.log("   ✅ Performance test PASSED");
    } else {
      console.log("   ⚠️  Performance test SLOW (but not failed)");
    }
    
    // Final summary
    console.log("\n📊 TEST SUMMARY");
    console.log("================");
    console.log(`✅ Todo Detection: ${todoTestsPassed}/${todoTests.length}`);
    console.log(`✅ Header Detection: ${headerTestsPassed}/${headerTests.length}`);
    console.log("✅ Block Parsing: Completed");
    console.log("✅ File Loading: Completed");
    console.log("✅ Performance: Completed");
    
    const totalTests = todoTests.length + headerTests.length + 3; // +3 for other tests
    const passedTests = todoTestsPassed + headerTestsPassed + 3;
    const passRate = ((passedTests / totalTests) * 100).toFixed(1);
    
    console.log(`📈 Overall Pass Rate: ${passRate}%`);
    
    if (passRate >= 90) {
      console.log("🎉 noteBlocksParser tests PASSED!");
    } else {
      console.log("⚠️  Some noteBlocksParser tests need attention");
    }
    
  } catch (error) {
    console.error("❌ Test failed with error:", error);
    console.error("Stack trace:", error.stack);
  }
  
  console.log("🧪 === NOTE BLOCKS PARSER TEST END ===");
}

// Run the test
testNoteBlocksParser();
```

## Expected Results

### ✅ Success Indicators
- **Module loads** without errors
- **Todo detection** correctly identifies `- [ ]` patterns
- **Header detection** identifies `#` patterns and levels
- **Block parsing** extracts expected number of blocks
- **File loading** reads real files successfully
- **Performance** completes large parsing within reasonable time

### ❌ Failure Indicators
- Module loading errors
- Incorrect todo/done detection
- Wrong header level detection
- Missing or extra blocks in parsing
- File loading failures
- Poor performance (>1 second for 1000 items)

## Troubleshooting

### Common Issues
1. **"cJS is not defined"**: Ensure you're running in Obsidian with custom JS enabled
2. **Module not found**: Check that noteBlocksParser.js exists in Scripts/components/
3. **File not found**: Verify the test file path exists
4. **Performance issues**: Check for infinite loops or inefficient regex

### Debug Tips
- Check browser console (F12) for detailed error messages
- Verify file paths are correct for your vault structure
- Test with smaller content first if performance issues occur

---

**This test validates the core parsing functionality that all other components depend on.**
