# -*- coding: utf-8 -*-
"""
voices ページの HTML テンプレート。

build_voices.py から読み込まれる。ロジックと分けてあるのは、
この文字列が長く、Python のコードに混ぜると読みにくくなるため。

{tokens} には site/index.html の :root がそのまま入る（配色を二重管理しない）。
{tiles} {blocks} {form_url} {page_url} {count} を build_voices.py が埋める。
CSS の波括弧は format() に食われないよう {{ }} で二重にしてある。
"""

PAGE_TEMPLATE = '''<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Voices｜創部40周年記念寄付金｜慶應義塾體育會ラクロス部</title>
<meta name="description" content="現役の主将、指導陣、OB・OGから届いた言葉。慶應義塾體育會ラクロス部 創部40周年記念寄付金。">
<meta name="theme-color" content="#02011C">

<link rel="canonical" href="{page_url}">

<!-- OGP / Twitter Card -->
<meta property="og:type" content="article">
<meta property="og:site_name" content="慶應義塾體育會ラクロス部 創部40周年記念寄付金">
<meta property="og:title" content="慶應ラクロスを、それぞれの場所から。">
<meta property="og:description" content="現役の主将、指導陣、OB・OGから届いた言葉をお届けします。">
<meta property="og:url" content="{page_url}">
<meta property="og:image" content="https://fund.keiolacrosse.com/assets/img/og.jpg">
<meta property="og:locale" content="ja_JP">
<meta name="twitter:card" content="summary_large_image">

<link rel="icon" href="../assets/img/favicon.svg" type="image/svg+xml">
<link rel="icon" href="../assets/img/favicon-180.png" sizes="180x180">
<link rel="apple-touch-icon" href="../assets/img/favicon-180.png">

<style>
/* =========================================================
   Voices ページ
   配色・書体トークンは site/index.html の :root をそのまま取り込んでいる
   （scripts/build_voices.py が自動で差し込む。手で書き換えないこと）
   ========================================================= */

{tokens}

*,*::before,*::after{{ box-sizing:border-box; }}
html{{ scroll-behavior:smooth; }}
@media (prefers-reduced-motion: reduce){{ html{{ scroll-behavior:auto; }} }}
section[id]{{ scroll-margin-top:92px; }}
@media (max-width:560px){{ section[id]{{ scroll-margin-top:68px; }} }}

body{{
  margin:0; background:var(--ground); color:var(--on-dark);
  font-family:var(--gothic); font-size:17px; line-height:1.95;
  letter-spacing:.02em; -webkit-font-smoothing:antialiased; overflow-x:hidden;
}}
img{{ max-width:100%; height:auto; display:block; }}
/* ロゴは height だけを指定して使う。width:auto を書かないと、width属性(977)が
   効いたまま height だけ縮んで、横に引き伸ばされた状態になる */
.logo{{ display:block; width:auto; height:auto; }}
a{{ color:var(--gold-2); }}
a:focus-visible, button:focus-visible{{ outline:3px solid var(--gold); outline-offset:3px; border-radius:2px; }}
::selection{{ background:rgba(200,162,75,.35); color:#fff; }}

.sr-only{{
  position:absolute; width:1px; height:1px; padding:0; margin:-1px;
  overflow:hidden; clip:rect(0,0,0,0); white-space:nowrap; border:0;
}}
.skip-link{{
  position:absolute; left:-9999px; top:0; z-index:100;
  background:var(--paper-2); color:var(--navy);
  font-weight:700; padding:14px 22px; text-decoration:none;
}}
.skip-link:focus{{ left:16px; top:16px; }}

.wrap{{ width:100%; max-width:var(--wrap); margin-inline:auto; padding-inline:24px; }}
.narrow{{ width:100%; max-width:var(--narrow); margin-inline:auto; padding-inline:24px; }}

/* ===== 日本語の改行 =====
   BudouX がビルド時に入れた <wbr> の位置でだけ折り返す。
   keep-all を当てているので、単語の途中では切れない。
   text-wrap:pretty は最終行に1語だけ残るのを防ぐ（非対応ブラウザでは無視される）。 */
.jp{{
  word-break:keep-all;
  overflow-wrap:break-word;   /* 1文節が1行に収まらない極端な場合の保険 */
  line-break:strict;          /* 句読点や小書き文字の禁則をきつめに */
  text-wrap:pretty;
}}

/* ===== ヘッダー ===== */
.site-header{{
  position:fixed; top:0; left:0; right:0; z-index:70;
  background:rgba(2,1,28,.92); border-bottom:1px solid var(--line-dark);
}}
@supports (backdrop-filter: blur(8px)){{
  @media (min-width:900px){{ .site-header{{ backdrop-filter:blur(10px) saturate(140%); }} }}
}}
.site-header .wrap{{ display:flex; align-items:center; justify-content:space-between; gap:16px; min-height:68px; }}
.brand{{ display:flex; flex-direction:row; align-items:center; gap:13px; line-height:1.3; }}
.brand-logo{{ height:42px; width:auto; flex:none; }}
.brand-txt{{ display:flex; flex-direction:column; }}
.brand b{{ font-family:var(--mincho); font-size:15px; font-weight:600; letter-spacing:.08em; color:#fff; white-space:nowrap; }}
.brand span{{ font-family:var(--display); font-size:11px; letter-spacing:.24em; color:var(--gold); white-space:nowrap; }}
@media (max-width:560px){{
  .site-header .wrap{{ min-height:56px; padding-inline:16px; gap:10px; }}
  .brand-logo{{ height:32px; }}
  .brand b{{ font-size:14px; letter-spacing:.01em; }}
  .brand span{{ display:none; }}
  .site-header .btn{{ padding:9px 13px; font-size:11.5px; letter-spacing:.02em; white-space:nowrap; }}
}}

/* ===== ボタン ===== */
.btn{{
  position:relative; overflow:hidden;
  display:inline-flex; align-items:center; justify-content:center; gap:.7em;
  font-family:var(--gothic); font-weight:700; font-size:15px; letter-spacing:.08em;
  padding:16px 34px; border:1px solid transparent; border-radius:2px;
  text-decoration:none; cursor:pointer;
  transition:color .3s var(--ease), border-color .3s var(--ease);
}}
.btn::before{{
  content:""; position:absolute; inset:0; z-index:0;
  background:linear-gradient(120deg, var(--gold) 0%, var(--gold-2) 100%);
  transform:translateY(101%); transition:transform .45s var(--ease);
}}
.btn > *{{ position:relative; z-index:1; }}
.btn-gold{{ background:linear-gradient(120deg, var(--gold) 0%, var(--gold-2) 100%); color:#05033A; }}
.btn-gold::before{{ background:#fff; }}
.btn-gold:hover::before, .btn-gold:focus-visible::before{{ transform:translateY(0); }}
.btn-dark{{ color:#fff; background:var(--navy); }}
.btn-dark:hover, .btn-dark:focus-visible{{ color:#05033A; }}
.btn-dark:hover::before, .btn-dark:focus-visible::before{{ transform:translateY(0); }}
.btn-ghost{{ color:#fff; border-color:rgba(233,237,246,.4); }}
.btn-ghost:hover, .btn-ghost:focus-visible{{ color:#05033A; border-color:transparent; }}
.btn-ghost:hover::before, .btn-ghost:focus-visible::before{{ transform:translateY(0); }}
/* 明るい面で使う枠線ボタン。紙の上で紺の文字なので 15.9:1 */
.btn-ghost-ink{{ color:var(--navy); border-color:var(--line-light); background:var(--paper-2); }}
.btn-ghost-ink:hover, .btn-ghost-ink:focus-visible{{ color:#05033A; border-color:transparent; }}
.btn-ghost-ink:hover::before, .btn-ghost-ink:focus-visible::before{{ transform:translateY(0); }}
.btn-sm{{ padding:12px 22px; font-size:14px; }}
.site-header .btn{{ white-space:nowrap; flex:none; }}
.btn-arrow::after{{ content:"→"; position:relative; z-index:1; transition:transform .35s var(--ease); }}
.btn:hover.btn-arrow::after{{ transform:translateX(5px); }}
.btn-row{{ display:flex; flex-wrap:wrap; gap:14px; }}

/* ===== 面 ===== */
.s-dark{{
  position:relative;
  background:
    radial-gradient(70% 50% at 82% 0%, rgba(10,7,87,.5) 0%, transparent 58%),
    radial-gradient(60% 50% at 8% 100%, rgba(4,2,61,.8) 0%, transparent 60%),
    var(--ground);
  color:var(--on-dark);
  overflow:hidden;
}}
.s-light{{ position:relative; background:var(--paper); color:var(--on-light); overflow:hidden; }}
/* 暗い面の上辺に金のごく細い光を置いて、面の切り替わりを見せる（LPと同じ作法） */
.s-dark::before{{
  content:""; position:absolute; top:0; left:0; right:0; height:1px;
  background:linear-gradient(90deg, transparent, rgba(200,162,75,.34) 22%, rgba(200,162,75,.34) 78%, transparent);
}}

/* ===== ヒーロー ===== */
.v-hero{{
  position:relative; padding:150px 0 clamp(56px,7vw,84px);
  background:
    radial-gradient(90% 70% at 76% 8%, rgba(21,15,114,.55) 0%, transparent 62%),
    linear-gradient(180deg, #05033F 0%, var(--navy) 30%, var(--ground) 100%);
  overflow:hidden;
}}
@media (max-width:560px){{ .v-hero{{ padding-top:116px; }} }}
.v-hero .eyebrow{{
  display:inline-flex; align-items:center; gap:.9em;
  font-family:var(--display); font-size:16px; letter-spacing:.22em;
  color:var(--gold); margin:0 0 22px; text-transform:uppercase; font-weight:700;
}}
.v-hero .eyebrow::before{{ content:""; width:40px; height:2px; background:var(--gold); }}
.v-hero h1{{
  font-family:var(--mincho); font-weight:600;
  font-size:clamp(27px,4.6vw,46px); line-height:1.45; letter-spacing:.03em;
  margin:0 0 26px; color:#fff; text-wrap:balance;
}}
.v-hero .lead{{ font-size:clamp(16px,1.7vw,18px); color:var(--on-dark-mute); max-width:36em; margin:0; }}
.v-hero .back{{
  display:inline-flex; align-items:center; gap:.5em; margin-top:30px;
  font-size:15px; color:var(--gold-2); text-decoration:none;
  border-bottom:1px solid var(--line-dark); padding-bottom:3px;
}}
.v-hero .back:hover{{ border-bottom-color:var(--gold); }}

/* ===== 一覧タイル ===== */
.v-index{{ padding:clamp(40px,5vw,60px) 0 clamp(56px,6vw,76px); }}
.v-index h2{{
  font-family:var(--display); font-size:14px; letter-spacing:.24em; font-weight:700;
  color:var(--gold); margin:0 0 24px; text-transform:uppercase;
}}
/* 人数が少ないうちは大きく、増えたら自動で列が増える */
.tiles{{
  display:grid; gap:18px;
  grid-template-columns:repeat(auto-fit, minmax(min(280px,100%), 1fr));
}}
.tile{{
  display:flex; align-items:center; gap:16px; text-decoration:none; color:inherit;
  background:rgba(10,7,87,.34); border:1px solid var(--line-soft); padding:14px;
  transition:border-color .35s var(--ease), transform .35s var(--ease), background .35s var(--ease);
}}
.tile:hover{{ border-color:var(--line-dark); transform:translateY(-3px); background:rgba(10,7,87,.55); }}
.tile-img{{
  flex:none; width:76px; height:76px; overflow:hidden;
  background:linear-gradient(140deg,#05033A,#0A0757); border:1px solid var(--line-dark);
}}
/* 正方形のタイルに 4:5 の肖像を流し込む。中央だと胴体が来るので、
   顔のある上寄り（20%）を見せる。全員分これ一律で合う */
.tile-img img{{ width:100%; height:100%; object-fit:cover; object-position:center 20%; }}
.tile-blank{{
  display:block; width:100%; height:100%; opacity:.5;
  background-image:
    repeating-linear-gradient(45deg, rgba(200,162,75,.2) 0 1px, transparent 1px 12px),
    repeating-linear-gradient(-45deg, rgba(200,162,75,.2) 0 1px, transparent 1px 12px);
}}
.tile-body{{ display:flex; flex-direction:column; gap:5px; min-width:0; }}
.tile-body b{{ font-family:var(--mincho); font-size:19px; color:#fff; letter-spacing:.06em; font-weight:600; }}
.tile-meta{{ font-size:13.5px; line-height:1.6; color:var(--on-dark-mute); }}

.badge{{
  display:inline-block; align-self:flex-start;
  font-family:var(--gothic); font-size:12.5px; font-weight:700; letter-spacing:.1em;
  padding:3px 10px; border-radius:2px; line-height:1.7; white-space:nowrap;
}}
.cat-genneki{{ background:rgba(200,162,75,.18); color:var(--gold-2); border:1px solid var(--line-dark); }}
.cat-shidou{{ background:rgba(21,15,114,.55); color:#CFCAF5; border:1px solid rgba(170,160,235,.45); }}
.cat-ob{{ background:rgba(233,237,246,.1); color:var(--on-dark); border:1px solid rgba(233,237,246,.3); }}

/* ===== 1人分：写真と掲げる言葉（暗い面） ===== */
.v-head{{ padding:clamp(56px,7vw,86px) 0; }}
.v-head-grid{{ display:grid; gap:clamp(28px,4vw,52px); align-items:center; grid-template-columns:1fr; }}
@media (min-width:900px){{ .v-head-grid{{ grid-template-columns:.42fr .58fr; }} }}
.v-photo{{ width:100%; max-width:420px; }}
@media (max-width:899px){{ .v-photo{{ max-width:300px; }} }}
.photo{{
  position:relative; display:block; width:100%; overflow:hidden;
  background:linear-gradient(140deg,#05033A 0%,#0A0757 100%); border:1px solid var(--line-dark);
}}
.r-4x5{{ aspect-ratio:4/5; }}
.r-3x2{{ aspect-ratio:3/2; }}
/* 本文の最後に置くプレー写真 */
.v-action{{ margin:2.6em 0 0; }}
.photo img{{ width:100%; height:100%; object-fit:cover; }}
.photo-blank{{
  position:absolute; inset:0; display:flex; align-items:center; justify-content:center;
  font-size:13.5px; letter-spacing:.1em; color:var(--on-dark-mute);
  background-image:
    repeating-linear-gradient(45deg, rgba(200,162,75,.16) 0 1px, transparent 1px 16px),
    repeating-linear-gradient(-45deg, rgba(200,162,75,.16) 0 1px, transparent 1px 16px);
}}
.v-num{{
  display:block; font-family:var(--display); font-weight:800; font-size:46px; line-height:1;
  color:transparent; -webkit-text-stroke:1.4px var(--gold); margin-bottom:18px;
}}
.v-headline{{
  font-family:var(--mincho); font-weight:600;
  font-size:clamp(30px,4.6vw,52px); line-height:1.45; letter-spacing:.04em;
  margin:0 0 26px; color:#fff; text-wrap:balance;
  word-break:keep-all; overflow-wrap:break-word;
}}
.v-name{{ display:flex; flex-wrap:wrap; align-items:baseline; gap:10px 16px; margin:0; }}
.v-name .v-meta{{ font-size:15.5px; color:var(--on-dark-mute); letter-spacing:.04em; }}
.v-name b{{ font-family:var(--mincho); font-size:clamp(21px,2.6vw,27px); color:#fff; letter-spacing:.1em; font-weight:600; }}
.v-name .v-sub{{ font-size:14.5px; color:var(--gold-2); letter-spacing:.06em; }}

/* ===== 1人分：本文（明るい面。ここを読ませる） ===== */
.v-body{{ padding:clamp(48px,6vw,76px) 0 clamp(56px,7vw,84px); }}
/* 本文だけは組み方が違う。見出しや短いリード（.jp）は「文節でしか折らない」が、
   本文は両端揃えにするため「どこでも折る」に戻し、カタカナ語と英数字だけを
   .nb（nowrap）で守っている。詳しくは build_voices.py の body_html() を参照 */
.v-text p{{
  font-family:var(--mincho);
  font-size:clamp(17px,1.9vw,19.5px); line-height:2.15; letter-spacing:.04em;
  margin:0 0 1.7em; color:var(--on-light);
  word-break:normal; overflow-wrap:break-word; line-break:strict; text-wrap:pretty;
  text-align:justify;        /* 右端を揃える（日本語の書籍と同じ組み方） */
  text-align-last:left;      /* ただし段落の最終行は伸ばさない */
}}
/* 「慶應ラクロス」「FINAL4」「OB・OG」などを割らせない */
.nb{{ white-space:nowrap; }}
.v-text p:last-child{{ margin-bottom:0; }}
.v-date{{ margin:2.2em 0 0; font-size:14.5px; color:var(--on-light-mute); letter-spacing:.06em; }}
.v-cta{{ margin-top:2em; }}

/* ===== 末尾のCTA ===== */
.v-end{{ padding:clamp(64px,8vw,104px) 0; text-align:center; }}
.v-end h2{{
  font-family:var(--mincho); font-weight:600;
  font-size:clamp(23px,3.4vw,36px); line-height:1.55; letter-spacing:.04em;
  margin:0 0 20px; color:#fff; text-wrap:balance;
  word-break:keep-all; overflow-wrap:break-word;
}}
.v-end p{{ color:var(--on-dark-mute); margin:0 0 34px; }}
.v-end .btn-row{{ justify-content:center; }}
.v-end .logo{{ height:clamp(52px,6.4vw,72px); width:auto; margin:0 auto 28px; }}

/* ===== フッター ===== */
.site-footer{{
  background:var(--ground); color:var(--on-dark-mute);
  padding:64px 0 80px; font-size:15.5px; border-top:1px solid var(--line-dark);
}}
.site-footer .muted{{ color:var(--on-dark-mute); }}
.footer-logo{{ height:clamp(48px,6vw,64px); width:auto; margin-bottom:22px; }}
.footer-brand{{ font-family:var(--mincho); color:#fff; font-size:19px; letter-spacing:.08em; margin:0 0 6px; }}
.footer-links{{ display:flex; flex-wrap:wrap; gap:10px 26px; margin:26px 0 0; padding:0; list-style:none; }}
.footer-links a{{ display:inline-block; padding:8px 2px; margin:-8px -2px; color:var(--gold-2); }}
.copyright{{ margin-top:34px; font-size:13.5px; color:var(--on-dark-mute); letter-spacing:.06em; }}

/* ===== 現れ方（LPと同じ作法） ===== */
.rv{{ opacity:0; transform:translateY(26px); transition:opacity .85s var(--ease), transform .85s var(--ease); }}
.rv.in{{ opacity:1; transform:none; }}
@media (prefers-reduced-motion: reduce){{
  .rv{{ opacity:1 !important; transform:none !important; transition:none !important; }}
}}

@media print{{
  .site-header{{ display:none !important; }}
  body{{ background:#fff; color:#000; font-size:12px; }}
}}
</style>
</head>
<body>
<a class="skip-link" href="#voices-top">本文へスキップ</a>

<header class="site-header">
  <div class="wrap">
    <div class="brand">
      <picture>
        <source srcset="../assets/img/logo-40th-white.webp" type="image/webp">
        <img class="logo brand-logo" src="../assets/img/logo-40th-white.png"
             alt="慶應ラクロス 創部40周年ロゴ" width="977" height="620">
      </picture>
      <span class="brand-txt">
        <b>慶應義塾體育會ラクロス部</b>
        <span>40TH ANNIVERSARY FUND</span>
      </span>
    </div>
    <a class="btn btn-gold btn-sm" href="{form_url}" target="_blank" rel="noopener"><span>ご寄付のお申し込み<span class="sr-only">（新しいタブで開きます）</span></span></a>
  </div>
</header>

<main id="voices-top">

  <section class="v-hero">
    <div class="wrap">
      <p class="eyebrow">Voices</p>
      <h1 class="jp">慶應ラクロスを、<br>それぞれの場所から。</h1>
      <p class="lead jp">現役の主将、指導陣、そして慶應ラクロスを築いてこられたOB・OGの皆様から届いた言葉を、順にお伝えしていきます。</p>
      <a class="back" href="../">← 創部40周年記念寄付金について</a>
    </div>
  </section>

  <section class="v-index s-dark">
    <div class="wrap">
      <h2>掲載中の{count}名</h2>
      <div class="tiles rv">
{tiles}
      </div>
    </div>
  </section>
{blocks}

  <section class="v-end s-dark">
    <div class="wrap rv">
      <picture><source srcset="../assets/img/logo-40th-white.webp" type="image/webp"><img class="logo" src="../assets/img/logo-40th-white.png" alt="" width="977" height="620" loading="lazy"></picture>
      <h2 class="jp">この挑戦を、次の40年へ。</h2>
      <p class="jp">皆様のご支援が、現役部員の挑戦を支える力になります。</p>
      <div class="btn-row">
        <a class="btn btn-gold btn-arrow" href="{form_url}" target="_blank" rel="noopener"><span>ご寄付のお申し込み<span class="sr-only">（新しいタブで開きます）</span></span></a>
        <a class="btn btn-ghost" href="../"><span>寄付金について詳しく見る</span></a>
      </div>
    </div>
  </section>

</main>

<footer class="site-footer">
  <div class="wrap">
    <picture><source srcset="../assets/img/logo-40th-white.webp" type="image/webp"><img class="logo footer-logo" src="../assets/img/logo-40th-white.png" alt="" width="977" height="620" loading="lazy"></picture>
    <p class="footer-brand">慶應義塾體育會ラクロス部</p>
    <p class="muted" style="margin:0;">創部40周年記念寄付金プロジェクト</p>
    <ul class="footer-links">
      <li><a href="../">寄付金トップ</a></li>
      <li><a href="https://www.keiomenslacrosse.com/" target="_blank" rel="noopener">男子部 公式サイト<span class="sr-only">（新しいタブで開きます）</span></a></li>
      <li><a href="https://keio-womenslacrosse.com/" target="_blank" rel="noopener">女子部 公式サイト<span class="sr-only">（新しいタブで開きます）</span></a></li>
      <li><a href="https://lin.ee/cvTAzM6" target="_blank" rel="noopener">公式LINE<span class="sr-only">（新しいタブで開きます）</span></a></li>
      <li><a href="mailto:fund@mitalax.onmicrosoft.com">お問い合わせ</a></li>
    </ul>
    <p class="copyright">© KEIO UNIVERSITY LACROSSE CLUB. All rights reserved.</p>
  </div>
</footer>

<script>
(function () {{
  'use strict';
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var items = document.querySelectorAll('.rv');
  function show(el) {{ el.classList.add('in'); }}
  if (reduce || !('IntersectionObserver' in window)) {{
    Array.prototype.forEach.call(items, show);
    return;
  }}
  var io = new IntersectionObserver(function (entries) {{
    entries.forEach(function (en) {{
      if (!en.isIntersecting) return;
      show(en.target);
      io.unobserve(en.target);
    }});
  }}, {{ rootMargin: '0px 0px -10% 0px', threshold: 0.1 }});
  Array.prototype.forEach.call(items, function (el) {{ io.observe(el); }});
}})();
</script>

</body>
</html>
'''
