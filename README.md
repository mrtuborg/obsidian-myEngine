# Personal Knowledge Management System - Developer Manual

## Table of Contents
1. [System Overview](#system-overview)
2. [Architecture](#architecture)
3. [Quick Start Guide](#quick-start-guide)
4. [Core Components](#core-components)
5. [Templates](#templates)
6. [Processing Pipeline](#processing-pipeline)
7. [Data Flow](#data-flow)
8. [Block Types and Parsing](#block-types-and-parsing)
9. [Todo Management](#todo-management)
10. [Activity System](#activity-system)
11. [Mentions and Cross-References](#mentions-and-cross-references)
12. [File Structure](#file-structure)
13. [Configuration](#configuration)
14. [API Reference](#api-reference)
15. [Testing](#testing)
16. [Performance Optimization](#performance-optimization)
17. [Security Considerations](#security-considerations)
18. [Troubleshooting](#troubleshooting)
19. [Development Guidelines](#development-guidelines)
20. [Examples and Use Cases](#examples-and-use-cases)
21. [Migration Guide](#migration-guide)
22. [FAQ](#faq)

## System Overview

This is a sophisticated Personal Knowledge Management (PKM) system built on top of Obsidian, utilizing DataviewJS and CustomJS plugins to create an automated, intelligent note-taking and task management system.

### Key Features
- **Automated Daily Notes**: Self-updating daily notes with todo rollover
- **Activity Management**: Project-based task organization with automatic processing
- **Smart Todo System**: Context-aware todo rollover and activity association
- **Cross-Reference System**: Automatic mention processing and content aggregation
- **Template-Based Architecture**: Consistent note structure and processing

### Technology Stack
- **Obsidian**: Base note-taking application
- **DataviewJS**: Dynamic content generation and queries
- **CustomJS**: Shared JavaScript modules and utilities
- **Moment.js**: Date manipulation and formatting

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    OBSIDIAN VAULT                           │
├─────────────────────────────────────────────────────────────┤
│  Templates/          │  Scripts/           │  Journal/      │
│  ├─ DailyNote        │  ├─ Composers       │  └─ YYYY/      │
│  ├─ Activity         │  ├─ Components      │     └─ MM.Mon/ │
│  └─ People           │  └─ Utilities       │        └─ DD   │
├─────────────────────────────────────────────────────────────┤
│  Activities/         │  People/            │  Spaces/       │
│  ├─ Active           │  ├─ Contacts        │  └─ Topics     │
│  ├─ Archive/         │  └─ Meetings/       │                │
│  └─ Workflow/        │                     │                │
└─────────────────────────────────────────────────────────────┘
```

## Core Components

### 1. Composers (High-Level Orchestrators)

#### `dailyNoteComposer.js`
**Purpose**: Orchestrates the complete daily note processing pipeline.

**Process Flow**:
1. **Load Dependencies**: Imports all required modules
2. **Content Extraction**: Separates frontmatter, DataviewJS, and content
3. **Block Parsing**: Processes all journal pages for mentions and todos
4. **Todo Rollover**: Rolls over incomplete todos from previous days (today only)
5. **Activity Integration**: Adds in-progress activities (today only)
6. **Mention Processing**: Aggregates cross-references from other notes
7. **Script Cleanup**: Removes DataviewJS blocks (today only)
8. **Content Assembly**: Combines all processed content and saves

**Key Logic**:
```javascript
// Only process special features for today's note
const pageIsToday = fileIO.isDailyNote(currentPageFile.name);

if (pageIsToday) {
  // Todo rollover, activities, script cleanup
}
// Always process mentions for all daily notes
```

#### `activityComposer.js`
**Purpose**: Manages activity note processing and lifecycle.

**Process Flow**:
1. **Frontmatter Processing**: Handles activity metadata (startDate, stage, responsible)
2. **Content Extraction**: Separates structure from content
3. **Block Parsing**: Processes journal pages for activity mentions
4. **Mention Aggregation**: Collects references from daily notes
5. **Content Assembly**: Combines processed content and saves

### 2. Components (Specialized Processors)

#### `noteBlocksParser.js`
**Purpose**: Parses note content into structured blocks for processing.

**Block Types**:
- **Header**: `# ## ### #### #####` - Multi-line blocks ending on next header, `---`, or 2+ empty lines
- **Callout**: `> text` - Single-line blocks
- **Code**: ``` blocks - Multi-line code blocks
- **Todo**: `- [ ]` - Individual todo items (created separately even within headers)
- **Done**: `- [x]` - Completed todo items
- **Mention**: `[[Link]]` - Single-line mention blocks

**Critical Parsing Rules**:
```javascript
// Header blocks end when:
// 1. Next header of same or higher level
// 2. Horizontal separator (--- or ----)
// 3. Two consecutive empty lines

// Todos are ALWAYS created as separate blocks
// even when they appear within header blocks
```

#### `todoRollover.js`
**Purpose**: Manages todo rollover from previous days to today.

**Activity Association Logic**:
1. **Direct Link Check**: Todo contains `[[Activities/...]]`, `[[MyObsidian]]`, or any `[[link]]`
2. **Block Context Check**: Todo appears within activity header block content
3. **Standalone Detection**: Todo is not associated with any activity

**Rollover Rules**:
- Only runs for today's daily note (`pageIsToday = true`)
- Only processes todos from dates before today
- Excludes activity-related todos
- Removes duplicates already present in current note

#### `mentionsProcessor.js`
**Purpose**: Aggregates content from notes that mention the current note.

**Processing Logic**:
1. **Mention Detection**: Finds blocks containing current note's name
2. **Content Filtering**: Excludes blocks from current note itself
3. **Directive Processing**: Converts `{directive}` to `(directive from filename)` for regular text
4. **Code Block Protection**: Preserves JavaScript syntax in DataviewJS blocks
5. **Deduplication**: Avoids adding duplicate content

**Directive System**:
```javascript
// Supported operations:
{attribute = value}     // Set attribute
{attribute += value}    // Add to attribute
{attribute -= value}    // Subtract from attribute
{attribute : value}     // Set string attribute

// Date arithmetic:
{startDate += 1d}       // Add 1 day
{startDate += 2w}       // Add 2 weeks
{startDate += 1m}       // Add 1 month
```

#### `activitiesInProgress.js`
**Purpose**: Adds activity sections to today's daily note.

**Selection Criteria**:
- Activities with `stage: active`
- Activities with `stage: planning` and recent activity (mentions in last 7 days)
- Excludes `MyObsidian` activity (handled separately)

### 3. Utilities

#### `fileIO.js`
**Purpose**: Centralized file operations and content generation.

**Key Functions**:
- `loadFile()` / `saveFile()`: File I/O operations
- `generateDailyNoteHeader()`: Creates daily note frontmatter
- `generateActivityHeader()`: Creates activity frontmatter
- `extractFrontmatterAndDataviewJs()`: Content structure parsing
- `isDailyNote()`: Determines if current note is today's date

## Templates

### `DailyNote-template.md`
**Purpose**: Template for daily journal notes with date-based naming.

**Structure**:
```markdown
---
---
### DD [[YYYY-MM|Month]] [[YYYY]]
#### Week: [[YYYY-WNN|NN]]

----

### Activities:
----

[DataviewJS block for processing]
```

**Processing**: Uses `dailyNoteComposer` for complete pipeline processing.

### `Activity-template.md`
**Purpose**: Template for project/activity management.

**Structure**:
```markdown
---
startDate: YYYY-MM-DD
stage: active|planning|completed|archived
responsible: [Me]
---

[DataviewJS block for processing]
```

**Processing**: Uses `activityComposer` for activity-specific processing.

## Processing Pipeline

### Daily Note Processing Flow

```
1. Template Instantiation
   ↓
2. dailyNoteComposer.processDailyNote()
   ↓
3. Content Structure Extraction
   ├─ Frontmatter
   ├─ DataviewJS Block
   └─ Page Content
   ↓
4. Block Parsing (noteBlocksParser)
   ├─ Parse all journal pages
   ├─ Extract todos, headers, mentions
   └─ Create structured block array
   ↓
5. Todo Processing (if today)
   ├─ Filter todos from previous days
   ├─ Exclude activity-related todos
   ├─ Remove duplicates
   └─ Add to page content
   ↓
6. Activity Integration (if today)
   ├─ Find active activities
   ├─ Generate activity sections
   └─ Add to page content
   ↓
7. Mention Processing
   ├─ Find mentions of current note
   ├─ Process directives
   ├─ Aggregate content
   └─ Add to page content
   ↓
8. Script Cleanup (if today)
   ├─ Remove DataviewJS blocks
   └─ Clean up processing artifacts
   ↓
9. Content Assembly & Save
   ├─ Combine frontmatter + content
   └─ Save to file
```

### Activity Note Processing Flow

```
1. Template Instantiation
   ↓
2. activityComposer.processActivity()
   ↓
3. Frontmatter Processing
   ├─ Extract startDate, stage, responsible
   ├─ Apply defaults if missing
   └─ Generate activity header
   ↓
4. Content Structure Extraction
   ├─ DataviewJS Block
   └─ Page Content
   ↓
5. Block Parsing (noteBlocksParser)
   ├─ Parse all journal pages
   ├─ Filter out current activity
   └─ Create structured block array
   ↓
6. Mention Processing
   ├─ Find mentions of current activity
   ├─ Process directives
   ├─ Aggregate content
   └─ Add to page content
   ↓
7. Content Assembly & Save
   ├─ Combine frontmatter + dataviewjs + content
   └─ Save to file
```

## Data Flow

### Block Structure
```javascript
{
  page: "Journal/2025/07.July/2025-07-05.md",
  blockType: "todo|done|header|mention|callout|code",
  data: "Block content as string",
  mtime: 1625097600000,
  headerLevel: 5  // Only for header blocks
}
```

### Todo Association Logic
```javascript
// Activity-related todos (NOT rolled over):
1. Todo contains [[Activities/...]] or [[MyObsidian]] or any [[link]]
2. Todo appears within activity header block content

// Standalone todos (WILL be rolled over):
1. Todo has no [[link]] references
2. Todo appears outside activity header blocks
```

### Mention Processing
```javascript
// Regular text: {directive} → (directive from filename)
// Code blocks: {directive} → preserved as-is
// Prevents JavaScript syntax corruption
```

## Block Types and Parsing

### Header Blocks
- **Pattern**: `^#+\s+.*$`
- **Levels**: 1-6 (`#` to `######`)
- **Termination**: Next header (same/higher level), `---` separator, or 2+ empty lines
- **Content**: Multi-line, includes everything until termination

### Todo/Done Blocks
- **Todo Pattern**: `^- \[ \]` or `^> - \[ \]`
- **Done Pattern**: `^- \[x\]` or `^> - \[x\]`
- **Behavior**: Always created as separate blocks, even within headers
- **Callout Support**: Handles `>` prefixed todos in callouts

### Activity Headers
- **Pattern**: `^#{5}\s+\[\[Activities/.*\]\]`
- **Purpose**: Level 5 headers linking to activity notes
- **Block Boundary**: Defines activity context for todo association

## Todo Management

### Rollover System
1. **Source**: Incomplete todos from previous daily notes
2. **Target**: Today's daily note only
3. **Filtering**: Excludes activity-related todos
4. **Deduplication**: Avoids adding existing todos
5. **Placement**: After last `---` separator or at end

### Activity Association
```javascript
// Activity todos (stay in place):
- [ ] Buy something [[Activities/Shopping]]  // Has link
- [ ] Task under activity header             // In activity block

// Standalone todos (roll over):
- [ ] Personal task                          // No links, outside blocks
- [ ] Call dentist                          // No activity context
```

### Recurrence Support
- `[[Review/Daily]]`: Daily recurrence
- `[[Review/Weekly]]`: Weekly recurrence  
- `[[Review/Monthly]]`: Monthly recurrence

## Activity System

### Activity Lifecycle
1. **Planning**: `stage: planning` - Ideas and preparation
2. **Active**: `stage: active` - Currently working on
3. **Completed**: `stage: completed` - Finished successfully
4. **Archived**: `stage: archived` - Inactive/cancelled

### Activity Integration
- **Active Activities**: Always appear in today's daily note
- **Planning Activities**: Appear if mentioned in last 7 days
- **Special Case**: `MyObsidian` activity handled separately

### Activity Frontmatter
```yaml
---
startDate: 2025-07-06        # Project start date
stage: active                # Current lifecycle stage
responsible: [Me, Partner]   # Who's responsible
---
```

## Mentions and Cross-References

### Mention Detection
- **Pattern**: `[[NoteName]]` or `[[NoteName|Alias]]`
- **Scope**: Searches all journal pages
- **Exclusion**: Ignores mentions from current note itself

### Content Aggregation
1. **Collection**: Gathers blocks mentioning current note
2. **Processing**: Applies directive transformations
3. **Organization**: Groups by source file
4. **Insertion**: Adds after last `---` separator

### Directive System
Enables dynamic frontmatter updates from mentions:
```javascript
// In daily note mentioning an activity:
{startDate += 1d}           // Extends activity start date
{stage = completed}         // Changes activity stage
{responsible += Partner}    // Adds to responsible list
```

## File Structure

```
Vault/
├── Engine/
│   ├── Scripts/
│   │   ├── dailyNoteComposer.js      # Daily note orchestrator
│   │   ├── activityComposer.js       # Activity orchestrator
│   │   ├── components/
│   │   │   ├── noteBlocksParser.js   # Content parser
│   │   │   ├── todoRollover.js       # Todo management
│   │   │   ├── mentionsProcessor.js  # Cross-reference handler
│   │   │   └── activitiesInProgress.js # Activity integration
│   │   └── utilities/
│   │       └── fileIO.js             # File operations
│   └── Templates/
│       ├── DailyNote-template.md     # Daily note template
│       └── Activity-template.md      # Activity template
├── Journal/
│   └── YYYY/
│       └── MM.Month/
│           └── YYYY-MM-DD.md         # Daily notes
├── Activities/
│   ├── ProjectName.md                # Active projects
│   ├── Archive/                      # Completed activities
│   └── Workflow/                     # Process activities
└── People/
    └── PersonName.md                 # Contact notes
```

## Configuration

### CustomJS Setup
Ensure all scripts are registered in CustomJS settings:
```javascript
// Required modules:
- dailyNoteComposer
- activityComposer  
- noteBlocksParser
- todoRollover
- mentionsProcessor
- activitiesInProgress
- fileIO
```

### Template Configuration
Templates should be placed in `Engine/Templates/` and configured in Templater plugin settings.

## Troubleshooting

### Common Issues

#### 1. "Unexpected token '('" Error
**Cause**: MentionsProcessor converting `{directive}` to `(directive from file)` in JavaScript code blocks.
**Solution**: Code block protection is implemented - ensure `isCodeBlock` parameter is properly passed.

#### 2. Todos Not Rolling Over
**Cause**: Todos incorrectly classified as activity-related.
**Solution**: Check todo content for `[[links]]` and verify activity header block boundaries.

#### 3. Duplicate Content in Mentions
**Cause**: Mention deduplication not working properly.
**Solution**: Verify normalized line comparison logic in mentionsProcessor.

#### 4. Activity Not Appearing in Daily Note
**Cause**: Activity stage not set to `active` or no recent mentions for `planning` stage.
**Solution**: Update activity frontmatter or add mentions in recent daily notes.

### Debug Logging
All components include console.log statements for debugging:
```javascript
console.log("TodoRollover: Starting rollover process");
console.log("MentionsProcessor: Processing mentions for", tagId);
```

## Development Guidelines

### Code Style
- Use ES6+ features (async/await, arrow functions, destructuring)
- Implement comprehensive error handling
- Add descriptive console logging for debugging
- Follow consistent naming conventions

### Testing
- Test with various note structures
- Verify edge cases (empty notes, malformed content)
- Test date boundary conditions
- Validate cross-reference integrity

### Performance Considerations
- Minimize file I/O operations
- Cache parsed content when possible
- Use efficient filtering and searching
- Avoid unnecessary re-processing

### Extension Points
- **New Block Types**: Extend noteBlocksParser with additional patterns
- **Custom Directives**: Add new directive operations in mentionsProcessor
- **Activity Stages**: Extend lifecycle stages in activityComposer
- **Template Types**: Create new templates with corresponding composers

### Error Handling
```javascript
try {
  // Processing logic
} catch (error) {
  console.error("ComponentName error:", error);
  return {
    success: false,
    error: error.message
  };
}
```

### Module Structure
```javascript
class ComponentName {
  // Private helper methods
  
  // Public processing methods
  
  // Main entry point
  async run(app, ...params) {
    return await this.processMethod(app, ...params);
  }
}
```

## Quick Start Guide

### Prerequisites
1. **Obsidian** with the following plugins installed:
   - DataviewJS
   - CustomJS
   - Templater
2. **Node.js** knowledge for JavaScript development
3. **Basic understanding** of Obsidian's file structure and linking system

### Initial Setup
1. **Clone/Copy Scripts**: Place all scripts in `Engine/Scripts/` directory
2. **Configure CustomJS**: Register all modules in CustomJS plugin settings
3. **Setup Templates**: Place templates in `Engine/Templates/` and configure Templater
4. **Create Folder Structure**: Ensure `Journal/`, `Activities/`, `People/` folders exist
5. **Test Basic Functionality**: Create a daily note and verify processing works

### First Daily Note
```markdown
1. Use DailyNote-template.md to create: Journal/2025/07.July/2025-07-06.md
2. The DataviewJS block will automatically process the note
3. Check console for any errors
4. Verify frontmatter and content are generated correctly
```

### First Activity
```markdown
1. Use Activity-template.md to create: Activities/TestProject.md
2. Set frontmatter: startDate, stage: active, responsible: [Me]
3. Add some content and todos
4. Create a daily note that mentions this activity
5. Verify cross-references work correctly
```

## API Reference

### Core Classes

#### `dailyNoteComposer`
```javascript
class dailyNoteComposer {
  async processDailyNote(app, dv, currentPageFile, title)
  // Returns: { success: boolean, frontmatter: string, content: string, isToday: boolean }
}
```

#### `activityComposer`
```javascript
class activityComposer {
  async processActivity(app, dv, currentPageFile)
  // Returns: { success: boolean, frontmatter: string, content: string }
}
```

#### `noteBlocksParser`
```javascript
class noteBlocksParser {
  parse(page, content)
  // Returns: Array<Block>
  
  async run(app, pages, namePattern = "")
  // Returns: Array<Block>
}

// Block Structure:
interface Block {
  page: string;
  blockType: 'todo'|'done'|'header'|'mention'|'callout'|'code';
  data: string;
  mtime: number;
  headerLevel?: number;
}
```

#### `todoRollover`
```javascript
class todoRollover {
  async rolloverTodos(app, blocks, todayDate, currentPageContent, removeOriginals)
  // Returns: string (updated content)
  
  isActivityRelatedTodo(todoBlock, allBlocks)
  // Returns: boolean
  
  async run(app, collectedBlocks, dailyNoteDate, currentPageContent, RemoveOriginals = false)
  // Returns: string (updated content)
}
```

#### `mentionsProcessor`
```javascript
class mentionsProcessor {
  async processMentions(currentPageContent, blocks, tagId, frontmatterObj)
  // Returns: string (updated content with mentions)
  
  async run(currentPageContent, collectedBlocks, mentionStr, frontmatterObj)
  // Returns: string (updated content)
}
```

#### `fileIO`
```javascript
class fileIO {
  static async loadFile(app, filename)
  // Returns: string (file content)
  
  static async saveFile(app, filename, content)
  // Returns: void
  
  static generateDailyNoteHeader(date)
  // Returns: string (frontmatter)
  
  static generateActivityHeader(startDate, stage, responsible)
  // Returns: string (frontmatter)
  
  static extractFrontmatterAndDataviewJs(content)
  // Returns: { frontmatter: string, dataviewJsBlock: string, pageContent: string }
  
  static isDailyNote(filename)
  // Returns: boolean
  
  static todayDate()
  // Returns: string (YYYY-MM-DD format)
}
```

### Directive Operations
```javascript
// Supported directive patterns in mentions:
{attribute = value}      // Set attribute to value
{attribute += value}     // Add value to attribute
{attribute -= value}     // Subtract value from attribute
{attribute : value}      // Set string attribute

// Date arithmetic examples:
{startDate += 1d}        // Add 1 day
{startDate += 2w}        // Add 2 weeks  
{startDate += 1m}        // Add 1 month
{startDate += 1y}        // Add 1 year
{startDate -= 3d}        // Subtract 3 days
```

## Testing

### Unit Testing Approach
```javascript
// Example test structure for todoRollover
describe('todoRollover', () => {
  let todoRollover;
  
  beforeEach(() => {
    todoRollover = new todoRollover();
  });
  
  test('should identify activity-related todos', () => {
    const todoBlock = {
      data: '- [ ] Task [[Activities/Project]]',
      page: 'Journal/2025/07.July/2025-07-05.md'
    };
    
    expect(todoRollover.isActivityRelatedTodo(todoBlock, [])).toBe(true);
  });
  
  test('should identify standalone todos', () => {
    const todoBlock = {
      data: '- [ ] Call dentist',
      page: 'Journal/2025/07.July/2025-07-05.md'
    };
    
    expect(todoRollover.isActivityRelatedTodo(todoBlock, [])).toBe(false);
  });
});
```

### Integration Testing
```javascript
// Test complete daily note processing
async function testDailyNoteProcessing() {
  const mockApp = createMockObsidianApp();
  const mockDv = createMockDataview();
  const mockFile = { path: 'Journal/2025/07.July/2025-07-06.md', name: '2025-07-06' };
  
  const composer = new dailyNoteComposer();
  const result = await composer.processDailyNote(mockApp, mockDv, mockFile, '2025-07-06');
  
  expect(result.success).toBe(true);
  expect(result.content).toContain('### 06 [[2025-07|July]] [[2025]]');
}
```

### Test Data Setup
```markdown
// Create test files in a separate test vault:
TestVault/
├── Journal/2025/07.July/
│   ├── 2025-07-05.md (with test todos)
│   └── 2025-07-06.md (target for rollover)
├── Activities/
│   └── TestActivity.md (with test content)
└── Engine/Scripts/ (copy of all scripts)
```

## Performance Optimization

### Caching Strategies
```javascript
// Cache parsed blocks to avoid re-parsing
class noteBlocksParser {
  constructor() {
    this.blockCache = new Map();
  }
  
  async run(app, pages, namePattern = "") {
    const cacheKey = pages.map(p => p.file.path + p.file.stat.mtime).join('|');
    
    if (this.blockCache.has(cacheKey)) {
      return this.blockCache.get(cacheKey);
    }
    
    const blocks = await this.parsePages(app, pages, namePattern);
    this.blockCache.set(cacheKey, blocks);
    return blocks;
  }
}
```

### Batch Operations
```javascript
// Process multiple files in batches to avoid memory issues
async function processBatch(files, batchSize = 10) {
  for (let i = 0; i < files.length; i += batchSize) {
    const batch = files.slice(i, i + batchSize);
    await Promise.all(batch.map(file => processFile(file)));
    
    // Allow other operations to run
    await new Promise(resolve => setTimeout(resolve, 0));
  }
}
```

### Memory Management
```javascript
// Clear caches periodically
setInterval(() => {
  if (blockCache.size > 1000) {
    blockCache.clear();
    console.log('Cleared block cache to prevent memory issues');
  }
}, 300000); // Every 5 minutes
```

## Security Considerations

### Input Validation
```javascript
// Validate file paths to prevent directory traversal
function validateFilePath(path) {
  if (path.includes('..') || path.startsWith('/')) {
    throw new Error('Invalid file path: ' + path);
  }
  return path;
}

// Sanitize directive values
function sanitizeDirectiveValue(value) {
  // Remove potentially dangerous characters
  return value.replace(/[<>\"'&]/g, '');
}
```

### Content Sanitization
```javascript
// Prevent script injection in processed content
function sanitizeContent(content) {
  // Remove script tags and dangerous HTML
  return content
    .replace(/<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/gi, '')
    .replace(/javascript:/gi, '')
    .replace(/on\w+\s*=/gi, '');
}
```

### File Access Control
```javascript
// Restrict file operations to vault directory
function isValidVaultPath(app, path) {
  const vaultPath = app.vault.adapter.basePath;
  const fullPath = require('path').resolve(vaultPath, path);
  return fullPath.startsWith(vaultPath);
}
```

## Examples and Use Cases

### Example 1: Custom Activity Stage
```javascript
// Extend activityComposer to support custom stages
class extendedActivityComposer extends activityComposer {
  getValidStages() {
    return ['planning', 'active', 'blocked', 'review', 'completed', 'archived'];
  }
  
  shouldIncludeInDaily(activity, mentions) {
    const stage = activity.stage;
    
    if (stage === 'blocked') {
      // Include blocked activities if mentioned in last 3 days
      return mentions.some(m => moment().diff(moment(m.date), 'days') <= 3);
    }
    
    return super.shouldIncludeInDaily(activity, mentions);
  }
}
```

### Example 2: Custom Block Type
```javascript
// Add support for habit tracking blocks
class extendedNoteBlocksParser extends noteBlocksParser {
  isHabitLine(line) {
    return line.match(/^- \[habit\]/);
  }
  
  parse(page, content) {
    const blocks = super.parse(page, content);
    
    // Add habit blocks
    const lines = content.split('\n');
    lines.forEach((line, index) => {
      if (this.isHabitLine(line)) {
        blocks.push({
          page: page,
          blockType: 'habit',
          data: line,
          mtime: Date.now(),
          lineNumber: index
        });
      }
    });
    
    return blocks;
  }
}
```

### Example 3: Custom Directive
```javascript
// Add support for priority directives
function processCustomDirective(directive, frontmatterObj) {
  if (directive.includes('priority')) {
    const match = directive.match(/priority\s*([=:+\-])\s*(\w+)/);
    if (match) {
      const operation = match[1];
      const value = match[2];
      
      switch (operation) {
        case '=':
        case ':':
          frontmatterObj.priority = value;
          break;
        case '+':
          frontmatterObj.priority = increasePriority(frontmatterObj.priority || 'low');
          break;
        case '-':
          frontmatterObj.priority = decreasePriority(frontmatterObj.priority || 'high');
          break;
      }
    }
  }
}

function increasePriority(current) {
  const levels = ['low', 'medium', 'high', 'urgent'];
  const index = levels.indexOf(current);
  return levels[Math.min(index + 1, levels.length - 1)];
}
```

## Migration Guide

### Upgrading from Previous Versions

#### Version 1.x to 2.x
```javascript
// Old way (deprecated):
const {todoRollover} = await cJS();
await todoRollover.run(app, blocks, date, content, true);

// New way:
const {todoRollover} = await cJS();
const result = await todoRollover.run(app, blocks, date, content, true);
if (result.success) {
  console.log('Rollover completed successfully');
}
```

#### Breaking Changes
1. **Return Values**: All processors now return structured objects instead of strings
2. **Error Handling**: Errors are now returned in result objects instead of thrown
3. **Async Operations**: All file operations are now properly async

#### Migration Script
```javascript
// Run this script to migrate old notes to new format
async function migrateNotes(app) {
  const files = app.vault.getMarkdownFiles();
  
  for (const file of files) {
    const content = await app.vault.read(file);
    
    // Update old directive format
    const updatedContent = content
      .replace(/\{(\w+)\s*=\s*([^}]+)\}/g, '{$1 = $2}')
      .replace(/\{(\w+)\s*\+=\s*([^}]+)\}/g, '{$1 += $2}');
    
    if (content !== updatedContent) {
      await app.vault.modify(file, updatedContent);
      console.log('Migrated:', file.path);
    }
  }
}
```

## FAQ

### Q: Why are my todos not rolling over?
**A**: Check if the todos contain `[[links]]` or are under activity headers. Only standalone todos without links roll over.

### Q: How do I add a new directive operation?
**A**: Extend the `processDirective` function in `mentionsProcessor.js` to handle your new operation pattern.

### Q: Can I customize the daily note structure?
**A**: Yes, modify `DailyNote-template.md` and update `generateDailyNoteHeader()` in `fileIO.js` accordingly.

### Q: How do I debug processing issues?
**A**: Enable browser console and look for component-specific log messages. Each component logs its processing steps.

### Q: Can I use this system with different folder structures?
**A**: Yes, but you'll need to update the path patterns in `noteBlocksParser.js` and file structure assumptions in composers.

### Q: How do I backup my data before making changes?
**A**: Use the provided `journal_backup.py` script or create manual backups of your vault before testing changes.

### Q: What happens if a script fails during processing?
**A**: Each component has error handling that logs errors and returns failure status without corrupting existing content.

### Q: Can I run multiple instances of the system?
**A**: Not recommended. The system assumes single-user operation and may have conflicts with concurrent processing.

### Q: How do I extend the system for team collaboration?
**A**: Consider adding user identification to frontmatter and filtering content by user in the processing pipeline.

### Q: What's the performance impact on large vaults?
**A**: Processing time scales with the number of journal pages. Consider implementing caching and batch processing for vaults with 1000+ notes.

This comprehensive manual provides developers with all the information needed to understand, maintain, extend, and troubleshoot the Personal Knowledge Management System effectively.
