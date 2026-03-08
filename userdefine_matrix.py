import numpy as np

print("--- Matrix Addition Setup ---")
# get a positive integer for rows

while True:
    try:
        r = int(input("Enter number of rows: "))
        if r > 0:
            break
        else:
            print(" Rows must be positive. Try again.")
    except ValueError:
        print(" Invalid input! Please enter a number.")

# 2. Get Columns (Must be Positive)
while True:
    try:
        c = int(input("Enter number of columns: "))
        if c > 0:
            break
        else:
            print(" Columns must be positive. Try again.")
    except ValueError:
        print(" Invalid input! Please enter a number.")

# MATRIX 1:
matrix1 = np.random.randint(-500, 501, size=(r, c))

matrix2 = 1 - matrix1

# 4. Result
matrix_sum = matrix1 + matrix2

print("\n--- Matrix 1 ---")
print(matrix1)
print("\n--- Matrix 2 ---")
print(matrix2)
print("\n--- Final Sum ---")
print(matrix_sum)
