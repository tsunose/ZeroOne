# ZeroOne V2.0.6 変更履歴

V2.0.5で見つかった2件のバグを修正し、自己ホスティングの土台となる
最初の実コード（ZeroOne自身で書いたLexer）を追加しました。

## 修正1（High）: 2段階以上のプロパティ代入ができない

**該当ファイル:** `compiler/parser.py`（`parse_identifier_statement`）

`a.child.value = 5`のように`.`が2回以上連続する代入文が
`ParserError: Unexpected token SYMBOL(.)`でクラッシュしていた。
プロパティ／添字アクセスの代入先を、1段階だけでなく`[...]`と`.name`を
任意の深さまで連続して読み取れるループに書き直した。読み取り専用の式
としての利用（`OUT(a.child.value)`など）はもともと問題なかった。

## 修正2（High）: 値を返さないLAMBDA本体がスタックを壊す

**該当ファイル:** `compiler/generator.py`（`generate_expression`の
`BuiltinCallNode`処理）

`LAMBDA (x) => OUT(...)`のように、本体が`OUT`など「値を残さない」
組み込み処理の場合、暗黙のRETURNが返す値がスタックに無いまま
`RETURN`が実行され、呼び出し元でスタックが1つ不足する
（`VMError: Stack underflow`、あるいは`VISIT`経由では
`Callable returned without a value.`）。

`generate_statement`側は同じ状況を認識して余分な`POP`を
スキップしていたが、`generate_expression`側（式としての利用、
＝暗黙のRETURN対象になるケース含む）には対応するケアが無かった。
`OUT`/`PRINT`/`SHOW`/`DISPLAY`/`ECHO`を式として使った直後に
`PUSH None`を補うようにした。

これにより、`VISIT`の典型的な使い方（副作用だけを行い値を返さない
ビジター関数）が実際に動くようになった。

## 自己ホスティングへの一歩: `self_hosting/lexer.zo`

V2.0.4〜V2.0.6でSTRUCT・ENUM・IMPORT/EXPORT・VISIT・第一級関数などが
実際に動くようになったことを確認するため、ZeroOne自身で書いた
最小限のLexerを追加した。

**注意：これは`compiler/lexer.py`の完全な置き換えではありません。**
対応しているのは整数・識別子・1文字記号・空白の読み飛ばしのみで、
文字列リテラルやコメント、複数文字記号（`>=`など）には未対応です。
「ZeroOneでLexerを書くこと自体が現実的に可能になった」ことを示す
最初のマイルストーンとして位置づけてください。

```
python zo.py run-source self_hosting/lexer.zo
```

で単体実行できます（`x1 + 42 * y`をトークン化するデモが含まれています）。

このファイルを書く過程で、副次的に以下を確認・修正しました。
- `SUBSTR(s, start, end)`は「開始位置＋長さ」ではなく「開始位置＋
  終了位置」（Pythonのスライスと同じ）である仕様を確認（バグではなく
  仕様。デモコード側の誤用を修正）。
- **[未修正・既知の問題として記録]** 整数と文字列を`+`で連結しようと
  すると、`VMError`ではなく生のPython例外（`TypeError`）でクラッシュ
  する。エラーハンドリングとしては本来`VMError`にラップされるべき。
  再現：`OUT(1 + "a")`


