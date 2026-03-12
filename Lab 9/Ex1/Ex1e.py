# Open the file names.txt and read its contents and print the number of names

with open("names.txt") as file_object:
    contents_list = file_object.readlines()
    print(contents_list)

with open("names.txt", "a") as file_object:
    print("Adding a name to the file...")
    file_object.write("Adams, Amy\n")
    contents_list.append("Adams, Amy\n")
    print(f"Number of names: {len(contents_list)}")