import pytest

from source.barcode_to_text import extract_barcodes_from_pdf
from source.find_position_of_text import find_text_position
from source.get_pdf_data import extract_text_from_pdf, text_to_dict
from source.utils import get_default_date_format, pretty_print


@pytest.fixture(scope="function")
def base_pdf():
    file_path = "../task/test_task.pdf"
    return file_path


@pytest.mark.usefixtures("base_pdf")
class TestPdfData:

    def test_barcode_text_matches_pdf_text(self, base_pdf):
        """Test if barcode text matches extracted PDF text."""

        # Extract text from PDF
        extracted_text_data = extract_text_from_pdf(base_pdf)
        data = text_to_dict(extracted_text_data)
        # pretty_print(data)

        # Extract barcode data from PDF
        barcode_data = extract_barcodes_from_pdf(base_pdf)
        # pretty_print(barcode_data)

        # Extract barcode values
        barcode_texts = [
            barcode["data"] for key, barcode in barcode_data.items()
            if key.startswith("barcode_")
        ]
        print(barcode_texts)

        # Assertions
        assert barcode_texts, "❌ No barcodes found in the PDF."
        pn = barcode_texts[0]
        quantity = barcode_texts[1]

        assert pn == data["PN"]
        assert quantity == data["Qty"]

    def test_dates_not_null(self, base_pdf):
        """Test if date is not null"""
        extracted_text_data = extract_text_from_pdf(base_pdf)
        data = text_to_dict(extracted_text_data)

        assert data["EXP DATE"] is not None
        assert data["REC.DATE"] is not None
        assert data["DOM"] is not None

        exp_date = get_default_date_format(data["EXP DATE"])
        dom_date = get_default_date_format(data["DOM"])

        assert exp_date == dom_date

    def test_text_position(self, base_pdf):
        """Test if text position matches extracted PDF text."""
        extracted_text_data = extract_text_from_pdf(base_pdf)
        data = text_to_dict(extracted_text_data)

        original_position = (6.01, 6.25, 184.74, 17.99)

        pretty_print(data["name"])
        position = find_text_position(base_pdf, data["name"])["Page_1"][0]

        assert position == original_position
