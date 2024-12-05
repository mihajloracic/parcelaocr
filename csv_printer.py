import os
import csv

from ocr_extractor import extract_data_from_pdf


def process_pdfs_to_csv(folder_path, output_csv_path):
    # List all PDF files in the folder
    pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]

    # Define the CSV columns
    csv_columns = [
        "nepokretnost_id", "maticni_broj_opstine", "opstina",
        "maticni_broj_ko", "katastarska_opstina", "datum_azurnosti",
        "sluzba", "potre_ulica", "broj_parcele", "povrsina",
        "broj_lista_nepokretnosti", "broj_dela", "vrsta_zemljista",
        "kultura", "imaoci_prava", "njiva"
    ]

    # Prepare to write the CSV file
    with open(output_csv_path, mode='w', newline='', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=csv_columns)
        writer.writeheader()

        # Process each PDF file
        for pdf_file in pdf_files:
            pdf_path = os.path.join(folder_path, pdf_file)
            extracted_data = extract_data_from_pdf(pdf_path)

            # Process `imaoci_prava` (assuming there's only one entry)
            imaoci_prava_list = extracted_data.get('imaoci_prava', [])
            imaoci_prava_str = ""
            if imaoci_prava_list:
                imaoci_prava = imaoci_prava_list[0]  # Take the first entry
                imaoci_prava_str = f"Naziv: {imaoci_prava['Naziv']}, " \
                                   f"Lice_upisano_sa_maticnim_brojem: {imaoci_prava['Lice_upisano_sa_maticnim_brojem']}, " \
                                   f"Vrsta_prava: {imaoci_prava['Vrsta_prava']}, " \
                                   f"Oblik_svojine: {imaoci_prava['Oblik_svojine']}, " \
                                   f"Udeo: {imaoci_prava['Udeo']}"
                print(f"Imaoci prava for {pdf_file}: {imaoci_prava_str}")

            # Add all data to the CSV row
            csv_row = {
                "nepokretnost_id": ', '.join(extracted_data.get("nepokretnost_id", [])),
                "maticni_broj_opstine": ', '.join(extracted_data.get("maticni_broj_opstine", [])),
                "opstina": ', '.join(extracted_data.get("opstina", [])),
                "maticni_broj_ko": ', '.join(extracted_data.get("maticni_broj_ko", [])),
                "katastarska_opstina": ', '.join(extracted_data.get("katastarska_opstina", [])),
                "datum_azurnosti": ', '.join(extracted_data.get("datum_azurnosti", [])),
                "sluzba": ', '.join(extracted_data.get("sluzba", [])),
                "potre_ulica": ', '.join(extracted_data.get("potre_ulica", [])),
                "broj_parcele": ', '.join(extracted_data.get("broj_parcele", [])),
                "povrsina": ', '.join(extracted_data.get("povrsina", [])),
                "broj_lista_nepokretnosti": ', '.join(extracted_data.get("broj_lista_nepokretnosti", [])),
                "broj_dela": ', '.join(extracted_data.get("broj_dela", [])),
                "vrsta_zemljista": ', '.join(extracted_data.get("vrsta_zemljista", [])),
                "kultura": ', '.join(extracted_data.get("kultura", [])),
                "imaoci_prava": imaoci_prava_str,
                "njiva": "Да" if "њива" in extracted_data.get("vrsta_zemљишта", []) else "Не"
            }

            writer.writerow(csv_row)


# Define paths
folder_path = 'files'  # Path to the folder containing PDF files
output_csv_path = 'extracted_data.csv'  # Path for the output CSV file

# Call the function to process PDFs and create the CSV
process_pdfs_to_csv(folder_path, output_csv_path)
