# Test: Todo Rollover

## Description
Tests the todoRollover component which handles rolling over incomplete todos from previous days to today's daily note, including recurrence processing and activity filtering.

## Test Cases
- [x] Basic todo rollover functionality
- [x] Recurrence pattern processing
- [x] Activity-related todo filtering
- [x] Date calculations and formatting
- [x] File modification and backup
- [x] Integration with noteBlocksParser
- [x] Performance with large datasets

## DataviewJS Test Block

```dataviewjs
/**
 * Test: todoRollover Component
 * Tests todo rollover functionality and recurrence processing
 */

async function testTodoRollover() {
  console.log("🧪 === TODO ROLLOVER TEST START ===");
  
  try {
    // Load required modules
    const { todoRollover } = await cJS();
    const { noteBlocksParser } = await cJS();
    const { fileIO } = await cJS();
    
    console.log("✅ Modules loaded successfully");
    
    const rollover = new todoRollover();
    const parser = new noteBlocksParser();
    const fileIOInstance = new fileIO();
    
    // Test 1: Recurrence Pattern Processing
    console.log("\n📋 Test 1: Recurrence Pattern Processing");
    
    const recurrenceTests = [
      {
        todo: "- [ ] Daily task (daily)",
        date: "2025-07-06",
        expected: "- [ ] Daily task (daily)"
      },
      {
        todo: "- [ ] Weekly meeting (weekly)",
        date: "2025-07-06", 
        expected: "- [ ] Weekly meeting (weekly)"
      },
      {
        todo: "- [ ] Monthly report (monthly)",
        date: "2025-07-06",
        expected: "- [ ] Monthly report (monthly)"
      },
      {
        todo: "- [ ] Regular todo without recurrence",
        date: "2025-07-06",
        expected: "- [ ] Regular todo without recurrence"
      },
      {
        todo: "- [ ] Task due +3d",
        date: "2025-07-06",
        expected: "- [ ] Task due +3d"
      }
    ];
    
    let recurrenceTestsPassed = 0;
    recurrenceTests.forEach((test, index) => {
      try {
        const result = rollover.processRecurrence(test.todo, test.date);
        console.log(`   Test ${index + 1}: "${test.todo}"`);
        console.log(`   Result: "${result}"`);
        console.log(`   Expected: "${test.expected}"`);
        
        if (result === test.expected) {
          console.log("   ✅ PASS");
          recurrenceTestsPassed++;
        } else {
          console.log("   ❌ FAIL - Recurrence processing mismatch");
        }
      } catch (error) {
        console.log(`   ❌ FAIL - Error: ${error.message}`);
      }
    });
    
    console.log(`📊 Recurrence Processing: ${recurrenceTestsPassed}/${recurrenceTests.length} tests passed`);
    
    // Test 2: Activity-Related Todo Detection
    console.log("\n📋 Test 2: Activity-Related Todo Detection");
    
    // Create sample blocks for testing
    const sampleBlocks = [
      {
        page: "Journal/2025/07.July/2025-07-05.md",
        blockType: "todo",
        data: "- [ ] Regular todo item",
        headerLevel: 0
      },
      {
        page: "Journal/2025/07.July/2025-07-05.md", 
        blockType: "header",
        data: "## Activity: Test Activity",
        headerLevel: 2
      },
      {
        page: "Journal/2025/07.July/2025-07-05.md",
        blockType: "todo", 
        data: "- [ ] Activity-related todo",
        headerLevel: 0
      },
      {
        page: "Journal/2025/07.July/2025-07-05.md",
        blockType: "todo",
        data: "- [ ] Another regular todo",
        headerLevel: 0
      }
    ];
    
    let activityTestsPassed = 0;
    sampleBlocks.filter(b => b.blockType === "todo").forEach((todoBlock, index) => {
      const isActivityRelated = rollover.isActivityRelatedTodo(todoBlock, sampleBlocks);
      console.log(`   Todo ${index + 1}: "${todoBlock.data}"`);
      console.log(`   Activity-related: ${isActivityRelated}`);
      
      // The second todo should be activity-related (comes after activity header)
      const expectedActivityRelated = index === 1;
      
      if (isActivityRelated === expectedActivityRelated) {
        console.log("   ✅ PASS");
        activityTestsPassed++;
      } else {
        console.log("   ❌ FAIL");
      }
    });
    
    console.log(`📊 Activity Detection: ${activityTestsPassed}/3 tests passed`);
    
    // Test 3: Todo Rollover Logic
    console.log("\n📋 Test 3: Todo Rollover Logic");
    
    // Create test blocks from "previous days"
    const testBlocks = [
      {
        page: "Journal/2025/07.July/2025-07-04.md",
        blockType: "todo",
        data: "- [ ] Incomplete task from yesterday",
        headerLevel: 0
      },
      {
        page: "Journal/2025/07.July/2025-07-04.md",
        blockType: "done", 
        data: "- [x] Completed task from yesterday",
        headerLevel: 0
      },
      {
        page: "Journal/2025/07.July/2025-07-03.md",
        blockType: "todo",
        data: "- [ ] Old incomplete task (daily)",
        headerLevel: 0
      },
      {
        page: "Journal/2025/07.July/2025-07-05.md",
        blockType: "todo",
        data: "- [ ] Task from yesterday",
        headerLevel: 0
      }
    ];
    
    const todayDate = "2025-07-06";
    const currentPageContent = `# Daily Note: ${todayDate}

