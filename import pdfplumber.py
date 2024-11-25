import pdfplumber

# Function to extract text from multiple PDF files and save it to a text file
def extract_text_from_pdfs(pdf_paths, output_dir):
    all_text = ""  # Initialize a variable to hold all extracted text
    for index, pdf_path in enumerate(pdf_paths, start=1):  # Start enumeration from 1
        with pdfplumber.open(pdf_path) as pdf:
            all_text += f"Application {index}:\n"  # Add title for each application
            for page in pdf.pages:
                all_text += page.extract_text() + '\n'
    
    # Create a single text file for all PDFs
    output_txt_path = f"{output_dir}/combined_output.txt"
    with open(output_txt_path, 'w') as file:
        file.write(all_text)
    print(f"Extracted text has been saved to {output_txt_path}")

# Example usage
pdf_paths = [
    '/Users/monova/Downloads/finalapps/app1.pdf',
    '//Users/monova/Downloads/finalapps/app2.pdf',
    '/Users/monova/Downloads/finalapps/app3.pdf',
    '/Users/monova/Downloads/finalapps/app4.pdf',
    '/Users/monova/Downloads/finalapps/app5.pdf',
    '/Users/monova/Downloads/finalapps/app6.pdf',
    '/Users/monova/Downloads/finalapps/app7.pdf',
    '/Users/monova/Downloads/finalapps/app8.pdf',
    '/Users/monova/Downloads/finalapps/app9.pdf',
    '/Users/monova/Downloads/finalapps/app10.pdf',
    '/Users/monova/Downloads/finalapps/app11.pdf',
    '/Users/monova/Downloads/finalapps/app12.pdf',
    '/Users/monova/Downloads/finalapps/app13.pdf',
    '/Users/monova/Downloads/finalapps/app14.pdf',
]
output_dir = '/Users/monova/Downloads/finalapps/'  # Directory to save text files
extract_text_from_pdfs(pdf_paths, output_dir)


