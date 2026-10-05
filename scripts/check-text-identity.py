#!/usr/bin/env python3
"""Prove the visible document text of every page is unchanged.

For each HTML page, extracts (stdlib html.parser, tags stripped):
  - <title> and meta description
  - <main> visible text, excluding the table-of-contents <nav class="toc"> subtree
    and any element marked data-added (new, non-legal presentation chrome)
  - TOC text (separately, since the TOC may move in the DOM)
  - every id inside <main> and every href inside <main> (excluding data-added)
Then compares before vs after and prints a unified diff on mismatch.
Usage: textcheck.py BEFORE_DIR AFTER_DIR
"""
import difflib
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}
BLOCK = {"p", "li", "h1", "h2", "h3", "h4", "h5", "h6", "div", "section", "article", "aside", "nav",
         "ul", "ol", "summary", "details", "header", "footer", "main", "dt", "dd", "dl", "td", "th", "tr", "br"}


class Extract(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []  # (tag, flags)
        self.title = ""
        self.desc = ""
        self.main_text = []
        self.toc_text = []
        self.ids = []
        self.hrefs = []
        self.toc_hrefs = []

    def _flags(self):
        f = {"main": False, "toc": False, "added": False, "title": False, "script": False}
        for _, fl in self.stack:
            for k, v in fl.items():
                f[k] = f[k] or v
        return f

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        cls = (a.get("class") or "").split()
        fl = {
            "main": tag == "main",
            "toc": tag == "nav" and "toc" in cls,
            "added": "data-added" in a,
            "title": tag == "title",
            "script": tag in ("script", "style"),
        }
        if tag == "meta" and a.get("name") == "description":
            self.desc = " ".join((a.get("content") or "").split())
        cur = self._flags()
        merged = {k: cur[k] or fl[k] for k in fl}
        if merged["main"] and not merged["added"]:
            if "id" in a and tag != "main":
                self.ids.append(a["id"])
            if tag == "a" and "href" in a:
                (self.toc_hrefs if merged["toc"] else self.hrefs).append(a["href"])
        if tag in BLOCK:
            self._sep(merged)
        if tag not in VOID:
            self.stack.append((tag, fl))

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID:
            self.stack.pop()

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                fl = self._flags()
                del self.stack[i:]
                if tag in BLOCK:
                    self._sep(fl)
                return

    def _sep(self, f):
        if f["main"] and not f["added"]:
            (self.toc_text if f["toc"] else self.main_text).append("\n")

    def handle_data(self, data):
        f = self._flags()
        if f["script"]:
            return
        if f["title"]:
            self.title += data
        if f["main"] and not f["added"]:
            (self.toc_text if f["toc"] else self.main_text).append(data)


def norm(chunks):
    text = "".join(chunks)
    lines = [" ".join(l.split()) for l in text.split("\n")]
    return [l for l in lines if l]


def extract(path):
    p = Extract()
    p.feed(path.read_text(encoding="utf-8"))
    return {
        "title": [" ".join(p.title.split())],
        "description": [p.desc],
        "main": norm(p.main_text),
        "toc": norm(p.toc_text),
        "ids": p.ids,
        "hrefs": p.hrefs,
        "toc_hrefs": p.toc_hrefs,
    }


def main():
    before, after = Path(sys.argv[1]), Path(sys.argv[2])
    pages = sorted(str(p.relative_to(before)) for p in before.rglob("*.html") if ".git" not in p.parts)
    ok = True
    total_lines = 0
    for rel in pages:
        b, a = extract(before / rel), extract(after / rel)
        page_ok = True
        for key in b:
            if b[key] != a[key]:
                page_ok = ok = False
                print(f"--- MISMATCH {rel} [{key}]")
                for line in difflib.unified_diff(b[key], a[key], "before", "after", lineterm="", n=1):
                    print("   ", line)
        total_lines += len(b["main"]) + len(b["toc"])
        print(f"{'OK  ' if page_ok else 'FAIL'} {rel}: main {len(b['main'])} lines, toc {len(b['toc'])} lines, "
              f"{len(b['ids'])} ids, {len(b['hrefs'])}+{len(b['toc_hrefs'])} hrefs")
    print(f"\n{len(pages)} pages, {total_lines} text lines compared -> {'IDENTICAL' if ok else 'DIFFERENT'}")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
