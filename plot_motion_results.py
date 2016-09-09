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
from ipywidgets import interact

output_notebook()

def plot_motion_results(df, x, y, variance, xlabel, ylabel):
    """
    This function should plot a plot with widgets.
    
    Args:
        df (Pandas data frame): This is the filename to a pandas data frame. df MUST include columns named `SampleSize`, `LowerAge`, `UpperAge`.
        x (str): Name of the column for the x axis
        y (str): Name of the column for the y axis
        variance (str): Name of the column for the error bar (it is the full width, not half).
    Returns:
        None    
    """
        #for col in df.columns:
    #    print(col)
    diagnosis_dict = {
        "Control" : 0,
        "Autism" : 1,
        "Aspergers" : 2,
        "PDD-NOS" : 3,
        "Aspergers or PDD-NOS" : 4
    }
    diagnosis_dict.keys()
    def get_dataset(src, diagnosis, age_range):
        src['ci'] = zip(src[y] + src[variance]/2, src[y] - src[variance]/2)
        src['ci_x'] = zip(src[x], src[x])
        df = src[src.DSM_IV_TR == diagnosis_dict[diagnosis]].copy()
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
    def update_plot(diagnosis, age_range):
        plot.title.text = diagnosis
        src = get_dataset(df, diagnosis, age_range)
        source.data.update(src.data)
        push_notebook()
    diagnosis = 'Control'
    age_range = 6
    source = get_dataset(df, diagnosis, age_range)
    plot = make_plot(source, diagnosis)
    layout = column(plot)
    show(layout, notebook_handle=True)
    interact(update_plot, diagnosis=diagnosis_dict.keys(), age_range=(6,19,2))
    