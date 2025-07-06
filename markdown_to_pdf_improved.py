#!/usr/bin/env python3
"""
Improved Markdown to PDF Converter
Converts the README.md documentation to a professional PDF format without wkhtmltopdf dependency.

Requirements (choose one):
    Option 1 (Recommended): pip install markdown weasyprint beautifulsoup4 pygments
    Option 2: pip install markdown reportlab beautifulsoup4 pygments
    Option 3 (Fallback): pip install markdown beautifulsoup4 pygments (HTML output only)

No external system dependencies required!
"""

import os
import sys
import subprocess
from datetime import datetime
from pathlib import Path
import argparse
import tempfile
import webbrowser

# Check for available PDF libraries
PDF_LIBRARIES = {
    'weasyprint': False,
    'reportlab': False,
    'pdfkit': False
}

try:
    import weasyprint
    PDF_LIBRARIES['weasyprint'] = True
    print("✅ WeasyPrint available")
except ImportError:
    pass

try:
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.lib import colors
    PDF_LIBRARIES['reportlab'] = True
    print("✅ ReportLab available")
except ImportError:
    pass

try:
    import pdfkit
    PDF_LIBRARIES['pdfkit'] = True
    print("✅ PDFKit available (requires wkhtmltopdf)")
except ImportError:
    pass

# Required libraries
try:
    import markdown
    from bs4 import BeautifulSoup
    print("✅ Core libraries available")
except ImportError as e:
    print(f"❌ Missing required package: {e}")
    print("📦 Install required packages with:")
    print("   pip install markdown beautifulsoup4 pygments")
    print("   # Plus one of:")
    print("   pip install weasyprint  # Recommended")
    print("   pip install reportlab   # Alternative")
    sys.exit(1)

