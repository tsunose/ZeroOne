# ZeroOne V2.0.7 変更履歴

前回報告した「TRYが再帰関数の奥から例外を捕まえると後続処理が
二重実行される」バグを修正し、さらに`self_hosting/mini_interpreter.zo`
を実際に書いて動かす過程で新たに2件のバグを発見・修正しました。
最後に、自己ホスティングの段階を一つ上げた「変数を持つミニ
インタプリタ」を追加しています。

## 修正1（Critical・前回報告分）: TRYが再帰関数の奥から例外を捕まえると後続処理が二重実行される

**該当ファイル:** `vm/vm.py`

`TRY`命令の実行時に、その時点の`call_stack`の深さを
`call_depth_at_try`として記録するようにし、例外を捕捉してハンドラへ
ジャンプする際に`call_stack`/`locals_stack`をその深さまで切り詰める
ようにした。詳細は前回の報告を参照。

## 修正2（High）: 辞書への動的キー書き込み `obj[key] = value` が壊れている

**該当ファイル:** `vm/vm.py`（`OpCode.ARRAY_SET`）

読み取り（`obj[key]`）は辞書（OBJECT/STRUCT/MAPの実体）に対応済み
だったが、書き込み側は`array[int(index)] = value`と常に整数キー
として扱っていたため、`myenv["x"] = 42`のような文字列キーでの
書き込みが`ValueError: invalid literal for int()`でクラッシュしていた。
`ARRAY_GET`と同様、対象が辞書なら文字列キーとして書き込むように修正。

**再現：**
```
SET env = OBJECT()
env["x"] = 42
OUT(env["x"])
```

**影響：** 変数名のように実行時に決まる文字列をキーとする環境
（シンボルテーブル）を`OBJECT`で実装する、という自己ホスティングで
非常によくあるパターンが使えなかった。

## 修正3（High）: 約250個の「行形式ビルトインのエイリアス名」が、変数として使われた際にインデックス／代入で壊れる

**該当ファイル:** `compiler/parser.py`（`parse_identifier_statement`）

`env`, `size`, `length`, `sort`, `first`, `last`, `max`, `min`, `push`,
`pop`など、`KEYWORD_ALIASES`に登録されている約250個の単語（`PRINT`の
旧行形式構文 `print "hello"` などを支えるためのエイリアス）を**変数名
として使った場合**、その変数を`[]`で添字アクセスしたり代入したりする
と、パーサーが「旧行形式のビルトイン呼び出し」だと誤認して構文エラー
になっていた。これは过去に修正した「予約語問題」の生き残りで、
レキサーのトークン化ではなく、`parse_identifier_statement`内の
別の独立したチェックが原因だった。

**再現：**
```
SET env = OBJECT()
SET key = "x"
env[key] = 42
```
→ `ParserError: Unexpected token in primary: SYMBOL(=)`

**修正：** 次のトークンが`[`・`.`・`=`のいずれかの場合は、旧行形式の
ビルトイン呼び出しとして扱わないようにした（`print "hello"`のような
本来の使い方はそのまま動作する）。

## その他: Lexerがアンダースコアを含む識別子を認識できなかった

**該当ファイル:** `self_hosting/lexer.zo`, `self_hosting/lexer_lib.zo`

`undefined_var`のようにアンダースコアを含む識別子が、字句解析の
時点で`undefined` / `_` / `var`のように分断されてしまっていた。
`isIdentifierStart`/`isIdentifierPart`にアンダースコアの許可を追加。
ZeroOne本体側のバグではなく、ZeroOneで書いたLexer自身の実装漏れ。

## 確認済み・デグレなし

- 元のテストスイート：34件中33件パス（唯一の失敗は無関係な旧
  バージョン番号チェック）。
- V2.0.1〜V2.0.6で修正された全項目を再確認し、すべて引き続き正常。

## 追加: 自己ホスティングの次の段階 `self_hosting/mini_interpreter.zo`

`self_hosting/calculator.zo`（式の評価だけ）から一段階進めて、
**複数の文と変数を持つ小さな言語**をZeroOne自身で実装した。

対応する文法：
```
program   := statement*
statement := "SET" IDENTIFIER "=" expr ";"
           | "OUT" "(" expr ")" ";"
```
変数の環境（シンボルテーブル）は`OBJECT()`を使い、実行時に決まる
変数名をキーとして`env[name]`の形で読み書きする（今回修正した
「辞書への動的キー書き込み」がまさにこの用途で必要になった）。

```
python zo.py run-source self_hosting/mini_interpreter.zo
```

。
