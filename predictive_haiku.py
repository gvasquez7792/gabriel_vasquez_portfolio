# Haiku Generator
import json
import requests
import random

# URLs to be used
base = "https://api.datamuse.com/words?md=s&rel_trg="
base1 = "https://api.datamuse.com/words?md=s&lc="

print("Hello, welcome to the predictive text Haiku generator!")

# while loop to prompt user for another Haiku for a succesful or failed attempt
again = "yes"
while again.lower() == "yes":
    # try block to check validility
    try:
        topic = input("What would you like to see a Haiku about?\n")

        # function with data parameter to do a syllable check and random word pick for each API call
        def syllable_check(data):
            list2 = []
            list3 = []
            func_data = data
            for line in func_data:
                if line["numSyllables"] == 2:
                    list2.append(line["word"])
                    word = random.choice(list2)
                elif line["numSyllables"] == 3:
                    list3.append(line["word"])
                    word = random.choice(list3)

            return word

        haiku_word_list = []
        response = requests.get(base + topic)
        # check  if successful response from topic related url
        if response:
            data0 = json.loads(response.text)
            # call function & append random word to haiku word list
            rand_word = syllable_check(data0)
            haiku_word_list.append(rand_word)

            response1 = requests.get(base1 + haiku_word_list[0])

        else:
            print("Sorry, connection error")
        # check if response successful from left context url w/ word0
        if response1:
            data1 = json.loads(response1.text)

            rand_word = syllable_check(data1)
            haiku_word_list.append(rand_word)

            response2 = requests.get(base1 + haiku_word_list[1])

        else:
            print("Sorry, connection error")
        # check if succesful response from left context url w/ word1
        if response2:
            data2 = json.loads(response2.text)

            rand_word = syllable_check(data2)
            haiku_word_list.append(rand_word)

            # while loop to ensure word0 is different from word2
            while haiku_word_list[0] == haiku_word_list[2]:
                haiku_word_list.pop()
                rand_word = syllable_check(data1)
                haiku_word_list.append(rand_word)

            response3 = requests.get(base1 + haiku_word_list[2])

        else:
            print("Sorry, connection error")
        # check if succesful response from left context url w/ word2
        if response3:
            data3 = json.loads(response3.text)

            rand_word = syllable_check(data3)
            haiku_word_list.append(rand_word)

            # ensure random words are different for haiku
            while haiku_word_list[1] == haiku_word_list[3]:
                haiku_word_list.pop()
                rand_word = syllable_check(data1)
                haiku_word_list.append(rand_word)

            response4 = requests.get(
                base1 + haiku_word_list[3] + "&rel_rhy=" + haiku_word_list[1])

        else:
            print("Sorry, connection error")
        # check if succesful response from left context url w/ word3 and adds rhymming parameter w/ word1
        if response4:
            data4 = json.loads(response4.text)

            rand_word = syllable_check(data4)
            haiku_word_list.append(rand_word)

            # ensure random words are different for haiku
            while haiku_word_list[4] == haiku_word_list[1] or haiku_word_list[4] == haiku_word_list[3]:
                haiku_word_list.pop()
                rand_word = syllable_check(data1)
                haiku_word_list.append(rand_word)

            response5 = requests.get(base1 + haiku_word_list[4])

        else:
            print("Sorry, connection error")
        # check if succesful response from left context url w/ word4
        if response5:
            data5 = json.loads(response5.text)

            rand_word = syllable_check(data5)
            haiku_word_list.append(rand_word)

            # ensure random words are different for haiku
            while haiku_word_list[5] == haiku_word_list[0] or haiku_word_list[5] == haiku_word_list[2]:
                haiku_word_list.pop()
                rand_word = syllable_check(data1)
                haiku_word_list.append(rand_word)

            response6 = requests.get(
                base1 + haiku_word_list[5] + "&rel_rhy=" + haiku_word_list[1])

        else:
            print("Sorry, connection error")
        # check if succesful response from left context url w/ word5 and adds rhymming parameter w/ word1
        if response6:
            data6 = json.loads(response6.text)

            rand_word = syllable_check(data6)
            haiku_word_list.append(rand_word)

            # ensure random words are different before creating haiku
            while haiku_word_list[6] == haiku_word_list[1] or haiku_word_list[6] == haiku_word_list[3] or haiku_word_list[6] == haiku_word_list[4]:
                haiku_word_list.pop()
                rand_word = syllable_check(data3)
                haiku_word_list.append(rand_word)

        else:
            print("Sorry, connection error")

        print("\n" + haiku_word_list[0], haiku_word_list[1])
        print(haiku_word_list[2], haiku_word_list[3], haiku_word_list[4])
        print(haiku_word_list[5], haiku_word_list[6] + "\n")

    except:
        print("\nSorry, a valid Haiku could not be generated.\n")

    again = input("Would you like to see another Haiku (yes/no)?\n")

print("Haiku generator ended!")
