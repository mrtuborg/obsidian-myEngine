# Development Environment Configuration

## System Information
**Last Updated:** July 24, 2025
**Operating System:** macOS
**Development Machine:** Mac with Python 3.13

## Project Setup
**Project Directory:** `/Users/vn/2ndBrain/Engine`
**Context Directory:** `/Users/vn/2ndBrain/Engine/LM_context`

## Development Tools
- **IDE/Editor:** VSCode
- **Version Control:** Git
- **Package Manager:** pip (Python), npm (Node.js)
- **Build Tools:** Native macOS development tools
- **Obsidian:** Primary application for PKM system

## Dependencies
- **Language:** Python 3.13+, JavaScript (ES6+)
- **Key Libraries:** 
  - Moment.js (date manipulation)
  - DataviewJS (Obsidian plugin)
  - CustomJS (Obsidian plugin)
- **System Dependencies:** 
  - Obsidian application
  - Node.js (for JavaScript development)

## Network Configuration
- **Development Machine IP:** Local development only
- **Target Devices:** None (local Obsidian vault)
- **Ports Used:** None (file-based system)

## Hardware Requirements
- **Minimum RAM:** 4GB (8GB recommended for large vaults)
- **Storage:** 1GB free space (varies with vault size)
- **Special Hardware:** None

## Environment Variables
[CUSTOMIZE: Any required environment variables]
```bash
export PROJECT_ROOT="/Users/vn/2ndBrain/Engine"
export CONTEXT_DIR="/Users/vn/2ndBrain/Engine/LM_context"
# Add other environment variables as needed
```

## Installation Instructions

### 1. Clone/Setup Project
```bash
cd /Users/vn/2ndBrain/Engine
# Project is already set up with LLM Context Management System
# Ensure all directories are present: Scripts/, Templates/, LM_context/
```

### 2. Install Dependencies
```bash
# Ensure Python 3.13+ is available
python3 --version

# Install Obsidian plugins:
# - DataviewJS
# - CustomJS
# - Configure CustomJS to load all Scripts/ modules
```

### 3. Verify Installation
```bash
# Verify LLM Context system
python3 LM_context/dynamic/assumption-validator.py --health-check

# Test basic functionality in Obsidian:
# - Create daily note from DailyNote-template.md
# - Create activity from Activity-template.md
# - Verify DataviewJS processing works
```

## Troubleshooting

### Common Issues
- **DataviewJS not processing:** Check that DataviewJS plugin is enabled and JavaScript execution is allowed
  - **Solution:** Enable DataviewJS in Obsidian settings, restart Obsidian
- **CustomJS modules not loading:** Verify Scripts/ directory is configured in CustomJS settings
  - **Solution:** Add all .js files in Scripts/ to CustomJS configuration
- **Template processing fails:** Check for syntax errors in JavaScript components
  - **Solution:** Use browser console (F12) to debug JavaScript errors
- **File permissions issues:** Ensure Obsidian has read/write access to vault directory
  - **Solution:** Check macOS file permissions for vault directory

## Performance Considerations
- **CPU Usage:** Low baseline, spikes during note processing (DataviewJS execution)
- **Memory Usage:** 100-500MB depending on vault size and active processing
- **Disk Usage:** Minimal additional storage for processed content and backups
- **Processing Time:** Scales with number of journal pages (typically <2s for <1000 notes)

---

**Environment Status:** ✅ Ready for development  
**Last Verified:** July 24, 2025  
**Next Review:** [Set a date for next environment review]
