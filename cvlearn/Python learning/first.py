# for iter
example_list = [1, 2, 3, 4, 5]

for i in example_list:
    print(i)


# range function
for i in range(5):   #0 to 4
    print(i)


for i in range(1, 6):  #1 to 5
    print(i)


for i in range(1, 11, 2):  #1 to 10 with step of 2
    print(i)

#--------------------------------------------------------------
# if sentence
x,y,z = 5,10,15

if x<y<z:    # python admits chained comparisons
    print("x is less than y and y is less than z")

if x<y>z:    # this is also valid
    print("x is less than y or y is greater than z")


#  use elif to mean"else if"
#  只要有一个条件满足，后面的条件就不再判断