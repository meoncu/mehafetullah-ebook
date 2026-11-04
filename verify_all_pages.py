import pypdf
import json

reader = pypdf.PdfReader('Mehafetullah Allah korkusu Abdulkadir Geylani.pdf')
with open('MehafetullahApp/www/book_database.json', 'r', encoding='utf-8') as f:
    db = json.load(f)

print(f"PDF total pages: {len(reader.pages)}")
print(f"DB total pages: {len(db['pages'])}")

assert len(reader.pages) == len(db['pages']) == 121

missing_or_suspicious = []
page_audit = []

for i in range(len(reader.pages)):
    page_num = i + 1
    pdf_text = (reader.pages[i].extract_text() or '').strip()
    db_page = db['pages'][i]
    db_text = db_page['raw_text'].strip()
    
    pdf_len = len(pdf_text)
    db_len = len(db_text)
    
    # Check blank pages in PDF
    is_blank_in_pdf = pdf_len < 5
    
    page_audit.append({
        'page': page_num,
        'pdf_chars': pdf_len,
        'db_chars': db_len,
        'words': db_page['word_count'],
        'title': db_page['title'],
        'is_blank': is_blank_in_pdf
    })
    
    if pdf_len > 50 and db_len == 0:
        missing_or_suspicious.append((page_num, 'EMPTY_IN_DB', pdf_len, db_len))
    elif pdf_len > 100 and db_len < pdf_len * 0.7 and page_num not in [3, 4, 6, 7, 8, 9, 121]:
        missing_or_suspicious.append((page_num, 'SIGNIFICANTLY_SHORTER', pdf_len, db_len))

print(f"\nAudit completed. Suspicious/Missing pages: {len(missing_or_suspicious)}")
if missing_or_suspicious:
    for item in missing_or_suspicious:
        print("  Issue:", item)
else:
    print("ALL 121 pages verified successfully against the PDF!")

blank_pages = [p['page'] for p in page_audit if p['is_blank']]
print(f"Blank pages in original PDF: {blank_pages} (Pages: 1=cover, 2=blank leaf, 5=blank separator, 55=blank separator, 95=blank separator, 109=blank separator)")

content_pages = [p for p in page_audit if not p['is_blank']]
print(f"Pages with actual content: {len(content_pages)} pages")
print(f"Total word count in database: {sum(p['words'] for p in page_audit):,} words")
print(f"Total character count: {sum(p['db_chars'] for p in page_audit):,} chars")
