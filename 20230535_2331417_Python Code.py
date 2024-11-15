# Import the os module to perform operating system-related tasks
import os
# Import the random module for generating random numbers and performing randomization tasks
import random
# Provides a convenient way to generate and display ASCII tables in Python
from prettytable import PrettyTable
# Import the sys module in Python
# Provides access to some variables used or maintained by the Python interpreter and functions that interact strongly with the interpreter.
import sys

# Define the text file which is to be used as the storage media
HORSE_DATABASE_FILE = "horse_database.txt"


# Function to create the database file if it does not exist
def create_file():
    if not os.path.isfile(HORSE_DATABASE_FILE):
        with open(HORSE_DATABASE_FILE, 'w') as file:
            # Add headers to the file
            headers = "Horse_ID,Horse_Name,Jockey_Name,Age,Breed,Race_Record,Group\n"
            file.write(headers)


# Function to load horse details
def load_data():
    data = []
    try:
        with open(HORSE_DATABASE_FILE, 'r') as file:
            current_group = None
            for line in file:
                line = line.strip()

                # Check if the line starts with "Group:"
                if line.startswith("Group:"):
                    current_group = line.split(":")[1].strip()
                    continue

                if current_group and line:
                    # Split each line by commas and create a dictionary
                    values = line.split(",")

                    # Check if the line has the expected number of values
                    if len(values) == 9:
                        horse = {
                            "Horse_ID": values[0],
                            "Horse_Name": values[1],
                            "Jockey_Name": values[2],
                            "Age": values[3],
                            "Breed": values[4],
                            "Race_Record": values[5] + ", " + values[6] + ", " + values[7],
                            "Group": current_group
                        }
                        data.append(horse)
                    else:
                        print(f"Ignoring invalid line: {line}")

    except FileNotFoundError:
        print("Database file not found. Creating a new one...")
    return data


# Function to save horse details
def save_data_to_file(data):
    with open(HORSE_DATABASE_FILE, 'w') as file:
        # Add headers to the file
        headers = "Horse_ID,Horse_Name,Jockey_Name,Age,Breed,Race_Record,Group\n"
        file.write(headers)

        # Categorize data by group
        grouped_data = {}
        for horse in data:
            group = horse["Group"]
            if group not in grouped_data:
                grouped_data[group] = []
            grouped_data[group].append(horse)

        # Sort and write data to the file, grouped by category and sorted by group
        for group in bubble_sort_group(list(grouped_data.keys())):
            file.write(f"\nGroup: {group}\n")
            group_data = grouped_data[group]

            # Sort the group data based on "Horse_ID" using bubble sort
            bubble_sort_group(group_data, key=lambda x: int(x["Horse_ID"]))

            for horse in group_data:
                # Convert each horse's details to a comma-separated string
                values = ",".join(map(str, horse.values()))
                file.write(values + "\n")

    print("Data saved successfully.")


# Function to sort data without python prebuilt function in sorting horses according to horse ids
def bubble_sort_horseId(data):
    n = len(data)
    for i in range(n):
        for j in range(0, n - i - 1):
            if int(data[j]["Horse_ID"]) > int(data[j + 1]["Horse_ID"]):
                data[j], data[j + 1] = data[j + 1], data[j]


# Function to sort data without python prebuilt function in sorting horses according to groups
def bubble_sort_group(data, key=None):
    n = len(data)
    for i in range(n):
        for j in range(0, n - i - 1):
            if key is None:
                if data[j] > data[j + 1]:
                    data[j], data[j + 1] = data[j + 1], data[j]
            else:
                if key(data[j]) > key(data[j + 1]):
                    data[j], data[j + 1] = data[j + 1], data[j]
    return data


# Function to sort data without python prebuilt function in ranking horses according to the assigned times
def bubble_sort_ranking(selected_horses):
    horses_list = list(selected_horses.values())
    n = len(horses_list)
    for i in range(n):
        for j in range(0, n - i - 1):
            if horses_list[j]["Time"] > horses_list[j + 1]["Time"]:
                horses_list[j], horses_list[j +
                                            1] = horses_list[j + 1], horses_list[j]
    return horses_list


# Function to display horse details
def display_data(data):
    if data:
        # Categorization according to the group it belongs

        # Extract unique groups
        groups = set([horse["Group"] for horse in data])

        # Convert groups to a list and sort in ascending order using bubble sort
        groups_list = bubble_sort_group(list(groups))

        for group in groups_list:
            print(f"\nGroup: {group}")
            header = list(data[0].keys())
            group_data = [row for row in data if row["Group"] == group]

            # Sort the group data based on the "Horse_ID" using bubble sort
            bubble_sort_group(group_data, key=lambda x: int(x["Horse_ID"]))

            # Create a PrettyTable object
            table = PrettyTable(header)

            for row in group_data:
                values = list(row.values())
                # Add each row to the PrettyTable
                table.add_row(values)

            # Print the PrettyTable
            print(table)
    else:
        print("No Horse Details in the File")


# Function to add horse details
def add_data(data):
    # Collect horse information
    horse = {}
    horse["Horse_ID"] = input("Enter Horse ID: ")

    # Check if the Horse ID already exists
    existing_horse = next((h for h in data if h["Horse_ID"] == horse["Horse_ID"]), None)
    if existing_horse:
        print("Horse with the same Horse ID already exists!")
        return

    horse["Horse_Name"] = input("Enter Horse Name: ")
    horse["Jockey_Name"] = input("Enter Jockey Name: ")
    horse["Age"] = input("Enter Age of the Horse: ")
    horse["Breed"] = input("Enter Breed of the Horse: ")
    horse["Race_Record"] = input("Enter Race Record Correctly: ")

    # Validate and get a valid "Group" input
    valid_groups = {"A", "B", "C", "D"}
    while True:
        group_input = input("Enter Updated Group of the Horse (One Group out of A, B, C, and D): ").upper()
        if group_input in valid_groups:
            horse["Group"] = group_input
            break
        else:
            print("Invalid input. Please enter A, B, C, or D.")

    data.append(horse)

    print("\nHorse Details Added Successfully!!!\n")


