#!/usr/bin/env python3
import re
import sys

def find_empty_msgstr(filename):
    """Find entries with truly empty msgstr"""
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern to match complete po entries
    pattern = r'(#:.*?\nmsgid.*?\nmsgstr[^\n]*(?:\n"[^"]*")*)'
    entries = re.findall(pattern, content, re.DOTALL)
    
    empty_entries = []
    
    for entry in entries:
        # Check if msgstr is truly empty (just msgstr "" with no following quoted strings)
        if re.search(r'msgstr ""\s*\n(?![\s]*")', entry):
            # Extract msgid content
            msgid_match = re.search(r'msgid\s+"([^"]*)"(?:\s*\n\s*"([^"]*)")*', entry)
            if msgid_match:
                msgid_content = msgid_match.group(1)
                if msgid_match.group(2):
                    msgid_content += msgid_match.group(2)
                
                # Skip obvious code examples
                if not any(x in msgid_content for x in ['def ', 'class ', '>>>', 'import ', 'return ']):
                    if msgid_content.strip():  # Non-empty msgid
                        empty_entries.append({
                            'msgid': msgid_content,
                            'entry': entry[:200] + '...' if len(entry) > 200 else entry
                        })
    
    print(f"Found {len(empty_entries)} truly empty msgstr entries:")
    for i, entry in enumerate(empty_entries[:10], 1):
        print(f"{i}: {entry['msgid']}")
        print(f"   Entry: {entry['entry']}")
        print()

if __name__ == "__main__":
    filename = sys.argv[1] if len(sys.argv) > 1 else 'library/typing.po'
    find_empty_msgstr(filename)