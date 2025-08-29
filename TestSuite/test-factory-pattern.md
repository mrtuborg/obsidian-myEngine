# Factory Pattern Test

This test verifies that all CustomJS factory functions are working correctly after the fixes.

## Test Cases
- [x] Test simpleTest factory
- [x] Test Block factory
- [x] Test BlockCollection factory
- [x] Test noteBlocksParser factory

## DataviewJS Test Block

```dataviewjs
/**
 * Test: Factory Pattern Verification
 * Tests that all CustomJS factory functions are working correctly
 */

async function testFactoryPattern() {
  dv.header(2, "🏭 Factory Pattern Test Results");
  dv.paragraph("**Testing:** CustomJS factory function availability and functionality");
  
  try {
    // Load CustomJS modules
    const cjsResult = await cJS();
    dv.paragraph("✅ **CustomJS loaded successfully**");
    
    // Show available modules
    const availableModules = Object.keys(cjsResult);
    dv.paragraph(`📦 **Available modules:** ${availableModules.join(', ')}`);
    
    let testsPassed = 0;
    let totalTests = 0;
    
    // Test 1: simpleTest factory
    dv.header(3, "🧪 Test 1: simpleTest Factory");
    totalTests++;
    try {
      if (cjsResult.simpleTest) {
        const simpleTestResult = cjsResult.simpleTest.run();
        if (simpleTestResult && simpleTestResult.success) {
          dv.paragraph("✅ **simpleTest factory:** Working correctly");
          testsPassed++;
        } else {
          dv.paragraph("❌ **simpleTest factory:** Returned unexpected result");
        }
      } else {
        dv.paragraph("❌ **simpleTest factory:** Not found in CustomJS");
      }
    } catch (error) {
      dv.paragraph(`❌ **simpleTest factory:** Error - ${error.message}`);
    }
    
    // Test 2: Block factory
    dv.header(3, "🧪 Test 2: Block Factory");
    totalTests++;
    try {
      if (cjsResult.createBlockInstance) {
        const block = cjsResult.createBlockInstance();
        block.page = "test.md";
        block.content = "Test content";
        block.setAttribute("type", "test");
        
        if (block.getAttribute("type") === "test" && block.page === "test.md") {
          dv.paragraph("✅ **Block factory:** Working correctly");
          testsPassed++;
        } else {
          dv.paragraph("❌ **Block factory:** Block creation failed");
        }
      } else {
        dv.paragraph("❌ **Block factory:** createBlockInstance not found");
      }
    } catch (error) {
      dv.paragraph(`❌ **Block factory:** Error - ${error.message}`);
    }
    
    // Test 3: BlockCollection factory
    dv.header(3, "🧪 Test 3: BlockCollection Factory");
    totalTests++;
    try {
      if (cjsResult.createBlockCollectionInstance) {
        const collection = cjsResult.createBlockCollectionInstance();
        
        // Create a test block to add
        if (cjsResult.createBlockInstance) {
          const testBlock = cjsResult.createBlockInstance();
          testBlock.page = "test.md";
          testBlock.content = "Test block";
          testBlock.setAttribute("type", "test");
          
          collection.addBlock(testBlock);
          
          if (collection.blocks.length === 1 && collection.blocks[0] === testBlock) {
            dv.paragraph("✅ **BlockCollection factory:** Working correctly");
            testsPassed++;
          } else {
            dv.paragraph("❌ **BlockCollection factory:** Block addition failed");
          }
        } else {
          dv.paragraph("⚠️ **BlockCollection factory:** Cannot test without Block factory");
        }
      } else {
        dv.paragraph("❌ **BlockCollection factory:** createBlockCollectionInstance not found");
      }
    } catch (error) {
      dv.paragraph(`❌ **BlockCollection factory:** Error - ${error.message}`);
    }
    
    // Test 4: noteBlocksParser factory
    dv.header(3, "🧪 Test 4: noteBlocksParser Factory");
    totalTests++;
    try {
      if (cjsResult.createnoteBlocksParserInstance) {
        const parser = cjsResult.createnoteBlocksParserInstance();
        
        // Test basic parsing functionality
        const testContent = `# Test Header
- [ ] Test todo
- [x] Test done`;
        
        const result = await parser.parse("test.md", testContent);
        
        if (result && result.blocks && result.blocks.length > 0) {
          const stats = result.getStats();
          dv.paragraph(`✅ **noteBlocksParser factory:** Working correctly (parsed ${stats.totalBlocks} blocks)`);
          dv.paragraph(`📊 **Block types found:** ${Object.keys(stats.types).join(', ')}`);
          testsPassed++;
        } else {
          dv.paragraph("❌ **noteBlocksParser factory:** Parsing failed");
        }
      } else {
        dv.paragraph("❌ **noteBlocksParser factory:** createnoteBlocksParserInstance not found");
      }
    } catch (error) {
      dv.paragraph(`❌ **noteBlocksParser factory:** Error - ${error.message}`);
    }
    
    // Test Summary
    dv.header(3, "📊 Test Summary");
    const passRate = totalTests > 0 ? ((testsPassed / totalTests) * 100).toFixed(1) : 0;
    
    dv.paragraph(`📈 **Tests Passed:** ${testsPassed}/${totalTests} (${passRate}%)`);
    
    if (testsPassed === totalTests) {
      dv.paragraph("🎉 **All factory pattern tests PASSED!**");
      dv.paragraph("✅ **CustomJS integration is working correctly**");
    } else {
      dv.paragraph(`⚠️ **${totalTests - testsPassed} factory pattern test(s) failed**`);
      dv.paragraph("❌ **Some CustomJS modules need attention**");
    }
    
  } catch (error) {
    dv.paragraph(`❌ **Factory pattern test failed:** ${error.message}`);
    dv.paragraph(`**Stack trace:** ${error.stack}`);
  }
}

// Run the test
testFactoryPattern();
```

## Expected Results

### ✅ Success Indicators
- **CustomJS loads** without errors
- **All factory functions** are available in cJS() result
- **simpleTest** runs and returns success
- **Block creation** works with attributes
- **BlockCollection** can add and manage blocks
- **noteBlocksParser** can parse content and return blocks

### ❌ Failure Indicators
- CustomJS loading errors
- Missing factory functions
- Factory functions return null/undefined
- Block creation or attribute setting fails
- Collection management fails
- Parser fails to process content

## Troubleshooting

### Common Issues
1. **"cJS is not defined"**: Ensure CustomJS plugin is enabled
2. **Factory not found**: Check that the .js file is in the correct Scripts directory
3. **Module loading errors**: Verify file syntax and class definitions
4. **Permission errors**: Check file access rights

### Debug Tips
- Check browser console (F12) for detailed error messages
- Verify all .js files are in Engine/Scripts/ or Engine/Scripts/components/
- Test individual factories one by one if multiple failures occur

---

**This test validates that the factory pattern fixes resolved the TestSuite issues.**
