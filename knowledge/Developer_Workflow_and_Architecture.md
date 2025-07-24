# Developer Workflow and Architecture for Knowledge Management System

This document provides a detailed technical overview of the knowledge management system architecture, workflows, and interactions for developers.

## Actors

- **User:** Creates and edits notes and daily journals in Obsidian.
- **Obsidian Plugins:**
  - **Daily Notes Plugin:** Automatically creates daily notes using templates.
  - **Dataview Plugin:** Provides querying and scripting capabilities.
  - **Templater Plugin:** Enables dynamic templates with embedded scripts.
  - **CustomJS Plugin:** Runs custom JavaScript modules.
- **Scripts:**
  - **activityComposer:** Main orchestrator for processing activity and daily notes.
  - **dailyNoteComposer:** Orchestrates daily journal note processing.
  - **mentionsProcessor:** Handles collection and insertion of mentions across notes.
  - **noteBlocksParser:** Parses note content into structured blocks.
  - **attributesProcessor:** Processes directives and updates frontmatter metadata.
  - **Other Components and Utilities:** Handle specialized processing and file operations.

## Workflow Sequence

```mermaid
sequenceDiagram
    participant User
    participant Obsidian
    participant DailyNotesPlugin
    participant TemplaterPlugin
    participant DataviewPlugin
    participant CustomJS
    participant activityComposer
    participant noteBlocksParser
    participant mentionsProcessor
    participant attributesProcessor
    participant FileSystem

    User->>Obsidian: Open/Create Daily Note
    Obsidian->>DailyNotesPlugin: Trigger daily note creation
    DailyNotesPlugin->>TemplaterPlugin: Apply DailyNote-template.md
    TemplaterPlugin->>DataviewPlugin: Execute embedded dataviewjs script
    DataviewPlugin->>CustomJS: Load activityComposer
    CustomJS->>activityComposer: processActivity(currentNote)
    activityComposer->>FileSystem: Load current note content
    activityComposer->>noteBlocksParser: Parse journal pages for blocks
    activityComposer->>attributesProcessor: Process attributes in note content
    activityComposer->>mentionsProcessor: Process mentions and update note content
    mentionsProcessor->>FileSystem: Read related notes for mentions
    mentionsProcessor->>activityComposer: Return updated content
    activityComposer->>FileSystem: Save updated note content
    activityComposer->>User: Return success status
```

## Flowchart Diagram

```mermaid
flowchart TD
    A[User opens/creates daily note] --> B[Daily Notes Plugin creates note using template]
    B --> C[Templater Plugin runs embedded dataviewjs scripts]
    C --> D[activityComposer.processActivity invoked]
    D --> E[noteBlocksParser parses journal pages]
    E --> F[attributesProcessor processes directives]
    F --> G[mentionsProcessor collects and inserts mentions]
    G --> H[Updated note content saved to vault]
    H --> I[User continues editing or reviewing notes]
```

## Key Points

- The system leverages Obsidian's plugin ecosystem to automate note creation and processing.
- JavaScript orchestrators coordinate parsing, metadata processing, and mention handling.
- Mentions ([[...]] links) in notes dynamically link related content and trigger activity updates.
- Frontmatter metadata is updated to reflect note status, dates, and responsibilities.
- The architecture supports extensibility through modular components and utilities.

## Template System Architecture Evolution

### Hybrid Templater+DataviewJS Approach

The system has evolved from a pure DataviewJS approach to a hybrid Templater+DataviewJS architecture that provides superior file organization and processing capabilities.

#### Why Hybrid Approach Works Better

1. **File Movement Capabilities:** Templater can move and rename files during template instantiation, which is impossible with DataviewJS blocks that execute after file creation.

2. **Conditional Logic:** Templates can decide file destination based on filename format before any content is written, enabling smart file organization.

3. **Template Execution Timing:** Templater runs once during file creation vs DataviewJS that runs every time the file is opened, providing better performance for setup logic.

4. **Content Generation:** Can dynamically generate different template content based on conditions, creating truly adaptive templates.

#### File Organization Logic

**Smart File Routing Pattern:**
```javascript
// In DailyNote template
if (!moment(title, "YYYY-MM-DD", true).isValid()) {
  // Non-daily file → Move to Activities folder
  const newPath = `Activities/${title}`;
  const fileExists = await app.vault.adapter.exists(newPath + '.md');
  if (!fileExists) {
    await tp.file.move(newPath);
  }
  // Generate activity content
} else {
  // Daily file → Stay in Journal, process as daily note
}
```

**File Movement Implementation:**
- Uses `app.vault.adapter.exists()` for existence checking
- Prevents overwrites of existing files
- Proper path handling for subfolders
- Console logging for debugging

#### Content Generation Strategy

**Activity File Structure:**
```yaml
---
startDate: YYYY-MM-DD
stage: active
responsible: [Me]
---

```dataviewjs
// Complete processing pipeline
const {fileIO} = await cJS();
// ... full activity processing logic
```
```

**Processing Pipeline:**
1. **Template Execution** (Templater processes `<%* ... %>` blocks)
2. **File Movement** (Smart routing based on filename pattern)
3. **Content Generation** (Frontmatter + DataviewJS block creation)
4. **Dynamic Processing** (DataviewJS executes on file open)
5. **Content Assembly** (Final processed content with cross-references)

#### Template Design Principles

1. **Detailed Inline Logic:** User preference over centralized composer approach for better maintainability and transparency.

2. **Content Preservation:** Templates maintain any existing user content during processing.

3. **Error Handling:** Proper existence checking and console logging for debugging.

4. **Performance Optimization:** One-time Templater execution for setup, ongoing DataviewJS for dynamic content.

#### Architecture Benefits

- **Automatic Organization:** Files are automatically sorted into correct folders
- **Consistent Structure:** All activity files have the same processing pipeline
- **Dynamic Processing:** DataviewJS blocks regenerate content on each file open
- **Template Name Preservation:** No changes to template filenames (important for plugin configuration)
- **Hybrid Performance:** Best of both worlds - Templater for setup, DataviewJS for processing

### Updated Workflow Sequence

```mermaid
sequenceDiagram
    participant User
    participant Obsidian
    participant TemplaterPlugin
    participant DataviewPlugin
    participant CustomJS
    participant FileSystem

    User->>Obsidian: Create note with template
    Obsidian->>TemplaterPlugin: Execute template (<%* ... %>)
    TemplaterPlugin->>TemplaterPlugin: Check filename pattern
    alt Non-daily filename
        TemplaterPlugin->>FileSystem: Check if Activities/filename exists
        TemplaterPlugin->>FileSystem: Move file to Activities/
        TemplaterPlugin->>TemplaterPlugin: Generate activity frontmatter
        TemplaterPlugin->>TemplaterPlugin: Generate activity DataviewJS block
    else Daily filename (YYYY-MM-DD)
        TemplaterPlugin->>TemplaterPlugin: Generate daily note DataviewJS block
    end
    TemplaterPlugin->>DataviewPlugin: DataviewJS block executes on file open
    DataviewPlugin->>CustomJS: Load processing components
    CustomJS->>FileSystem: Process content and save
```

---

*Document created as part of project knowledge base.*
*Last updated: July 24, 2025 - Added template system architecture evolution*
