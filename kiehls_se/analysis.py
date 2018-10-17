import numpy as np
import pandas as pd
import csv
import matplotlib
import matplotlib.pyplot as plt
import nltk
from wordcloud import WordCloud


with open(r'C:\nydsa bootcamp slides\Projects\1\kiehls_se\reviews.csv','rb') as f:
    rawfile=pd.read_csv(f,header=None)

    #change the header of the DF
    rawfile=rawfile.rename(columns={0: 'Rating', 1: 'User_Location', 2: 'Publish_Date', 3: 'Subject', 4: 'Cons', 5: 'Text'})

    #sort the DF by comment publish date
    rawfile = rawfile.sort_values('Publish_Date')

    #trim the month and year info from the Publish_Date column and add them as new columns into the DF
    rawfile['Month'] = rawfile['Publish_Date']
    rawfile['Year'] = rawfile['Publish_Date']

    for index in range(len(rawfile.index)):
        Month = int(str(rawfile.loc[[index], 'Month']).split('-')[1])
        Year = int(str(rawfile.loc[[index], 'Year']).split('-')[0][-4:])
        rawfile.loc[[index], 'Month'] = Month
        rawfile.loc[[index], 'Year'] = Year

    #1 Rating trend (from 2010 to 2018)
    rating_yearlyave = rawfile.groupby('Year').agg({'Rating': ['mean']})
    rating_yearlyave.plot.line()
    plt.show()

    # 2 rating/year
    rating_num = rawfile.groupby('Year').agg({'Year': ['count']})
    rating_num.plot.bar(y='Year', rot=0)
    plt.show()

    #3. wordcloud of cons
    con_text = ""
    for index in range(len(rawfile.index)):
        if rawfile['Cons'][index] is not pd.np.nan:
            con_text += rawfile['Cons'][index] + ' '
    con_text = con_text.replace('con', '').replace(':)', '').replace('none', '').replace('no', '').replace('skin', '')
    wc = WordCloud()
    wc.generate(con_text)
    plt.imshow(wc, interpolation='bilinear')
    plt.axis("off")
    plt.show()

    #4 Rating impacted by seasons
    subdf = rawfile[['Rating', 'Month']]
    temp = subdf['Month']
    temp = temp.replace([1, 2, 12], 'winter').replace([3, 4, 5], 'Spring').replace([6, 7, 8], 'Summer').replace([9, 10, 11], 'Autumn')
    subdf.insert(2, 'season', temp)
    season = subdf.groupby('season').agg({'Rating': ['mean', 'count']})
    season.columns = season.columns.droplevel(0)
    season_count = season[['count']]
    season_count.plot.pie(subplots=True, figsize=(8, 8))
    plt.show()
