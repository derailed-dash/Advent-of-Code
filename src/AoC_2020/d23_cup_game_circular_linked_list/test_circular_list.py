from circular_linked_list import Circular_Linked_List

# define a new list
circular_list = Circular_Linked_List()

# insert a few values at the end
circular_list.insert_end(50)
circular_list.insert_end(60)
circular_list.insert_end(70)

# insert a few values at the beginning
circular_list.insert_beg(90)
circular_list.insert_beg(100)

print('After Insertion')
print('-'*20)
print(circular_list)

a_node = circular_list[3]
print(f"Node 3: {a_node}")

# grab a node
last_node = circular_list.get_end()

# insert value inbetween two nodes.
print(f'Inserting 20 after {last_node}...')
circular_list.insert_after_node(last_node, 20)
print('-'*20)
print(circular_list)

print(f'Inserting 10 after {a_node}...')
circular_list.insert_after_node(a_node, 10)
print('-'*20)
print(circular_list)

print('Popping first and last...')
# delete the first and last value
old_beg = circular_list.pop_beg()
print(old_beg)
old_end = circular_list.pop_end()
print(old_end)

print('\nAfter deletion')
print('-'*20)
print(circular_list)

# reverse the list
circular_list.reverse()

print('After Reversal')
print('-'*20)
print(circular_list)

# return the list size
circular_list.get_size()

# delete a node at position 3
print('Popping mid at 3...')
print('-'*20)
mid_node = circular_list.pop_mid_by_index(3)
print(mid_node)

print('After Mid Deletion')
print('-'*20)
print(circular_list)

print('\nNow iterate...')
for val in circular_list:
    print(val)

a_node = circular_list[circular_list.get_size() - 1]
print(f'Last node by index: {a_node}')

print('Covert to list...')
new_list = circular_list.get_list()
print(new_list)
print(f"Size: {circular_list.get_size()}")

print(f"Current head: {circular_list.get_head()}")

print("Move head to 2")
circular_list.move_head_by_index(2)
print(f"Current head: {circular_list.get_head()}")
print(circular_list)

print("Move head to 0")
circular_list.move_head_by_index(0)
print(f"Current head: {circular_list.get_head()}")
print(circular_list)

print("Move head to end")
circular_list.move_head_by_index(circular_list.get_size()-1)
print(f"Current head: {circular_list.get_head()}")
print(circular_list)
