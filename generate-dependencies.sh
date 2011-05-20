#!/bin/sh
# Generate a dependency graph for the project

# Output PDF
sfood --internal --internal ./ | sfood-graph | dot -Tps | ps2pdf - dependencies.pdf

# Output PNG
#sfood --internal --internal ./ | sfood-graph | dot -Tpng -o dependencies.png

