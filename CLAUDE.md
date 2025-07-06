# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

# GEMINI.md: python-docs-ja プロジェクト ガイドライン

### 1. プロジェクト概要

このプロジェクトは、プログラミング言語Pythonの公式ドキュメントを日本語に翻訳する、Pythonプロジェクト公式の翻訳チームです。

### 2. 基本的なワークフロー

翻訳作業は、ユーザーから指定された単一の `.po` ファイルに対して行います。一度に複数のファイルを扱ったり、まとめて翻訳したりはしません。



### 3. 翻訳作業のルール

作業を行う際には、以下のルールを厳守してください。

#### 3.1. poファイルのフォーマットを維持する

-   翻訳は gettext を利用した `.po` ファイル形式で行われます。
-   `msgid` (原文) と `msgstr` (訳文) のペアで構成されています。
-   **絶対に `.po` ファイルの構造を壊さないでください。** 翻訳対象は `msgstr` の中身だけです。

#### 3.2. reStructuredTextの構文を維持する

-   ドキュメントは reStructuredText で記述されています。
-   ``:mod:`` のようなロールや、`.. note::` のようなディレクティブ、リンクなどの構文を壊さないように、細心の注意を払って翻訳してください。

#### 3.3. 翻訳の進め方

-   **既存翻訳の確認:** すでに翻訳されている箇所 (`msgstr` に記述がある箇所) は、原文 (`msgid`) の内容が正しく反映されているかを確認します。必要であれば、より適切で自然な表現に修正します。
-   **未翻訳部分の翻訳:** `msgstr` が空になっている未翻訳の部分は、他の部分の翻訳スタイルやトーンと違和感がないように、自然な日本語訳を作成・追加します。

#### 3.4. 翻訳品質の自動改善

翻訳作業時は、特別な指示がなくても以下の点を自動的にチェックし、読みにくい訳文を改善してください：

-   **不自然な表現の修正:** 「だったり」「させる」などの不自然な語尾や接続表現を自然な日本語に修正
-   **用語の統一:** 同じ概念を表す用語は一貫して使用（例：「並行処理」「並列処理」の使い分け）
-   **技術用語の日本語化:** 一般的に日本語化されている用語は日本語で記述（例：「Transport」→「トランスポート」、「subprocesses」→「サブプロセス」）
-   **語尾の統一:** 箇条書きなどでは語尾をですます調に統一
-   **読みやすさの向上:** 冗長な表現を簡潔にし、より自然で読みやすい日本語に改善
-   **文脈に適した表現:** 技術文書として適切な表現を選択

これらの改善は、翻訳の正確性を保ちながら、より自然で読みやすい日本語文書にするために行います。

### 4. 具体的な作業例

「`library/asyncio.po` を翻訳してください」という指示があった場合、以下の手順で作業を進めます。

**重要**: 翻訳作業は必ず `translate_workflow.py` スクリプトを使用して実行してください。

1. **翻訳ワークフロー開始**:
   ```bash
   python3 translate_workflow.py library/asyncio.po
   ```

2. **作業の自動判定**:
   - スクリプトが既存の作業状況を自動チェック
   - 未着手の場合: 自動的にファイル分割（20KB超の場合）
   - 作業中の場合: 次に翻訳すべきファイルを表示
   - 完了済みの場合: 自動的にファイル結合と最終チェック

3. **翻訳作業の実行**:
   - 表示された分割ファイルを順次翻訳
   - 各ファイル完了後、`.splitted_done/` ディレクトリに移動
   - 翻訳完了後、再度スクリプトを実行して次のファイルへ

4. **完了確認**:
   - 全ファイル翻訳完了後、自動的に結合処理
   - 最終的な翻訳漏れチェックを実行
   - 元のファイルが更新されて翻訳が完了
   - 一時ファイル（`.splitted/`, `.splitted_done/`）は自動削除

5. **作業ファイルの削除**:
   - 翻訳完了後、作成された作業ファイル（`translated_*.po` など）を削除
   - 作業ディレクトリを整理し、不要なファイルを残さない

#### 4.0 翻訳ワークフローシステム

翻訳作業は中断・再開が可能な専用システムで管理されます。

**ディレクトリ構造**:
```
.splitted/              # 分割ファイル格納
  └── [ファイル名]/      # ファイル固有ディレクトリ
.splitted_done/         # 翻訳完了ファイル格納
  └── [ファイル名]/      # ファイル固有ディレクトリ
```

