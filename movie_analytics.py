# A movie analytics tool that allows the user to search for a movie of their choosing and obtain further information about it using online data and text analytics
import requests
import json
import xmltodict
import matplotlib.pyplot as plt
import textblob
import wordcloud
import nltk
import skimage.io

nltk.download("popular")

api_key = "<Enter Your Key Here!>"
repeat = "yes"
repeat_fix = "yes"
# prompt user for a movie amd the type of analysis to execute
movie = input("\nHello, please enter a movie to analyze: ")
analysis = input(
    "Next, please select an analysis to run: Background, Reception, Poster, Wordcloud, or Sentiment\n")


def correct_filter(repeat, analysis):
    """
    Uses the correct() method with textblob variable derived from the repeat and analysis user variables. This veries fixes any spelling mistakes to the assumed word the correct() method thinks the user is trying to spell. Creates two global vairables to be able to use the "fixed" values throughout the program. 
    """
    repeat_blob = textblob.TextBlob(repeat)
    global repeat_fix
    repeat_fix = str(repeat_blob.correct())
    analysis_blob = textblob.TextBlob(analysis)
    global analysis_fix
    analysis_fix = str(analysis_blob.correct())


def analyzer(movie, analysis_fix, api_key):
    """
    Determins which of the five analysis the user would like to run and executes the chosen one. First decides which of the two APIs to use. Next, it finds the correct analysis to run. Then executes the analysis.
    """
    analysis = analysis_fix
    if analysis.lower() == "background" or analysis.lower() == "reception" or analysis.lower() == "poster":
        response = requests.get(
            "https://www.omdbapi.com/?r=xml&apikey="+api_key+"&t="+movie.lower())
        if response:
            data = xmltodict.parse(response.text)
            # create variables to hold the background, reception, and poster data
            main_data = data["root"]["movie"]
            background_data = [main_data["@year"],
                               main_data["@rated"], main_data["@runtime"],  main_data["@genre"], main_data["@actors"], main_data["@plot"]]
            reception_data = [main_data["@awards"],
                              main_data["@metascore"], main_data["@imdbRating"]]
            poster_data = main_data["@poster"]
            # if background analysis: print out the movie's year of release, rating, runtime, genre, actors, and plot summary
            if analysis.lower() == "background":
                print("\nYear: ", background_data[0])
                print("Rating: ", background_data[1])
                print("Runtime: ", background_data[2])
                print("Genre: ", background_data[3])
                print("Actors: ", background_data[4])
                print("Plot: ", background_data[5])

                # if reception analysis: print out the movie's awards, metascore, and IMDb rating
            elif analysis.lower() == "reception":
                print("\nAwards: ", reception_data[0])
                print("Metascore: ", reception_data[1])
                print("IMDb rating: ", reception_data[2])
                # if poster analysis: display an image of the movie's poster using URL from OMBDb API and display using plot.lib
            elif analysis.lower() == "poster":
                image = skimage.io.imread(poster_data)
                plt.imshow(image, interpolation="bilinear")
                plt.axis("off")
                plt.show()

            else:
                print("\nError chosing analysis with 1st API")
        else:
            print("\nError getting request from OMDb API")

    else:
        response = requests.get(
            "https://dgoldberg.sdsu.edu/515/imdb/"+movie + ".json")

        if response:
            data = json.loads(response.text)
            reviews_downloaded = ""
            # for each line in the data list that is related to 'review text' assign to review variable and include that new line to the downloaded reviews list
            for line in data:
                review = line["Review text"]
                reviews_downloaded = reviews_downloaded + review + " "

            # if wordcloud analysis: generate a wordcloud based on reviews from MIS 515 API
            if analysis.lower() == "wordcloud":

                cloud = wordcloud.WordCloud()

                cloud.generate(reviews_downloaded)
                plt.imshow(cloud, interpolation="bilinear")
                plt.axis("off")
                plt.show()

                # if sentiment analysis: displau the averahe review polarity and subjectivity scores from MIS 515 API movie reviews
            elif analysis.lower() == "sentiment":

                polarity_list = []
                subjectivity_list = []

                reviews_blob = textblob.TextBlob(reviews_downloaded)

                polarity_list.append(reviews_blob.polarity)
                subjectivity_list.append(reviews_blob.subjectivity)

                pol_sum = 0
                sub_sum = 0
                for i in polarity_list:
                    pol_sum = pol_sum + i

                for i in subjectivity_list:
                    sub_sum = sub_sum + i

                pol_avg = pol_sum / len(polarity_list)
                sub_avg = sub_sum / len(subjectivity_list)
                print("Average IMDb review polarity: ", pol_avg)
                print("Average IMDb review subjectivity: ", sub_avg)

            else:
                print("\nError chosing analysis with 2nd API")

        else:
            print("\nError getting request from MIS 515 API")


# while user wants to continue with new movie or analysis, execute prompts to get user data and call functions: correct_filter() and analyzer()
while(repeat.lower() == "yes" and repeat_fix.lower() == "yes"):
    correct_filter(repeat, analysis)
    # call analyzer function with given values
    analyzer(movie, analysis_fix, api_key)
    repeat = input("\nWould you like to further analyze this movie (yes/no)? ")
    correct_filter(repeat, analysis)
    repeat = repeat_fix
    # if user does not want to further anaylyze the initial movie, use next prompt
    if repeat.lower() == "no":
        repeat = input("\nWould you like to analyze a new movie (yes/no)? ")
        correct_filter(repeat, analysis)
        repeat = repeat_fix
        # if user enters 'yes' prompt for a new movie and analysis to execute
        if repeat.lower() == "yes":
            movie = input("\nPlease enter new movie to conduct analysis on: ")
            analysis = input(
                "\nNext, please select an analysis to run: Background, Reception, Poster, Wordcloud, or Sentiment\n")
            correct_filter(repeat, analysis)
        # if user enters 'no' program will end
        else:
            print("Ending program...")
    # if user enters anything besides 'no' execute prompt
    else:
        analysis = input("\nPlease enter the new analysis to run on " + movie +
                         ": Background, Reception, Poster, Wordcloud, or Sentiment\n")
        correct_filter(repeat, analysis)
