import fitz
import re


def clean_text(text):
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def extract_text_by_page(uploaded_file):
    file_bytes = uploaded_file.getvalue()
    doc = fitz.open(stream=file_bytes, filetype="pdf")

    pages_text = []

    for i, page in enumerate(doc):
        raw_text = page.get_text()
        cleaned = clean_text(raw_text)

        pages_text.append({
            "page": i + 1,
            "raw_text" : raw_text,
            "cleaned_text": cleaned
        })

    return pages_text


def extract_section(text, section_name):
    pattern = rf"{section_name}(.*?)(\d+\)\s+[A-Z]|$)"

    match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)

    if match:
        return match.group(1).strip()

    return None


def extract_key_values(section_text):
    data = {}

    pattern = r"([A-Za-z ]+)\s*:\s*(.+)"
    matches = re.findall(pattern, section_text)

    for key, value in matches:
        value = value.strip()
        value = value.replace("On ", "")
        data[key.strip()] = value

    return data

def extract_fields(pages_text):
    results = {}

    full_text = "\n".join([p["raw_text"] for p in pages_text])

    # extract section from FULL text
    loss_section = extract_section(full_text, "Loss Particulars")

    if loss_section:
        loss_data = extract_key_values(loss_section)
        results["loss_particulars"] = loss_data

    return results