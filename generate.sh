#!/bin/bash
set -e

XML_FILES_DIR="./descriptions"
OUT_DIR="./generated"

mkdir -p "$OUT_DIR"

echo "Searching for *mav.xml files in $XML_FILES_DIR..."

mapfile -d '' MAV_FILES < <(find "$XML_FILES_DIR" -type f -name '*mav.xml' -print0)

if [ ${#MAV_FILES[@]} -eq 0 ]; then
    echo "⚠️  No '*mav.xml' files found in $XML_FILES_DIR. Nothing to do."
    exit 0
fi

for xml_file in "${MAV_FILES[@]}"; do
    xml_file="$xml_file"
    base_name=$(basename "$xml_file" .xml)

    python_out="$OUT_DIR/python/$base_name"
    c_out="$OUT_DIR/c/$base_name"

    mkdir -p "$python_out"
    mkdir -p "$c_out"

    echo "\nGenerating MAVLink bindings from: $xml_file"
    echo "    -> Python: $python_out"
    mavgen.py \
        --lang Python \
        --wire-protocol 2.0 \
        --output "$python_out" \
        "$xml_file"

    echo "    -> C: $c_out"
    mavgen.py \
        --lang C \
        --wire-protocol 2.0 \
        --output "$c_out" \
        "$xml_file"
done

echo "\nDone!"
echo "Generated Python bindings under: $OUT_DIR/python/"
echo "Generated C bindings under:      $OUT_DIR/c/"
