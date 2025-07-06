# PDF Converter for Documentation

This directory contains tools to convert the README.md documentation to PDF format.

## ⚠️ Important Notice
**wkhtmltopdf has been discontinued** as of December 2024. The full-featured PDF converter (Option 1) may not work on newer systems. **We recommend using Option 2 (Simple HTML Converter)** as the primary solution.

## Option 1: Improved PDF Converter (Recommended) ✅

**NEW**: Enhanced converter that works without wkhtmltopdf!

### Features
- **No wkhtmltopdf dependency** - uses modern Python libraries
- **Multiple PDF engines**: WeasyPrint (recommended), ReportLab, or fallback to HTML
- **Professional formatting** with enhanced CSS and typography
- **Table of contents** generation with clickable navigation
- **Page breaks** and print optimization
- **Syntax highlighting** for code blocks
- **Automatic fallback** to HTML if no PDF libraries available

### Requirements & Installation

#### Option A: WeasyPrint (Recommended - No System Dependencies)
```bash
# Create virtual environment
python3 -m venv pdf_converter_env
source pdf_converter_env/bin/activate

# Install packages
pip install markdown weasyprint beautifulsoup4 pygments

# Run the improved converter
python3 markdown_to_pdf_improved.py

# Deactivate when done
deactivate
```

#### Option B: ReportLab (Alternative)
```bash
# Create virtual environment
python3 -m venv pdf_converter_env
source pdf_converter_env/bin/activate

# Install packages
pip install markdown reportlab beautifulsoup4 pygments

# Run the improved converter
python3 markdown_to_pdf_improved.py

# Deactivate when done
deactivate
```

#### Option C: HTML Fallback (No PDF Libraries)
```bash
# Install only core packages
pip install markdown beautifulsoup4 pygments

# Run converter (will output HTML)
python3 markdown_to_pdf_improved.py
```

### Usage
```bash
# Convert README.md to README.pdf
python3 markdown_to_pdf_improved.py

# Convert with custom output name
python3 markdown_to_pdf_improved.py -o PKM_Developer_Manual.pdf

# Convert different file
python3 markdown_to_pdf_improved.py -i README.md -o manual.pdf

# Show help
python3 markdown_to_pdf_improved.py --help
```

## Option 2: Full-Featured PDF Converter (Legacy - May Not Work)

### Requirements

#### Option A: Using Virtual Environment (Recommended)
```bash
# Create and activate virtual environment
python3 -m venv pdf_converter_env
source pdf_converter_env/bin/activate

# Install Python packages
pip install markdown pdfkit beautifulsoup4 pygments

# Install wkhtmltopdf (required by pdfkit)
# ⚠️ WARNING: wkhtmltopdf has been discontinued as of Dec 2024
# This may not work on newer systems
# macOS (may fail):
brew install wkhtmltopdf

# Run the converter
python3 markdown_to_pdf.py

# Deactivate when done
deactivate
```

#### Option B: Using pipx (Application-focused)
```bash
# Install pipx if not already installed
brew install pipx

# Install packages globally with pipx
pipx install markdown
pipx install pdfkit
pipx install beautifulsoup4
pipx install pygments

# Install wkhtmltopdf (⚠️ discontinued)
brew install wkhtmltopdf
```

#### Option C: System-wide Installation (Not Recommended)
```bash
# Only if you understand the risks
pip install --user markdown pdfkit beautifulsoup4 pygments

# Or with break-system-packages (risky)
pip install --break-system-packages markdown pdfkit beautifulsoup4 pygments

# Install wkhtmltopdf (⚠️ discontinued)  
brew install wkhtmltopdf
```

#### Linux/Ubuntu
```bash
# Install system packages
sudo apt-get install wkhtmltopdf python3-pip python3-venv

# Create virtual environment
python3 -m venv pdf_converter_env
source pdf_converter_env/bin/activate
pip install markdown pdfkit beautifulsoup4 pygments
```

#### Windows
```bash
# Download and install wkhtmltopdf from https://wkhtmltopdf.org/downloads.html
# Create virtual environment
python -m venv pdf_converter_env
pdf_converter_env\Scripts\activate
pip install markdown pdfkit beautifulsoup4 pygments
```

