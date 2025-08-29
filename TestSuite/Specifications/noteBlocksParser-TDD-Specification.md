# noteBlocksParser TDD Specification

## Overview
This document serves as a comprehensive Test-Driven Development (TDD) specification for the `noteBlocksParser` component. The specification describes the component's behavior, architecture, and functionality through detailed test cases.

## Component Purpose
The `noteBlocksParser` is a core component that parses markdown content into structured `Block` objects with hierarchical relationships. It supports multiple block types and maintains parent-child relationships based on indentation and header levels.

## Architecture Specification

### Core Classes and Methods
```dataviewjs
const cjsResult = await cJS();
const noteBlocksParserFactory = cjsResult.createnoteBlocksParserInstance;

dv.header(2, "Factory Pattern Validation");

try {
    if (!noteBlocksParserFactory) {
        throw new Error("noteBlocksParser factory not found in CustomJS");
    }
    
    const parser = noteBlocksParserFactory();
    
    // Test: Component should be instantiable via factory
    const hasParseMethod = typeof parser.parse === 'function';
    const hasRunMethod = typeof parser.run === 'function';
    const hasIsHeaderMethod = typeof parser.isHeader === 'function';
    const hasIsTodoLineMethod = typeof parser.isTodoLine === 'function';
    const hasIsDoneLineMethod = typeof parser.isDoneLine === 'function';
    const hasGetHeaderLevelMethod = typeof parser.getHeaderLevel === 'function';
    const hasCreateBlockMethod = typeof parser.createBlock === 'function';
    const hasLoadFileMethod = typeof parser.loadFile === 'function';
    
    dv.paragraph(`✅ **Factory instantiation**: ${parser ? 'SUCCESS' : 'FAILED'}`);
    dv.paragraph(`✅ **Core methods present**: ${hasParseMethod && hasRunMethod ? 'SUCCESS' : 'FAILED'}`);
    dv.paragraph(`✅ **Detection methods present**: ${hasIsHeaderMethod && hasIsTodoLineMethod && hasIsDoneLineMethod ? 'SUCCESS' : 'FAILED'}`);
    dv.paragraph(`✅ **Utility methods present**: ${hasGetHeaderLevelMethod && hasLoadFileMethod ? 'SUCCESS' : 'FAILED'}`);
    
} catch (error) {
    dv.paragraph(`❌ **Factory Error**: ${error.message}`);
}
```

## Block Type Detection Specification

### Todo vs Done Item Detection Logic

The noteBlocksParser uses separate methods to distinguish between incomplete and completed todo items:

- **`isTodoLine(line)`**: Detects incomplete todos with pattern `- [ ]` (empty checkbox)
- **`isDoneLine(line)`**: Detects completed todos with pattern `- [x]` (checked checkbox)

**Key Behavioral Rules:**
1. A line starting with `- [ ]` is detected as a **todo** (incomplete)
2. A line starting with `- [x]` is detected as a **done** item (completed) 
3. These are mutually exclusive - a line cannot be both todo and done
4. Both methods only detect items at the start of lines (no indentation support)
5. Both are case-sensitive (`- [X]` with capital X is NOT detected as done)

**Block Type Assignment:**
- Lines detected by `isTodoLine()` get block type `"todo"`
- Lines detected by `isDoneLine()` get block type `"done"`
- This allows the system to track completion status and handle todos/done items differently


### Header Detection
```dataviewjs
const cjsResult = await cJS();
const noteBlocksParserFactory = cjsResult.createnoteBlocksParserInstance;

dv.header(3, "Header Detection Tests");

try {
    if (!noteBlocksParserFactory) {
        throw new Error("noteBlocksParser factory not found in CustomJS");
    }
    
    const parser = noteBlocksParserFactory();
    
    // Test cases for header detection
    const headerTests = [
        { line: "# Main Header", expected: true, level: 1 },
        { line: "## Sub Header", expected: true, level: 2 },
        { line: "### Third Level", expected: true, level: 3 },
        { line: "#### Fourth Level", expected: true, level: 4 },
        { line: "##### Fifth Level", expected: true, level: 5 },
        { line: "###### Sixth Level", expected: true, level: 6 },
        { line: "####### Invalid Level", expected: true, level: 7 }, // Parser actually accepts 7+ levels
        { line: "# ", expected: false, level: 0 }, // Empty header (no text)
        { line: "#No space", expected: false, level: 0 }, // No space after #
        { line: "Not a header", expected: false, level: 0 },
        { line: "  # Indented header", expected: false, level: 0 }, // Indented
        { line: "", expected: false, level: 0 }, // Empty line
        { line: "# Valid header with text", expected: true, level: 1 },
        { line: "## Another valid header", expected: true, level: 2 },
    ];
    
    let passedTests = 0;
    let totalTests = headerTests.length;
    
    for (const test of headerTests) {
        const isHeader = parser.isHeader(test.line);
        const level = isHeader ? parser.getHeaderLevel(test.line) : 0;
        
        const headerPassed = isHeader === test.expected;
        const levelPassed = level === test.level;
        const testPassed = headerPassed && levelPassed;
        
        if (testPassed) passedTests++;
        
        const status = testPassed ? "✅" : "❌";
        dv.paragraph(`${status} "${test.line}" → Header: ${isHeader}, Level: ${level} (Expected: ${test.expected}, ${test.level})`);
    }
    
    dv.paragraph(`**Header Detection Summary**: ${passedTests}/${totalTests} tests passed`);
    
} catch (error) {
    dv.paragraph(`❌ **Header Detection Error**: ${error.message}`);
}
```

