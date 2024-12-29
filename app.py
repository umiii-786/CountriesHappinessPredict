import streamlit as st 
import pandas as pd
import numpy as np 




analysis_page=st.Page(
    page="views/Analysis.py",
    default=True,
    title="Analysis",
    icon=':material/bar_chart:'
)

formpage=st.Page(page="views/formData.py",
                 title="Predict",
                 icon=':material/dynamic_form:'
                 )


navigate=st.navigation(pages=[analysis_page,formpage])
navigate.run()