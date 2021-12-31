from __future__ import annotations

class LinkedListNode:
    """ Allow any value to be wrapped in a LinkedListNode which is linked to next and prev.
    Thus allowing formation of a LinkedList.

    To establish the LinkedList, map all items in an existing list to a Node.
    Then iterate through the items, joining up the Nodes.
    If we want a CircularLinkedList, be sure to join the last to the first.

    linked_list = map(LinkedListNode, existing_list)
    for i, item in enumerate(linked_list):
        if i < (len(linked_list) - 1):
            linked_list[i].next = linked_list[i+1]
            linked_list[i+1].prev = linked_list[i]
    """
    def __init__(self, value) -> None:
        self._value = value
        self._next = None
        self._prev = None
    
    @property
    def value(self):
        return self._value
    
    @property
    def next(self) -> LinkedListNode | None:
        return self._next
    
    @next.setter
    def next(self, next_node):
        self._next = next_node
        
    @property
    def prev(self) -> LinkedListNode | None:
        return self._prev
    
    @prev.setter
    def prev(self, prev_node):
        self._prev = prev_node
    
    def unlink(self):
        """Removes reference to this node any adjacent nodes. """
        if self.next is not None:
            self.next.prev = self.prev
        else:       # self is at the end; we need a new end
            self.next = None
        
        if self.prev is not None:
            self.prev.next = self.next
        else:       # self is at the beginning; we need a new beginning
            self.prev = None
    
    def __repr__(self) -> str:
        prev_value = self.prev.value if self.prev is not None else "None"
        next_value = self.next.value if self.next is not None else "None"
        return f"{self.__class__.__name__}:self={self.value},prev={prev_value},next={next_value}"

    def __str__(self) -> str:
        return repr(self)