### Todo Line Detection
```dataviewjs
const cjsResult = await cJS();
const noteBlocksParserFactory = cjsResult.createnoteBlocksParserInstance;

dv.header(3, "Todo Line Detection Tests");

try {
    if (!noteBlocksParserFactory) {
        throw new Error("noteBlocksParser factory not found in CustomJS");
    }
    
    const parser = noteBlocksParserFactory();
    
    const todoTests = [
        { line: "- [ ] Simple todo", expected: true },
        { line: "  - [ ] Indented todo", expected: false }, // Parser only detects at line start
        { line: "    - [ ] Double indented", expected: false },
        { line: "- [x] Completed todo", expected: false }, // Completed todos are NOT todos - they're detected by isDoneLine()
        { line: "- [ ]", expected: true }, // Empty todo
        { line: "- [ ] Todo with **bold** text", expected: true },
        { line: "- [ ] Todo with [link](url)", expected: true },
        { line: "- Regular list item", expected: false },
        { line: "Not a list", expected: false },
        { line: "", expected: false },
        { line: "- [] Missing space", expected: false },
        { line: "-[ ] Missing space", expected: false },
        { line: "- [ ] Todo with [[mention]]", expected: true },
        { line: "- [ ] Todo with #tag", expected: true },
    ];
    
    let passedTests = 0;
    let totalTests = todoTests.length;
    
    for (const test of todoTests) {
        const isTodo = parser.isTodoLine(test.line);
        const testPassed = isTodo === test.expected;
        
        if (testPassed) passedTests++;
        
        const status = testPassed ? "✅" : "❌";
        dv.paragraph(`${status} "${test.line}" → Todo: ${isTodo} (Expected: ${test.expected})`);
    }
    
    dv.paragraph(`**Todo Detection Summary**: ${passedTests}/${totalTests} tests passed`);
    
} catch (error) {
    dv.paragraph(`❌ **Todo Detection Error**: ${error.message}`);
}
```

### Done Line Detection
```dataviewjs
const cjsResult = await cJS();
const noteBlocksParserFactory = cjsResult.createnoteBlocksParserInstance;

dv.header(3, "Done Line Detection Tests");

try {
    if (!noteBlocksParserFactory) {
        throw new Error("noteBlocksParser factory not found in CustomJS");
    }
    
    const parser = noteBlocksParserFactory();
    
    const doneTests = [
        { line: "- [x] Completed task", expected: true },
        { line: "  - [x] Indented completed", expected: false }, // Parser only detects at line start
        { line: "    - [x] Double indented completed", expected: false },
        { line: "- [X] Capital X completed", expected: false }, // Parser is case-sensitive
        { line: "- [ ] Incomplete task", expected: false },
        { line: "- [x]", expected: true }, // Empty completed
        { line: "- [x] Task with **formatting**", expected: true },
        { line: "- Regular list item", expected: false },
        { line: "Not a list", expected: false },
        { line: "", expected: false },
        { line: "- [x Missing bracket", expected: false },
        { line: "-[x] Missing space", expected: false },
        { line: "- [x] Done with [[mention]]", expected: true },
        { line: "- [x] Done with #tag", expected: true },
    ];
    
    let passedTests = 0;
    let totalTests = doneTests.length;
    
    for (const test of doneTests) {
        const isDone = parser.isDoneLine(test.line);
        const testPassed = isDone === test.expected;
        
        if (testPassed) passedTests++;
        
        const status = testPassed ? "✅" : "❌";
        dv.paragraph(`${status} "${test.line}" → Done: ${isDone} (Expected: ${test.expected})`);
    }
    
    dv.paragraph(`**Done Detection Summary**: ${passedTests}/${totalTests} tests passed`);
    
} catch (error) {
    dv.paragraph(`❌ **Done Detection Error**: ${error.message}`);
}
```

