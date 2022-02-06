import threading
import time 

def funct(steps, delay):
    print('thread functions start')
    for i in range(steps):
        time.sleep(delay)
        print(f'Step: {i}')
    print('thread function stop')

print('Main thread start')

# create threads
t1 = threading.Thread(target=funct, args=(5,1,))
t2 = threading.Thread(target=funct, args=(5,0.5,))

# Start threads
t1.start()
t2.start()
time.sleep(2)

# wait for all threads to finish
t1.join()
t2.join()

# end application
print('Main thread stop')