import threading
import time 

def funct(steps):
    print('thread functions start')
    for i in range(steps):
        time.sleep(0.5)
        print(f'Step: {i}')
    print('thread function stop')

t = threading.Thread(target=funct, args=(5,))
print('Main thread start')
t.start()
time.sleep(2)
print('Main thread stop')