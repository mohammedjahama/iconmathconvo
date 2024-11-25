import pdfplumber

# Function to extract text from a PDF file and save it to a text file
def extract_text_from_pdf(pdf_path, output_txt_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ''
        for page in pdf.pages:
            text += page.extract_text() + '\n'
    
    with open(output_txt_path, 'w') as file:
        file.write(text)

# Example usage
pdf_path = '/Users/monova/Downloads/app1.pdf' '/Users/monova/Downloads/app2.pdf' '/Users/monova/Downloads/app3.pdf' '/Users/monova/Downloads/app4.pdf'
output_txt_path = '/Users/monova/Downloads/apptext1.txt'
extract_text_from_pdf(pdf_path, output_txt_path)
print(f"Extracted text has been saved to {output_txt_path}")


