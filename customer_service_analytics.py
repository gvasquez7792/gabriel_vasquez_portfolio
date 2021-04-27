# A tool that allows the user to assess the linguistic properties of major companies' customer sercice tweets
import requests
import matplotlib.pyplot as plt
import nltk
import textblob
import json
import syllables
nltk.download("popular")

# declare a list variable for each company in the data set, create repeat variable for while loop
repeat = "yes"
sprintcare = []
ask_Spectrum = []
askPlayStation = []
xboxSupport = []
upsHelp = []
amazonhelp = []
appleSupport = []
uber_Support = []
spotifyCares = []
comcastcares = []
tMobileHelp = []
hulu_support = []


# format the request url using the API with JSON formatted data
response = requests.get(
    "https://dgoldberg.sdsu.edu/515/customer_service_tweets_full.json")


def polarity_subjectivity_avg_calculator(company_list):
    j = 0
    analysis_average = []
    total_holder = []
    polar_avg = []
    subj_avg = []
    total_polar_holder = []
    total_subj_holder = []

    for line in company_names:  # iterate through list of company names
        polarity = []
        subjectivity = []
        for line in company_list[j]:  # iterate through list of company tweet text
            blob = textblob.TextBlob(str(line))

            if analysis == "polarity":
                polarity.append(blob.polarity)
                total_holder = polarity

            elif analysis == "subjectivity":
                subjectivity.append(blob.subjectivity)
                total_holder = subjectivity

            elif analysis == "search":
                # execute when main iteration matches the handle searched by user
                if company_names[j] == target_twitter_handle:
                    # perform polar calculations
                    polarity.append(blob.polarity)
                    total_polar_holder = polarity

                    # perform subj calculations
                    subjectivity.append(blob.subjectivity)
                    total_subj_holder = subjectivity

        if analysis == "polarity" or analysis == "subjectivity":
            line_avg = (sum(total_holder) / len(total_holder))
            analysis_average.append(line_avg)
            print(company_names[j], ":", analysis_average[j])

        # execute when main iteration matches the handle searched by user and search analysis
        elif analysis == "search" and company_names[j] == target_twitter_handle:
            polar_avg.append(sum(total_polar_holder) / len(total_polar_holder))
            subj_avg.append(sum(total_subj_holder) / len(total_subj_holder))
            print("\nAverage polarity: ", polar_avg[0])
            print("Average subjectivity: ", subj_avg[0])

        j += 1
    # return list of avg for each company
    return analysis_average


def fkgl_smog_avg_calulator():

    analysis_average = []
    fkgl_avg = []
    smog_avg = []
    j = 0
    # calculate and print fkgl values for each company
    for line in company_names:
        all_sentences = []
        all_words = []
        all_syllables = []
        total_syllables = 0
        fkgl = 0
        # smog  specific variables
        total_polysyllables = 0
        smog = 0
        # holders for each line total
        total_holder = []
        fkgl_total_holder = []
        smog_total_holder = []

        for line in company_list[j]:
            all_sentences = []
            blob = textblob.TextBlob(str(line))
            total_words = len(blob.words)
            all_words.append(total_words)
            total_sentences = len(blob.sentences)
            all_sentences.append(total_sentences)
            total_syllables = syllables.estimate(str(blob))
            all_syllables.append(total_syllables)
            smog = 0
            total_polysyllables = 0

            if readability_analysis == "fkgl":
                fkgl = (((.39 * (sum(all_words) / sum(all_sentences))) +
                         (11.8 * (sum(all_syllables) / sum(all_words)))) - 15.59)
                total_holder.append(fkgl)
                all_sentences = []
                all_words = []
                all_syllables = []
                total_syllables = 0

            elif readability_analysis == "smog":
                for word in blob.words:
                    if syllables.estimate(word) >= 3:
                        total_polysyllables += 1
                smog = (1.043)*((float(total_polysyllables) *
                                 (30/sum(all_sentences)))**(1/2))+(3.1291)
                total_holder.append(smog)

            elif readability_analysis == "search":
                if company_names[j] == target_twitter_handle:
                    # perform fkgl calculations
                    fkgl = (((.39 * (sum(all_words) / sum(all_sentences))) +
                             (11.8 * (sum(all_syllables) / sum(all_words)))) - 15.59)
                    fkgl_total_holder.append(fkgl)
                    # perform smog calculations
                    for word in blob.words:
                        if syllables.estimate(word) >= 3:
                            total_polysyllables += 1
                    smog = (1.043)*((float(total_polysyllables) *
                                     (30/sum(all_sentences)))**(1/2))+(3.1291)
                    smog_total_holder.append(smog)
                    # clear lists for fkgl
                    all_sentences = []
                    all_words = []
                    all_syllables = []

        if readability_analysis == "fkgl" or readability_analysis == "smog":
            line_avg = (sum(total_holder) / len(total_holder))
            analysis_average.append(line_avg)
            print(company_names[j], ": ", analysis_average[j])

        elif readability_analysis == "search" and company_names[j] == target_twitter_handle:
            fkgl_avg.append(sum(fkgl_total_holder) /
                            len(fkgl_total_holder))
            smog_avg.append(sum(smog_total_holder) /
                            len(smog_total_holder))
            print("Average fkgl: ", fkgl_avg[0])
            print("Average smog: ", smog_avg[0])

        j += 1

    return analysis_average