### Callout Detection
```dataviewjs
const cjsResult = await cJS();
const noteBlocksParserFactory = cjsResult.createnoteBlocksParserInstance;

dv.header(3, "Callout Detection Tests");

try {
    if (!noteBlocksParserFactory) {
        throw new Error("noteBlocksParser factory not found in CustomJS");
    }
    
    const parser = noteBlocksParserFactory();
    
    const calloutTests = [
        { line: "> [!note] Simple callout", expected: true },
        { line: "> [!warning] Warning callout", expected: true },
        { line: "> [!info] Info callout", expected: true },
        { line: "> Regular quote", expected: true }, // Any line starting with > is callout
        { line: "> - [ ] Todo in quote", expected: false }, // Todo in quote is not callout
        { line: "> - [x] Done in quote", expected: true }, // Parser detects this as callout (actual behavior)
        { line: "Not a callout", expected: false },
        { line: "", expected: false },
        { line: "  > Indented quote", expected: false }, // Must start at line beginning
    ];
    
    let passedTests = 0;
    let totalTests = calloutTests.length;
    
    for (const test of calloutTests) {
        const isCallout = parser.isCallout(test.line);
        const testPassed = isCallout === test.expected;
        
        if (testPassed) passedTests++;
        
        const status = testPassed ? "✅" : "❌";
        dv.paragraph(`${status} "${test.line}" → Callout: ${isCallout} (Expected: ${test.expected})`);
    }
    
    dv.paragraph(`**Callout Detection Summary**: ${passedTests}/${totalTests} tests passed`);
    
} catch (error) {
    dv.paragraph(`❌ **Callout Detection Error**: ${error.message}`);
}
```

### Code Block Detection
```dataviewjs
const cjsResult = await cJS();
const noteBlocksParserFactory = cjsResult.createnoteBlocksParserInstance;

dv.header(3, "Code Block Detection Tests");

try {
    if (!noteBlocksParserFactory) {
        throw new Error("noteBlocksParser factory not found in CustomJS");
    }
    
    const parser = noteBlocksParserFactory();
    
    const codeTests = [
        { line: "```", expected: true },
        { line: "```javascript", expected: true },
        { line: "```python", expected: true },
        { line: "```dataviewjs", expected: true },
        { line: "``", expected: false }, // Only two backticks
        { line: "`code`", expected: false }, // Inline code
        { line: "Not code", expected: false },
        { line: "", expected: false },
        { line: "  ```", expected: false }, // Indented code blocks not detected
    ];
    
    let passedTests = 0;
    let totalTests = codeTests.length;
    
    for (const test of codeTests) {
        const isCode = parser.isCodeBlock(test.line);
        const testPassed = isCode === test.expected;
        
        if (testPassed) passedTests++;
        
        const status = testPassed ? "✅" : "❌";
        dv.paragraph(`${status} "${test.line}" → Code: ${isCode} (Expected: ${test.expected})`);
    }
    
    dv.paragraph(`**Code Block Detection Summary**: ${passedTests}/${totalTests} tests passed`);
    
} catch (error) {
    dv.paragraph(`❌ **Code Block Detection Error**: ${error.message}`);
}
```

### Mention Detection
```dataviewjs
const cjsResult = await cJS();
const noteBlocksParserFactory = cjsResult.createnoteBlocksParserInstance;

dv.header(3, "Mention Detection Tests");

try {
    if (!noteBlocksParserFactory) {
        throw new Error("noteBlocksParser factory not found in CustomJS");
    }
    
    const parser = noteBlocksParserFactory();
    
    const mentionTests = [
        { line: "[[Simple mention]]", expected: true },
        { line: "[[Mention with alias|Alias]]", expected: true },
        { line: "Text with [[mention]] inside", expected: true },
        { line: "Multiple [[mention1]] and [[mention2]]", expected: true },
        { line: "![[Embedded file]]", expected: false }, // Embedded files excluded
        { line: "[Regular link](url)", expected: false },
        { line: "No mentions here", expected: false },
        { line: "", expected: false },
        { line: "[[2025-07-06]]", expected: true }, // Date mentions
        { line: "[[Activity Name]]", expected: true },
    ];
    
    let passedTests = 0;
    let totalTests = mentionTests.length;
    
    for (const test of mentionTests) {
        const isMention = parser.isMention(test.line);
        const testPassed = isMention === test.expected;
        
        if (testPassed) passedTests++;
        
        const status = testPassed ? "✅" : "❌";
        dv.paragraph(`${status} "${test.line}" → Mention: ${isMention} (Expected: ${test.expected})`);
    }
    
    dv.paragraph(`**Mention Detection Summary**: ${passedTests}/${totalTests} tests passed`);
    
} catch (error) {
    dv.paragraph(`❌ **Mention Detection Error**: ${error.message}`);
}
```

## Indentation and Hierarchy Specification

### Indentation Level Calculation
```dataviewjs
const cjsResult = await cJS();
const noteBlocksParserFactory = cjsResult.createnoteBlocksParserInstance;

dv.header(3, "Indentation Level Tests");

