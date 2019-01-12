# From Linux Kernel : linux/include/linux/list.h


class Dlist:

    def __init__(self, data=None):

        self.data = data
        self.init()

    def init(self):
        self.next = self
        self.prev = self

    @staticmethod
    def __add(new, prev, next):
        next.prev = new
        new.next = next
        new.prev = prev
        prev.next = new

    @staticmethod
    def __del(prev, next):
        next.prev = prev
        prev.next = next

    @staticmethod
    def __splice(head, prev, next):
        first = head.next
        last  = head.prev

        prev.next  = first
        first.prev = prev

        next.prev  = last
        last.next  = next

    def add(self, new):
        Dlist.__add(new, self, self.next)

    def add_tail(self, new):
        Dlist.__add(new, self.prev, self)

    def remove(self):

        self.prev.next_ = self.next
        self.next.prev_ = self.prev

        self.next = self
        self.prev = self

    def move(self, head):
        self.remove()
        head.add(self)

    def move_tail(self, head):
        self.remove()
        head.add_tail(self)

    def is_last_of(self, head):
        return self.next is head

    def is_empty(self):
        return self is self.next

    def is_singular(self):
        return not self.is_empty and (self.next == self.prev)

    def rotate_left(self):
        if not self.is_empty():
            self.next.move_tail(self)
