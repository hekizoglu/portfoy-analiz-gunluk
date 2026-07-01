from __future__ import annotations

import argparse
from html import unescape
from pathlib import Path
import re
from urllib.parse import urljoin
from urllib.request import urlopen


REPORTS_URL = "https://www.oyakyatirim.com.tr/arastirma-raporlari"
LINK_RE = re.compile(r'/Reports/DownloadFile\?fileUrl=([^"\']*degerleme-tablosu[^"\']*\.pdf)', re.IGNORECASE)


def fetch_latest_pdf(output_path: Path) -> tuple[str, Path]:
    html = urlopen(REPORTS_URL, timeout=30).read().decode("utf-8", errors="replace")
    matches = LINK_RE.findall(html)
    if not matches:
        raise RuntimeError("Could not find latest OYAK valuation PDF link on research page.")

    file_url = unescape(matches[-1]).replace("\r", "").replace("\n", "")
    pdf_url = urljoin(REPORTS_URL, f"/Reports/DownloadFile?fileUrl={file_url}")
    binary = urlopen(pdf_url, timeout=60).read()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(binary)
    return pdf_url, output_path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="artifacts/raw/oyak_latest.pdf")
    args = parser.parse_args()
    pdf_url, output = fetch_latest_pdf(Path(args.output))
    print(f"PDF_URL={pdf_url}")
    print(f"OUTPUT={output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