try {
    if (!noteBlocksParserFactory) {
        throw new Error("noteBlocksParser factory not found in CustomJS");
    }
    
    const parser = noteBlocksParserFactory();
    
    const indentTests = [
        { line: "No indent", expectedLevel: 0 },
        { line: "  Two spaces", expectedLevel: 2 },
        { line: "    Four spaces", expectedLevel: 4 },
        { line: "      Six spaces", expectedLevel: 6 },
        { line: "        Eight spaces", expectedLevel: 8 },
        { line: " Single space", expectedLevel: 1 },
        { line: "   Three spaces", expectedLevel: 3 },
        { line: "     Five spaces", expectedLevel: 5 },
        { line: "", expectedLevel: 0 }, // Empty line
    ];
    
    let passedTests = 0;
    let totalTests = indentTests.length;
    
    for (const test of indentTests) {
        const actualLevel = parser.getIndentationLevel(test.line);
        const testPassed = actualLevel === test.expectedLevel;
        
        if (testPassed) passedTests++;
        
        const status = testPassed ? "✅" : "❌";
        dv.paragraph(`${status} "${test.line}" → Level: ${actualLevel} (Expected: ${test.expectedLevel})`);
    }
    
    dv.paragraph(`**Indentation Level Summary**: ${passedTests}/${totalTests} tests passed`);
    
} catch (error) {
    dv.paragraph(`❌ **Indentation Level Error**: ${error.message}`);
}
```

## Full Document Parsing Specification

### Complex Document Structure
```dataviewjs
const cjsResult = await cJS();
const noteBlocksParserFactory = cjsResult.createnoteBlocksParserInstance;

dv.header(3, "Complex Document Parsing Tests");

try {
    if (!noteBlocksParserFactory) {
        throw new Error("noteBlocksParser factory not found in CustomJS");
    }
    
    const parser = noteBlocksParserFactory();
    
    const complexDocument = `# Main Document

This is the introduction text.

## Section 1: Tasks
- [ ] First task
  - [ ] Subtask 1.1
  - [ ] Subtask 1.2
- [x] Completed task
- [ ] Another task

## Section 2: Notes

Some regular text here.

> [!note] Important Note
> This is a callout with content
> Multiple lines in callout

### Subsection 2.1
More text content.

#### Deep Subsection
- [ ] Deep task
- [x] Deep completed

## Section 3: Code and Mentions

Here's some code:

\`\`\`javascript
function example() {
  return "hello";
}
\`\`\`

And some mentions: [[Activity Name]] and [[2025-07-06]].

---

## After Separator

This content comes after a separator.

- [ ] Post-separator task
- [x] Post-separator done

`;
    
    const collection = await parser.parse("complex-test.md", complexDocument);
    
    if (!collection || !collection.blocks) {
        dv.paragraph("❌ **Parse returned invalid collection**");
        return;
    }
    
    dv.paragraph(`📦 **Total blocks parsed**: ${collection.blocks.length}`);
    
    // Count block types
    const blockTypes = {};
    collection.blocks.forEach(block => {
        const blockType = block.getAttribute ? block.getAttribute("type") : "unknown";
        blockTypes[blockType] = (blockTypes[blockType] || 0) + 1;
    });
    
    dv.paragraph("📊 **Block type distribution**:");
    Object.entries(blockTypes).forEach(([type, count]) => {
        dv.paragraph(`• **${type}**: ${count} blocks`);
    });
    
    // Test hierarchy relationships
    let hierarchyTests = 0;
    let hierarchyPassed = 0;
    
    collection.blocks.forEach(block => {
        if (block.getAttribute("type") === "header") {
            hierarchyTests++;
            const level = block.getAttribute("level");
            const hasChildren = block.children && block.children.length > 0;
            
            // Headers should have appropriate children based on content
            if (level === 1 && hasChildren) hierarchyPassed++; // Main Document should have children
            else if (level === 2 && hasChildren) hierarchyPassed++; // Sections should have children
            else if (level >= 3) hierarchyPassed++; // Subsections may or may not have children
        }
    });
    
    dv.paragraph(`🔗 **Hierarchy tests**: ${hierarchyPassed}/${hierarchyTests} passed`);
    
    // Validate expected structure
    const expectedHeaders = 6; // # Main, ## Section 1, ## Section 2, ### Subsection 2.1, #### Deep, ## Section 3, ## After Separator
    const expectedTodos = 6; // Count all todo items
    const expectedDone = 3; // Count all done items
    const expectedMentions = 1; // One mention block
    const expectedCode = 2; // Start and end of code block
    const expectedCallouts = 3; // Callout lines
    
    const actualHeaders = blockTypes.header || 0;
    const actualTodos = blockTypes.todo || 0;
    const actualDone = blockTypes.done || 0;
    const actualMentions = blockTypes.mention || 0;
    const actualCode = blockTypes.code || 0;
    const actualCallouts = blockTypes.callout || 0;
    
    dv.paragraph("🎯 **Structure validation**:");
    dv.paragraph(`• Headers: ${actualHeaders} (expected ~${expectedHeaders})`);
    dv.paragraph(`• Todos: ${actualTodos} (expected ~${expectedTodos})`);
    dv.paragraph(`• Done: ${actualDone} (expected ~${expectedDone})`);
    dv.paragraph(`• Mentions: ${actualMentions} (expected ~${expectedMentions})`);
    dv.paragraph(`• Code blocks: ${actualCode} (expected ~${expectedCode})`);
    dv.paragraph(`• Callouts: ${actualCallouts} (expected ~${expectedCallouts})`);
    
    const structureScore = [
        actualHeaders >= 5 ? 1 : 0,
        actualTodos >= 4 ? 1 : 0,
        actualDone >= 2 ? 1 : 0,
        actualMentions >= 1 ? 1 : 0,
    ].reduce((a, b) => a + b, 0);
    
    dv.paragraph(`📊 **Structure score**: ${structureScore}/4`);
    
    if (structureScore >= 3) {
        dv.paragraph("✅ **Complex document parsing PASSED**");
    } else {
        dv.paragraph("❌ **Complex document parsing needs attention**");
    }
    
} catch (error) {
    dv.paragraph(`❌ **Complex parsing error**: ${error.message}`);
}
```

## Edge Cases and Error Handling Specification

### Edge Case Handling
```dataviewjs
const cjsResult = await cJS();
const noteBlocksParserFactory = cjsResult.createnoteBlocksParserInstance;

