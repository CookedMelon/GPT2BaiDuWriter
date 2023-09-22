#!/bin/bash

cd "./newarticles/$1"
find . -name '*.txt' -print0 |
xargs -0 -I {} sh -c 'pandoc -o "$(dirname "{}")/$(basename "{}" .txt).docx" "{}"&& rm "{}"'
echo "Done!"