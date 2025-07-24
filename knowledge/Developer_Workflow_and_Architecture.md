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

---

*Document created as part of project knowledge base.*
