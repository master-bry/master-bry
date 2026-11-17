# Profile analytics

The `README.md` on the default branch is the GitHub profile page. Several of
its visuals are generated or cached automatically.

## Generated assets

| Path | Generator | Refreshed by |
| --- | --- | --- |
| `assets/github-snake.svg` | `Platane/snk/svg-only@v3` | Profile Analytics workflow |
| `assets/github-snake-dark.svg` | `Platane/snk/svg-only@v3` | Profile Analytics workflow |
| `profile-summary-card-output/<theme>/*.svg` | `vn7n24fzkq/github-profile-summary-cards` | Profile Analytics workflow |

The profile uses the `tokyonight` cards. The other themes are kept so the look
can be changed without regenerating anything.

## Workflows

- `.github/workflows/profile-analytics.yml` runs daily and on demand. It needs
  the `SUMMARY_GITHUB_TOKEN` secret with permission to read private activity,
  regenerates the cards and the snake, refreshes the image query strings and
  commits the results.
- `.github/workflows/update-readme.yml` refreshes the streak cache key every
  six hours.

Both workflows mark their commits with `[skip ci]` so they cannot trigger
themselves in a loop.

## Troubleshooting

- Stale contribution graph: run **Profile Analytics** manually and check that
  `SUMMARY_GITHUB_TOKEN` is still valid.
- Stale streak only: run **Refresh README Stats** manually.
- The `output` branch still contains the original snake deployment. The
  README now reads the snapshots from `main`, so that branch is no longer a
  single point of failure.
