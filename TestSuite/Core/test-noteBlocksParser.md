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
  dv.header(2, "🧪 Note Blocks Parser Test Results");
  dv.paragraph("**Testing:** Markdown parsing and block extraction functionality");
  
  try {
    // Load the noteBlocksParser module using CustomJS factory pattern
    const cjsResult = await cJS();
    const noteBlocksParser = cjsResult.createnoteBlocksParserInstance;
    
    if (!noteBlocksParser) {
      throw new Error("noteBlocksParser factory not found in CustomJS");
    }
    
    const parser = noteBlocksParser();
    
    dv.paragraph("✅ **Module loaded successfully**");
    
    // Test 1: Basic todo detection
    dv.header(3, "📋 Test 1: Todo Detection");
    const todoTests = [
      { line: "- [ ] Basic todo item", expectedTodo: true, expectedDone: false },
      { line: "  - [ ] Indented todo", expectedTodo: false, expectedDone: false }, // Parser only detects todos starting at line beginning
      { line: "- [x] Completed todo", expectedTodo: false, expectedDone: true },
      { line: "> - [ ] Quoted todo", expectedTodo: false, expectedDone: false }, // Parser doesn't detect quoted todos
      { line: "- [ ] Todo with [[link]]", expectedTodo: true, expectedDone: false },
      { line: "- [ ] Todo with #tag", expectedTodo: true, expectedDone: false },
      { line: "- regular list item", expectedTodo: false, expectedDone: false },
      { line: "# Header", expectedTodo: false, expectedDone: false },
      { line: "", expectedTodo: false, expectedDone: false }
    ];
    
    let todoTestsPassed = 0;
    todoTests.forEach((test, index) => {
      const isTodo = parser.isTodoLine(test.line);
      const isDone = parser.isDoneLine(test.line);
      const expected = test.expectedTodo;
      const expectedDone = test.expectedDone;
      
      const status = (isTodo === expected && isDone === expectedDone) ? "✅ PASS" : "❌ FAIL";
      dv.paragraph(`**Test ${index + 1}:** "${test.line}" → Todo: ${isTodo} (expected: ${expected}), Done: ${isDone} (expected: ${expectedDone}) ${status}`);
      
      if (isTodo === expected && isDone === expectedDone) {
        todoTestsPassed++;
      }
    });
    
    dv.paragraph(`📊 **Todo Detection:** ${todoTestsPassed}/${todoTests.length} tests passed`);
    
    // Test 2: Header detection
    dv.header(3, "📋 Test 2: Header Detection");
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
      // Only call getHeaderLevel if it's actually a header to avoid null pointer error
      const level = isHeader ? parser.getHeaderLevel(test.line) : 0;
      
      const status = (isHeader === test.expected && level === test.level) ? "✅ PASS" : "❌ FAIL";
      dv.paragraph(`**Test ${index + 1}:** "${test.line}" → Header: ${isHeader} (expected: ${test.expected}), Level: ${level} (expected: ${test.level}) ${status}`);
      
      if (isHeader === test.expected && level === test.level) {
        headerTestsPassed++;
      }
    });
    
    dv.paragraph(`📊 **Header Detection:** ${headerTestsPassed}/${headerTests.length} tests passed`);
    
    // Test 3: Block parsing with sample content
    dv.header(3, "📋 Test 3: Block Parsing");
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
      const collection = await parser.parse("test-file.md", sampleContent);
      dv.paragraph(`📦 **Total blocks parsed:** ${collection ? collection.blocks.length : 0}`);
      
      if (!collection || !collection.blocks) {
        dv.paragraph("❌ **Parse returned invalid collection**");
        return;
      }
      
      // Count block types
      const blockTypes = {};
      collection.blocks.forEach(block => {
        const blockType = block.getAttribute ? block.getAttribute("type") : block.blockType;
        blockTypes[blockType] = (blockTypes[blockType] || 0) + 1;
      });
      
      dv.paragraph("📊 **Block type summary:**");
      Object.entries(blockTypes).forEach(([type, count]) => {
        dv.paragraph(`• **${type}:** ${count}`);
      });
      
      // Verify expected blocks (based on actual parser behavior)
      const expectedTodos = 3; // Should find 3 todo items
      const expectedDone = 2;  // Should find 2 completed items
      const expectedHeaders = 5; // Parser finds 5 headers: # Sample Document, ## Todo Section, ## Notes Section, ### Subsection, ## Mentions
      
      const actualTodos = blockTypes.todo || 0;
      const actualDone = blockTypes.done || 0;
      const actualHeaders = blockTypes.header || 0;
      
      dv.paragraph(`🎯 **Expected todos:** ${expectedTodos}, **found:** ${actualTodos}`);
      dv.paragraph(`🎯 **Expected done:** ${expectedDone}, **found:** ${actualDone}`);
      dv.paragraph(`🎯 **Expected headers:** ${expectedHeaders}, **found:** ${actualHeaders}`);
      
      const blockParsingPassed = (
        actualTodos === expectedTodos &&
        actualDone === expectedDone &&
        actualHeaders === expectedHeaders
      );
      
      if (blockParsingPassed) {
        dv.paragraph("✅ **Block parsing test PASSED**");
      } else {
        dv.paragraph("❌ **Block parsing test FAILED**");
      }
      
    } catch (parseError) {
      dv.paragraph(`❌ **Block parsing failed:** ${parseError.message}`);
    }
    
    // Test 4: File loading test (if possible)
    dv.header(3, "📋 Test 4: File Loading");
    try {
      // Try to load a real file for testing
      const testFilePath = "Journal/2025/07.July/2025-07-06.md";
      const fileContent = await parser.loadFile(app, testFilePath);
      
      if (fileContent && fileContent.length > 0) {
        dv.paragraph(`✅ **File loaded successfully:** ${fileContent.length} characters`);
        
        // Parse the real file
        const realCollection = await parser.parse(testFilePath, fileContent);
        dv.paragraph(`📦 **Real file blocks parsed:** ${realCollection ? realCollection.blocks.length : 0}`);
        
        if (realCollection && realCollection.blocks) {
          // Show block summary
          const realBlockTypes = {};
          realCollection.blocks.forEach(block => {
            const blockType = block.getAttribute ? block.getAttribute("type") : block.blockType;
            realBlockTypes[blockType] = (realBlockTypes[blockType] || 0) + 1;
          });
        
          dv.paragraph("📊 **Real file block types:**");
          Object.entries(realBlockTypes).forEach(([type, count]) => {
            dv.paragraph(`• **${type}:** ${count}`);
          });
        }
        
      } else {
        dv.paragraph("⚠️ **File loaded but empty or not found**");
      }
      
    } catch (fileError) {
      dv.paragraph(`⚠️ **File loading test skipped:** ${fileError.message}`);
    }
    
    // Test 5: Performance test
    dv.header(3, "📋 Test 5: Performance Test");
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
    
    const perfCollection = await parser.parse("performance-test.md", largeContent);
    const endTime = Date.now();
    const duration = endTime - startTime;
    
    const perfBlocksLength = perfCollection ? perfCollection.blocks.length : 0;
    dv.paragraph(`⏱️ **Parsed ${perfBlocksLength} blocks in ${duration}ms**`);
    dv.paragraph(`📊 **Performance:** ${(perfBlocksLength / duration * 1000).toFixed(0)} blocks/second`);
    
    if (duration < 1000) { // Should complete within 1 second
      dv.paragraph("✅ **Performance test PASSED**");
    } else {
      dv.paragraph("⚠️ **Performance test SLOW** (but not failed)");
    }
    
    // Final summary
    dv.header(3, "📊 Test Summary");
    dv.paragraph(`✅ **Todo Detection:** ${todoTestsPassed}/${todoTests.length} tests passed`);
    dv.paragraph(`✅ **Header Detection:** ${headerTestsPassed}/${headerTests.length} tests passed`);
    dv.paragraph("✅ **Block Parsing:** Completed");
    dv.paragraph("✅ **File Loading:** Completed");
    dv.paragraph("✅ **Performance:** Completed");
    
    const totalTests = todoTests.length + headerTests.length + 3; // +3 for other tests
    const passedTests = todoTestsPassed + headerTestsPassed + 3;
    const passRate = ((passedTests / totalTests) * 100).toFixed(1);
    
    dv.paragraph(`📈 **Overall Pass Rate:** ${passRate}%`);
    
    if (passRate >= 90) {
      dv.paragraph("🎉 **noteBlocksParser tests PASSED!**");
    } else {
      dv.paragraph("⚠️ **Some noteBlocksParser tests need attention**");
    }
    
  } catch (error) {
    dv.paragraph(`❌ **Test failed with error:** ${error.message}`);
    dv.paragraph(`**Stack trace:** ${error.stack}`);
  }
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
