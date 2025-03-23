#!/bin/bash
# build.sh - Build the site for production with the correct base path


python3 src/main.py "/static-sites2/"

echo "Site built successfully with base path /static-sites2/"