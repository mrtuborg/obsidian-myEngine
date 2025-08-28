# Block System Test Suite

This test suite provides comprehensive testing for the new object-oriented Block system that replaces the array-based noteBlocksParser.

## 🧪 Test Files Overview

### 1. `test-basic-hierarchy.md`
**Purpose:** Tests fundamental hierarchy structure and indentation-based relationships
**Covers:**
- Basic header → child relationships
- Todo item nesting with indentation
- Multiple content types (headers, todos, callouts, code, mentions)
- Hierarchy breaks with separators (----)
- Query operations on Block objects

**How to test:** Open the file in Obsidian and check the console output

### 2. `test-edge-cases.md`
**Purpose:** Tests boundary conditions and corner cases
**Covers:**
- Empty lines and their effect on hierarchy
- Mixed indentation levels (2, 4, 6, 8+ spaces)
- Content immediately after headers vs. after empty lines
- Deep nesting (8+ levels)
- Empty content blocks
- Horizontal rule hierarchy breaks
- Parent-child relationship consistency

**How to test:** Open the file in Obsidian and verify edge case handling

### 3. `test-compatibility.md`
**Purpose:** Verifies backward compatibility with existing components
**Covers:**
- BlockCollection to compatibility array conversion
- Integration with mentionsProcessor
- Performance testing with multiple queries
- Memory usage estimation
- Consistency between old and new formats

**How to test:** Open the file in Obsidian and check compatibility results

### 4. `test-real-world-scenario.md`
**Purpose:** Tests with realistic daily note content
**Covers:**
- Complex nested todo structures
- Multiple activity mentions
- Mixed content types in hierarchy
- Productivity metrics calculation
- Performance with realistic content volume
- Time-based analysis

**How to test:** Open the file in Obsidian and analyze real-world performance

### 5. `test-mixed-types.md`
**Purpose:** Tests blocks with multiple types and complex attribute combinations
**Covers:**
- Headers that also contain mentions
- Blocks with multiple mentions
- Mixed-type attribute queries
- Enhanced attribute system capabilities
- Complex content analysis and tagging
- Advanced querying with multiple criteria

**How to test:** Open the file in Obsidian and verify mixed-type support

## 🚀 How to Run Tests

### Prerequisites
1. Ensure CustomJS plugin is installed and configured
2. Make sure all Block system files are in place:
   - `Engine/Scripts/components/Block.js`
   - `Engine/Scripts/components/noteBlocksParser.js`
   - Updated mentionsProcessor, dailyNoteComposer, activityComposer

### Running Individual Tests
1. Open any test file (`.md`) in Obsidian
2. The DataviewJS block will execute automatically
3. Check the console (F12 → Console) for detailed output
4. Look for ✅ success indicators or ❌ error messages

### Running All Tests
1. Open each test file one by one
2. Wait for each test to complete before opening the next
3. Compare results across different test scenarios

## 📊 Expected Test Results

### Basic Hierarchy Test
- Should parse 15-25 blocks depending on content
- Should show proper parent-child relationships
- Should handle different indentation levels correctly
- Query operations should return expected counts

### Edge Cases Test
- Should handle deep nesting (8+ levels) without errors
- Should properly break hierarchy on empty lines and separators
- Should maintain parent-child consistency (0 errors)
- Should handle mixed content types gracefully

### Compatibility Test
- BlockCollection should convert to compatibility array correctly
- mentionsProcessor should work with both formats
- Query performance should be under 50ms for 100 operations
- Memory usage should be reasonable (under 100KB for test content)

### Real-World Scenario Test
- Should parse 50+ blocks from complex daily note
- Should calculate productivity metrics correctly
- Should handle multiple activity references
- Should maintain good performance with realistic content

### Mixed Types Test
- Should support blocks with multiple attributes simultaneously
- Should track multiple mentions per block correctly
- Should enable complex queries combining different attributes
- Should preserve hierarchy regardless of mixed types
- Should demonstrate enhanced attribute system capabilities

## 🔍 Debugging Failed Tests

### Common Issues and Solutions

**Error: "Block is not defined"**
- Solution: Ensure `Block.js` is loaded by CustomJS
- Check CustomJS settings and file paths

**Error: "noteBlocksParser is not defined"**
- Solution: Verify `noteBlocksParser.js` is updated with new implementation
- Check for syntax errors in the parser file

**Hierarchy not working correctly**
- Check indentation in test content (should use spaces, not tabs)
- Verify empty line counting logic
- Look for separator handling issues

**Performance issues**
- Check for infinite loops in hierarchy building
- Verify parent-child relationship consistency
- Look for memory leaks in Block objects

### Debug Mode
Add this to any test for more detailed output:
```javascript
// Enable debug mode
console.log("Debug: Collection structure", collection.toDebugArray());
console.log("Debug: Hierarchy tree", JSON.stringify(collection.getHierarchy(), null, 2));
```

## 📈 Success Criteria

### ✅ All Tests Should Pass If:
1. **Hierarchy Structure**: Indentation-based parent-child relationships work correctly
2. **Content Types**: All block types (header, todo, mention, callout, code, text) are recognized
3. **Attributes**: Generic attribute system allows flexible block properties
4. **Mixed Types**: Blocks can have multiple attributes simultaneously (e.g., header + mention)
5. **Queries**: Fast and accurate querying by type and attributes
6. **Compatibility**: Existing components work with new Block system
7. **Performance**: Good performance with realistic content volumes
8. **Edge Cases**: Robust handling of boundary conditions

### 🎯 Key Metrics to Verify:
- **Parsing Speed**: Should handle typical daily notes in <100ms
- **Memory Usage**: Reasonable memory footprint for Block objects
- **Hierarchy Accuracy**: Parent-child relationships match indentation structure
- **Query Performance**: Fast filtering and searching operations
- **Compatibility**: Seamless integration with existing workflow

## 🛠️ Troubleshooting

If tests fail, check:
1. CustomJS plugin configuration
2. File paths and imports
3. Console errors for syntax issues
4. Block system file integrity
5. Obsidian plugin compatibility

## 📝 Test Results Log

After running tests, document results here:

**Date:** ___________
**Basic Hierarchy:** ✅/❌ ___________
**Edge Cases:** ✅/❌ ___________  
**Compatibility:** ✅/❌ ___________
**Real-World:** ✅/❌ ___________
**Mixed Types:** ✅/❌ ___________
**Notes:** ___________

---

**Last Updated:** August 28, 2025
**Version:** 1.0 - Initial Block System Implementation
