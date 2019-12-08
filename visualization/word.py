
from matplotlib import pyplot as plt

from wordcloud import WordCloud


def word_count(df,width = 1200, height = 1000, NaN = True):
    if NaN:
        text = ' '.join(df.fillna('NaN').values)
    else:
        text = ' '.join(df.fillna('').values)
    wordcloud = WordCloud(max_font_size=None, background_color='white',
                      width=width, height=height).generate(text)
    plt.imshow(wordcloud)
    plt.axis("off")
