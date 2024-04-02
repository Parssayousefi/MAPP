from docx import Document
import os
import re

def sanitize_filename(filename):
    """
    Sanitize the block name to be used as a valid filename by removing or replacing invalid characters.
    """
    return re.sub(r'[\\/*?:"<>|]', "", filename)

def parse_and_create_docs(docx_path, output_path):
    doc = Document(docx_path)
    current_block_name = ""
    block_started = False
    new_doc = None

    for paragraph in doc.paragraphs:
        text = paragraph.text.strip()
        if text.startswith("Start of Block:"):
            if new_doc:  # Save and close the previous document before starting a new one
                filename = os.path.join(output_path, sanitize_filename(current_block_name) + ".docx")
                new_doc.save(filename)
            current_block_name = text[len("Start of Block:"):].strip()
            new_doc = Document()  # Start a new document
            block_started = True
        elif text.startswith("End of Block:"):
            if new_doc:  # End of block, save the document
                filename = os.path.join(output_path, sanitize_filename(current_block_name) + ".docx")
                new_doc.save(filename)
                new_doc = None
            block_started = False
        else:
            if block_started:  # If we are currently in a block, add the paragraph to the new doc
                new_doc.add_paragraph(text)

    # Handle tables separately
    if new_doc:  # If there's an open document, save it
        filename = os.path.join(output_path, sanitize_filename(current_block_name) + ".docx")
        new_doc.save(filename)

    # Now, process tables
    for table in doc.tables:
        if new_doc:  # Assuming tables should be added to the end of the current document
            new_table = new_doc.add_table(rows=0, cols=0)  # Create a new table to copy the content
            for row in table.rows:
                new_cells = new_table.add_row().cells
                for index, cell in enumerate(row.cells):
                    if index < len(new_cells):  # Prevent index error
                        new_cells[index].text = cell.text
            filename = os.path.join(output_path, sanitize_filename(current_block_name) + ".docx")
            new_doc.save(filename)

# Example usage
#parse_and_create_docs(".\\Questionairs\\Scale_Survey.docx", ".\\Questionairs\\word_files")


docx_path = r"C:\Users\prsyu\OneDrive\Bidlung\University\M.S. Leiden University\M.S. Neuroscience (Research)\MAPP\Analysis\Github_Clone\MAPP\Questionairs\Scale_Survey.docx" 

output_path = r"C:\Users\prsyu\OneDrive\Bidlung\University\M.S. Leiden University\M.S. Neuroscience (Research)\MAPP\Analysis\Github_Clone\MAPP\Questionairs\word_files" 


# Ensure output directory exists
os.makedirs(output_path, exist_ok=True)

# Now call your function
parse_and_create_docs(docx_path, output_path)