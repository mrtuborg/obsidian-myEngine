# 🚀 Quick Start Guide - PKM Test Suite

## Getting Started in 3 Steps

### 1. 📋 Load Test Helpers (Optional but Recommended)
```
Open: Engine/TestSuite/Utils/test-helpers.md
Execute: The DataviewJS block
Result: PKMTestHelpers loaded globally
```

### 2. 🧪 Run Your First Test
```
Open: Engine/TestSuite/TestRunner.md
Execute: The DataviewJS block
Check: Browser console (F12) for results
```

### 3. 📊 View Results
```
Console Output: Detailed test results
Pass/Fail Status: ✅ or ❌ indicators
Performance Metrics: Execution times
```

## 🎯 Test Categories

### Core Components
- **test-noteBlocksParser**: Markdown parsing and block extraction
- **test-fileIO**: File operations and daily note detection

### Features
- **test-todoRollover**: Todo management and rollover logic

### Integration
- **test-fullWorkflow**: End-to-end system validation

## 🔧 Running Specific Tests

### Individual Test Files
1. Navigate to any test file (e.g., `Core/test-noteBlocksParser.md`)
2. Execute the DataviewJS block
3. Check console for detailed results

### Custom Test Selection
1. Open `TestRunner.md`
2. Uncomment the `runSpecificTests` section
3. Add desired test names to the array
4. Execute the block

## 📈 Understanding Results

### Success Indicators
- ✅ **Green checkmarks**: Tests passed
- 📊 **High pass rate**: System healthy
- ⏱️ **Fast execution**: Good performance

### Warning Signs
- ❌ **Red X marks**: Tests failed
- 💥 **Error symbols**: Unexpected failures
- 🐌 **Slow execution**: Performance issues

## 🐛 Troubleshooting

### Common Issues & Solutions

#### "cJS is not defined"
- **Cause**: Custom JavaScript not enabled
- **Solution**: Enable custom JS in Obsidian settings

#### "Module not found"
- **Cause**: Script files missing or wrong path
- **Solution**: Verify file paths match your vault structure

#### "Permission denied"
- **Cause**: File access restrictions
- **Solution**: Check file permissions and vault settings

#### Tests run but show no results
- **Cause**: Console not visible
- **Solution**: Open browser dev tools (F12) → Console tab

## 📚 Sample Test Workflow

### Daily Development Workflow
1. **Make changes** to PKM scripts
2. **Run relevant tests** to verify functionality
3. **Check console** for any failures
4. **Fix issues** if tests fail
5. **Run full suite** before committing changes

### Weekly Health Check
1. **Run full test suite** (`TestRunner.md`)
2. **Review performance metrics**
3. **Address any failing tests**
4. **Update tests** for new features

## 🎮 Interactive Testing

### Test Individual Components
```javascript
// In any test file, you can modify and run specific tests
PKMTestHelpers.assert(condition, "My custom test");
PKMTestHelpers.timer.start("myTimer");
// ... test code ...
PKMTestHelpers.timer.end("myTimer");
```

### Generate Test Data
```javascript
// Create sample data for testing
const todos = PKMTestHelpers.generateTestData.todos(10);
const dailyNote = PKMTestHelpers.generateTestData.dailyNote("2025-07-06");
```

## 📊 Performance Benchmarks

### Expected Performance
- **Small datasets** (<100 items): <100ms
- **Medium datasets** (100-1000 items): <500ms
- **Large datasets** (1000+ items): <2000ms

### Performance Testing
```javascript
// Built into most tests
PKMTestHelpers.timer.start("performance");
// ... run operations ...
const duration = PKMTestHelpers.timer.end("performance");
```

## 🔄 Continuous Testing

### Before Making Changes
1. Run existing tests to establish baseline
2. Ensure all tests pass before modifications

### After Making Changes
1. Run affected component tests
2. Run integration tests
3. Run full suite if major changes

### Before Committing
1. Full test suite execution
2. All tests must pass
3. Performance within acceptable ranges

## 📝 Adding New Tests

### For New Features
1. Create test file in appropriate category
2. Follow naming convention: `test-featureName.md`
3. Include comprehensive test cases
4. Add to TestRunner.md test lists

### Test File Template
```markdown
# Test: Feature Name

## Description
Brief description of what this test covers.

## Test Cases
- [ ] Test case 1
- [ ] Test case 2

## DataviewJS Test Block
\`\`\`dataviewjs
async function testFeature() {
  console.log("=== TEST START ===");
  // Test implementation
  console.log("=== TEST END ===");
}
testFeature();
\`\`\`
```

## 🎯 Best Practices

### Test Writing
- **Clear descriptions** for each test case
- **Comprehensive coverage** of edge cases
- **Performance considerations** for large datasets
- **Error handling** validation

### Test Execution
- **Regular testing** during development
- **Full suite** before major releases
- **Performance monitoring** over time
- **Result documentation** for tracking

## 🆘 Getting Help

### Debug Information
1. **Console logs**: Detailed execution information
2. **Error messages**: Specific failure reasons
3. **Stack traces**: Code execution path
4. **Performance metrics**: Timing information

### Common Solutions
- **Restart Obsidian**: Clears cached modules
- **Check file paths**: Ensure correct vault structure
- **Verify permissions**: File access rights
- **Update dependencies**: Ensure latest versions

---

**Happy Testing! 🧪✨**

*The test suite is designed to be your development companion - use it regularly to maintain code quality and catch issues early.*
