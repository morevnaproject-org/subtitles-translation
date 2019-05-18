#!/bin/bash

set -e

SCRIPT_DIR=$(cd `dirname "$0"`; pwd)
BASE_DIR=`dirname "${SCRIPT_DIR}"`

cd "${BASE_DIR}"

# Extracts all languages, or only select ones if arguments are passed in
extractLanguages () {
  # Regular file
  if [ ! -d "$1" ]; then
    
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
  
  # Directory
  else
    
    local dir="$1"
    FILELIST=`ls -1 "$dir/"*.msrt`
    shift
    if [ $# -gt 0 ]; then
      # Languages were specified in positional arguments, use them
      langs_option=$@
    fi
    
    for file in ${FILELIST}; do
        file=`basename ${file} .msrt`
        
        if [ -z "${langs_option}" ]; then
          langs=$("${SCRIPT_DIR}/msrt_tool.py" --list "${BASE_DIR}/$dir/$file.msrt" | cut -d ' ' -f1)
        else
          langs=${langs_option}
        fi
        
        local lang
        for lang in ${langs}; do
          echo "Generating $lang for $dir/$file"
          [ -d "${BASE_DIR}/output/$dir/$lang" ] || mkdir -p "${BASE_DIR}/output/$dir/$lang"
          "${SCRIPT_DIR}/msrt_tool.py" --extract "$lang" "${BASE_DIR}/output/$dir/$lang/$file.srt" "${BASE_DIR}/$dir/$file.msrt"
        done
    done
    
  fi
}

FILES=( "pepper-and-carrot-ep6" "morevna-ep3" "morevna-ep4" "course-synfig" "course-pepper" "the-story-of-mim-and-tiger" )

# generating subtitles
for FILE in "${FILES[@]}"; do
  extractLanguages "$FILE"
done

# creating release archives
cd "${BASE_DIR}/output"
rm *.zip || true
FILES=( "course-synfig" "course-pepper" )
for DIR in "${FILES[@]}"; do
  zip -r ${DIR}.zip ${DIR}
done
