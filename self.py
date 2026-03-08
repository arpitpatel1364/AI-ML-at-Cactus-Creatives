import sys

def ultra_fast_concatenation(limit):
    chunks = [str(i) for i in range(1, limit)]
    
    final_string = "".join(chunks)
    return final_string

print(ultra_fast_concatenation(99999999))

from multiprocessing import cpu_count

if __name__ == "__main__": 
    cores = cpu_count()
    print(f"Number of CPU cores: {cores}")

