#!/usr/bin/env python3
"""
Simple HTML Converter for README.md
Converts markdown to HTML without external dependencies.
Use browser's "Print to PDF" function to create PDF.

No external dependencies required - uses only Python standard library.
"""

import os
import sys
import re
import webbrowser
from datetime import datetime
from pathlib import Path

class SimpleMarkdownToHTMLConverter:
    def __init__(self):
        self.css_styles = """
        <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 1200px;
            margin: 0 auto;
            padding: 40px 20px;
            font-size: 14px;
        }
        
        h1 {
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
            font-size: 2.5em;
            margin-top: 40px;
            margin-bottom: 20px;
        }
        
        h2 {
            color: #34495e;
            border-bottom: 2px solid #ecf0f1;
            padding-bottom: 8px;
            font-size: 2em;
            margin-top: 35px;
            margin-bottom: 15px;
        }
        
        h3 {
            color: #2c3e50;
            font-size: 1.5em;
            margin-top: 25px;
            margin-bottom: 10px;
        }
        
        h4 {
            color: #34495e;
            font-size: 1.25em;
            margin-top: 20px;
            margin-bottom: 8px;
        }
        
        h5, h6 {
            color: #7f8c8d;
            font-size: 1.1em;
            margin-top: 15px;
            margin-bottom: 5px;
        }
        
        p {
            margin-bottom: 16px;
            text-align: justify;
        }
        
        ul, ol {
            margin-bottom: 16px;
            padding-left: 30px;
        }
        
        li {
            margin-bottom: 8px;
        }
        
        code {
            background-color: #f8f9fa;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', 'Consolas', monospace;
            font-size: 0.9em;
            color: #e74c3c;
            border: 1px solid #e9ecef;
        }
        
        pre {
            background-color: #f8f9fa;
            border: 1px solid #e9ecef;
            border-radius: 6px;
            padding: 20px;
            overflow-x: auto;
            margin-bottom: 20px;
            font-size: 0.9em;
            line-height: 1.4;
        }
        
        pre code {
            background-color: transparent;
            padding: 0;
            color: #333;
            font-size: inherit;
            border: none;
        }
        
        blockquote {
            border-left: 4px solid #3498db;
            margin: 20px 0;
            padding: 15px 25px;
            background-color: #f8f9fa;
            font-style: italic;
            border-radius: 4px;
        }
        
        blockquote p {
            margin-bottom: 0;
        }
        
        table {
            border-collapse: collapse;
            width: 100%;
            margin-bottom: 20px;
            font-size: 0.9em;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }
        
        th, td {
            border: 1px solid #ddd;
            padding: 12px;
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
            margin-bottom: 50px;
            padding: 30px;
            background-color: #f8f9fa;
            border-radius: 8px;
            border: 2px solid #e9ecef;
        }
        
        .header-info h1 {
            margin: 0;
            border: none;
            color: #2c3e50;
            font-size: 2.5em;
        }
        
        .header-info p {
            margin: 8px 0;
            color: #7f8c8d;
            font-size: 1.1em;
        }
        
        .toc {
            background-color: #f8f9fa;
            border: 1px solid #e9ecef;
            border-radius: 6px;
            padding: 25px;
            margin-bottom: 40px;
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
        
        .toc a:hover {
            text-decoration: underline;
        }
        
        .print-instructions {
            background-color: #e8f5e8;
            border: 2px solid #4caf50;
            border-radius: 6px;
            padding: 20px;
            margin-bottom: 30px;
            text-align: center;
        }
        
        .print-instructions h3 {
            color: #2e7d32;
            margin-top: 0;
        }
        
        .print-instructions p {
            margin-bottom: 10px;
            text-align: center;
        }
        
        kbd {
            background-color: #f8f9fa;
            border: 1px solid #ccc;
            border-radius: 3px;
            padding: 2px 6px;
            font-family: monospace;
            font-size: 0.9em;
            box-shadow: 0 1px 1px rgba(0,0,0,0.1);
        }
        
        @media print {
            body { 
                font-size: 12px; 
                padding: 20px;
            }
            h1 { font-size: 20px; }
            h2 { font-size: 18px; }
            h3 { font-size: 16px; }
            h4 { font-size: 14px; }
            pre, code { font-size: 10px; }
            table { font-size: 11px; }
            .print-instructions { display: none; }
            .header-info { 
                page-break-after: always; 
                margin-bottom: 0;
            }
            h1, h2, h3 { page-break-after: avoid; }
            pre, table { page-break-inside: avoid; }
        }
        </style>
        """

    def read_file(self, file_path):
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

    def convert_headers(self, text):
        """Convert markdown headers to HTML."""
        # H1-H6 headers
        text = re.sub(r'^#{6}\s+(.+)$', r'<h6>\1</h6>', text, flags=re.MULTILINE)
        text = re.sub(r'^#{5}\s+(.+)$', r'<h5>\1</h5>', text, flags=re.MULTILINE)
        text = re.sub(r'^#{4}\s+(.+)$', r'<h4>\1</h4>', text, flags=re.MULTILINE)
        text = re.sub(r'^#{3}\s+(.+)$', r'<h3>\1</h3>', text, flags=re.MULTILINE)
        text = re.sub(r'^#{2}\s+(.+)$', r'<h2>\1</h2>', text, flags=re.MULTILINE)
        text = re.sub(r'^#{1}\s+(.+)$', r'<h1>\1</h1>', text, flags=re.MULTILINE)
        return text

    def convert_code_blocks(self, text):
        """Convert code blocks to HTML with proper escaping."""
        # Fenced code blocks with language
        def replace_code_block(match):
            language = match.group(1) or ''
            code_content = match.group(2)
            # Escape HTML entities in code
            code_content = code_content.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            lang_class = f' class="language-{language}"' if language else ''
            return f'<pre{lang_class}><code{lang_class}>{code_content}</code></pre>'
        
        text = re.sub(r'```(\w+)?\n(.*?)\n```', replace_code_block, text, flags=re.DOTALL)
        
        # Inline code
        def replace_inline_code(match):
            code_content = match.group(1)
            # Escape HTML entities in inline code
            code_content = code_content.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            return f'<code>{code_content}</code>'
        
        text = re.sub(r'`([^`]+)`', replace_inline_code, text)
        return text

    def convert_lists(self, text):
        """Convert markdown lists to HTML with proper nesting support."""
        lines = text.split('\n')
        result = []
        list_stack = []  # Stack to track nested lists
        
        for line in lines:
            # Unordered list
            ul_match = re.match(r'^(\s*)[-*+]\s+(.+)', line)
            if ul_match:
                item_indent = len(ul_match.group(1))
                item_content = ul_match.group(2)
                
                # Close deeper lists
                while list_stack and list_stack[-1][1] > item_indent:
                    list_type, _ = list_stack.pop()
                    result.append(f'</{list_type}>')
                
                # Start new list or continue existing
                if not list_stack or list_stack[-1][0] != 'ul' or list_stack[-1][1] != item_indent:
                    result.append('<ul>')
                    list_stack.append(('ul', item_indent))
                
                result.append(f'<li>{item_content}</li>')
                continue
            
            # Ordered list
            ol_match = re.match(r'^(\s*)\d+\.\s+(.+)', line)
            if ol_match:
                item_indent = len(ol_match.group(1))
                item_content = ol_match.group(2)
                
                # Close deeper lists
                while list_stack and list_stack[-1][1] > item_indent:
                    list_type, _ = list_stack.pop()
                    result.append(f'</{list_type}>')
                
                # Start new list or continue existing
                if not list_stack or list_stack[-1][0] != 'ol' or list_stack[-1][1] != item_indent:
                    result.append('<ol>')
                    list_stack.append(('ol', item_indent))
                
                result.append(f'<li>{item_content}</li>')
                continue
            
            # Not a list item - close all lists
            while list_stack:
                list_type, _ = list_stack.pop()
                result.append(f'</{list_type}>')
            
            result.append(line)
        
        # Close any remaining lists
        while list_stack:
            list_type, _ = list_stack.pop()
            result.append(f'</{list_type}>')
            
        return '\n'.join(result)

    def convert_formatting(self, text):
        """Convert basic markdown formatting to HTML."""
        # Bold + Italic combinations (must come first)
        text = re.sub(r'\*\*\*([^*]+)\*\*\*', r'<strong><em>\1</em></strong>', text)
        text = re.sub(r'___([^_]+)___', r'<strong><em>\1</em></strong>', text)
        
        # Bold
        text = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', text)
        text = re.sub(r'__([^_]+)__', r'<strong>\1</strong>', text)
        
        # Italic (after bold to avoid conflicts)
        text = re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)', r'<em>\1</em>', text)
        text = re.sub(r'(?<!_)_([^_]+)_(?!_)', r'<em>\1</em>', text)
        
        # Strikethrough
        text = re.sub(r'~~([^~]+)~~', r'<del>\1</del>', text)
        
        # Links
        text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2" target="_blank">\1</a>', text)
        
        # Horizontal rules
        text = re.sub(r'^---+$', r'<hr>', text, flags=re.MULTILINE)
        text = re.sub(r'^\*\*\*+$', r'<hr>', text, flags=re.MULTILINE)
        
        return text

    def convert_tables(self, text):
        """Convert markdown tables to HTML."""
        lines = text.split('\n')
        result = []
        in_table = False
        
        for i, line in enumerate(lines):
            if '|' in line and line.strip():
                if not in_table:
                    result.append('<table>')
                    in_table = True
                
                # Check if this is a header separator line
                if re.match(r'^\s*\|[\s\-\|:]+\|\s*$', line):
                    continue
                
                # Process table row
                cells = [cell.strip() for cell in line.split('|')[1:-1]]
                
                # Check if this is the first row (header)
                is_header = (i + 1 < len(lines) and 
                           re.match(r'^\s*\|[\s\-\|:]+\|\s*$', lines[i + 1]))
                
                if is_header:
                    row = '<tr>' + ''.join(f'<th>{cell}</th>' for cell in cells) + '</tr>'
                else:
                    row = '<tr>' + ''.join(f'<td>{cell}</td>' for cell in cells) + '</tr>'
                
                result.append(row)
            else:
                if in_table:
                    result.append('</table>')
                    in_table = False
                result.append(line)
        
        if in_table:
            result.append('</table>')
            
        return '\n'.join(result)

    def convert_blockquotes(self, text):
        """Convert blockquotes to HTML."""
        lines = text.split('\n')
        result = []
        in_blockquote = False
        blockquote_content = []
        
        for line in lines:
            if line.startswith('> '):
                if not in_blockquote:
                    in_blockquote = True
                    blockquote_content = []
                blockquote_content.append(line[2:])  # Remove '> '
            else:
                if in_blockquote:
                    # Process the blockquote content
                    quote_text = '\n'.join(blockquote_content)
                    result.append(f'<blockquote><p>{quote_text}</p></blockquote>')
                    in_blockquote = False
                    blockquote_content = []
                result.append(line)
        
        # Handle blockquote at end of file
        if in_blockquote:
            quote_text = '\n'.join(blockquote_content)
            result.append(f'<blockquote><p>{quote_text}</p></blockquote>')
            
        return '\n'.join(result)

    def convert_paragraphs(self, text):
        """Convert text to paragraphs with better handling."""
        # Split by double newlines to identify paragraphs
        paragraphs = text.split('\n\n')
        result = []
        
        for para in paragraphs:
            para = para.strip()
            if para:
                # Skip if it's already HTML block elements
                if re.match(r'^<(?:h[1-6]|ul|ol|table|pre|blockquote|div|hr)', para):
                    result.append(para)
                # Skip if it contains only HTML tags
                elif re.match(r'^</(?:ul|ol|table|blockquote|div)>$', para):
                    result.append(para)
                # Skip if it's a list item or table row
                elif re.match(r'^<(?:li|tr|th|td)', para):
                    result.append(para)
                # Convert to paragraph if it's plain text or inline HTML
                else:
                    # Handle line breaks within paragraphs
                    para = para.replace('\n', '<br>\n')
                    result.append(f'<p>{para}</p>')
        
        return '\n\n'.join(result)

    def generate_toc(self, text):
        """Generate table of contents from headers."""
        headers = re.findall(r'<h([1-6])>([^<]+)</h[1-6]>', text)
        if not headers:
            return "", text
        
        toc_html = '<div class="toc">\n<h2>Table of Contents</h2>\n<ul>\n'
        
        for level, title in headers:
            # Create anchor from title
            anchor = re.sub(r'[^\w\s-]', '', title).strip()
            anchor = re.sub(r'[-\s]+', '-', anchor).lower()
            
            # Add anchor to original header
            text = text.replace(f'<h{level}>{title}</h{level}>', 
                              f'<h{level} id="{anchor}">{title}</h{level}>')
            
            # Add to TOC
            indent = '  ' * (int(level) - 1)
            toc_html += f'{indent}<li><a href="#{anchor}">{title}</a></li>\n'
        
        toc_html += '</ul>\n</div>\n\n'
        return toc_html, text

    def convert_markdown_to_html(self, markdown_content):
        """Convert markdown content to HTML."""
        # Remove the first h1 (will be replaced by header)
        markdown_content = re.sub(r'^#\s+.*\n', '', markdown_content, count=1)
        
        # Convert markdown elements in proper order
        html = markdown_content
        html = self.convert_code_blocks(html)
        html = self.convert_headers(html)
        html = self.convert_tables(html)
        html = self.convert_lists(html)
        html = self.convert_blockquotes(html)
        html = self.convert_formatting(html)
        html = self.convert_paragraphs(html)
        
        # Generate TOC
        toc_html, html = self.generate_toc(html)
        
        return toc_html + html

    def create_header(self):
        """Create professional header."""
        current_date = datetime.now().strftime("%B %d, %Y")
        return f"""
        <div class="header-info">
            <h1>Personal Knowledge Management System</h1>
            <p><strong>Developer Manual</strong></p>
            <p>Generated on {current_date}</p>
            <p>Comprehensive documentation for understanding, maintaining, and extending the PKM system</p>
        </div>
        """

    def create_print_instructions(self):
        """Create print instructions."""
        return """
        <div class="print-instructions">
            <h3>📄 Convert to PDF Instructions</h3>
            <p><strong>1.</strong> Press <kbd>Ctrl+P</kbd> (or <kbd>Cmd+P</kbd> on Mac) to open print dialog</p>
            <p><strong>2.</strong> Select "Save as PDF" or "Microsoft Print to PDF" as destination</p>
            <p><strong>3.</strong> Choose "More settings" and set margins to "Minimum"</p>
            <p><strong>4.</strong> Enable "Background graphics" for better styling</p>
            <p><strong>5.</strong> Click "Save" to generate your PDF</p>
        </div>
        """

    def create_complete_html(self, content_html):
        """Create complete HTML document."""
        header_html = self.create_header()
        instructions_html = self.create_print_instructions()
        
        return f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Personal Knowledge Management System - Developer Manual</title>
            {self.css_styles}
        </head>
        <body>
            {header_html}
            {instructions_html}
            {content_html}
        </body>
        </html>
        """

    def convert(self, input_file, output_file=None, open_browser=True):
        """Main conversion method."""
        print("🚀 Simple HTML Converter")
        print("=" * 50)
        
        # Read markdown file
        print(f"📖 Reading markdown file: {input_file}")
        markdown_content = self.read_file(input_file)
        if not markdown_content:
            return False

        # Convert to HTML
        print("🔄 Converting markdown to HTML...")
        content_html = self.convert_markdown_to_html(markdown_content)
        
        # Create complete HTML document
        print("✨ Adding professional formatting...")
        complete_html = self.create_complete_html(content_html)
        
        # Generate output filename if not provided
        if not output_file:
            input_path = Path(input_file)
            output_file = input_path.parent / f"{input_path.stem}.html"
        
        # Save HTML file
        print(f"💾 Saving HTML file: {output_file}")
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(complete_html)
        except Exception as e:
            print(f"❌ Error saving HTML file: {e}")
            return False
        
        file_size = os.path.getsize(output_file)
        file_size_kb = file_size / 1024
        print(f"✅ HTML created successfully!")
        print(f"📊 File size: {file_size_kb:.1f} KB")
        print(f"📁 Location: {output_file}")
        
        # Open in browser
        if open_browser:
            print("🌐 Opening in browser...")
            try:
                webbrowser.open(f'file://{os.path.abspath(output_file)}')
                print("📄 Use Ctrl+P (Cmd+P on Mac) and 'Save as PDF' to create PDF")
            except Exception as e:
                print(f"⚠️  Could not open browser automatically: {e}")
                print(f"📂 Manually open: {os.path.abspath(output_file)}")
        
        return True

def main():
    input_file = "README.md"
    
    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"❌ Error: Input file '{input_file}' not found.")
        print(f"📁 Current directory: {os.getcwd()}")
        print(f"📋 Available files: {', '.join([f for f in os.listdir('.') if f.endswith('.md')])}")
        sys.exit(1)
    
    # Create converter and run conversion
    converter = SimpleMarkdownToHTMLConverter()
    success = converter.convert(input_file)
    
    if success:
        print("\n🎉 Conversion completed successfully!")
        print("📄 Use your browser's print function to save as PDF")
        sys.exit(0)
    else:
        print("\n❌ Conversion failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
