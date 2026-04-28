for i in range(10):
    print("Hello, World!")
for i in range(10):
    print("hiii")
for i in range(10):
    print("good morning")

import threading

# Define the tasks
def task1():
    for i in range(10):
        print("Hello, World!")

def task2():
    for i in range(10):
        print("hiii")

def task3():
    for i in range(10):
        print("good morning")

# Create thread objects
t1 = threading.Thread(target=task1)
t2 = threading.Thread(target=task2)
t3 = threading.Thread(target=task3)

# Start the threads (they run in parallel)
t1.start()
t2.start()
t3.start()

# Wait for all threads to finish before moving on
t1.join()
t2.join()
t3.join()

print("All tasks finished!")