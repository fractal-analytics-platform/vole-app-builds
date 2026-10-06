# Vol-E App Builds

This repository is used to generate pre-built versions of the [Vol-E App](https://github.com/allen-cell-animated/vole-app), with the configuration suitable for usage within the [Fractal platform](https://fractal-analytics-platform.github.io).

The upstream Vol-E App is released under the [BSD 3-Clause License (Copyright 2017-2026, Allen Institute)](https://github.com/allen-cell-animated/vole-app/blob/main/LICENSE).

---

The build script is available at [`build-vole.sh`](./build-vole.sh).
The differences with respect to the upstream repository are:
    * We disable tracking, by setting `VITE_GTM_ID=`.
    * We install `@fontsource/open-sans`.
    * We bundle `materialicons.woff2` in the `assets` folder of the build.
    * We apply the [`fonts.patch`](./fonts.patch) patch.