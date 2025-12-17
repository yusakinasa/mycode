try:
    file = open("nonexistentfile.txt", "r")
except Exception as e:
    print(f"An error occurred: {e}")
else:
    content = file.read()
    print(content)