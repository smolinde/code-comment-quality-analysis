# Import necessary libraries
import numpy as np  # For numerical operations
import pandas as pd  # For data manipulation and analysis
import scipy.stats as scs  # For statistical tests
import seaborn as sns  # For data visualization
import matplotlib.pyplot as plt  # For plotting graphs

# Define lists for quality attributes and entities (Human and Machine)
QUALITIES = [
    'Form and Length',  # Quality attribute 1
    'Readability',      # Quality attribute 2
    'Complexity',       # Quality attribute 3
    'Completeness',     # Quality attribute 4
    'Accuracy',         # Quality attribute 5
    'Usefulness'        # Quality attribute 6
]
ENTITIES = [
    'Human',  # Entity 1
    'Machine' # Entity 2
]

# Load the Qualtrics survey responses into a pandas DataFrame
df_responses = pd.DataFrame(pd.read_csv('../Datasets/Qualtrics_Responses.csv'))

# Print summary statistics about the responses
print(42*"-")
print(f"Total responses: {len(df_responses)}")
print(f"Average age: {np.mean(df_responses['Age_1']):.0f} years")
print(f"Men:\t{len(df_responses[df_responses['Gender'] == 1]) / len(df_responses) * 100:.2f}%")
print(f"Women:\t{len(df_responses[df_responses['Gender'] == 2]) / len(df_responses) * 100:.2f}%")

# Initialize a nested list to store grouped values for each quality and entity
grouped_values = [[[] for _ in range(6)] for _ in range(2)]

