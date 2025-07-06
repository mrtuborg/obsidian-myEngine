# Test Helpers and Utilities

## Description
Provides helper functions and utilities for testing the PKM system components. These utilities can be used across different test files to standardize testing procedures and reduce code duplication.

## Available Helpers

### DataviewJS Test Helpers

```dataviewjs
/**
 * Test Helper Functions
 * Reusable utilities for PKM system testing
 */

// Global test helpers object
window.PKMTestHelpers = {
  
  /**
   * Assert function for test validation
   */
  assert: function(condition, message) {
    if (condition) {
      console.log(`✅ PASS: ${message}`);
      return true;
    } else {
      console.log(`❌ FAIL: ${message}`);
      return false;
    }
  },
  
  /**
   * Assert equality with detailed output
   */
  assertEqual: function(actual, expected, message) {
    const isEqual = actual === expected;
    if (isEqual) {
      console.log(`✅ PASS: ${message}`);
      console.log(`   Expected: ${expected}, Got: ${actual}`);
    } else {
      console.log(`❌ FAIL: ${message}`);
      console.log(`   Expected: ${expected}, Got: ${actual}`);
    }
    return isEqual;
  },
  
  /**
   * Assert array contains specific elements
   */
  assertContains: function(array, element, message) {
    const contains = Array.isArray(array) && array.includes(element);
    if (contains) {
      console.log(`✅ PASS: ${message}`);
    } else {
      console.log(`❌ FAIL: ${message}`);
      console.log(`   Array: [${array}], Looking for: ${element}`);
    }
    return contains;
  },
  
  /**
   * Assert string contains substring
   */
  assertStringContains: function(string, substring, message) {
    const contains = typeof string === 'string' && string.includes(substring);
    if (contains) {
      console.log(`✅ PASS: ${message}`);
    } else {
      console.log(`❌ FAIL: ${message}`);
      console.log(`   String length: ${string ? string.length : 'null'}, Looking for: "${substring}"`);
    }
    return contains;
  },
  
  /**
   * Performance timer utility
   */
  timer: {
    start: function(name) {
      this[name] = Date.now();
    },
    
    end: function(name) {
      if (this[name]) {
        const duration = Date.now() - this[name];
        console.log(`⏱️  ${name}: ${duration}ms`);
        delete this[name];
        return duration;
      }
      return 0;
    }
  },
  
  /**
   * Generate test data
   */
  generateTestData: {
    
    /**
     * Generate sample todo items
     */
    todos: function(count = 5) {
      const todos = [];
      for (let i = 0; i < count; i++) {
        todos.push(`- [ ] Test todo item ${i + 1}`);
      }
      return todos;
    },
    
    /**
     * Generate sample daily note content
     */
    dailyNote: function(date) {
      return `---
date: ${date}
tags: [daily, test]
---

# Daily Note: ${date}

## Tasks
- [ ] Sample task 1
- [ ] Sample task 2
- [x] Completed task

## Notes
This is a test daily note generated for testing purposes.

## Activities
### Activity: Test Activity
- [ ] Activity todo 1
- [ ] Activity todo 2

## Reflection
Test reflection content.
`;
    },
    
    /**
     * Generate sample activity content
     */
    activity: function(name, stage = "In Progress") {
      return `---
stage: "${stage}"
created: ${moment().format("YYYY-MM-DD")}
updated: ${moment().format("YYYY-MM-DD")}
tags: [activity, test]
---

# ${name}

## Description
This is a test activity for testing purposes.

## Tasks
- [ ] Test task 1
- [ ] Test task 2 (daily)
- [x] Completed test task

