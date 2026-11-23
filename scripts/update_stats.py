import json
import os
import urllib.request

USER = "master-bry"
TOKEN = os.environ.get("GITHUB_TOKEN", "")


def api(url):
    req = urllib.request.Request(url)
    req.add_header("Accept", "application/vnd.github+json")
    if TOKEN:
        req.add_header("Authorization", "Bearer " + TOKEN)
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp)


def all_repos():
    repos, page = [], 1
    while True:
        batch = api(f"https://api.github.com/users/{USER}/repos?per_page=100&page={page}")
        if not batch:
            break
        repos.extend(batch)
        page += 1
    return repos


def card(x, label, value, color):
    return (
        f'<g transform="translate({x},0)">'
        f'<rect width="180" height="70" rx="8" fill="#0f172a" stroke="{color}" stroke-width="2"/>'
        f'<text x="90" y="34" text-anchor="middle" font-family="Segoe UI, Arial, sans-serif" '
        f'font-size="26" font-weight="700" fill="{color}">{value}</text>'
        f'<text x="90" y="56" text-anchor="middle" font-family="Segoe UI, Arial, sans-serif" '
        f'font-size="13" fill="#94a3b8">{label}</text></g>'
    )


def main():
    user = api(f"https://api.github.com/users/{USER}")
    repos = all_repos()
    stars = sum(r.get("stargazers_count", 0) for r in repos)

    cards = [
        ("Followers", user["followers"], "#22c55e"),
        ("Public Repos", user["public_repos"], "#0ea5e9"),
        ("Stars", stars, "#f59e0b"),
        ("Following", user["following"], "#a78bfa"),
    ]
    body = "".join(card(i * 200, lbl, val, col) for i, (lbl, val, col) in enumerate(cards))
    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" width="780" height="70" viewBox="0 0 780 70">'
        + body + "</svg>"
    )

    os.makedirs("assets", exist_ok=True)
    with open("assets/stats.svg", "w", encoding="utf-8") as f:
        f.write(svg)


if __name__ == "__main__":
    main()
