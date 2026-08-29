# ZeroOne

**ZeroOneは、誰でも簡単にプログラムを書けることを目指しているプログラミング言語です。**

## 書きやすい言語

ZeroOneは、できるだけ**シンプルで分かりやすく、書きやすい構文**を目指して作っています。

プログラミングを始めたばかりの人でも、コードを見ただけで何をしているのか分かるような言語を目指しています。

複雑な記述をできるだけ減らし、

- 簡単に書ける
- 読みやすい
- 覚えやすい
- すぐに試せる

そんなプログラミング言語を目指しています。

## 現在の目標

ZeroOneの最終的な大きな目標は、**ZeroOne自身でZeroOneのコンパイラをコンパイルできるようにすること**です。

現在はコンパイラと仮想マシンの一部がPythonで実装されています。
今後はZeroOneでコンパイラを書き直し、段階的にPythonへの依存を減らしていきます。

### Self-hosting

目標は次の流れです。

```text
現在
ZeroOne → Python製コンパイラ → ZeroOne VM

↓

将来
ZeroOne → ZeroOne製コンパイラ → ZeroOne VM
```

最終的には、ZeroOne自身が自分自身をコンパイルできる**自己ホスティング（self-hosting）**を目指します。

## 構成

```text
ZeroOne/
├─ compiler/   # Lexer / Parser / AST / Generator / Bytecode
├─ vm/         # ZeroOne Virtual Machine
├─ tests/      # テスト
├─ zo.py       # ZeroOne CLI
└─ hello.zo    # サンプルプログラム
```

## Hello World

```zeroone
OUT "Hello, ZeroOne!"
EXIT
```

## 実行

```bash
python zo.py compile hello.zo
python zo.py run hello.zbc
```

> 現在は開発途中です。文法やVMの仕様は今後変更される可能性があります。
