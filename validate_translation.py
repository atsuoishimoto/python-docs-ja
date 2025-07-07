#!/usr/bin/env python3
import re
import sys

def validate_po_file(filename):
    """
    Validate .po file for untranslated entries without syntax errors
    """
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f'❌ ファイル {filename} が見つかりません')
        return False
    
    # Simple regex pattern to find untranslated entries
    # Look for msgstr "" with no content between quotes
    pattern = r'msgstr\s*""\s*\n'
    untranslated_simple = re.findall(pattern, content)
    
    # More comprehensive check for truly empty msgstr
    entries = content.split('\n\n')
    empty_msgstr_count = 0
    translatable_empty = 0
    
    for entry in entries:
        if 'msgid' in entry and 'msgstr' in entry:
            # Check if msgstr is empty
            msgstr_match = re.search(r'msgstr\s*"([^"]*)"', entry)
            if msgstr_match and msgstr_match.group(1).strip() == '':
                empty_msgstr_count += 1
                
                # Check if it's translatable content
                msgid_match = re.search(r'msgid\s*"([^"]*)"', entry)
                if msgid_match:
                    msgid_content = msgid_match.group(1)
                    # Simple heuristic: if it contains common code patterns, skip
                    if not any(pattern in msgid_content for pattern in [
                        'def ', 'class ', 'import ', '>>>', 'print(', 'assert ',
                        'return ', 'if __name__', 'try:', 'except:', '.py',
                        'http://', 'https://'
                    ]):
                        # This might be translatable
                        if len(msgid_content.strip()) > 0:
                            translatable_empty += 1
    
    print(f'📊 翻訳検証結果: {filename}')
    print(f'=' * 60)
    print(f'空のmsgstr総数: {empty_msgstr_count}')
    print(f'翻訳が必要と思われる空のmsgstr: {translatable_empty}')
    
    if translatable_empty == 0:
        print('✅ 翻訳対象エントリはすべて翻訳済みと思われます')
        return True
    else:
        print(f'⚠️  {translatable_empty}個のエントリが未翻訳の可能性があります')
        return False

if __name__ == "__main__":
    filename = sys.argv[1] if len(sys.argv) > 1 else 'library/typing.po'
    validate_po_file(filename)