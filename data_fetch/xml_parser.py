import xml.etree.ElementTree as ET

# TODO
# Script should have input parameters such as :
# - Path to the file we are going to parse
# - Path to directory where we are going to save data
# - Needed tags needed to take from xml file
# If file contains more than 1 xml object, need to create
# logic to have unique paths to parsed files
# PS: Used module require not damaged single xml file
# Saving every xml file to its tmp file holder is
# inefficient so script should have buffer to which we
# save xml object

def process_xml_file(xml_file):
    try:
        # Try to open xml file
        with open(xml_file, 'r') as file:
            xml_content = file.read()

        # Try to parse file content
        #! Vulnerable
        root = ET.fromstring(xml_content)

        # Iterate over xml object and print its content
        for element in root.iter():
            print(f"Tag: {element.tag}, Value: {element.text}")

    except FileNotFoundError:
        print(f"File {xml_file} was not found.")
    except ET.ParseError as e:
        print(f"Parse error XML: {e}")

if __name__ == "__main__":
    xml_file_path = "sample.xml"
    process_xml_file(xml_file_path)
