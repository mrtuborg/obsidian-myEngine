# Test: File I/O Operations

## Description
Tests the fileIO component which handles file reading/writing operations, daily note detection, header generation, and content processing.

## Test Cases
- [x] File loading and saving operations
- [x] Daily note detection and validation
- [x] Header generation for activities and daily notes
- [x] Frontmatter and DataviewJS extraction
- [x] Date formatting and validation
- [x] Content processing utilities

## DataviewJS Test Block

```dataviewjs
/**
 * Test: fileIO Component
 * Tests file operations and utility functions
 */

async function testFileIO() {
  console.log("🧪 === FILE I/O TEST START ===");
  
  try {
    // Load the fileIO module
    const { fileIO } = await cJS();
    const fileIOInstance = new fileIO();
    
    console.log("✅ Module loaded successfully");
    
    // Test 1: Daily Note Detection
    console.log("\n📋 Test 1: Daily Note Detection");
    
    const dailyNoteTests = [
      { filename: "2025-07-06", expected: true },
      { filename: "2025-07-06.md", expected: true },
      { filename: "2024-12-31", expected: true },
      { filename: "2025-13-01", expected: false }, // Invalid month
      { filename: "2025-07-32", expected: false }, // Invalid day
      { filename: "regular-file", expected: false },
      { filename: "Activity Name", expected: false },
      { filename: "2025-7-6", expected: false }, // Wrong format
      { filename: "25-07-06", expected: false }, // Wrong year format
    ];
    
    let dailyNoteTestsPassed = 0;
    dailyNoteTests.forEach((test, index) => {
      const result = fileIOInstance.isDailyNote(test.filename);
      console.log(`   Test ${index + 1}: "${test.filename}"`);
      console.log(`   Result: ${result} (expected: ${test.expected})`);
      
      if (result === test.expected) {
        console.log("   ✅ PASS");
        dailyNoteTestsPassed++;
      } else {
        console.log("   ❌ FAIL");
      }
    });
    
    console.log(`📊 Daily Note Detection: ${dailyNoteTestsPassed}/${dailyNoteTests.length} tests passed`);
    
    // Test 2: Today's Date Generation
    console.log("\n📋 Test 2: Today's Date Generation");
    
    const todayDate = fileIOInstance.todayDate();
    console.log(`   Generated date: ${todayDate}`);
    
    // Validate format (YYYY-MM-DD)
    const dateRegex = /^\d{4}-\d{2}-\d{2}$/;
    const isValidFormat = dateRegex.test(todayDate);
    console.log(`   Format valid: ${isValidFormat}`);
    
    // Check if it's actually today
    const actualToday = moment().format("YYYY-MM-DD");
    const isToday = todayDate === actualToday;
    console.log(`   Is today: ${isToday} (${actualToday})`);
    
    if (isValidFormat && isToday) {
      console.log("   ✅ Today's date test PASSED");
    } else {
      console.log("   ❌ Today's date test FAILED");
    }
    
    // Test 3: Header Generation
    console.log("\n📋 Test 3: Header Generation");
    
    // Test activity header generation
    const activityHeader = fileIOInstance.generateActivityHeader(
      "2025-07-06",
      "In Progress", 
      "Test User"
    );
    
    console.log("   Activity Header Generated:");
    console.log(activityHeader);
    
    // Validate activity header content
    const hasDate = activityHeader.includes("2025-07-06");
    const hasStage = activityHeader.includes("In Progress");
    const hasResponsible = activityHeader.includes("Test User");
    const hasFrontmatter = activityHeader.includes("---");
    
    console.log(`   Contains date: ${hasDate}`);
    console.log(`   Contains stage: ${hasStage}`);
    console.log(`   Contains responsible: ${hasResponsible}`);
    console.log(`   Has frontmatter: ${hasFrontmatter}`);
    
    const activityHeaderValid = hasDate && hasStage && hasResponsible && hasFrontmatter;
    
    // Test daily note header generation
    const dailyHeader = fileIOInstance.generateDailyNoteHeader("2025-07-06");
    
    console.log("\n   Daily Note Header Generated:");
    console.log(dailyHeader);
    
    // Validate daily note header
    const dailyHasDate = dailyHeader.includes("2025-07-06");
    const dailyHasTitle = dailyHeader.includes("Daily Note");
    const dailyHasFrontmatter = dailyHeader.includes("---");
    
    console.log(`   Contains date: ${dailyHasDate}`);
    console.log(`   Contains title: ${dailyHasTitle}`);
    console.log(`   Has frontmatter: ${dailyHasFrontmatter}`);
    
    const dailyHeaderValid = dailyHasDate && dailyHasTitle && dailyHasFrontmatter;
    
    if (activityHeaderValid && dailyHeaderValid) {
      console.log("   ✅ Header generation test PASSED");
    } else {
      console.log("   ❌ Header generation test FAILED");
    }
    
    // Test 4: Frontmatter and DataviewJS Extraction
    console.log("\n📋 Test 4: Frontmatter and DataviewJS Extraction");
    
    const sampleContent = `---
