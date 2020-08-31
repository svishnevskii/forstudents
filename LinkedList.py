class Node:
    def __init__(self, data):
        self.element = data
        self.nextElemen = None
    
    def set_data(self, data):
        self.element = data
    def get_data(self):
        return self.element
    
    def set_next(self, node):
        self.nextElemen = node
    def get_next(self):
        return self.nextElemen   

class LinkedList:
    def __init__(self):
        self.head = None    
        self.tail = None
    
    def is_empty(self):
        return self.head is None
    
    def add(self, item):
        node = Node(item)
        node.set_next(self.head)
        self.head = node
        if self.tail is None:
            self.tail = node
    
    def size(self):
        current = self.head
        count = 0
        while not current is None:
            current = current.get_next()
            count += 1
        return count
    
    def search(self, item) -> bool:
        current = self.head
        while not current is None:
            if current.get_data() == item:
                return True
            else:
                current = current.get_next()
        return False
    
    def remove(self, item):
        current = self.head
        prev = None
        while True:
            if current.get_data() == item:
                break
            else:
                prev = current
                current = current.get_next()
                
        if prev is None:
            self.head = current.get_next()
        else:
            prev.set_next(current.get_next())
    
    def __str__(self):
        if self.head is None:
            return '[]'
        current = self.head
        out = '[' + str(current.get_data()) + ','
        while not current.get_next() is None:
            current = current.get_next()
            out += str(current.get_data()) + ','
        return out + ']'

    def append(self, item):
        node = Node(item)
        current = self.tail
        current.set_next(node)
        self.tail = node
    
        
my_list = LinkedList()

my_list.add(44)
my_list.add(45)
my_list.add(11)
my_list.add(46)

size = my_list.size()
is_empty = my_list.is_empty()
find = my_list.search(11)


print(
    my_list,
    is_empty,
    find,
)
    
    