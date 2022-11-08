

# %%
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import os
from plotly.subplots import make_subplots
import matplotlib.lines as mlines

# %%
# Parameters
main_dir = '/Users/h/Dropbox/projects_dropbox/other_sideprojects/green_climatechange/fig9_oct31'
co2_df = pd.read_csv(os.path.join(main_dir, 'OUTPUT_g02_rank_city.csv'))
# co2_df = pd.read_csv(os.path.join(main_dir, 'INPUT_ohbm_171819_freqexpandrow.csv'))
# %%
co2_df['location'] = co2_df['location'].str.replace('_', ',')
# [x] TODO: Jan 14, convert kg to metric ton
# co2_df['co2_metricton'] = co2_df['co2']/3000
co2_df['co2_millionmetricton'] = (
    co2_df['weightedsum_co2ton'] * 1/1000000).round(decimals=2) # thousand metric ton
co2_df['co2_thousandmetricton'] = (
    co2_df['weightedsum_co2ton'] * 1/1000).round(decimals=2) # thousand metric ton

# https://coderzcolumn.com/tutorials/data-science/how-to-create-connection-map-chart-in-python-jupyter-notebook-plotly-and-geopandas

# %% sns barplot - 06/10/2022 ____________________________________

co2_top30 = co2_df.sort_values('weightedsum_co2ton', ascending=True).head(20)
co2_top30['labels'] = 'Best (top 20 most ideal)'
co2_bottom10 = co2_df.sort_values(
    'weightedsum_co2ton', ascending=False).head(10)
co2_bottom10['labels'] = 'Worst (bottom 10 least ideal)'
co2_bottom10.sort_values('weightedsum_co2ton', ascending=True, inplace=True)
co2_merge = pd.concat([co2_bottom10, co2_top30])
# co2_merge.drop(co2_merge.index[co2_merge['city'] == 'Tirana'], inplace=True)


sns.set_context('paper')
sns.set_style('whitegrid')
co2_sort = co2_merge.sort_values('weightedsum_co2ton', ascending=True)

f, ax = plt.subplots(figsize=(8, 6.8), dpi = 600)
sns.set_color_codes('pastel')
sns.set(font_scale=0.8)
colors = ['#FFA556' if (s == 'Worst (bottom 10 least ideal)')
          else '#6BBC6C' for s in co2_sort['labels']]
ax = sns.barplot(x='weightedsum_co2ton',
                 y='location',
                 data=co2_sort,
                 label='labels',
                 palette=colors,
                 edgecolor='w',
                 dodge=False
                 )




rects = ax.patches # add ticks inside

for rect in rects: # Place a label for each bar
    # Get X and Y placement of label from rect
    x_value = rect.get_width()
    y_value = rect.get_y() + rect.get_height() / 2
    space = -50 # Number of points between bar and label; change to your liking  
    ha = 'left' # Vertical alignment for positive values
    # If value of bar is negative: place label to the left of the bar
    if x_value < 0:
        space *= -.1 # Invert space to place label to the left
        ha = 'right' # Horizontally align label to the right

    label = '{:,.02f}'.format(x_value)     # Use X value as label and format number

    # Create annotation
    plt.annotate(
        label,                      # Use `label` as label
        (x_value, y_value),         # Place label at bar end
        xytext=(space, 0),          # Horizontally shift label by `space`
        textcoords='offset points',  # Interpret `xytext` as offset in points
        va='center',                # Vertically center label
        # Horizontally align label differently for positive and negative values
        ha=ha,
        color='white', 
        weight="bold")            # Change label color to white
#ax.set_ylim(30, -1)
ax.set_xlim(0, 35000)
ax.tick_params(axis='y', labelrotation=20)

green_square = mlines.Line2D([0], [0],
                             color='#6BBC6C',
                             marker='s',
                             markeredgecolor='black',
                                                          linestyle='None',
                             markersize=10,
                             label='TOP 20 mimimum emission')
orange_square = mlines.Line2D([0], [0],
                              color='#FFA556',
                              marker='s',
                              markeredgecolor='black',
                              linestyle='None',
                              markersize=10,
                              label='BOTTOM 10 maximum emmision')
h, l = ax.get_legend_handles_labels()
ax.legend(h,
          title='',
          loc='upper right',
          #labels=['TOP 20 mimimum emission', 'bottom 10 maximum emmision'],
          handles=[green_square, orange_square],
          facecolor = 'white')

leg = ax.get_legend()
leg.legendHandles[0].set_color('#6BBC6C')
leg.legendHandles[1].set_color('#FFA556')
ax.set_xlabel(
    "Emissions \n(metric tons of carbon dioxide equivalents)", fontsize=13)
ax.set_ylabel("Destination location \n(city, country)", fontsize=13)
sns.despine()
plt.tight_layout()

# ax.relim()
ax.autoscale_view()
ax.margins(y=0.0001)
plt.show()
f.savefig(os.path.join(main_dir, 'OUTPUT_co2_per_city.png'))
# %%
# visualize
# http://www.carbonvisuals.com/projects/new-yorks-carbon-emissions-in-real-time
# https://stackoverflow.com/questions/47391702/how-to-make-a-colored-markers-legend-from-scratch