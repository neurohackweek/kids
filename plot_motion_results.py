import numpy as np
import os
import pandas as pd
import nibabel as nib

from bokeh.io import curdoc, output_notebook, output_file, push_notebook
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, DataRange1d, Range1d, VBox, HBox, Select
from bokeh.palettes import Blues4
from bokeh.plotting import Figure, show
from scipy.signal import savgol_filter
from ipywidgets import interact, FloatSlider

output_notebook()

def get_dataset(src, samplesize, lowerage, upperage):
    src['ci'] = zip(src[y] + src[variance]/2, src[y] - src[variance]/2)
    src['ci_x'] = zip(src[x], src[x])
    df = src[(src.SampleSize == int(samplesize)) & (src.LowerAge >= int(lowerage)) & (src.UpperAge <= int(upperage))].copy()
    df = df.set_index([x])
    df.sort_index(inplace=True)
    return ColumnDataSource(data=df)

def make_plot(source, title):
    plot = Figure(plot_width=800, plot_height=600, tools="", toolbar_location=None)
    plot.title.text = title
    colors = Blues4[0:3]

    plot.scatter(x=x, y=y, source=source)
    plot.multi_line('ci_x', 'ci', source=source)

    # fixed attributes
    plot.xaxis.axis_label = xlabel
    plot.yaxis.axis_label = ylabel
    plot.axis.major_label_text_font_size = "8pt"
    plot.axis.axis_label_text_font_size = "8pt"
    plot.axis.axis_label_text_font_style = "bold"

    return plot
def update_plot(N, min_age, max_age):
    plot.title.text = "Motion for sample size " + str(N) + ", ages " + str(min_age) + "-" + str(max_age)
    src = get_dataset(df, N, min_age, max_age)
    source.data.update(src.data)
    push_notebook()
    
samplesize = df.SampleSize.max()
lowerage = df.LowerAge.min()
upperage = df.UpperAge.max()

def getspacing(alist):
    azip=zip(alist[1:], alist[:-1])
    thediffs=[q[0]-q[1] for q in azip]
    uniquediffs=list(set(thediffs))
    nonzerodiffs=uniquediffs[uniquediffs != 0]
    if (hasattr(nonzerodiffs, '__len__')) or (isinstance(nonzerodiffs, str)):
        nonzerodiffs=-1
    return(nonzerodiffs)
sampleSpacing=getspacing(df.SampleSize)

samplesize_widget = FloatSlider(min=df.SampleSize.min(), max=df.SampleSize.max(), step=sampleSpacing, value=samplesize)
lowerage_widget = FloatSlider(min=df.LowerAge.min(), max=df.LowerAge.max(), step=1, value=lowerage)
upperage_widget = FloatSlider(min=df.UpperAge.min(), max=df.UpperAge.max(), step=1, value=upperage)

def update_upperage_range(*args):
    if lowerage_widget.value > upperage_widget.value:
        upperage_widget.value = lowerage_widget.value
lowerage_widget.observe(update_upperage_range, 'value')
def update_lowerage_range(*args):
    if upperage_widget.value < lowerage_widget.value:
        lowerage_widget.value = upperage_widget.value
upperage_widget.observe(update_lowerage_range, 'value')

source = get_dataset(df, samplesize, lowerage, upperage)
plot = make_plot(source, "Motion for sample size " + str(samplesize) + ", ages " + str(lowerage) + "-" + str(upperage))
show(plot, notebook_handle=True)

interact(update_plot, N=samplesize_widget, min_age=lowerage_widget, max_age=upperage_widget)

