text = "This is a sample text.\nThis is the second line.\nAnd this is the third line. "
print(text)

# write to a file
my_file = open("my_file.txt", "w")    #only write
my_file.write(text)
my_file.close()   #remember to close the file

#------------------
#append to a file
my_file = open("my_file.txt", "a")    #append
my_file.write("\nThis is the fourth line.") 
my_file.close()   #remember to close the file

#read from a file
file = open("my_file.txt", "r")    #read
content  = file.read()

content = file.readline()   #read one line at a time
content = file.readline()   #read the next line
content = file.readlines()  #read all lines into a list

print(content)
file.close()   #remember to close the file