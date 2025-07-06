#!/usr/bin/env python3
"""
Activity Todos Restoration Utility

This script reads all Activity files in the vault and restores todos to the corresponding daily notes
based on the date markers found in each activity file.

Usage: 
  python restore_activity_todos.py --dry-run    # Preview changes without making them
  python restore_activity_todos.py --confirm    # Make changes with confirmation
  python restore_activity_todos.py --auto       # Make changes automatically
"""

import os
import re
import glob
import argparse
import shutil
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Union
from datetime import datetime

class ActivityTodosRestorer:
    def __init__(self, vault_path: str = "..", dry_run: bool = True):
        # Since script is in Engine folder, vault root is one level up
        self.vault_path = Path(vault_path).resolve()
        self.activities_path = self.vault_path / "Activities"
        self.journal_path = self.vault_path / "Journal"
        self.dry_run = dry_run
        self.backup_dir = None
        self.backed_up_files = set()
        
    def read_file(self, file_path: Path) -> str:
        """Read file content safely"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return ""
    
    def create_backup_dir(self) -> Path:
        """Create backup directory with timestamp in script directory"""
        if self.backup_dir is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            script_dir = Path(__file__).parent  # Engine directory
            self.backup_dir = script_dir / f"restore_todos_backup_{timestamp}"
            
            if not self.dry_run:
                self.backup_dir.mkdir(parents=True, exist_ok=True)
                print(f"📦 Created backup directory: {self.backup_dir}")
        
        return self.backup_dir

    def backup_file(self, file_path: Path) -> bool:
        """Create backup of file before modification"""
        if self.dry_run or str(file_path) in self.backed_up_files:
            return True
        
        try:
            backup_dir = self.create_backup_dir()
            
            # Create relative path structure in backup
            relative_path = file_path.relative_to(self.vault_path)
            backup_file_path = backup_dir / relative_path
            
            # Create backup directory structure
            backup_file_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Copy file to backup
            shutil.copy2(file_path, backup_file_path)
            self.backed_up_files.add(str(file_path))
            print(f"  💾 Backed up: {relative_path}")
            return True
            
        except Exception as e:
            print(f"  ⚠️  Failed to backup {file_path}: {e}")
            return False

    def write_file(self, file_path: Path, content: str) -> bool:
        """Write file content safely with backup"""
        if self.dry_run:
            print(f"  [DRY RUN] Would write to: {file_path}")
            return True
        
        # Create backup before modifying
        if file_path.exists():
            self.backup_file(file_path)
            
        try:
            # Create directory if it doesn't exist
            file_path.parent.mkdir(parents=True, exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        except Exception as e:
            print(f"Error writing {file_path}: {e}")
            return False
    
    def extract_activity_todos(self, activity_file: Path) -> Dict[str, List[str]]:
        """Extract todos from activity file organized by date"""
        content = self.read_file(activity_file)
        if not content:
            return {}
        
        # Find all date markers and their associated todos
        date_todos = {}
        
        # Pattern to match date markers like [[2025-07-04]]
        date_pattern = r'\[\[(\d{4}-\d{2}-\d{2})\]\]'
        
        # Split content by date markers
        parts = re.split(date_pattern, content)
        
        # Process parts in pairs (date, content)
        for i in range(1, len(parts), 2):
            if i + 1 < len(parts):
                date = parts[i]
                section_content = parts[i + 1]
                
                # Extract todos from this section
                todos = self.extract_todos_from_section(section_content)
                if todos:
                    date_todos[date] = todos
        
        return date_todos
    
    def extract_todos_from_section(self, section: str) -> List[str]:
        """Extract todo items from a section of text"""
        todos = []
        lines = section.split('\n')
        
        for line in lines:
            line = line.strip()
            # Match todo items: - [ ] or - [x]
            if re.match(r'^- \[[x ]\]', line):
                todos.append(line)
        
        return todos
    
    def get_daily_note_path(self, date: str) -> Optional[Path]:
        """Get the path to a daily note based on date"""
        try:
            # Parse date
            date_obj = datetime.strptime(date, '%Y-%m-%d')
            year = date_obj.year
            month_num = date_obj.month
            month_name = date_obj.strftime('%m.%B')
            
            # Construct path: Journal/2025/07.July/2025-07-05.md
            daily_note_path = self.journal_path / str(year) / month_name / f"{date}.md"
            return daily_note_path
            
        except ValueError as e:
            print(f"Invalid date format {date}: {e}")
            return None

    def create_daily_note(self, date: str, confirm: bool = False) -> bool:
        """Create a new daily note with proper structure"""
        daily_note_path = self.get_daily_note_path(date)
        if not daily_note_path:
            return False
        
        if daily_note_path.exists():
            return True  # Already exists
        
        try:
            # Parse date for formatting
            date_obj = datetime.strptime(date, '%Y-%m-%d')
            day = date_obj.strftime('%d')
            month_name = date_obj.strftime('%B')
            year = date_obj.year
            
            # Calculate week number
            week_num = date_obj.isocalendar()[1]
            
            # Create daily note content
            daily_note_content = f"""---
