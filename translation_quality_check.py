#!/usr/bin/env python3
"""
翻訳品質統合チェックスクリプト
複数のチェックを組み合わせて翻訳品質を総合的に評価
"""
import re
import sys
from typing import Dict, List, Tuple
from improved_untranslated_check import improved_untranslated_check

def check_rst_syntax_preservation(filename: str) -> Tuple[bool, List[str]]:
    """
    reStructuredText構文が保持されているかチェック
    """
    issues = []
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        return False, [f'ファイル {filename} が見つかりません']
    
    # msgstrの中でRST構文が壊れていないかチェック
    msgstr_pattern = r'msgstr\s+"([^"]*(?:\n"[^"]*)*)"'
    msgstrs = re.findall(msgstr_pattern, content, re.MULTILINE)
    
    for i, msgstr in enumerate(msgstrs):
        if not msgstr.strip():
            continue
            
        # 一般的なRST構文チェック
        if ':' in msgstr and '`' in msgstr:
            # ロール構文のチェック (:func:`name` など)
            role_pattern = r':[a-zA-Z]+:`[^`]+`'
            if re.search(r':[a-zA-Z]+:`[^`]*[^\w\s\.~\-_][^`]*`', msgstr):
                issues.append(f'msgstr {i+1}: 不正なロール構文の可能性')
        
        # リンク構文のチェック
        if '_` <' in msgstr and '>`_' not in msgstr:
            issues.append(f'msgstr {i+1}: 不完全なリンク構文')
    
    return len(issues) == 0, issues

def check_terminology_consistency(filename: str) -> Tuple[bool, List[str]]:
    """
    専門用語の統一性をチェック
    """
    issues = []
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        return False, [f'ファイル {filename} が見つかりません']
    
    # 翻訳された部分のみを抽出
    msgstr_pattern = r'msgstr\s+"([^"]*(?:\n"[^"]*)*)"'
    msgstrs = re.findall(msgstr_pattern, content, re.MULTILINE)
    translated_text = ' '.join([m for m in msgstrs if m.strip()])
    
    # 用語の統一をチェック
    terminology_checks = [
        (r'(?:関数|function)', r'ファンクション', '「関数」と「ファンクション」の混在'),
        (r'(?:メソッド|method)', r'メソード', '「メソッド」と「メソード」の混在'),
        (r'(?:パラメーター|パラメータ)', None, '「パラメーター」と「パラメータ」の混在'),
        (r'(?:引数|argument)', r'アーギュメント', '「引数」と「アーギュメント」の混在'),
        (r'(?:戻り値|返り値|return value)', None, '戻り値表現の不統一'),
    ]
    
    for pattern, avoid_pattern, message in terminology_checks:
        matches = re.findall(pattern, translated_text, re.IGNORECASE)
        if len(set(matches)) > 1:  # 複数の表現が混在
            issues.append(message + f': {set(matches)}')
        
        if avoid_pattern and re.search(avoid_pattern, translated_text, re.IGNORECASE):
            issues.append(f'非推奨用語の使用: {avoid_pattern}')
    
    return len(issues) == 0, issues

def comprehensive_quality_check(filename: str) -> Dict:
    """
    包括的な翻訳品質チェック
    """
    results = {
        'filename': filename,
        'overall_pass': True,
        'checks': {}
    }
    
    print(f'🔍 翻訳品質統合チェック: {filename}')
    print('=' * 80)
    
    # 1. 未翻訳エントリチェック
    print('1. 未翻訳エントリチェック...')
    untranslated_count, untranslated_entries = improved_untranslated_check(filename)
    untranslated_pass = untranslated_count == 0
    results['checks']['untranslated'] = {
        'pass': untranslated_pass,
        'count': untranslated_count,
        'entries': untranslated_entries[:5]  # 最初の5個のみ
    }
    
    if untranslated_pass:
        print('   ✅ 未翻訳エントリなし')
    else:
        print(f'   ❌ 未翻訳エントリ: {untranslated_count}個')
        results['overall_pass'] = False
    
    # 2. RST構文保持チェック
    print('2. reStructuredText構文チェック...')
    rst_pass, rst_issues = check_rst_syntax_preservation(filename)
    results['checks']['rst_syntax'] = {
        'pass': rst_pass,
        'issues': rst_issues
    }
    
    if rst_pass:
        print('   ✅ RST構文は適切に保持されています')
    else:
        print(f'   ⚠️  RST構文の問題: {len(rst_issues)}個')
        for issue in rst_issues[:3]:  # 最初の3個のみ表示
            print(f'      - {issue}')
    
    # 3. 用語統一チェック
    print('3. 専門用語統一性チェック...')
    term_pass, term_issues = check_terminology_consistency(filename)
    results['checks']['terminology'] = {
        'pass': term_pass,
        'issues': term_issues
    }
    
    if term_pass:
        print('   ✅ 用語の統一性は良好です')
    else:
        print(f'   ⚠️  用語統一の改善余地: {len(term_issues)}個')
        for issue in term_issues:
            print(f'      - {issue}')
    
    # 総合判定
    print('\n' + '=' * 80)
    if results['overall_pass']:
        print('🎉 翻訳品質チェック: 合格')
        print('   すべての翻訳対象エントリが完了しています。')
    else:
        print('⚠️  翻訳品質チェック: 要改善')
        print('   未翻訳エントリの解決が必要です。')
    
    print('=' * 80)
    
    return results

def main():
    if len(sys.argv) < 2:
        print('使用方法: python3 translation_quality_check.py <filename.po>')
        sys.exit(1)
    
    filename = sys.argv[1]
    results = comprehensive_quality_check(filename)
    
    # 結果をJSON形式で保存することも可能
    # import json
    # with open(f'{filename}_quality_report.json', 'w', encoding='utf-8') as f:
    #     json.dump(results, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()