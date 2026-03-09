# import fitz  # PyMuPDF
# import re
# import os
# import time
# from concurrent.futures import ProcessPoolExecutor, as_completed

# def process_single_pdf(input_path, base_output_folder):
#     """
#     Optimized Worker: Splits a single PDF into sub-folders based on Account No.
#     """
#     try:
#         file_name = os.path.splitext(os.path.basename(input_path))[0]
#         save_dir = os.path.join(base_output_folder, file_name)
        
#         if not os.path.exists(save_dir):
#             os.makedirs(save_dir, exist_ok=True)

#         doc = fitz.open(input_path)
#         current_acc_no = None
#         start_page = 0
#         extracted_count = 0
#         total_pages = len(doc)

#         for page_num in range(total_pages):
#             page = doc[page_num]
#             # Fast text extraction
#             text = page.get_text()

#             if "Account No" in text:
#                 if current_acc_no is not None:
#                     out_name = os.path.join(save_dir, f"Acc_{current_acc_no}.pdf")
#                     new_doc = fitz.open()
#                     new_doc.insert_pdf(doc, from_page=start_page, to_page=page_num - 1)
#                     # Use garbage=3 for smallest file size, or 0 for fastest save
#                     new_doc.save(out_name, garbage=0)
#                     new_doc.close()
#                     extracted_count += 1

#                 match = re.search(r"Account\s*No\s*:\s*([0-9A-Za-z]+)", text)
#                 current_acc_no = match.group(1) if match else f"UNKNOWN_{page_num}"
#                 start_page = page_num

#         # Save final chunk
#         if current_acc_no is not None:
#             out_name = os.path.join(save_dir, f"Acc_{current_acc_no}.pdf")
#             new_doc = fitz.open()
#             new_doc.insert_pdf(doc, from_page=start_page, to_page=total_pages - 1)
#             new_doc.save(out_name, garbage=0)
#             new_doc.close()
#             extracted_count += 1

#         doc.close()
#         return f"DONE: {file_name} ({extracted_count} splits)"
#     except Exception as e:
#         return f"FAIL: {input_path} | {str(e)}"

# def batch_process_folder(input_folder, output_root):
#     start_time = time.perf_counter()
    
#     # Filter only PDF files
#     pdf_files = [
#         os.path.join(input_folder, f) 
#         for f in os.listdir(input_folder) 
#         if f.lower().endswith('.pdf')
#     ]

#     if not pdf_files:
#         print("No PDF files found.")
#         return

#     print(f"Processing {len(pdf_files)} files using all CPU cores...")

#     # We don't specify max_workers so it defaults to the number of processors
#     with ProcessPoolExecutor() as executor:
#         # Submit all tasks
#         future_to_pdf = {executor.submit(process_single_pdf, pdf, output_root): pdf for pdf in pdf_files}
        
#         for future in as_completed(future_to_pdf):
#             print(future.result())

#     duration = time.perf_counter() - start_time
#     print(f"\n--- COMPLETED ---")
#     print(f"Total Time: {duration:.2f} seconds")

# if __name__ == "__main__":
#     # Use 'r' before the string to handle Windows backslashes correctly
#     SOURCE_DIR = r"E:\AI-ML-at-Cactus-Creatives\demofiles"
#     EXPORT_DIR = r"E:\AI-ML-at-Cactus-Creatives\sep_file"
    
#     batch_process_folder(SOURCE_DIR, EXPORT_DIR)



import fitz
import re
import os
import time
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import Manager

def process_single_pdf(input_path, base_output_folder, completed_list):
    """
    Worker: Processes PDF and appends the filename to the shared list upon success.
    """
    try:
        file_name = os.path.splitext(os.path.basename(input_path))[0]
        save_dir = os.path.join(base_output_folder, file_name)
        os.makedirs(save_dir, exist_ok=True)

        doc = fitz.open(input_path)
        current_acc_no = None
        start_page = 0
        total_pages = len(doc)

        for page_num in range(total_pages):
            page = doc[page_num]
            text = page.get_text()

            if "Account No" in text:
                if current_acc_no is not None:
                    out_name = os.path.join(save_dir, f"Acc_{current_acc_no}.pdf")
                    new_doc = fitz.open()
                    new_doc.insert_pdf(doc, from_page=start_page, to_page=page_num - 1)
                    new_doc.save(out_name, garbage=0)
                    new_doc.close()

                match = re.search(r"Account\s*No\s*:\s*([0-9A-Za-z]+)", text)
                current_acc_no = match.group(1) if match else f"UNKNOWN_{page_num}"
                start_page = page_num

        if current_acc_no is not None:
            out_name = os.path.join(save_dir, f"Acc_{current_acc_no}.pdf")
            new_doc = fitz.open()
            new_doc.insert_pdf(doc, from_page=start_page, to_page=total_pages - 1)
            new_doc.save(out_name, garbage=0)
            new_doc.close()

        doc.close()
        
        # Insert filename into the blank list (Records)
        completed_list.append(file_name)
        return True
    except Exception:
        return False

def batch_process_folder(input_folder, output_root):
    # Start the clock
    overall_start_time = time.perf_counter()
    
    with Manager() as manager:
        completed_records = manager.list() # Your blank records list
        
        pdf_files = [
            os.path.join(input_folder, f) 
            for f in os.listdir(input_folder) 
            if f.lower().endswith('.pdf')
        ]
        
        total_files = len(pdf_files)
        print(f"--- Process Started for {total_files} Files ---")

        with ProcessPoolExecutor() as executor:
            # Kick off all processing jobs ASAP
            futures = [
                executor.submit(process_single_pdf, pdf, output_root, completed_records) 
                for pdf in pdf_files
            ]
            
            last_reported_count = 0
            
            # Monitoring loop: Runs while there are unfinished tasks
            while last_reported_count < total_files:
                time.sleep(5)
                
                # Check current status from the shared records list
                current_snapshot = list(completed_records)
                current_count = len(current_snapshot)
                
                # Identify which specific files finished in the last 5 seconds
                newly_sliced = current_snapshot[last_reported_count:]
                
                print(f"[{time.strftime('%H:%M:%S')}] Total Complated: {current_count}/{total_files}")
                if newly_sliced:
                    print(f" > Newly Sliced: {newly_sliced}")
                
                last_reported_count = current_count
                
                # Safety break: If all jobs are actually finished, stop the sleep loop
                if all(f.done() for f in futures):
                    break

    # Calculate Total Time
    total_duration = time.perf_counter() - overall_start_time
    
    print("\n" + "="*40)
    print(f"--- ALL PROCESSES COMPLETE ---")
    print(f"Total Files Processed: {total_files}")
    print(f"Total Execution Time: {total_duration:.2f} seconds")
    print("="*40)

if __name__ == "__main__":
    # Your specific directories
    SOURCE_DIR = r"E:\AI-ML-at-Cactus-Creatives\demofiles"
    EXPORT_DIR = r"E:\AI-ML-at-Cactus-Creatives\sep_file"
    
    batch_process_folder(SOURCE_DIR, EXPORT_DIR)