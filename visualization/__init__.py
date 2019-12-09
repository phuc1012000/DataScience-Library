import pandas as pd
import numpy as np

from matplotlib import pyplot as plt
import seaborn as sns

### distribution ###
def distribution(df,columns = None, column_fig = 2 , figsize=(18,4),color = None, compare = None):

    # Distribution over 1 feature
    if columns is None:
        amount_val = df
        sns.distplot(df,color=color)
        plt.title('Distribution')
        plt.xlim([min(amount_val), max(amount_val)])

    # Draw multiple Distribution figure
    else:
        num_ax = 0
        num_ax_limit = len(columns)
        column_fig_index = 0

        if compare is not None:
            column_label , label = zip(*compare.items())
            column_label = column_label[0]

            if label[0] == 'all':
                label = df[column_label].unique()

            else:
                label = label[0]

            column_fig = len(label) + 1

        fig, ax = plt.subplots(1, column_fig , figsize = figsize)

        while num_ax < num_ax_limit:
            if compare and column_fig_index  < column_fig -1:
                amount_val = df.loc[df[column_label] == label[column_fig_index]][columns[num_ax]].values
            else:
                amount_val = df[columns[num_ax]].values

            if color == None:
                sns.distplot(amount_val, ax=ax[column_fig_index])
            else:
                sns.distplot(amount_val, ax=ax[column_fig_index],color = color[column_fig_index])

            if compare and column_fig_index  < column_fig -1:
                ax[column_fig_index].set_title('Distribution of '+ columns[num_ax] +' of Class: ' + str(label[column_fig_index]))
            else:
                ax[column_fig_index].set_title('Distribution of '+ columns[num_ax])

            ax[column_fig_index].set_xlim([min(amount_val), max(amount_val)])

            column_fig_index += 1

            if not compare:
                num_ax +=1

            if column_fig_index == column_fig:
                column_fig_index = 0
                if compare:
                    num_ax +=1

                if num_ax != num_ax_limit:
                    fig, ax = plt.subplots(1, column_fig , figsize = figsize)


