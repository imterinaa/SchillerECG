#!/bin/sh

xml_file="./sample.xml"
server_url="http://91.222.236.29:5000/upload"
response=$(curl -X POST "$server_url" --data-binary @$xml_file)
echo "Response from server:"
echo "$response"
