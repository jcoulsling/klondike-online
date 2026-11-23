#!/bin/bash
# Rebuilds the Hän FireRed game from nothing on Ubuntu or WSL.
# Run it in an empty folder that holds this script, han-firered.patch and the workbook.
set -e
HERE="$(cd "$(dirname "$0")" && pwd)"
BOOK="$HERE/haa_firered-strings_coulson_2026-11-17.xlsx"

sudo apt-get update
sudo apt-get install -y build-essential binutils-arm-none-eabi git libpng-dev python3-pil python3-openpyxl

[ -d agbcc ] || git clone https://github.com/pret/agbcc
[ -d pokefirered ] || git clone https://github.com/pret/pokefirered
# the Pokémon pictures and animations come from Emerald's source when the game is built
[ -d pokeemerald ] || git clone https://github.com/pret/pokeemerald
(cd pokeemerald && git checkout -q 9103e529c2fbdd7add4a1ff3350c6c1f92112c42)

# the exact versions this patch was made against
(cd agbcc && git checkout -q da598c1d918402c42c0c0d7128ba14567f3175e9 && ./build.sh && ./install.sh ../pokefirered)

cd pokefirered
git checkout -q ce6406d8c2eaf46d543c8a2606de0c3cb1951982

# 1. the untouched source must rebuild the original game exactly
make compare -j"$(nproc)"        # must end with: pokefirered.gba: OK

# 2. add the Hän letters and tools
git apply "$HERE/han-firered.patch"

# CHAMPION JANE's battle theme is someone else's music, so it is not in the patch.
# If you have the MIDI file Jane used, put it in this folder as jane_theme.mid. The build looks for it there.
# (A recording works too: tools/han/README.md says how.)
# Without it the game builds the same, and her battle has the ELITE FOUR's battle music, as before.
# And for MANDI's SYLVEON: sylveon.png in this folder. Without it the SYLVEON is shown as ??.

# 3. put the Hän text in and build
python3 tools/han/han_text.py build "$BOOK" --report "$HERE/workbook_after_build.xlsx"

echo
echo "Done. The game is pokefirered/pokefirered.gba"
echo "To rebuild after editing the workbook, run step 3 again with the new file."
