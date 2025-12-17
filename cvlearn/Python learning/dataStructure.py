# tuple 
#元组是固定且不可改变的。这意味着一旦元组被创建，和列表不同，它的内容无法被修改或它的大小也无法被改变。
a_tuple = (1, 2, 3, 4)
another_tuple = 1, 2, 3, 4  



# for iriterate
for item in a_tuple:
    print(item) 


for index in range(len(a_tuple)):
    print('index:', index, 'value:', a_tuple[index])


# list

a= [1, 2, 3, 4]

a.append(5)
print(a)   # [1, 2, 3, 4, 5]    

a.insert(2,6)   #this means insert 6 before index 2
print(a)   # [1, 2, 6, 3, 4, 5]

a.remove(3)   #remove the first 3
print(a)   # [1, 2, 6, 4, 5]

print(a[-1])   # 5, the last element
print(a[0:3])   # [1, 2, 6], from index 0 to index 3 but not include index 3
print(a[1:])   # [2, 6, 4, 5], from index 1 to the end
print(a[:3])   # [1, 2, 6], from the beginning

print(a.index(2))   # 1, the index of the first 2
print(a.count(2))   # 1, the number of 2 in the list

a.sort()   # sort the list in ascending order
a.sort(reverse=True)   # sort the list in descending order
a.reverse()   # reverse the list

#  multiply list
b= [[1, 2], [3, 4]]   # a 2D list
print(b[0][1])   # 2, the 0 row, 1 column


# dictionary   which is a key-value pair ,not ordered
d = {'name': 'Alice', 'age': 25, 'city': 'New York'}
print(d['name'])   # Alice
d['age'] = 26   # update age
d['job'] = 'Engineer'   # add job

