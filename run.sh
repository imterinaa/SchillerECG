#!/bin/bash
PORT=8080
OUTPUT_FILE="sample.xml"

while true; do
        request = $(nc -l -p $PORT)
        echo "Recieved request:"
        echo "$request"

        data=$(echo "$request" | awk '/^$/ {p=1; next} p')

        echo "Recieved data:"
        echo "$data"
        
        echo "$data" >> "${OUTPUT_FILE}"
        closing_tag="</com.xiriuz.sema.xml.schillerEDI.SchillerEDI>"
        if [ ! -f "${OUTPUT_FILE}" ]; then
            echo "Файл ${OUTPUT_FILE} не существует."
        fi
        if grep -q "$closing_tag" "${OUTPUT_FILE}"; then
            echo "XML файл содержит закрывающийся тег: $closing_tag"
            ./sendfile.sh 
            rm "${OUTPUT_FILE}"
        else
            echo "XML файл НЕ содержит закрывающийся тег: $closing_tag"
        fi
