import fitz  # PyMuPDF
import re
import os
import time
from concurrent.futures import ProcessPoolExecutor, as_completed

def process_single_pdf(input_path, base_output_folder):
    """
    Worker function: Handles one specific PDF file, 
    scans it, and splits it into a dedicated sub-folder.
    """
    file_name = os.path.splitext(os.path.basename(input_path))[0]
    # Create a specific folder for this PDF's results
    save_dir = os.path.join(base_output_folder, file_name)
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    try:
        doc = fitz.open(input_path)
        current_acc_no = None
        start_page = 0
        extracted_count = 0

        for page_num in range(len(doc)):
            page = doc[page_num]
            text = page.get_text()

            if "Account No" in text:
                if current_acc_no is not None:
                    # Save the range found so far
                    out_name = os.path.join(save_dir, f"Acc_{current_acc_no}.pdf")
                    new_doc = fitz.open()
                    new_doc.insert_pdf(doc, from_page=start_page, to_page=page_num - 1)
                    new_doc.save(out_name)
                    new_doc.close()
                    extracted_count += 1

                # Regex to find the new account number
                match = re.search(r"Account\s*No\s*:\s*([0-9A-Za-z]+)", text)
                current_acc_no = match.group(1) if match else f"UNKNOWN_{page_num}"
                start_page = page_num

        # Save the very last chunk of the file
        if current_acc_no is not None:
            out_name = os.path.join(save_dir, f"Acc_{current_acc_no}.pdf")
            new_doc = fitz.open()
            new_doc.insert_pdf(doc, from_page=start_page, to_page=len(doc) - 1)
            new_doc.save(out_name)
            new_doc.close()
            extracted_count += 1

        doc.close()
        return f"SUCCESS: {file_name} -> {extracted_count} accounts split."
    except Exception as e:
        return f"ERROR processing {file_name}: {str(e)}"

def batch_process_folder(input_folder, output_root):
    start_time = time.perf_counter()
    
    # Gather all PDF files from the input directory
    pdf_files = [
        os.path.join(input_folder, f) 
        for f in os.listdir(input_folder) 
        if f.lower().endswith('.pdf')
    ]

    print(f"Found {len(pdf_files)} PDFs. Starting batch processing...")

    # Using ProcessPoolExecutor to handle multiple PDFs at once
    # This will automatically use the number of cores available on your machine
    with ProcessPoolExecutor() as executor:
        # Submit all PDF tasks to the pool
        futures = [executor.submit(process_single_pdf, pdf, output_root) for pdf in pdf_files]
        
        for future in as_completed(futures):
            print(future.result())

    total_time = time.perf_counter() - start_time
    print(f"\n--- ALL PROCESSES COMPLETE ---")
    print(f"Total time for {len(pdf_files)} files: {total_time:.2f} seconds")

if __name__ == "__main__":
    # CONFIGURATION
    SOURCE_DIR = "E:\AI-ML-at-Cactus-Creatives\demofiles"   # Folder containing your 50-60 PDFs
    EXPORT_DIR = "E:\AI-ML-at-Cactus-Creatives\sep_file" # Where the sub-folders will be created
    
    batch_process_folder(SOURCE_DIR, EXPORT_DIR)