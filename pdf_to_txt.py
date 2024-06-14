import os
import fitz  # PyMuPDF
import pytesseract
from PIL import Image

def extract_text_from_pdfs(directory):
    for filename in os.listdir(directory):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(directory, filename)
            txt_path = os.path.join(directory, filename.replace('.pdf', '.txt'))

            try:
                pdf_document = fitz.open(pdf_path)
                text = ''

                for page_num in range(len(pdf_document)):
                    page = pdf_document.load_page(page_num)
                    text_page = page.get_text()

                    if text_page.strip():
                        text += text_page + '\n'
                    else:
                        try:
                            # Renderize a página para um pixmap
                            pix = page.get_pixmap()
                            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                            ocr_text = pytesseract.image_to_string(img)
                            if ocr_text.strip():
                                text += ocr_text + '\n'
                        except fitz.fitz.Error as e:
                            print(f"Erro MuPDF na página {page_num} do arquivo {filename}: {e}")
                        except Exception as e:
                            print(f"Erro ao processar imagem na página {page_num} do arquivo {filename}: {e}")

                if text.strip():
                    with open(txt_path, 'w', encoding='utf-8') as txt_file:
                        txt_file.write(text)
                else:
                    print(f"Nenhum texto extraído do arquivo {filename}")

            except Exception as e:
                print(f"Erro ao processar o arquivo {filename}: {e}")

if __name__ == "__main__":
    current_directory = os.path.dirname(os.path.abspath(__file__))
    extract_text_from_pdfs(current_directory)
