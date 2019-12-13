
from matplotlib import pyplot as plt

from wordcloud import WordCloud


def word_count(df,width = 1200, height = 1000, NaN = True,colormap="Dark2",  background_color='white', interpolation="bilinear", color_func = None, ):
    if NaN:
        text = ' '.join(df.fillna('NaN').values)
    else:
        text = ' '.join(df.fillna('').values)
    wordcloud = WordCloud(max_font_size=None, background_color=background_color,
                      width=width, height=height, color_func= color_func, colormap=colormap).generate(text)
    plt.imshow(wordcloud,  interpolation=interpolation)
    plt.axis("off")
