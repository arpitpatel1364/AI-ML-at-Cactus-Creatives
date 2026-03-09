import fitz  # PyMuPDF
import re
import os
import sqlite3
import shutil
from datetime import datetime

# CONFIGURATION: Define roles and keywords
SKILL_SETS = {
    "backend": ["python", "django", "flask", "fastapi", "sql", "sqlite", "postgresql", "docker", "rest api", "git"],
    "data_science": ["python", "pandas", "numpy", "scikit-learn", "tensorflow", "pytorch", "machine learning", "nlp"],
    "frontend": ["javascript", "react", "angular", "vue", "html", "css", "typescript", "tailwind", "bootstrap"]
}

class HighPerfATS:
    def __init__(self):
        # Database path directly assigned
        self.db_path = r"ATS\ats_database.db"
        
        # Ensure the ATS base folder exists
        if not os.path.exists("ATS"):
            os.makedirs("ATS")
            
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        self._setup_db()
        
    def _setup_db(self):
        # SCHEMA CHANGED: We now store 'raw_text' instead of a specific role score.
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS candidates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                email TEXT UNIQUE,
                raw_text TEXT,
                file_path TEXT,
                timestamp DATETIME
            )
        """)
        self.conn.commit()

    # ==========================================
    # FUNCTION 1: JUST READ & SAVE (NO SCORING)
    # ==========================================
    def read_and_save_all(self):
        folder_path = r"ATS\All_resume"
        
        if not os.path.exists(folder_path):
            print(f"❌ Error: Folder '{folder_path}' not found! Create it and add PDFs.")
            return

        print(f"\n--- Reading PDFs from {folder_path} and saving to Database ---")
        
        count = 0
        for filename in os.listdir(folder_path):
            if filename.lower().endswith(".pdf"):
                path = os.path.join(folder_path, filename)
                
                # Extract Text
                text = ""
                try:
                    with fitz.open(path) as doc:
                        for page in doc:
                            text += page.get_text()
                except:
                    continue # Skip broken PDFs

                # Extract Email & Name
                email_match = re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)
                email = email_match.group(0) if email_match else "Unknown"
                lines = [l.strip() for l in text.split('\n') if l.strip()]
                name = lines[0] if lines else "Unknown"
                
                # Save Raw Data to DB
                self.cursor.execute("""
                    INSERT OR REPLACE INTO candidates (name, email, raw_text, file_path, timestamp)
                    VALUES (?, ?, ?, ?, ?)
                """, (name, email, text, path, datetime.now()))
                count += 1
                
        self.conn.commit()
        print(f"✅ Extracted and saved {count} resumes into Database.")

    # ==========================================
    # FUNCTION 2: CALCULATE ATS SCORE & EXPORT TOP 5
    # ==========================================
    def calculate_ats_and_export(self, role_key):
        output_folder = r"ATS\Top_Matches"
        
        # Setup Output Folder
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        else:
            # Clean old files
            for f in os.listdir(output_folder):
                os.remove(os.path.join(output_folder, f))

        # Fetch all raw data from DB
        self.cursor.execute("SELECT name, raw_text, file_path FROM candidates")
        all_candidates = self.cursor.fetchall()
        
        if not all_candidates:
            print("⚠️ No data found in Database! Run Option 1 first.")
            return

        keywords = SKILL_SETS[role_key]
        scored_candidates = []

        # Calculate score on the fly
        for name, raw_text, path in all_candidates:
            text_lower = raw_text.lower() if raw_text else ""
            found_skills = [word for word in keywords if word.lower() in text_lower]
            score = (len(found_skills) / len(keywords)) * 100 if keywords else 0
            
            scored_candidates.append((name, score, path))

        # Sort by score (Descending) and grab Top 5
        scored_candidates.sort(key=lambda x: x[1], reverse=True)
        top_5 = scored_candidates[:5]

        print(f"\n--- Exporting Top 5 {role_key.upper()} Matches to {output_folder} ---")
        
        for i, (name, score, path) in enumerate(top_5):
            # Get the exact old filename (e.g., arpit_resume.pdf)
            old_filename = os.path.basename(path)
            
            # Attach Rank to the front of the old filename
            new_filename = f"Rank_{i+1}_{old_filename}"
            
            shutil.copy(path, os.path.join(output_folder, new_filename))
            print(f"Rank {i+1}: {name} ({score:.0f}%) -> Saved as {new_filename}")


def main():
    ats = HighPerfATS()
    role_list = list(SKILL_SETS.keys())

    print("\n" + "="*40)
    print("      CACTUS CREATIVES - ATS ENGINE")
    print("="*40)
    
    # MAIN MENU
    print("\nSelect Operation:")
    print("1. [INGEST] Read all PDFs and save raw data to Database")
    print("2. [PROCESS] Calculate ATS Scores and Export Top 5")
    op_choice = input("Choice (1/2): ").strip()

    if op_choice == "1":
        ats.read_and_save_all()
        
    elif op_choice == "2":
        print("\nSelect Job Role to Calculate Scores:")
        for i, role in enumerate(role_list, 1):
            print(f"{i}. {role.replace('_', ' ').title()}")
        
        try:
            choice = int(input(f"Enter Choice (1-{len(role_list)}): "))
            selected_role = role_list[choice - 1]
        except:
            print("❌ Invalid Selection.")
            return
            
        ats.calculate_ats_and_export(selected_role)
        
    else:
        print("❌ Invalid Operation.")

if __name__ == "__main__":
    main()