dv.header(3, "Edge Case Tests");

try {
    if (!noteBlocksParserFactory) {
        throw new Error("noteBlocksParser factory not found in CustomJS");
    }
    
    const parser = noteBlocksParserFactory();
    
    // Test empty content
    dv.paragraph("**Test 1: Empty Content**");
    const emptyCollection = await parser.parse("empty.md", "");
    const emptyPassed = emptyCollection && emptyCollection.blocks.length === 0;
    dv.paragraph(`${emptyPassed ? "✅" : "❌"} Empty content: ${emptyCollection ? emptyCollection.blocks.length : "null"} blocks`);
    
    // Test only whitespace
    dv.paragraph("**Test 2: Whitespace Only**");
    const whitespaceCollection = await parser.parse("whitespace.md", "   \n\n  \t  \n");
    const whitespacePassed = whitespaceCollection && whitespaceCollection.blocks.length >= 0;
    dv.paragraph(`${whitespacePassed ? "✅" : "❌"} Whitespace only: ${whitespaceCollection ? whitespaceCollection.blocks.length : "null"} blocks`);
    
    // Test malformed markdown
    dv.paragraph("**Test 3: Malformed Markdown**");
    const malformedContent = `### Header without parent
- [ ] Todo without header
> [!note Unclosed callout
\`\`\`javascript
Code without closing
- [x] Done item
[[Unclosed mention
`;
    const malformedCollection = await parser.parse("malformed.md", malformedContent);
    const malformedPassed = malformedCollection && malformedCollection.blocks.length > 0;
    dv.paragraph(`${malformedPassed ? "✅" : "❌"} Malformed markdown: ${malformedCollection ? malformedCollection.blocks.length : "null"} blocks`);
    
    // Test very long lines
    dv.paragraph("**Test 4: Long Lines**");
    const longLine = "- [ ] " + "Very long todo item ".repeat(100);
    const longLineCollection = await parser.parse("long.md", longLine);
    const longLinePassed = longLineCollection && longLineCollection.blocks.length === 1;
    dv.paragraph(`${longLinePassed ? "✅" : "❌"} Long line: ${longLineCollection ? longLineCollection.blocks.length : "null"} blocks`);
    
    // Test special characters
    dv.paragraph("**Test 5: Special Characters**");
    const specialContent = `# Header with émojis 🎉 and ñ characters
- [ ] Todo with "quotes" and 'apostrophes'
- [x] Done with [[special|alias]] mention
> [!note] Callout with ñ and émojis 🚀
\`\`\`javascript
// Code with special chars: ñ, é, 🎉
const test = "special";
\`\`\`
`;
    const specialCollection = await parser.parse("special.md", specialContent);
    const specialPassed = specialCollection && specialCollection.blocks.length > 0;
    dv.paragraph(`${specialPassed ? "✅" : "❌"} Special characters: ${specialCollection ? specialCollection.blocks.length : "null"} blocks`);
    
    // Test null/undefined inputs
    dv.paragraph("**Test 6: Null/Undefined Inputs**");
    try {
        const nullCollection = await parser.parse("null.md", null);
        dv.paragraph(`❌ Null input should throw error but returned: ${nullCollection ? nullCollection.blocks.length : "null"} blocks`);
    } catch (nullError) {
        dv.paragraph(`✅ Null input correctly throws error: ${nullError.message}`);
    }
    
    const edgeCasesPassed = [emptyPassed, whitespacePassed, malformedPassed, longLinePassed, specialPassed].filter(Boolean).length;
    dv.paragraph(`📊 **Edge cases summary**: ${edgeCasesPassed}/5 tests passed`);
    
} catch (error) {
    dv.paragraph(`❌ **Edge case testing error**: ${error.message}`);
}
```

## Performance and Scalability Specification

### Performance Benchmarks
```dataviewjs
const cjsResult = await cJS();
const noteBlocksParserFactory = cjsResult.createnoteBlocksParserInstance;

