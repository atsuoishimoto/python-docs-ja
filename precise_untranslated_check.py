#!/usr/bin/env python3
import re
import sys

def parse_po_file(filename):
    """
    More accurate .po file parser that handles multi-line entries correctly
    """
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f'❌ ファイル {filename} が見つかりません')
        return
    
    # Split content into blocks, each starting with #:
    blocks = re.split(r'\n(?=#:)', content)
    
    untranslated_entries = []
    total_entries = 0
    
    for block in blocks:
        if not block.strip():
            continue
            
        # Skip header block
        if 'msgid ""' in block and 'Project-Id-Version' in block:
            continue
            
        # Check if this block has msgid and msgstr
        if 'msgid' in block and 'msgstr' in block:
            total_entries += 1
            
            # Extract msgid content (handle multi-line)
            msgid_match = re.search(r'msgid\s+(.*?)(?=\nmsgstr|\nmsgid|\n#|\nZ)', block, re.DOTALL)
            msgstr_match = re.search(r'msgstr\s+(.*?)(?=\n#|\nmsgid|\nZ)', block, re.DOTALL)
            
            if msgid_match and msgstr_match:
                msgid_content = msgid_match.group(1).strip()
                msgstr_content = msgstr_match.group(1).strip()
                
                # Clean up quotes and whitespace
                msgid_clean = re.sub(r'^""|""$', '', msgid_content.replace('\n', ' ').replace('"', ''))
                msgstr_clean = re.sub(r'^""|""$', '', msgstr_content.replace('\n', ' ').replace('"', ''))
                
                # Check if msgstr is truly empty
                if not msgstr_clean.strip():
                    # Determine if this should be translated
                    should_translate = not any([
                        # Code examples
                        'def ' in msgid_clean,
                        'class ' in msgid_clean,
                        'import ' in msgid_clean,
                        '>>>' in msgid_clean,
                        'print(' in msgid_clean,
                        'return ' in msgid_clean,
                        'assert ' in msgid_clean,
                        'raise ' in msgid_clean,
                        'try:' in msgid_clean,
                        'except:' in msgid_clean,
                        'if __name__' in msgid_clean,
                        # File paths
                        '.py' in msgid_clean and '/' in msgid_clean,
                        '.txt' in msgid_clean and '/' in msgid_clean,
                        # URLs
                        'http://' in msgid_clean,
                        'https://' in msgid_clean,
                        # Version numbers only
                        re.match(r'^\d+\.\d+$', msgid_clean.strip()),
                        # Empty content
                        not msgid_clean.strip(),
                        # Just newlines
                        msgid_clean.strip() == '\\n'
                    ])
                    
                    if should_translate and len(msgid_clean.strip()) > 0:
                        untranslated_entries.append({
                            'content': msgid_clean[:100] + '...' if len(msgid_clean) > 100 else msgid_clean,
                            'full_block': block[:300] + '...' if len(block) > 300 else block
                        })
    
    print(f'📊 精密な翻訳状況レポート: {filename}')
    print(f'=' * 80)
    print(f'総エントリ数: {total_entries}')
    print(f'未翻訳で翻訳が必要: {len(untranslated_entries)}')
    
    if len(untranslated_entries) > 0:
        print(f'\n⚠️  {len(untranslated_entries)}個の翻訳対象エントリが未翻訳です')
        print('\n未翻訳エントリ（最初の10個）:')
        print('-' * 80)
        for i, entry in enumerate(untranslated_entries[:10], 1):
            print(f'{i:3d}: {entry["content"]}')
        
        if len(untranslated_entries) > 10:
            print(f'... 他 {len(untranslated_entries) - 10}個')
    else:
        print('✅ すべての翻訳対象エントリが翻訳済みです！')
    
    print(f'=' * 80)

if __name__ == "__main__":
    filename = sys.argv[1] if len(sys.argv) > 1 else 'library/typing.po'
    parse_po_file(filename)