**基本コマンド**:
```bash
# 翻訳開始/再開
python3 translate_workflow.py [ファイル名].po

# 状況確認
python3 translate_workflow.py --status [ファイル名].po

# 完了ファイル結合
python3 translate_workflow.py --join [ファイル名].po
```

**作業フロー**:
1. 20KB以下のファイル: 直接翻訳
2. 20KB超のファイル: 30エントリずつ自動分割
3. 各分割ファイルの翻訳完了後、`.splitted_done/` に移動
4. 全分割ファイル完了後、自動結合と最終チェック

このシステムにより、作業の中断・再開が確実に行え、翻訳漏れを防止できます。

#### 4.1 ファイルの分割（自動化済み）

**注意**: 以下の手動分割手順は `translate_workflow.py` により自動化されています。直接実行する必要はありません。

.poファイルのサイズが20kbを超える場合は、translate_workflow.pyが自動的にsplitpoコマンドでpoファイルを30エントリずつに分割して、それぞれを翻訳します。

**手動実行時の参考コマンド**:
```
 splitpo -h
usage: splitpo [-h] [-o OUTPUT_DIR] [-e ENTRIES] input_file

Split a .po file into chunks by entry count

positional arguments:
  input_file            Input .po file to split

options:
  -h, --help            show this help message and exit
  -o, --output-dir OUTPUT_DIR
                        Output directory for split files
  -e, --entries ENTRIES
                        Number of entries per split file (default: 100)
```

**自動実行例**:
  `translate_workflow.py` が実行: `splitpo -o .splitted/pathlib -e 30 library/pathlib.po`

**分割ファイル命名規則**:
- `input.po` → `input_part_000.po`, `input_part_001.po`, etc.
- Number of digits adjusts to file count (minimum 3 digits)
- Numbering starts from 0

**結合処理**:
翻訳完了後、`translate_workflow.py` が自動的にjoinpoコマンドで分割したファイルを結合します。

```
 joinpo -h
usage: joinpo [-h] -o OUTPUT input_files [input_files ...]

Join split .po files back together

positional arguments:
  input_files          Input .po files to join (supports wildcards)

options:
  -h, --help           show this help message and exit
  -o, --output OUTPUT  Output .po file
```

**自動実行例**:
  `translate_workflow.py` が実行: 
  1. `joinpo -o translated_pathlib.po .splitted_done/pathlib/*.po`
  2. 元のファイルを翻訳済みファイルで更新
  3. 一時ファイルとディレクトリを削除
  4. 作業ファイル（`translated_*.po`）を削除





### 4.2 翻訳の完全性

翻訳作業では、**翻訳が必要なすべてのエントリを必ず翻訳する**必要があります。一部だけを残すことは許可されません。

#### 翻訳が必要なエントリの判別

- **翻訳が必要**: 説明文、エラーメッセージ、ドキュメント本文など
- **翻訳不要（`msgstr ""`のまま）**: 
  - コード実行例（`>>> ...`形式のPythonコード）
  - プログラムコードサンプル
  - ファイルパス例
  - 設定値例
  - コマンド出力例

#### 翻訳作業の要件

1. **完全性の確保**: 翻訳が必要なすべてのエントリを必ず翻訳する
2. **抜け漏れなし**: 時間的制約に関係なく、すべての翻訳対象エントリを完了させる
3. **系統的な作業**: 分割ファイルでも各ファイルのすべての翻訳対象エントリを完了してから次に進む
4. **既存翻訳の確認**: 新規翻訳だけでなく、既存の翻訳についても品質をチェックし、必要に応じて改善する

#### 翻訳完了の確認

翻訳作業を完了する前に、以下を確認してください：

1. すべての説明文が翻訳されている
2. 既存翻訳の品質が改善されている  
3. コード例等の翻訳不要な部分は適切に `msgstr ""` のまま残されている

### 4.3 翻訳作業完了前の必須チェック手順（自動化済み）

**重要**: 以下の最終チェック手順は `translate_workflow.py` により自動化されています。翻訳完了時に自動実行されますが、必要に応じて手動でも実行できます。

#### 最終チェックスクリプトの実行（自動化済み）

`translate_workflow.py` が翻訳完了時に自動実行するチェックスクリプトです。手動実行時は以下のPythonスクリプトを実行し、未翻訳のテキストエントリが残っていないか確認します：