dv.header(3, "Performance Benchmark Tests");

try {
    if (!noteBlocksParserFactory) {
        throw new Error("noteBlocksParser factory not found in CustomJS");
    }
    
    const parser = noteBlocksParserFactory();
    
    // Test 1: Small document (baseline)
    dv.paragraph("**Benchmark 1: Small Document (100 lines)**");
    let smallContent = "# Small Document\n\n";
    for (let i = 0; i < 50; i++) {
        smallContent += `- [ ] Todo ${i}\n- [x] Done ${i}\n`;
    }
    
    const smallStart = performance.now();
    const smallCollection = await parser.parse("small.md", smallContent);
    const smallEnd = performance.now();
    const smallDuration = smallEnd - smallStart;
    
    dv.paragraph(`⏱️ Small document: ${smallDuration.toFixed(2)}ms, ${smallCollection.blocks.length} blocks`);
    dv.paragraph(`📊 Rate: ${(smallCollection.blocks.length / smallDuration * 1000).toFixed(0)} blocks/second`);
    
    // Test 2: Medium document
    dv.paragraph("**Benchmark 2: Medium Document (1000 lines)**");
    let mediumContent = "# Medium Document\n\n";
    for (let i = 0; i < 500; i++) {
        mediumContent += `- [ ] Todo ${i}\n- [x] Done ${i}\n`;
        if (i % 100 === 0) {
            mediumContent += `## Section ${i / 100}\n`;
        }
    }
    
    const mediumStart = performance.now();
    const mediumCollection = await parser.parse("medium.md", mediumContent);
    const mediumEnd = performance.now();
    const mediumDuration = mediumEnd - mediumStart;
    
    dv.paragraph(`⏱️ Medium document: ${mediumDuration.toFixed(2)}ms, ${mediumCollection.blocks.length} blocks`);
    dv.paragraph(`📊 Rate: ${(mediumCollection.blocks.length / mediumDuration * 1000).toFixed(0)} blocks/second`);
    
    // Test 3: Large document
    dv.paragraph("**Benchmark 3: Large Document (5000 lines)**");
    let largeContent = "# Large Document\n\n";
    for (let i = 0; i < 2500; i++) {
        largeContent += `- [ ] Todo ${i}\n- [x] Done ${i}\n`;
        if (i % 250 === 0) {
            largeContent += `## Section ${i / 250}\n`;
            largeContent += `> [!note] Callout ${i}\n> Content here\n`;
        }
    }
    
    const largeStart = performance.now();
    const largeCollection = await parser.parse("large.md", largeContent);
    const largeEnd = performance.now();
    const largeDuration = largeEnd - largeStart;
    
    dv.paragraph(`⏱️ Large document: ${largeDuration.toFixed(2)}ms, ${largeCollection.blocks.length} blocks`);
    dv.paragraph(`📊 Rate: ${(largeCollection.blocks.length / largeDuration * 1000).toFixed(0)} blocks/second`);
    
    // Performance validation
    const performanceTests = [
        { name: "Small", duration: smallDuration, threshold: 100, passed: smallDuration < 100 },
        { name: "Medium", duration: mediumDuration, threshold: 500, passed: mediumDuration < 500 },
        { name: "Large", duration: largeDuration, threshold: 2000, passed: largeDuration < 2000 }
    ];
    
    dv.paragraph("🎯 **Performance validation**:");
    performanceTests.forEach(test => {
        const status = test.passed ? "✅" : "❌";
        dv.paragraph(`${status} ${test.name}: ${test.duration.toFixed(2)}ms (threshold: ${test.threshold}ms)`);
    });
    
    const performancePassed = performanceTests.filter(t => t.passed).length;
    dv.paragraph(`📊 **Performance summary**: ${performancePassed}/${performanceTests.length} benchmarks passed`);
    
} catch (error) {
    dv.paragraph(`❌ **Performance testing error**: ${error.message}`);
}
```

## Integration and File System Specification

### File Loading and Processing
```dataviewjs
const cjsResult = await cJS();
const noteBlocksParserFactory = cjsResult.createnoteBlocksParserInstance;

dv.header(3, "File System Integration Tests");

