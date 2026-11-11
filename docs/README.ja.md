# IamGroot

[English](../README.md) · [中文](README.zh.md) · [हिन्दी](README.hi.md) · [Español](README.es.md) · [Français](README.fr.md) · [العربية](README.ar.md) · [বাংলা](README.bn.md) · [Português](README.pt.md) · [Русский](README.ru.md) · [اردو](README.ur.md) · [Bahasa Indonesia](README.id.md) · [Deutsch](README.de.md) · **日本語** · [मराठी](README.mr.md) · [Tiếng Việt](README.vi.md)

**あなた専用の仕事探しアシスタント。**

仕事探しにはたくさんの時間がかかります。IamGroot は、時間のかかる退屈な作業をあなたの代わりに行います。Claude Code、Codex、ChatGPT、Gemini、Cursor などの AI チャットツールの中で動くお手伝い役です。どんな仕事にも、どの国でも使えます。

## できること

1. **あなたのことを知る。** 履歴書を読み、どこで働きたいか、いつから働けるかなど、いくつか質問をします。
2. **読みやすい履歴書を作る。** 採用ソフトがまちがえずに読める、1 ページの履歴書を作ります。
3. **仕事を探す。** たくさんの会社の採用ページを調べ、あなたに合う仕事だけを残します。
4. **あなたの代わりに応募する。** 応募フォームにあなたの情報を入力して送信します。お使いの AI ツールがブラウザを使えない場合は、答えを書くので、あなたが送信してください。
5. **一覧にまとめる。** すべての仕事を 1 つの一覧に記録するので、どこに応募してどうなったかがいつでもわかります。
6. **学ぶ。** あなたの答えを覚えるので、同じ質問を二度しません。

## はじめ方

必要なのは AI チャットツールだけです。

1. AI チャットツールを開きます。
2. 次のメッセージをコピーして送信します。

   ```text
   Set up IamGroot from https://github.com/ashok-cse/iamgroot and onboard me.
   ```

   （意味：このアドレスから IamGroot をセットアップして、まず私のことを知ってください。）

3. 履歴書を渡して、質問に答えます。
4. 仕事を探して応募するように頼みます。

## あなたの情報はあなたの手元に

あなたに関する情報はすべて、あなた自身のパソコンの `profile/` というフォルダに保存されます。このプロジェクトに追加されることも、共有されることもありません。

## 絶対にしないこと

- スキルや職歴、答えを作り上げること。あなたにしかわからないことは、あなたに質問します。
- アカウントを作ること、パスワードを入力すること、「私はロボットではありません」の確認をすり抜けること。
- 数を増やすためだけに、あなたに合わない仕事に応募すること。

## くわしい情報

以下のファイルは英語です。

- 手順ごとのしくみ: [`skills/iamgroot/SKILL.md`](../skills/iamgroot/SKILL.md)
- 守っているすべてのルール: [`skills/iamgroot/references/instructions.md`](../skills/iamgroot/references/instructions.md)
- 対応している AI ツール: [`skills/iamgroot/references/agents.md`](../skills/iamgroot/references/agents.md)
- 実際の応募から学んだこと: [`skills/iamgroot/references/lessons.md`](../skills/iamgroot/references/lessons.md)
- 求人サイトのフォームの入力方法: [`skills/iamgroot/references/ats-playbook.md`](../skills/iamgroot/references/ats-playbook.md)
- コマンド: `python3 skills/iamgroot/scripts/iamgroot.py --help`
