import json
import streamlit as st 
from streamlit_elements import mui
from .dashboard import Dashboard
import pandas as pd 

class DataGrid2(Dashboard.Item):

    df = pd.DataFrame(dict(
                    Time = ['08:00', '08:10', '08:20', '08:30', '08:40', '08:50', 
                    '09:00', '09:10', '09:20', '09:30', '09:40', '09:50', 
                    '10:00', '10:10', '10:20', '10:30', '10:40', '10:50', 
                    '11:00', '11:10', '11:20', '11:30', '11:40', '11:50'],
                    Temperatures = [20, 20.1, 20.1, 20.4, 20.5, 20.6,
                    21, 21.1, 20, 21.4, 20.5, 20.6,
                    22, 22, 21.6, 21.4, 22.5, 21.9,
                    22.5, 22.7, 22.3, 23, 23.2, 23.6],
                    Populations = [8, 8, 5, 5, 5, 5,
                    5, 5, 5, 5, 5, 5,
                    6, 6, 8, 8, 10, 10,
                    6, 6, 6, 6, 7+6, 7+6
                    ],
                    ))

    def _handle_edit(self, params):
        print(params)

    def __call__(self):
        m
        st.table(self.df)
