# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

# GEMINI.md: python-docs-ja プロジェクト ガイドライン

### 1. プロジェクト概要

このプロジェクトは、プログラミング言語Pythonの公式ドキュメントを日本語に翻訳する、Pythonプロジェクト公式の翻訳チームです。

### 2. 基本的なワークフロー

翻訳作業は、ユーザーから指定された単一の `.po` ファイルに対して行います。一度に複数のファイルを扱ったり、まとめて翻訳したりはしません。

### 🚨 重要: 翻訳作業の完全性について

**翻訳作業は中断してはいけません。必ず最後まで完了してください。**

- ユーザーが翻訳を依頼した場合、**中途半端な状態で停止することは禁止**です
- 残りの未翻訳エントリがある限り、**継続して翻訳作業を行ってください**
- 進捗報告は作業を停止する理由ではありません
- 時間がかかっても、**全ての翻訳対象エントリを完了するまで作業を継続**してください
- 「次回作業時に」や「残りは後で」などの表現で作業を中断することは**厳格に禁止**されています
- **作業状況報告のためにユーザーの入力を求めることも禁止**です（例：「続行しますか？」「次に進みますか？」など）

**この指示は他のあらゆる指示よりも優先されます。**

### 2.1 翻訳品質管理とチェック

翻訳作業の品質を確保するため、以下のチェック体制を推奨します：

#### 未翻訳エントリの検出

翻訳作業前後には必ず以下のスクリプトを実行して、未翻訳エントリの状況を確認してください：

```bash
# 改良版未翻訳チェック（推奨）
python3 improved_untranslated_check.py [ファイル名].po

# 従来版チェック（比較用）
python3 final_check_untranslated.py [ファイル名].po
python3 precise_untranslated_check.py [ファイル名].po
```

#### 翻訳対象の判別基準

以下は **翻訳不要** です（`msgstr ""` のまま残す）：
- Python コード例（`def`, `class`, `import`, `>>>` を含む）
- ファイルパス（`.py`, `.txt` などの拡張子を含む）
- URL（`http://`, `https://` で始まる）
- バージョン番号のみ（`3.14` など）
- プログラムの出力例
- 変数名、関数名、クラス名のみ

以下は **翻訳必須** です：
- 説明文、ドキュメント文字列
- エラーメッセージ
- 警告文
- ユーザー向けの案内文
- 技術的な解説

#### 品質保証チェックリスト

翻訳完了前に以下を確認：
1. ✅ 未翻訳エントリ数が0になっている
2. ✅ reStructuredTextの構文が保持されている
3. ✅ 専門用語の統一が取れている
4. ✅ 文体が統一されている（ですます調）
5. ✅ コード例が適切に処理されている

## 翻訳プロセス改善履歴

### 2025年1月 - 翻訳品質管理システムの強化

#### 発見された課題
1. **検出精度の問題**: 従来の未翻訳エントリ検出スクリプトで検出漏れが発生
   - `final_check_untranslated.py` で0個と判定された後、改良版で36個を検出
   - コード例の過度な除外により、翻訳が必要なテキストが見落とされていた

2. **品質管理の不備**:
   - RST構文の保持チェックが不十分
   - 専門用語統一性の確認が手動に依存
   - 包括的な品質評価システムの欠如

#### 実装された改善策

##### 1. 改良版未翻訳エントリ検出システム
**ファイル**: `improved_untranslated_check.py`

**主な改善点**:
- より正確なマルチライン解析
- 翻訳対象判別ロジックの精緻化
- コード例と説明文の適切な分類

**使用方法**:
```bash
python3 improved_untranslated_check.py [ファイル名].po
```

##### 2. 統合品質チェックシステム
**ファイル**: `translation_quality_check.py`

**チェック項目**:
- 未翻訳エントリの検出
- reStructuredText構文の保持確認
- 専門用語統一性の評価

**使用方法**:
```bash
python3 translation_quality_check.py [ファイル名].po
```

##### 3. 翻訳対象判別基準の明確化

**翻訳不要な項目（改訂版）**:
```
- 関数定義: def function_name()
- クラス定義: class ClassName
- import文: import module / from module import
- doctest例: >>> code
- assert文: assert condition
- return文: return value
- print文: print(...)
- 例外処理: raise Exception / try: / except:
- ファイルパス: module.py, file.txt
- URL: http://, https://
- バージョン番号: 3.14, 1.0.0
- 純粋な数値・記号列
```

**翻訳必須な項目（改訂版）**:
```
- 技術的説明文
- ユーザー向けガイダンス
- エラーメッセージ・警告文
- 機能の動作説明
- パラメーター・戻り値の説明
- 使用例の文章説明部分
- 注意事項・補足説明
```

