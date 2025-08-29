# Test Writing Best Practices for CustomJS Components

## Overview
This document provides guidelines for writing tests that work correctly with the CustomJS factory pattern used throughout the PKM system.

## CustomJS Factory Pattern Requirements

### ✅ Correct Pattern
```javascript
// Load CustomJS result
const cjsResult = await cJS();

// Get factory function
const componentFactory = cjsResult.createComponentNameInstance;

// Validate factory exists
if (!componentFactory) {
  throw new Error("componentFactory not found in CustomJS");
}

// Create instance using factory
const instance = componentFactory();
```

### ❌ Incorrect Pattern (Old Constructor)
```javascript
// DON'T DO THIS - Will cause errors
const { componentName } = await cJS();
const instance = new componentName();
```

## Component Factory Names

### Core Components
- `fileIO` → `cjsResult.createfileIOInstance`
- `noteBlocksParser` → `cjsResult.createnoteBlocksParserInstance`
- `mentionsProcessor` → `cjsResult.creatementionsProcessorInstance`

### Block System Components
- `Block` → `cjsResult.createBlockInstance`
- `BlockCollection` → `cjsResult.createBlockCollectionInstance`

### Composers
- `dailyNoteComposer` → `cjsResult.createdailyNoteComposerInstance`
- `activityComposer` → `cjsResult.createactivityComposerInstance`

### Processors
- `todoRollover` → `cjsResult.createtodoRolloverInstance`
- `activitiesInProgress` → `cjsResult.createactivitiesInProgressInstance`

## Test Structure Template

### Single Component Test
```javascript
```dataviewjs
async function testComponentName() {
  console.log("🧪 === COMPONENT TEST START ===");
  
  try {
    // Load CustomJS factory
    const cjsResult = await cJS();
    const componentFactory = cjsResult.createComponentNameInstance;
    
    if (!componentFactory) {
      throw new Error("componentFactory not found in CustomJS");
    }
    
    const instance = componentFactory();
    console.log("✅ Module loaded successfully");
    
    // Test 1: Basic functionality
    console.log("\n📋 Test 1: Basic Functionality");
    // ... test code here
    
    // Test validation and summary
    console.log("\n📊 TEST SUMMARY");
    // ... summary code here
    
  } catch (error) {
    console.error("❌ Test failed with error:", error);
    console.error("Stack trace:", error.stack);
  }
  
  console.log("🧪 === COMPONENT TEST END ===");
}

// Run the test
testComponentName();
```
```

### Multiple Component Test
```javascript
```dataviewjs
async function testMultipleComponents() {
  console.log("🧪 === INTEGRATION TEST START ===");
  
  try {
    // Load all required modules using CustomJS factory pattern
    const cjsResult = await cJS();
    
    // Get factory functions
    const component1Factory = cjsResult.createComponent1Instance;
    const component2Factory = cjsResult.createComponent2Instance;
    const component3Factory = cjsResult.createComponent3Instance;
    
    // Validate all factories are available
    if (!component1Factory || !component2Factory || !component3Factory) {
      throw new Error("One or more factory functions not found in CustomJS");
    }
    
    console.log("✅ All modules loaded successfully");
    
    // Create instances using factory functions
    const instance1 = component1Factory();
    const instance2 = component2Factory();
    const instance3 = component3Factory();
    
    // ... test code here
    
  } catch (error) {
    console.error("❌ Test failed with error:", error);
    console.error("Stack trace:", error.stack);
  }
  
  console.log("🧪 === INTEGRATION TEST END ===");
}

// Run the test
testMultipleComponents();
```
```

## Visual Feedback Best Practices

### Use DataviewJS Display Functions
```javascript
// ✅ Correct - Shows in document
dv.header(2, "🎭 Test Results");
dv.paragraph("**Testing:** Component functionality");
dv.paragraph(`✅ **Test passed:** ${result}`);

// ❌ Incorrect - Only shows in console
console.log("Test Results");
console.log("Testing: Component functionality");
```

### Test Result Display Template
```javascript
// Test Validation Section
dv.header(3, "✅ Test Validation");
let allTestsPassed = true;
let testResults = [];

// Test 1: Basic functionality
if (basicTestPassed) {
  testResults.push("✅ **Basic functionality:** PASSED");
} else {
  testResults.push("❌ **Basic functionality:** FAILED");
  allTestsPassed = false;
}

// Display all results
testResults.forEach(result => dv.paragraph(result));

// Final summary
if (allTestsPassed) {
  dv.paragraph("🎉 **ALL TESTS PASSED!** Component is working correctly.");
} else {
  dv.paragraph("⚠️ **SOME TESTS FAILED.** Check the results above for details.");
}
```

## Variable Naming Best Practices

