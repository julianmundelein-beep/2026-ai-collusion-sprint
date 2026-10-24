#!/bin/sh
# Export paper/report.docx to paper/report.pdf through Pages (scripted), then print pages and headings per page.
# Needs the template font "Old Standard TT" installed for the user (the three .ttf files embedded in the template,
# copied to ~/Library/Fonts once); Pages must be restarted after installing it. Microsoft Word can replace Pages
# here when its scripting works on this machine.
set -e
cd "$(dirname "$0")/.."
SRC="$PWD/paper/report.docx"; OUT="$PWD/paper/report.pdf"
rm -f "$OUT"
osascript <<APPLESCRIPT
with timeout of 300 seconds
tell application "Pages"
  set d to open POSIX file "$SRC"
  export d to POSIX file "$OUT" as PDF
  close d saving no
end tell
end timeout
APPLESCRIPT
pdfinfo "$OUT" | grep -E '^(Pages|Page size)'
pdffonts "$OUT" | awk 'NR>2{print $1}' | sort -u | tr '\n' ' '; echo
n=$(pdfinfo "$OUT" | awk '/^Pages/{print $2}')
i=1; while [ $i -le $n ]; do
  printf "page %2d: " $i
  pdftotext -f $i -l $i "$OUT" - | grep -m1 -E '^(Abstract|[1-6]\. [A-Z]|Code and Data|References|Appendix|Limitations and Dual|LLM Usage)' || echo "(cont.)"
  i=$((i+1))
done
