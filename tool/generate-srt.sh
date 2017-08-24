#!/bin/sh

set -e

# TODO: Ideally, it would be nice to improve msrt_tool.py, so it can automatically extract all available languages from msrt file.

SCRIPT_DIR=$(cd `dirname "$0"`; pwd)
BASE_DIR=`dirname "${SCRIPT_DIR}"`

cd ${BASE_DIR}

FILE="pepper-and-carrot-ep6"
for LANG in rus dan eng epo jbo fra deu por ita spa; do
[ -d "${BASE_DIR}/output/${FILE}" ] || mkdir -p "${BASE_DIR}/output/${FILE}"
python ${SCRIPT_DIR}/msrt_tool.py ${FILE}.msrt --extract ${LANG} ${BASE_DIR}/output/${FILE}/${FILE}-${LANG}.srt
done

FILE="morevna-ep3"
for LANG in rus eng; do
[ -d "${BASE_DIR}/output/${FILE}" ] || mkdir -p "${BASE_DIR}/output/${FILE}"
python ${SCRIPT_DIR}/msrt_tool.py ${FILE}.msrt --extract ${LANG} ${BASE_DIR}/output/${FILE}/${FILE}-${LANG}.srt
done

#FILE="synfig-course-promo"
#for LANG in rus eng epo spa; do
#[ -d "${BASE_DIR}/output/${FILE}" ] || mkdir -p "${BASE_DIR}/output/${FILE}"
#python ${SCRIPT_DIR}/msrt_tool.py ${FILE}.msrt --extract ${LANG} ${BASE_DIR}/output/${FILE}/${FILE}-${LANG}.srt
#done