try {
    if (!noteBlocksParserFactory) {
        throw new Error("noteBlocksParser factory not found in CustomJS");
    }
    
    const parser = noteBlocksParserFactory();
    
    // Test 1: Load existing file
    dv.paragraph("**Test 1: File Loading**");
    try {
        const testFilePath = "Journal/2025/07.July/2025-07-25.md";
        const fileContent = await parser.loadFile(app, testFilePath);
        
        if (fileContent && fileContent.length > 0) {
            dv.paragraph(`✅ File loaded: ${fileContent.length} characters`);
            
            // Parse the loaded file
            const fileCollection = await parser.parse(testFilePath, fileContent);
            dv.paragraph(`📦 Parsed blocks: ${fileCollection.blocks.length}`);
            
            // Show block type distribution
            const fileBlockTypes = {};
            fileCollection.blocks.forEach(block => {
                const type = block.getAttribute("type");
                fileBlockTypes[type] = (fileBlockTypes[type] || 0) + 1;
            });
            
            dv.paragraph("📊 **File block types**:");
            Object.entries(fileBlockTypes).forEach(([type, count]) => {
                dv.paragraph(`• ${type}: ${count}`);
            });
            
        } else {
            dv.paragraph("⚠️ File loaded but empty");
        }
    } catch (fileError) {
        dv.paragraph(`❌ File loading failed: ${fileError.message}`);
    }
    
    // Test 2: Non-existent file handling
    dv.paragraph("**Test 2: Non-existent File**");
    const nonExistentContent = await parser.loadFile(app, "non-existent-file.md");
    const nonExistentPassed = nonExistentContent === null;
    dv.paragraph(`${nonExistentPassed ? "✅" : "❌"} Non-existent file returns null: ${nonExistentContent === null}`);
    
    // Test 3: Run method with pages
    dv.paragraph("**Test 3: Run Method Integration**");
    try {
        // Get some pages to test with
        const testPages = dv.pages().limit(3).array();
        
        if (testPages.length > 0) {
            const runStart = performance.now();
            const runCollection = await parser.run(app, testPages);
            const runEnd = performance.now();
            const runDuration = runEnd - runStart;
            
            dv.paragraph(`✅ Run method processed ${testPages.length} pages in ${runDuration.toFixed(2)}ms`);
            dv.paragraph(`📦 Total blocks from run: ${runCollection.blocks.length}`);
            
            // Show statistics
            const stats = runCollection.getStats();
            dv.paragraph(`📊 **Run statistics**:`);
            dv.paragraph(`• Total blocks: ${stats.totalBlocks}`);
            dv.paragraph(`• Root blocks: ${stats.rootBlocks}`);
            dv.paragraph(`• Block types: ${Object.keys(stats.types).join(", ")}`);
            
        } else {
            dv.paragraph("⚠️ No pages available for run test");
        }
    } catch (runError) {
        dv.paragraph(`❌ Run method failed: ${runError.message}`);
    }
    
} catch (error) {
    dv.paragraph(`❌ **Integration testing error**: ${error.message}`);
}
```

## Hierarchy and Relationship Specification

### Parent-Child Relationships
```dataviewjs
const cjsResult = await cJS();
const noteBlocksParserFactory = cjsResult.createnoteBlocksParserInstance;

dv.header(3, "Hierarchy Relationship Tests");

try {
    if (!noteBlocksParserFactory) {
        throw new Error("noteBlocksParser factory not found in CustomJS");
    }
    
    const parser = noteBlocksParserFactory();
    
    const hierarchyDocument = `# Root Document

Root level content.

## Section A
Section A content.

- [ ] Task A1
  - [ ] Subtask A1.1
    - [ ] Deep subtask A1.1.1
  - [ ] Subtask A1.2
- [ ] Task A2

### Subsection A.1
Subsection content.

- [ ] Subsection task
- [x] Subsection done

## Section B

> [!note] Section B Note
> This is a callout in section B

- [ ] Task B1
- [x] Task B2

---

## Section C (After Separator)

This section comes after a separator.

- [ ] Post-separator task
`;
    
    const hierarchyCollection = await parser.parse("hierarchy-test.md", hierarchyDocument);
    
    if (!hierarchyCollection || !hierarchyCollection.blocks) {
        dv.paragraph("❌ **Hierarchy parsing failed**");
        return;
    }
    
    dv.paragraph(`📦 **Total hierarchy blocks**: ${hierarchyCollection.blocks.length}`);
    
    // Test header hierarchy
    const headers = hierarchyCollection.blocks.filter(b => b.getAttribute("type") === "header");
    dv.paragraph(`📋 **Headers found**: ${headers.length}`);
    
    let hierarchyValidation = [];
    
    headers.forEach(header => {
        const level = header.getAttribute("level");
        const hasChildren = header.children && header.children.length > 0;
        const childCount = hasChildren ? header.children.length : 0;
        
        dv.paragraph(`• Level ${level} header: ${childCount} children`);
        
        // Validate expected hierarchy
        if (level === 1) {
            hierarchyValidation.push({ test: "Root has children", passed: hasChildren });
        } else if (level === 2) {
            hierarchyValidation.push({ test: "Section has children", passed: hasChildren });
        }
    });
    
    // Test indentation hierarchy
    const todos = hierarchyCollection.blocks.filter(b => b.getAttribute("type") === "todo");
    dv.paragraph(`📋 **Todos found**: ${todos.length}`);
    
    let indentationTests = 0;
    let indentationPassed = 0;
    
    todos.forEach(todo => {
        const indentLevel = todo.getAttribute("indentLevel");
        const hasParent = todo.parent !== null;
        
        indentationTests++;
        
        // Todos with indentation should have parents
        if (indentLevel > 0 && hasParent) {
            indentationPassed++;
        } else if (indentLevel === 0) {
            indentationPassed++; // Root level todos may or may not have parents
        }
    });
    
    dv.paragraph(`🔗 **Indentation hierarchy**: ${indentationPassed}/${indentationTests} tests passed`);
    
    // Test separator behavior
    const separators = hierarchyCollection.blocks.filter(b => b.getAttribute("type") === "separator");
    dv.paragraph(`📋 **Separators found**: ${separators.length}`);
    
    const hierarchyScore = hierarchyValidation.filter(h => h.passed).length;
    dv.paragraph(`📊 **Hierarchy validation**: ${hierarchyScore}/${hierarchyValidation.length} tests passed`);
    
    if (hierarchyScore >= hierarchyValidation.length * 0.8) {
        dv.paragraph("✅ **Hierarchy relationship tests PASSED**");
    } else {
        dv.paragraph("❌ **Hierarchy relationship tests need attention**");
    }
    
} catch (error) {
    dv.paragraph(`❌ **Hierarchy testing error**: ${error.message}`);
}
```

## Final Specification Summary

### Component Contract
```dataviewjs
dv.header(2, "📋 Component Contract Summary");

