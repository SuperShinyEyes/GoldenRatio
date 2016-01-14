
#mgilson did a good job but I'd like to add some more.

list1 = [1]
list2 = [1]
    
def main():
    list1.append(3)
    #list1 = [9]
    list2 = [222]

    print list1, list2


print "before main():", list1, list2
#>>> [1] [1]
main()
#>>> [1,3] [222]
print list1, list2    
#>>> [1, 3] [1]

"""
Inside a function, Python assumes every variable as local variable
unless you declare it as global, or you are accessing a global variable. 

list1.append(2) was possible because you are accessing the 'list1' and lists are mutable.
list2 was possible because you are initializing a local variable.
However if you uncomment #list1 = [9], you will get
UnboundLocalError: local variable 'list1' referenced before assignment
It means you are trying to initialize a new local variable 'list1' but it was already referenced before,
and you are out of the scope to reassign it.
"""