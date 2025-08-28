# Simple CustomJS Test

This page tests if CustomJS plugin is working correctly.

```dataviewjs
// Test CustomJS basic functionality
try {
  console.log("🧪 Testing CustomJS basic functionality...");
  
  // Try to load a simple script
  const { simpleTest } = await cJS();
  console.log("✅ CustomJS loaded simpleTest successfully");
  
  // Try different calling patterns
  console.log("simpleTest type:", typeof simpleTest);
  console.log("simpleTest:", simpleTest);
  
  // Try calling directly on the class
  let result;
  try {
    result = await simpleTest.run();
    console.log("✅ Direct class call worked:", result);
  } catch (e1) {
    console.log("❌ Direct class call failed:", e1.message);
    
    // Try creating instance
    try {
      const tester = new simpleTest();
      result = await tester.run();
      console.log("✅ Instance call worked:", result);
    } catch (e2) {
      console.log("❌ Instance call failed:", e2.message);
      throw new Error("Both calling patterns failed");
    }
  }
  console.log("✅ simpleTest.run() executed:", result);
  
  if (result.success) {
    dv.paragraph(`✅ **CustomJS is working correctly!**`);
    dv.paragraph(`Message: ${result.message}`);
  } else {
    dv.paragraph(`❌ **Simple test failed**`);
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
