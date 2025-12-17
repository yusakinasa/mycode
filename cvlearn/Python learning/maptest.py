a =[1,2,3]
b = [4,5,6]

c = zip(a,b)
print(list(c))   #[(1, 4), (2, 5), (3, 6)]


for i,j in zip(a,b):   
    print(i,j)   


d = zip(a,a,b)  #also works
#--------------------

fun1=lambda x:x+1    #to define a simple function
print(fun1(2))   #3


print(list(map(fun1,a)))   #[2, 3, 4]    