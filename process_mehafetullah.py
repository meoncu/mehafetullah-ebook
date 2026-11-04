# -*- coding: utf-8 -*-
"""
MEHÂFETULLÂH (ALLAH KORKUSU) - Abdülkâdir Geylânî (k.s.)
Complete 121-page Digital Extraction, Cleaning, and Database Generation
"""

import os
import re
import json
import pypdf

# 1. Parse TOC to map topics to PDF pages
with open('Mehafetullah_toc_raw.txt', 'r', encoding='utf-8') as f:
    toc_raw = f.read()

toc_lines = [l.strip() for l in toc_raw.splitlines() if l.strip()]
filtered = []
for l in toc_lines:
    if l == 'İçindekiler' or re.search(r'\bMehafetullah\b|Abdülkadir Geylani \d+', l):
        continue
    filtered.append(l)

combined = []
i = 0
while i < len(filtered):
    curr = filtered[i]
    if not re.search(r'\.{2,}\s*\d+$', curr) and i + 1 < len(filtered):
        curr = curr + ' ' + filtered[i+1]
        i += 1
    combined.append(curr)
    i += 1

toc_items = []
toc_by_pdf_page = {}

for c in combined:
    m = re.search(r'^(.*?)\s*\.{2,}\s*(\d+)$', c)
    if m:
        raw_title = m.group(1).replace('•', '').strip()
        clean_title = re.sub(r'\s+', ' ', raw_title)
        printed_page = int(m.group(2))
        pdf_page = printed_page + 1  # PDF page formula
        item = {
            'title': clean_title,
            'printed_page': printed_page,
            'pdf_page': pdf_page
        }
        toc_items.append(item)
        if pdf_page not in toc_by_pdf_page:
            toc_by_pdf_page[pdf_page] = []
        toc_by_pdf_page[pdf_page].append(clean_title)

print(f"Loaded {len(toc_items)} TOC topics.")

# Special page metadata
PAGE_METADATA = {
    1: {'title': "Kapak Görseli", 'type': 'cover'},
    2: {'title': "Boş Sayfa", 'type': 'blank'},
    3: {'title': "Künye & Yayın Bilgileri", 'type': 'frontmatter'},
    4: {'title': "İç Başlık", 'type': 'frontmatter'},
    5: {'title': "Bölüm Ayırıcı", 'type': 'divider'},
    6: {'title': "İçindekiler (1. Kısım)", 'type': 'toc'},
    7: {'title': "İçindekiler (2. Kısım)", 'type': 'toc'},
    8: {'title': "İçindekiler (3. Kısım)", 'type': 'toc'},
    9: {'title': "İçindekiler (4. Kısım)", 'type': 'toc'},
    10: {'title': "Abdülkâdir Geylânî'nin Hayatı ve Şahsiyeti", 'type': 'chapter'},
    11: {'title': "Abdülkâdir Geylânî (Talebesi ve İlim Hayatı)", 'type': 'content'},
    12: {'title': "Abdülkâdir Geylânî (Menkıbeleri ve Eserleri)", 'type': 'content'},
    13: {'title': "Abdülkâdir Geylânî'nin Eserleri", 'type': 'content'},
    55: {'title': "Bölüm Ayırıcı", 'type': 'divider'},
    95: {'title': "Bölüm Ayırıcı", 'type': 'divider'},
    109: {'title': "Bölüm Ayırıcı", 'type': 'divider'},
    121: {'title': "Medine Yayıncılık — Abdülkâdir Geylânî Külliyatı", 'type': 'backmatter'},
}

