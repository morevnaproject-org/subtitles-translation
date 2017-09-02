#!/bin/sh

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
    #if [[ -n $lang ]]; then
      echo "Generating $lang for $file"
      [ -d "${BASE_DIR}/output/$file" ] || mkdir -p "${BASE_DIR}/output/$file"
      echo "$lang" "${BASE_DIR}/output/$file/$file-$lang.srt" "${BASE_DIR}/$file.msrt"
      "${SCRIPT_DIR}/msrt_tool.py" --extract "$lang" "${BASE_DIR}/output/$file/$file-$lang.srt" "${BASE_DIR}/$file.msrt"
    #fi
  done
}

FILES=("pepper-and-carrot-ep6" "morevna-ep3")

for FILE in "${FILES[@]}"; do
  extractLanguages "$FILE"
done

#FILE="synfig-course-promo"
#for LANG in rus eng epo spa; do
#[ -d "${BASE_DIR}/output/${FILE}" ] || mkdir -p "${BASE_DIR}/output/${FILE}"
#python ${SCRIPT_DIR}/msrt_tool.py ${FILE}.msrt --extract ${LANG} ${BASE_DIR}/output/${FILE}/${FILE}-${LANG}.srt
#done
