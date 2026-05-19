#!/usr/bin/env python3
"""Regenerate repo-sana.svg from live GitHub data.

NVlabs has org-level PAT restrictions that cause both the official
github-readme-stats service and community forks to fail for NVlabs/Sana,
so this card is rendered locally and refreshed on a schedule.
"""
from __future__ import annotations

import json
import os
import sys
import urllib.request
from pathlib import Path

OWNER = "NVlabs"
REPO = "Sana"
LANG = "Python"
LANG_COLOR = "#3572A5"
OUT_PATH = Path(__file__).resolve().parent.parent / "repo-sana.svg"


def fetch_repo() -> dict:
    req = urllib.request.Request(
        f"https://api.github.com/repos/{OWNER}/{REPO}",
        headers={
            "User-Agent": "haoyizhu-readme-card-updater",
            "Accept": "application/vnd.github+json",
        },
    )
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp)


def k_formatter(n: int) -> str:
    """Match readme-stats' kFormatter: 6589 -> '6.6k', 469 -> '469'."""
    if abs(n) > 999:
        return f"{n / 1000:.1f}k"
    return str(n)


def wrap_description(desc: str, max_chars: int = 55) -> tuple[str, str]:
    line1, line2 = "", ""
    for word in desc.split():
        candidate = (line1 + " " + word).strip() if line1 else word
        if len(candidate) <= max_chars and not line2:
            line1 = candidate
        else:
            line2 = (line2 + " " + word).strip() if line2 else word
    if len(line2) > max_chars:
        line2 = line2[: max_chars - 1] + "…"
    return line1, line2


def xml_escape(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def render(data: dict) -> str:
    title = f"{OWNER}/{REPO}"
    desc = data.get("description") or ""
    stars = k_formatter(data.get("stargazers_count", 0))
    forks = k_formatter(data.get("forks_count", 0))
    language = data.get("language") or LANG
    line1, line2 = wrap_description(desc)

    return f"""<svg width="400" height="140" viewBox="0 0 400 140" fill="none" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="descId">
  <title id="titleId">{xml_escape(title)}</title>
  <desc id="descId">{xml_escape(desc)}</desc>
  <style>
    .bg {{ fill: #fffefe; stroke: #e4e2e2; }}
    .header {{ font: 600 18px 'Segoe UI', Ubuntu, Sans-Serif; fill: #2f80ed; }}
    .description {{ font: 400 13px 'Segoe UI', Ubuntu, Sans-Serif; fill: #434d58; }}
    .gray {{ font: 400 12px 'Segoe UI', Ubuntu, Sans-Serif; fill: #434d58; }}
    .icon {{ fill: #586069; }}
    @supports(-moz-appearance: auto) {{ .header {{ font-size: 15.5px; }} }}
    @media (prefers-color-scheme: dark) {{
      .bg {{ fill: #151515; stroke: #e4e2e2; }}
      .header {{ fill: #fff; }}
      .description {{ fill: #9f9f9f; }}
      .gray {{ fill: #9f9f9f; }}
      .icon {{ fill: #79ff97; }}
    }}
  </style>
  <rect class="bg" data-testid="card-bg" x="0.5" y="0.5" rx="4.5" height="99%" width="399" stroke-opacity="1"/>
  <g data-testid="card-title" transform="translate(25, 35)">
    <g transform="translate(0, 0)">
      <svg class="icon" x="0" y="-13" viewBox="0 0 16 16" width="16" height="16">
        <path fill-rule="evenodd" d="M2 2.5A2.5 2.5 0 014.5 0h8.75a.75.75 0 01.75.75v12.5a.75.75 0 01-.75.75h-2.5a.75.75 0 110-1.5h1.75v-2h-8a1 1 0 00-.714 1.7.75.75 0 01-1.072 1.05A2.495 2.495 0 012 11.5v-9zm10.5-1V9h-8c-.356 0-.694.074-1 .208V2.5a1 1 0 011-1h8zM5 12.25v3.25a.25.25 0 00.4.2l1.45-1.087a.25.25 0 01.3 0L8.6 15.7a.25.25 0 00.4-.2v-3.25a.25.25 0 00-.25-.25h-3.5a.25.25 0 00-.25.25z"/>
      </svg>
    </g>
    <g transform="translate(25, 0)">
      <text x="0" y="0" class="header">{xml_escape(title)}</text>
    </g>
  </g>
  <g data-testid="main-card-body" transform="translate(0, 55)">
    <text class="description" x="25" y="-5">
      <tspan dy="1.2em" x="25">{xml_escape(line1)}</tspan><tspan dy="1.2em" x="25">{xml_escape(line2)}</tspan>
    </text>
    <g transform="translate(30, 65)">
      <g transform="translate(0, 0)">
        <g data-testid="primary-lang">
          <circle data-testid="lang-color" cx="0" cy="-5" r="6" fill="{LANG_COLOR}"/>
          <text data-testid="lang-name" class="gray" x="15">{xml_escape(language)}</text>
        </g>
      </g>
      <g transform="translate(62.275, 0)">
        <svg class="icon" y="-12" viewBox="0 0 16 16" width="16" height="16">
          <path fill-rule="evenodd" d="M8 .25a.75.75 0 01.673.418l1.882 3.815 4.21.612a.75.75 0 01.416 1.279l-3.046 2.97.719 4.192a.75.75 0 01-1.088.791L8 12.347l-3.766 1.98a.75.75 0 01-1.088-.79l.72-4.194L.818 6.374a.75.75 0 01.416-1.28l4.21-.611L7.327.668A.75.75 0 018 .25zm0 2.445L6.615 5.5a.75.75 0 01-.564.41l-3.097.45 2.24 2.184a.75.75 0 01.216.664l-.528 3.084 2.769-1.456a.75.75 0 01.698 0l2.77 1.456-.53-3.084a.75.75 0 01.216-.664l2.24-2.183-3.096-.45a.75.75 0 01-.564-.41L8 2.694v.001z"/>
        </svg>
        <text data-testid="stargazers" class="gray" x="20">{stars}</text>
      </g>
      <g transform="translate(123.24, 0)">
        <svg class="icon" y="-12" viewBox="0 0 16 16" width="16" height="16">
          <path fill-rule="evenodd" d="M5 3.25a.75.75 0 11-1.5 0 .75.75 0 011.5 0zm0 2.122a2.25 2.25 0 10-1.5 0v.878A2.25 2.25 0 005.75 8.5h1.5v2.128a2.251 2.251 0 101.5 0V8.5h1.5a2.25 2.25 0 002.25-2.25v-.878a2.25 2.25 0 10-1.5 0v.878a.75.75 0 01-.75.75h-4.5A.75.75 0 015 6.25v-.878zm3.75 7.378a.75.75 0 11-1.5 0 .75.75 0 011.5 0zm3-8.75a.75.75 0 100-1.5.75.75 0 000 1.5z"/>
        </svg>
        <text data-testid="forkcount" class="gray" x="20">{forks}</text>
      </g>
    </g>
  </g>
</svg>
"""


def main() -> int:
    data = fetch_repo()
    svg = render(data)
    OUT_PATH.write_text(svg, encoding="utf-8")
    print(
        f"Wrote {OUT_PATH} | stars={data['stargazers_count']} "
        f"forks={data['forks_count']} lang={data.get('language')}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
