#!/bin/bash

set -e

SCRIPT_DIR=$(cd `dirname "$0"`; pwd)
BASE_DIR=`dirname "${SCRIPT_DIR}"`

cd "${BASE_DIR}"

# Extracts all languages, or only select ones if arguments are passed in
extractLanguages () {
  # Get language list
  local langs file="$1"
  shift
  if [ $# -gt 0 ]; then
    # Languages were specified in positional arguments, use them
    langs=$@
  else
    # No languages specified, get all of them
    langs=$("${SCRIPT_DIR}/msrt_tool.py" --list "${BASE_DIR}/$file.msrt" | cut -d ' ' -f1)
  fi

  # Extract languages from list 1 at a time
  local lang
  for lang in ${langs}; do
    echo "Generating $lang for $file"
    [ -d "${BASE_DIR}/output/$file" ] || mkdir -p "${BASE_DIR}/output/$file"
    "${SCRIPT_DIR}/msrt_tool.py" --extract "$lang" "${BASE_DIR}/output/$file/$file-$lang.srt" "${BASE_DIR}/$file.msrt"
  done
}

FILES=( "pepper-and-carrot-ep6" "morevna-ep3" "pepper-course-lesson-1" )

for FILE in "${FILES[@]}"; do
  extractLanguages "$FILE"
done
