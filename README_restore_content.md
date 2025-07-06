# Activity Content Restoration Utility

This Python utility reads all Activity files in your vault and restores **all content** (not just todos) to the corresponding daily notes based on the date markers found in each activity file.

## How It Works

The utility:
1. **Scans all Activity files** in the `Activities/` directory
2. **Extracts all content** (todos, notes, lists, headers, etc.) organized by date markers like `[[2025-07-04]]`
3. **Finds corresponding daily notes** in `Journal/YYYY/MM.Month/`
4. **Restores missing content** to the correct activity sections
5. **Preserves existing content** (won't overwrite if activity section already has content)

## Usage

**Note:** Run these commands from the `Engine/` directory where the script is located.

### 1. Preview Changes (Safe - Default)
```bash
cd Engine
python restore_activity_todos.py
# or explicitly:
python restore_activity_todos.py --dry-run
```
This shows what would be restored without making any changes.

### 2. Restore with Confirmation
```bash
cd Engine
python restore_activity_todos.py --confirm
```
This asks for confirmation before each change.

### 3. Restore Automatically
```bash
cd Engine
python restore_activity_todos.py --auto
```
This makes all changes automatically without prompts.

## Example Output

```
🚀 Activity Todos Restoration Utility
==================================================
🔍 Running in DRY RUN mode - no files will be modified

🔄 [DRY RUN] Starting Activity Todos Restoration...
📂 Vault path: /Users/vn/2ndBrain
📂 Activities path: /Users/vn/2ndBrain/Activities
📂 Journal path: /Users/vn/2ndBrain/Journal
🔍 DRY RUN MODE: No files will be modified
📋 Found 15 activity files

📁 Processing activity: Binary dependencies in cmake
  📅 Found dates: 2025-07-02, 2025-07-03
  📅 Date 2025-07-02: 2 todos
  📝 Will add 2 todos to 'Binary dependencies in cmake' in 2025-07-02.md:
    - [x] Накидать план с ChatGPT. Какие существуют варианты решения
    - [ ] Двигаться по полученым шагам и сформировать статью HowTo
  [DRY RUN] Would restore 2 todos for 'Binary dependencies in cmake' in 2025-07-02.md
  📅 Date 2025-07-03: 1 todos
  📝 Will add 1 todos to 'Binary dependencies in cmake' in 2025-07-03.md:
    - [ ] Накидать план с ChatGPT. Какие существуют варианты решения
  [DRY RUN] Would restore 1 todos for 'Binary dependencies in cmake' in 2025-07-03.md

📁 Processing activity: Embedded docker course
  📅 Found dates: 2025-07-04
  📅 Date 2025-07-04: 2 todos
  📝 Will add 2 todos to 'Embedded docker course' in 2025-07-04.md:
    - [ ] Изучить Moby project. Найти Quick Start
    - [ ] Есть ли moby project в Yocto?
  [DRY RUN] Would restore 2 todos for 'Embedded docker course' in 2025-07-04.md

✅ [DRY RUN] Restoration complete!
📊 Summary:
   - Activities processed: 15
   - Daily notes restored: 120

🔍 DRY RUN: Would restore todos to 120 daily notes!
💡 Run with --confirm to make changes with prompts, or --auto to make changes automatically
```

## Safety Features

- **Dry Run by Default**: No changes made unless explicitly requested
- **Confirmation Mode**: Asks before each change
- **Existing Todo Protection**: Won't overwrite if activity section already has todos
- **Missing Section Creation**: Creates missing Activities sections and activity subsections with permission
- **Error Handling**: Continues processing even if individual files have issues
- **Detailed Logging**: Shows exactly what will be changed

## Requirements

- Python 3.6+
- No external dependencies (uses only standard library)

## File Structure Expected

```
/Users/vn/2ndBrain/
├── Activities/
│   ├── Binary dependencies in cmake.md
│   ├── Embedded docker course.md
│   └── ...
└── Journal/
    └── 2025/
        ├── 01.January/
        │   ├── 2025-01-02.md
        │   └── ...
        ├── 07.July/
        │   ├── 2025-07-02.md
        │   ├── 2025-07-04.md
        │   └── ...
        └── ...
```

## Activity File Format

The utility looks for date markers in activity files:

```markdown
[[2025-07-02]]
- [x] Completed todo
- [ ] Pending todo

[[2025-07-04]]
- [ ] Another todo
- [ ] Yet another todo
```

## Daily Note Format

The utility finds activity sections in daily notes:

```markdown
##### [[Activities/Binary dependencies in cmake.md|Binary dependencies in cmake]]
----
##### [[Activities/Embedded docker course.md|Embedded docker course]]
----
```

And restores todos to the empty sections.

## Troubleshooting

- **"Activities directory not found"**: Make sure you're running from the vault root
- **"Daily note does not exist"**: The utility only restores to existing daily notes
- **"Activity section not found"**: The daily note must have the activity section header
- **"Already has todos, skipping"**: The utility won't overwrite existing todos

Run with `--dry-run` first to see what would be changed!
