import matplotlib.pyplot as plt
from matplotlib.figure import Figure

def labelFreqFig(data):
    labels = ['positive', 'negative']
    positives = 0
    negatives = 0
    total = len(data.keys())
    for value in data.items():
        if value == 'positive':
            positives += 1
        else:
            negatives += 1
    values = [float(positives/total) * 100, float(negatives/total) * 100]
    fig = Figure()
    ax1 = fig.subplots()
    ax1.pie(values, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
    ax1.axis('equal')
    return fig