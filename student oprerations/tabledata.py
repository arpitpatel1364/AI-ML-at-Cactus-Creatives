
import pandas as pd
import os
        


FILENAME ="student oprerations\student_records.txt"
COLUMNS = ["Student ID", "Student Name", "Maths", "Science", "English", "Total", "Average", "Grade"]


if os.path.exists(FILENAME):
    df = pd.read_csv(FILENAME)
else:
    df = pd.DataFrame(columns=COLUMNS)

def calculate_grade(avg):
    if avg >= 90:
        return "A"
    elif avg >= 75:
        return "B"
    elif avg >= 60:
        return "C"
    elif avg >= 40:
        return "D"
    else:
        return "Fail"

def save_file():
    # """Helper function to sync the DataFrame to the text file"""
    global df
    df.to_csv(FILENAME, index=False)
    print(f"Data saved in to {FILENAME}")

def add_student():
    global df
    try:
        while True:
            SIDS = set(map(int, df["Student ID"])) if not df.empty else set()
            sid = int(input("Enter Student ID: ").strip())

            # for make sure student id is unique
            if sid <= 0:
                print("Student ID must be a positive. enter again.")
                
            elif sid in SIDS:
                print("This Student ID already exists. Enter a different ID.")
            
            else:
                break
# make sure marks was not nagative or more than 100
        name = input("Enter Student Name: ").strip()
        while True:
            m = int(input("Maths Marks: ")) 
            if 0 <= m <= 100:
                break
            else:  
                continue
        while True:
            s = int(input("Science Marks: ")) 
            if 0 <= s <= 100:
                break  
            else:  
                continue
        while True:
            e = int(input("English Marks: ")) 
            if 0 <= e <= 100:
                break    
            else:  
                continue
                
            
        total = m + s + e 
        avg = total / 3 

        grade = calculate_grade(avg) 
        # cursor.execute(f"INSERT INTO students VALUES ({sid},{name},{m},{s},{e},{total},{avg},{grade})", df)
        new_row = [sid, name, m, s, e, total, avg, grade]
        new_data = pd.DataFrame([new_row], columns=COLUMNS)
        
        df = pd.concat([df, new_data], ignore_index=True)
        
        #  for save
        save_file()
        print("Student added successfully!")
    except ValueError:
        print("Error: Please enter numeric values for marks.")

def main():
    while True:
        print("\n--- Wel come, it is Student Result Management System ---") 
        print("1. Add Student\n2. Display All\n3. Search ID\n4. Topper\n5. Highest marks by SUB\n6. Class Average\n7. Exit") 
        choice = input("Select Option: ")

        if choice == '1': 
            add_student()
        elif choice == '2': 
            print("\n", df if not df.empty else "No records found.")
            # cursor.execute("SELECT * FROM students")
        elif choice == '3':
            try:
                sid = int(input("Search ID: "))
                result = df[df["Student ID"].astype(str) == str(sid)]
                print(result if not result.empty else "Student not found.")
            except ValueError:
                print("Invalid input. Please enter a numeric Student ID.")
                
        elif choice == '4':
            if not df.empty:
                print("\nClass Topper:")
                print(df.loc[df['Total'].idxmax()])
            else: print("No data available.")
        elif choice == '5':
            if not df.empty:
                print("\nHighest Marks per Subject:") 
                print(df[['Maths', 'Science', 'English']].max())
            else: print("No data available.")
        elif choice == '6':
            if not df.empty:
                print(f"\nOverall Class Average: {df['Average'].mean():.2f}") 
            else: print("No data available.")
        elif choice == '7': 
            print("please come again, thank you!")
            break 



main()
# if we reuse this code in anthor file 
# if __name__=="__main__":
#     main()

# conn.close()