### Usage
```bash
# Convert README.md to README.pdf
python3 markdown_to_pdf.py

# Convert with custom output name
python3 markdown_to_pdf.py -o PKM_Developer_Manual.pdf

# Convert different file
python3 markdown_to_pdf.py -i README.md -o manual.pdf

# Show help
python3 markdown_to_pdf.py --help
```

### Features
- Professional PDF formatting with custom CSS
- Syntax highlighting for code blocks
- Table of contents generation
- Page numbers and headers/footers
- Optimized for printing and digital viewing

## Option 3: Simple HTML Converter (No Dependencies)

If you can't install the required packages, use the enhanced HTML converter:

```bash
# Convert README.md to HTML (opens in browser for PDF printing)
python3 simple_html_converter.py
```

Then use your browser's "Print to PDF" function.

### Enhanced Features:
- **Professional styling** with modern CSS design
- **Proper markdown parsing** including:
  - Code blocks with syntax highlighting classes
  - Nested lists with correct indentation
  - Tables with alternating row colors
  - Blockquotes with elegant styling
  - Bold, italic, strikethrough formatting
  - Links that open in new tabs
  - Horizontal rules with gradient styling
- **Table of contents** with clickable navigation
- **Print-optimized** CSS for perfect PDF output
- **No external dependencies** - pure Python standard library

## Option 4: Online Converters

You can also use online markdown to PDF converters:
1. Copy the content of README.md
2. Paste into online converters like:
   - https://www.markdowntopdf.com/
   - https://md-to-pdf.fly.dev/
   - https://dillinger.io/ (export as PDF)

## Output

The generated PDF will include:
- Professional title page with generation date
- Complete table of contents with page numbers
- Syntax-highlighted code examples
- Properly formatted tables and lists
- Page numbers and document structure
- Optimized typography for readability

## File Structure

```
Engine/
├── README.md                       # Main documentation (renamed from DEVELOPER_MANUAL.md)
├── markdown_to_pdf_improved.py    # Improved PDF converter (recommended)
├── markdown_to_pdf.py             # Legacy PDF converter (requires wkhtmltopdf)
├── simple_html_converter.py       # Simple HTML converter (no dependencies)
├── README_PDF_CONVERTER.md        # This file
└── PKM_Developer_Manual.pdf       # Generated PDF output
```

## Troubleshooting

### Common Issues

1. **"externally-managed-environment" Error (macOS/Linux)**
   ```
   error: externally-managed-environment
   × This environment is externally managed
   ```
   **Solution**: Use a virtual environment (recommended):
   ```bash
   python3 -m venv pdf_converter_env
   source pdf_converter_env/bin/activate
   pip install markdown pdfkit beautifulsoup4 pygments
   python3 markdown_to_pdf.py
   deactivate
   ```
   
   **Alternative**: Use the simple HTML converter (no dependencies required):
   ```bash
   python3 simple_html_converter.py
   ```

2. **"wkhtmltopdf not found" or "Cask 'wkhtmltopdf' has been disabled"**
   ```
   Error: Cask 'wkhtmltopdf' has been disabled because it is discontinued upstream!
   ```
   **Solution**: wkhtmltopdf has been discontinued as of December 2024. Use alternatives:
   
   **Recommended**: Use the simple HTML converter:
   ```bash
   python3 simple_html_converter.py
   ```
   
   **Alternative**: Install wkhtmltopdf manually from archived releases:
   - Download from: https://github.com/wkhtmltopdf/packaging/releases
   - Or use Docker: `docker run --rm -v $(pwd):/workspace surnet/alpine-wkhtmltopdf`

3. **"No module named 'markdown'"**
   - Install required Python packages in a virtual environment
   - Or use the simple HTML converter as fallback

4. **Permission denied**
   - Make script executable: `chmod +x markdown_to_pdf.py`

5. **PDF generation fails**
   - Try the simple HTML converter as fallback
   - Check that all dependencies are properly installed

### Alternative Methods

If the Python script doesn't work, you can:
1. Open README.md in any markdown viewer (like Typora, Mark Text, or VS Code preview)
2. Use the print function to save as PDF
3. Use online markdown to PDF converters
4. Use pandoc: `pandoc README.md -o README.pdf` (if installed)

## Support

The PDF converter includes comprehensive error handling and will guide you through any missing dependencies or configuration issues.
