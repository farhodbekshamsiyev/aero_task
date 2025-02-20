from source.barcode_to_text import extract_barcodes_from_pdf
from source.get_pdf_data import extract_text_from_pdf, text_to_dict
from source.utils import pretty_print


def main():
    print("Reading pdf and getting data!")
    pdf_path = "./task/test_task.pdf"
    pdf_content = extract_text_from_pdf(pdf_path)
    output = text_to_dict(pdf_content)
    pretty_print(output)
    print(end="\\" * 55)

    print("\nReading Barcode!")
    barcode_data = extract_barcodes_from_pdf(pdf_path)
    pretty_print(barcode_data)


if __name__ == "__main__":
    main()
