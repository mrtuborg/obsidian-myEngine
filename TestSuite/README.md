# Test Suite for Obsidian Custom Scripts

This test suite provides comprehensive testing for all custom scripts in the Personal Knowledge Management (PKM) system. Each feature has dedicated test files that can be run independently to verify functionality.

**📚 Main Documentation:** For complete system documentation, architecture details, and API reference, see [Engine/README.md](../README.md)

## 🎯 Purpose

- **Feature Testing**: Test individual script components in isolation
- **Integration Testing**: Test how components work together
- **Regression Testing**: Ensure new changes don't break existing functionality
- **Development Aid**: Quick testing during development and debugging

## 📁 Test Suite Structure

```
TestSuite/
├── README.md                           # This file
├── TestRunner.md                       # Main test runner interface
├── Core/                               # Core component tests
│   ├── test-noteBlocksParser.md        # Note blocks parsing tests
│   ├── test-fileIO.md                  # File I/O operations tests
│   ├── test-mentionsProcessor.md       # Mentions processing tests
│   └── test-attributesProcessor.md     # Attributes processing tests
├── Features/                           # Feature-specific tests
│   ├── test-todoRollover.md           # Todo rollover functionality
│   ├── test-activitiesInProgress.md   # Activities in progress tests
│   ├── test-activityComposer.md       # Activity composition tests
│   ├── test-dailyNoteComposer.md      # Daily note composition tests
│   └── test-scriptsRemove.md          # Script removal tests
├── Integration/                        # Integration tests
│   ├── test-fullWorkflow.md           # Complete workflow tests
│   ├── test-activityToDaily.md        # Activity to daily note flow
│   └── test-dataConsistency.md        # Data consistency tests
├── BlockSystem/                        # Block system tests
│   ├── README.md                       # Block system test documentation
│   ├── test-basic-hierarchy.md        # Basic hierarchy tests
│   ├── test-edge-cases.md             # Edge case tests
│   ├── test-mixed-types.md            # Mixed block type tests
│   ├── test-real-world-scenario.md    # Real-world scenario tests
│   └── test-compatibility.md          # Compatibility tests
├── Specifications/                     # TDD specifications
│   ├── README.md                       # Specifications documentation
│   └── noteBlocksParser-TDD-Specification.md  # Complete TDD spec for noteBlocksParser
├── Samples/                            # Sample data for testing
│   ├── sample-activity.md             # Sample activity file
│   ├── sample-daily-note.md           # Sample daily note
│   ├── sample-todos.md                # Sample todos for testing
│   └── sample-mentions.md             # Sample mentions for testing
└── Utils/                              # Testing utilities
    ├── test-helpers.md                 # Helper functions for tests
    └── test-data-generator.md          # Generate test data
```

## 🚀 Quick Start

### Running Individual Tests

1. **Open any test file** in Obsidian
2. **Execute the DataviewJS block** to run the test
3. **Check console output** (F12 → Console) for results
4. **Look for ✅ success or ❌ error indicators**

### Running All Tests

1. **Open `TestRunner.md`**
2. **Execute the main test runner**
3. **Review comprehensive test results**

## 📋 Test Categories

### Core Component Tests
- **noteBlocksParser**: Tests markdown parsing, todo detection, block creation
- **fileIO**: Tests file reading/writing, daily note detection, header generation
- **mentionsProcessor**: Tests mention parsing, directive processing, date calculations
- **attributesProcessor**: Tests frontmatter processing, attribute calculations

### Feature Tests
- **todoRollover**: Tests todo rollover logic, recurrence, activity filtering
- **activitiesInProgress**: Tests activity filtering, todo analysis, daily note insertion
- **activityComposer**: Tests activity file composition and processing
- **dailyNoteComposer**: Tests daily note composition and formatting

### Integration Tests
- **fullWorkflow**: Tests complete end-to-end workflows
- **activityToDaily**: Tests activity → daily note integration
- **dataConsistency**: Tests data integrity across operations

### Block System Tests
- **basic-hierarchy**: Tests fundamental block hierarchy relationships
- **edge-cases**: Tests boundary conditions and error scenarios
- **mixed-types**: Tests complex documents with multiple block types
- **real-world-scenario**: Tests realistic usage patterns
- **compatibility**: Tests backward compatibility and integration

### TDD Specifications
- **noteBlocksParser**: Comprehensive specification with 100+ test cases covering all functionality
- Complete behavioral contracts for core components
- Performance benchmarks and requirements
- Edge case documentation and validation
- Integration testing with Obsidian file system

## 🧪 Test Types

### Unit Tests
- Test individual functions and methods
- Isolated component testing
- Mock data and dependencies

### Integration Tests
- Test component interactions
- Real data scenarios
- Cross-component workflows

### Regression Tests
- Verify existing functionality still works
- Test edge cases and known issues
- Performance and reliability tests

## 📊 Test Results

Each test provides:
- **✅ Pass/❌ Fail indicators**
- **Detailed console output**
- **Performance metrics**
- **Error details and stack traces**
- **Test coverage information**

## 🔧 Adding New Tests

### For New Features

1. **Create test file** in appropriate category
2. **Follow naming convention**: `test-featureName.md`
3. **Include test documentation**
4. **Add to TestRunner.md**

### Test File Template

```markdown
# Test: Feature Name

## Description
Brief description of what this test covers.

## Test Cases
- [ ] Test case 1
- [ ] Test case 2
- [ ] Test case 3

## DataviewJS Test Block
\`\`\`dataviewjs
// Test implementation
async function testFeature() {
  console.log("=== FEATURE TEST START ===");
  // Test logic here
  console.log("=== FEATURE TEST END ===");
}
testFeature();
\`\`\`

## Expected Results
Description of expected test outcomes.
```

## 🐛 Debugging Tests

### Console Output
- Open browser developer tools (F12)
- Check Console tab for detailed logs
- Look for error messages and stack traces

### Common Issues
- **Module loading errors**: Check cJS() imports
- **File path issues**: Verify file paths are correct
- **Permission errors**: Ensure files are accessible
- **Async timing**: Check for proper await usage

## 📈 Test Metrics

The test suite tracks:
- **Test execution time**
- **Success/failure rates**
- **Code coverage**
- **Performance benchmarks**
- **Memory usage**

## 🔄 Continuous Testing

### Development Workflow
1. **Write/modify code**
2. **Run relevant tests**
3. **Fix any failures**
4. **Run full test suite**
5. **Commit changes**

### Test Automation
- Tests can be run automatically
- Integration with development workflow
- Continuous monitoring of system health

## 📚 Documentation

Each test file includes:
- **Purpose and scope**
- **Prerequisites**
- **Step-by-step instructions**
- **Expected outcomes**
- **Troubleshooting guide**

## 🤝 Contributing

When adding new features:
1. **Create corresponding tests**
2. **Update test documentation**
3. **Ensure all tests pass**
4. **Add integration tests if needed**

## 📞 Support

For test-related issues:
1. **Check console output** for error details
2. **Review test documentation**
3. **Run individual components** to isolate issues
4. **Check sample data** for correct format

---

**Happy Testing! 🧪✨**