def clean_and_format_page(pdf_text, page_num):
    # Check pre-defined pages
    if page_num == 1:
        html = """<div class="cover-container">
  <div class="cover-card">
    <img src="cover.jpg" alt="Mehâfetullâh Kapak" class="book-cover-img" onerror="this.style.display='none'">
    <div class="cover-text-group">
      <div class="kulliyat-badge">ABDÜLKÂDİR GEYLÂNÎ KÜLLİYATI: 10</div>
      <h1 class="book-main-title">MEHÂFETULLÂH</h1>
      <h2 class="book-sub-title">ALLAH KORKUSU</h2>
      <p class="book-author">Gavs-ı A'zam eş-Şeyh Abdülkâdir Geylânî (k.s.)</p>
      <div class="cover-divider">✦ ✦ ✦</div>
      <p class="book-publisher">Medine Yayıncılık — Ravza Yayınları</p>
    </div>
  </div>
</div>"""
        return "Kapak Görseli", html, "Mehâfetullâh Allah Korkusu Abdülkâdir Geylânî Medine Yayıncılık"

    if page_num == 2:
        return "Boş Sayfa", '<div class="empty-leaf"><span class="leaf-ornament">❧</span><p>Orijinal eserde boş bırakılmış yaprak</p></div>', ""

    if page_num in (5, 55, 95, 109):
        return PAGE_METADATA[page_num]['title'], f'<div class="section-divider-leaf"><span class="leaf-ornament">✦ ✦ ✦</span><p>Bölüm Ayırıcı Yaprak — Sayfa {page_num}</p></div>', ""

    if page_num == 3:
        # Künye
        kunye_lines = [l.strip() for l in pdf_text.splitlines() if l.strip()]
        html_lines = ["<div class='kunye-card'>", "<h2 class='kunye-title'>YAYIN BİLGİLERİ & KÜNYE</h2>", "<div class='kunye-grid'>"]
        for kl in kunye_lines:
            if ':' in kl:
                k, v = kl.split(':', 1)
                html_lines.append(f"<div class='kunye-row'><span class='k-label'>{k.strip()}:</span> <span class='k-value'>{v.strip()}</span></div>")
            else:
                html_lines.append(f"<p class='kunye-p'>{kl}</p>")
        html_lines.append("</div></div>")
        return "Künye & Yayın Bilgileri", "\n".join(html_lines), pdf_text

    if page_num == 4:
        # Inner title
        html = """<div class="inner-title-page">
  <div class="inner-ornament">﷽</div>
  <p class="author-prefix">eş-Şeyh</p>
  <h1 class="inner-book-title">ABDÜLKÂDİR GEYLÂNÎ</h1>
  <p class="inner-honorific">(küddise sirruhu)</p>
  <div class="title-rule"></div>
  <h2 class="inner-work-title">MEHÂFETULLÂH</h2>
  <h3 class="inner-sub">Allah (cc) Korkusu</h3>
  <div class="inner-city">İstanbul 2012</div>
</div>"""
        return "İç Başlık", html, pdf_text

    if 6 <= page_num <= 9:
        # İçindekiler
        raw_lines = [l.strip() for l in pdf_text.splitlines() if l.strip()]
        html_lines = ["<div class='toc-view-card'>", f"<h2 class='toc-view-heading'>İÇİNDEKİLER <span class='toc-part'>— Bölüm {page_num-5} / 4</span></h2>", "<ul class='toc-view-list'>"]
        for l in raw_lines:
            if 'Mehafetullah' in l or 'Abdülkadir' in l or l == 'İçindekiler':
                continue
            m = re.search(r'^(.*?)\s*\.{2,}\s*(\d+)$', l)
            if m:
                t = m.group(1).replace('•', '').strip()
                p = int(m.group(2))
                pdf_p = p + 1
                html_lines.append(f"<li class='toc-view-item'><a href='#p{pdf_p}' class='toc-link-item' onclick='goToPage({pdf_p}); return false;'><span class='toc-t'>{t}</span><span class='toc-dots'></span><span class='toc-p'>{p}</span></a></li>")
            else:
                html_lines.append(f"<li class='toc-view-text'>{l}</li>")
        html_lines.append("</ul></div>")
        return f"İçindekiler (Sayfa {page_num})", "\n".join(html_lines), pdf_text

    if page_num == 121:
        # Katalog
        cat_lines = [l.strip() for l in pdf_text.splitlines() if l.strip()]
        html_lines = ["<div class='catalog-card'>", "<h2 class='catalog-heading'>MEDİNE YAYINCILIK'TAN ÇIKAN<br><span class='cat-sub'>GEYLÂNÎ KÜLLİYATI</span></h2>", "<ol class='catalog-list'>"]
        for cl in cat_lines:
            cleaned_cl = re.sub(r'^\d+\-?\s*', '', cl)
            if re.match(r'^\d+\-?\s*', cl):
                html_lines.append(f"<li class='catalog-item'>{cleaned_cl}</li>")
            elif 'Geylânî Külliyatı' in cl:
                html_lines.append(f"</ol><p class='catalog-footer'>{cl}</p>")
        return "Abdülkâdir Geylânî Külliyatı Kataloğu", "\n".join(html_lines), pdf_text

    # Standard body pages (10 to 120)
    raw_lines = [l.strip() for l in pdf_text.splitlines() if l.strip()]
    clean_lines = []
    for idx, line in enumerate(raw_lines):
        # Remove running headers
        if idx < 2 and re.search(r'^(?:\d+\s*)?(?:Mehafetullah\s*-\s*Allah\s*Korkusu|Abdülkadir\s*Geylani)(?:\s*\d+)?$', line, re.IGNORECASE):
            continue
        clean_lines.append(line)

    # Hyphen rejoining
    joined = []
    i = 0
    while i < len(clean_lines):
        line = clean_lines[i]
        if line.endswith('-') and i + 1 < len(clean_lines):
            next_l = clean_lines[i+1]
            if next_l and next_l[0].islower():
                joined.append(line[:-1] + next_l)
                i += 2
                continue
        joined.append(line)
        i += 1

    # Check for known TOC topics on this page
    topics_here = toc_by_pdf_page.get(page_num, [])

    # Process paragraphs, headings, and footnotes
    paragraphs = []
    current_p = []
    primary_title = None

    for line in joined:
        line_clean = line.strip()
        if not line_clean:
            if current_p:
                paragraphs.append(" ".join(current_p))
                current_p = []
            continue

        # Check if line matches a topic title
        is_topic_heading = False
        for top in topics_here:
            # Fuzzy match or exact match
            if top.lower() in line_clean.lower() or line_clean.lower() in top.lower():
                if len(line_clean) < len(top) + 20:
                    is_topic_heading = True
                    if not primary_title:
                        primary_title = top
                    if current_p:
                        paragraphs.append(" ".join(current_p))
                        current_p = []
                    paragraphs.append(f"<heading>{top}</heading>")
                    break

        if is_topic_heading:
            continue

        # Check if line is a footnote (e.g., "1 Fâtır, 10" or "3 Sehavi, ...")
        if re.match(r'^\d+\s+[A-ZÇĞİÖŞÜ][a-zçğıöşü\s\’\']+(?:\s*,\s*[\d\/\-]+)?', line_clean):
            if current_p:
                paragraphs.append(" ".join(current_p))
                current_p = []
            paragraphs.append(f"<footnote>{line_clean}</footnote>")
            continue

        # Spiritual khutba calls (Ey cemaat!, Ey evlat!, Ey oğul!)
        if re.match(r'^(?:Ey\s+cemaat|Ey\s+evlat|Ey\s+oğul|Ey\s+kardeş)[!:\.\,]', line_clean, re.IGNORECASE):
            if current_p:
                paragraphs.append(" ".join(current_p))
                current_p = []
            paragraphs.append(f"<khutba>{line_clean}</khutba>")
            continue

        # Bullet list item
        if line_clean.startswith('•') or re.match(r'^\d+\-\s+', line_clean):
            if current_p:
                paragraphs.append(" ".join(current_p))
                current_p = []
            paragraphs.append(f"<bullet>{line_clean}</bullet>")
            continue

        # Paragraph flow
        if current_p:
            prev = current_p[-1]
            if len(prev) < 45 and re.search(r'[\.\?\!\:\”\"]\s*$', prev):
                paragraphs.append(" ".join(current_p))
                current_p = [line_clean]
            else:
                current_p.append(line_clean)
        else:
            current_p.append(line_clean)

    if current_p:
        paragraphs.append(" ".join(current_p))

    # Build semantic HTML
    html_output = []
    for p in paragraphs:
        if p.startswith("<heading>"):
            h_text = p.replace("<heading>", "").replace("</heading>", "")
            html_output.append(f"""<div class="topic-header-block">
  <div class="topic-ornament">❦</div>
  <h2 class="topic-title">{h_text}</h2>
  <div class="topic-line"></div>
</div>""")
        elif p.startswith("<footnote>"):
            fn_text = p.replace("<footnote>", "").replace("</footnote>", "")
            html_output.append(f"""<div class="footnote-box"><span class="fn-badge">Dipnot</span> {fn_text}</div>""")
        elif p.startswith("<khutba>"):
            kh_text = p.replace("<khutba>", "").replace("</khutba>", "")
            html_output.append(f"""<div class="khutba-callout"><span class="callout-icon">📿</span> <strong>{kh_text}</strong></div>""")
        elif p.startswith("<bullet>"):
            b_text = p.replace("<bullet>", "").replace("</bullet>", "").lstrip("•- ").strip()
            html_output.append(f"""<li class="book-bullet-point">{b_text}</li>""")
        else:
            # First paragraph styling on chapter starts
            html_output.append(f"""<p class="book-paragraph">{p}</p>""")

    if not primary_title:
        if topics_here:
            primary_title = topics_here[0]
        elif page_num in PAGE_METADATA:
            primary_title = PAGE_METADATA[page_num]['title']
        else:
            primary_title = f"Mehâfetullâh — Sayfa {page_num}"

    raw_clean_text = "\n".join(clean_lines)
    return primary_title, "\n".join(html_output), raw_clean_text

