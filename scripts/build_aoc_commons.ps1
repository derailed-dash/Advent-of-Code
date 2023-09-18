# Author: Darren
# 
# Utility script to build dazbo-aoc-commons and upload it to PyPI.
# Then, install the module:
# py -m pip install dazbo-aoc-commons

Set-Location C:\Users\djl\localdev\Python\Advent-of-Code\scripts
Set-Location ..\src\aoc_common\
"`nDeleting dist folder..."
if (Test-Path "dist") {
    Remove-Item -LiteralPath "dist" -Recurse -Force
}

"`nRunning package build..."
py -m setup sdist

"`nUploading to PyPi..."
py ..\..\scripts\upload_to_pypi.py

"`nResetting folder."
Set-Location ..\..
