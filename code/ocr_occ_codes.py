#!/usr/bin/env python3
"""
Simplest one-file builder:
- Tries to extract text with pdfplumber (no OCR needed if PDF has text).
- Falls back to OCR (pytesseract + pdf2image) if needed.
- Parses occupation codes (e.g., "ACCOUNTANT   ACCT.") into a tidy CSV.

Usage:
  python build_occupation_mapping.py

Adjust the CONFIG section below for paths/pages.
"""

# --- CONFIG ---------------------------------------------------------
PDF_PATH = "/Users/jackturek/Documents/Repos/Irish-Famine-Immigration/data/Scanned_Tech_Doc.pdf"   # input PDF
FIRST_PAGE = 3                               # first page with codes (1-indexed)
LAST_PAGE = None                             # set to an int to stop earlier
OUT_CSV = "/Users/jackturek/Documents/Repos/Irish-Famine-Immigration/data/occupation_mapping.csv"   # output mapping CSV

NCOLS              = 4     # number of vertical columns on each page
COLUMN_GUTTER_PTS  = 4     # trim a few points inside each column to avoid bleed
LINE_Y_TOL         = 3.5   # vertical tolerance (points) when grouping words into lines
# -------------------------------------------------------------------

import re
import sys
import pandas as pd

def clean_code(code: str) -> str:
    # Uppercase, strip, drop trailing punctuation like '.' or ','
    return re.sub(r"[^\w]+$", "", code.strip().upper())

def clean_desc(desc: str) -> str:
    # Normalize whitespace; keep readable casing
    return re.sub(r"\s+", " ", desc.strip()).title()

PAIR_AT_END = re.compile(r"(.+?)\s+([A-Z]{2,8}\.?)$")  # "... DESC ...   CODE"

def words_by_column(words, page_width, ncols, gutter=0):
    """Assign words to vertical columns by x0."""
    col_w = page_width / ncols
    bounds = []
    for i in range(ncols):
        x0 = i * col_w + gutter
        x1 = (i + 1) * col_w - gutter
        bounds.append((x0, x1))

    cols = [[] for _ in range(ncols)]
    for w in words:
        x0 = float(w["x0"])
        for i, (b0, b1) in enumerate(bounds):
            if b0 <= x0 < b1:
                cols[i].append(w)
                break
    for c in cols:
        c.sort(key=lambda d: (float(d["top"]), float(d["x0"])))
    return cols

def lines_from_words(col_words, y_tol=3.5):
    """Group words into lines by 'top' proximity; join words with a space."""
    lines = []
    cur_line = []
    cur_top = None
    for w in col_words:
        top = float(w["top"])
        if cur_top is None or abs(top - cur_top) > y_tol:
            if cur_line:
                lines.append(" ".join(x["text"] for x in cur_line))
            cur_line = [w]
            cur_top = top
        else:
            cur_line.append(w)
    if cur_line:
        lines.append(" ".join(x["text"] for x in cur_line))
    return lines

def parse_streaming(lines):
    """
    Stream lines; allow wrapped descriptions that end with a CODE on a later line.
    If a line doesn't contain a trailing CODE, hold it in 'carry' and append the next line.
    """
    mapping = {}
    carry = ""
    for ln in lines:
        text = ln.strip()
        if not text:
            continue
        candidate = (carry + " " + text).strip() if carry else text
        m = PAIR_AT_END.search(candidate)
        if m:
            desc, code = m.groups()
            code = clean_code(code)
            desc = clean_desc(desc)
            # Keep first seen or prefer the longer description
            if code not in mapping or len(desc) > len(mapping[code]):
                mapping[code] = desc
            carry = ""
        else:
            # Handle hyphenated wrap (join without extra space)
            if candidate.endswith("-"):
                carry = candidate[:-1]
            else:
                carry = candidate
    return mapping

def main():
    try:
        import pdfplumber
    except ImportError:
        sys.exit("Please install dependencies:\n  pip install pdfplumber pandas")

    all_map = {}
    with pdfplumber.open(PDF_PATH) as pdf:
        start = max(0, FIRST_PAGE - 1)
        end = len(pdf.pages) if LAST_PAGE is None else min(LAST_PAGE, len(pdf.pages))

        # Quick check: is there any selectable text?
        sample_words = pdf.pages[start].extract_words() if start < end else []
        if not sample_words:
            sys.exit("No text layer detected on the target pages. "
                     "This PDF appears to be image-only; OCR would be required.")

        for i in range(start, end):
            page = pdf.pages[i]
            words = page.extract_words()
            if not words:
                continue

            cols = words_by_column(words, page_width=page.width,
                                   ncols=NCOLS, gutter=COLUMN_GUTTER_PTS)
            for col_words in cols:
                lines = lines_from_words(col_words, y_tol=LINE_Y_TOL)
                m = parse_streaming(lines)
                for k, v in m.items():
                    # keep first seen; or choose longer desc if duplicate
                    if k not in all_map or len(v) > len(all_map[k]):
                        all_map[k] = v

    if not all_map:
        sys.exit("Parsed no occupation pairs. Try adjusting LINE_Y_TOL/COLUMN_GUTTER_PTS/NCOLS or page range.")

    df = pd.DataFrame(sorted(all_map.items()), columns=["occupation_code", "occupation_desc"])
    df["occupation_code_norm"] = df["occupation_code"].str.replace(".", "", regex=False)
    df.to_csv(OUT_CSV, index=False)
    print(f"✅ Wrote {len(df)} occupation codes to {OUT_CSV}")

if __name__ == "__main__":
    main()