# end of function declarations


if response:
    data = json.loads(response.text)
    print("Welcome to the customer service linguistics analyzer!")

    for line in data:
        if line["Company"] == "@sprintcare":
            sprintcare.append(line["Text"])
        if line["Company"] == "@Ask_Spectrum":
            ask_Spectrum.append(line["Text"])
        if line["Company"] == "@AskPlayStation":
            askPlayStation.append(line["Text"])
        if line["Company"] == "@XboxSupport":
            xboxSupport.append(line["Text"])
        if line["Company"] == "@UPSHelp":
            upsHelp.append(line["Text"])
        if line["Company"] == "@AmazonHelp":
            amazonhelp.append(line["Text"])
        if line["Company"] == "@AppleSupport":
            appleSupport.append(line["Text"])
        if line["Company"] == "@Uber_Support":
            uber_Support.append(line["Text"])
        if line["Company"] == "@SpotifyCares":
            spotifyCares.append(line["Text"])
        if line["Company"] == "@comcastcares":
            comcastcares.append(line["Text"])
        if line["Company"] == "@TMobileHelp":
            tMobileHelp.append(line["Text"])
        if line["Company"] == "@hulu_support":
            hulu_support.append(line["Text"])

    company_names = ["@sprintcare", "@ask_spectrum", "@askplaystation", "@xboxsupport", "@upshelp", "@amazonhelp", "@applesupport", "@uber_support", "@spotifycares",  "@comcastcares",
                     "@tmobilehelp", "@hulu_support"]

    company_list = [sprintcare, ask_Spectrum, askPlayStation, xboxSupport, upsHelp, amazonhelp,
                    appleSupport, uber_Support, spotifyCares, comcastcares, tMobileHelp, hulu_support]

    while repeat.lower() == "yes":
        # ask the user to specify the type of analysis to perform within while loop
        analysis = input(
            "\nWhich analysis would you like to perform \n(polarity/subjectivity/readability/search)? ").lower()
        print("")

        if analysis == "polarity" or analysis == "subjectivity" or analysis == "readability" or analysis == "search":
            # Polarity Analysis: calculate the avg sentiment polarity across that company's customer service tweets for each company in data set (based on sentiment scores per-tweet). Each avg polarity value will be printed with a bar graph display
            if analysis == "polarity":
                analysis_average = polarity_subjectivity_avg_calculator(
                    company_list)

                plt.title("Polarities by Twitter handle")
                plt.ylabel("Polarity")
                plt.xlabel("Twitter handle")
                plt.xticks(rotation=45, ha="right")
                # use returned list from function for data
                plt.bar(company_names, analysis_average)
                plt.show()
                plt.close()

            # Subjectivity Analysis:
            elif analysis == "subjectivity":
                analysis_average = polarity_subjectivity_avg_calculator(
                    company_list)

                plt.title("Subjectivity by Twitter handle")
                plt.ylabel("Subjectivity")
                plt.xlabel("Twitter handle")
                plt.xticks(rotation=45, ha="right")
                plt.bar(company_names, analysis_average)
                plt.show()
                plt.close()

            # Readability Analysis:
            elif analysis == "readability":
                again_analysis = "yes"

                while again_analysis.lower() == "yes":
                    readability_analysis = input(
                        "\nWould you like to analyse FKGL or SMOG? ").lower()

                    if readability_analysis == "fkgl" or readability_analysis == "smog":

                        if readability_analysis == "fkgl":
                            anaylysis_average = fkgl_smog_avg_calulator()
                            plt.title("Readability by Twitter handle")
                            plt.ylabel("Flesch-Kincaid Grade Level")
                            plt.xlabel("Twitter handle")
                            plt.xticks(rotation=45, ha="right")
                            plt.bar(company_names, anaylysis_average)
                            plt.show()
                            plt.close()

                        elif readability_analysis == "smog":
                            anaylysis_average = fkgl_smog_avg_calulator()
                            plt.title("Readability by Twitter handle")
                            plt.ylabel("SMOG Index")
                            plt.xlabel("Twitter handle")
                            plt.xticks(rotation=45, ha="right")
                            plt.bar(company_names, anaylysis_average)
                            plt.show()
                            plt.close()
                    else:
                        print(
                            "Sorry, that type of analysis is not supported. Please try again. ")
                    again_analysis = input(
                        "\nWould you like to run another FKGL or SMOG analysis (yes/no)? ").lower()

            # Search Analysis:
            elif analysis == "search":
                target_twitter_handle = input(
                    "Which Twitter handle would you like to search?: ")
                # call polarity_subjectivity_avg_calculator
                polarity_subjectivity_avg_calculator(company_list)
                # call fkgl_smog_avg_calculator
                readability_analysis = "search"
                fkgl_smog_avg_calulator()

            else:
                print(analysis)

        else:
            print("\nSorry, that type of analysis is not supported. Please try again. ")

        repeat = input("\nWould you like to run another analysis (yes/no) ")
    else:
        print("Program Ended.")
