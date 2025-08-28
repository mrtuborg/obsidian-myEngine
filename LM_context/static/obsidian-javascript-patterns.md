# Obsidian JavaScript Patterns - CustomJS & DataviewJS

## Important Note for Future Reference

This document captures the correct patterns for writing JavaScript in Obsidian with DataviewJS and CustomJS plugins, based on real-world testing and debugging sessions.

## CustomJS Plugin Patterns

### Script Structure
- Scripts are placed in the configured folder (e.g., `Engine/Scripts`)
- Each script is a JavaScript class
- CustomJS automatically loads all `.js` files from the configured folder

### Class Definition Pattern
```javascript
// Correct pattern - instance methods
class scriptName {
  async run() {
    // Implementation here
    return { success: true, data: "result" };
  }
}

// NOT static methods - CustomJS doesn't handle these correctly
// class scriptName {
//   static async run() { ... } // ❌ This doesn't work
// }
```

### Calling Pattern in DataviewJS
```javascript
// Load the script
const { scriptName } = await cJS();

// Robust calling pattern (handles both direct and instance calls)
let result;
try {
  // Try direct class call first
  result = await scriptName.run();
} catch (e1) {
  // Fallback to instance creation
  try {
    const instance = new scriptName();
    result = await instance.run();
  } catch (e2) {
    throw new Error("Both calling patterns failed");
  }
}
```

### Key Insights Discovered
1. **CustomJS loads classes, not instances** - you get the class constructor
2. **Calling patterns vary** - sometimes direct class calls work, sometimes you need instances
3. **No static methods** - CustomJS doesn't properly handle static class methods
4. **Robust pattern needed** - always try both calling methods for reliability

## DataviewJS Integration
- Use `dv.paragraph()` for output display
- Use `console.log()` for debugging (visible in F12 console)
- Async/await works correctly in DataviewJS blocks
- Error handling is crucial - wrap in try/catch blocks

## Template Integration
- Templates use the same CustomJS loading pattern: `const { scriptName } = await cJS();`
- Scripts are called directly on the loaded class: `await scriptName.run(app, params)`
- This suggests the template environment may handle class instantiation differently

## Testing Pattern
Always create diagnostic tests when unsure:
```javascript
// Diagnostic pattern
console.log("Script type:", typeof scriptName);
console.log("Script object:", scriptName);

// Test both patterns
try {
  result = await scriptName.run();
  console.log("✅ Direct call worked");
} catch (e) {
  console.log("❌ Direct call failed:", e.message);
  // Try instance pattern...
}
```

## Common Mistakes to Avoid
1. Using `static` methods in CustomJS scripts
2. Assuming one calling pattern works everywhere
3. Not providing fallback calling patterns
4. Forgetting error handling in DataviewJS blocks
5. Not checking console output for debugging information

## Best Practices
1. Always use instance methods in CustomJS scripts
2. Implement robust calling patterns that try both methods
3. Include comprehensive error handling and logging
4. Test scripts in isolation before integrating
5. Use diagnostic tests to understand CustomJS behavior

---

**Created during Block system implementation - August 2025**
**Context: Debugging CustomJS calling patterns for test scripts**
