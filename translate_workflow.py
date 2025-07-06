#!/usr/bin/env python3
"""
Translation workflow management script for python-docs-ja project.

This script provides resumable translation workflow by:
1. Splitting large .po files into manageable chunks
2. Tracking translation progress
3. Resuming from interruptions
4. Joining completed translations back together
"""

import os
import sys
import glob
import subprocess
import argparse
from pathlib import Path


def get_file_size_kb(filepath):
    """Get file size in KB."""
    return os.path.getsize(filepath) / 1024


def get_base_filename(filepath):
    """Get base filename without extension."""
    return Path(filepath).stem


def check_existing_work(po_file):
    """Check for existing split files or completed work."""
    base_name = get_base_filename(po_file)
    
    # Check for existing split files
    splitted_dir = f".splitted/{base_name}"
    done_dir = f".splitted_done/{base_name}"
    
    existing_splits = []
    completed_splits = []
    
    if os.path.exists(splitted_dir):
        existing_splits = glob.glob(f"{splitted_dir}/*.po")
        existing_splits.sort()
    
    if os.path.exists(done_dir):
        completed_splits = glob.glob(f"{done_dir}/*.po")
        completed_splits.sort()
    
    return existing_splits, completed_splits


def split_po_file(po_file, entries_per_split=30):
    """Split .po file into chunks."""
    base_name = get_base_filename(po_file)
    output_dir = f".splitted/{base_name}"
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Run splitpo command
    cmd = ["splitpo", "-o", output_dir, "-e", str(entries_per_split), po_file]
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"Error splitting file: {result.stderr}")
        return []
    
    # Return list of created split files
    split_files = glob.glob(f"{output_dir}/*.po")
    split_files.sort()
    return split_files


def join_po_files(po_file):
    """Join completed split files back together."""
    base_name = get_base_filename(po_file)
    done_dir = f".splitted_done/{base_name}"
    
    if not os.path.exists(done_dir):
        print(f"No completed translations found in {done_dir}")
        return False
    
    # Get all completed files
    completed_files = glob.glob(f"{done_dir}/*.po")
    completed_files.sort()
    
    if not completed_files:
        print(f"No completed translation files found in {done_dir}")
        return False
    
    # Create output filename
    output_file = f"translated_{base_name}.po"
    
    # Run joinpo command
    cmd = ["joinpo", "-o", output_file] + completed_files
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"Error joining files: {result.stderr}")
        return False
    
    print(f"✅ Translation completed! Output: {output_file}")
    return True


def get_translation_status(po_file):
    """Get translation status and next file to work on."""
    existing_splits, completed_splits = check_existing_work(po_file)
    
    if not existing_splits:
        return "not_started", None, 0, 0
    
    # Find next file to translate
    completed_basenames = {Path(f).name for f in completed_splits}
    
    for split_file in existing_splits:
        split_basename = Path(split_file).name
        if split_basename not in completed_basenames:
            total_splits = len(existing_splits)
            completed_count = len(completed_splits)
            return "in_progress", split_file, completed_count, total_splits
    
    # All splits are completed
    total_splits = len(existing_splits)
    return "ready_to_join", None, total_splits, total_splits


def move_to_done(split_file, po_file):
    """Move completed split file to done directory."""
    base_name = get_base_filename(po_file)
    done_dir = f".splitted_done/{base_name}"
    
    os.makedirs(done_dir, exist_ok=True)
    
    split_basename = Path(split_file).name
    dest_path = f"{done_dir}/{split_basename}"
    
    # Copy the file
    subprocess.run(["cp", split_file, dest_path], check=True)
    print(f"✅ Completed: {split_basename}")


def run_final_check(output_file):
    """Run the final translation completeness check."""
    check_script = f"""
import re
with open('{output_file}', 'r', encoding='utf-8') as f:
    content = f.read()

# 重複エントリも含めてすべての未翻訳エントリをチェック
all_entries = re.findall(r'(#: [^\\n]+\\nmsgid[^m]+?msgstr "")', content, re.DOTALL)
untranslated_text = []

for entry in all_entries:
    # コードサンプルを除外
    if not any(marker in entry for marker in ['def ', 'class ', 'assert ', 'print(', 'return ', '>>>', 'import ', 'raise ']):
        untranslated_text.append(entry[:200])

print(f'未翻訳テキストエントリ数: {{len(untranslated_text)}}')
if untranslated_text:
    print('\\n未翻訳エントリ:')
    for i, entry in enumerate(untranslated_text, 1):
        print(f'{{i}}: {{entry}}...')
        print('---')
    print('\\n⚠️  これらのエントリを翻訳してから作業を完了してください。')
else:
    print('✅ すべての翻訳対象エントリが翻訳済みです！')
"""
    
    result = subprocess.run(["python3", "-c", check_script], capture_output=True, text=True)
    print(result.stdout)
    return "未翻訳テキストエントリ数: 0" in result.stdout


def main():
    parser = argparse.ArgumentParser(description="Manage translation workflow for .po files")
    parser.add_argument("po_file", help="Path to .po file to translate")
    parser.add_argument("--entries", "-e", type=int, default=30, help="Entries per split file")
    parser.add_argument("--status", action="store_true", help="Show translation status only")
    parser.add_argument("--join", action="store_true", help="Join completed files only")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.po_file):
        print(f"Error: File {args.po_file} not found")
        return 1
    
    # Check if file needs splitting
    file_size_kb = get_file_size_kb(args.po_file)
    needs_splitting = file_size_kb > 20
    
    print(f"📄 File: {args.po_file} ({file_size_kb:.1f} KB)")
    
    if args.join:
        success = join_po_files(args.po_file)
        if success:
            # Run final check
            base_name = get_base_filename(args.po_file)
            output_file = f"translated_{base_name}.po"
            print(f"\n🔍 Running final completeness check...")
            run_final_check(output_file)
        return 0 if success else 1
    
    # Get current status
    status, next_file, completed, total = get_translation_status(args.po_file)
    
    if args.status:
        print(f"Status: {status}")
        if next_file:
            print(f"Next file: {next_file}")
        print(f"Progress: {completed}/{total}")
        return 0
    
    # Handle different statuses
    if status == "not_started":
        if needs_splitting:
            print(f"🔄 Splitting file into {args.entries}-entry chunks...")
            split_files = split_po_file(args.po_file, args.entries)
            if split_files:
                print(f"✅ Created {len(split_files)} split files")
                print(f"📝 Next: Translate {split_files[0]}")
            else:
                print("❌ Failed to split file")
                return 1
        else:
            print(f"📝 File is small enough ({file_size_kb:.1f} KB), translate directly")
    
    elif status == "in_progress":
        print(f"🔄 Resuming translation... Progress: {completed}/{total}")
        print(f"📝 Next file to translate: {next_file}")
    
    elif status == "ready_to_join":
        print(f"✅ All {total} files completed! Ready to join...")
        success = join_po_files(args.po_file)
        if success:
            # Run final check
            base_name = get_base_filename(args.po_file)
            output_file = f"translated_{base_name}.po"
            print(f"\n🔍 Running final completeness check...")
            run_final_check(output_file)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())