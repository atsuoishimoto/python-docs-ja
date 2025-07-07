#!/usr/bin/env python3
import re
import sys

def check_untranslated(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f'❌ ファイル {filename} が見つかりません')
        return

    # POエントリを正確に分割
    entries = re.findall(r'#:.*?\nmsgid.*?\nmsgstr.*?(?=\n#:|$)', content, re.DOTALL)
    
    untranslated_count = 0
    code_samples = 0
    translatable_untranslated = []

    for i, entry in enumerate(entries):
        # msgidとmsgstrを抽出
        msgid_match = re.search(r'msgid\s+"(.*?)"', entry, re.DOTALL)
        msgstr_match = re.search(r'msgstr\s+"(.*?)"', entry, re.DOTALL)
        
        if not msgid_match or not msgstr_match:
            continue
            
        msgid_content = msgid_match.group(1)
        msgstr_content = msgstr_match.group(1)
        
        # 空のmsgstrかチェック
        if msgstr_content.strip() == "":
            untranslated_count += 1
            
            # コードサンプルまたは翻訳不要な内容かチェック
            is_code_or_no_translate = (
                # 空のmsgid
                msgid_content.strip() == "" or
                # プログラムコード
                'def ' in msgid_content or
                'class ' in msgid_content or
                'assert ' in msgid_content or
                'print(' in msgid_content or
                'return ' in msgid_content or
                'import ' in msgid_content or
                '>>>' in msgid_content or
                'raise ' in msgid_content or
                'if __name__' in msgid_content or
                'try:' in msgid_content or
                'except:' in msgid_content or
                # パス、URL、コマンド例
                ('.py' in msgid_content and '/' in msgid_content) or
                ('.txt' in msgid_content and '/' in msgid_content) or
                'http://' in msgid_content or
                'https://' in msgid_content or
                # バージョン番号のみ
                re.match(r'^\d+\.\d+$', msgid_content.strip()) or
                # PEPやissue番号のみ
                re.match(r'^:pep:`\d+`$', msgid_content.strip()) or
                re.match(r'^:gh:`\d+`$', msgid_content.strip()) or
                # 単一の技術用語（既に翻訳されているもの）
                msgid_content.strip() in ['Parameters', 'Examples:', 'Constant'] or
                # 改行のみの内容
                msgid_content.strip() == "\\n" or
                # 空白のみの内容
                re.match(r'^\\s*$', msgid_content)
            )
            
            if is_code_or_no_translate:
                code_samples += 1
            else:
                # 翻訳可能だが未翻訳のエントリ
                translatable_untranslated.append({
                    'entry_num': i + 1,
                    'msgid': msgid_content[:100] + '...' if len(msgid_content) > 100 else msgid_content
                })

    print(f'📊 翻訳状況レポート: {filename}')
    print(f'=' * 80)
    print(f'総未翻訳エントリ数: {untranslated_count}')
    print(f'  - コードサンプル/翻訳不要: {code_samples}')
    print(f'  - 翻訳が必要: {len(translatable_untranslated)}')
    
    total_entries = len(entries)
    translated_entries = total_entries - untranslated_count
    translation_rate = (translated_entries / total_entries * 100) if total_entries > 0 else 0
    
    print(f'翻訳完了率: {translation_rate:.1f}% ({translated_entries}/{total_entries})')
    
    if len(translatable_untranslated) == 0:
        print('✅ すべての翻訳対象エントリが翻訳済みです！')
    else:
        print(f'⚠️  {len(translatable_untranslated)}個の翻訳対象エントリが未翻訳です')
        print()
        print('未翻訳エントリ一覧（最初の20個）:')
        print('-' * 80)
        for entry in translatable_untranslated[:20]:
            print(f'{entry["entry_num"]:4d}: {entry["msgid"]}')
        
        if len(translatable_untranslated) > 20:
            print(f'... 他 {len(translatable_untranslated) - 20}個')

    print(f'=' * 80)

if __name__ == "__main__":
    filename = sys.argv[1] if len(sys.argv) > 1 else 'library/typing.po'
    check_untranslated(filename)