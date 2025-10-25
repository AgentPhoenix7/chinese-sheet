#!/usr/bin/env python3
"""
Combine Chinese character worksheets into one A4 PDF.
Adds a styled cover (black sidebar, title, centered image) before the worksheets.
"""

import os
import io
from PyPDF2 import PdfReader, PdfWriter, PageObject
from PyPDF2.generic import NameObject, ArrayObject
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.pdfbase.ttfonts import TTFont

# --- Configuration ---
INPUT_DIR = "./worksheets"
OUTPUT_FILE = "Chinese_Workbook_A4.pdf"
COVER_IMAGE = "cover.png"   # center artwork
A4_WIDTH, A4_HEIGHT = A4
# ----------------------

# Register built-in Simplified Chinese font so the Chinese glyph renders
pdfmetrics.registerFont(UnicodeCIDFont("STSong-Light"))

# Register HanyiSentyPagoda Regular for the single Chinese glyph (fallback to STSong-Light)
def _choose_hanyi_font():
    candidates = [
        os.path.join(os.path.dirname(__file__), "fonts", "HanyiSentyPagoda.ttf"),
        r"C:\Windows\Fonts\HanyiSentyPagoda.ttf",
        r"C:\Windows\Fonts\HanyiSentyPagoda_Regular.ttf",
    ]
    for path in candidates:
        if os.path.exists(path):
            pdfmetrics.registerFont(TTFont("HanyiSenty", path))
            return "HanyiSenty"
    # fallback to built-in if Hanyi not available
    return "STSong-Light"

HANYI_FONT = _choose_hanyi_font()

def make_final_cover():
    """Styled cover with black sidebar, title, and centered cover.png."""
    packet = io.BytesIO()
    c = canvas.Canvas(packet, pagesize=A4)

    # Background (soft cream)
    c.setFillColorRGB(0.99, 0.98, 0.94)
    c.rect(0, 0, A4_WIDTH, A4_HEIGHT, fill=1, stroke=0)

    # Left black sidebar
    sidebar_w = 55
    c.setFillColor(colors.black)
    c.rect(0, 0, sidebar_w, A4_HEIGHT, fill=1, stroke=0)

    # --- Center the cover.png image (exactly centered on the page) ---
    img = ImageReader(COVER_IMAGE)
    src_w, src_h = img.getSize()

    # Fit image into page with small page margins, then center it exactly.
    page_margin = 70
    max_w = A4_WIDTH - 2 * page_margin
    max_h = A4_HEIGHT - 2 * page_margin
    scale = min(max_w / src_w, max_h / src_h, 1.0)
    draw_w = src_w * scale
    draw_h = src_h * scale

    x = (A4_WIDTH - draw_w) / 2
    y = (A4_HEIGHT - draw_h) / 2

    # nudge the centered artwork downward so it doesn't overlap the title block
    # downward_shift is in points; increase/decrease to taste
    downward_shift = 100
    min_bottom = 20  # keep at least this many points above the page bottom
    y = max(min_bottom, y - downward_shift)

    c.drawImage(img, x, y, width=draw_w, height=draw_h, mask='auto')
    # -------------------------------------------------------------

    # Draw a cream-filled title background so the centered artwork won't show through.
    # This keeps the image visually centered while the top-left title block stays clean.
    title_bg_w = 300
    title_bg_h = 200
    title_bg_x = sidebar_w            # start right after the black sidebar
    title_bg_y = A4_HEIGHT - 270      # covers the title/underline area
    c.setFillColorRGB(0.99, 0.98, 0.94)
    c.rect(title_bg_x, title_bg_y, title_bg_w, title_bg_h, fill=1, stroke=0)

    # Title block (top-left) - draw AFTER image so it stays visible
    c.setFillColor(colors.black)

    # Use Helvetica-Bold for all Latin text so it stays bold/consistent
    c.setFont("Helvetica-Bold", 44)
    title_x = sidebar_w + 35
    c.drawString(title_x, A4_HEIGHT - 130, "MY")

    # Draw HSK1 then measure its width so we can place the Chinese glyph snugly after it
    c.setFont("Helvetica-Bold", 44)
    hsk_y = A4_HEIGHT - 190
    c.drawString(title_x, hsk_y, "HSK1")
    hsk_width = c.stringWidth("HSK1", "Helvetica-Bold", 44)

    # Use the registered Hanyi font only for the Chinese character and place it close to HSK1
    c.setFont(HANYI_FONT, 44)
    chinese_padding = 8  # small gap in points between Latin text and Chinese glyph
    c.drawString(title_x + hsk_width + chinese_padding, hsk_y, "壹")

    # Subheading in Helvetica-Bold
    c.setFont("Helvetica-Bold", 36)
    c.drawString(title_x, A4_HEIGHT - 245, "NOTEBOOK")

    # Underline
    c.setLineWidth(3)
    c.line(title_x, A4_HEIGHT - 255, title_x + 235, A4_HEIGHT - 255)

    c.save()
    packet.seek(0)

    # Ensure the returned page has an explicit A4 MediaBox by merging onto a blank A4 page.
    reader = PdfReader(packet)
    src_page = reader.pages[0]
    cover_page = PageObject.create_blank_page(width=A4_WIDTH, height=A4_HEIGHT)
    cover_page.merge_page(src_page)
    return cover_page

