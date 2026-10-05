#!/bin/sh

set -e

if [ "$#" -lt 1 ]; then
  echo "Usage: $0 <tag-or-commit>"
  exit 2
fi

rm -rf ./vole-app
git clone https://github.com/allen-cell-animated/vole-app.git
cd vole-app
git checkout "$1"

git apply ../fonts.patch
cp ../.env.local .

npm ci
npm i @fontsource/open-sans

mkdir src/aics-image-viewer/assets/fonts/materialicons/
wget -O src/aics-image-viewer/assets/fonts/materialicons/materialicons.woff2 https://fonts.gstatic.com/s/materialicons/v29/2fcrYFNaTjcS6g4U3t-Y5ZjZjT5FdEJ140U2DJYC3mY.woff2

npm run s3-build

cp LICENSE imageviewer/
tar -C imageviewer -czf vole-app.tar.gz .
