import pdfplumber
import sys

def extract_arabic_text(pdf_path):
    """
    Extract text from a PDF file with proper Arabic text handling
    """
    try:
        with pdfplumber.open(pdf_path) as pdf:
            all_text = []
            for page in pdf.pages:
                # Extract text with proper encoding
                text = page.extract_text()
                if text:
                    all_text.append(text)
                
            if not all_text:
                print("No text was extracted from the PDF. The file might be:")
                print("- An image-based PDF (scanned document)")
                print("- Protected/encrypted")
                print("- Corrupted")
                return None
                
            # Join all pages with proper text direction handling
            complete_text = '\n\n'.join(all_text)
            
            # Ensure proper encoding for Arabic text
            return complete_text.encode('utf-8').decode('utf-8')
            
    except Exception as e:
        print(f"Error processing PDF: {str(e)}")
        return None

def main():
    if len(sys.argv) != 2:
        print("Usage: python arabic_pdf_extractor.py <path_to_pdf>")
        sys.exit(1)
        
    pdf_path = sys.argv[1]
    extracted_text = extract_arabic_text(pdf_path)
    
    if extracted_text:
        print("\nExtracted text:")
        print("-" * 50)
        print(extracted_text)
        print("-" * 50)

if __name__ == "__main__":
    main()
