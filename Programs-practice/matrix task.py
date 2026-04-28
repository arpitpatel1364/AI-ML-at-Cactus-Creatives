import numpy as np

matrix1 = np.random.randint(-25, 26, size=(3, 3))

matrix2 = 1 - matrix1

print("--- Matrix 1 ---")
print(matrix1)

print("\n--- Matrix 2 ---")
print(matrix2)

matrix_sum = matrix1 + matrix2
matrix_product = matrix1 * matrix2

print("\n--- Sum of Matrix 1 and Matrix 2 (All should be 1) ---")
print(matrix_sum)
print("\n--- Product of Matrix 1 and Matrix 2 (All should be 0) ---")
print(matrix_product)

