import random


# ============================================================
# Node Class
# ============================================================

class Node:

    def __init__(self, destination, next_hop, level):
        self.destination = destination
        self.next_hop = next_hop

        # Forward pointers for different levels
        self.forward = [None] * (level + 1)


# ============================================================
# Skip List Class
# ============================================================

class SkipList:

    def __init__(self, max_level):

        # Header/Sentinel node
        self.header = Node("", "", max_level)

        # Current highest level
        self.level = 0

        # Maximum possible level
        self.MAX_LEVEL = max_level


    # --------------------------------------------------------
    # Generate Random Level
    # --------------------------------------------------------

    def randomLevel(self):

        level = 0

        while random.random() < 0.5 and level < self.MAX_LEVEL:
            level += 1

        return level


    # --------------------------------------------------------
    # Insert Routing Entry
    # --------------------------------------------------------

    def insertRoute(self, destination, next_hop):

        current = self.header

        # Stores previous nodes at every level
        update = [None] * (self.MAX_LEVEL + 1)


        # Start from highest level and move downward
        for i in range(self.level, -1, -1):

            while (current.forward[i] is not None and
                   current.forward[i].destination < destination):

                current = current.forward[i]

            update[i] = current


        # Move to level 0
        current = current.forward[0]


        # Check if route already exists
        if current is not None and current.destination == destination:

            # Update next hop if destination already exists
            current.next_hop = next_hop

            print("\nRoute already exists.")
            print("Next hop updated successfully.")

            return


        # Generate random level for new node
        rlevel = self.randomLevel()


        # If new node has a higher level
        if rlevel > self.level:

            for i in range(self.level + 1, rlevel + 1):
                update[i] = self.header

            self.level = rlevel


        # Create new routing node
        newNode = Node(destination, next_hop, rlevel)


        # Connect new node at every level
        for i in range(rlevel + 1):

            newNode.forward[i] = update[i].forward[i]

            update[i].forward[i] = newNode


        print("\nRoute inserted successfully.")
        print("Destination :", destination)
        print("Next Hop    :", next_hop)


    # --------------------------------------------------------
    # Search Routing Entry
    # --------------------------------------------------------

    def searchRoute(self, destination):

        current = self.header


        # Start from highest level
        for i in range(self.level, -1, -1):

            while (current.forward[i] is not None and
                   current.forward[i].destination < destination):

                current = current.forward[i]


        # Move to level 0
        current = current.forward[0]


        # Check whether destination exists
        if current is not None and current.destination == destination:

            return current


        return None


    # --------------------------------------------------------
    # Delete Routing Entry
    # --------------------------------------------------------

    def deleteRoute(self, destination):

        current = self.header

        update = [None] * (self.MAX_LEVEL + 1)


        # Find position of destination
        for i in range(self.level, -1, -1):

            while (current.forward[i] is not None and
                   current.forward[i].destination < destination):

                current = current.forward[i]

            update[i] = current


        # Move to level 0
        current = current.forward[0]


        # Check whether route exists
        if current is None or current.destination != destination:

            print("\nRoute not found.")

            return


        # Remove node from all levels
        for i in range(self.level + 1):

            if update[i].forward[i] != current:
                break

            update[i].forward[i] = current.forward[i]


        # Reduce Skip List level if necessary
        while (self.level > 0 and
               self.header.forward[self.level] is None):

            self.level -= 1


        print("\nRoute deleted successfully.")
        print("Destination :", destination)


    # --------------------------------------------------------
    # Display Routing Table
    # --------------------------------------------------------

    def displayRoutingTable(self):

        print("\n")
        print("=" * 80)
        print("                         ROUTING TABLE")
        print("=" * 80)

        print("{:<25} {:<20}".format(
            "Destination Network",
            "Next Hop"
        ))

        print("-" * 80)


        # Get all nodes from Level 0
        nodes = []

        current = self.header.forward[0]

        while current is not None:

            nodes.append(current)

            current = current.forward[0]


        # Check if list is empty
        if len(nodes) == 0:

            print("Routing table is empty.")

            print("=" * 80)

            return


        # Display routing entries
        for node in nodes:

            print("{:<25} {:<20}".format(
                node.destination,
                node.next_hop
            ))


        print("=" * 80)


    # --------------------------------------------------------
    # Display Skip List Structure
    # --------------------------------------------------------

    def displaySkipList(self):

        print("\n")
        print("=" * 100)
        print("                    SKIP LIST STRUCTURE")
        print("=" * 100)


        # Get all nodes from Level 0
        nodes = []

        current = self.header.forward[0]

        while current is not None:

            nodes.append(current)

            current = current.forward[0]


        # Empty list
        if len(nodes) == 0:

            print("Skip List is empty.")

            print("=" * 100)

            return


        # Width of every position
        SPACE = 20


        # Display from highest level to level 0
        for level in range(self.level, -1, -1):

            print("Level {}: ".format(level), end="")


            for node in nodes:

                # Check whether node exists at this level
                if len(node.forward) > level:

                    print(
                        node.destination.center(SPACE),
                        end=""
                    )

                else:

                    print(
                        " " * SPACE,
                        end=""
                    )


            print()


            # Print vertical connections
            if level != 0:

                print("        ", end="")


                for node in nodes:

                    if len(node.forward) > level:

                        print("|".center(SPACE), end="")

                    else:

                        print(" " * SPACE, end="")


                print()


        print("=" * 100)

MAX_LEVEL = 6

skiplist = SkipList(MAX_LEVEL)


while True:

    print("\n")
    print("========================================")
    print("          ROUTING TABLE MENU")
    print("========================================")
    print("1. Insert Route")
    print("2. Display Routing Table")
    print("3. Search Route")
    print("4. Delete Route")
    print("5. Display Skip List Structure")
    print("6. Exit")
    print("========================================")


    choice = input("Enter your choice: ")
    if choice == "1":

        destination = input(
            "Enter destination network: "
        )

        next_hop = input(
            "Enter next hop: "
        )

        skiplist.insertRoute(
            destination,
            next_hop
        )
    elif choice == "2":

        skiplist.displayRoutingTable()
    elif choice == "3":

        destination = input(
            "Enter destination network to search: "
        )

        node = skiplist.searchRoute(destination)
        if node is not None:

            print("\nRoute found!")
            print(
                "Destination :",
                node.destination
            )
            print(
                "Next Hop    :",
                node.next_hop
            )
        else:
            print("\nRoute not found.")
    elif choice == "4":
        destination = input(
            "Enter destination network to delete: "
        )
        print("\n--- Routing Table Before Deletion ---")
        skiplist.displayRoutingTable()
        skiplist.deleteRoute(destination)
        print("\n--- Routing Table After Deletion ---")
        skiplist.displayRoutingTable()
    elif choice == "5":

        skiplist.displaySkipList()

    elif choice == "6":

        print("\nExiting program...")

        break
    else:

        print("\nInvalid choice. Please try again.")