### HEATMAP ###
def heatmap(x, y,figsize = (10,10) ,title = "HEATMAP", **kwargs):

    plt.figure(figsize=figsize)

    if 'color' in kwargs:
        color = kwargs['color']
    else:
        color = [1]*len(x)

    if 'palette' in kwargs:
        palette = kwargs['palette']
        n_colors = len(palette)
    else:
        n_colors = 256 # Use 256 colors for the diverging color palette
        palette = sns.color_palette("Blues", n_colors)

    if 'color_range' in kwargs:
        color_min, color_max = kwargs['color_range']
    else:
        color_min, color_max = min(color), max(color) # Range of values that will be mapped to the palette, i.e. min and max possible correlation

    def value_to_color(val):
        if color_min == color_max:
            return palette[-1]
        else:
            val_position = float((val - color_min)) / (color_max - color_min) # position of value in the input range, relative to the length of the input range
            val_position = min(max(val_position, 0), 1) # bound the position betwen 0 and 1
            ind = int(val_position * (n_colors - 1)) # target index in the color palette
            return palette[ind]

    if 'size' in kwargs:
        size = kwargs['size']
    else:
        size = [1]*len(x)

    if 'size_range' in kwargs:
        size_min, size_max = kwargs['size_range'][0], kwargs['size_range'][1]
    else:
        size_min, size_max = min(size), max(size)

    size_scale = kwargs.get('size_scale', 500)

    def value_to_size(val):
        if size_min == size_max:
            return 1 * size_scale
        else:
            val_position = (val - size_min) * 0.99 / (size_max - size_min) + 0.01 # position of value in the input range, relative to the length of the input range
            val_position = min(max(val_position, 0), 1) # bound the position betwen 0 and 1
            return val_position * size_scale
    if 'x_order' in kwargs:
        x_names = [t for t in kwargs['x_order']]
    else:
        x_names = [t for t in sorted(set([v for v in x]))]
    x_to_num = {p[1]:p[0] for p in enumerate(x_names)}

    if 'y_order' in kwargs:
        y_names = [t for t in kwargs['y_order']]
    else:
        y_names = [t for t in sorted(set([v for v in y]))]
    y_to_num = {p[1]:p[0] for p in enumerate(y_names)}

    plot_grid = plt.GridSpec(1, 15, hspace=0.2, wspace=0.1) # Setup a 1x10 grid
    ax = plt.subplot(plot_grid[:,:-1]) # Use the left 14/15ths of the grid for the main plot

    marker = kwargs.get('marker', 's')

    kwargs_pass_on = {k:v for k,v in kwargs.items() if k not in [
         'color', 'palette', 'color_range', 'size', 'size_range', 'size_scale', 'marker', 'x_order', 'y_order'
    ]}

    ax.scatter(
        x=[x_to_num[v] for v in x],
        y=[y_to_num[v] for v in y],
        marker=marker,
        s=[value_to_size(v) for v in size],
        c=[value_to_color(v) for v in color],
        **kwargs_pass_on
    )
    ax.set_xticks([v for k,v in x_to_num.items()])
    ax.set_xticklabels([k for k in x_to_num], rotation=45, horizontalalignment='right')
    ax.set_yticks([v for k,v in y_to_num.items()])
    ax.set_yticklabels([k for k in y_to_num])

    ax.grid(False, 'major')
    ax.grid(True, 'minor')
    ax.set_xticks([t + 0.5 for t in ax.get_xticks()], minor=True)
    ax.set_yticks([t + 0.5 for t in ax.get_yticks()], minor=True)

    ax.set_xlim([-0.5, max([v for v in x_to_num.values()]) + 0.5])
    ax.set_ylim([-0.5, max([v for v in y_to_num.values()]) + 0.5])
    ax.set_facecolor('#F1F1F1')

    # Add color legend on the right side of the plot
    if color_min < color_max:
        ax = plt.subplot(plot_grid[:,-1]) # Use the rightmost column of the plot

        col_x = [0]*len(palette) # Fixed x coordinate for the bars
        bar_y=np.linspace(color_min, color_max, n_colors) # y coordinates for each of the n_colors bars

        bar_height = bar_y[1] - bar_y[0]
        ax.barh(
            y=bar_y,
            width=[5]*len(palette), # Make bars 5 units wide
            left=col_x, # Make bars start at 0
            height=bar_height,
            color=palette,
            linewidth=0
        )
        ax.set_xlim(1, 2) # Bars are going from 0 to 5, so lets crop the plot somewhere in the middle
        ax.grid(False) # Hide grid
        ax.set_facecolor('white') # Make background white
        ax.set_xticks([]) # Remove horizontal ticks
        ax.set_yticks(np.linspace(min(bar_y), max(bar_y), 3)) # Show vertical ticks for min, middle and max
        ax.yaxis.tick_right() # Display HEATMAP that variance in side and color
    plt.title(title)
    plt.figure()

### corrplot ###
def corrplot(data, size_scale=500, marker='s', method=None, figsize= (10,10), title= "correlation Matrix"):
    if method is None:
        data = data.corr()
    else:
        data = data.corr()
    corr = pd.melt(data.reset_index(), id_vars='index')
    corr.columns = ['x', 'y', 'value']
    heatmap(
        corr['x'], corr['y'],
        figsize = figsize,
        title = title,
        color=corr['value'], color_range=[-1, 1],
        palette=sns.diverging_palette(20, 220, n=256),
        size=corr['value'].abs(), size_range=[0,1],
        marker=marker,
        x_order=data.columns,
        y_order=data.columns[::-1],
        size_scale=size_scale
    )

def bar(df, column, add_percentage = True, hue =None, title = None, legend = False):

    total = df[column].count()

    if add_percentage:
        ax = sns.countplot(y=column, data= df, hue =hue)
        percentage(ax, total)
    else:
        ax = sns.countplot(x=column, data= df, hue =hue)

    if legend:
        plt.legend()

    plt.title(title)
    plt.show()

def percentage(ax, total):
    for p in ax.patches:
        percentage = '{:.1f}%'.format(100 * p.get_width()/total)
        x = p.get_x() + p.get_width() + 0.02
        y = p.get_y() + p.get_height()/2
        ax.annotate(percentage, (x, y))


############################
"""
### COMPARE_FIG ###
def mul_fig(row, column, figsize= (20, 4), axis_visible =  False, figs = *fig):

    plt.figure(figsize=figsize)

    for i in range(1,column+1):
        for j in range(row):
            ax = plt.subplot(row, column, i)
            plt.imshow(fig[i][j])
            plt.gray()
            ax.get_xaxis().set_visible(axis_visible)
            ax.get_yaxis().set_visible(axis_visible)

    plt.show()
"""