#### 推奨ワークフロー（改訂版）

**翻訳作業開始前**:
```bash
# 1. 改良版チェックで正確な未翻訳数を把握
python3 improved_untranslated_check.py [ファイル名].po

# 2. 既存スクリプトとの比較（デバッグ用）
python3 final_check_untranslated.py [ファイル名].po
python3 precise_untranslated_check.py [ファイル名].po
```

**翻訳作業中**:
- 翻訳対象判別基準に従って系統的に作業
- 不明な場合は翻訳する方向で判断
- RST構文の保持に注意

**翻訳作業完了後**:
```bash
# 包括的品質チェック
python3 translation_quality_check.py [ファイル名].po

# 未翻訳エントリが0になるまで作業継続
# RST構文エラーがある場合は修正
# 用語統一の問題がある場合は調整
```

#### 今後の課題と改善計画

**短期的改善（次回翻訳作業時に実装）**:
1. `library/typing.po` の36個の追加未翻訳エントリの精査と翻訳
2. RST構文エラー（19個検出）の修正
3. 用語統一（パラメーター/パラメータ、戻り値/返り値）の調整

**中期的改善（継続的に実装）**:
1. 翻訳メモリシステムの構築
2. 自動翻訳品質スコアリング
3. CI/CDパイプラインへの品質チェック統合

**長期的改善（将来検討）**:
1. 機械学習による翻訳対象自動判別
2. リアルタイム翻訳品質フィードバック
3. 多言語翻訳プロジェクトへの拡張

#### 教訓とベストプラクティス

**重要な教訓**:
1. **複数のチェックツールの併用**: 単一のツールでは検出漏れが発生する
2. **翻訳対象の保守的判断**: 迷った場合は翻訳する方向で判断
3. **品質チェックの自動化**: 人手によるチェックは漏れが生じやすい
4. **継続的改善**: 翻訳作業を通じて検出システムを継続的に改良

**確立されたベストプラクティス**:
1. 翻訳作業は中断せず最後まで完了する
2. 複数のチェックスクリプトで相互検証する
3. 品質チェックは翻訳完了の必須条件とする
4. 改善点は必ずドキュメント化して共有する



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

`translate_workflow.py` が翻訳完了時に自動実行するチェックスクリプトです。手動実行時は以下の2つの方法で未翻訳エントリを確認できます：

**方法1: 専用スクリプトを使用（推奨）**
```bash
python3 check_untranslated.py 対象ファイル.po
```

**方法2: シンプルな検証スクリプト**
```bash
python3 validate_translation.py 対象ファイル.po
```

**方法3: 手動での簡易チェック**
```bash
# 空のmsgstrを検索
grep -n 'msgstr ""' 対象ファイル.po | wc -l
```

**構文エラーの回避**

翻訳作業中に以下のようなエラーが発生する場合：
```
SyntaxError: unexpected character after line continuation character
```

これは埋め込みPythonスクリプトの文字エスケープ問題です。以下の対策を取ってください：

1. **専用スクリプトの使用**: 埋め込みスクリプトではなく、独立したPythonファイル（`check_untranslated.py` や `validate_translation.py`）を使用する

2. **文字エスケープの注意**: 複雑な正規表現や文字列処理を含む場合は、埋め込みスクリプトを避ける

3. **シンプルな検証**: 完全な分析が不要な場合は、`grep` や `wc` コマンドを使用した簡易チェックを利用する

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
python3 validate_translation.py ファイル名.po
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

```bash
# 専用スクリプトを使用（推奨）
python3 check_untranslated.py ファイル名.po

# または簡易版
python3 validate_translation.py ファイル名.po
```

**注意**: 埋め込みPythonスクリプトは文字エスケープの問題で構文エラーが発生する可能性があるため、独立したスクリプトファイルを使用することを強く推奨します。

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

### 4.5 翻訳作業完了後の未翻訳部分検索と件数報告

翻訳作業完了後、必ず以下の手順で未翻訳部分を検索し、件数を報告してください。

#### 未翻訳部分検索スクリプト

以下の3つの方法で未翻訳エントリを確認できます：

**方法1: 詳細分析スクリプト（推奨）**
```bash
# 専用スクリプトを実行
python3 check_untranslated.py [ファイル名.po]

# 例: library/typing.poをチェック
python3 check_untranslated.py library/typing.po
```

**方法2: 簡易検証スクリプト**
```bash
python3 validate_translation.py [ファイル名.po]
```

