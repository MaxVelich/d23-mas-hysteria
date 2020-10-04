
print("Test file")

from queue import PriorityQueue
 
q = PriorityQueue()
 
q.put((1, 'high_priority_2'))
q.put((1, 'low_priority'))
q.put((1, 'high_priority_1'))
q.put((1, 'medium_priority'))
 
while not q.empty():
    next_item = q.get()
    print(next_item)