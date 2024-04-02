from docx import Document
import re

def sanitize_filename(filename):
    """
    Sanitize the block name to be used as a valid filename by removing or replacing invalid characters.
    """
    return re.sub(r'[\\/*?:"<>|]', "", filename)  # Removes characters that are invalid in Windows filenames

def parse_questionnaire(docx_path):
    doc = Document(docx_path)
    current_block_name = ""
    block_contents = []
    blocks = {}

    for paragraph in doc.paragraphs:
        text = paragraph.text.strip()
        if text.startswith("Start of Block:"):
            # If a new block starts, save the previous block (if any) and reset variables
            if current_block_name and block_contents:
                blocks[current_block_name] = block_contents
            current_block_name = text[len("Start of Block:"):].strip()
            block_contents = []
        elif text.startswith("End of Block:"):
            # When a block ends, save it
            if current_block_name and block_contents:
                blocks[current_block_name] = block_contents
                current_block_name = ""
                block_contents = []
        else:
            block_contents.append(text)

    # In case the document does not end with "End of Block:"
    if current_block_name and block_contents:
        blocks[current_block_name] = block_contents

    # Write each block to a separate file
    for block_name, contents in blocks.items():
        filename = sanitize_filename(block_name) + ".txt"
        with open(filename, "w", encoding="utf-8") as file:
            file.write("\n".join(contents))
        print(f"Block '{block_name}' saved to {filename}.")

# Example usage
parse_questionnaire("\Questionairs\Scale_Survey.docx")
