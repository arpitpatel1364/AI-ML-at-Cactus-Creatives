# import os
# import re
# import time
# from pypdf import PdfReader, PdfWriter

# input_pdf = input("enter the pdf file name: ")
# output_folder = input("enter the output save folder name: ")

# if not os.path.exists(output_folder):
#     os.makedirs(output_folder)

# def safe_filename_part(value: str) -> str:
#     # Windows invalid filename chars: < > : " / \ | ? *
#     invalid = '<>:"/\\|?*'
#     cleaned = "".join("_" if c in invalid else c for c in str(value))
#     cleaned = cleaned.strip().strip(".")
#     return cleaned or "UNKNOWN"

# start_time = time.perf_counter()
# reader = PdfReader(input_pdf)

# current_writer = None
# current_acc_no = None
# start_page_index = None

# for i, page in enumerate(reader.pages):
#     text = page.extract_text() or ""

#     if "Account No" in text:
#         # If we were already collecting pages for a previous account,
#         # finish and save that PDF before starting a new one.
#         if current_writer is not None and current_acc_no is not None:
#             file_path = os.path.join(output_folder, f"Account No {safe_filename_part(current_acc_no)}.pdf")
#             with open(file_path, "wb") as f:
#                 current_writer.write(f)
#             print(f"Processed account {current_acc_no} (pages {start_page_index + 1}-{i}) -> {file_path}")

#         # Start a new writer for the new Account No section
#         match = re.search(r"Account\s*No\s*:\s*([0-9A-Za-z]+)", text)
#         if match:
#             acc_no = match.group(1)
#         else:
#             acc_no = "UNKNOWN"

#         current_writer = PdfWriter()
#         current_acc_no = acc_no
#         start_page_index = i

#     # If we are in an account section, keep adding pages
#     if current_writer is not None:
#         current_writer.add_page(page)

# # After the loop, save the last collected account (if any)
# if current_writer is not None and current_acc_no is not None:
#     file_path = os.path.join(output_folder, f"Account No {safe_filename_part(current_acc_no)}.pdf")
#     with open(file_path, "wb") as f:
#         current_writer.write(f)
#     end_page = len(reader.pages)
#     print(f"Processed account {current_acc_no} (pages {start_page_index + 1}-{end_page}) -> {file_path}")

# elapsed_s = time.perf_counter() - start_time
# print(f"Total runtime: {elapsed_s:.2f} seconds")


import fitz  # This is PyMuPDF
import re
import os
import time

def split_with_pymupdf(input_file, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        
    start_time = time.perf_counter()
    
    # Open the document
    doc = fitz.open(input_file)
    
    current_acc_no = None
    start_page = 0
    
    print(f"Processing {len(doc)} pages...")

    for page_num in range(len(doc)):
        page = doc[page_num]
        # PyMuPDF text extraction is nearly instantaneous
        text = page.get_text()

        if "Account No" in text:
            # Save the previous account if it exists
            if current_acc_no is not None:
                new_doc = fitz.open() # Create new empty PDF
                new_doc.insert_pdf(doc, from_page=start_page, to_page=page_num - 1)
                new_doc.save(os.path.join(output_folder, f"Acc_{current_acc_no}.pdf"))
                new_doc.close()

            # Find new account number
            match = re.search(r"Account\s*No\s*:\s*([0-9A-Za-z]+)", text)
            current_acc_no = match.group(1) if match else "UNKNOWN"
            start_page = page_num

    # Save the last account
    if current_acc_no is not None:
        new_doc = fitz.open()
        new_doc.insert_pdf(doc, from_page=start_page, to_page=len(doc) - 1)
        new_doc.save(os.path.join(output_folder, f"Acc_{current_acc_no}.pdf"))
        new_doc.close()

    doc.close()
    print(f" Finished in {time.perf_counter() - start_time:.2f} seconds")

# Usage
split_with_pymupdf("demo.pdf", "sep_file")