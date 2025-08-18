import statistics as st
import queue


def average(values: list[int]) -> float:
    return round(sum(values) / len(values), 2) if values else 0


values = [1, 2, 3, 4]

print(st.mean(values))

q = queue.Queue(2)
q.put(1)
q.put(2)
print(q.get_nowait())
print(q.get_nowait())
q.get()
# q.put(3)
# q.put(4)

# print(q.qsize())
