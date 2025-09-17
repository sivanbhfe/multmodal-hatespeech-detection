import PyPDF2
import pandas as pd
from collections import Counter
import re
import os

from indic_transliteration.sanscript_cli.help_text import output_file
from pdf2image import convert_from_path
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    for subfolder in os.listdir(root_folder):
        subfolder_path = os.path.join(root_folder, subfolder)

        if os.path.isdir(subfolder_path):
            print(f"📂 Processing subfolder: {subfolder}")

            all_text = []
            breaking_count = 0
            breaking_count_stop = 50
            # Loop through PDFs inside this subfolder
            for filename in os.listdir(subfolder_path):

                if filename.lower().endswith(".pdf"):
                    pdf_path = os.path.join(subfolder_path, filename)
                    print(f"   📝 Processing PDF: {filename}")

                    # Convert PDF to images
                    pages = convert_from_path(pdf_path, dpi=300)

                    for i, page in enumerate(pages, start=1):
                        # OCR (Tamil)
                        text = pytesseract.image_to_string(page, lang="tam")
                        all_text.append(text)
                breaking_count = breaking_count + 1
                print(breaking_count)
                if breaking_count >=breaking_count_stop:
                   break

            # Save text for this subfolder
            output_file = os.path.join(output_folder, f"{subfolder}.txt")
            with open(output_file, "w", encoding="utf-8") as f:
                f.write("\n".join(all_text))

            print(f"✅ Saved {output_file}")

# Function to clean and count words
def get_word_counts(output_folder,output_dict_file):
    all_words = []
    for filename in os.listdir(output_folder):
        if filename.lower().endswith(".txt"):
            file_path = os.path.join(output_folder, filename)
            print(f"📖 Reading {filename}")

            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read().lower()

                # Extract words (Tamil/English safe regex)
                words = re.findall(r'[\w\u0B80-\u0BFF]+', text)
                all_words.extend(words)
    # Count occurrences of all words
    word_counts = Counter(all_words)

    # Create DataFrame
    df = pd.DataFrame(word_counts.items(), columns=["Word", "Count"])
    df = df.sort_values(by="Count", ascending=False).reset_index(drop=True)

    print(df.head(20))


    with open(output_dict_file, "w", encoding="utf-8") as f:
        for _, row in df.iterrows():
            f.write(f"{row['Word']} {row['Count']}\n")

    print(f"✅ SymSpell dictionary saved to {output_dict_file}")

# Main
root_folder = "D:\\AI_Doctorate\\HateSpeechModel_Draft\\MultimodelHateSpeechDetection_related\\corpus_source\\pdf"  # Replace with your file path
output_folder = "D:\\AI_Doctorate\\HateSpeechModel_Draft\\MultimodelHateSpeechDetection_related\\corpus_source\\txt"
output_dict_file = "D:\\AI_Doctorate\HateSpeechModel_Draft\\MultimodelHateSpeechDetection_related\\corpus_source\\symspell_dictionary.txt"


extract_text_from_pdf(root_folder)
word_counts = get_word_counts(output_folder,output_dict_file)

# Convert to DataFrame
# df = pd.DataFrame(word_counts.items(), columns=["Word", "Occurrence"])
# df = df.sort_values(by="Occurrence", ascending=False).reset_index(drop=True)

# print(df.head(20))  # Show top 20