### Avoid Duplicate Variable Names
```javascript
// ✅ Correct - Unique variable names
const todoMentions = collection.blocks.filter(/* todo logic */);
const todoStyleMentions = mentionBlocks.filter(/* todo-style logic */);
const todoWithMentionBlocks = collection.blocks.filter(/* enhanced logic */);

// ❌ Incorrect - Duplicate names cause SyntaxError
const todoMentionBlocks = collection.blocks.filter(/* first usage */);
// ... later in code ...
const todoMentionBlocks = mentionBlocks.filter(/* second usage - ERROR! */);
```

### Use Descriptive Names
```javascript
// ✅ Good naming
const headerMentions = blocks.filter(b => b.type === "header" && b.hasMentions);
const todoStyleMentions = mentionBlocks.filter(b => b.content.includes("- [ ]"));
const codeStyleMentions = mentionBlocks.filter(b => b.content.includes("//"));

// ❌ Poor naming
const blocks1 = blocks.filter(/* ... */);
const blocks2 = mentionBlocks.filter(/* ... */);
const blocks3 = mentionBlocks.filter(/* ... */);
```

## Error Handling Patterns

### Factory Validation
```javascript
// Always validate factory functions exist
const cjsResult = await cJS();
const componentFactory = cjsResult.createComponentNameInstance;

if (!componentFactory) {
  throw new Error("componentFactory not found in CustomJS");
}
```

### Graceful Test Failures
```javascript
try {
  // Test code here
  const result = await component.method();
  
  if (result) {
    dv.paragraph("✅ **Test passed:** Method executed successfully");
  } else {
    dv.paragraph("❌ **Test failed:** Method returned empty result");
  }
  
} catch (testError) {
  dv.paragraph(`⚠️ **Test skipped:** ${testError.message}`);
}
```

## Performance Considerations

### Async/Await Usage
```javascript
// ✅ Correct - Proper async handling
const collection = await parser.parse("test-file.md", content);

// ❌ Incorrect - Missing await
const collection = parser.parse("test-file.md", content); // May be Promise
```

### Resource Cleanup
```javascript
// Clean up large test data
let largeContent = "# Test\n";
for (let i = 0; i < 1000; i++) {
  largeContent += `- [ ] Item ${i}\n`;
}

const result = parser.parse("test.md", largeContent);

// Clear large variables when done
largeContent = null;
```

## Common Pitfalls to Avoid

### 1. Constructor Pattern Usage
- **Problem:** Using `new ComponentName()` instead of factory functions
- **Solution:** Always use `componentFactory()` pattern

### 2. Missing Factory Validation
- **Problem:** Not checking if factory function exists
- **Solution:** Always validate with `if (!factory)` check

### 3. Variable Name Conflicts
- **Problem:** Declaring same variable name twice in same scope
- **Solution:** Use descriptive, unique variable names

### 4. Console-Only Output
- **Problem:** Using `console.log()` for test results
- **Solution:** Use `dv.paragraph()` and `dv.header()` for document display

### 5. Missing Error Handling
- **Problem:** Tests crash on unexpected errors
- **Solution:** Wrap test sections in try-catch blocks

## Test Categories and Organization

### Core Tests (`TestSuite/Core/`)
- Test individual components in isolation
- Focus on component-specific functionality
- Use single component factory pattern

### Integration Tests (`TestSuite/Integration/`)
- Test multiple components working together
- Focus on data flow between components
- Use multiple component factory pattern

### Block System Tests (`TestSuite/BlockSystem/`)
- Test Block system components specifically
- Focus on parsing, hierarchy, and queries
- Use Block-specific factory patterns

## Validation Checklist

Before submitting a test, verify:

- [ ] Uses CustomJS factory pattern (not constructors)
- [ ] Validates all factory functions exist
- [ ] Uses unique variable names throughout
- [ ] Displays results with `dv.paragraph()` and `dv.header()`
- [ ] Includes proper error handling with try-catch
- [ ] Has descriptive test names and comments
- [ ] Includes test validation and summary sections
- [ ] Uses appropriate async/await for promises
- [ ] Cleans up large test data when possible

## Example: Converting Old Test to New Pattern

### Before (Incorrect)
```javascript
const { noteBlocksParser } = await cJS();
const parser = new noteBlocksParser();

const todoMentionBlocks = blocks.filter(/* ... */);
// ... later ...
const todoMentionBlocks = otherBlocks.filter(/* ... */); // ERROR!

console.log("Test results"); // Console only
```

### After (Correct)
```javascript
const cjsResult = await cJS();
const noteBlocksParser = cjsResult.createnoteBlocksParserInstance;

if (!noteBlocksParser) {
  throw new Error("noteBlocksParser factory not found in CustomJS");
}

const parser = noteBlocksParser();

const todoMentions = blocks.filter(/* ... */);
// ... later ...
const todoStyleMentions = otherBlocks.filter(/* ... */); // Unique name

dv.paragraph("✅ **Test results:** All tests passed"); // Document display
```

---

**Following these guidelines ensures tests work correctly with the CustomJS system and provide clear, reliable results.**
