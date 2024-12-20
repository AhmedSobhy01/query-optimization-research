import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from statsmodels.formula.api import ols
import statsmodels.api as sm
from scipy import stats
from statsmodels.stats.multicomp import pairwise_tukeyhsd

# Create output directories if they don't exist
os.makedirs("plots/medium_baseline", exist_ok=True)
os.makedirs("plots/medium_high", exist_ok=True)
os.makedirs("plots/large_baseline", exist_ok=True)
os.makedirs("plots/large_high", exist_ok=True)
os.makedirs("results", exist_ok=True)

datasets = {
    "medium_baseline": "medium_baseline.csv",
    "medium_high": "medium_high.csv",
    "large_baseline": "large_baseline.csv",
    "large_high": "large_high.csv",
}

for dataset_name, filename in datasets.items():
    # Read the CSV file
    df = pd.read_csv(filename)

    # Convert ExecutionTime_ms to numeric (in case it's not)
    df["ExecutionTime_ms"] = pd.to_numeric(df["ExecutionTime_ms"], errors="coerce")

    # Drop rows with NaN ExecutionTime_ms
    df = df.dropna(subset=["ExecutionTime_ms"])

    # Descriptive Statistics
    desc_stats = df.groupby(["Query", "IndexStrategy"])["ExecutionTime_ms"].agg(
        ["mean", "median", "std", "var", "min", "max", "count"]
    )
    desc_stats.to_csv(f"results/{dataset_name}_descriptive_statistics.csv")

    # Save central tendency and variability plots
    plt.figure(figsize=(12, 6))
    sns.boxplot(x="IndexStrategy", y="ExecutionTime_ms", hue="Query", data=df)
    plt.title(f"Execution Time Distribution - {dataset_name}")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f"plots/{dataset_name}/boxplot_execution_time.png")
    plt.close()

    # ANOVA
    # We will perform ANOVA for each Query separately
    anova_results = {}
    for query in df["Query"].unique():
        df_query = df[df["Query"] == query]
        model = ols("ExecutionTime_ms ~ C(IndexStrategy)", data=df_query).fit()
        anova_table = sm.stats.anova_lm(model, typ=2)
        anova_results[query] = anova_table
        # Save ANOVA table
        anova_table.to_csv(f"results/{dataset_name}_anova_{query}.csv")

        # Tukey's HSD test
        tukey = pairwise_tukeyhsd(
            endog=df_query["ExecutionTime_ms"],
            groups=df_query["IndexStrategy"],
            alpha=0.05,
        )
        # Save Tukey's test results
        with open(f"results/{dataset_name}_tukey_{query}.txt", "w") as f:
            f.write(str(tukey))

        # Plot Tukey's HSD results
        tukey.plot_simultaneous()
        plt.title(f"Tukey HSD - {dataset_name} - {query}")
        plt.xlabel("Execution Time Difference (ms)")
        plt.ylabel("Index Strategy Comparison")

        plt.tight_layout()
        plt.savefig(f"plots/{dataset_name}/tukey_{query}.png", bbox_inches='tight')
        plt.close()

    # Two-sample t-tests between indexing strategies for each query
    ttest_results = []
    index_strategies = df["IndexStrategy"].unique()
    for query in df["Query"].unique():
        df_query = df[df["Query"] == query]
        for i in range(len(index_strategies)):
            for j in range(i + 1, len(index_strategies)):
                idx_strat_1 = index_strategies[i]
                idx_strat_2 = index_strategies[j]
                group1 = df_query[df_query["IndexStrategy"] == idx_strat_1][
                    "ExecutionTime_ms"
                ]
                group2 = df_query[df_query["IndexStrategy"] == idx_strat_2][
                    "ExecutionTime_ms"
                ]
                t_stat, p_value = stats.ttest_ind(group1, group2, equal_var=False)
                ttest_results.append(
                    {
                        "Query": query,
                        "IndexStrategy1": idx_strat_1,
                        "IndexStrategy2": idx_strat_2,
                        "t_stat": t_stat,
                        "p_value": p_value,
                    }
                )
    ttest_df = pd.DataFrame(ttest_results)
    ttest_df.to_csv(f"results/{dataset_name}_ttest_results.csv", index=False)

    # Regression Analysis
    # Since both IndexStrategy and Query are categorical variables, we can proceed with the regression
    # and then perform diagnostics appropriate for categorical predictors

    # Encode categorical variables
    df["IndexStrategyCode"] = df["IndexStrategy"].astype("category").cat.codes
    df["QueryCode"] = df["Query"].astype("category").cat.codes

    # Regression model
    model = ols("ExecutionTime_ms ~ C(IndexStrategy) + C(Query)", data=df).fit()
    regression_summary = model.summary()
    # Save regression results
    with open(f"results/{dataset_name}_regression_summary.txt", "w") as f:
        f.write(str(regression_summary))

    # Regression Diagnostics
    # Plot residuals vs fitted
    plt.figure(figsize=(10, 6))
    plt.scatter(model.fittedvalues, model.resid)
    plt.xlabel("Fitted values")
    plt.ylabel("Residuals")
    plt.title(f"Residuals vs Fitted - {dataset_name}")
    plt.axhline(y=0, color="r", linestyle="--")
    plt.tight_layout()
    plt.savefig(f"plots/{dataset_name}/residuals_vs_fitted.png")
    plt.close()

    # QQ plot of residuals
    sm.qqplot(model.resid, line="s")
    plt.title(f"Normal Q-Q Plot - {dataset_name}")
    plt.tight_layout()
    plt.savefig(f"plots/{dataset_name}/residuals_qq_plot.png")
    plt.close()

    # Histogram of residuals
    plt.figure(figsize=(10, 6))
    sns.histplot(model.resid, kde=True)
    plt.xlabel("Residuals")
    plt.title(f"Histogram of Residuals - {dataset_name}")
    plt.tight_layout()
    plt.savefig(f"plots/{dataset_name}/residuals_histogram.png")
    plt.close()

    # Correlation between Execution Time and RunNumber (if any)
    corr = df[["ExecutionTime_ms", "RunNumber"]].corr()
    corr.to_csv(f"results/{dataset_name}_correlation.csv")

print(
    "Analysis complete. Plots and results have been saved to the 'plots' and 'results' directories."
)
