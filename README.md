# Vol-E App Builds

This repository is used to generate pre-built versions of the [Vol-E App](https://github.com/allen-cell-animated/vole-app), with the configuration suitable for usage within the [Fractal platform](https://fractal-analytics-platform.github.io).

The upstream Vol-E App is released under the [BSD 3-Clause License (Copyright 2017-2026, Allen Institute)](https://github.com/allen-cell-animated/vole-app/blob/main/LICENSE).

---

More details:
1. The build script is available at [`build-vole.sh`](./build-vole.sh), and it also applies the [`fonts.patch`](./fonts.patch) patch.
2. A helper script to compare the latest upstream tag with the existing ones and trigger a new build can be run via `uv run compare-and-create-tags.py`.
