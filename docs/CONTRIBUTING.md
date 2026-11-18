# Maintaining this profile

This repository is both a GitHub profile README and a snapshot of the
generated assets that the README embeds. The default branch is the profile
page, so every commit here is visible at `github.com/master-bry`.

## Layout

| Path | Purpose |
| --- | --- |
| `README.md` | Profile page shown on GitHub |
| `assets/` | Contribution snake snapshots used by the README |
| `profile-summary-card-output/` | Card snapshots for every theme |
| `profile-summary-card-output/INDEX.md` | Alphabetical theme index |
| `scripts/validate_profile.py` | Local and CI integrity checks |
| `.github/workflows/` | Regeneration and validation automation |

## Changing the profile

Edit `README.md` on `main`. Use local paths under `assets/` or
`profile-summary-card-output/` for images that live in this repository, and
keep descriptive alt text on every image.

To switch the visible card theme, replace the `tokyonight` path in the four
image URLs in the **Profile Summary** section with another directory from the
[theme index](../profile-summary-card-output/INDEX.md). The other palettes are
already generated, so no CI run is required.

## Regenerating analytics

Run **Profile Analytics** from the Actions tab to rebuild all card themes and
the contribution snake. It needs `SUMMARY_GITHUB_TOKEN` with access to private
contributions. The workflow also refreshes `?v=` cache keys in the README.

Run **Refresh README Stats** to refresh the streak cache key between daily
analytics runs.

Both automation workflows commit with `[skip ci]`. The **Validate Profile**
workflow checks the result on every push and pull request.

## Checks

Run the same checks as CI before committing:

```bash
python3 scripts/validate_profile.py
```

The validator checks that every theme has five well-formed SVG cards, that
theme pages showcase all five cards with descriptive alt text, that all local
README images resolve, and that every theme is listed in the gallery index.

## Adding a theme

1. Run **Profile Analytics** after the generator supports the new palette.
2. Confirm the new directory has `0-profile-details.svg` through
   `4-productive-time.svg` and its own `README.md`.
3. Add the theme to `profile-summary-card-output/INDEX.md`.
4. Improve the generated theme page with a short description and navigation,
   then run the validator.