---
### {day} [[{year}-{date_obj.strftime('%m')}|{month_name}]] [[{year}]]
#### Week: [[{year}-W{week_num:02d}|{week_num}]]

----

### Activities:
----

"""
            
            # Ask for confirmation if needed
            if confirm and not self.dry_run:
                response = input(f"  ❓ Create missing daily note {daily_note_path.name}? (y/N): ").strip().lower()
                if response != 'y':
                    print(f"  ⏭️  Skipped creating daily note {daily_note_path.name}")
                    return False
            
            # Write the daily note
            if self.write_file(daily_note_path, daily_note_content):
                if self.dry_run:
                    print(f"  [DRY RUN] Would create daily note: {daily_note_path.name}")
                else:
                    print(f"  ✅ Created daily note: {daily_note_path.name}")
                return True
            else:
                print(f"  ❌ Failed to create daily note: {daily_note_path.name}")
                return False
                
        except Exception as e:
            print(f"  ❌ Error creating daily note for {date}: {e}")
            return False
    
    def find_activities_section(self, content: str) -> Tuple[int, int]:
        """Find the Activities section in daily note"""
        # Look for "### Activities:" section
        activities_match = re.search(r'^### Activities:\s*\n----\s*\n', content, re.MULTILINE)
        if not activities_match:
            return -1, -1
        
        start_pos = activities_match.end()
        
        # Find the end of Activities section (next ### section)
        remaining_content = content[start_pos:]
        next_section_match = re.search(r'\n\n### ', remaining_content)
        
        if next_section_match:
            end_pos = start_pos + next_section_match.start()
        else:
            end_pos = len(content)
        
        return start_pos, end_pos

    def find_activity_section_in_daily_note(self, content: str, activity_name: str) -> Tuple[int, int]:
        """Find the start and end positions of an activity section in daily note"""
        # Pattern to match activity header (without expecting immediate ----)
        pattern = rf'##### \[\[Activities/{re.escape(activity_name)}\.md\|{re.escape(activity_name)}\]\]'
        
        match = re.search(pattern, content)
        if not match:
            return -1, -1
        
        # Start position is after the header line
        header_end = match.end()
        # Find the end of the line
        newline_pos = content.find('\n', header_end)
        if newline_pos == -1:
            return -1, -1
        
        start_pos = newline_pos + 1
        
        # Find the end of this activity section (look for ---- that ends this activity)
        remaining_content = content[start_pos:]
        
        # Look for ---- that marks the end of this activity
        end_marker_match = re.search(r'^----\s*$', remaining_content, re.MULTILINE)
        
        if end_marker_match:
            end_pos = start_pos + end_marker_match.start()
        else:
            # Fallback: look for next activity or end of activities section
            next_activity_match = re.search(r'^##### \[\[Activities/', remaining_content, re.MULTILINE)
            if next_activity_match:
                end_pos = start_pos + next_activity_match.start()
            else:
                # Look for end of activities section
                end_match = re.search(r'\n\n### ', remaining_content)
                if end_match:
                    end_pos = start_pos + end_match.start()
                else:
                    end_pos = len(content)
        
        return start_pos, end_pos

    def create_activities_section(self, content: str) -> str:
        """Create Activities section if it doesn't exist"""
        # Look for a good place to insert Activities section
        # Try to insert after the header section but before other content
        
        # Find the end of the frontmatter and header
        lines = content.split('\n')
        insert_pos = 0
        
        # Skip frontmatter
        if lines[0].strip() == '---':
            for i in range(1, len(lines)):
                if lines[i].strip() == '---':
                    insert_pos = i + 1
                    break
        
        # Skip header lines (### date, #### week, etc.)
        while insert_pos < len(lines):
            line = lines[insert_pos].strip()
            if line.startswith('###') or line.startswith('####') or line == '----' or line == '':
                insert_pos += 1
            else:
                break
        
        # Insert Activities section
        activities_section = [
            '',
            '### Activities:',
            '----',
            ''
        ]
        
        new_lines = lines[:insert_pos] + activities_section + lines[insert_pos:]
        return '\n'.join(new_lines)

    def create_activity_subsection(self, content: str, activity_name: str, todos: List[str]) -> str:
        """Create a new activity subsection within the Activities section"""
        activities_start, activities_end = self.find_activities_section(content)
        
        if activities_start == -1:
            # Create Activities section first
            content = self.create_activities_section(content)
            activities_start, activities_end = self.find_activities_section(content)
        
        # Create the activity subsection with proper formatting
        activity_section = [
            f'##### [[Activities/{activity_name}.md|{activity_name}]]'
        ] + todos + [
            '----',
            ''  # Empty line after ----
        ]
        
        activity_text = '\n'.join(activity_section)
        
        # Insert at the end of Activities section (before the next ### section)
        new_content = content[:activities_end] + activity_text + content[activities_end:]
        
        return new_content
    
    def restore_todos_to_daily_note(self, daily_note_path: Path, activity_name: str, todos: List[str], confirm: bool = False) -> bool:
        """Restore todos to a specific activity section in a daily note"""
        if not daily_note_path.exists():
            print(f"  📅 Daily note does not exist: {daily_note_path.name}")
            
            # Extract date from filename for daily note creation
            date_str = daily_note_path.stem  # e.g., "2025-07-04"
            
            # Ask permission to create the daily note
            if confirm and not self.dry_run:
                response = input(f"  ❓ Create missing daily note {daily_note_path.name}? (y/N): ").strip().lower()
                if response != 'y':
                    print(f"  ⏭️  Skipped creating daily note {daily_note_path.name}")
                    return False
            
            # Create the daily note
            if not self.create_daily_note(date_str, confirm):
                print(f"  ❌ Failed to create daily note {daily_note_path.name}")
                return False
        
        content = self.read_file(daily_note_path)
        if not content:
            return False
        
        # Find the activity section
        start_pos, end_pos = self.find_activity_section_in_daily_note(content, activity_name)
        
        if start_pos == -1:
            print(f"  ⚠️  Activity section '{activity_name}' not found in {daily_note_path.name}")
            
            # Ask permission to create the activity section
            if confirm and not self.dry_run:
                response = input(f"  ❓ Create activity section '{activity_name}' in {daily_note_path.name}? (y/N): ").strip().lower()
                if response != 'y':
                    print(f"  ⏭️  Skipped creating section for '{activity_name}' in {daily_note_path.name}")
                    return False
            
            # Create the activity section
            print(f"  🔧 Creating activity section '{activity_name}' in {daily_note_path.name}")
            new_content = self.create_activity_subsection(content, activity_name, todos)
            
            # Write back to file
            if self.write_file(daily_note_path, new_content):
                if self.dry_run:
                    print(f"  [DRY RUN] Would create activity section and restore {len(todos)} todos for '{activity_name}' in {daily_note_path.name}")
                else:
                    print(f"  ✅ Created activity section and restored {len(todos)} todos for '{activity_name}' in {daily_note_path.name}")
                return True
            else:
                print(f"  ❌ Failed to create activity section for '{activity_name}' in {daily_note_path.name}")
                return False
        
        # Check if section already has todos
        section_content = content[start_pos:end_pos]
        if re.search(r'- \[[x ]\]', section_content):
            print(f"  ⏭️  Activity '{activity_name}' in {daily_note_path.name} already has todos, skipping")
            return False
        
        # Show what will be added
        print(f"  📝 Will add {len(todos)} todos to existing '{activity_name}' section in {daily_note_path.name}:")
        for todo in todos:
            print(f"    {todo}")
        
        if confirm and not self.dry_run:
            response = input(f"  ❓ Add these todos to {daily_note_path.name}? (y/N): ").strip().lower()
            if response != 'y':
                print(f"  ⏭️  Skipped {daily_note_path.name}")
                return False
        
        # Insert todos after the activity header
        todos_text = '\n'.join(todos) + '\n'
        new_content = content[:start_pos] + '\n' + todos_text + content[end_pos:]
        
        # Write back to file
        if self.write_file(daily_note_path, new_content):
            if self.dry_run:
                print(f"  [DRY RUN] Would restore {len(todos)} todos for '{activity_name}' in {daily_note_path.name}")
            else:
                print(f"  ✅ Restored {len(todos)} todos for '{activity_name}' in {daily_note_path.name}")
            return True
        else:
            print(f"  ❌ Failed to write todos for '{activity_name}' in {daily_note_path.name}")
            return False
    
    def process_activity_file(self, activity_file: Path, confirm: bool = False) -> int:
        """Process a single activity file and restore its todos"""
        activity_name = activity_file.stem
        print(f"\n📁 Processing activity: {activity_name}")
        
        # Extract todos organized by date
        date_todos = self.extract_activity_todos(activity_file)
        
        if not date_todos:
            print(f"  No dated todos found in {activity_name}")
            return 0
        
        restored_count = 0
        
        # Sort dates in ascending order
        sorted_dates = sorted(date_todos.keys())
        print(f"  📅 Found dates: {', '.join(sorted_dates)}")
        
        # Process each date in ascending order
        for date in sorted_dates:
            todos = date_todos[date]
            print(f"  📅 Date {date}: {len(todos)} todos")
            
            # Get daily note path
            daily_note_path = self.get_daily_note_path(date)
            if not daily_note_path:
                continue
            
            # Restore todos to daily note
            if self.restore_todos_to_daily_note(daily_note_path, activity_name, todos, confirm):
                restored_count += 1
        
        return restored_count
    
    def run(self, confirm: bool = False) -> Dict[str, Union[int, str, bool, List[str]]]:
        """Main restoration process"""
        mode_text = "[DRY RUN] " if self.dry_run else ""
        print(f"🔄 {mode_text}Starting Activity Todos Restoration...")
        print(f"📂 Vault path: {self.vault_path.absolute()}")
        print(f"📂 Activities path: {self.activities_path}")
        print(f"📂 Journal path: {self.journal_path}")
        
        if self.dry_run:
            print("🔍 DRY RUN MODE: No files will be modified")
        
        if not self.activities_path.exists():
            print(f"❌ Activities directory not found: {self.activities_path}")
            return {"error": "Activities directory not found"}
        
        if not self.journal_path.exists():
            print(f"❌ Journal directory not found: {self.journal_path}")
            return {"error": "Journal directory not found"}
        
        # Find all activity files recursively
        activity_files = list(self.activities_path.rglob("*.md"))
        print(f"📋 Found {len(activity_files)} activity files (including subfolders)")
        
        # Track summaries
        affected_daily_notes = set()
        used_activity_files = set()
        unused_activity_files = set()
        problematic_activity_files = set()
        activity_to_dates = {}
        date_to_activities = {}
        
        total_restored = 0
        processed_activities = 0
        
        # Process each activity file
        for activity_file in activity_files:
            try:
                activity_name = activity_file.stem
                relative_path = activity_file.relative_to(self.activities_path)
                
                # Try to extract todos
                date_todos = self.extract_activity_todos(activity_file)
                
                if date_todos:
                    used_activity_files.add(str(relative_path))
                    activity_to_dates[str(relative_path)] = sorted(date_todos.keys())
                    
                    for date in date_todos.keys():
                        daily_note_path = self.get_daily_note_path(date)
                        if daily_note_path:
                            # Include both existing and potentially created daily notes
                            affected_daily_notes.add(date)
                            if date not in date_to_activities:
                                date_to_activities[date] = []
                            date_to_activities[date].append(activity_name)
                else:
                    # Check if file has date markers but no todos (problematic format)
                    content = self.read_file(activity_file)
                    if re.search(r'\[\[(\d{4}-\d{2}-\d{2})\]\]', content):
                        problematic_activity_files.add(str(relative_path))
                    else:
                        unused_activity_files.add(str(relative_path))
                
                restored = self.process_activity_file(activity_file, confirm)
                total_restored += restored
                processed_activities += 1
            except Exception as e:
                print(f"❌ Error processing {activity_file.name}: {e}")
                problematic_activity_files.add(str(activity_file.relative_to(self.activities_path)))
        
        print(f"\n✅ {mode_text}Restoration complete!")
        print(f"📊 Summary:")
        print(f"   - Activities processed: {processed_activities}")
        print(f"   - Daily notes restored: {total_restored}")
        
        # Detailed summaries
        summary_content = self.print_detailed_summaries(used_activity_files, unused_activity_files, problematic_activity_files, 
                                    affected_daily_notes, activity_to_dates, date_to_activities)
        
        # Save summaries to file
        self.save_summary_to_file(summary_content, used_activity_files, unused_activity_files, 
                                 problematic_activity_files, affected_daily_notes, activity_to_dates, 
                                 date_to_activities, processed_activities, total_restored)
        
        if self.dry_run:
            print(f"\n💡 To actually make changes, run with --confirm or --auto")
        else:
            # Show backup information
            if self.backed_up_files:
                print(f"\n📦 BACKUP INFORMATION:")
                print(f"   💾 Backed up {len(self.backed_up_files)} files to: {self.backup_dir}")
                print(f"   🔄 To restore from backup, copy files back from backup directory")
        
        return {
            "activities_processed": processed_activities,
            "daily_notes_restored": total_restored,
            "used_activity_files": list(used_activity_files),
            "affected_daily_notes": sorted(list(affected_daily_notes)),
            "success": True
        }

    def print_detailed_summaries(self, used_activity_files: set, unused_activity_files: set, 
                                problematic_activity_files: set, affected_daily_notes: set, 
                                activity_to_dates: dict, date_to_activities: dict) -> str:
        """Print detailed summaries of what will be affected and return content for saving"""
        summary_lines = []
        
        print(f"\n" + "="*60)
        print(f"📋 DETAILED SUMMARIES")
        print(f"="*60)
        
        summary_lines.append("="*60)
        summary_lines.append("📋 DETAILED SUMMARIES")
        summary_lines.append("="*60)
        
        # Activity Files Used
        print(f"\n🗂️  ACTIVITY FILES USED ({len(used_activity_files)} files):")
        print(f"-" * 40)
        summary_lines.append(f"\n🗂️  ACTIVITY FILES USED ({len(used_activity_files)} files):")
        summary_lines.append("-" * 40)
        
        for activity_name in sorted(used_activity_files):
            dates = activity_to_dates.get(activity_name, [])
            date_range = f"{dates[0]} to {dates[-1]}" if len(dates) > 1 else dates[0] if dates else "No dates"
            print(f"   📁 {activity_name}")
            print(f"      📅 Dates: {', '.join(dates)} ({len(dates)} dates)")
            print(f"      📊 Range: {date_range}")
            print()
            
            summary_lines.append(f"   📁 {activity_name}")
            summary_lines.append(f"      📅 Dates: {', '.join(dates)} ({len(dates)} dates)")
            summary_lines.append(f"      📊 Range: {date_range}")
            summary_lines.append("")
        
        # Unused Activity Files
        if unused_activity_files:
            print(f"🚫 UNUSED ACTIVITY FILES ({len(unused_activity_files)} files):")
            print(f"-" * 40)
            print("   These files have no date markers [[YYYY-MM-DD]] with todos:")
            
            summary_lines.append(f"🚫 UNUSED ACTIVITY FILES ({len(unused_activity_files)} files):")
            summary_lines.append("-" * 40)
            summary_lines.append("   These files have no date markers [[YYYY-MM-DD]] with todos:")
            
            for activity_name in sorted(unused_activity_files):
                print(f"   📁 {activity_name}")
                summary_lines.append(f"   📁 {activity_name}")
            print()
            summary_lines.append("")
        
        # Problematic Activity Files
        if problematic_activity_files:
            print(f"⚠️  PROBLEMATIC ACTIVITY FILES ({len(problematic_activity_files)} files):")
            print(f"-" * 40)
            print("   These files have date markers but no todos or formatting issues:")
            
            summary_lines.append(f"⚠️  PROBLEMATIC ACTIVITY FILES ({len(problematic_activity_files)} files):")
            summary_lines.append("-" * 40)
            summary_lines.append("   These files have date markers but no todos or formatting issues:")
            
            for activity_name in sorted(problematic_activity_files):
                print(f"   📁 {activity_name}")
                summary_lines.append(f"   📁 {activity_name}")
            print()
            summary_lines.append("")
        
        # Daily Notes Affected
        print(f"📝 DAILY NOTES AFFECTED ({len(affected_daily_notes)} notes):")
        print(f"-" * 40)
        summary_lines.append(f"📝 DAILY NOTES AFFECTED ({len(affected_daily_notes)} notes):")
        summary_lines.append("-" * 40)
        
        # Group by month for better organization
        notes_by_month = {}
        for date in sorted(affected_daily_notes):
            month_key = date[:7]  # YYYY-MM
            if month_key not in notes_by_month:
                notes_by_month[month_key] = []
            notes_by_month[month_key].append(date)
        
        for month, dates in sorted(notes_by_month.items()):
            print(f"   📅 {month} ({len(dates)} notes):")
            summary_lines.append(f"   📅 {month} ({len(dates)} notes):")
            for date in dates:
                activities = date_to_activities.get(date, [])
                activities_text = ", ".join(sorted(activities))
                print(f"      • {date} → {len(activities)} activities: {activities_text}")
                summary_lines.append(f"      • {date} → {len(activities)} activities: {activities_text}")
            print()
            summary_lines.append("")
        
        # Summary Statistics
        print(f"📊 STATISTICS:")
        print(f"-" * 40)
        summary_lines.append(f"📊 STATISTICS:")
        summary_lines.append("-" * 40)
        
        total_files = len(used_activity_files) + len(unused_activity_files) + len(problematic_activity_files)
        print(f"   🗂️  Total activity files found: {total_files}")
        print(f"   ✅ Activity files with dated todos: {len(used_activity_files)}")
        print(f"   🚫 Activity files unused: {len(unused_activity_files)}")
        print(f"   ⚠️  Activity files with issues: {len(problematic_activity_files)}")
        print(f"   📝 Total daily notes to be modified: {len(affected_daily_notes)}")
        
        summary_lines.append(f"   🗂️  Total activity files found: {total_files}")
        summary_lines.append(f"   ✅ Activity files with dated todos: {len(used_activity_files)}")
        summary_lines.append(f"   🚫 Activity files unused: {len(unused_activity_files)}")
        summary_lines.append(f"   ⚠️  Activity files with issues: {len(problematic_activity_files)}")
        summary_lines.append(f"   📝 Total daily notes to be modified: {len(affected_daily_notes)}")
        
        if affected_daily_notes:
            date_range = f"{min(affected_daily_notes)} to {max(affected_daily_notes)}"
            print(f"   📅 Date range: {date_range}")
            summary_lines.append(f"   📅 Date range: {date_range}")
        
        # Activity usage statistics
        activity_usage = [(len(activity_to_dates.get(activity, [])), activity) for activity in used_activity_files]
        activity_usage.sort(reverse=True)
        
        print(f"   🔝 Most active (by date count):")
        summary_lines.append(f"   🔝 Most active (by date count):")
        for count, activity in activity_usage[:5]:
            print(f"      • {activity}: {count} dates")
            summary_lines.append(f"      • {activity}: {count} dates")
        
        print(f"\n" + "="*60)
        summary_lines.append("")
        summary_lines.append("="*60)
        
        return "\n".join(summary_lines)

    def save_summary_to_file(self, summary_content: str, used_activity_files: set, unused_activity_files: set,
                            problematic_activity_files: set, affected_daily_notes: set, activity_to_dates: dict,
                            date_to_activities: dict, processed_activities: int, total_restored: int):
        """Save detailed summary to a file in script directory"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        mode_suffix = "dry_run" if self.dry_run else "executed"
        summary_filename = f"activity_todos_restoration_summary_{timestamp}_{mode_suffix}.md"
        script_dir = Path(__file__).parent  # Engine directory
        summary_path = script_dir / summary_filename
        
        # Create comprehensive summary content
        full_summary = []
        full_summary.append(f"# Activity Todos Restoration Summary")
        full_summary.append(f"")
        full_summary.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        full_summary.append(f"**Mode:** {'DRY RUN' if self.dry_run else 'EXECUTED'}")
        full_summary.append(f"**Vault Path:** {self.vault_path.absolute()}")
        full_summary.append(f"")
        
        # Execution Summary
        full_summary.append(f"## Execution Summary")
        full_summary.append(f"")
        full_summary.append(f"- **Activities Processed:** {processed_activities}")
        full_summary.append(f"- **Daily Notes Restored:** {total_restored}")
        full_summary.append(f"- **Total Activity Files Found:** {len(used_activity_files) + len(unused_activity_files) + len(problematic_activity_files)}")
        full_summary.append(f"- **Files with Dated Todos:** {len(used_activity_files)}")
        full_summary.append(f"- **Unused Files:** {len(unused_activity_files)}")
        full_summary.append(f"- **Problematic Files:** {len(problematic_activity_files)}")
        full_summary.append(f"")
        
        if not self.dry_run and self.backed_up_files:
            full_summary.append(f"## Backup Information")
            full_summary.append(f"")
            full_summary.append(f"- **Backup Directory:** {self.backup_dir}")
            full_summary.append(f"- **Files Backed Up:** {len(self.backed_up_files)}")
            full_summary.append(f"")
            full_summary.append(f"### Backed Up Files:")
            for file_path in sorted(self.backed_up_files):
                relative_path = Path(file_path).relative_to(self.vault_path)
                full_summary.append(f"- {relative_path}")
            full_summary.append(f"")
        
        # Add the detailed summaries
        full_summary.append(summary_content)
        
        # Write to file
        summary_text = "\n".join(full_summary)
        
        try:
            with open(summary_path, 'w', encoding='utf-8') as f:
                f.write(summary_text)
            print(f"\n📄 Summary saved to: {summary_filename}")
        except Exception as e:
            print(f"\n⚠️  Failed to save summary to file: {e}")

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="Restore activity todos to daily notes")
    parser.add_argument("--dry-run", action="store_true", default=True, 
                       help="Preview changes without making them (default)")
    parser.add_argument("--confirm", action="store_true", 
                       help="Make changes with confirmation prompts")
    parser.add_argument("--auto", action="store_true", 
                       help="Make changes automatically without prompts")
    
    args = parser.parse_args()
    
    # Determine mode
    if args.auto:
        dry_run = False
        confirm = False
    elif args.confirm:
        dry_run = False
        confirm = True
    else:
        dry_run = True
        confirm = False
    
    print("🚀 Activity Todos Restoration Utility")
    print("=" * 50)
    
    if dry_run:
        print("🔍 Running in DRY RUN mode - no files will be modified")
    elif confirm:
        print("❓ Running in CONFIRM mode - will ask before each change")
    else:
        print("⚡ Running in AUTO mode - will make changes automatically")
    
    print()
    
    # Initialize restorer
    restorer = ActivityTodosRestorer(dry_run=dry_run)
    
    # Run restoration
    result = restorer.run(confirm=confirm)
    
    if result.get("success"):
        if dry_run:
            print(f"\n🔍 DRY RUN: Would restore todos to {result['daily_notes_restored']} daily notes!")
            print("💡 Run with --confirm to make changes with prompts, or --auto to make changes automatically")
        else:
            print(f"\n🎉 Successfully restored todos to {result['daily_notes_restored']} daily notes!")
    else:
        print(f"\n❌ Restoration failed: {result.get('error', 'Unknown error')}")

if __name__ == "__main__":
    main()
