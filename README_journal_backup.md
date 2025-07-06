# Journal Backup Utility

A Python utility to create compressed backups of your Obsidian Journal directory with detailed logging.

## Features

- **Compressed Backups**: Creates tar.gz archives with configurable compression levels
- **Timestamped Files**: Automatic timestamping prevents overwriting existing backups
- **Detailed Logging**: Comprehensive logs saved alongside backups
- **Progress Tracking**: Real-time progress updates during backup creation
- **Directory Structure**: Logs complete Journal directory structure
- **Backup Management**: Lists existing backups with timestamps and sizes
- **Error Handling**: Robust error handling with cleanup of partial backups

## Usage

### Basic Usage
```bash
cd Engine
python journal_backup.py
```

### Advanced Options
```bash
# Specify custom backup directory
python journal_backup.py --backup-dir /path/to/backups

# Set compression level (1-9, default: 6)
python journal_backup.py --compress-level 9

# Specify vault path (if running from different location)
python journal_backup.py --vault-path /path/to/vault
```

## File Structure

The utility creates the following structure in the Engine directory:

```
Engine/
├── journal_backup.py                           ← Main script
├── README_journal_backup.md                    ← This documentation
└── journal_backups/                            ← Default backup directory
    ├── journal_backup_20250706_131500.tar.gz   ← Compressed backup
    ├── journal_backup_20250706_131500.log      ← Detailed log
    ├── journal_backup_20250705_094500.tar.gz   ← Previous backup
    └── journal_backup_20250705_094500.log      ← Previous log
```

## Backup Contents

Each backup contains:
- **Complete Journal Directory**: All subdirectories and files
- **Preserved Structure**: Maintains original folder hierarchy
- **Markdown Files**: All .md files with full content
- **Metadata**: File timestamps and permissions preserved

## Log File Contents

Each log file includes:
- **Execution Summary**: Start/end times, success status
- **Directory Structure**: Complete Journal folder tree
- **File Statistics**: File count, sizes, compression ratios
- **Progress Updates**: Real-time backup progress
- **Error Details**: Any issues encountered during backup
- **Existing Backups**: List of previous backups

### Sample Log Output
```
🚀 Journal Backup Utility
==================================================
📅 Started: 2025-07-06 13:15:00
🏠 Vault path: /Users/vn/2ndBrain
📂 Journal path: /Users/vn/2ndBrain/Journal
💾 Backup directory: /Users/vn/2ndBrain/Engine/journal_backups
📝 Log file: /Users/vn/2ndBrain/Engine/journal_backups/journal_backup_20250706_131500.log

📋 Existing backups (2):
   📦 journal_backup_20250705_094500.tar.gz - 2025-07-05 09:45:00 (2.3 MB)
   📦 journal_backup_20250704_183000.tar.gz - 2025-07-04 18:30:00 (2.1 MB)

📊 Source: /Users/vn/2ndBrain/Journal
📊 Files to backup: 156
📊 Total size: 3.2 MB
🗜️  Compression level: 6

📋 Journal Directory Structure:
----------------------------------------
📁 2024/
  📁 07.July/
    📄 2024-07-01.md (2.1 KB)
    📄 2024-07-02.md (1.8 KB)
  📁 08.August/
    📄 2024-08-15.md (3.2 KB)
📁 2025/
  📁 06.June/
    📄 2025-06-27.md (4.1 KB)
  📁 07.July/
    📄 2025-07-01.md (2.8 KB)
    📄 2025-07-02.md (3.5 KB)

🔄 Creating backup: journal_backup_20250706_131500.tar.gz
📦 Target: /Users/vn/2ndBrain/Engine/journal_backups/journal_backup_20250706_131500.tar.gz
  📄 Processed 10 files...
  📄 Processed 20 files...
  📄 Processed 30 files...
  ...
  📄 Processed 150 files...

✅ Backup completed successfully!
📊 Backup Statistics:
   📁 Files processed: 156
   📏 Original size: 3.2 MB
   🗜️  Compressed size: 1.1 MB
   📉 Compression ratio: 65.6%
   ⏱️  Duration: 2.3 seconds
   💾 Backup file: /Users/vn/2ndBrain/Engine/journal_backups/journal_backup_20250706_131500.tar.gz

==================================================
🎉 Journal backup completed successfully!
📦 Backup file: journal_backup_20250706_131500.tar.gz
📝 Log file: journal_backup_20250706_131500.log
🏁 Finished: 2025-07-06 13:15:02
```

## Compression Levels

Choose compression level based on your needs:

| Level | Speed | Compression | Use Case |
|-------|-------|-------------|----------|
| 1     | Fastest | Lowest | Quick backups, large files |
| 3     | Fast | Low | Regular backups |
| 6     | Balanced | Good | **Default - recommended** |
| 9     | Slowest | Highest | Archival, storage-constrained |

## Restoring from Backup

To restore from a backup:

```bash
# Extract to current directory
tar -xzf journal_backup_20250706_131500.tar.gz

# Extract to specific location
tar -xzf journal_backup_20250706_131500.tar.gz -C /path/to/restore/location

# List contents without extracting
tar -tzf journal_backup_20250706_131500.tar.gz
```

## Automation

### Daily Backup (cron)
```bash
# Add to crontab for daily backup at 2 AM
0 2 * * * cd /path/to/vault/Engine && python journal_backup.py
```

### Weekly Backup with High Compression
```bash
# Weekly backup with maximum compression
0 3 * * 0 cd /path/to/vault/Engine && python journal_backup.py --compress-level 9
```

## Error Handling

The utility handles various error conditions:
- **Missing Journal Directory**: Exits with clear error message
- **Permission Issues**: Reports access problems
- **Disk Space**: Handles insufficient storage
- **Partial Backups**: Cleans up incomplete files
- **Existing Files**: Prevents overwriting existing backups

## Best Practices

1. **Regular Backups**: Run daily or weekly depending on usage
2. **Monitor Logs**: Check log files for any issues
3. **Test Restores**: Periodically test backup restoration
4. **Storage Management**: Clean up old backups to save space
5. **Compression Balance**: Use level 6 for most cases
6. **Backup Location**: Store backups on different drive/location

## Troubleshooting

### Common Issues

**"Journal directory not found"**
- Ensure you're running from the Engine directory
- Check that Journal directory exists in vault root

**"Permission denied"**
- Ensure write permissions to backup directory
- Check file system permissions

**"Backup file already exists"**
- Backups are timestamped to prevent conflicts
- If seeing this error, check system clock

**"Failed to create backup directory"**
- Check parent directory permissions
- Ensure sufficient disk space

### Debug Mode
For troubleshooting, check the detailed log file created alongside each backup.

## Integration

This utility works alongside other Engine tools:
- **restore_activity_todos.py**: Restore todos before backing up
- **Other Scripts**: Can be integrated into larger backup workflows

## Requirements

- Python 3.6+
- Standard library modules (no external dependencies)
- Read access to Journal directory
- Write access to backup directory