# 2. Extract and Process All 121 Pages
reader = pypdf.PdfReader('Mehafetullah Allah korkusu Abdulkadir Geylani.pdf')
total_pages = len(reader.pages)
print(f"Processing all {total_pages} pages from PDF...")

os.makedirs('MehafetullahApp/www', exist_ok=True)
os.makedirs('MehafetullahApp/extracted_pages', exist_ok=True)

book_pages = []
for p_idx in range(total_pages):
    page_num = p_idx + 1
    pdf_text = reader.pages[p_idx].extract_text() or ''
    title, content_html, raw_text = clean_and_format_page(pdf_text, page_num)
    
    # Save individual page text file
    txt_path = f"MehafetullahApp/extracted_pages/page_{page_num:04d}.txt"
    with open(txt_path, 'w', encoding='utf-8') as pf:
        pf.write(f"MEHÂFETULLÂH (ALLAH KORKUSU) — Sayfa {page_num} / {total_pages}\n")
        pf.write(f"Başlık: {title}\n")
        pf.write("="*60 + "\n\n")
        pf.write(raw_text if raw_text else "(Boş veya Özel Sayfa)")

    words = len(raw_text.split()) if raw_text else 0
    chars = len(raw_text) if raw_text else 0

    page_entry = {
        'page': page_num,
        'printed_page': max(1, page_num - 1) if page_num > 1 else 1,
        'title': title,
        'content_html': content_html,
        'raw_text': raw_text,
        'word_count': words,
        'char_count': chars,
        'has_topics': page_num in toc_by_pdf_page
    }
    book_pages.append(page_entry)