class ImprovedMarkdownToPDFConverter:
    def __init__(self):
        self.css_styles = """
        <style>
        @page {
            size: A4;
            margin: 2cm;
            @bottom-right {
                content: "Page " counter(page) " of " counter(pages);
                font-size: 9pt;
                color: #666;
            }
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            font-size: 11pt;
            margin: 0;
            padding: 0;
        }
        
        h1 {
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
            font-size: 24pt;
            margin-top: 30px;
            margin-bottom: 20px;
            page-break-after: avoid;
        }
        
        h2 {
            color: #34495e;
            border-bottom: 2px solid #ecf0f1;
            padding-bottom: 8px;
            font-size: 18pt;
            margin-top: 25px;
            margin-bottom: 15px;
            page-break-after: avoid;
        }
        
        h3 {
            color: #2c3e50;
            font-size: 14pt;
            margin-top: 20px;
            margin-bottom: 10px;
            page-break-after: avoid;
        }
        
        h4 {
            color: #34495e;
            font-size: 12pt;
            margin-top: 15px;
            margin-bottom: 8px;
            page-break-after: avoid;
        }
        
        h5, h6 {
            color: #7f8c8d;
            font-size: 11pt;
            margin-top: 10px;
            margin-bottom: 5px;
            page-break-after: avoid;
        }
        
        p {
            margin-bottom: 12px;
            text-align: justify;
            orphans: 2;
            widows: 2;
        }
        
        ul, ol {
            margin-bottom: 12px;
            padding-left: 25px;
        }
        
        li {
            margin-bottom: 5px;
        }
        
        code {
            background-color: #f8f9fa;
            padding: 2px 4px;
            border-radius: 3px;
            font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', 'Consolas', monospace;
            font-size: 9pt;
            color: #e74c3c;
            border: 1px solid #e9ecef;
        }
        
        pre {
            background-color: #f8f9fa;
            border: 1px solid #e9ecef;
            border-radius: 5px;
            padding: 15px;
            overflow-x: auto;
            margin-bottom: 15px;
            font-size: 9pt;
            line-height: 1.4;
            page-break-inside: avoid;
        }
        
        pre code {
            background-color: transparent;
            padding: 0;
            color: #333;
            font-size: 9pt;
            border: none;
        }
        
        blockquote {
            border-left: 4px solid #3498db;
            margin: 15px 0;
            padding: 10px 20px;
            background-color: #f8f9fa;
            font-style: italic;
            border-radius: 4px;
        }
        
        table {
            border-collapse: collapse;
            width: 100%;
            margin-bottom: 15px;
            font-size: 10pt;
            page-break-inside: avoid;
        }
        
        th, td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }
        
        th {
            background-color: #f2f2f2;
            font-weight: bold;
            color: #2c3e50;
        }
        
        tr:nth-child(even) {
            background-color: #f9f9f9;
        }
        
        a {
            color: #3498db;
            text-decoration: none;
        }
        
        a:hover {
            text-decoration: underline;
        }
        
        strong {
            color: #2c3e50;
            font-weight: 600;
        }
        
        em {
            color: #34495e;
            font-style: italic;
        }
        
        del {
            text-decoration: line-through;
            color: #999;
        }
        
        hr {
            border: none;
            height: 2px;
            background: linear-gradient(to right, #3498db, #ecf0f1);
            margin: 30px 0;
        }
        
        .header-info {
            text-align: center;
            margin-bottom: 40px;
            padding: 30px;
            background-color: #f8f9fa;
            border-radius: 8px;
            border: 2px solid #e9ecef;
            page-break-after: always;
        }
        
        .header-info h1 {
            margin: 0;
            border: none;
            color: #2c3e50;
            font-size: 28pt;
        }
        
        .header-info p {
            margin: 8px 0;
            color: #7f8c8d;
            font-size: 12pt;
        }
        
        .toc {
            background-color: #f8f9fa;
            border: 1px solid #e9ecef;
            border-radius: 6px;
            padding: 25px;
            margin-bottom: 40px;
            page-break-after: always;
        }
        
        .toc h2 {
            margin-top: 0;
            color: #2c3e50;
            border-bottom: 2px solid #3498db;
        }
        
        .toc ul {
            list-style-type: none;
            padding-left: 0;
        }
        
        .toc li {
            margin-bottom: 8px;
            padding-left: 20px;
        }
        
        .toc a {
            text-decoration: none;
            color: #3498db;
            font-weight: 500;
        }
        
        /* Syntax highlighting */
        .codehilite .hll { background-color: #ffffcc }
        .codehilite .c { color: #408080; font-style: italic }
        .codehilite .k { color: #008000; font-weight: bold }
        .codehilite .o { color: #666666 }
        .codehilite .cm { color: #408080; font-style: italic }
        .codehilite .cp { color: #BC7A00 }
        .codehilite .c1 { color: #408080; font-style: italic }
        .codehilite .cs { color: #408080; font-style: italic }
        .codehilite .gd { color: #A00000 }
        .codehilite .ge { font-style: italic }
        .codehilite .gr { color: #FF0000 }
        .codehilite .gh { color: #000080; font-weight: bold }
        .codehilite .gi { color: #00A000 }
        .codehilite .go { color: #888888 }
        .codehilite .gp { color: #000080; font-weight: bold }
        .codehilite .gs { font-weight: bold }
        .codehilite .gu { color: #800080; font-weight: bold }
        .codehilite .gt { color: #0044DD }
        .codehilite .kc { color: #008000; font-weight: bold }
        .codehilite .kd { color: #008000; font-weight: bold }
        .codehilite .kn { color: #008000; font-weight: bold }
        .codehilite .kp { color: #008000 }
        .codehilite .kr { color: #008000; font-weight: bold }
        .codehilite .kt { color: #B00040 }
        .codehilite .m { color: #666666 }
        .codehilite .s { color: #BA2121 }
        .codehilite .na { color: #7D9029 }
        .codehilite .nb { color: #008000 }
        .codehilite .nc { color: #0000FF; font-weight: bold }
        .codehilite .no { color: #880000 }
        .codehilite .nd { color: #AA22FF }
        .codehilite .ni { color: #999999; font-weight: bold }
        .codehilite .ne { color: #D2413A; font-weight: bold }
        .codehilite .nf { color: #0000FF }
        .codehilite .nl { color: #A0A000 }
        .codehilite .nn { color: #0000FF; font-weight: bold }
        .codehilite .nt { color: #008000; font-weight: bold }
        .codehilite .nv { color: #19177C }
        .codehilite .ow { color: #AA22FF; font-weight: bold }
        .codehilite .w { color: #bbbbbb }
        .codehilite .mb { color: #666666 }
        .codehilite .mf { color: #666666 }
        .codehilite .mh { color: #666666 }
        .codehilite .mi { color: #666666 }
        .codehilite .mo { color: #666666 }
        .codehilite .sb { color: #BA2121 }
        .codehilite .sc { color: #BA2121 }
        .codehilite .sd { color: #BA2121; font-style: italic }
        .codehilite .s2 { color: #BA2121 }
        .codehilite .se { color: #BB6622; font-weight: bold }
        .codehilite .sh { color: #BA2121 }
        .codehilite .si { color: #BB6688; font-weight: bold }
        .codehilite .sx { color: #008000 }
        .codehilite .sr { color: #BB6688 }
        .codehilite .s1 { color: #BA2121 }
        .codehilite .ss { color: #19177C }
        .codehilite .bp { color: #008000 }
        .codehilite .vc { color: #19177C }
        .codehilite .vg { color: #19177C }
        .codehilite .vi { color: #19177C }
        .codehilite .il { color: #666666 }
        </style>
        """

    def read_markdown_file(self, file_path):
        """Read markdown file content."""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except FileNotFoundError:
            print(f"❌ Error: File '{file_path}' not found.")
            return None
        except Exception as e:
            print(f"❌ Error reading file: {e}")
            return None

    def convert_markdown_to_html(self, markdown_content):
        """Convert markdown content to HTML with extensions."""
        extensions = [
            'markdown.extensions.codehilite',
            'markdown.extensions.fenced_code',
            'markdown.extensions.tables',
            'markdown.extensions.toc',
            'markdown.extensions.nl2br',
            'markdown.extensions.sane_lists'
        ]
        
        extension_configs = {
            'markdown.extensions.codehilite': {
                'css_class': 'codehilite',
                'use_pygments': True
            },
            'markdown.extensions.toc': {
                'permalink': True,
                'toc_depth': 4
            }
        }
        
        md = markdown.Markdown(
            extensions=extensions,
            extension_configs=extension_configs
        )
        
        html_content = md.convert(markdown_content)
        toc = getattr(md, 'toc', '')
        
        return html_content, toc

    def add_header_and_toc(self, html_content, toc):
        """Add professional header and table of contents to HTML."""
        current_date = datetime.now().strftime("%B %d, %Y")
        
        header_html = f"""
        <div class="header-info">
            <h1>Personal Knowledge Management System</h1>
            <p><strong>Developer Manual</strong></p>
            <p>Generated on {current_date}</p>
            <p>Comprehensive documentation for understanding, maintaining, and extending the PKM system</p>
        </div>
        """
        
        toc_html = ""
        if toc:
            toc_html = f"""
            <div class="toc">
                <h2>Table of Contents</h2>
                {toc}
            </div>
            """
        
        # Remove the first h1 tag from content
        soup = BeautifulSoup(html_content, 'html.parser')
        first_h1 = soup.find('h1')
        if first_h1:
            first_h1.extract()
        
        return header_html + toc_html + str(soup)

    def create_complete_html(self, html_content):
        """Create complete HTML document with CSS."""
        complete_html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Personal Knowledge Management System - Developer Manual</title>
            {self.css_styles}
        </head>
        <body>
            {html_content}
        </body>
        </html>
        """
        return complete_html

    def convert_with_weasyprint(self, html_content, output_path):
        """Convert HTML to PDF using WeasyPrint."""
        try:
            print("🔄 Using WeasyPrint for PDF generation...")
            weasyprint.HTML(string=html_content).write_pdf(output_path)
            return True
        except Exception as e:
            print(f"❌ WeasyPrint error: {e}")
            return False

    def convert_with_pdfkit(self, html_content, output_path):
        """Convert HTML to PDF using pdfkit (requires wkhtmltopdf)."""
        try:
            print("🔄 Using pdfkit for PDF generation...")
            options = {
                'page-size': 'A4',
                'margin-top': '0.75in',
                'margin-right': '0.75in',
                'margin-bottom': '0.75in',
                'margin-left': '0.75in',
                'encoding': "UTF-8",
                'no-outline': None,
                'enable-local-file-access': None,
                'print-media-type': None,
                'disable-smart-shrinking': None,
                'footer-right': '[page] of [topage]',
                'footer-font-size': '9',
                'footer-spacing': '5',
                'header-spacing': '5'
            }
            pdfkit.from_string(html_content, output_path, options=options)
            return True
        except Exception as e:
            print(f"❌ pdfkit error: {e}")
            return False

    def save_html_fallback(self, html_content, output_path):
        """Save HTML file as fallback when PDF generation fails."""
        html_path = output_path.replace('.pdf', '.html')
        try:
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            print(f"💾 HTML saved as fallback: {html_path}")
            print("📄 Open in browser and use 'Print to PDF' to create PDF")
            
            # Try to open in browser
            try:
                webbrowser.open(f'file://{os.path.abspath(html_path)}')
                print("🌐 Opened in browser")
            except:
                print(f"📂 Manually open: {os.path.abspath(html_path)}")
            
            return True
        except Exception as e:
            print(f"❌ Error saving HTML: {e}")
            return False

    def convert_html_to_pdf(self, html_content, output_path):
        """Convert HTML to PDF using available libraries."""
        # Try WeasyPrint first (best option)
        if PDF_LIBRARIES['weasyprint']:
            if self.convert_with_weasyprint(html_content, output_path):
                return True
        
        # Try pdfkit if available (requires wkhtmltopdf)
        if PDF_LIBRARIES['pdfkit']:
            if self.convert_with_pdfkit(html_content, output_path):
                return True
        
        # Fallback to HTML output
        print("⚠️  No PDF libraries available, saving as HTML...")
        return self.save_html_fallback(html_content, output_path)

    def convert(self, input_file, output_file=None):
        """Main conversion method."""
        print("🚀 Improved Markdown to PDF Converter")
        print("=" * 50)
        
        # Show available PDF libraries
        available_libs = [lib for lib, available in PDF_LIBRARIES.items() if available]
        if available_libs:
            print(f"📚 Available PDF libraries: {', '.join(available_libs)}")
        else:
            print("⚠️  No PDF libraries available - will output HTML for browser conversion")
        
        # Read markdown file
        print(f"📖 Reading markdown file: {input_file}")
        markdown_content = self.read_markdown_file(input_file)
        if not markdown_content:
            return False

        # Convert to HTML
        print("🔄 Converting markdown to HTML...")
        html_content, toc = self.convert_markdown_to_html(markdown_content)
        
        # Add header and TOC
        print("✨ Adding professional formatting...")
        html_content = self.add_header_and_toc(html_content, toc)
        
        # Create complete HTML document
        complete_html = self.create_complete_html(html_content)
        
        # Generate output filename if not provided
        if not output_file:
            input_path = Path(input_file)
            output_file = input_path.parent / f"{input_path.stem}.pdf"
        
        # Convert to PDF
        print(f"📄 Converting to PDF: {output_file}")
        success = self.convert_html_to_pdf(complete_html, str(output_file))
        
        if success:
            if os.path.exists(str(output_file)):
                file_size = os.path.getsize(str(output_file))
                file_size_mb = file_size / (1024 * 1024)
                print(f"✅ PDF created successfully!")
                print(f"📊 File size: {file_size_mb:.2f} MB")
                print(f"📁 Location: {output_file}")
            else:
                print(f"✅ HTML created successfully!")
                print(f"📁 Location: {str(output_file).replace('.pdf', '.html')}")
            return True
        else:
            return False

def main():
    parser = argparse.ArgumentParser(
        description="Convert README.md to professional PDF format (improved version)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 markdown_to_pdf_improved.py                    # Convert README.md to README.pdf
  python3 markdown_to_pdf_improved.py -i README.md       # Same as above
  python3 markdown_to_pdf_improved.py -i README.md -o manual.pdf  # Custom output name
  
Requirements (choose one):
  Option 1 (Recommended): pip install markdown weasyprint beautifulsoup4 pygments
  Option 2: pip install markdown reportlab beautifulsoup4 pygments  
  Option 3 (Fallback): pip install markdown beautifulsoup4 pygments
  
No external system dependencies required!
        """
    )
    
    parser.add_argument(
        '-i', '--input',
        default='README.md',
        help='Input markdown file (default: README.md)'
    )
    
    parser.add_argument(
        '-o', '--output',
        help='Output PDF file (default: same name as input with .pdf extension)'
    )
    
    args = parser.parse_args()
    
    # Check if input file exists
    if not os.path.exists(args.input):
        print(f"❌ Error: Input file '{args.input}' not found.")
        print(f"📁 Current directory: {os.getcwd()}")
        print(f"📋 Available files: {', '.join([f for f in os.listdir('.') if f.endswith('.md')])}")
        sys.exit(1)
    
    # Show installation suggestions if no PDF libraries available
    if not any(PDF_LIBRARIES.values()):
        print("\n💡 To enable direct PDF generation, install one of:")
        print("   pip install weasyprint      # Recommended - no system dependencies")
        print("   pip install reportlab       # Alternative PDF library")
        print("   pip install pdfkit          # Requires wkhtmltopdf system package")
        print("\n🔄 Proceeding with HTML output (use browser to convert to PDF)...")
    
    # Create converter and run conversion
    converter = ImprovedMarkdownToPDFConverter()
    success = converter.convert(args.input, args.output)
    
    if success:
        print("\n🎉 Conversion completed successfully!")
        if not any(PDF_LIBRARIES.values()):
            print("📄 Open the HTML file in your browser and use 'Print to PDF'")
        sys.exit(0)
    else:
        print("\n❌ Conversion failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
