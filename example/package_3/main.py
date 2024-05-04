import argparse
import subprocess
import sys

def convert_pdf_to_txt(pdf_file, output_txt_file=None):
    if output_txt_file is None:
        output_txt_file = pdf_file.replace('.pdf', '.txt')

    # Using subprocess to call pdftotext
    result = subprocess.run(['pdftotext', pdf_file, output_txt_file], capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"Failed to convert PDF: {result.stderr}", file=sys.stderr)
        sys.exit(1)
    
    print(f"Successfully converted '{pdf_file}' to '{output_txt_file}'")

def main():
    parser = argparse.ArgumentParser(description="Convert PDF to Text")
    parser.add_argument("pdf_file", type=str, help="The path to the PDF file to convert.")
    parser.add_argument("-o", "--output", type=str, help="The path to save the text output. Optional.")
    
    args = parser.parse_args()
    
    convert_pdf_to_txt(args.pdf_file, args.output)

if __name__ == "__main__":
    main()
