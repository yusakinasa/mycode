import copy
a = [1,2,3]
b = a   #just a reference, not a copy     shares the same memory address(id)
a[0]=100 #change a, b also changes


c = copy.copy(a)  #shallow copy, different memory address(id)
a[1]=200 #c does not change

#--------
a = [[1,2],[3,4]]
b = copy.copy(a)  #shallow copy, different memory address(id)
a[0][0]=100 #b changes because inner list is not copied


c = copy.deepcopy(a)  #deep copy, different memory address(id)
a[0][1]=200 #c does not change

