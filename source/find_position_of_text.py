import fitz  # PyMuPDF

def find_text_position(pdf_path, search_text):
    """Find the exact position of text in a PDF."""
    results = {}

    with fitz.open(pdf_path) as doc:  # Using context manager
        for page_num in range(len(doc)):
            page = doc[page_num]
            text_instances = page.search_for(search_text)  # Find occurrences of text

            if text_instances:
                results[f"Page_{page_num + 1}"] = [
                    (round(rect.x0, 2), round(rect.y0, 2), round(rect.x1, 2), round(rect.y1, 2))
                    for rect in text_instances
                ]

    return results



# Example Usage
pdf_path = "../task/test_task.pdf"  # Replace with your actual PDF file
text_to_find = "GRIFFON AVIATION SERVICES LLC"  # Text you want to locate
positions = find_text_position(pdf_path, text_to_find)
print(type(positions["Page_1"]))

print(positions)  # Output: {'Page_1': [Rect(50.2, 100.3, 200.4, 120.5)]}
