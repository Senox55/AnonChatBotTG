import queue


class ChatQueue:
    def __init__(self):
        self.queue = queue.Queue

    def enqueue(self, user_id: int):
        self.queue.put(user_id)

    def dequeue(self):
        if self.queue:
            return self.queue.get()
        return None