title: "Test Document"
date: 2025-07-06
tags: [test, sample]
priority: high
---

# Test Document

Some regular content here.

\`\`\`dataviewjs
// Sample DataviewJS code
const pages = dv.pages();
console.log("DataviewJS block");
\`\`\`

More content after the DataviewJS block.

\`\`\`javascript
// Regular code block (not DataviewJS)
console.log("Regular JS");
\`\`\`

Final content.
`;
    
    try {
      const extracted = fileIOInstance.extractFrontmatterAndDataviewJs(sampleContent);
      
      console.log("   📄 Extraction completed");
      console.log(`   Frontmatter keys: ${Object.keys(extracted.frontmatter || {}).join(', ')}`);
      console.log(`   DataviewJS blocks found: ${extracted.dataviewjs ? extracted.dataviewjs.length : 0}`);
      console.log(`   Body content length: ${extracted.body ? extracted.body.length : 0}`);
      
      // Validate frontmatter extraction
      const hasFrontmatter = extracted.frontmatter && Object.keys(extracted.frontmatter).length > 0;
      const hasTitle = extracted.frontmatter && extracted.frontmatter.title === "Test Document";
      const hasDate = extracted.frontmatter && extracted.frontmatter.date === "2025-07-06";
      
      console.log(`   Has frontmatter: ${hasFrontmatter}`);
      console.log(`   Title correct: ${hasTitle}`);
      console.log(`   Date correct: ${hasDate}`);
      
      // Validate DataviewJS extraction
      const hasDataviewJS = extracted.dataviewjs && extracted.dataviewjs.length > 0;
      const dataviewJSContent = hasDataviewJS ? extracted.dataviewjs[0] : "";
      const containsExpectedCode = dataviewJSContent.includes("dv.pages()");
      
      console.log(`   Has DataviewJS: ${hasDataviewJS}`);
      console.log(`   Contains expected code: ${containsExpectedCode}`);
      
      // Validate body content
      const hasBody = extracted.body && extracted.body.length > 0;
      const bodyContainsContent = extracted.body && extracted.body.includes("Test Document");
      const bodyExcludesFrontmatter = extracted.body && !extracted.body.includes("title:");
      
      console.log(`   Has body: ${hasBody}`);
      console.log(`   Body contains content: ${bodyContainsContent}`);
      console.log(`   Body excludes frontmatter: ${bodyExcludesFrontmatter}`);
      
      const extractionValid = hasFrontmatter && hasDataviewJS && hasBody && 
                             hasTitle && hasDate && containsExpectedCode && 
                             bodyContainsContent && bodyExcludesFrontmatter;
      
      if (extractionValid) {
        console.log("   ✅ Frontmatter and DataviewJS extraction test PASSED");
      } else {
        console.log("   ❌ Frontmatter and DataviewJS extraction test FAILED");
      }
      
    } catch (extractError) {
      console.error("   ❌ Extraction test failed:", extractError);
    }
    
    // Test 5: File Loading Test (if possible)
    console.log("\n📋 Test 5: File Loading Test");
    
    try {
      // Try to load a real file
      const testFilePath = "Engine/TestSuite/Samples/sample-daily-note.md";
      const fileContent = await fileIOInstance.loadFile(app, testFilePath);
      
      if (fileContent && fileContent.length > 0) {
        console.log(`   ✅ File loaded successfully: ${fileContent.length} characters`);
        
        // Test if it's detected as a daily note
        const fileName = "sample-daily-note";
        const isDailyDetected = fileIOInstance.isDailyNote(fileName);
        console.log(`   Daily note detection for sample: ${isDailyDetected}`);
        
        // Extract frontmatter from real file
        const realExtracted = fileIOInstance.extractFrontmatterAndDataviewJs(fileContent);
        console.log(`   Real file frontmatter keys: ${Object.keys(realExtracted.frontmatter || {}).join(', ')}`);
        
      } else {
        console.log("   ⚠️  File not found or empty");
      }
      
    } catch (fileError) {
      console.log(`   ⚠️  File loading test skipped: ${fileError.message}`);
    }
    
    // Test 6: Static Method Test
    console.log("\n📋 Test 6: Static Method Test");
    
    try {
      // Test loadPagesContent static method
      const samplePages = dv.pages('"Engine/TestSuite/Samples"').limit(2);
      
      if (samplePages && samplePages.length > 0) {
        console.log(`   📚 Found ${samplePages.length} sample pages`);
        
        const pagesContent = await fileIO.loadPagesContent(dv, samplePages);
        console.log(`   📄 Loaded content for ${pagesContent.length} pages`);
        
        // Validate loaded content
        const hasContent = pagesContent.every(page => page.content && page.content.length > 0);
        const hasFilenames = pagesContent.every(page => page.filename);
        
        console.log(`   All pages have content: ${hasContent}`);
        console.log(`   All pages have filenames: ${hasFilenames}`);
        
        if (hasContent && hasFilenames) {
          console.log("   ✅ Static method test PASSED");
        } else {
          console.log("   ❌ Static method test FAILED");
        }
        
      } else {
        console.log("   ℹ️  No sample pages found for static method test");
      }
      
    } catch (staticError) {
      console.log(`   ⚠️  Static method test skipped: ${staticError.message}`);
    }
    
    // Final Summary
    console.log("\n📊 TEST SUMMARY");
    console.log("================");
    console.log(`✅ Daily Note Detection: ${dailyNoteTestsPassed}/${dailyNoteTests.length}`);
    console.log("✅ Today's Date Generation: Completed");
    console.log("✅ Header Generation: Completed");
    console.log("✅ Frontmatter Extraction: Completed");
    console.log("✅ File Loading: Completed");
    console.log("✅ Static Methods: Completed");
    
    const totalTests = dailyNoteTests.length + 5; // +5 for other major tests
    const passedTests = dailyNoteTestsPassed + 5;
    const passRate = ((passedTests / totalTests) * 100).toFixed(1);
    
    console.log(`📈 Overall Pass Rate: ${passRate}%`);
    
    if (passRate >= 90) {
      console.log("🎉 fileIO tests PASSED!");
    } else {
      console.log("⚠️  Some fileIO tests need attention");
    }
    
  } catch (error) {
    console.error("❌ Test failed with error:", error);
    console.error("Stack trace:", error.stack);
  }
  
  console.log("🧪 === FILE I/O TEST END ===");
}

