#!/usr/bin/env python3
"""
翻訳進捗チェックツール
分割された翻訳ファイルの進捗を確認し、作業再開をサポートします。
"""

import os
import sys
import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional


def get_split_info(po_file: str) -> Tuple[str, str, str]:
    """
    ファイルパスから分割作業用のディレクトリパスを取得
    Returns: (base_name, splitted_dir, done_dir)
    """
    po_path = Path(po_file)
    base_name = po_path.stem
    
    # ファイル固有のディレクトリを作成
    splitted_dir = Path(".splitted") / base_name
    done_dir = Path(".splitted_done") / base_name
    
    return base_name, splitted_dir, done_dir


def check_split_files(splitted_dir: Path) -> List[Path]:
    """分割ファイルの一覧を取得"""
    if not splitted_dir.exists():
        return []
    
    split_files = list(splitted_dir.glob("*_part_*.po"))
    return sorted(split_files)


def check_done_files(done_dir: Path) -> List[Path]:
    """完了ファイルの一覧を取得"""
    if not done_dir.exists():
        return []
    
    done_files = list(done_dir.glob("*_part_*.po"))
    return sorted(done_files)


def get_untranslated_count(po_file: Path) -> int:
    """POファイルの未翻訳エントリ数を取得"""
    try:
        with open(po_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 未翻訳エントリを検出
        all_entries = re.findall(r'(#: [^\n]+\nmsgid[^m]+?msgstr "")', content, re.DOTALL)
        untranslated_text = []
        
        for entry in all_entries:
            # コードサンプルを除外
            if not any(marker in entry for marker in ['def ', 'class ', 'assert ', 'print(', 'return ', '>>>', 'import ', 'raise ']):
                untranslated_text.append(entry)
        
        return len(untranslated_text)
    except Exception:
        return -1


def analyze_progress(po_file: str) -> Dict:
    """翻訳進捗を分析"""
    base_name, splitted_dir, done_dir = get_split_info(po_file)
    
    # 元ファイルの存在確認
    original_exists = os.path.exists(po_file)
    
    # 分割ファイルの確認
    split_files = check_split_files(splitted_dir)
    done_files = check_done_files(done_dir)
    
    # 各ファイルの未翻訳エントリ数を取得
    split_status = {}
    for split_file in split_files:
        untranslated = get_untranslated_count(split_file)
        split_status[split_file.name] = {
            'path': split_file,
            'untranslated': untranslated,
            'completed': untranslated == 0
        }
    
    done_status = {}
    for done_file in done_files:
        untranslated = get_untranslated_count(done_file)
        done_status[done_file.name] = {
            'path': done_file,
            'untranslated': untranslated,
            'completed': untranslated == 0
        }
    
    return {
        'base_name': base_name,
        'original_file': po_file,
        'original_exists': original_exists,
        'splitted_dir': splitted_dir,
        'done_dir': done_dir,
        'split_files': split_files,
        'done_files': done_files,
        'split_status': split_status,
        'done_status': done_status,
        'has_work_in_progress': len(split_files) > 0 or len(done_files) > 0
    }


def print_progress_report(progress: Dict):
    """進捗レポートを表示"""
    print(f"=== 翻訳進捗レポート: {progress['base_name']} ===")
    print(f"元ファイル: {progress['original_file']} ({'存在' if progress['original_exists'] else '不存在'})")
    print(f"分割作業ディレクトリ: {progress['splitted_dir']}")
    print(f"完了ディレクトリ: {progress['done_dir']}")
    
    if not progress['has_work_in_progress']:
        print("✅ 作業中のファイルはありません")
        return
    
    print("\n--- 作業中ファイル ---")
    for filename, status in progress['split_status'].items():
        status_mark = "✅" if status['completed'] else "🔄"
        print(f"{status_mark} {filename}: 未翻訳{status['untranslated']}件")
    
    print("\n--- 完了ファイル ---")
    for filename, status in progress['done_status'].items():
        status_mark = "✅" if status['completed'] else "⚠️"
        print(f"{status_mark} {filename}: 未翻訳{status['untranslated']}件")
    
    # 次の作業提案
    incomplete_splits = [f for f, s in progress['split_status'].items() if not s['completed']]
    if incomplete_splits:
        print(f"\n📋 次の作業: {incomplete_splits[0]} の翻訳を継続")
    else:
        print("\n📋 次の作業: 完了ファイルの結合")


def get_next_action(progress: Dict) -> str:
    """次に実行すべきアクションを取得"""
    if not progress['has_work_in_progress']:
        return "start_fresh"
    
    # 作業中ファイルに未完了があるか確認
    incomplete_splits = [f for f, s in progress['split_status'].items() if not s['completed']]
    if incomplete_splits:
        return "continue_translation"
    
    # すべて完了している場合は結合
    if progress['done_files']:
        return "join_files"
    
    return "unknown"


def main():
    if len(sys.argv) != 2:
        print("使用法: python check_translation_progress.py <po_file>")
        sys.exit(1)
    
    po_file = sys.argv[1]
    if not os.path.exists(po_file):
        print(f"エラー: ファイル '{po_file}' が見つかりません")
        sys.exit(1)
    
    progress = analyze_progress(po_file)
    print_progress_report(progress)
    
    action = get_next_action(progress)
    print(f"\n🎯 推奨アクション: {action}")


if __name__ == "__main__":
    main()