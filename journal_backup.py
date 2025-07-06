#!/usr/bin/env python3
"""
Journal Backup Utility

This script creates compressed backups of the Journal directory in tar.gz format.
It creates timestamped backups and maintains detailed logs of the backup process.

Usage: 
  python journal_backup.py                    # Create backup with default settings
  python journal_backup.py --backup-dir ./backups  # Specify backup directory
  python journal_backup.py --compress-level 6      # Set compression level (1-9)
"""

import os
import sys
import tarfile
import argparse
import logging
from pathlib import Path
from datetime import datetime
from typing import Optional, Tuple, List
import shutil

class JournalBackup:
    def __init__(self, vault_path: str = "..", backup_dir: Optional[str] = None, compress_level: int = 6):
        # Since script is in Engine folder, vault root is one level up
        self.vault_path = Path(vault_path).resolve()
        self.journal_path = self.vault_path / "Journal"
        
        # Set backup directory (default to Engine/journal_backups)
        if backup_dir:
            self.backup_dir = Path(backup_dir).resolve()
        else:
            script_dir = Path(__file__).parent  # Engine directory
            self.backup_dir = script_dir / "journal_backups"
        
        self.compress_level = max(1, min(9, compress_level))  # Ensure 1-9 range
        self.logger = None
        self.backup_filename = None
        self.log_filename = None
        
    def setup_logging(self, log_file: Path) -> None:
        """Setup logging to both file and console"""
        # Create logger
        self.logger = logging.getLogger('journal_backup')
        self.logger.setLevel(logging.INFO)
        
        # Clear any existing handlers
        self.logger.handlers.clear()
        
        # Create formatters
        file_formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_formatter = logging.Formatter('%(message)s')
        
        # File handler
        file_handler = logging.FileHandler(log_file, mode='w', encoding='utf-8')
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)
    
    def log_info(self, message: str) -> None:
        """Log info message"""
        if self.logger:
            self.logger.info(message)
        else:
            print(message)
    
    def log_error(self, message: str) -> None:
        """Log error message"""
        if self.logger:
            self.logger.error(message)
        else:
            print(f"ERROR: {message}")
    
    def get_directory_size(self, path: Path) -> Tuple[int, int]:
        """Get total size and file count of directory"""
        total_size = 0
        file_count = 0
        
        try:
            for file_path in path.rglob('*'):
                if file_path.is_file():
                    total_size += file_path.stat().st_size
                    file_count += 1
        except Exception as e:
            self.log_error(f"Error calculating directory size: {e}")
        
        return total_size, file_count
    
    def format_size(self, size_bytes: int) -> str:
        """Format size in human readable format"""
        size = float(size_bytes)
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} TB"
    
    def get_journal_structure(self) -> List[str]:
        """Get Journal directory structure for logging"""
        structure = []
        try:
            for item in sorted(self.journal_path.rglob('*')):
                if item.is_dir():
                    relative_path = item.relative_to(self.journal_path)
                    level = len(relative_path.parts)
                    indent = "  " * level
                    structure.append(f"{indent}📁 {item.name}/")
                elif item.is_file() and item.suffix == '.md':
                    relative_path = item.relative_to(self.journal_path)
                    level = len(relative_path.parts) - 1
                    indent = "  " * (level + 1)
                    file_size = item.stat().st_size
                    structure.append(f"{indent}📄 {item.name} ({self.format_size(file_size)})")
        except Exception as e:
            structure.append(f"Error reading structure: {e}")
        
        return structure
    
    def create_backup(self) -> bool:
        """Create compressed backup of Journal directory"""
        if not self.journal_path.exists():
            self.log_error(f"Journal directory not found: {self.journal_path}")
            return False
        
        if not self.journal_path.is_dir():
            self.log_error(f"Journal path is not a directory: {self.journal_path}")
            return False
        
        # Create backup directory if it doesn't exist
        try:
            self.backup_dir.mkdir(parents=True, exist_ok=True)
            self.log_info(f"📁 Backup directory: {self.backup_dir}")
        except Exception as e:
            self.log_error(f"Failed to create backup directory: {e}")
            return False
        
        # Generate backup filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.backup_filename = f"journal_backup_{timestamp}.tar.gz"
        backup_path = self.backup_dir / self.backup_filename
        
        # Check if backup already exists
        if backup_path.exists():
            self.log_error(f"Backup file already exists: {backup_path}")
            return False
        
        # Get source directory info
        source_size, file_count = self.get_directory_size(self.journal_path)
        self.log_info(f"📊 Source: {self.journal_path}")
        self.log_info(f"📊 Files to backup: {file_count}")
        self.log_info(f"📊 Total size: {self.format_size(source_size)}")
        self.log_info(f"🗜️  Compression level: {self.compress_level}")
        self.log_info("")
        
        # Log directory structure
        self.log_info("📋 Journal Directory Structure:")
        self.log_info("-" * 40)
        structure = self.get_journal_structure()
        for line in structure[:50]:  # Limit to first 50 lines to avoid huge logs
            self.log_info(line)
        if len(structure) > 50:
            self.log_info(f"... and {len(structure) - 50} more items")
        self.log_info("")
        
        # Create backup
        self.log_info(f"🔄 Creating backup: {self.backup_filename}")
        self.log_info(f"📦 Target: {backup_path}")
        
        try:
            start_time = datetime.now()
            
            with tarfile.open(backup_path, 'w:gz', compresslevel=self.compress_level) as tar:
                # Add progress tracking
                files_processed = 0
                
                def progress_filter(tarinfo):
                    nonlocal files_processed
                    files_processed += 1
                    if files_processed % 10 == 0:  # Log every 10 files
                        self.log_info(f"  📄 Processed {files_processed} files...")
                    return tarinfo
                
                # Add the entire Journal directory to the archive
                tar.add(
                    self.journal_path, 
                    arcname="Journal",  # This will be the root folder name in the archive
                    filter=progress_filter
                )
            
            end_time = datetime.now()
            duration = end_time - start_time
            
            # Get backup file size
            backup_size = backup_path.stat().st_size
            compression_ratio = (1 - backup_size / source_size) * 100 if source_size > 0 else 0
            
            self.log_info("")
            self.log_info("✅ Backup completed successfully!")
            self.log_info(f"📊 Backup Statistics:")
            self.log_info(f"   📁 Files processed: {files_processed}")
            self.log_info(f"   📏 Original size: {self.format_size(source_size)}")
            self.log_info(f"   🗜️  Compressed size: {self.format_size(backup_size)}")
            self.log_info(f"   📉 Compression ratio: {compression_ratio:.1f}%")
            self.log_info(f"   ⏱️  Duration: {duration.total_seconds():.1f} seconds")
            self.log_info(f"   💾 Backup file: {backup_path}")
            
            return True
            
        except Exception as e:
            self.log_error(f"Failed to create backup: {e}")
            # Clean up partial backup file
            if backup_path.exists():
                try:
                    backup_path.unlink()
                    self.log_info("🧹 Cleaned up partial backup file")
                except Exception as cleanup_error:
                    self.log_error(f"Failed to clean up partial backup: {cleanup_error}")
            return False
    
    def list_existing_backups(self) -> List[Tuple[Path, datetime, int]]:
        """List existing backup files with their info"""
        backups = []
        
        if not self.backup_dir.exists():
            return backups
        
        try:
            for backup_file in self.backup_dir.glob("journal_backup_*.tar.gz"):
                try:
                    # Extract timestamp from filename
                    timestamp_str = backup_file.stem.replace("journal_backup_", "").replace(".tar", "")
                    timestamp = datetime.strptime(timestamp_str, "%Y%m%d_%H%M%S")
                    size = backup_file.stat().st_size
                    backups.append((backup_file, timestamp, size))
                except Exception as e:
                    self.log_error(f"Error processing backup file {backup_file}: {e}")
        except Exception as e:
            self.log_error(f"Error listing backups: {e}")
        
        # Sort by timestamp (newest first)
        backups.sort(key=lambda x: x[1], reverse=True)
        return backups
    
    def run(self) -> bool:
        """Main backup process"""
        # Generate log filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_filename = f"journal_backup_{timestamp}.log"
        log_path = self.backup_dir / self.log_filename
        
        # Create backup directory for log file
        try:
            self.backup_dir.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            print(f"ERROR: Failed to create backup directory: {e}")
            return False
        
        # Setup logging
        self.setup_logging(log_path)
        
        self.log_info("🚀 Journal Backup Utility")
        self.log_info("=" * 50)
        self.log_info(f"📅 Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        self.log_info(f"🏠 Vault path: {self.vault_path}")
        self.log_info(f"📂 Journal path: {self.journal_path}")
        self.log_info(f"💾 Backup directory: {self.backup_dir}")
        self.log_info(f"📝 Log file: {log_path}")
        self.log_info("")
        
        # List existing backups
        existing_backups = self.list_existing_backups()
        if existing_backups:
            self.log_info(f"📋 Existing backups ({len(existing_backups)}):")
            for backup_file, backup_time, backup_size in existing_backups[:5]:  # Show last 5
                self.log_info(f"   📦 {backup_file.name} - {backup_time.strftime('%Y-%m-%d %H:%M:%S')} ({self.format_size(backup_size)})")
            if len(existing_backups) > 5:
                self.log_info(f"   ... and {len(existing_backups) - 5} more backups")
            self.log_info("")
        
        # Create backup
        success = self.create_backup()
        
        self.log_info("")
        self.log_info("=" * 50)
        if success:
            self.log_info("🎉 Journal backup completed successfully!")
            self.log_info(f"📦 Backup file: {self.backup_filename}")
            self.log_info(f"📝 Log file: {self.log_filename}")
        else:
            self.log_info("❌ Journal backup failed!")
        
        self.log_info(f"🏁 Finished: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        return success

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="Create compressed backup of Journal directory")
    parser.add_argument("--backup-dir", type=str, 
                       help="Directory to store backups (default: Engine/journal_backups)")
    parser.add_argument("--compress-level", type=int, default=6, choices=range(1, 10),
                       help="Compression level 1-9 (default: 6)")
    parser.add_argument("--vault-path", type=str, default="..",
                       help="Path to vault root (default: .. from Engine directory)")
    
    args = parser.parse_args()
    
    print("🚀 Journal Backup Utility")
    print("=" * 50)
    
    # Initialize backup utility
    backup = JournalBackup(
        vault_path=args.vault_path,
        backup_dir=args.backup_dir,
        compress_level=args.compress_level
    )
    
    # Run backup
    success = backup.run()
    
    if success:
        print(f"\n🎉 Backup completed successfully!")
        print(f"📁 Check backup directory: {backup.backup_dir}")
    else:
        print(f"\n❌ Backup failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
