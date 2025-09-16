import fitz  # PyMuPDF
import os
import json
from pathlib import Path


# function to extract text from a PDF file
def extract_text_from_pdf(pdf_path):
    """
    Extracts all text (including from tables & multi-columns) from a PDF file.
    Ignores plots/graphics, since they usually don't contain text.
    Returns a dictionary with page numbers as keys and extracted text as values.
    """
    doc = fitz.open(pdf_path)
    all_text = {}

    for page_num, page in enumerate(doc, start=1):
        # Extract raw text from page
        text = page.get_text("text")  # layout-aware extraction

        if not text.strip():  # fallback if text empty (maybe scanned)
            text = page.get_text("blocks")  # another strategy
            text = " ".join([block[4] for block in text if isinstance(block[4], str)])

        all_text[page_num] = text

    doc.close()
    return all_text


# Function save the extracted text to a .txt file
def save_text_to_file(all_text, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        for page_num, text in all_text.items():
            f.write(f"\n--- Page {page_num} ---\n{text}\n")
    print(f"Extracted text saved to: {output_path}")


# Function to count keywords in the extracted text
def search_keywords_in_text(all_text, keywords):
    """
    Searches for keywords in the extracted text
    Returns a dictionary with keyword matches and their counts
    """
    result = {}

    for keyword in keywords:
        keyword_lower = keyword.lower()
        count_total = 0
        pages_found = []

        for page_num, text in all_text.items():
            count = text.lower().count(keyword_lower)
            if count > 0:
                count_total += count
                # Record the page number where the keyword was found
                # page_num = int(page_num) - 1  # if the document has a page 0
                page_num = int(page_num)  # if the document starts at page 1
                pages_found.append(page_num)

        if count_total > 0:
            result[keyword] = {"count": count_total, "pages": pages_found}

    return result


def get_default_keywords():
    """
    Returns a list of default keywords to search for in the PDF text."""
    keywords = [
        "discrimination",
        "racism",
        "structural factors",
        "bias",
        "equity",
        "health equity",
        # Racial/Ethnic groups
        "white",
        "black",
        "asian",
        "hispanic",
        "latino",
        "latinx",
        "native american",
        "alaska native",
        "pacific islander",
        "middle eastern",
        "multiracial",
        # Other demographic or social groups
        "rural health",
        "disabled",
        "low ses",
        "low socioeconomic status",
        # Gender & Sexual identity
        "transgender",
        "lesbian",
        "gay",
        "pan gender",
        "poly gender",
        "sex",
        "diversity"
    ]
    return keywords
    # return ["Discrimination", "neutrophil", "phagocytosis"]


def process_pdf_with_keywords(pdf_path, keywords):
    """
    Complete workflow: extract text from PDF and search for keywords
    Returns tuple: (extracted_text_dict, keyword_results_dict)
    """
    # Step 1: Extract text from PDF
    pdf_text = extract_text_from_pdf(pdf_path)

    # Step 2: Search for keywords
    keyword_results = search_keywords_in_text(pdf_text, keywords)

    return pdf_text, keyword_results


# Saving keywords in a JSON file
def get_keywords_file_path():
    """
    Get the path for the keywords file in user's home directory
    """
    return Path.home() / ".smart_search_keywords.json"


def save_keywords(keywords_list):
    """
    Save keywords list to a single file
    """
    try:
        filepath = get_keywords_file_path()
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(keywords_list, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        return False


def load_keywords():
    """
    Load keywords from file, return default if file doesn't exist
    """
    try:
        filepath = get_keywords_file_path()
        if filepath.exists():
            with open(filepath, "r", encoding="utf-8") as f:
                return json.load(f)
    except:
        pass

    # Return default keywords if file doesn't exist or can't be loaded
    return get_default_keywords()


## ======================================================
# Example Usage

if __name__ == "__main__":

    pdf_file = "sample-application.pdf"
    keywords = ["cytotoxicity", "neutrophil", "phagocytosis"]

    print("Smart Search Backend - Example Usage")
    print("=" * 50)

    # Check if the PDF file exists
    if os.path.exists(pdf_file):
        # Extract text from PDF
        pdf_text = extract_text_from_pdf(pdf_file)
        print(f"Extracted text from {len(pdf_text)} pages")

        # Save extracted text to a file
        output_file = "extracted_text.txt"
        save_text_to_file(pdf_text, output_file)

        # Search for keywords
        keyword_results = search_keywords_in_text(pdf_text, keywords)

        # Print keyword search results
        if keyword_results:
            print("Keyword Matches Found:")
            for keyword, info in keyword_results.items():
                pages = ", ".join(map(str, info["pages"]))
                print(f"'{keyword}': found {info["count"]} times on pages: {pages}")
        else:
            print("No keyword matches found.")