```python
python3 -c "
import re
with open('対象ファイル.po', 'r', encoding='utf-8') as f:
    content = f.read()

# POエントリを分割して真に空のものをカウント
entries = re.split(r'\n\n(?=#)', content)
empty_count = 0

for i, entry in enumerate(entries):
    if 'msgid' in entry and 'msgstr \"\"' in entry:
        lines = entry.strip().split('\n')
        msgstr_started = False
        is_empty = True
        
        # msgidの内容をチェック
        msgid_content = ''
        for line in lines:
            if line.startswith('msgid'):
                msgid_content = line
            elif line.startswith('\"') and not msgstr_started:
                msgid_content += line
        
        # コードサンプルでないテキストエントリかチェック
        is_code_only = ('def ' in msgid_content or 
                       'class ' in msgid_content or 
                       'assert ' in msgid_content or
                       'print(' in msgid_content or
                       'return ' in msgid_content or
                       msgid_content.count('\\\\\"') > 2)
        
        for line in lines:
            if line.startswith('msgstr'):
                msgstr_started = True
                if '\"\"' in line and len(line.strip()) > 9:
                    is_empty = False
                    break
            elif msgstr_started and line.startswith('\"'):
                is_empty = False
                break
        
        if is_empty and not is_code_only:
            empty_count += 1
            print(f'未翻訳テキストエントリ {i+1}:')
            print(msgid_content[:200] + '...' if len(msgid_content) > 200 else msgid_content)
            print('---')

print(f'残り未翻訳テキストエントリ数: {empty_count}')
if empty_count == 0:
    print('✅ All translatable text entries have been translated!')
else:
    print('⚠️  未翻訳のテキストエントリが残っています。これらを翻訳してから作業を完了してください。')
"
```

#### チェック結果の処理

1. **未翻訳エントリが見つからない場合（empty_count = 0）**: 
   - 翻訳作業完了
   - 「✅ All translatable text entries have been translated!」が表示されることを確認

2. **未翻訳エントリが見つかった場合**: 
   - **必ず**すべてのエントリを翻訳してから作業を完了する
   - 翻訳方針:
     - **コードサンプル**: `def`、`class`、`assert`、`print`、`return`等を含む場合は通常そのままコピー
     - **説明文**: 日本語に翻訳
     - **エラーメッセージ**: 日本語に翻訳
     - **ドキュメント文字列**: 日本語に翻訳
     - **技術用語**: 既存の翻訳スタイルに合わせて統一

3. **再チェック**: 
   - 未翻訳エントリを修正後、再度スクリプトを実行
   - 「残り未翻訳テキストエントリ数: 0」になるまで繰り返す

#### このチェックが重要な理由

- 分割→翻訳→結合の過程で翻訳が失われる場合がある
- 大きなファイルでは一部のエントリが見落とされる可能性がある
- 翻訳の品質と完全性を保証するため
- ユーザーに未完成の翻訳を提供することを防ぐため

**注意**: この最終チェックを省略してはいけません。翻訳作業の品質保証において必須の手順です。

### 4.4 翻訳漏れ防止のための必須手順（自動化済み）

**重要**: 以下の翻訳漏れ防止手順は `translate_workflow.py` により自動化されています。手動実行時の参考として記載しています。

#### 翻訳作業開始前の事前確認（自動化済み）

`translate_workflow.py` が自動実行する確認項目:

1. **重複エントリの検出**:
```bash
# 同じmsgidが複数回登場していないかチェック
rg -o 'msgid "[^"]*"' ファイル名.po | sort | uniq -d
```

2. **未翻訳エントリの総数把握**:
```bash
# 翻訳前の未翻訳エントリ数を記録
python3 -c "
import re
with open('ファイル名.po', 'r', encoding='utf-8') as f:
    content = f.read()
print(f'翻訳前未翻訳エントリ数: {len(re.findall(r\"msgstr \\\"\\\"\", content))}')
"
```

#### 翻訳作業中の段階的確認

3. **定期的な進捗確認**:
   - `translate_workflow.py` が進捗状況を自動表示
   - 重複エントリを発見した場合は**すべて**翻訳する

4. **分割ファイル処理時の特別措置**:
   - 各分割ファイルの翻訳完了後、`.splitted_done/` ディレクトリに自動移動
   - 結合前に各分割ファイルの翻訳完了を自動確認

#### 翻訳作業完了前の厳格な最終チェック（自動化済み）

5. **最終チェックスクリプト（改良版）**:
`translate_workflow.py` が自動実行するチェックスクリプト:

