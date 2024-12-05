import pytesseract
from pdf2image import convert_from_path
import re

def extract_data_from_pdf(pdf_path):
    # Convert PDF to images
    images = convert_from_path(pdf_path, dpi=400)

    # Perform OCR on each page and combine text
    text = ""
    for img in images:
        page_text = pytesseract.image_to_string(img, lang='srp')
        # Preprocess text to handle common OCR issues
        page_text = re.sub(r'[\n\r]+', ' ', page_text)  # Replace line breaks with a space
        page_text = re.sub(r'\s+', ' ', page_text)  # Collapse multiple spaces into one
        text += page_text

    # Define refined patterns for each data point
    patterns = {
        "nepokretnost_id": r"Подаци о непокретности\s?([a-zA-Z0-9-]+)",
        "maticni_broj_opstine": r"Матични број општине:\s?(\d+)",
        "opstina": r"Општина:\s?([\w ]+)",
        "maticni_broj_ko": r"Матични број катастарске општине:\s?(\d+)",
        "katastarska_opstina": r"Катастарска општина:\s?([\w ]+)",
        "datum_azurnosti": r"Датум ажурности:\s?([\d. :]+)",
        "sluzba": r"Служба:\s?([\w ]+)",
        "potre_ulica": r"Потес / Улица:\s?([\w ]+)",
        "broj_parcele": r"Број парцеле:\s?([\w/]+)",
        "povrsina": r"Површина.*?:\s?(\d+)",
        "broj_lista_nepokretnosti": r"Број листа непокретности:\s?(\d+)",
        "broj_dela": r"Број дела:\s?(\d+)",
        "vrsta_zemljista": r"Врста земљишта:\s?([\w ]+)",
        "kultura": r"Култура:\s?([\w ]+)",
        "imaoci_prava": r"Назив:\s?([\w \(\)]+)\s*Лице уписано са матичним бројем:\s?(ДА|НЕ)\s*Врста права:\s?([\w ]+)\s*Облик својине:\s?([\w ]+)\s*Удео:\s?([\d/]+)"
    }

    # Extract each field using the patterns
    extracted_data = {}
    for key, pattern in patterns.items():
        matches = re.findall(pattern, text)
        extracted_data[key] = matches if matches else []

    # Format 'imaoci_prava' as a list of dictionaries
    imaoci_prava = []
    for match in extracted_data['imaoci_prava']:
        if len(match) == 5:  # Ensure all fields are present in each match
            imaoci_prava.append({
                "Naziv": match[0].strip(),
                "Lice_upisano_sa_maticnim_brojem": match[1].strip(),
                "Vrsta_prava": match[2].strip(),
                "Oblik_svojine": match[3].strip(),
                "Udeo": match[4].strip()
            })
    extracted_data['imaoci_prava'] = imaoci_prava

    return extracted_data
