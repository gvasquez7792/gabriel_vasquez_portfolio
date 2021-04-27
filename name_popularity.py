# MIS-515 HW #1 | This progam is capable of conducting two types of anlysis (Name Comparison or Maximum Popularity) on a csv file of baby names (1900 to 2014)

import csv

repeat = "y"

print("Welcome to the baby name analyzer! ")

while repeat == "y":

    # open csv file and create reader for file
    with open("usa_baby_names.csv", "r") as file:
        reader = csv.reader(file)
        # prompt user which mode to use: Name Comparison or Maximum Popularity
        search = input(
            "Choose an analysis: Name Comparison or Maximum Popularity \n")
        # input validation
        # if Name Comparison; prompt user for two names to compare
        if search.title() == "Name Comparison":
            # then compute the totals for each name (sum) between 1900 & 2014
            baby_name1 = input("Enter the first baby name to compare: ")
            baby_name2 = input("Enter the second baby name to compare: ")

            list_1 = []
            list_2 = []
            # for loop through csv file | if statement to decide which list to append freq number
            for line in reader:
                name = line[0]

                if baby_name1.lower() == name.lower():
                    list_1.append(int(line[2]))

                if baby_name2.lower() == name.lower():
                    list_2.append(int(line[2]))

            name1_sum = sum(list_1)
            name2_sum = sum(list_2)
            # then report totals for each name as well as which name was most common
            if name1_sum > name2_sum:
                print(baby_name1, "is more popular than",
                      baby_name2, ":", name1_sum, ">", name2_sum)

            else:
                print(baby_name2, "is more popular than",
                      baby_name1, ":", name2_sum, ">", name1_sum)
        # if Maximium Popularity; prompt user for a single name
        elif search.title() == "Maximum Popularity":
            baby_name1 = input(
                "Enter a baby name to display most popular year: \n")

            list_1 = []
            popular_year = 0
            max_freq = 0
            # create a for loop to run thru the reader
            for line in reader:
                name = line[0]
                year = line[1]
                freq_num = line[2]
                # 1st if statement collect line[n] Freq. num to list_1
                if baby_name1.lower() == name.lower():
                    list_1.append(int(freq_num))
                    # use the last appended freq. num in 2nd if statement to update popular_year and max_freq
                    if list_1[-1] > max_freq:
                        popular_year = year
                        max_freq = max(list_1)

            print("The year", popular_year, "for the name", baby_name1.title(),
                  "was its most popular with a frequency of", max_freq)
        # if invalid input; prompt user to enter a valid analysis option or end program
        else:
            print("Invalid input.")
    # After analysis is completed ask if user is done or wants to do another analysis
    repeat = input("Would you like to run another analysis (y/n): ")

print("Thank you!")
