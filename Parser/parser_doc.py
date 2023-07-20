import os
import docx
import re

def parse_docx(file_path):
    doc = docx.Document(file_path)
    paragraphs = doc.paragraphs

    # Regular expression patterns to match headings
    heading_pattern = re.compile(r'^\s*\d+(?:\.\d+)*\s*(.*)$')
    sub_heading_pattern = re.compile(r'^\s*\d+(?:\.\d+)*\s*(.*)$')
    sub_sub_heading_pattern = re.compile(r'^\s*\d+(?:\.\d+)*\s*(.*)$')

    # Create a folder for the extracted text files
    folder_name = "Extracted_Text"
    os.makedirs(folder_name, exist_ok=True)

    heading = ''
    sub_heading = ''
    sub_sub_heading = ''
    text = ''
    for paragraph in paragraphs:
        line = paragraph.text.strip()

        # Check if the line matches the heading pattern
        match_heading = heading_pattern.match(line)
        match_sub_heading = sub_heading_pattern.match(line)
        match_sub_sub_heading = sub_sub_heading_pattern.match(line)

        print(match_heading)
        print(match_sub_heading)
        print(match_sub_sub_heading)

        if match_heading:
            # Save the previous heading, subheading, and text to a file
            if heading and text:
                save_to_file(folder_name, heading, sub_heading, sub_sub_heading, text)

            # Update the heading, subheading, and sub-subheading
            heading = match_heading.group(1)
            sub_heading = ''
            sub_sub_heading = ''
            text = ''

        elif match_sub_heading:
            # Save the previous subheading and text to a file
            if sub_heading and text:
                save_to_file(folder_name, heading, sub_heading, sub_sub_heading, text)

            # Update the subheading and sub-subheading
            sub_heading = match_sub_heading.group(1)
            sub_sub_heading = ''
            text = ''

        elif match_sub_sub_heading:
            # Save the previous sub-subheading and text to a file
            if sub_sub_heading and text:
                save_to_file(folder_name, heading, sub_heading, sub_sub_heading, text)

            # Update the sub-subheading
            sub_sub_heading = match_sub_sub_heading.group(1)
            text = ''

        else:
            # Add the line to the text
            text += line + '\n'

    # Save the last heading, subheading, sub-subheading, and text to a file
    if heading and text:
        save_to_file(folder_name, heading, sub_heading, sub_sub_heading, text)


def save_to_file(folder, heading, sub_heading, sub_sub_heading, text):
    # Replace any invalid characters in the headings with underscores
    heading = re.sub(r'[^\w\s-]', '_', heading)
    sub_heading = re.sub(r'[^\w\s-]', '_', sub_heading)
    sub_sub_heading = re.sub(r'[^\w\s-]', '_', sub_sub_heading)

    # Create a file path with the folder and headings
    file_path = os.path.join(folder, f"{heading}{sub_heading}{sub_sub_heading}.txt")
    print("hi")
    with open(file_path, 'w') as file:
        file.write(text)

# Example usage
docx_file_path = 'Threat.docx'
parse_docx(docx_file_path)