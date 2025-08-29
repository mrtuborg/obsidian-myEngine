# Simple CustomJS Test

This page tests if CustomJS plugin is working correctly.

```dataviewjs
// Test CustomJS basic functionality
try {
  console.log("🧪 Testing CustomJS basic functionality...");
  
  // First, let's see what cJS() returns
  const cjsResult = await cJS();
  console.log("cJS() returned:", cjsResult);
  console.log("cJS() keys:", Object.keys(cjsResult));
  
  // Check if simpleTest is in the result
  if ('simpleTest' in cjsResult) {
    console.log("✅ simpleTest found in cJS() result");
    const { simpleTest } = cjsResult;
    console.log("simpleTest type:", typeof simpleTest);
    console.log("simpleTest:", simpleTest);
    
    if (simpleTest) {
      // Call method directly on the provided instance (CustomJS pattern)
      try {
        const result = simpleTest.run();
        console.log("✅ Direct method call worked:", result);
        
        if (result && result.success) {
          dv.paragraph(`✅ **CustomJS is working correctly!**`);
          dv.paragraph(`Message: ${result.message}`);
        } else {
          dv.paragraph(`❌ **Simple test failed - unexpected result**`);
        }
      } catch (e) {
        console.log("❌ Direct method call failed:", e.message);
        dv.paragraph(`❌ **Method call failed:** ${e.message}`);
      }
    } else {
      console.log("❌ simpleTest is null/undefined");
      dv.paragraph(`❌ **simpleTest is null/undefined**`);
    }
  } else {
    console.log("❌ simpleTest not found in cJS() result");
    dv.paragraph(`❌ **simpleTest not found in CustomJS**`);
    dv.paragraph(`Available modules: ${Object.keys(cjsResult).join(', ')}`);
  }
  
} catch (error) {
  dv.paragraph(`❌ **CustomJS Error:** ${error.message}`);
  console.error("CustomJS test error:", error);
}
```

## Instructions

1. **Open this file** in Obsidian
2. **Check the results** above
3. **Open console** (F12 → Console) for detailed output

If this works, then CustomJS is configured correctly and the issue is with the test-blocks.js script structure.
If this doesn't work, then there's a CustomJS configuration issue.