book_db = {
    'meta': {
        'title': "Mehâfetullâh (Allah Korkusu)",
        'author': "Gavs-ı A'zam eş-Şeyh Abdülkâdir Geylânî (k.s.)",
        'publisher': "Medine Yayıncılık",
        'series': "Abdülkâdir Geylânî Külliyatı: 10",
        'translators': "Kâzım Ağcakaya & Mustafa Kasadar",
        'city_year': "İstanbul, 2012",
        'isbn': "978-605-4411-74-0",
        'total_pages': total_pages,
        'total_topics': len(toc_items),
        'total_words': sum(p['word_count'] for p in book_pages),
        'total_chars': sum(p['char_count'] for p in book_pages)
    },
    'toc': toc_items,
    'pages': book_pages
}

# Save JSON database
json_path = 'MehafetullahApp/www/book_database.json'
with open(json_path, 'w', encoding='utf-8') as jf:
    json.dump(book_db, jf, ensure_ascii=False, indent=2)

# Save JS database (for easy direct inclusion without CORS issues)
js_path = 'MehafetullahApp/www/book_database.js'
with open(js_path, 'w', encoding='utf-8') as jsf:
    jsf.write("window.BOOK_DATABASE = ")
    json.dump(book_db, jsf, ensure_ascii=False)
    jsf.write(";\n")

# Copy cover to www
import shutil
if os.path.exists('Mehafetullah_cover.jpg'):
    shutil.copy('Mehafetullah_cover.jpg', 'MehafetullahApp/www/cover.jpg')

print("="*60)
print(f"DATABASE CREATED SUCCESSFULLY!")
print(f"Book: {book_db['meta']['title']}")
print(f"Author: {book_db['meta']['author']}")
print(f"Pages: {book_db['meta']['total_pages']}")
print(f"TOC Topics: {book_db['meta']['total_topics']}")
print(f"Total Words: {book_db['meta']['total_words']:,}")
print(f"Total Characters: {book_db['meta']['total_chars']:,}")
print(f"Saved: {json_path} ({os.path.getsize(json_path):,} bytes)")
print(f"Saved: {js_path} ({os.path.getsize(js_path):,} bytes)")
print("="*60)