## Notes
Test activity notes and content.
`;
    },
    
    /**
     * Generate sample blocks for parser testing
     */
    blocks: function(count = 10) {
      const blocks = [];
      for (let i = 0; i < count; i++) {
        blocks.push({
          page: `test-page-${i}.md`,
          blockType: i % 3 === 0 ? "todo" : (i % 3 === 1 ? "done" : "header"),
          data: i % 3 === 0 ? `- [ ] Test todo ${i}` : 
                (i % 3 === 1 ? `- [x] Done todo ${i}` : `## Header ${i}`),
          headerLevel: i % 3 === 2 ? 2 : 0
        });
      }
      return blocks;
    }
  },
  
  /**
   * File system test utilities
   */
  fileSystem: {
    
    /**
     * Check if file exists (mock)
     */
    fileExists: function(path) {
      // In a real implementation, this would check actual file existence
      // For testing, we'll simulate based on common paths
      const commonPaths = [
        "Engine/Scripts/components/noteBlocksParser.js",
        "Engine/Scripts/components/todoRollover.js",
        "Engine/Scripts/utilities/fileIO.js",
        "Engine/TestSuite/Samples/sample-activity.md",
        "Engine/TestSuite/Samples/sample-daily-note.md"
      ];
      return commonPaths.includes(path);
    },
    
    /**
     * Get mock file content
     */
    getMockContent: function(type) {
      switch (type) {
        case 'daily':
          return this.generateTestData.dailyNote(moment().format("YYYY-MM-DD"));
        case 'activity':
          return this.generateTestData.activity("Test Activity");
        default:
          return "# Test Content\n\nThis is mock content for testing.";
      }
    }
  },
  
  /**
   * Test result aggregation
   */
  results: {
    tests: [],
    
    add: function(testName, passed, message = "") {
      this.tests.push({
        name: testName,
        passed: passed,
        message: message,
        timestamp: new Date().toISOString()
      });
    },
    
    summary: function() {
      const total = this.tests.length;
      const passed = this.tests.filter(t => t.passed).length;
      const failed = total - passed;
      const passRate = total > 0 ? ((passed / total) * 100).toFixed(1) : 0;
      
      console.log("\n📊 TEST RESULTS SUMMARY");
      console.log("=======================");
      console.log(`📈 Total Tests: ${total}`);
      console.log(`✅ Passed: ${passed}`);
      console.log(`❌ Failed: ${failed}`);
      console.log(`📊 Pass Rate: ${passRate}%`);
      
      if (failed > 0) {
        console.log("\n❌ FAILED TESTS:");
        this.tests.filter(t => !t.passed).forEach(test => {
          console.log(`   • ${test.name}: ${test.message}`);
        });
      }
      
      return { total, passed, failed, passRate };
    },
    
    clear: function() {
      this.tests = [];
    }
  },
  
  /**
   * Mock data providers
   */
  mocks: {
    
    /**
     * Mock Obsidian app object
     */
    app: {
      vault: {
        read: async function(file) {
          return "Mock file content";
        },
        modify: async function(file, content) {
          return true;
        }
      }
    },
    
    /**
     * Mock dataview object
     */
    dv: {
      pages: function(query) {
        return [
          { file: { name: "test-page-1", path: "test/path1.md" } },
          { file: { name: "test-page-2", path: "test/path2.md" } }
        ];
      },
      current: function() {
        return { file: { name: "current-page", path: "current/path.md" } };
      }
    }
  },
  
  /**
   * Validation utilities
   */
  validate: {
    
    /**
     * Validate daily note format
     */
    dailyNoteFormat: function(filename) {
      const regex = /^\d{4}-\d{2}-\d{2}$/;
      return regex.test(filename.replace('.md', ''));
    },
    
    /**
     * Validate todo format
     */
    todoFormat: function(line) {
      return line.trim().match(/^-\s*\[\s*\]\s*.+/);
    },
    
    /**
     * Validate done item format
     */
    doneFormat: function(line) {
      return line.trim().match(/^-\s*\[x\]\s*.+/i);
    },
    
    /**
     * Validate header format
     */
    headerFormat: function(line) {
      return line.trim().match(/^#+\s*.+/);
    },
    
    /**
     * Validate frontmatter
     */
    frontmatter: function(content) {
      return content.startsWith('---') && content.includes('---\n');
    }
  },
  
  /**
   * Test environment setup
   */
  setup: {
    
    /**
     * Initialize test environment
     */
    init: function() {
      console.log("🔧 Initializing test environment...");
      PKMTestHelpers.results.clear();
      console.log("✅ Test environment ready");
    },
    
    /**
     * Cleanup after tests
     */
    cleanup: function() {
      console.log("🧹 Cleaning up test environment...");
      // Cleanup operations would go here
      console.log("✅ Cleanup complete");
    }
  }
};

// Initialize test helpers
PKMTestHelpers.setup.init();

console.log("🧪 PKM Test Helpers loaded successfully!");
console.log("📚 Available helpers:");
console.log("   • PKMTestHelpers.assert()");
console.log("   • PKMTestHelpers.assertEqual()");
console.log("   • PKMTestHelpers.assertContains()");
console.log("   • PKMTestHelpers.assertStringContains()");
console.log("   • PKMTestHelpers.timer");
console.log("   • PKMTestHelpers.generateTestData");
console.log("   • PKMTestHelpers.fileSystem");
console.log("   • PKMTestHelpers.results");
console.log("   • PKMTestHelpers.mocks");
console.log("   • PKMTestHelpers.validate");
console.log("   • PKMTestHelpers.setup");
```

## Usage Examples

### Basic Assertions
```javascript
// Simple assertion
PKMTestHelpers.assert(true, "This should pass");

// Equality assertion
PKMTestHelpers.assertEqual(5, 5, "Numbers should be equal");

// String contains assertion
PKMTestHelpers.assertStringContains("Hello World", "World", "Should contain 'World'");
```

### Performance Testing
```javascript
// Start timer
PKMTestHelpers.timer.start("myTest");

// ... run test code ...

// End timer and get duration
const duration = PKMTestHelpers.timer.end("myTest");
```

### Test Data Generation
```javascript
// Generate test todos
const todos = PKMTestHelpers.generateTestData.todos(10);

// Generate test daily note
const dailyNote = PKMTestHelpers.generateTestData.dailyNote("2025-07-06");

// Generate test blocks
const blocks = PKMTestHelpers.generateTestData.blocks(20);
```

### Result Tracking
```javascript
// Add test result
PKMTestHelpers.results.add("Test Name", true, "Test passed successfully");

// Get summary
const summary = PKMTestHelpers.results.summary();
```

### Validation
```javascript
// Validate formats
const isValidDaily = PKMTestHelpers.validate.dailyNoteFormat("2025-07-06");
const isValidTodo = PKMTestHelpers.validate.todoFormat("- [ ] Test todo");
```

## Integration with Test Files

To use these helpers in your test files, simply reference them:

```javascript
// In any test file
const helpers = PKMTestHelpers;

// Use assertions
helpers.assert(condition, "Test description");

// Track results
helpers.results.add("My Test", passed, message);

// Get summary at end
helpers.results.summary();
```

---

**These helpers standardize testing procedures and make test files more maintainable.**
