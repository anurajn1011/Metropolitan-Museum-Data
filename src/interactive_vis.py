'''
interactive_vis.py

Python file for building cross-department and
department-specific visualizations based on the Met
Database

Created: November 18th 2025
'''

# imports
import pandas as pd
import numpy as np
import sqlite3
import plotly.express as px
import ipywidgets as widgets
from ipywidgets import interact
from skimage import io


# set up connecting to the met database
conn = sqlite3.connect("met_data/met.db")
cursor = conn.cursor()

# pull categorical data types for further visualization
categorical = ['isHighlight', 'isPublicDomain', 'country', 'classification']

# pull in department names for future visualizations
department_names = pd.read_sql('''SELECT displayName FROM Department WHERE department_id IN (SELECT department_id
                               FROM Objects)''', conn)


# helper functions
def one_p_filter(pie_df, field):
    '''collapses the entries in the given field to Other for entries under 1%'''
    if type(pie_df.dtypes[field]) is str or type(pie_df.dtypes[field]) == np.dtypes.ObjectDType:
        cutoff = sum(pie_df['num_objects']) * 0.01
        pie_df.loc[pie_df['num_objects'] < cutoff, field] = "Other " + field
    return pie_df.copy()


def select_dept_field(dept, field, filter_1_p):
    '''filters the met db by the department and groups by field. can optionally roll up groups with under 1% of the total count'''
    conn = sqlite3.connect("met_data/met.db")
    cursor = conn.cursor()
    pie_data = pd.read_sql(f'''SELECT a.{field}, COUNT(*) as num_objects 
                           FROM Art a, Objects o, Department d WHERE d.displayName="''' + dept +  f'''" AND a.object_id=o.object_id 
                           AND o.department_id=d.department_id GROUP BY {field}''', conn)
    
    # filter if a categorical type rather than boolean
    if field in ("isHighlight", "isPublicDomain"):
        pie_data[field] = pie_data[field].map({0:"No", 1:"Yes"})
    elif filter_1_p:
        pie_data= one_p_filter(pie_data, field)
    
    fig = px.pie(pie_data, values='num_objects', names=field, title=f'{dept} Department {field} Breakdown')
    fig.show()
    conn.close()



def create_box_chart():
    '''groups met data by department and plots the creation year of the art'''
    conn = sqlite3.connect("met_data/met.db")
    cursor = conn.cursor()
    create_years = pd.read_sql('''
        SELECT CAST(a.objectBeginDate as integer) as earliest, CAST(a.objectEndDate as integer) as latest, 
                               d.displayName FROM Art a, Department d, Objects o WHERE a.object_id=o.object_id
                                AND o.department_id=d.department_id AND CAST(a.objectBeginDate as integer)!= 0 
                                AND CAST(a.objectEndDate as integer) <= 2025
        ''', conn)

    fig = px.box(create_years, x='earliest', y='displayName', title='Creation Year of the Art Objects per Department')
    fig.update_layout(xaxis_title='Creation Year')
    fig.show()
    conn.close()


def acq_bar_chart():
    '''groups met data by department and pltos the acquistion years'''
    conn = sqlite3.connect("met_data/met.db")
    cursor = conn.cursor()
    accquision_years = pd.read_sql('''
            SELECT CAST(a.accessionYear as integer) as accessionYear, d.displayName FROM Art a, 
            Department d, Objects o WHERE a.object_id=o.object_id AND o.department_id=d.department_id
             AND CAST(a.accessionYear as integer)!=0
        ''', conn)
    
    fig = px.histogram(accquision_years, x='accessionYear', color='displayName', title='Accession Year by Department', nbins=20)
    fig.update_layout(bargap=0.2, yaxis_title='Number of Art Objects')
    fig.show()
    conn.close()



def show_highlights(play, dept):
    '''pulls Art Objects with an available image and tagged as highlights of the collection and plots it'''
    conn = sqlite3.connect("met_data/met.db")
    cursor = conn.cursor()
    image_available = pd.read_sql(f'''SELECT *
                           FROM Art a, Objects o, Department d WHERE d.displayName="''' + dept +  f'''" AND a.object_id=o.object_id 
                           AND o.department_id=d.department_id AND primaryImage NOT LIKE "Unknown" AND isHighlight=1''', conn)
    
    # Allows the animation to loop over the list without knowing the exact length
    curr_index = play % len(image_available)

    # reads the image
    f = io.imread(image_available.iloc[curr_index]['primaryImage'])

    # dynamic title set
    title = f'''{image_available.iloc[curr_index]['title']}<br>
    {image_available.iloc[curr_index]['objectBeginDate']} - {image_available.iloc[curr_index]['objectEndDate']}<br>
    {image_available.iloc[curr_index]['artistAlphaSort']}'''

    # read the image file into a plotly figure
    fig = px.imshow(f, title=title)
    fig.update_xaxes(showticklabels=False)
    fig.update_yaxes(showticklabels=False)
    fig.update_layout(title_x=0.5)
    fig.show()
    conn.close()

# create the interactive pie chart
interactive_pie = widgets.interactive(select_dept_field, 
    dept= widgets.Dropdown(
        options=department_names['displayName'].to_list(),
        value='The Cloisters',
        description='Department:',
        disabled=False), 
    field=widgets.ToggleButtons(
        options=categorical,
        description='Field of Interest:',
        disabled=False),
    filter_1_p= widgets.Checkbox(
        value=False,
        description='Collapse values under 1%?',
        disabled=False,
        button_style='success',
        tooltip='Description',
        icon='check' #
    ))

# creates the interactive slideshow
interactive_slideshow = widgets.interactive(show_highlights, play=widgets.Play(
    value=0,
    min=0,
    max=1000,
    step=1,
    interval=5000,
    description="Press play",
    disabled=False),
        dept= widgets.Dropdown(
        options=department_names['displayName'].to_list(),
        value='The Cloisters',
        description='Department:',
        disabled=False))
