import os
import pdfplumber
import re

def parse_pdf(file_path, master_folder, new_file_path):
    with pdfplumber.open(file_path) as pdf:
        num_pages = len(pdf.pages)

        # Regular expression patterns to match headings
        heading_pattern = re.compile(r'^\s*\d+(?:\.\d+)*\s*(.*)$')
        sub_heading_pattern = re.compile(r'^\s*\d+(?:\.\d+)*\s*(.*)$')
        sub_sub_heading_pattern = re.compile(r'^\s*\d+(?:\.\d+)*\s*(.*)$')

        # Create a folder for the extracted text files
        if new_file_path is None:
            new_file_path = file_path
        
        folder_name = os.path.splitext(os.path.basename(new_file_path))[0]
        folder_path = os.path.join(master_folder, folder_name)
        os.makedirs(folder_path, exist_ok=True)

        for page_num in range(num_pages):
            page = pdf.pages[page_num]
            content = page.extract_text()

            # Split the content into lines
            lines = content.split('\n')

            heading = ''
            sub_heading = ''
            sub_sub_heading = ''
            text = ''
            tables = page.extract_tables()  # Extract all tables from the page

            for line in lines:
                line = line.strip()

                # Check if the line matches the heading pattern
                match_heading = heading_pattern.match(line)
                match_sub_heading = sub_heading_pattern.match(line)
                match_sub_sub_heading = sub_sub_heading_pattern.match(line)

                if match_heading:
                    # Save the previous heading, subheading, text, and tables to a file
                    if heading and (text or tables):
                        save_to_file(folder_path, heading, sub_heading, sub_sub_heading, text, tables)

                    # Update the heading, subheading, and sub-subheading
                    heading = match_heading.group(1)
                    sub_heading = ''
                    sub_sub_heading = ''
                    text = ''
                    tables = []

                elif match_sub_heading:
                    # Save the previous subheading, text, and tables to a file
                    if sub_heading and (text or tables):
                        save_to_file(folder_path, heading, sub_heading, sub_sub_heading, text, tables)

                    # Update the subheading and sub-subheading
                    sub_heading = match_sub_heading.group(1)
                    sub_sub_heading = ''
                    text = ''
                    tables = []

                elif match_sub_sub_heading:
                    # Save the previous sub-subheading, text, and tables to a file
                    if sub_sub_heading and (text or tables):
                        save_to_file(folder_path, heading, sub_heading, sub_sub_heading, text, tables)

                    # Update the sub-subheading
                    sub_sub_heading = match_sub_sub_heading.group(1)
                    text = ''
                    tables = []

                else:
                    # Add the line to the text
                    text += line + '\n'

            # Save the last heading, subheading, sub-subheading, text, and tables to a file
            if heading and (text or tables):
                save_to_file(folder_path, heading, sub_heading, sub_sub_heading, text, tables)

def save_to_file(folder, heading, sub_heading, sub_sub_heading, text, tables):
    # Replace any invalid characters in the headings with underscores
    heading = re.sub(r'[^\w\s-]', '', heading)
    sub_heading = re.sub(r'[^\w\s-]', '', sub_heading)
    sub_sub_heading= re.sub(r'[^\w\s-]', '', sub_sub_heading)
    filename_pattern = re.compile(r"\d\d-[A-Za-z][A-Za-z][A-Za-z]-[0-9]+")

    # Create a file path with the folder and headings
    filename = heading + sub_heading + sub_sub_heading

    if filename_pattern.match(filename) is None:
        file_path = os.path.join(folder, f"{filename}.txt")
        try:
            with open(file_path, 'w') as file:
                if text.strip():
                    file.write(text.strip())
                if tables:
                    for table in tables:
                        file.write('\t'.join(row) + '\n')
        except IOError as e:
            print(f"Failed to write file: {file_path}. Error: {e}")
    else:
        # Handle the case when the filename does not match the specified pattern
        # You can choose to skip saving the file or modify the filename to match the desired format
        print(f"Skipping file: {filename}.txt")
        print(filename_pattern.match(filename))


def pdf_ext_auto():
    master_folder = "./MASTER_EXTRACT_AUTO"
    os.makedirs(master_folder, exist_ok=True)

    # Loop to input multiple pdf files from a folder and process them automatically
    file_store_dir = "./Files_to_be_parsed"
    stored_files = os.listdir(file_store_dir)

    # Store the file extension check
    ext = ".pdf"
    for i in range(0, len(stored_files)):
        if stored_files[i][-4:] == ext:
            try:
                parse_pdf(file_store_dir+"/"+stored_files[i], master_folder, new_file_path=None)
            except Exception as e:
                print(f"Error parsing file: {stored_files[i]}. Error: {e}")


def pdf_ext_manual():
    # Create the "MASTER" folder
    master_folder = "./MASTER_EXTRACT_MANUAL"
    os.makedirs(master_folder, exist_ok=True)

    # Loop to process multiple PDF files
    while True:
        pdf_file_path = input("Enter Original Document Name (or 'stop' to exit): ")
        try:
            if pdf_file_path.lower() == "stop" or pdf_file_path.lower()=="exit":
                break
            if(pdfplumber.open(pdf_file_path)== False):
             print("File Does not exist")
             break
        except Exception as e:
            print(f"File does not exist: {pdf_file_path}. Error: {e}")
            continue

       

        new_file_path = input("Enter the Folder Name: ")

        try:
            parse_pdf(pdf_file_path, master_folder, new_file_path)
        except Exception as e:
            print(f"Error parsing file: {pdf_file_path}. Error: {e}")

    print("Extraction completed.")

print("\n*********************Auto PDFParser v1.0*********************\n")
print("There are two modes in this program\nAuto and Manual Mode.\nIn manual mode, each file name needs to be inputted with its extension (.pdf)\nalso all the files need to be in the Parser Directory.\n \nAuto mode requires you to put all the files in the (./Files_to_be_Parsed) directory.")
choice = input("\nManual or Auto Mode? ")
if choice.lower() == "auto" or choice.lower() == "a":
    pdf_ext_auto()
elif choice.lower() == "manual" or choice.lower() == "m":
    pdf_ext_manual()
else:
    print('Invalid choice.')
