import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import ttest_rel, ttest_1samp
import time

df = pd.read_csv("programs/Final_Data_Updated_09_02.csv")
def plot_line(col):
    plt.style.use('fivethirtyeight')
    temp_df = df[[col+'_Goqii', col+'_Hospital', 'Abs_'+col+'_Diff', 'Mean_'+col]]
    temp_df['Mean_'+col] = np.floor(temp_df['Mean_'+col])
    temp_mean = temp_df[['Abs_'+col+'_Diff', 'Mean_'+col]].groupby('Mean_'+col, sort=True, as_index=False).mean()
    plt.figure(figsize=(16, 12))
    plt.plot(temp_mean['Mean_'+col].values, temp_mean['Abs_'+col+'_Diff'].values, marker='o')
    plt.title(f'{col} Vs Mean Absolute {col} Difference', fontsize=30)
    plt.xlabel(f'{col}', fontsize=25)
    plt.ylabel(f"Mean Absolute {col} Difference", fontsize=25)
    plt.xticks(fontsize=18)
    plt.yticks(fontsize=18)
    new_graph_name = col+"_" + str(time.time()) + ".png"
    plt.savefig('static/img/'+ new_graph_name)
    new_graph_name = 'static/img/' + new_graph_name
    return new_graph_name

def plot_hist(col):
    fig, (ax1, ax2) = plt.subplots(1,2, figsize=(16, 12))
    temp1 = np.floor(df[col+'_Goqii'])
    ax1.hist(temp1, edgecolor='black', bins=7)
    for p in ax1.patches:
        ax1.annotate(np.round(p.get_height(), decimals=2),
                (p.get_x()+p.get_width()/2, p.get_height()),
                ha='center', va='center', xytext=(0,10), textcoords='offset points', fontsize=15)
    ax1.set_xlabel(f'{col}_Goqii', fontsize=25)
    ax1.set_ylabel("Frequency", fontsize=25)
    ax1.set_title("HISTOGRAM", fontsize=30)
    ax1.tick_params(axis="x", labelsize=20)
    ax1.tick_params(axis="y", labelsize=20)
    temp2 = np.floor(df[col+'_Hospital'])
    ax2.hist(temp2, edgecolor='black', bins=7)
    for p in ax2.patches:
        ax2.annotate(np.round(p.get_height(), decimals=2),
                (p.get_x()+p.get_width()/2, p.get_height()),
                ha='center', va='center', xytext=(0,10), textcoords='offset points', fontsize=15)
    ax2.set_xlabel(f'{col}_Hospital', fontsize=25)
    ax2.set_ylabel("Frequency", fontsize=25)
    ax2.set_title("HISTOGRAM", fontsize=30)
    ax2.tick_params(axis="x", labelsize=15)
    ax2.tick_params(axis="y", labelsize=15)

    new_graph_name1 = col+"_" + str(time.time()) + ".png"
    plt.savefig('static/img/'+ new_graph_name1)
    print(new_graph_name1)
    return 'static/img/'+new_graph_name1

def plot_bland(col):
    plt.figure(figsize=(16, 12))
    data1     = np.asarray(df[col+'_Goqii'])
    data2     = np.asarray(df[col+'_Hospital'])
    mean      = np.mean([data1, data2], axis=0)
    diff      = data1 - data2                   # Difference between data1 and data2
    md        = np.mean(diff)                   # Mean of the difference
    sd        = np.std(diff, axis=0)            # Standard deviation of the difference
    plt.scatter(mean, diff)
    plt.axhline(md,           color='gray', linestyle='--')
    plt.axhline(md + 1.96*sd, color='gray', linestyle='--')
    plt.axhline(md - 1.96*sd, color='gray', linestyle='--')
    plt.xlabel(f"Mean {col}", fontsize=25)
    plt.ylabel(f"{col} Difference", fontsize=25)
    plt.title(f"Bland-Altman - {col}", fontsize=30)
    plt.xticks(fontsize=18)
    plt.yticks(fontsize=18)
    new_graph_name2 = col+"_" + str(time.time()) + ".png"
    plt.savefig('static/img/'+ new_graph_name2)
    new_graph_name2 = 'static/img/' + new_graph_name2
    return new_graph_name2