from ocr_extractor import extract_data_from_pdf

def test_extraction():
    # Test case 1: PDF with two owners
    pdf_path_1 = 'files/3380_1.pdf'
    extracted_data_1 = extract_data_from_pdf(pdf_path_1)
    assert len(extracted_data_1['imaoci_prava']) == 2, f"Owner list length mismatch for 3380_1.pdf: {len(extracted_data_1['imaoci_prava'])}"
    print("Test case 1 passed.")

    # Test case 2: PDF with one owner
    pdf_path_2 = 'files/2134_198.pdf'
    extracted_data_2 = extract_data_from_pdf(pdf_path_2)
    assert len(extracted_data_2['imaoci_prava']) == 1, f"Owner list length mismatch for 2134_198.pdf: {len(extracted_data_2['imaoci_prava'])}"
    print("Test case 2 passed.")

if __name__ == "__main__":
    test_extraction()
