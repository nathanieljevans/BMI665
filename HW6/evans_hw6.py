# -*- coding: utf-8 -*-
"""
Created on Wed Nov 21 16:19:38 2018

@author: nathaniel evans
@prof: mike mooney 
@class: bmi665
#hw: 6 

$ wget https://sakai.ohsu.edu/access/content/group/BMI-565-665-DL-F18/Week%208/heart.dat ./data/ # didn't work (pulled html, not data), ended up just copying from browser

Run this program by navigating to script and running: 
    $ python3 evans_hw6.py 
    
There must be two directories with the script: 
    /outputs/
    /data/
        /heart.dat 
        
The purpose of this script is to run a data analysis on the heart.dat dataset. 
"""

import pandas as pd 
from matplotlib import pyplot as plt 
import seaborn as sns 
import numpy as np 
from scipy.stats import norm
import statsmodels.api as sm

HRT_DATA_URL = 'https://sakai.ohsu.edu/access/content/group/BMI-565-665-DL-F18/Week%208/heart.dat'
 
def read_data(): 
    '''
    reads the space delimited file into memory and returns a pandas dataframe. 
    File located in ./data/heart.dat
    
    inputs:
        None
        
    ouputs 
        pandas dataframe representing heart data
    '''
    # Column Names to pass to read_csv()
    names = ["age", "sex", "pain_type", "resting_bp", "chol", "fast_sugar", "ekg", "max_hr", "angina", "old_peak", "peak_slope", "n_major", "thal", "hdd"]
    
    data = pd.read_csv('./data/heart.dat', sep=' ', names=names)

    return data 

def plot_kde(x0, ax): 
    '''
    plots the x0 data to the given axes object with a scaled normal pdf distribution superimposed for comparison. 
    
    inputs 
        x0 <list of numerics> data to be converted to pdf and plotted 
        ax <Axes obj> the axes to be plotted, allows for convenient subplotting 
        
    outputs 
        None 
    '''
    sns.kdeplot(x0, ax=ax)
    
    mu,std = norm.fit(x0)
    xmin, xmax = ax.get_xlim()
    x = np.linspace(xmin, xmax, num=len(x0))
    p = norm.pdf(x, mu, std)
    ax.plot(x, p)

# Data Analysis Script 
if __name__ == '__main__' : 
    
    ''' 1. Read the data into a Pandas data frame. ''' 
    heart = read_data()

    ''' 2. Select all continuous variables (those labeled as ‘Real’ in the table below) in the data frame and visualize their correlation matrix. '''
    
    real = ['age', 'resting_bp', 'chol', 'max_hr', 'old_peak', 'n_major']
    
    # select data labeled as 'real' 
    real_df = heart[real]
    
    # generate correllation matrix 
    corr = real_df.corr() 
    
    # mask the upper triangle for pretty plotting and add different color scheme 
    mask = np.zeros_like(corr, dtype=np.bool)
    mask[np.triu_indices_from(mask)] = True
    cmap = sns.diverging_palette(220, 10, as_cmap=True)
    
    # plot correllation matrix as a labeled heat map
    f, ax = plt.subplots(figsize=(11, 9))
    sns.heatmap(corr, mask=mask, cmap=cmap, annot=True, vmax=.3, center=0,
            square=True, linewidths=.5, cbar_kws={"shrink": .5})
    
    f.savefig('./outputs/var_corr_matrix.png')
    
    ''' 3. Identify the three variables with a high correlation (absolute value > 0.2) with the dependent variable (‘old_peak’; column 10). '''

    # old_peak ~ [max_hr, age, resting_bp]    

    ''' 4. Check whether the variables’ distributions appear normal using a KDE plot. ''' 
    
    f, ((ax1, ax2), (ax3, ax4)) = plt.subplots(nrows = 2, ncols = 2, figsize=(11, 9), sharex=False)
    
    f.suptitle('Population Distribution')
    
    plot_kde(real_df['max_hr'], ax= ax1)   
    plot_kde(real_df['age'], ax= ax2)
    ax2.set_ylim( (0,0.05) ) # normal dist overlay is a little taller 
    plot_kde(real_df['resting_bp'], ax= ax3)
    plot_kde(real_df['old_peak'], ax= ax4)
    
    f.savefig('./outputs/variable_pdf.png')
    
    ''' 5. Run a univariate linear regression analysis for each variable, with ‘old_peak’ as the dependent variable, using the statsmodels package. Visualize each regression using a joint plot. '''
    
    # old_peak ~ max_hr / chol / resting_bp
    Y = real_df['old_peak']
    
    dep = ['max_hr', 'age', 'resting_bp']
    
    Xs = [sm.add_constant(real_df[d], prepend=False) for d in dep]
    
    models = [sm.OLS(Y, x) for x in Xs]
    
    [(open('./outputs/sum_%s.txt' %(dep[i]),  'w').write(str(mod.fit().summary()))) for i,mod in enumerate(models)] # is this leaving open file handles or does garbage collection close them since there is no assigned handle ? 
    
    [sns.jointplot(d, 'old_peak', data=real_df, kind='reg').savefig('./outputs/regression_%s' %(d)) for d in dep]

    ''' 6. Create a multiple regression model using the three variables. How does it perform?  '''
    
    # There is colinearity between these variables
    X = sm.add_constant(real_df[dep], prepend=False)
    
    mod = sm.OLS(Y, X) 
    fit = mod.fit() 
    with open('./outputs/full_model_summary.txt' , 'w') as f: 
        f.write(str(fit.summary()))
        
    
    