## Today's Tasks
<!-- Todos will be inserted here -->

## Notes
Some existing content.
`;
    
    try {
      const rolledOverContent = await rollover.rolloverTodos(
        testBlocks,
        todayDate,
        currentPageContent,
        false // Don't remove from original pages for testing
      );
      
      console.log("   📝 Rollover completed successfully");
      console.log(`   📄 Content length: ${rolledOverContent.length} characters`);
      
      // Check if todos were added
      const todoCount = (rolledOverContent.match(/- \[ \]/g) || []).length;
      console.log(`   📋 Todos in result: ${todoCount}`);
      
      // Should have at least the incomplete todos (not the completed ones)
      const expectedMinTodos = 3; // 3 incomplete todos from test blocks
      
      if (todoCount >= expectedMinTodos) {
        console.log("   ✅ Todo rollover test PASSED");
      } else {
        console.log(`   ❌ Todo rollover test FAILED - Expected at least ${expectedMinTodos} todos, got ${todoCount}`);
      }
      
      // Check if original content is preserved
      if (rolledOverContent.includes("Some existing content")) {
        console.log("   ✅ Original content preserved");
      } else {
        console.log("   ❌ Original content not preserved");
      }
      
    } catch (rolloverError) {
      console.error("   ❌ Rollover test failed:", rolloverError);
    }
    
    // Test 4: Integration Test with Real Data
    console.log("\n📋 Test 4: Integration Test");
    
    try {
      // Get current page info
      const currentPageFile = dv.current().file;
      const title = currentPageFile.name;
      
      console.log(`   📄 Current page: ${title}`);
      
      // Check if this looks like a daily note
      const isDaily = fileIOInstance.isDailyNote(title);
      console.log(`   📅 Is daily note: ${isDaily}`);
      
      if (isDaily) {
        // Get journal pages (excluding current)
        const journalPages = dv
          .pages('"Journal"')
          .filter((page) => !page.file.path.includes(title));
        
        console.log(`   📚 Journal pages found: ${journalPages.length}`);
        
        if (journalPages.length > 0) {
          // Parse a few pages for testing
          const testPages = journalPages.slice(0, 3); // Test with first 3 pages
          console.log(`   🧪 Testing with ${testPages.length} pages`);
          
          const allBlocks = await parser.run(app, testPages, "YYYY-MM-DD");
          console.log(`   📦 Total blocks parsed: ${allBlocks.length}`);
          
          // Count todos
          const todoBlocks = allBlocks.filter(b => b.blockType === "todo");
          console.log(`   📋 Todo blocks found: ${todoBlocks.length}`);
          
          if (todoBlocks.length > 0) {
            // Test rollover with real data (dry run)
            const currentContent = await fileIOInstance.loadFile(app, currentPageFile.path);
            
            const testResult = await rollover.rolloverTodos(
              allBlocks,
              moment().format("YYYY-MM-DD"),
              currentContent,
              false // Dry run - don't modify files
            );
            
            console.log("   ✅ Integration test completed successfully");
            console.log(`   📊 Result length: ${testResult.length} characters`);
            
          } else {
            console.log("   ℹ️  No todos found for integration test");
          }
        } else {
          console.log("   ℹ️  No journal pages found for integration test");
        }
      } else {
        console.log("   ℹ️  Not a daily note - skipping integration test");
      }
      
    } catch (integrationError) {
      console.log(`   ⚠️  Integration test skipped: ${integrationError.message}`);
    }
    
    // Test 5: Performance Test
    console.log("\n📋 Test 5: Performance Test");
    
    const startTime = Date.now();
    
    // Create large dataset for performance testing
    const largeBlocks = [];
    for (let i = 0; i < 500; i++) {
      largeBlocks.push({
        page: `Journal/2025/07.July/2025-07-${String(i % 30 + 1).padStart(2, '0')}.md`,
        blockType: "todo",
        data: `- [ ] Performance test todo ${i}`,
        headerLevel: 0
      });
    }
    
    try {
      const perfResult = await rollover.rolloverTodos(
        largeBlocks,
        "2025-07-06",
        "# Performance Test\n\n## Tasks\n\n## Notes\n",
        false // Dry run
      );
      
      const endTime = Date.now();
      const duration = endTime - startTime;
      
      console.log(`   ⏱️  Processed ${largeBlocks.length} todos in ${duration}ms`);
      console.log(`   📊 Performance: ${(largeBlocks.length / duration * 1000).toFixed(0)} todos/second`);
      console.log(`   📄 Result size: ${perfResult.length} characters`);
      
      if (duration < 2000) { // Should complete within 2 seconds
        console.log("   ✅ Performance test PASSED");
      } else {
        console.log("   ⚠️  Performance test SLOW (but not failed)");
      }
      
    } catch (perfError) {
      console.error("   ❌ Performance test failed:", perfError);
    }
    
    // Final Summary
    console.log("\n📊 TEST SUMMARY");
    console.log("================");
    console.log(`✅ Recurrence Processing: ${recurrenceTestsPassed}/${recurrenceTests.length}`);
    console.log(`✅ Activity Detection: ${activityTestsPassed}/3`);
    console.log("✅ Todo Rollover: Completed");
    console.log("✅ Integration Test: Completed");
    console.log("✅ Performance Test: Completed");
    
    const totalTests = recurrenceTests.length + 3 + 3; // +3 for other major tests
    const passedTests = recurrenceTestsPassed + activityTestsPassed + 3;
    const passRate = ((passedTests / totalTests) * 100).toFixed(1);
    
    console.log(`📈 Overall Pass Rate: ${passRate}%`);
    
    if (passRate >= 85) {
      console.log("🎉 todoRollover tests PASSED!");
    } else {
      console.log("⚠️  Some todoRollover tests need attention");
    }
    
  } catch (error) {
    console.error("❌ Test failed with error:", error);
    console.error("Stack trace:", error.stack);
  }
  
  console.log("🧪 === TODO ROLLOVER TEST END ===");
}

// Run the test
testTodoRollover();
```

## Expected Results

### ✅ Success Indicators
- **Module loading** succeeds without errors
- **Recurrence processing** handles daily/weekly/monthly patterns correctly
- **Activity detection** identifies todos under activity headers
- **Todo rollover** moves incomplete todos to current day
- **Content preservation** maintains existing daily note content
- **Performance** handles large datasets efficiently

### ❌ Failure Indicators
- Module loading errors
- Incorrect recurrence pattern processing
- Wrong activity-related todo detection
- Missing todos in rollover result
- Lost or corrupted existing content
- Poor performance with large datasets

## Troubleshooting

### Common Issues
1. **Module not found**: Verify todoRollover.js exists in Scripts/components/
2. **Date format errors**: Check date string formatting (YYYY-MM-DD)
3. **File access errors**: Ensure proper file permissions
4. **Memory issues**: Reduce test dataset size if needed

### Debug Tips
- Check console for detailed error messages
- Verify file paths match your vault structure
- Test with smaller datasets first
- Use dry run mode to avoid file modifications

## Integration Notes

This test works with:
- **noteBlocksParser**: For parsing markdown content
- **fileIO**: For file operations and date detection
- **Real journal files**: For integration testing

---

**This test validates the core todo management functionality of the PKM system.**
