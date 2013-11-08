class Byte_Queue:
    
    def __init__(self):
        self.qsize = 0
        self.array = [None]*512
        self.first = 0
        self.put_next = 0

    def put(self, byte):
        self.array[self.put_next] = byte
        self.put_next += 1
        self.qsize += 1
        if self.put_next >= len(self.array):
            self.put_next = 0

    def peek(self):
        return self.array[self.first]

    def get(self):
        if not self.empty():
            value = self.array[self.first]
            self.first += 1
            self.qsize -= 1
            if self.first >= len(self.array):
                self.first = 0
            return value

    def size(self):
        return self.qsize

    def empty(self):
        return self.first == self.put_next
    # methods:
    # put
    # peek
    # get
    # size (returns qsize)
    # empty
