# Obsidian JavaScript & CustomJS Patterns Reference

**Last Updated:** August 28, 2025  
**Purpose:** Reference guide for proper JavaScript patterns in Obsidian with CustomJS plugin  
**Target Audience:** LLM assistants working on the Obsidian Engine project

## Overview

This document provides the definitive patterns for writing and calling JavaScript methods within Obsidian using the CustomJS plugin. These patterns are based on the working codebase and should be followed exactly to ensure compatibility.

## CustomJS Plugin Behavior

### How CustomJS Works
1. **Automatic Instantiation:** CustomJS automatically instantiates all classes found in configured JavaScript files
2. **Instance Provision:** Provides both the instance and a constructor function
3. **Global Access:** Makes instances available through the `cJS()` function
4. **No Manual Instantiation:** Never use `new ClassName()` - instances are pre-created

### CustomJS Loading Pattern
```javascript
// CustomJS loads: Scripts/utilities/fileIO.js
// Creates: fileIO instance + createfileIOInstance function
// Available as: cJS().fileIO and cJS().createfileIOInstance
```

## JavaScript Class Structure Patterns

### ✅ CORRECT: Standard Class Definition
```javascript
// File: Scripts/utilities/fileIO.js
class fileIO {
  async saveFile(app, filename, content) {
    // Implementation here
  }
  
  async loadFile(app, filename) {
    // Implementation here
  }
  
  todayDate() {
    return new Date().toISOString().split("T")[0];
  }
}
```

### ✅ CORRECT: Component Class with Run Method
```javascript
// File: Scripts/components/mentionsProcessor.js
class mentionsProcessor {
  async processMentions(currentPageContent, blocks, tagId, frontmatterObj) {
    // Main processing logic
  }
  
  async run(currentPageContent, collectedBlocks, mentionStr, frontmatterObj) {
    return await this.processMentions(
      currentPageContent,
      collectedBlocks,
      mentionStr,
      frontmatterObj
    );
  }
}
```

### ❌ INCORRECT: Export Statements
```javascript
// DON'T DO THIS - CustomJS doesn't use exports
export class fileIO { }
export default fileIO;
module.exports = fileIO;
```

### ❌ INCORRECT: Static Methods Only
```javascript
// DON'T DO THIS - CustomJS needs instance methods
class fileIO {
  static saveFile() { } // Won't work with CustomJS pattern
}
```

## CustomJS Calling Patterns

### ✅ CORRECT: Direct Instance Method Calls
```javascript
// In DataviewJS blocks or templates
const {fileIO} = await cJS();
const content = await fileIO.loadFile(app, filename);
await fileIO.saveFile(app, filename, newContent);
```

### ✅ CORRECT: Multiple Module Loading
```javascript
const {fileIO, mentionsProcessor, noteBlocksParser} = await cJS();
const content = await fileIO.loadFile(app, currentPageFile.path);
const blocks = await noteBlocksParser.run(app, journalPages, "YYYY-MM-DD");
const mentions = await mentionsProcessor.run(content, blocks, tagId, frontmatterObj);
```

### ✅ CORRECT: Component with Run Method
```javascript
const {mentionsProcessor} = await cJS();
const result = await mentionsProcessor.run(content, blocks, tagId, frontmatterObj);
```

### ❌ INCORRECT: Manual Instantiation
```javascript
// DON'T DO THIS - CustomJS already instantiated the class
const {fileIO} = await cJS();
const instance = new fileIO(); // ❌ Error: fileIO is not a constructor
```

### ❌ INCORRECT: Static Method Calls
```javascript
// DON'T DO THIS - CustomJS provides instances, not classes
const {fileIO} = await cJS();
const result = fileIO.staticMethod(); // ❌ Won't work
```

## Template Integration Patterns

### ✅ CORRECT: Templater Template Usage
```javascript
<%*
// Templater template with CustomJS integration
function generateActivityProcessingBlock() {
  let block = "```dataviewjs\n";
  block += "const {fileIO} = await cJS();\n";
  block += "const currentPageFile = dv.current().file;\n";
  block += "let currentPageContent = await fileIO.loadFile(app, currentPageFile.path);\n";
  // ... more processing
  block += "```\n";
  return block;
}

tR += generateActivityProcessingBlock();
%>
```

### ✅ CORRECT: DataviewJS Block Usage
```javascript
```dataviewjs
const {fileIO, mentionsProcessor} = await cJS();
const currentPageFile = dv.current().file;
let currentPageContent = await fileIO.loadFile(app, currentPageFile.path);

const mentions = await mentionsProcessor.run(
  currentPageContent, 
  allBlocks, 
  tagId, 
  frontmatterObj
);

await fileIO.saveFile(app, currentPageFile.path, processedContent);
```
```

## Common Method Patterns

### File Operations Pattern
```javascript
const {fileIO} = await cJS();

// Load file content
const content = await fileIO.loadFile(app, filePath);

// Save file content
await fileIO.saveFile(app, filePath, newContent);

// Generate headers
const header = fileIO.generateActivityHeader(date, stage, responsible);
const dailyHeader = fileIO.generateDailyNoteHeader(title);

// Utility methods
const today = fileIO.todayDate();
const isDaily = fileIO.isDailyNote(fileName);
```

### Processing Component Pattern
```javascript
const {noteBlocksParser, mentionsProcessor, attributesProcessor} = await cJS();

// Parse journal blocks
const allBlocks = await noteBlocksParser.run(app, journalPages, "YYYY-MM-DD");

