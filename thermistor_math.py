#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 17 13:51:54 2020

@author: aryeh
"""
import numpy as np
import pandas as pd
import plotly.express as px
from plotly.offline import plot
import plotly.graph_objects as go


def get_resistance(temp_percent, r=46000):
    return r*temp_percent/(1-temp_percent)




def get_temp(R, old_new):
    
    if old_new=='old':
    # old thermistors
        A = 0.6872188391*10**-3
        B = 2.103627383*10**-4
        C = 0.5449073998*10**-7
    else:
        # new thermistors
        A = 1.216527419*10**-3
        B = 1.337979364*10**-4
        C = 3.947291334*10**-7

    T = (A +B*np.log(R)+C*(np.log(R)**3) )**-1
    T = T*(9/5) - 459.67
    
    return(T)


x = np.linspace(.01,.99,200)
fig = go.Figure()
base_r = 46000

for o in ['old', 'new']:
    y=[]
    for i in x:
        y.append(get_temp(get_resistance(i), old_new=o))
        
        fig.add_trace(
            go.Scatter(
                x=y
                ,y=x
                ,mode='lines'
                ,name='{}'.format(o)
                )
            )



plot(fig)

# plot(px.line(x=x,y=y))


# x = 
# get_temp