**方法3: 手動での簡易チェック**
```bash
# 空のmsgstrを検索
grep -n 'msgstr ""' [ファイル名.po] | wc -l
```

#### 構文エラーの回避

これらの独立したスクリプトファイルを使用することで、埋め込みPythonスクリプトで発生していた以下の構文エラーを回避できます：
```
SyntaxError: unexpected character after line continuation character
```

#### 分析内容

`check_untranslated.py` は以下の分類で未翻訳エントリを分析します：
- **翻訳が必要**: 実際に日本語翻訳が必要なテキスト
- **翻訳不要**: コードサンプル、パス、URL、バージョン番号など

スクリプトは以下の情報を提供します：
- 総未翻訳エントリ数
- 翻訳不要エントリ数（コードサンプル等）
- 翻訳が必要なエントリ数
- 翻訳完了率
- 未翻訳エントリの一覧（最初の20個）

#### 実行例

```bash
# 特定のファイルをチェック
python3 -c "[上記スクリプト]" library/typing.po

# 結果例:
# 📊 翻訳状況レポート: library/typing.po
# ============================================================
# 未翻訳テキストエントリ数: 15
# ⚠️  15個の未翻訳エントリが残っています
# 
# 未翻訳エントリ一覧:
# ------------------------------------------------------------
# 行  123: msgid "ABCs and Protocols for working with I/O"
# 行  156: msgid "Generic class ``IO[AnyStr]`` and its subclasses..."
# ...
```

#### 報告形式

翻訳作業完了時は、以下の形式で必ず報告してください：

```
翻訳完了報告: [ファイル名]
- 処理したファイル: library/typing.po
- 翻訳完了エントリ数: [数]
- 残り未翻訳エントリ数: [数]
- 翻訳完了率: [%]

未翻訳が残っている場合の理由:
- コードサンプル: [数]個
- 技術的制約: [数]個  
- その他: [数]個

次回作業時の優先事項:
- [具体的な作業内容]
```

#### 継続作業のガイドライン

1. **未翻訳が残っている場合**:
   - 理由を明確にする（コードサンプル、技術的制約など）
   - 次回の作業優先順位を設定
   - 翻訳可能な部分は可能な限り完了させる

2. **完全翻訳完了の場合**:
   - 最終確認を実施
   - 翻訳品質の検証
   - 作業完了を明確に報告

この手順により、翻訳の進捗状況を正確に把握し、継続的な改善が可能になります。

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

## 翻訳品質管理システムの改善記録

### 改善の背景

`library/typing.po` の翻訳作業中に、従来の検出スクリプトでは見逃されていた未翻訳エントリが36個発見されました。これを受けて、翻訳品質管理システムを改善しました。

### 実装された改善策

#### 1. 改良版未翻訳検出スクリプト (`improved_untranslated_check.py`)

**主な改善点:**
- より正確な .po ファイル解析（マルチライン対応改善）
- 翻訳対象判別ロジックの強化
- コードサンプルとテキストの区別精度向上
- ファイルパス、URL、バージョン番号の適切な除外

**使用方法:**
```bash
python3 improved_untranslated_check.py [ファイル名].po
```

#### 2. 統合品質チェックスクリプト (`translation_quality_check.py`)

**チェック項目:**
- 未翻訳エントリの検出
- reStructuredText構文の保持確認  
- 専門用語統一性チェック

**使用方法:**
```bash
python3 translation_quality_check.py [ファイル名].po
```

### 推奨ワークフロー

#### 翻訳作業前
```bash
# 初期状態確認
python3 improved_untranslated_check.py [ファイル名].po
```

#### 翻訳作業中
- 定期的な進捗確認
- 系統的な翻訳実行（すべてのエントリを完了）

#### 翻訳作業後  
```bash
# 最終品質チェック
python3 translation_quality_check.py [ファイル名].po

# 従来版との比較（オプション）
python3 final_check_untranslated.py [ファイル名].po
```

### 品質保証の要点

1. **完全性の確保**: すべての翻訳対象エントリを必ず翻訳する
2. **検出精度の向上**: 改良版スクリプトで見逃しを防止
3. **継続的改善**: 新たに発見された課題に基づく随時改善

### 学んだ教訓

- 翻訳作業は**中断せず最後まで完了**することが最重要
- **ユーザーの確認を求めて作業を中断してはいけない**
- 複数の検出手法を組み合わせることで品質向上
- 定期的なツール改善により作業効率と品質が向上
- 自律的な作業継続が翻訳品質の向上に直結

この改善により、今後の翻訳作業の品質と効率が大幅に向上することが期待されます。