// Process mentions
const mentions = await mentionsProcessor.run(content, allBlocks, tagId, frontmatterObj);

// Process attributes
const processed = await attributesProcessor.processAttributes(frontmatterObj, content);
```

### Activity Management Pattern
```javascript
const {activitiesInProgress, todoSyncManager} = await cJS();

// Sync todos first
await todoSyncManager.run(app);

// Get activities
const activities = await activitiesInProgress.run(app, pageContent);
```

## Error Handling Patterns

### ✅ CORRECT: Proper Error Handling
```javascript
try {
  const {fileIO} = await cJS();
  const content = await fileIO.loadFile(app, filePath);
  // Process content
  await fileIO.saveFile(app, filePath, processedContent);
} catch (error) {
  console.error("Processing failed:", error);
  dv.paragraph(`❌ Error: ${error.message}`);
}
```

### ✅ CORRECT: Module Availability Check
```javascript
try {
  const cjsResult = await cJS();
  if ('fileIO' in cjsResult) {
    const {fileIO} = cjsResult;
    // Use fileIO
  } else {
    console.error("fileIO module not available");
  }
} catch (error) {
  console.error("CustomJS not available:", error);
}
```

## Testing Patterns

### ✅ CORRECT: Simple Test Structure
```javascript
// File: Scripts/simple-test.js
class simpleTest {
  run() {
    console.log("Simple test is working!");
    return { success: true, message: "Simple test passed" };
  }
}
```

### ✅ CORRECT: Test Execution
```javascript
```dataviewjs
try {
  const {simpleTest} = await cJS();
  const result = simpleTest.run(); // Direct method call
  
  if (result.success) {
    dv.paragraph(`✅ Test passed: ${result.message}`);
  }
} catch (error) {
  dv.paragraph(`❌ Test failed: ${error.message}`);
}
```
```

## Debugging Patterns

### CustomJS Module Inspection
```javascript
```dataviewjs
// Debug: See all available modules
const cjsResult = await cJS();
console.log("Available modules:", Object.keys(cjsResult));

// Debug: Inspect specific module
const {fileIO} = cjsResult;
console.log("fileIO type:", typeof fileIO);
console.log("fileIO methods:", Object.getOwnPropertyNames(Object.getPrototypeOf(fileIO)));
```
```

### Method Call Debugging
```javascript
```dataviewjs
try {
  const {fileIO} = await cJS();
  console.log("Calling fileIO.todayDate()");
  const today = fileIO.todayDate();
  console.log("Result:", today);
} catch (error) {
  console.error("Method call failed:", error);
}
```
```

## Common Mistakes to Avoid

### ❌ Constructor Confusion
```javascript
// WRONG: Trying to instantiate CustomJS-provided instances
const {fileIO} = await cJS();
const instance = new fileIO(); // Error: not a constructor
```

### ❌ Static Method Assumption
```javascript
// WRONG: Assuming static methods work
const {fileIO} = await cJS();
fileIO.staticMethod(); // Won't work - fileIO is an instance
```

### ❌ Export Statement Usage
```javascript
// WRONG: Using Node.js/ES6 export patterns
export class fileIO { } // CustomJS doesn't use exports
```

### ❌ Missing Async/Await
```javascript
// WRONG: Not awaiting CustomJS loading
const {fileIO} = cJS(); // Missing await
```

## File Organization

### Directory Structure
```
Scripts/
├── components/          # Processing components (mentionsProcessor, etc.)
├── utilities/          # Utility classes (fileIO, etc.)
├── simple-test.js      # Test files
└── test-blocks.js      # Complex test systems
```

### Naming Conventions
- **File names:** kebab-case or camelCase (e.g., `simple-test.js`, `fileIO.js`)
- **Class names:** camelCase matching filename (e.g., `class simpleTest`, `class fileIO`)
- **Method names:** camelCase (e.g., `saveFile`, `processAttributes`)

## Integration with Obsidian API

### App Object Usage
```javascript
const {fileIO} = await cJS();

// File operations through app
const file = app.vault.getAbstractFileByPath(filename);
await app.vault.modify(file, content);

// Metadata access
const metadata = app.metadataCache.getFileCache(file);
```

### Dataview Integration
```javascript
```dataviewjs
const {fileIO} = await cJS();
const currentPageFile = dv.current().file;
const journalPages = dv.pages('"Journal"');

// Process with CustomJS modules
const content = await fileIO.loadFile(app, currentPageFile.path);
```
```

## Performance Considerations

### Module Loading
- CustomJS loads all modules once at startup
- `await cJS()` is fast after initial load
- Destructure only needed modules: `const {fileIO} = await cJS()`

### Method Calls
- Instance methods are ready to use immediately
- No instantiation overhead
- Async methods should be properly awaited

---

## Quick Reference

### Basic Pattern
```javascript
const {moduleName} = await cJS();
const result = await moduleName.methodName(parameters);
```

### Multi-Module Pattern
```javascript
const {module1, module2, module3} = await cJS();
const result1 = await module1.run(params);
const result2 = module2.utilityMethod();
```

### Error Handling Pattern
```javascript
try {
  const {moduleName} = await cJS();
  const result = await moduleName.run(params);
} catch (error) {
  console.error("Operation failed:", error);
}
```

---

**Remember:** CustomJS provides instances, not constructors. Always call methods directly on the provided instances, never try to instantiate with `new`.
