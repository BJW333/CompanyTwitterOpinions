import tweepy
import pandas as pd
from afinn import Afinn
import matplotlib.pyplot as plt

#these api no work cause not paid verison
bearer_token = "AAAAAAAAAAAAAAAAAAAAACUuuwEAAAAAankO%2FZuz8C8krpMLga0cRyu8gWI%3D6AC3J7k5yd6kgqMCo5U3GoS27Q3UU8htRXoJXbb5z4L6nzj7NI"
consumer_key = "ymVyLlLQXP3IP1wrfF8CMhMhB"
consumer_secret = "ds2CNoOxL5rzptxXJgHdFR7fSi9MpnkhKdlP9dVXYpt6Vxk4Yq"
access_token = "1805661374090985473-mKtH3QAnqYS7F4aa4K0XwxJMCai1is"
access_token_secret = "TC755kc9CxydtTmav41AQvm1kU1ZIZkr4bFniy7ZGffIR"
#client id UXVFSDY4WUQ4RUdlaldsaFRTMmQ6MTpjaQ
#client secret 6OrgjzLg9_2GLZ-NRRE52Dr09qBNge4AyOrghRAfj6gYVeMwNs

#Auth
Client = tweepy.Client(
    bearer_token=bearer_token,
    consumer_key=consumer_key,
    consumer_secret=consumer_secret,
    access_token=access_token,
    access_token_secret=access_token_secret,
    wait_on_rate_limit=True)

afinn = Afinn()

def RecentTweets(q, max_results, combined_data):
    response = Client.search_recent_tweets(query=q, expansions=["author_id"], max_results=max_results, tweet_fields=["created_at"])
    tweets = response.data
    for tweet in tweets:
        combined_data["User ID"].append(tweet.author_id)
        combined_data["Created At"].append(tweet.created_at)
        combined_data["Tweet ID"].append(tweet.id)
        combined_data["Tweet Text"].append(tweet.text)
        
def PullTweetslogic():
    while True:
        try:
            PullTweets = input('Would you like to pull tweets? (Y/N): ')
            if PullTweets not in ['Y', 'N']:
                raise ValueError('Sorry, please enter Y or N\n')
            elif PullTweets in ['Y']:
                return PullTweets
            else:
                if PullTweets in ['N']:
                    exit()
        except ValueError as ve:
            print(ve)

def PullWords():
    VarPullList = []
    while True:
        VarPullWords = input('Please enter a word or phrase to pull from Twitter eg company name or enter N to finish: ')
        if VarPullWords.lower() == 'n':
            return VarPullList
        else:
            VarPullList.append(VarPullWords)

def PullCount():
    while True:
        VarPullCount = input('How many Tweets would you like to pull per word/phrase? ')
        try:
            if VarPullCount.isdigit() != True:
                raise ValueError('Please enter a number.\n')
            else:
                return int(VarPullCount)
        except ValueError as ve:
            print(ve)

def QueryChart():
    VarQueryList = []
    while True:
        VarQueryChart = input('What words/phrases/companys would you like to query for or enter N to stop: ')
        if VarQueryChart == 'N':
            return VarQueryList
        else:
            VarQueryList.append(VarQueryChart)

def Pull_Tweets(VarPullList, VarPullCount, DictData):
    for i in range(len(VarPullList)):
        RecentTweets(VarPullList[i], VarPullCount, DictData)
        df = pd.DataFrame.from_dict(DictData)
        return df

def Update_Excel(df, file_path):
    df['Created At'] = df['Created At'].dt.tz_localize(None)
    ExistingDF = pd.read_excel(file_path)
    CombinedDF = pd.concat([ExistingDF, df.dropna(axis=1, how='all')], ignore_index=True)
    CombinedDF.to_excel(file_path, index=False)
    
def Pie_Chart(file_path):
    Pie_Chart_df = pd.read_excel(file_path)
    AvailableColors = ['blue', 'orange', 'green', 'red', 'purple', 'brown', 'pink', 'gray', '#aec7e8',
                       'cyan', '#ff9896', 'lightgreen', '#ffbb78', '#c5b0d5', '#c49c94']
    VarQueryChart = QueryChart()
    ChartLabels = [word.upper() for word in VarQueryChart]

    QueryChartCount = []
    for i in range(len(ChartLabels)):
        QueryChartCount.append(0)

    ChartColors = []
    for i in range(len(ChartLabels)):
        ChartColors.append(AvailableColors[i])

    Dict_Referenced_Tweet = []
    for index, row in Pie_Chart_df.iterrows():
        TweetText = row["Tweet Text"]
        for i in range(len(VarQueryChart)):
            if VarQueryChart[i] in TweetText.lower():
                QueryChartCount[i] += 1

    TotalOccurences = 0
    for i in range(len(QueryChartCount)):
        TotalOccurences += QueryChartCount[i]

    for i in range(len(ChartLabels)):
        print(ChartLabels[i] + ' was found: ' + str(QueryChartCount[i]))

    plt.figure(figsize=(15, 15))
    plt.pie(QueryChartCount, labels=ChartLabels, autopct='%.2f%%', colors=ChartColors)
    plt.text(0, 1.25, f'Percentage out of {TotalOccurences} occurences', fontsize=22, color='black', ha='center')
    plt.show()


def main():
    file_path = "/Users/blakeweiss/Desktop/CompanyTwitterOpinions/TweetData.xlsx"

    #words to query Twitter for
    VarPullTweets = PullTweetslogic()
    if VarPullTweets == 'Y':
        DictData = {"User ID": [], "Created At": [], "Tweet ID": [], "Tweet Text": []}
        VarPullList = PullWords()
        VarPullCount = PullCount()
        #Loop through wordlist and pulls tweets
        df = Pull_Tweets(VarPullList, VarPullCount, DictData)
        Update_Excel(df, file_path)

    Pie_Chart(file_path)

main()