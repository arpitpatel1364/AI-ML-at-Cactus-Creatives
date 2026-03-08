import pandas as pd
import sqlite3
import sys

class StudentManager:
    def __init__(self, db_name="student_records.db"):
        self.db_name = db_name
        self.columns = ["Student ID", "Name", "Maths", "Science", "English", "Total", "Average", "Grade"]
        self._setup_db()

    def _setup_db(self):
        """Initializes the database table if it doesn't exist."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS students (
                    
                    id TEXT PRIMARY KEY,
                    name TEXT,
                    maths INTEGER,
                    science INTEGER,
                    english INTEGER,
                    total INTEGER,
                    average REAL,
                    grade TEXT
                )
            """)
            conn.commit()

    def get_all_records(self):
        """Fetches fresh data from SQL into a Pandas DataFrame."""
        with sqlite3.connect(self.db_name) as conn:
            return pd.read_sql_query("SELECT * FROM students", conn)

    def calculate_grade(self, average):
        if average >= 90: 
            return "A"
        if average >= 75: 
            return "B"
        if average >= 60: 
            return "C"
        if average >= 40:
            return "D"
        with average < 40:
            return "Fail"

    def validate_marks(self, subject):
        while True:
            try:
                score = int(input(f"Enter {subject} marks (0-100): "))
                if 0 <= score <= 100:
                    return score
                print(" Please enter a score between 0 and 100.")
            except ValueError:
                print(" Invalid input. Please enter a whole number.")

    def add_student(self):

        while True:
            print("\n Register New Student ")
            student_id = input("Student ID: ").strip()
            
            # Check for existing ID
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT id FROM students WHERE id = ?", (student_id,))
            
            if cursor.fetchone():
                print(f" ! Error: ID '{student_id}' already exists.")
                    
            elif 0 > int(student_id):
                    print("please enter valid StudentID.")       
            else:
                break

        
            

        name = input("Student Name: ").strip() or "N/A"
        maths = self.validate_marks("Maths")
        science = self.validate_marks("Science")
        english = self.validate_marks("English")

        total = maths + science + english
        avg = round(total / 3, 2)
        grade = self.calculate_grade(avg)

        try:
            cursor.execute(
                "INSERT INTO students VALUES (?,?,?,?,?,?,?,?)",
                (student_id, name, maths, science, english, total, avg, grade)
            )
            conn.commit()
            print(f"\nSuccessfully added {name}\'s details !")
        except Exception as e:
            print(f"An error occurred: {e}")

    def show_stats(self, df):
        if df.empty:
            print("\n ! No records found .")
            return False
        return True


def main():
    manager = StudentManager()
    
    while True:
        
        print("1. Add Student\n2. Display All\n3. Search ID\n4. Topper\n5. Highest marks by SUB\n6. Class Average\n7. Exit") 
        
        choice = input("\nSelect an option: ")

        # get data
        df = manager.get_all_records()
    
        if choice == '1':
            manager.add_student()
            print("\n")

        elif choice == '2':
            if not df.empty:
                print("\n", df.to_string(index=False))
                print("\n")
            else:
                print("\nDatabase is currently empty.")
                print("\n")

        elif choice == '3':
            while True:
                search_id = input("Enter ID to find: ")
                result = df[df['id'] == search_id]
                if not result.empty:
                    print("\nRecord Found:\n", result.to_string(index=False))
                    print("\n")
                    break
                elif int(search_id.strip()) < 0:
                    print("Please enter a valid numeric ID.")
                else:
                    print("No student found with that ID.")
                    print("\n")
                    break

        elif choice == '4':
            if manager.show_stats(df):
                topper = df.loc[df['total'].idxmax()]
                print(f"\n Class Topper \nName: {topper['name']}\nTotal: {topper['total']}\nGrade: {topper['grade']} \n")

        elif choice == '5':
            if manager.show_stats(df):
                print("\nSubject Highest:")
                print(df[['maths', 'science', 'english']].max())
        
        elif choice == "6": 
            print(f"\nOverall Class Average: {df['average'].mean():.2f}")
            print("\n")
                

        elif choice == '7':
            print("Exiting system. Have a great day!")
            print("\n")
            sys.exit()
            

        
        # elif choice == '0':
        #     print(len(df))

        else:
            print("Invalid selection. Please try again.")

if __name__ == "__main__":
    main()
