import os

import fitz  # PyMuPDF

from source.utils import pretty_print


def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF and return as a dictionary with error handling."""
    pdf_data = {"metadata": {}, "pages": {}}

    try:
        doc = fitz.open(pdf_path)
        pdf_data["metadata"] = doc.metadata if doc.metadata else {}

        for page_num in range(len(doc)):
            try:
                text = doc[page_num].get_text("text").strip()
                pdf_data["pages"][f"Page_{page_num + 1}"] = text if text else "No text found on this page."
            except Exception as e:
                print(f"Error extracting text from page {page_num + 1}: {e}")
                pdf_data["pages"][f"Page_{page_num + 1}"] = f"Error reading page: {e}"

        doc.close()

    except FileNotFoundError:
        print(f"Error: PDF file '{pdf_path}' not found.")
    except PermissionError:
        print(f"Error: Permission denied for '{pdf_path}'.")
    except Exception as e:
        print(f"Unexpected error while processing PDF: {e}")

    return pdf_data


def text_to_dict(text):
    """Convert structured text into a dictionary."""
    text = text["pages"]["Page_1"]
    data_dict = {}
    lines = text.split("\n")

    data_dict["name"] = lines[0].strip()
    data_dict["others"] = list()

    for line in lines[1:]:
        if ":" in line:  # Ensure line contains key-value pair
            key, value = line.split(":", 1)  # Split only on first colon
            data_dict[key.strip()] = value.strip()
        elif line:
            data_dict["others"].append(line.strip())

    return data_dict


if __name__ == "__main__":
    pdf_path = "../task/test_task.pdf"

    if not os.path.exists(pdf_path):
        print(f"Error: PDF file '{pdf_path}' does not exist.")
    else:
        pdf_content = extract_text_from_pdf(pdf_path)
        output = text_to_dict(pdf_content)
        pretty_print(output)
