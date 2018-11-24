# -*- coding: utf-8 -*-
"""
Created on Wed Nov 21 16:19:38 2018

@author: nathaniel evans
@prof: mike mooney 
@class: bmi665
#hw: 6 

$ wget https://sakai.ohsu.edu/access/content/group/BMI-565-665-DL-F18/Week%208/heart.dat ./data/ # didn't work (pulled html, not data), ended up just copying from browser
"""
import pandas as pd 
from matplotlib import pyplot as plt 
import seaborn as sns 
import numpy as np 
from scipy.stats import norm


HRT_DATA_URL = 'https://sakai.ohsu.edu/access/content/group/BMI-565-665-DL-F18/Week%208/heart.dat'

 
def read_data(): 
    
    
    # Column Names to pass to read_csv()
    names = ["age", "sex", "pain_type", "resting_bp", "chol", "fast_sugar", "ekg", "max_hr", "angina", "old_peak", "peak_slope", "n_major", "thal", "hdd"]
    
    data = pd.read_csv('./data/heart.dat', sep=' ', names=names)

    return data 

def plot_kde(x0, ax): 
    
    sns.kdeplot(x0, ax=ax)
    
    mu,std = norm.fit(x0)
    xmin, xmax = ax.get_xlim()
    x = np.linspace(xmin, xmax, num=len(x0))
    p = norm.pdf(x, mu, std)
    ax.plot(x, p)



if __name__ == '__main__' : 
    
    
    ''' 1. Read the data into a Pandas data frame. ''' 
    heart = read_data()

    ''' 2. Select all continuous variables (those labeled as ‘Real’ in the table below) in the data frame and visualize their correlation matrix. '''
    
    real = ['age', 'resting_bp', 'chol', 'max_hr', 'old_peak', 'n_major']
    
    real_df = heart[real]
    corr = real_df.corr() 
    
    mask = np.zeros_like(corr, dtype=np.bool)
    mask[np.triu_indices_from(mask)] = True
    cmap = sns.diverging_palette(220, 10, as_cmap=True)
    
    f, ax = plt.subplots(figsize=(11, 9))
    
    sns.heatmap(corr, mask=mask, cmap=cmap, annot=True, vmax=.3, center=0,
            square=True, linewidths=.5, cbar_kws={"shrink": .5})
    
    
    ''' 3. Identify the three variables with a high correlation (absolute value > 0.2) with the dependent variable (‘old_peak’; column 10). '''
    
    # n_major : age (+) - 0.36
    # old_peak : max_hr (-) - 0.35
    # max_hr : age (-) - 0.4

    ''' 4. Check whether the variables’ distributions appear normal using a KDE plot. ''' 
    
    f, ((ax1, ax2), (ax3, ax4)) = plt.subplots(nrows = 2, ncols = 2, figsize=(11, 9), sharex=False)
    
    f.suptitle('Population Distribution')
    
    plot_kde(real_df['n_major'], ax= ax1)   
    plot_kde(real_df['age'], ax= ax2)
    plot_kde(real_df['max_hr'], ax= ax3)
    plot_kde(real_df['old_peak'], ax= ax4)

    ''' 5. Run a univariate linear regression analysis for each variable, with ‘old_peak’ as the dependent variable, using the statsmodels package. Visualize each regression using a joint plot. '''


    ''' 6. Create a multiple regression model using the three variables. How does it perform?  '''
    