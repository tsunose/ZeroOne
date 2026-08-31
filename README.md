# ZeroOne V2.0.5

## 概要

V2.0.5 は、ZeroOne の**セルフホスティング（自己コンパイル）**へ向けた基盤強化版です。

V2.0.4 までに確認・修正された既知のバグを維持しながら、ZeroOne 自身で Lexer / Parser / AST / Compiler を記述するために必要な機能を追加しました。

## 主な変更

### バグ修正・言語基盤

- プロパティ名に予約語を使用できるよう修正
  - `token.type`
  - `TokenType.NUMBER`
- `STRUCT` 宣言を実際の実行時値として生成
- `STRUCT` コンストラクタを追加
- `ENUM` 宣言をメンバー名→整数値のマップとして生成
- ZeroOne の LAMBDA を `MAP` / `FILTER` / `REDUCE` から呼び出せるよう修正
- 高階関数実行時の VM の命令ポインタ処理を修正

### セルフホスティング向け追加

- `READ_FILE`
- `WRITE_FILE`
- `FILE_EXISTS`
- `PATH_JOIN`
- `PATH_DIR`
- `PATH_NAME`
- `CHAR_AT`
- `ORD`
- `CHR`
- `TO_STRING`
- `TO_INT`
- `PARSE_INT`
- `PARSE_FLOAT`
- `VISIT`
- `PACK`
- `UNPACK`

既存の `READ_BYTES` / `WRITE_BYTES` / `PACK_INT` / `UNPACK_INT` などは互換性のため維持します。

### 開発環境

- `.github/workflows/ci.yml` を追加
- V2.0.5 専用の回帰テストを追加
- Python 3.12 + pytest による CI を想定

## セルフホスティングへの位置付け

V2.0.5 の目的は「Pythonを今すぐ削除すること」ではありません。

まず Python 版コンパイラをブートストラップとして利用し、

1. ZeroOne で Lexer を記述
2. ZeroOne で Parser を記述
3. ZeroOne で AST / Generator を記述
4. ZeroOne 版コンパイラから同等の `.zbc` を生成
5. Python 版との出力互換性を確認
6. Python 依存を段階的に削除

という手順で Python 脱却を目指します。

## モジュール

`IMPORT` / `EXPORT` の最小実装を追加しました。

- `IMPORT "file.zo"` はコンパイル時に相対パスからソースを読み込み、ASTへ展開
- ネストしたIMPORTに対応
- 循環IMPORTはエラーとして検出
- `EXPORT name` は公開APIのマーカーとして受理
- 重複して読み込まれたモジュールは一度だけ展開

より高度な名前空間・公開範囲制御は今後の拡張対象です。

## テスト

V2.0.5 では以下を確認します。

- 文字列・数値変換
- STRUCT / ENUM
- 予約語プロパティ
- ZeroOne LAMBDA + MAP / FILTER / REDUCE
- PACK / UNPACK
- 既存 V2.0.4 回帰テスト