# Populate the grouped_values list with survey responses
for i in range(1, 3):  # Iterate over entities (Human and Machine)
    for j in range(1, 13):  # Iterate over questions
        for k in range(1, 13):  # Iterate over sub-questions
            # Extract responses, drop missing values, convert to integers, and add to the list
            grouped_values[i - 1][(k // 2 + k % 2) - 1].extend(
                df_responses[f'Q{i}_{j}_{k}'].dropna().astype(int).to_numpy().tolist()
            )

# Print Shapiro-Wilk test results for normality of each quality attribute
print(42*"-")
for i in range(len(QUALITIES)):
    print(f"Shapiro-Wilk Tests for {QUALITIES[i]}:")
    print(f"Human Group:\tstat = {scs.shapiro(grouped_values[0][i]).statistic:.4f}\tp = {scs.shapiro(grouped_values[0][i]).pvalue:.4f}")
    print(f"Machine Group:\tstat = {scs.shapiro(grouped_values[1][i]).statistic:.4f}\tp = {scs.shapiro(grouped_values[1][i]).pvalue:.4f}")
    print(42*"-")

# Print Mann-Whitney U test results for comparing Human and Machine groups
print(50*"-")
for i in range(len(QUALITIES)):
    print(f"Mann-Whitney U Tests for {QUALITIES[i]}:")
    mwu_less = scs.mannwhitneyu(grouped_values[0][i], grouped_values[1][i], alternative = 'less')
    mwu_two_sided = scs.mannwhitneyu(grouped_values[0][i], grouped_values[1][i], alternative = 'two-sided')
    mwu_greater = scs.mannwhitneyu(grouped_values[0][i], grouped_values[1][i], alternative = 'greater')
    print(f"Human < Machine:\tstat = {mwu_less.statistic}\tp = {mwu_less.pvalue:.4f}")
    print(f"Human ≠ Machine:\tstat = {mwu_two_sided.statistic}\tp = {mwu_two_sided.pvalue:.4f}")
    print(f"Human > Machine:\tstat = {mwu_greater.statistic}\tp = {mwu_greater.pvalue:.4f}")
    print(50*"-")

# Initialize a list to store guesses for each entity
guesses = [[] for _ in range(2)]

# Populate the guesses list with responses
for i in range(1, 3):  # Iterate over entities
    for j in range(1, 13):  # Iterate over questions
        guesses[i - 1].extend(df_responses[f'Q{i}_{j}'].dropna().astype(int).to_numpy().tolist())

# Print the correct guess rate for the Human group
print(f"Correct Guess Rate: {(guesses[0].count(1) / len(guesses[0]))*100:.2f}%")
print(50*"-")

# Perform Chi-Square and Binomial tests to check randomness of guesses
for i in range(len(ENTITIES)):
    unique, counts = np.unique(guesses[i], return_counts = True)
    observed = dict(zip(unique, counts))
    chi_square = scs.chisquare(list(observed.values()), [len(guesses[i]) / 2] * 2)
    binomial = scs.binomtest(guesses[i].count(i + 1), len(guesses[i]), p = 0.5, alternative = 'two-sided')
    print(f"Randomness Tests for {ENTITIES[i]} Group:")
    print(f"Chi-Square Test:\tstat = {chi_square.statistic:.4f}\tp = {chi_square.pvalue:.4f}")
    print(f"Binomial Test:\t\tstat = {binomial.statistic:.4f}\tp = {binomial.pvalue:.4f}")
    print(50*"-")

# Calculate the number of correct guesses for each respondent
df_responses['Correct_Guesses'] = df_responses[
    [f'Q1_{i}' for i in range(1, 13)]
].eq(1).sum(axis = 1) + df_responses[
    [f'Q2_{i}' for i in range(1, 13)]
].eq(2).sum(axis = 1)

# Perform Shapiro-Wilk tests for Experience, Education, and Correct Guesses
stat_exp, p_exp = scs.shapiro(df_responses['Experience'])
stat_edu, p_edu = scs.shapiro(df_responses['Education'])
stat_corr, p_corr = scs.shapiro(df_responses['Correct_Guesses'])
print("Shapiro-Wilk Tests:")
print(f"Years of Experience:\tstat = {stat_exp:.4f}\tp = {p_exp:.4f}")
print(f"Level of Education:\tstat = {stat_edu:.4f}\tp = {p_edu:.4f}")
print(f"Correct Guesses:\tstat = {stat_corr:.4f}\tp = {p_corr:.4f}")
print(58*"-")

# Perform Pearson correlation tests
print("Pearson Correlation:")
r, p = scs.pearsonr(df_responses['Experience'], df_responses['Correct_Guesses'])
print(f"Experience x Correct Guesses:\tr = {r:.4f}\tp = {p:.4f}")
r, p = scs.pearsonr(df_responses['Education'], df_responses['Correct_Guesses'])
print(f"Education x Correct Guesses:\tr = {r:.4f}\tp = {p:.4f}")
print(58*"-")

# Perform Spearman correlation tests
print("Spearman Correlation:")
rho, p = scs.spearmanr(df_responses['Experience'], df_responses['Correct_Guesses'])
print(f"Experience x Correct Guesses:\trho = {rho:.4f}\tp = {p:.4f}")
rho, p = scs.spearmanr(df_responses['Education'], df_responses['Correct_Guesses'])
print(f"Education x Correct Guesses:\trho = {rho:.4f}\tp = {p:.4f}")
print(58*"-")

# Calculate mean scores for each quality and entity
grouped_means = [[np.mean(cell) for cell in row] for row in grouped_values]

# Create a figure with subplots for visualizing the results
fig, axes = plt.subplots(2, 3, figsize = (12, 8))
plt.suptitle('Code Comment Evaluation Results', fontsize = 24, fontweight = 'bold', y = 1)

# Define colors for the bars based on significance
colors = [
    ("grey", "grey"),  # Non-significant
    ("blue", "orange") # Significant
]

# Plot bar charts for each quality attribute
for i, ax in enumerate(axes.flat):  
    x = [1.2, 1.8]  # X-axis positions for Human and Machine
    width = 0.4  # Width of the bars
    pvalue = scs.mannwhitneyu(grouped_values[0][i], grouped_values[1][i], alternative = 'less').pvalue
    if pvalue > 0.05:
        color1, color2 = colors[0]  # Use grey for non-significant results
    else:
        color1, color2 = colors[1]  # Use blue and orange for significant results

    # Plot the bars
    bars = ax.bar(x, [grouped_means[0][i], grouped_means[1][i]], width = width, color = [color1, color2], edgecolor = 'black')
    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, yval + 0.2, f'{yval:.2f}', ha = 'center', va = 'bottom', fontsize = 10)
        
    # Add p-value annotations
    if pvalue <= 0.0001:
        ax.text(0.1, 9, f'MWU Test p-value: {pvalue:.4f} ****', ha = 'left', va = 'bottom', fontsize = 9, color = 'black')
    elif pvalue <= 0.001:
        ax.text(0.1, 9, f'MWU Test p-value: {pvalue:.4f} ***', ha = 'left', va = 'bottom', fontsize = 9, color = 'black')
    elif pvalue <= 0.01:
        ax.text(0.1, 9, f'MWU Test p-value: {pvalue:.4f} **', ha = 'left', va = 'bottom', fontsize = 9, color = 'black')
    elif pvalue <= 0.05:
        ax.text(0.1, 9, f'MWU Test p-value: {pvalue:.4f} *', ha = 'left', va = 'bottom', fontsize = 9, color = 'black')
    else:
        ax.text(0.1, 9, f'MWU Test p-value: {pvalue:.4f}', ha = 'left', va = 'bottom', fontsize = 9, color = 'black')

    # Set plot properties
    ax.set_xticks(x)
    ax.set_xticklabels(["Human", "Machine"])
    ax.set_xlim(0, 3)
    ax.set_ylim(0, 10)
    ax.set_title(f"Average Scores for {QUALITIES[i]}")

# Add footnotes for significance stars
footnote = ("\n"
            "p-value < 0.05\n"
            "p-value < 0.01\n"
            "p-value < 0.001\n"
            "p-value < 0.0001")
stars = ("Significance Stars:\n"
        "*\n"
        "**\n"
        "***\n"
        "****\n")

fig.text(0.01, 0.01, stars, ha = 'left', va = 'top', fontsize = 10, color = 'black')
fig.text(0.05, 0.01, footnote, ha = 'left', va = 'top', fontsize = 10, color = 'black')

# Adjust layout and save the figure
plt.subplots_adjust(top = 0.9, bottom = 0.1)
plt.tight_layout()
plt.savefig('../Images/Summary.png', dpi = 600, bbox_inches = 'tight', pad_inches = 0.1)
plt.savefig('../Images/Summary.svg', dpi = 600, bbox_inches = 'tight', pad_inches = 0.1)
print("Files saved (summary.png, summary.svg)")