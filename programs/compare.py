import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import ttest_rel, ttest_1samp
import time

def line(file1, file2):
    plt.style.use('fivethirtyeight')

    col1 = file1.iloc[:, 1]
    col2 = file2.iloc[:, 1]
    dev1 = file1.iloc[:, 0].values
    col1_name = list(file1.columns)[1]
    col2_name = list(file2.columns)[1]
    plt.figure(figsize=(16, 12))
    plt.plot(dev1, col1.values, marker='+')
    plt.plot(dev1, col2.values, marker='o')
    plt.title(f'{col1_name} vs {col2_name}', fontsize=30)
    plt.xlabel(f'Device', fontsize=25)
    plt.ylabel(f'Parameter', fontsize=25)
    plt.xticks(fontsize=18)
    plt.yticks(fontsize=18)
    plt.legend(loc='best', labels=[col1_name, col2_name], prop={'size': 16})
    new_graph_name = 'Line_' + str(time.time()) + ".png"
    plt.savefig('static/img/'+ new_graph_name)
    new_graph_name = 'static/img/' + new_graph_name
    return new_graph_name

def hist(file1, file2):
    fig, (ax1, ax2) = plt.subplots(1,2, figsize=(16, 12))
    col1 = file1.iloc[:, 1].values
    col2 = file2.iloc[:, 1].values
    ax1.hist(col1, edgecolor='black', bins=7)
    for p in ax1.patches:
        ax1.annotate(np.round(p.get_height(), decimals=2),
                (p.get_x()+p.get_width()/2, p.get_height()),
                ha='center', va='center', xytext=(0,10), textcoords='offset points', fontsize=15)
    ax1.set_xlabel(f'Parameter 1', fontsize=25)
    ax1.set_ylabel("Frequency 1", fontsize=25)
    ax1.set_title("HISTOGRAM 1", fontsize=30)
    ax1.tick_params(axis="x", labelsize=20)
    ax1.tick_params(axis="y", labelsize=20)
    ax2.hist(col2, edgecolor='black', bins=7)
    for p in ax2.patches:
        ax2.annotate(np.round(p.get_height(), decimals=2),
                (p.get_x()+p.get_width()/2, p.get_height()),
                ha='center', va='center', xytext=(0,10), textcoords='offset points', fontsize=15)
    ax2.set_xlabel(f'Parameter 2', fontsize=25)
    ax2.set_ylabel("Frequency 2", fontsize=25)
    ax2.set_title("HISTOGRAM 2", fontsize=30)
    ax2.tick_params(axis="x", labelsize=15)
    ax2.tick_params(axis="y", labelsize=15)

    new_graph_name1 = "Histogram_" + str(time.time()) + ".png"
    plt.savefig('static/img/'+ new_graph_name1)
    print(new_graph_name1)
    return 'static/img/'+new_graph_name1

def bland(file1, file2):
    plt.figure(figsize=(16, 12))
    col1 = file1.iloc[:, 1].values
    col2 = file2.iloc[:, 1].values
    data1     = np.asarray(col1)
    data2     = np.asarray(col2)
    mean      = np.mean([data1, data2], axis=0)
    diff      = data1 - data2                   # Difference between data1 and data2
    md        = np.mean(diff)                   # Mean of the difference
    sd        = np.std(diff, axis=0)            # Standard deviation of the difference
    plt.scatter(mean, diff)
    plt.axhline(md,           color='gray', linestyle='--')
    plt.axhline(md + 1.96*sd, color='gray', linestyle='--')
    plt.axhline(md - 1.96*sd, color='gray', linestyle='--')
    plt.xlabel(f"Mean of Parameter Values ", fontsize=25)
    plt.ylabel(f"Difference between Parameter Values", fontsize=25)
    plt.title(f"Bland-Altman ", fontsize=30)
    plt.xticks(fontsize=18)
    plt.yticks(fontsize=18)
    new_graph_name2 = 'Bland_' + str(time.time()) + ".png"
    plt.savefig('static/img/'+ new_graph_name2)
    new_graph_name2 = 'static/img/' + new_graph_name2
    return new_graph_name2