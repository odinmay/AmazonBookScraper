# Grant List Creator
# Colin Stoll and Odin May

run = True
while run:
    action = input("Please input a URL, or type Q to quit:\nInput: ")
    if "amazon" in action:
        action += ","
        with open("book_list.txt", "a") as file:
            file.writelines([action])
        print("URL Successfully Added\n")


    if action == "Q":
        print("Goodbye")
        run = False