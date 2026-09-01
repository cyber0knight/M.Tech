import random

class Node:
    def __init__(self,key, level ):
        self.key = key
        self.forward = [None] * (level+1)

class SkipList:
    def __init__(self, max_level):
        self.header = Node(float("-inf"), max_level)
        self.level = 0
        self.MAX_LEVEL = max_level

    def randomLevel(self):
        level = 0
        while random.random() < 0.5 and level < self.MAX_LEVEL:
            level += 1
        return level

    def insertNode(self, key):
        current = self.header
        update = [None] * (self.MAX_LEVEL + 1)

        for i in range(self.level, -1, -1):
            while current.forward[i] and current.forward[i].key < key:
                current = current.forward[i]
            update[i] = current

        current = current.forward[0]

        if current is None or current.key != key:
            rlevel = self.randomLevel()

            if rlevel > self.level:
                for i in range(self.level+1, rlevel +1):
                    update[i] = self.header
                self.level = rlevel

            newNode = Node(key, rlevel)
            for i in range(rlevel + 1):
                newNode.forward[i] = update[i].forward[i]
                update[i].forward[i] = newNode

    def searchNode(self, key):
        current = self.header
        for i in range(self.level, -1, -1):
            while current.forward[i] and current.forward[i].key < key:
                current = current.forward[i]
        current = current.forward[0]
        if current and current.key == key:
            return current
        return None

    def displayList(self):

        print("\n")
        print("=" * 70)
        print("                    SKIP LIST")
        print("=" * 70)

        nodes = []

        current = self.header.forward[0]

        while current is not None:
            nodes.append(current)
            current = current.forward[0]

        if len(nodes) == 0:
            print("Skip List is empty.")
            return

        # Width of each position
        SPACE = 7

        # Display from highest level to level 0
        for level in range(self.level, -1, -1):

            print("Level {}: ".format(level), end="")
            current = self.header.forward[0]
            for node in nodes:
                # Check whether this node exists at this level
                if len(node.forward) > level:
                    print(str(node.key).center(SPACE), end="")
                else:
                    print(" " * SPACE, end="")
            print()
            # Print vertical lines except after Level 0
            if level != 0:
                print("        ", end="")
                for node in nodes:
                    if len(node.forward) > level:
                        print("|".center(SPACE), end="")
                    else:
                        print(" " * SPACE, end="")
                print()
        print("=" * 70)

    def deleteNode(self, key):
      current = self.header
      update = [None] * (self.MAX_LEVEL + 1)

      for i in range(self.level, -1, -1):
         while current.forward[i] and current.forward[i].key < key:
            current = current.forward[i]
         update[i] = current
      current = current.forward[0]

      if current and current.key == key:
         for i in range(self.level + 1):
            if update[i].forward[i] != current:
               break
            update[i].forward[i] = current.forward[i]
         while self.level > 0 and self.header.forward[self.level] is None:
            self.level -= 1
         del current



# Driver code
MAX_LEVEL = 6
list = SkipList(MAX_LEVEL)
print("\n========== MENU ==========")
print("1. Insert")
print("2. Display")
print("3. search")
print("4. delete")
print("5. Exit")
print("==========================")
while True:
    choice = input("Enter your choice: ")
    # INSERT
    if choice == "1":
        try:
            key = int(input("Enter the value to insert: "))
            list.insertNode(key)
        except ValueError:
            print("Please enter a valid integer.")
    # DISPLAY
    elif choice == "2":
        list.displayList()
    # EXIT
    elif choice == "5":
        print("Exiting program...")
        break
    elif choice == "3":
        val = int(input("Enter the value to search: "))
        node = list.searchNode(val)
        if node:
            print("Key found: ", node.key)
        else:
            print("Key not found")
    elif choice == "4":
        val = int(input("Enter the value to delete: "))
        print("list before deletion")
        list.displayList()
        list.deleteNode(val)
        print("list after deleteion")
        list.displayList()

    else:
        print("Invalid choice. Please try again.")