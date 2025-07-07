#!/usr/bin/env python3
import re
import sys

def final_check_untranslated(filename):
    """
    Final comprehensive check for untranslated entries
    """
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split into entries based on #: comments
    entries = re.split(r'\n(?=#:)', content)
    
    untranslated_entries = []
    
    for entry in entries:
        if not entry.strip() or '#: ../../library/typing.rst:' not in entry:
            continue
        
        # Look for patterns: msgid ... msgstr ""
        # where msgstr is truly empty (no following quoted content)
        if 'msgid' in entry and 'msgstr' in entry:
            # Find the msgstr line and check if it's followed by actual translation
            lines = entry.split('\n')
            msgstr_found = False
            is_empty = True
            msgid_content = ""
            
            for i, line in enumerate(lines):
                if line.startswith('msgid'):
                    # Collect msgid content
                    msgid_content = line
                    j = i + 1
                    while j < len(lines) and (lines[j].startswith('"') or lines[j].strip() == ''):
                        if lines[j].startswith('"'):
                            msgid_content += " " + lines[j]
                        j += 1
                
                if line.startswith('msgstr'):
                    msgstr_found = True
                    # Check if this msgstr line is just msgstr ""
                    if line.strip() == 'msgstr ""':
                        # Check if the next lines contain translation
                        j = i + 1
                        has_translation = False
                        while j < len(lines) and not lines[j].startswith('#'):
                            if lines[j].startswith('"') and lines[j].strip() != '""':
                                has_translation = True
                                break
                            elif lines[j].startswith('msgid'):
                                break
                            j += 1
                        
                        if not has_translation:
                            # This is truly untranslated
                            # But skip if it's clearly code
                            msgid_clean = re.sub(r'"', '', msgid_content)
                            if not any(x in msgid_clean for x in [
                                'def ', 'class ', '>>>', 'import ', 'return ', 'print(',
                                'assert ', 'raise ', 'try:', 'except:', 'if __name__'
                            ]) and msgid_clean.strip():
                                untranslated_entries.append({
                                    'msgid': msgid_clean[:100] + '...' if len(msgid_clean) > 100 else msgid_clean,
                                    'location': re.search(r'#: (.*)', entry).group(1) if re.search(r'#: (.*)', entry) else 'unknown'
                                })
                    break
    
    print(f'🔍 最終確認 - 未翻訳エントリ: {filename}')
    print(f'=' * 80)
    print(f'見つかった未翻訳エントリ: {len(untranslated_entries)}')
    
    if untranslated_entries:
        print('\n未翻訳エントリ:')
        for i, entry in enumerate(untranslated_entries, 1):
            print(f'{i:3d}: {entry["location"]}')
            print(f'     {entry["msgid"]}')
            print()
    else:
        print('✅ 未翻訳エントリは見つかりませんでした！')
    
    print(f'=' * 80)

if __name__ == "__main__":
    filename = sys.argv[1] if len(sys.argv) > 1 else 'library/typing.po'
    final_check_untranslated(filename)