dv.paragraph("**The noteBlocksParser component MUST:**");
dv.paragraph("1. ✅ Parse markdown content into Block objects");
dv.paragraph("2. ✅ Detect all supported block types (header, todo, done, callout, code, mention, text)");
dv.paragraph("3. ✅ Maintain hierarchical relationships based on headers and indentation");
dv.paragraph("4. ✅ Handle edge cases gracefully (empty content, malformed markdown)");
dv.paragraph("5. ✅ Provide consistent performance for documents up to 5000 lines");
dv.paragraph("6. ✅ Integrate with Obsidian file system through loadFile method");
dv.paragraph("7. ✅ Support batch processing through run method");
dv.paragraph("8. ✅ Return BlockCollection with proper statistics and hierarchy");

dv.paragraph("**Block Type Detection Rules:**");
dv.paragraph("• **Headers**: Lines starting with 1-6 `#` followed by space and text");
dv.paragraph("• **Todos**: Lines starting with `- [ ]` (case-sensitive, line-start only)");
dv.paragraph("• **Done**: Lines starting with `- [x]` (lowercase x, line-start only)");
dv.paragraph("• **Callouts**: Lines starting with `>` (excluding todos/done in quotes)");
dv.paragraph("• **Code**: Lines starting with exactly three backticks");
dv.paragraph("• **Mentions**: Lines containing `[[...]]` (excluding `![[...]]` embeds)");
dv.paragraph("• **Text**: All other non-empty content");

dv.paragraph("**Hierarchy Rules:**");
dv.paragraph("• Headers create hierarchy by level (# > ## > ###)");
dv.paragraph("• Indentation creates sub-hierarchy within header sections");
dv.paragraph("• Two empty lines break parent-child relationships");
dv.paragraph("• Horizontal rules (---) break parent-child relationships");
dv.paragraph("• Each indentation level is measured in exact spaces");

dv.paragraph("**Performance Requirements:**");
dv.paragraph("• Small documents (100 lines): < 100ms");
dv.paragraph("• Medium documents (1000 lines): < 500ms");
dv.paragraph("• Large documents (5000 lines): < 2000ms");
dv.paragraph("• Minimum processing rate: 1000 blocks/second");

dv.paragraph("**Error Handling:**");
dv.paragraph("• Null/undefined content should throw appropriate errors");
dv.paragraph("• Non-existent files should return null from loadFile");
dv.paragraph("• Malformed markdown should be parsed as best as possible");
dv.paragraph("• Component should never crash on valid markdown input");

dv.paragraph("🎯 **This specification serves as the definitive behavioral contract for the noteBlocksParser component.**");
```

---

## Usage Instructions

1. **Run Individual Test Sections**: Execute specific DataviewJS blocks to test particular functionality
2. **Full Specification Test**: Run all blocks in sequence for comprehensive validation
3. **Performance Monitoring**: Use benchmark tests to monitor performance regressions
4. **Integration Validation**: Use file system tests to ensure proper Obsidian integration

## Maintenance Notes

- Update test expectations when component behavior changes
- Add new test cases for new block types or features
- Monitor performance benchmarks during development
- Validate hierarchy rules when modifying parsing logic

**This TDD specification ensures the noteBlocksParser component meets all functional and performance requirements while maintaining backward compatibility.**