# Function to update horse details by id
def update_data(data):
    horse_id = input("Enter ID of the Horse to be updated: ")
    for horse in data:
        if horse["Horse_ID"] == horse_id:
            horse["Horse_Name"] = input("Enter Updated Horse Name: ")
            horse["Jockey_Name"] = input("Enter Updated Jockey Name: ")
            horse["Age"] = input("Enter Updated Age of the Horse: ")
            horse["Breed"] = input("Enter Updated Breed of the Horse: ")
            horse["Race_Record"] = input(
                "Enter Updated Race Record Correctly: ")

            # Validate and get a valid "Group" input
            valid_groups = {"A", "B", "C", "D"}
            while True:
                group_input = input("Enter Updated Group of the Horse (One Group out of A, B, C, and D): ").upper()
                if group_input in valid_groups:
                    horse["Group"] = group_input
                    break
                else:
                    print("Invalid input. Please enter A, B, C, or D.")

            print("Horse Details Updated Successfully!!!\n\n")
            return
    print("Horse with the given ID Not Found!!!")


# Function to delete horse details by id
def delete_data(data):
    horse_id = input("Enter ID of the Horse to be removed: ")
    for horse in data:
        if horse["Horse_ID"] == horse_id:
            data.remove(horse)
            print("Horse Details Deleted Successfully!!!\n\n")
            return
    print("Horse with the given ID Not Found!!!")


# Function to select a horse for the final round from each group randomly
def select_horse_for_final_round(data):
    groups = bubble_sort_group(list(set([horse["Group"] for horse in data])))
    selected_horses = {}

    for group in groups:
        group_data = [horse for horse in data if horse["Group"] == group]
        if group_data:
            selected_horse = random.choice(group_data)
            selected_horses[group] = selected_horse
    return selected_horses


# Function to assign a random time for horses selected to the final round
def assign_random_time(selected_horses):
    for horse in selected_horses.values():
        try:
            horse["Time"] = random.randint(0, 90)
        except ValueError as e:
            print(f"Error assigning random time to horse {horse['Horse_ID']}: {e}")


# Function to rank the selected horses according to their times
def rank_horses(selected_horses):
    sorted_horses = bubble_sort_ranking(selected_horses)
    return sorted_horses


# Function to visualize time with asterisks
def visualize_time(horse):
    num_asterisks = horse["Time"] // 10
    asterisks = "*" * num_asterisks
    return f"{asterisks} {horse['Time']}s"


# Function to display the final round results
def display_final_round_results(ranked_horses):
    positions = ["1st", "2nd", "3rd", "4th"]
    for i, horse in enumerate(ranked_horses):
        position = positions[i] if i < len(positions) else str(i + 1)
        print(f"Horse {horse['Horse_ID']}: {visualize_time(horse)} ({position} Place)")


# Define the main method to display a console menu system to enable the user input with validations
def main():
    create_file()

    data = load_data()

    while True:
        print("\n\n************************************************")
        print("\nWelcome to the Rapid Run Horse Management System\n")
        print("************************************************")
        print("AHD - Add Horse Details")
        print("UHD - Update Horse Details")
        print("DHD - Delete Horse Details")
        print("VHD - View the Registered Horses' Details Table (Sorted by Horse ID and Categorized by Group)")
        print("SHD - Save Horse Details")
        print("SDD - Select Horses Randomly For the Final Round")
        print("WHD - Display Winning Horses' Details")
        print("VWH - Visualize the Time of Winning Horses")
        print("ESC - Exit the Program")
        print("************************************************\n\n")

        choice = input("Please enter your choice: ")

        if choice == 'AHD':
            add_data(data)
        elif choice == 'UHD':
            update_data(data)
        elif choice == 'DHD':
            delete_data(data)
        elif choice == 'VHD':
            # Sort records in ascending order based on horse id
            bubble_sort_horseId(data)
            print("Horses in Ascending order by Horse ID and Categorized by Group: ")
            display_data(data)
        elif choice == 'SHD':
            save_data_to_file(data)
        elif choice == 'SDD':
            selected_horses = select_horse_for_final_round(data)
            print("Horses randomly selected for the Final Round!!!\n")
            for group, horse in selected_horses.items():
                print(f"Group: {group}, Selected Horse Details: {horse}")
        elif choice == 'WHD':
            if selected_horses:
                assign_random_time(selected_horses)
                print(
                    "Random Time (between 0 to 90s) was assigned for horses selected to the final round...\n\n")
                # Perform sorting with own function for ranking based on time
                ranked_horses = bubble_sort_ranking(selected_horses)
                print("Final Round Results:")
                for i, horse in enumerate(ranked_horses):
                    position = "1st" if i == 0 else "2nd" if i == 1 else "3rd" if i == 2 else "4th" if i == 3 else ""
                    print(f"Group: {horse['Group']}")
                    print(f"{position} Place - {horse['Horse_ID']}")
        elif choice == 'VWH':
            if selected_horses:
                # Perform sorting with own function for ranking based on time
                ranked_horses = bubble_sort_ranking(selected_horses)
                print("Final Round Results With Time Spent by them:")
                display_final_round_results(ranked_horses)
        elif choice == 'ESC':
            print("Thanks for Staying with Us. Good Bye!!!")
            sys.exit()  # This line exits the program
        else:
            print("Invalid Choice. Please enter a valid option...")


if __name__ == "__main__":
    main()
