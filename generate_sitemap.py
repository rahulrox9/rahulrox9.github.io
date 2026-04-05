from pathlib import Path
from xml.etree.ElementTree import Element, SubElement, ElementTree

BASE_URL = "https://rahulrox9.github.io"
ROOT = Path(".")

EXCLUDE_DIRS = {
    ".git",
    ".github",
    "__pycache__",
    "node_modules",
    "Admin"
}

EXCLUDE_FILES = {
    "404.html",
    "google44fb8477eecedcfd.html",
    "sitemap.xml"
}

INCLUDE_SUFFIXES = {".html"}

def should_include(path: Path) -> bool:
    if path.name in EXCLUDE_FILES:
        return False
    if path.suffix.lower() not in INCLUDE_SUFFIXES:
        return False
    if any(part in EXCLUDE_DIRS for part in path.parts):
        return False
    return True

def to_url(path: Path) -> str:
    rel = path.as_posix()
    if rel == "index.html":
        return f"{BASE_URL}/"
    return f"{BASE_URL}/{rel}"

def main():
    html_files = sorted(
        p for p in ROOT.rglob("*")
        if p.is_file() and should_include(p)
    )

    urlset = Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")

    for path in html_files:
        url = SubElement(urlset, "url")
        loc = SubElement(url, "loc")
        loc.text = to_url(path)

    tree = ElementTree(urlset)
    tree.write("sitemap.xml", encoding="utf-8", xml_declaration=True)

if __name__ == "__main__":
    main()
