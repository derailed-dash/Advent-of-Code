# pyright: reportOptionalMemberAccess=false
# pyright: reportUnboundVariable=false
''' Circular Linked List implementation, including a Node wrapper. 
The implementation also uses a dict under-the-hood for fast retrieval by index. '''

class Node(object):
    ''' Wrapper for any data we want to add to the CLL '''
    def __init__(self, data = None, next_node = None):
        self._data = data
        self._next_node = next_node

    def set_next(self, next_node):
        self._next_node = next_node

    def get_next(self):
        return self._next_node

    def get_data(self):
        return self._data

    def __str__(self):
        return str(self._data)

    def __repr__(self):
        return f"{self.__class__.__name__}: " + str(self._data)

# Todo: fix length which depends on popping working

class CircularLinkedList():
    ''' Stores hashable objects in a linked list.
        Any retrievals or inserts by index would be costly for large lists.
        So under the covers, we use a dict to speed up the indexing process.
        Generally, the external API with the class should return node values, not the nodes themselves.
        Same goes for updates. '''

    def __init__(self, head = None, end = None):
        # logical beginning and end
        self._head = head
        self._end = end

        self._nodedict: dict[object, Node] = {}  # store all nodes as {value: node} for rapid retrieval
    
    def _create_node_in_dict(self, value):
        ''' Create dict entry for any node created. Value needs to be hashable for lookup to be unique. '''
        node = Node(value)
        self._nodedict[value] = node
        return node

    def get_end(self):
        if self._end:
            return self._end.get_data()

    def get_head(self):
        if self._head:
            return self._head.get_data()

    def index(self, item) -> Node:
        """ Get the node that contains this value. """

        item = Node(item)
        if item not in self._nodedict:
            raise ValueError(f"{item} not found")

        return self._nodedict[item]

    def move_head_after_value(self, value):
        '''
            Move the head to be the node after the specified value
            This list can't traverse backwards, which is why I'm doing it this way
        '''
        retrieved_node = self._nodedict[value]
        self._end = retrieved_node
        self._head = retrieved_node.get_next()

    def move_head_by_index(self, index):
        '''
            Set the head to the new index value.
            Fine for small lists.
        '''
        if index >= len(self):
            raise ValueError("Index out of bounds")  

        current_node = self._head
        
        if index == 0:    
            # nothing to do
            return 

        current_index = 0

        while current_index < index:
            last_node = current_node
            current_node = current_node.get_next()
            current_index += 1

        self._head = current_node
        self._end = last_node

        return        

    def __iter__(self):
        curr_node = self._head
        while curr_node.get_next():
            yield curr_node.get_data()
            curr_node = curr_node.get_next()

            if curr_node == self._head:
                break

    def __str__(self):
        '''  Traverse the list and return the values as a str. '''
        return_str = []

        # define the first node
        curr_node = self._head
        
        # as long as there is a next node, keep going
        while curr_node.get_next():  
            return_str.append(str(curr_node.get_data()))
            curr_node = curr_node.get_next() 
            
            # Here is the issue, if we don't add this condition we get an infinite loop.
            if curr_node == self._head:
                break

        return "\n".join(return_str)
        
    def __getitem__(self, index):
        '''
            Allows indexing of this linked list.
            Works fine for small lists. Slow for large.
        '''
        if index >= len(self):
            raise ValueError("Index out of bounds")  

        if index == 0:    
            return self._head.get_data()

        current_index = 0
        current_node = self._head

        # as long as there is a next node, keep going
        while current_index < index:
            current_node = current_node.get_next()
            current_index += 1

        return current_node.get_data()
            
    def __delitem__(self, index):
        return self.pop_mid_by_index(index)

    def __setitem__(self, index, value):
        # not yet implemented
        pass

    def insert_end(self, data):
        ''' Insert a node at the end of our linked list. '''  
        
        new_node = self._create_node_in_dict(data)
        
        # handle empty list case
        if self._head is None:            
            self._head = new_node
            self._head.set_next(new_node)
            self._end = new_node
            return
        
        # handle non-empty list case
        if self._end is not None:
            self._end.set_next(new_node)
            new_node.set_next(self._head)
            self._end = new_node
            return
                
    def insert_beg(self, data):
        ''' Insert a node at the beginning of our linked list. ''' 
        
        new_node = self._create_node_in_dict(data)
        new_node.set_next(self._head)
        curr_node = self._head
                   
        # handle empty list case
        if curr_node is None:            
            self._head = new_node
            self._end = new_node
            self._head.set_next(new_node)
            return
        
        # handle non-empty list case
        if self._end is not None:
            self._end.set_next(new_node)
            new_node.set_next(self._head)
            self._head = new_node
            return
    
    def index_of(self, reference_value):
        ''' Identifies the index of the value supplied '''
        current_index = 0
        current_node = self._head

        # as long as there is a next node, keep going
        while current_index < len(self):
            if (current_node.get_data() == reference_value):
                return current_index
            
            current_node = current_node.get_next()
            current_index += 1

        raise ValueError("Value not in list")
                
    def insert_after_index(self, index, data):
        ''' Inserts a new node after the index supplied '''
        # if we are inserting after the end node, then just use the insert_end method
        if index == (len(self) - 1):
            self.insert_end(data)
            return

        if index == 0:
            self.insert_beg(data)

        current_index = 0
        current_node = self._head
        current_node = current_node.get_next()

        # as long as there is a next node, keep going
        while current_index < index:
            last_node = current_node
            current_node = current_node.get_next()
            current_index += 1

        new_node = self._create_node_in_dict(data)
        next_node = last_node.get_next()

        last_node.set_next(new_node)
        new_node.set_next(next_node) 

    def insert_after_node(self, ref_data, data):
        '''
            Insert a node at the middle of our linked list, AFTER a given node.
            This one determines where to insert AFTER, by using the dict lookup.
            Thus, much faster than insert_after_index() with large lists.
        ''' 
        new_node = self._create_node_in_dict(data)
        previous_node = self._nodedict[ref_data]
        next_node = previous_node.get_next()
        previous_node.set_next(new_node)
        new_node.set_next(next_node)
        
    def pop_beg(self):
        ''' Delete and return value at the beginning of our list. ''' 
        
        if self._head is not None:
            old_head = self._head
            aft_head = self._head.get_next()  # grab the node that comes after the head.
            self._end.set_next(aft_head)  # have the last node now point to that node
            
            # set the head property.
            self._head = aft_head

            self._nodedict.pop(old_head.get_data())
            return old_head.get_data()
        else:
            raise ValueError("The list is empty")
          
    def pop_end(self):
        ''' Delete and return value at the end of our list. ''' 
        
        if self._end is not None:
            old_end = self._end
            curr_node = self._head  # grab the head
            
            # traverse until the end
            while curr_node.get_next().get_next() != self._head:                        
                curr_node = curr_node.get_next()
             
            # set the last node equal to the node before the last one.
            self._end = curr_node
            
            # have the new last node link to the head.
            curr_node.set_next(self._head)

            self._nodedict.pop(old_end.get_data())
            return old_end.get_data()
        else:
            raise ValueError("The list is empty")

    def pop_after_value(self, value):
        '''
            Delete and return the value in the node AFTER the value specified.
            Would prefer to implement pop(self, value), but I'd need to traverse backwards.
        '''
        previous_node = self._nodedict[value]
        node_to_pop = previous_node.get_next()
        new_next_node = node_to_pop.get_next()
        previous_node.set_next(new_next_node)

        self._nodedict.pop(node_to_pop.get_data())
        return node_to_pop.get_data()

    def pop_mid_by_index(self, index):
        ''' Delete a node in the middle of our list, at the specified index. ''' 
        # if position is 0 then delete first.
        if index == 0:            
            return self.pop_beg()
        
        # if position is the size of the list then delete the last one.
        if index == len(self) - 1:
            return self.pop_end()
        
        if index >= len(self):
            raise ValueError("Index out of bounds")            

        # grab the first node
        current_node = self._head
        current_index = 0
        
        # traverse till you reach the position
        while current_index < index: 
            prev_node = current_node
            current_node = current_node.get_next()

            current_index += 1
            
        # have it point to the node after the one you want to delete.
        prev_node.set_next(current_node.get_next())
        self._nodedict.pop(current_node.get_data())
        return current_node.get_data()
        
    def get_list(self):
        ''' 
            Convert to a regular list.
            Costly for large lists.
        '''
        the_list = []
        # grab the head
        curr_node = self._head
        the_list.append(curr_node.get_data())

        # traverse until you reach the head again
        while curr_node.get_next():
            curr_node = curr_node.get_next()
            
            # prevents infinite loop
            if curr_node == self._head:
                break
            else:
                the_list.append(curr_node.get_data())
                
        return the_list        

    def __len__(self):
        '''  Return the size of our list. ''' 
        return len(self._nodedict)
    
    def get_node_after(self, value):
        current_node = self._nodedict[value]
        next_node = current_node.get_next()
        return next_node.get_data()

    def get_prev_node(self, ref_node):
        '''
            Return the node before a given reference node.
            Allows backwards traversal, but doesn't scale well to large lists.
        ''' 
        
        # handle empty list case
        if self._head is None:
            raise ValueError("The list is empty")
        
        # define the first node
        current = self._head
        
        # keep going until you reach the desired node.
        while current.get_next() != ref_node:
            current = current.get_next()
                   
        return current
       
    def reverse(self):
        ''' Reverse the circular list, so that the tail is now the head. ''' 
        
        # if the head is empty return
        if self._head is None:
            raise ValueError("The list is empty")
        
        # initalize a few of our variables
        last = self._head
        curr = self._head
        prev = self._end        
        next_node = curr.get_next()
        

        curr.set_next(prev) # reassign the last node to the head's next node
        prev = curr  # the old previous now becomes the old current
        curr = next_node  # the old current now becomes the old next, the one after the head
        
        # keep going until you reach the last node
        while curr != last:
            
            # reassign next
            next_node=curr.get_next()
            
            # do the same reassignment steps as upabove
            curr.set_next(prev)
            prev = curr
            curr = next_node
        
        # one final reassignment, make sure the last node points to the head
        curr.set_next(prev)
        
        # then redefine your head and tail.
        self._head = prev
        self._end = curr
