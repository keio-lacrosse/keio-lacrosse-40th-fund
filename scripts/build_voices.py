#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
voices ページ（現役・指導陣・OB/OGのメッセージ）を生成する。

content/voices.json の内容から site/voices/index.html を作る。
原稿を足すときは voices.json に1件追加して、このスクリプトを実行するだけでよい。

日本語の改行について:
  `word-break: auto-phrase` は Chrome/Edge にしか無く、iPhone の Safari では効かない。
  そこで Google の BudouX で文節を判定し、ビルド時に <wbr> を埋め込む。
  CSS 側で word-break:keep-all を当てているので、改行は <wbr> の位置でしか起きない。
  つまり「単語の途中で切れる」ことが原理的に起こらない。

配色トークンは site/index.html の :root からそのまま抜き出して使う。
ベタ書きすると、LP側の色を変えたときにこのページだけ取り残されるため。

使い方（08_寄付金 フォルダで実行）:
    python scripts/build_voices.py
"""

from pathlib import Path
import html as html_mod
import json
import re
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))

from voices_template import PAGE_TEMPLATE

try:
    import budoux
except ImportError:
    print("[エラー] budoux が入っていません。`pip install budoux` を実行してください。")
    sys.exit(1)

BASE = Path(__file__).resolve().parent.parent
DATA = BASE / "content" / "voices.json"
LP = BASE / "site" / "index.html"
OUT = BASE / "site" / "voices" / "index.html"

PAGE_URL = "https://fund.keiolacrosse.com/voices/"
FORM_URL = ("https://forms.cloud.microsoft/Pages/ResponsePage.aspx?"
            "id=0QaieAvhGE2PbSGoTkztRKd54a_JBv9DjjHvS0Lkh0tUMllTVzlHUjRIUDM2SUdTWkxLUE9KSTRUMSQlQCN0PWcu")

CATEGORY = {
    "genneki": ("現役", "cat-genneki"),
    "shidou":  ("指導陣", "cat-shidou"),
    "ob":      ("OB・OG", "cat-ob"),
}

_parser = budoux.load_default_japanese_parser()


# ブラウザが勝手に折ってしまう位置を塞ぐ。
# U+2060 WORD JOINER は「ここでは改行しない」を意味する幅ゼロの文字。
WJ = "⁠"


def no_break(text: str) -> str:
    """中黒と桁区切りの直後で行が割れるのを防ぐ。

    ・（U+30FB）は日本語の行分割規則で「直後に改行してよい」扱いになっているため、
    word-break:keep-all を当てていても「OB・」で行が終わり「OG」が次行に落ちる。
    同じ理由で「1,000」が「1,」と「000」に割れることもある。
    """
    # 置換は lambda で組み立てる（\1 を書くとエスケープ事故が起きやすい）
    text = re.sub(r"([・／/])(?=\S)", lambda m: m.group(1) + WJ, text)       # 中黒・スラッシュの後ろ
    text = re.sub(r"(?<=\d)([,，])(?=\d)", lambda m: m.group(1) + WJ, text)  # 桁区切りの後ろ
    return text


def wbr(text: str) -> str:
    """文節の切れ目に <wbr> を入れる。HTMLエスケープもここで済ませる。

    text 内の \n は <br> にする（短い決め台詞の行を意図どおり折る用）。
    """
    lines = text.split("\n")
    out_lines = []
    for line in lines:
        chunks = _parser.parse(no_break(line))
        out_lines.append("<wbr>".join(html_mod.escape(c) for c in chunks))
    return "<br>".join(out_lines)


# カタカナ（長音記号・中黒を含む）と英数字の連なり。ここだけは途中で折らせない
NO_SPLIT = re.compile(r"[A-Za-z0-9ァ-ヺー・]+")


def body_html(text: str) -> str:
    """本文（両端揃えにする長文）用のマークアップをつくる。

    見出しや短いリードと組み方が違う。あちらは「文節でしか折らない」が、
    本文は両端揃えにしたいので、その方針だと行の長さが揃わず字間が大きく開く
    （実測でスマホの充填率が中央値87.9%まで落ち、41行中16行が85%未満だった）。

    そこで本文は日本語の書籍と同じ「どこでも折る」に戻したうえで、
    **カタカナ語と英数字の連なりだけ** nowrap で守る。
    「慶應ラクロス」「FINAL4」「OB・OG」は割れず、漢字・ひらがなは自由に折れるので、
    行が右端まで埋まり、字間の伸びがほぼ無くなる（充填率の中央値100%）。

    漢字・ひらがなが途中で折れるのは日本語組版では普通で、読み手はまず気づかない。
    目に付くのはカタカナ語と英数字が割れたときなので、そこだけを守っている。
    """
    out_lines = []
    for line in text.split("\n"):
        line = no_break(line)

        # 守る範囲を決める。(開始, 終了) の組で持つ
        spans = [m.span() for m in NO_SPLIT.finditer(line)]

        # 末尾の1文節も守る。ここを自由に折らせると「お返しし／ます。」となり、
        # 最終行に「ます。」だけが残る（ユーザーが最初に指摘した形）。
        # 文節単位で守れば最終行は1文節分（この原稿では7文字前後）の長さになる。
        chunks = _parser.parse(line)
        if chunks:
            tail = chunks[-1]
            if len(tail) >= 2 and line.endswith(tail):
                spans.append((len(line) - len(tail), len(line)))

        # 重なりを潰して左から並べ直す
        spans.sort()
        merged = []
        for st, en in spans:
            if merged and st <= merged[-1][1]:
                merged[-1] = (merged[-1][0], max(merged[-1][1], en))
            else:
                merged.append((st, en))

        buf, pos = [], 0
        for st, en in merged:
            buf.append(html_mod.escape(line[pos:st]))
            buf.append(f'<span class="nb">{html_mod.escape(line[st:en])}</span>')
            pos = en
        buf.append(html_mod.escape(line[pos:]))
        out_lines.append("".join(buf))
    return "<br>".join(out_lines)


def jp_date(iso: str) -> str:
    """2026-09-23 → 2026年9月23日（0埋めを外す）"""
    try:
        y, m, d = iso.split("-")
        return f"{int(y)}年{int(m)}月{int(d)}日"
    except ValueError:
        return html_mod.escape(iso)


def read_tokens() -> str:
    """LP の :root{...} をそのまま取り出す（配色・書体の単一の情報源にする）"""
    src = LP.read_text(encoding="utf-8")
    m = re.search(r"^:root\{.*?^\}", src, re.S | re.M)
    if not m:
        print("[中止] site/index.html から :root が見つかりません")
        sys.exit(1)
    return m.group(0)


def render_tile(v: dict) -> str:
    label, cls = CATEGORY.get(v["category"], ("", ""))
    if v.get("photo"):
        # 見出し横と同じ4:5の画像を使い回す。正方形のタイルには CSS の
        # object-position で顔の高さを出しているので、別途正方形を書き出さない
        img = (f'<picture><source srcset="../assets/img/voices/{v["photo"]}.webp" type="image/webp">'
               f'<img src="../assets/img/voices/{v["photo"]}.jpg" alt="" '
               f'width="720" height="900" loading="lazy" decoding="async"></picture>')
    else:
        img = '<span class="tile-blank" aria-hidden="true"></span>'
    return f'''        <a class="tile" href="#{v["id"]}">
          <span class="tile-img">{img}</span>
          <span class="tile-body">
            <span class="badge {cls}">{label}</span>
            <b>{html_mod.escape(v["name"])}</b>
            <span class="tile-meta">{wbr(v["meta"])}</span>
          </span>
        </a>'''


def render_voice(v: dict, index: int) -> str:
    label, cls = CATEGORY.get(v["category"], ("", ""))
    num = f"{index:02d}"

    if v.get("photo"):
        photo = (f'<picture><source srcset="../assets/img/voices/{v["photo"]}.webp" type="image/webp">'
                 f'<img src="../assets/img/voices/{v["photo"]}.jpg" '
                 f'alt="{html_mod.escape(v["meta"])} {html_mod.escape(v["name"])}さん" '
                 f'width="720" height="900" loading="lazy" decoding="async"></picture>')
    else:
        photo = '<span class="photo-blank" aria-hidden="true">写真を準備中です</span>'

    # プレー中の写真（3:2）。本文を読み終えた位置に置く
    action = ""
    if v.get("photo2"):
        action = (f'''      <div class="v-action">
        <span class="photo r-3x2 clip is-filled"><picture>'''
                  f'<source srcset="../assets/img/voices/{v["photo2"]}.webp" type="image/webp">'
                  f'<img src="../assets/img/voices/{v["photo2"]}.jpg" '
                  f'alt="{html_mod.escape(v["name"])}さんのプレー中の様子" '
                  f'width="1400" height="933" loading="lazy" decoding="async">'
                  f'''</picture></span>
      </div>
''')

    sub = f'<span class="v-sub">{html_mod.escape(v["sub"])}</span>' if v.get("sub") else ""

    insta = ""
    if v.get("instagram"):
        insta = (f'<a class="btn btn-ghost-ink btn-sm" href="{v["instagram"]}" '
                 f'target="_blank" rel="noopener">'
                 f'<span>Instagramで見る<span class="sr-only">（新しいタブで開きます）</span></span></a>')

    paras = "\n".join(f'          <p>{body_html(p)}</p>' for p in v["body"])

    return f'''
  <!-- ============ {v["name"]} ============ -->
  <section class="v-head s-dark" id="{v["id"]}">
    <div class="wrap v-head-grid rv">
      <div class="v-photo">
        <span class="photo r-4x5 clip is-filled">{photo}</span>
      </div>
      <div class="v-intro">
        <span class="v-num">{num}</span>
        <p class="v-headline">「{wbr(v["headline"])}」</p>
        <p class="v-name">
          <span class="badge {cls}">{label}</span>
          <span class="v-meta">{wbr(v["meta"])}</span>
          <b>{html_mod.escape(v["name"])}</b>
          {sub}
        </p>
      </div>
    </div>
  </section>

  <section class="v-body s-light">
    <div class="narrow rv">
      <div class="v-text">
{paras}
      </div>
{action}      <p class="v-date">掲載：{jp_date(v["date"])}</p>
      <div class="btn-row v-cta">
        <a class="btn btn-dark btn-arrow" href="{FORM_URL}" target="_blank" rel="noopener"><span>ご寄付のお申し込み<span class="sr-only">（新しいタブで開きます）</span></span></a>
        {insta}
      </div>
    </div>
  </section>'''


def main() -> int:
    if not DATA.exists():
        print(f"[エラー] {DATA} がありません")
        return 1

    try:
        data = json.loads(DATA.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        # GitHub の画面で手編集する人向け。よくある原因を添える
        print(f"[中止] voices.json の {e.lineno} 行目あたりの書き方が崩れています。\n"
              "  よくある原因: 項目と項目の間の「,」の付け忘れ／最後の項目の後ろの余分な「,」／"
              "「\"」の閉じ忘れ／全角の「”」")
        return 1
    voices = data["voices"]
    if not voices:
        print("[中止] voices が空です")
        return 1

    required = ("id", "category", "headline", "meta", "name", "date", "body")
    for i, v in enumerate(voices, 1):
        lack = [k for k in required if k not in v]
        if lack:
            print(f"[中止] voices の{i}件目（{v.get('name', '名前なし')}）に {', '.join(lack)} がありません")
            return 1
        if v["category"] not in CATEGORY:
            print(f"[中止] {v['name']} の category「{v['category']}」は genneki / shidou / ob のどれかにしてください")
            return 1
        if not re.fullmatch(r"[a-z0-9-]+", v["id"]):
            print(f"[中止] {v['name']} の id「{v['id']}」は半角の小文字英数字とハイフンだけにしてください")
            return 1

    # id の重複はアンカーが壊れるので止める
    ids = [v["id"] for v in voices]
    dup = {i for i in ids if ids.count(i) > 1}
    if dup:
        print(f"[中止] id が重複しています: {dup}")
        return 1

    tokens = read_tokens()
    tiles = "\n".join(render_tile(v) for v in voices)
    blocks = "\n".join(render_voice(v, i + 1) for i, v in enumerate(voices))

    page = PAGE_TEMPLATE.format(
        tokens=tokens, tiles=tiles, blocks=blocks,
        page_url=PAGE_URL, form_url=FORM_URL, count=len(voices))

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(page, encoding="utf-8")

    print(f"生成: {OUT}")
    print(f"  掲載{len(voices)}件 / {OUT.stat().st_size/1024:.0f}KB")
    for v in voices:
        photo = v["photo"] if v.get("photo") else "（写真なし・枠のみ）"
        print(f"  - #{v['id']}  {v['meta']} {v['name']}  写真:{photo}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
