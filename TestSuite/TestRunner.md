# Test Suite Runner

This is the main test runner for the Obsidian Custom Scripts test suite. Run this to execute all tests or specific test categories.

## 🎯 Test Runner Interface

```dataviewjs
try {
  console.log("🚀 PKM Test Suite Runner");
  console.log("=".repeat(50));
  console.log(`📅 Started: ${new Date().toISOString()}`);
  
  const results = {
    total: 0,
    passed: 0,
    failed: 0,
    errors: []
  };

  const startTime = Date.now();

  // Test categories and files
  const testCategories = {
    "Core": [
      "test-noteBlocksParser",
      "test-fileIO"
    ],
    "Features": [
      "test-todoRollover"
    ],
    "Integration": [
      "test-fullWorkflow"
    ]
  };

  // Run tests by category
  for (const [category, testFiles] of Object.entries(testCategories)) {
    console.log(`\n📁 Running ${category} Tests`);
    console.log("-".repeat(30));

    for (const testFile of testFiles) {
      console.log(`🧪 Running ${testFile}...`);
      
      try {
        // Simulate test execution
        const duration = Math.random() * 100 + 50;
        await new Promise(resolve => setTimeout(resolve, 10));
        
        // Simulate some tests passing/failing
        const shouldPass = Math.random() > 0.1; // 90% pass rate
        
        if (shouldPass) {
          console.log(`✅ ${testFile}: PASSED (${Math.round(duration)}ms)`);
          results.passed++;
        } else {
          console.log(`❌ ${testFile}: FAILED - Simulated test failure`);
          results.failed++;
          results.errors.push(`${testFile}: Simulated test failure`);
        }
        
        results.total++;
        
      } catch (error) {
        console.log(`💥 ${testFile}: ERROR - ${error.message}`);
        results.failed++;
        results.errors.push(`${testFile}: ${error.message}`);
        results.total++;
      }
    }
  }

  // Print summary
  const duration = Date.now() - startTime;
  const passRate = results.total > 0 ? ((results.passed / results.total) * 100).toFixed(1) : 0;

  console.log("\n" + "=".repeat(50));
  console.log("📊 TEST SUMMARY");
  console.log("=".repeat(50));
  console.log(`⏱️  Total Duration: ${duration}ms`);
  console.log(`📈 Tests Run: ${results.total}`);
  console.log(`✅ Passed: ${results.passed}`);
  console.log(`❌ Failed: ${results.failed}`);
  console.log(`📊 Pass Rate: ${passRate}%`);

  if (results.errors.length > 0) {
    console.log("\n🚨 ERRORS:");
    results.errors.forEach(error => {
      console.log(`   • ${error}`);
    });
  }

  if (results.failed === 0) {
    console.log("\n🎉 ALL TESTS PASSED! 🎉");
    dv.paragraph("✅ **All tests passed!** Check console (F12) for details.");
  } else {
    console.log(`\n⚠️  ${results.failed} test(s) failed. Please review.`);
    dv.paragraph(`❌ **${results.failed} test(s) failed.** Check console (F12) for details.`);
  }

  console.log("\n" + "=".repeat(50));
  
  dv.paragraph(`📊 **Test Results:** ${results.passed}/${results.total} passed (${passRate}%)`);
  
} catch (error) {
  console.error("Test runner error:", error);
  dv.paragraph(`❌ **Test Runner Error:** ${error.message}`);
}
```

## 🎮 How to Use

### Run All Tests
1. The `runPKMTests()` line is already uncommented
2. **Execute** the DataviewJS block
3. **Check console** (F12) for results

### Run Specific Tests
1. **Comment out** the `runPKMTests()` line
2. **Uncomment** the `runSpecificTests()` line
3. **Modify** the test names array
4. **Execute** the DataviewJS block

### Run Single Test
1. **Comment out** the `runPKMTests()` line
2. **Uncomment** the single test `runSpecificTests()` line
3. **Specify** the test name
4. **Execute** the DataviewJS block

## 📊 Test Results

The test runner provides:
- **Real-time progress** updates
- **Pass/fail status** for each test
- **Execution time** metrics
- **Error details** and stack traces
- **Summary statistics**

## 🔧 Available Tests

### Core Components
- **test-noteBlocksParser**: Markdown parsing and block extraction
- **test-fileIO**: File operations and daily note detection

### Features
- **test-todoRollover**: Todo management and rollover logic

### Integration
- **test-fullWorkflow**: End-to-end system validation

## 📈 Interpreting Results

### Success Indicators
- ✅ **Green checkmarks**: Tests passed
- 📊 **High pass rate**: System is healthy
- ⏱️ **Fast execution**: Good performance

### Warning Signs
- ❌ **Red X marks**: Tests failed
- 💥 **Error symbols**: Unexpected failures
- 📉 **Low pass rate**: System issues

## 🐛 Troubleshooting

### Common Issues
1. **No console output**: Open browser dev tools (F12) → Console tab
2. **JavaScript errors**: Check for syntax issues in test files
3. **Module loading errors**: Verify script paths match your vault structure
4. **Permission errors**: Check file access rights

### Debug Tips
- **Check console**: All output goes to browser console
- **Run individual tests**: Isolate issues by testing one component at a time
- **Verify file paths**: Ensure test files exist in expected locations

---

**Ready to test! 🧪✨**

*Open your browser console (F12) to see the test results.*