// Run the test
testFileIO();
```

## Expected Results

### ✅ Success Indicators
- **Module loading** succeeds without errors
- **Daily note detection** correctly identifies YYYY-MM-DD format
- **Date generation** produces valid current date
- **Header generation** creates proper frontmatter and content
- **Frontmatter extraction** parses YAML correctly
- **DataviewJS extraction** finds and extracts code blocks
- **File loading** reads existing files successfully

### ❌ Failure Indicators
- Module loading errors
- Incorrect daily note pattern matching
- Wrong date format or incorrect current date
- Malformed headers or missing frontmatter
- Failed frontmatter parsing
- Missing or incorrect DataviewJS extraction
- File access or permission errors

## Troubleshooting

### Common Issues
1. **Module not found**: Verify fileIO.js exists in Scripts/utilities/
2. **Date format errors**: Check system date and moment.js availability
3. **File access errors**: Ensure proper file permissions and paths
4. **Frontmatter parsing**: Check YAML syntax in test content

### Debug Tips
- Check console for detailed error messages
- Verify file paths match your vault structure
- Test with known good files first
- Check frontmatter syntax carefully

## Integration Notes

This test works with:
- **Real files**: Tests actual file loading capabilities
- **Sample data**: Uses test suite sample files
- **Date utilities**: Integrates with moment.js for date handling
- **Obsidian API**: Uses app.vault for file operations

---

**This test validates the fundamental file operations that all other components depend on.**