def make_page_number_overlay(page_num: int):
    """Centered page number at top."""
    packet = io.BytesIO()
    c = canvas.Canvas(packet, pagesize=A4)
    c.setFont("Helvetica-Bold", 12)
    text = str(page_num)
    text_width = c.stringWidth(text, "Helvetica-Bold", 12)
    c.drawString((A4_WIDTH - text_width) / 2, A4_HEIGHT - 25, text)
    c.save()
    packet.seek(0)
    return PdfReader(packet).pages[0]

def clean_page(page):
    """Remove hyperlinks and images (kept as in your 'correct' version)."""
    if "/Annots" in page:
        page[NameObject("/Annots")] = ArrayObject()
    if "/Resources" in page and "/XObject" in page["/Resources"]:
        for key in list(page["/Resources"]["/XObject"].keys()):
            del page["/Resources"]["/XObject"][key]
    return page

def resize_to_a4(input_pdf):
    """Scale and center a single-page PDF to A4."""
    reader = PdfReader(input_pdf)
    page = reader.pages[0]
    page = clean_page(page)
    w, h = float(page.mediabox.width), float(page.mediabox.height)
    scale = min(A4_WIDTH / w, A4_HEIGHT / h)
    tx, ty = (A4_WIDTH - w * scale) / 2, (A4_HEIGHT - h * scale) / 2
    new_page = PageObject.create_blank_page(width=A4_WIDTH, height=A4_HEIGHT)
    page.add_transformation((scale, 0, 0, scale, tx, ty))
    new_page.merge_page(page)
    return new_page

def combine_pdfs():
    """Add cover, clean, resize, number, and combine all worksheets."""
    writer = PdfWriter()
    files = sorted(
        [f for f in os.listdir(INPUT_DIR) if f.lower().endswith(".pdf")],
        key=lambda x: int(os.path.splitext(x)[0])
    )

    if not files:
        print("⚠️ No PDFs found in", INPUT_DIR)
        return

    print(f"Found {len(files)} files. Creating workbook with centered cover...\n")

    # Cover page
    cover = make_final_cover()
    writer.add_page(cover)

    # Worksheets
    for i, filename in enumerate(files, start=1):
        path = os.path.join(INPUT_DIR, filename)
        print(f"  {i}. {filename}")
        page = resize_to_a4(path)
        overlay = make_page_number_overlay(i)
        page.merge_page(overlay)
        writer.add_page(page)

    with open(OUTPUT_FILE, "wb") as f:
        writer.write(f)

    print(f"\n✅ Saved: {OUTPUT_FILE} ({len(files) + 1} pages)")

if __name__ == "__main__":
    combine_pdfs()
