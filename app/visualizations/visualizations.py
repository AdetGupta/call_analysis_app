import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def get_data():
    base_path = os.path.dirname(__file__)
    path_to_csv = os.path.join(base_path, "data/call_metrics.csv")
    df = pd.read_csv(path_to_csv)
    return df


def generate_bar():
    df = get_data()

    # Select columns
    df_overtalk = df[['Agent_overtalk', 'Customer_overtalk']]
    df_silence = df[['Agent_silence', 'Customer_silence']]

    # Create figure with 2 subplots
    fig, axes = plt.subplots(2, 1, figsize=(15, 10))  # 2 rows, 1 column

    # Plot overtalk
    df_overtalk.plot(kind='bar', stacked=True, ax=axes[0])
    axes[0].set_title("Agent vs Customer Overtalk per Call")
    axes[0].set_ylabel("Percentage")
    axes[0].set_xticklabels([])  # remove crowded x-ticks

    # Plot silence
    df_silence.plot(kind='bar', stacked=True, ax=axes[1])
    axes[1].set_title("Agent vs Customer Silence per Call")
    axes[1].set_ylabel("Percentage")
    axes[1].set_xticklabels([])  # remove crowded x-ticks

    plt.tight_layout()  # avoid overlap
    plt.show()

def generate_box():
    cols = ['Agent_overtalk', 'Customer_overtalk', 'Agent_silence', 'Customer_silence']
    df = get_data()
    sns.boxplot(data=df[cols])
    plt.title("Distribution of Overtalk and Silence")
    plt.ylabel("Percentage")
    plt.show()


if __name__ == '__main__':
    generate_box()
    generate_bar()