```python
python3 -c "
import re
with open('ファイル名.po', 'r', encoding='utf-8') as f:
    content = f.read()

# 重複エントリも含めてすべての未翻訳エントリをチェック
all_entries = re.findall(r'(#: [^\n]+\nmsgid[^m]+?msgstr \"\")', content, re.DOTALL)
untranslated_text = []

for entry in all_entries:
    # コードサンプルを除外
    if not any(marker in entry for marker in ['def ', 'class ', 'assert ', 'print(', 'return ', '>>>', 'import ', 'raise ']):
        untranslated_text.append(entry[:200])

print(f'未翻訳テキストエントリ数: {len(untranslated_text)}')
if untranslated_text:
    print('\\n未翻訳エントリ:')
    for i, entry in enumerate(untranslated_text, 1):
        print(f'{i}: {entry}...')
        print('---')
    print('\\n⚠️  これらのエントリを翻訳してから作業を完了してください。')
else:
    print('✅ すべての翻訳対象エントリが翻訳済みです！')
"
```

#### 品質保証のための二重チェック

6. **翻訳完了後の検証**:
   - `translate_workflow.py` が翻訳前後の未翻訳エントリ数の差分を自動確認
   - 重複エントリがすべて翻訳されていることを自動確認
   - 既存翻訳の品質向上も完了していることを確認

#### 緊急時の対応

7. **翻訳漏れ発見時の対応**:
   - 発見した未翻訳エントリを即座に記録
   - 同じ`msgid`の他のエントリも確認
   - 翻訳完了まで作業を継続

**重要**: `translate_workflow.py` を使用することで、これらの手順が自動化され、翻訳品質が保証されます。

## Repository Structure

The repository is organized as follows:
- Root level: Core documentation files (about.po, bugs.po, copyright.po, etc.)
- `c-api/`: C API documentation translations
- `library/`: Standard library documentation translations  
- `tutorial/`: Tutorial documentation translations
- `reference/`: Language reference translations
- `whatsnew/`: "What's New" documentation for different Python versions
- `deprecations/`: Deprecation notices
- `extending/`, `distributing/`, `installing/`: Advanced topics
- `faq/`, `howto/`: FAQ and how-to guides
- `using/`: Platform-specific usage guides

## Common Development Commands

### Build Documentation
```bash
make                    # Build HTML documentation locally
make htmlview          # Build and open documentation in browser
```

### Translation Management
```bash
make todo              # List remaining translation tasks and show progress
make fuzzy             # Find fuzzy translation strings that need review
make wrap              # Rewrap modified .po files to fix line lengths
```

### Quality Assurance
```bash
make verifs            # Run all verification checks (spell, line-length, sphinx-lint)
make spell             # Check spelling in translation files
make line-length       # Check for lines exceeding 80 characters
make sphinx-lint       # Run Sphinx linting on .po files
```

### Maintenance
```bash
make clean             # Remove build artifacts and temporary files
scripts/update.sh      # Pull latest translations from Transifex (requires setup)
```

## Prerequisites

Before working with this repository, ensure you have the required dependencies:

```bash
# Install CPython documentation build dependencies
python -m pip install -r venv/cpython/Doc/requirements.txt

# Required tools (installed via pip or system package manager)
pip install powrap pospell pomerge potodo
```

## Translation Workflow

1. **Translation Source**: Translations are managed via Transifex, not directly in this repository
2. **File Generation**: .po files are generated from Transifex translations
3. **Local Building**: Use `make` commands to build and verify translations locally
4. **Issue Reporting**: Report translation issues to [python-doc-ja repository](https://github.com/python-doc-ja/python-doc-ja/issues)

## Architecture Notes

- **CPython Integration**: The build system clones CPython repository into `venv/cpython/` and builds documentation using CPython's Sphinx configuration
- **Commit Tracking**: `CPYTHON_CURRENT_COMMIT` in Makefile tracks the specific CPython commit used for generating .po files
- **Excluded Files**: Older Python version documentation (2.x, 3.0-3.10) are excluded from translation
- **Language Configuration**: Target language is Japanese (`ja`), branch is `3.14`

## File Format

All translation files are in gettext .po format containing:
- Original English text (`msgid`)
- Japanese translation (`msgstr`)
- Translation metadata and comments
- Fuzzy markers for translations needing review

## Pull Request Policy

This repository does not accept pull requests. Translation changes must be made through the Transifex platform and will be automatically synchronized to this repository.


