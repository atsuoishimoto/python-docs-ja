#!/usr/bin/env python3
"""
改良版未翻訳エントリ検出スクリプト
これまでの翻訳作業で判明した課題を解決する改善版
"""
import re
import sys
from typing import List, Dict, Tuple

def parse_po_entries(content: str) -> List[Dict[str, str]]:
    """
    .poファイルのエントリをより正確に解析
    マルチライン対応、コメント処理、空行処理を改善
    """
    # エントリを #: で分割（ただし先頭の場合は除く）
    entries = re.split(r'\n(?=#:)', content)
    parsed_entries = []
    
    for i, entry in enumerate(entries):
        if not entry.strip():
            continue
            
        # ヘッダーエントリをスキップ
        if 'Project-Id-Version' in entry:
            continue
            
        # msgidとmsgstrを抽出
        msgid_match = re.search(r'msgid\s+((?:"[^"]*"\s*)+)', entry, re.MULTILINE | re.DOTALL)
        msgstr_match = re.search(r'msgstr\s+((?:"[^"]*"\s*)*)', entry, re.MULTILINE | re.DOTALL)
        
        if msgid_match and msgstr_match:
            # 引用符を結合してクリーンアップ
            msgid_raw = msgid_match.group(1)
            msgstr_raw = msgstr_match.group(1)
            
            # 複数行の文字列を結合
            msgid_clean = re.sub(r'"\s*\n\s*"', '', msgid_raw).strip('"')
            msgstr_clean = re.sub(r'"\s*\n\s*"', '', msgstr_raw).strip('"')
            
            # 位置情報を抽出
            location_match = re.search(r'#:\s*([^\n]+)', entry)
            location = location_match.group(1) if location_match else 'unknown'
            
            parsed_entries.append({
                'msgid': msgid_clean,
                'msgstr': msgstr_clean,
                'location': location,
                'raw_entry': entry
            })
    
    return parsed_entries

def is_translatable_content(msgid: str) -> bool:
    """
    翻訳が必要なコンテンツかどうかを判定
    これまでの作業で判明したパターンを含む改良版
    """
    if not msgid.strip():
        return False
    
    # 明らかにコードのパターン
    code_patterns = [
        r'^\s*def\s+\w+',           # 関数定義
        r'^\s*class\s+\w+',         # クラス定義
        r'^\s*import\s+',           # import文
        r'^\s*from\s+\w+\s+import', # from import文
        r'^\s*>>>\s*',              # doctest
        r'^\s*\.\.\.\s*$',          # doctest continuation
        r'^\s*assert\s+',           # assert文
        r'^\s*return\s+',           # return文
        r'^\s*print\s*\(',          # print関数
        r'^\s*raise\s+',            # raise文
        r'^\s*try\s*:',             # try文
        r'^\s*except\s*[:\w]',      # except文
        r'^\s*if\s+__name__',       # if __name__ == "__main__"
        r'^\s*#.*$',                # コメント行のみ
    ]
    
    for pattern in code_patterns:
        if re.match(pattern, msgid, re.MULTILINE):
            return False
    
    # ファイルパス、URL、バージョン番号のパターン
    non_translatable_patterns = [
        r'^[a-zA-Z_][a-zA-Z0-9_]*\.py$',  # .pyファイル
        r'^https?://',                     # URL
        r'^\d+\.\d+(\.\d+)?$',            # バージョン番号
        r'^[a-zA-Z0-9_/]+\.txt$',         # .txtファイル
        r'^\s*\.\s*$',                    # 単独のドット
        r'^\s*\n\s*$',                    # 改行のみ
    ]
    
    for pattern in non_translatable_patterns:
        if re.match(pattern, msgid.strip()):
            return False
    
    # コードブロック（複数行にわたるコード）
    if re.search(r'(?:def|class|import|from.*import)\s+\w+', msgid):
        return False
    
    # ピュア数値・記号
    if re.match(r'^[\d\s\+\-\*\/\(\)\[\]{},.=<>!&|]+$', msgid.strip()):
        return False
    
    return True

def improved_untranslated_check(filename: str) -> Tuple[int, List[Dict]]:
    """
    改良版未翻訳チェック
    """
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f'❌ ファイル {filename} が見つかりません')
        return 0, []
    
    entries = parse_po_entries(content)
    untranslated_entries = []
    
    for entry in entries:
        # msgstrが空の場合
        if not entry['msgstr'].strip():
            # 翻訳が必要かどうかを判定
            if is_translatable_content(entry['msgid']):
                untranslated_entries.append({
                    'location': entry['location'],
                    'msgid': entry['msgid'][:100] + '...' if len(entry['msgid']) > 100 else entry['msgid'],
                    'full_msgid': entry['msgid']
                })
    
    return len(untranslated_entries), untranslated_entries

def main():
    filename = sys.argv[1] if len(sys.argv) > 1 else 'library/typing.po'
    count, entries = improved_untranslated_check(filename)
    
    print(f'🔍 改良版未翻訳チェック: {filename}')
    print(f'=' * 80)
    print(f'未翻訳エントリ数: {count}')
    
    if entries:
        print('\n未翻訳エントリ:')
        for i, entry in enumerate(entries[:20], 1):  # 最初の20個まで表示
            print(f'{i:3d}: {entry["location"]}')
            print(f'     {entry["msgid"]}')
            print()
        
        if len(entries) > 20:
            print(f'... 他 {len(entries) - 20}個')
    else:
        print('✅ 未翻訳エントリは見つかりませんでした！')
    
    print(f'=' * 80)

if __name__ == "__main__":
    main()