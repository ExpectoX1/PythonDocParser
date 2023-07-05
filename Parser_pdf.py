import os
import PyPDF2
import re

def parse_pdf(file_path):
    pdf_file = open(file_path, 'rb')
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    num_pages = len(pdf_reader.pages)

    # Regular expression patterns to match headings
    heading_pattern = re.compile(r'^\s*\d+(?:\.\d+)*\s*(.*)$')
    sub_heading_pattern = re.compile(r'^\s*\d+(?:\.\d+)*\s*(.*)$')
    sub_sub_heading_pattern = re.compile(r'^\s*\d+(?:\.\d+)*\s*(.*)$')
    

    # Create a folder for the extracted text files
    folder_name = "Extracted_Text"
    os.makedirs(folder_name, exist_ok=True)

    for page_num in range(num_pages):
        page = pdf_reader.pages[page_num]
        content = page.extract_text()

        # Split the content into lines
        lines = content.split('\n')

        heading = ''
        sub_heading = ''
        sub_sub_heading = ''
        text = ''
        for line in lines:
            line = line.strip()

            # Check if the line matches the heading pattern
            match_heading = heading_pattern.match(line)
            match_sub_heading = sub_heading_pattern.match(line)
            match_sub_sub_heading = sub_sub_heading_pattern.match(line)

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

    pdf_file.close()

def save_to_file(folder, heading, sub_heading, sub_sub_heading, text):
    # Replace any invalid characters in the headings with underscores
    heading = re.sub(r'[^\w\s-]', '_', heading)
    sub_heading = re.sub(r'[^\w\s-]', '_', sub_heading)
    sub_sub_heading = re.sub(r'[^\w\s-]', '_', sub_sub_heading)
    filename_pattern = re.compile(r"\d\d-[A-Za-z][A-Za-z][A-Za-z]-[0-9]+")

    # Create a file path with the folder and headings
    filename = heading + sub_heading + sub_sub_heading

    if (filename_pattern.match(filename) == None):
        file_path = os.path.join(folder, f"{filename}.txt")
        with open(file_path, 'w') as file:
            file.write(text)
    else:
        # Handle the case when the filename does not match the specified pattern
        # You can choose to skip saving the file or modify the filename to match the desired format
        print(f"Skipping file: {filename}.txt")
        print(filename_pattern.match(filename))


# Example usage
pdf_file_path = 'Threat.pdf'
parse_pdf(pdf_file_path)
