#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
公開用のサイト一式を _site/ に組み立てる。GitHub Actions が push のたびに実行する。

  1. content/voices.json から voices ページを生成（build_voices.py）
  2. site/ を _site/ にコピー
  3. photos/ に上げられた写真を Web 用に変換して、同名の写真を差し替える
  4. 口座番号の混入チェック

ここで失敗すると公開は行われず、サイトは前の版のまま残る。
エラー文は GitHub の Actions 画面に出るので、編集者が読める日本語で書く。

使い方（リポジトリ直下で実行）:
    python scripts/build_site.py
"""

from pathlib import Path
import json
import shutil
import subprocess
import sys

from PIL import Image, ImageOps

BASE = Path(__file__).resolve().parent.parent
SITE = BASE / "site"
PHOTOS = BASE / "photos"
OUT = BASE / "_site"

ACCOUNT_NO = "7778540"
PHOTO_EXTS = {".jpg", ".jpeg", ".png", ".webp"}

# 長辺の最大px。ここに無い写真は DEFAULT_EDGE
EDGE = {"hero": 2000}
DEFAULT_EDGE = 1600


def fail(msg: str) -> None:
    print(f"\n[公開を中止しました] {msg}\nサイトは前の版のまま変わっていません。")
    sys.exit(1)


def convert(src: Path, dest_dir: Path, name: str, max_edge: int) -> None:
    """1枚を webp と jpg に書き出す。保存し直すので位置情報などの EXIF は消える。"""
    try:
        with Image.open(src) as im:
            im = ImageOps.exif_transpose(im).convert("RGB")   # スマホ写真の回転を反映
            im.thumbnail((max_edge, max_edge), Image.LANCZOS)
            im.save(dest_dir / f"{name}.webp", "WEBP", quality=82, method=6)
            im.save(dest_dir / f"{name}.jpg", "JPEG", quality=84, optimize=True, progressive=True)
            print(f"  写真を差し替え: {src.relative_to(BASE)} → {name} ({im.width}x{im.height})")
    except OSError:
        fail(f"{src.relative_to(BASE)} を写真として読み込めませんでした。JPEG か PNG で保存し直して上げてください。")


def voice_photo_names() -> set[str]:
    data = json.loads((BASE / "content" / "voices.json").read_text(encoding="utf-8"))
    return {v[k] for v in data["voices"] for k in ("photo", "photo2") if v.get(k)}


def apply_photos() -> None:
    if not PHOTOS.exists():
        return
    voice_names = voice_photo_names()
    for src in sorted(PHOTOS.rglob("*")):
        if not src.is_file() or src.name.lower() == "readme.md":
            continue
        rel = src.relative_to(BASE)
        if src.suffix.lower() not in PHOTO_EXTS:
            fail(f"{rel} は使えない形式です（使えるのは jpg / jpeg / png / webp）。"
                 "iPhone の HEIC 形式は JPEG に変換してから上げてください。")
        name = src.stem
        if src.parent == PHOTOS / "voices":
            if name not in voice_names:
                fail(f"{rel} の名前が voices.json のどの photo / photo2 とも一致しません。"
                     "ファイル名か voices.json を直してください。")
            convert(src, OUT / "assets" / "img" / "voices", name, 1400 if name.endswith("-2") else 900)
        elif src.parent == PHOTOS:
            if not (SITE / "assets" / "img" / f"{name}.jpg").exists():
                fail(f"{rel} の名前（{name}）に一致する写真の枠がありません。"
                     "photos/README.md の一覧にある名前で上げてください。")
            convert(src, OUT / "assets" / "img", name, EDGE.get(name, DEFAULT_EDGE))
        else:
            fail(f"{rel} は置き場所が違います。photos/ か photos/voices/ に置いてください。")


def check_voice_photos() -> None:
    """voices.json が指している写真が、どこにも無いまま公開されるのを防ぐ"""
    out_dir = OUT / "assets" / "img" / "voices"
    missing = [n for n in sorted(voice_photo_names()) if not (out_dir / f"{n}.jpg").exists()]
    if missing:
        fail("voices.json に書かれた写真が見つかりません: " + ", ".join(missing)
             + "\n  photos/voices/ に、その名前で写真を上げてください（例: " + missing[0] + ".jpg）。")


def main() -> int:
    r = subprocess.run([sys.executable, str(BASE / "scripts" / "build_voices.py")])
    if r.returncode != 0:
        fail("voices ページを作れませんでした（上のメッセージを確認してください）。")

    if OUT.exists():
        shutil.rmtree(OUT)
    shutil.copytree(SITE, OUT, ignore=shutil.ignore_patterns("README.md"))
    (OUT / "assets" / "img" / "voices").mkdir(parents=True, exist_ok=True)

    apply_photos()
    check_voice_photos()

    # 安全弁: 口座番号はフォーム記入後に個別案内する方式。ページに載るのは想定外
    for p in OUT.rglob("*.html"):
        if ACCOUNT_NO in p.read_text(encoding="utf-8"):
            fail(f"口座番号がページ（{p.relative_to(OUT)}）に含まれています。口座情報はサイトに載せない決まりです。")

    n = sum(1 for p in OUT.rglob("*") if p.is_file())
    print(f"\n組み立て完了: {OUT}（{n}ファイル）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
