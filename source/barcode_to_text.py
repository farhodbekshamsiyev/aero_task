import json
import os
import shutil

import cv2
from pdf2image import convert_from_path
from pyzbar.pyzbar import decode

from source.utils import pretty_print

# Constants
OUTPUT_FOLDER = "pdf_images"


def convert_pdf_to_images(pdf_path):
    """Convert PDF pages to PNG images and save them."""
    try:
        os.makedirs(OUTPUT_FOLDER, exist_ok=True)  # Ensure output folder exists
        images = convert_from_path(pdf_path)
        image_paths = []

        for i, image in enumerate(images):
            image_filename = f"{OUTPUT_FOLDER}/page_{i + 1}.png"
            image.save(image_filename, "PNG")
            image_paths.append(image_filename)

        if not image_paths:
            raise ValueError("No images were generated from the PDF.")

        return image_paths

    except FileNotFoundError:
        print(f"Error: PDF file not found at {pdf_path}.")
    except PermissionError:
        print(f"Error: Permission denied when accessing {pdf_path}.")
    except Exception as e:
        print(f"Unexpected error while converting PDF to images: {e}")
    return []


def decode_barcodes_from_images(image_paths):
    """Decode barcodes from PNG images within specific regions."""
    barcode_data = {}
    regions = [
        (15, 45, 755, 110),  # Adjust these coordinates for your PDF
        (45, 225, 245, 515)
    ]

    try:
        if not image_paths:
            raise ValueError("No images provided for barcode decoding.")

        for image_path in image_paths:
            image = cv2.imread(image_path)
            if image is None:
                print(f"Warning: Unable to read image at {image_path}. Skipping...")
                continue

            barcode_data["image"] = image_path

            for idx, region in enumerate(regions):
                try:
                    x, y, w, h = region
                    roi = image[y:y + h, x:x + w]
                    decoded_objects = decode(roi)

                    if decoded_objects:
                        for obj in decoded_objects:
                            barcode_data[f"barcode_{idx + 1}"] = {  # NOQA
                                "data": obj.data.decode("utf-8"), # NOQA
                                "type": obj.type
                            }
                    else:
                        barcode_data[f"barcode_{idx + 1}"] = "No barcode detected"

                except Exception as e:
                    print(f"Error processing region {idx + 1} in {image_path}: {e}")

        return barcode_data

    except ValueError as ve:
        print(ve)
    except Exception as e:
        print(f"Unexpected error while decoding barcodes: {e}")
    return {}


def extract_barcodes_from_pdf(pdf_path):
    """Convert PDF to images, extract barcodes, and clean up images."""
    try:
        image_paths = convert_pdf_to_images(pdf_path)
        barcodes = decode_barcodes_from_images(image_paths)

        shutil.rmtree(OUTPUT_FOLDER, ignore_errors=True)  # Cleanup after processing

        if not barcodes:
            print("No barcodes found in the PDF.")

        return barcodes

    except Exception as e:
        print(f"Unexpected error while extracting barcodes from PDF: {e}")
    return {}


if __name__ == "__main__":
    pdf_path = "../task/test_task.pdf"

    if not os.path.exists(pdf_path):
        print(f"Error: PDF file '{pdf_path}' does not exist.")
    else:
        barcode_data = extract_barcodes_from_pdf(pdf_path)
        pretty_print(barcode_data)
