import pdfplumber

def extract_arabic_text(pdf_path):
    try:
        with pdfplumber.open(pdf_path) as pdf:
            # Extract text from first page
            first_page = pdf.pages[0]
            text = first_page.extract_text()
            print("Extracted text:")
            print(text)
            return text
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return None

# Test with a PDF file containing Arabic text
if __name__ == "__main__":
    # Replace with path to your Arabic PDF
    pdf_path = "sample_arabic.pdf"
    extract_arabic_text(pdf_path)
