import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def save_plot(filename):
    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    plt.close()



files = [
    'large_high',
    'large_baseline',
    'medium_high',
    'medium_baseline',
]

paths = [
    './large/highMemory',
    './large/baseline',
    './medium/highMemory',
    './medium/baseline',
]


def createPlots(location, filename):
    # Load dataset
    data = pd.read_csv(f'{filename}.csv')

    # Convert columns to proper data types if necessary
    data['ExecutionTime_ms'] = pd.to_numeric(
        data['ExecutionTime_ms'], errors='coerce')

    print(data.head())

    plt.figure(figsize=(8, 5))
    for strategy in data['IndexStrategy'].unique():
        subset = data[data['IndexStrategy'] == strategy]
        sns.histplot(subset['ExecutionTime_ms'], label=strategy, kde=True, bins=30,
                     alpha=0.6)
        plt.title(
            'Histogram of Query Execution Times Under Different Indexing Strategies')
        plt.xlabel('Execution Time (ms)')
        plt.ylabel('Frequency')
        plt.legend(title='Indexing Strategy')

    save_plot(f'{location}_histogram.png')
    plt.show()

    sns.boxplot(x='IndexStrategy', y='ExecutionTime_ms', data=data)
    plt.title('Box Plot of Execution Times by Indexing Strategy')
    plt.xlabel('Indexing Strategy')
    plt.ylabel('Execution Time (ms)')
    plt.xticks(rotation=30)
    save_plot(f'{location}_boxplot.png')
    plt.show()

    sns.scatterplot(x='Query', y='ExecutionTime_ms',
                    hue='IndexStrategy', data=data)
    plt.title('Execution Time vs. Query Type by Indexing Strategy')
    plt.xlabel('Query')
    plt.ylabel('Execution Time (ms)')
    save_plot(f'{location}_scatterplot.png')
    plt.show()

    mean_exec_time = data.groupby(['IndexStrategy', 'Query'])[
        'ExecutionTime_ms'].mean().reset_index()
    # Line Plot of Mean Execution Time Across Configurations
    sns.lineplot(x='Query', y='ExecutionTime_ms', hue='IndexStrategy',
                 data=mean_exec_time)

    plt.title('Mean Execution Time per Query by Indexing Strategy')
    plt.xlabel('Query')
    plt.ylabel('Mean Execution Time (ms)')
    plt.legend(title='Indexing Strategy')
    save_plot(f'{location}_lineplot.png')
    plt.show()

    data['IndexStrategy'] = data['IndexStrategy'].astype('category')
    data['Query'] = data['Query'].astype('category')

    encoded_data = data.copy()
    encoded_data['IndexStrategy'] = encoded_data['IndexStrategy'].cat.codes
    encoded_data['Query'] = encoded_data['Query'].cat.codes
    # Calculate correlation matrix
    corr_matrix = encoded_data[['ExecutionTime_ms', 'IndexStrategy',
                                'Query']].corr()

    # Heatmap of Correlation Matrix
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')
    plt.title('Correlation Matrix Heatmap')
    save_plot(f'{location}_heatmap.png')
    plt.show()

    avg_exec_time = data.groupby(['Query', 'IndexStrategy'])[
        'ExecutionTime_ms'].mean().reset_index()
    sns.barplot(x='Query', y='ExecutionTime_ms', hue='IndexStrategy',
                data=avg_exec_time)
    plt.title('Average Execution Time per Query and Indexing Strategy')
    plt.xlabel('Query')
    plt.ylabel('Average Execution Time (ms)')
    plt.legend(title='Indexing Strategy')
    save_plot(f'{location}_barplot.png')
    plt.show()


for i in range(len(files)):
    createPlots(paths[i], files[i])
