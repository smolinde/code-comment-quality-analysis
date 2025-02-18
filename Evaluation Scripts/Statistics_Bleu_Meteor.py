# Import necessary libraries
import pandas as pd  # For data manipulation and analysis
import numpy as np  # For numerical operations
import nltk  # Natural Language Toolkit for text processing

# Download necessary NLTK datasets
nltk.download('punkt_tab')  # Tokenizer models
nltk.download('wordnet')  # Lexical database for English

# Import specific functions from NLTK for text evaluation
from nltk.translate.bleu_score import sentence_bleu  # For BLEU score calculation
from nltk.translate.meteor_score import meteor_score  # For METEOR score calculation
from nltk.translate.bleu_score import SmoothingFunction  # For smoothing BLEU scores
from nltk.tokenize import word_tokenize  # For tokenizing text into words

# Import statistical functions from SciPy
from scipy.stats import f_oneway, ttest_ind, ttest_1samp, levene  # For statistical tests

# Define weights for BLEU score calculation at different n-gram levels
BLEU_SCORE_WEIGHTS = [
    [1.0, 0.0, 0.0, 0.0],  # BLEU-1 (unigrams)
    [0.5, 0.5, 0.0, 0.0],  # BLEU-2 (bigrams)
    [0.33, 0.33, 0.33, 0.0],  # BLEU-3 (trigrams)
    [0.25, 0.25, 0.25, 0.25]  # BLEU-4 (four-grams)
]

# Define column names for storing BLEU and METEOR scores
SCORE_COLUMN_NAMES = [
    'bleu_1',  # BLEU-1 score
    'bleu_2',  # BLEU-2 score
    'bleu_3',  # BLEU-3 score
    'bleu_4',  # BLEU-4 score
    'meteor'   # METEOR score
]

# Function to calculate BLEU score between ground truth and hypothesis text
def calculate_bleu_score(ground_truth, hypothesis, score_level):
    # Tokenize the ground truth text into a list of words
    ground_truth_tokens = [ground_truth.split()]
    # Tokenize the hypothesis text into a list of words
    hypothesis_tokens = hypothesis.split()
    # Calculate and return the BLEU score using the specified weights and smoothing function
    return sentence_bleu(
        ground_truth_tokens,
        hypothesis_tokens,
        weights = BLEU_SCORE_WEIGHTS[score_level],
        smoothing_function = SmoothingFunction().method1
    )

# Load the dataset containing code comments and ground truth for evaluation
code_comments = pd.DataFrame(pd.read_csv('../Datasets/Code_Comments_BLEU_Evaluation.csv', delimiter = ','))

# Iterate over each row in the dataset to calculate BLEU and METEOR scores
for i in range(len(code_comments)):
    # Calculate BLEU scores for each n-gram level (1 to 4)
    for j in range(len(BLEU_SCORE_WEIGHTS)):
        code_comments.loc[i, SCORE_COLUMN_NAMES[j]] = calculate_bleu_score(
            code_comments.comment_text_block[i],  # Hypothesis text
            code_comments.ground_truth[i],  # Ground truth text
            j  # BLEU score level (0 for BLEU-1, 1 for BLEU-2, etc.)
        )
    # Calculate METEOR score for the current row
    code_comments.loc[i, 'meteor'] = meteor_score(
        [word_tokenize(code_comments.ground_truth[i])],  # Ground truth text tokenized
        word_tokenize(code_comments.comment_text_block[i])  # Hypothesis text tokenized
    )

# Print a separator line for clarity
print(55*"-")

# Perform statistical tests to compare Human and Machine groups for each score
for i in range(len(SCORE_COLUMN_NAMES)):
    # Perform ANOVA test to check within-group differences
    within_group = f_oneway(
        code_comments[code_comments['author'] == 'Human'][SCORE_COLUMN_NAMES[i]].values,  # Human group scores
        code_comments[code_comments['author'] == 'Machine'][SCORE_COLUMN_NAMES[i]].values  # Machine group scores
    )
    # Perform independent T-test to check between-group differences
    between_group = ttest_ind(
        code_comments[code_comments['author'] == 'Human'][SCORE_COLUMN_NAMES[i]].values,  # Human group scores
        code_comments[code_comments['author'] == 'Machine'][SCORE_COLUMN_NAMES[i]].values,  # Machine group scores
        equal_var = False  # Assume unequal variance between groups
    )
    
    # Calculate variance and standard deviation for Human group
    variance_human = np.var(code_comments[code_comments['author'] == 'Human'][SCORE_COLUMN_NAMES[i]].values)
    std_dev_human = np.std(code_comments[code_comments['author'] == 'Human'][SCORE_COLUMN_NAMES[i]].values)

    # Calculate variance and standard deviation for Machine group
    variance_machine = np.var(code_comments[code_comments['author'] == 'Machine'][SCORE_COLUMN_NAMES[i]].values)
    std_dev_machine = np.std(code_comments[code_comments['author'] == 'Machine'][SCORE_COLUMN_NAMES[i]].values)

    # Print the results of the statistical tests
    print(f"Statistical Test Results for {SCORE_COLUMN_NAMES[i]} Score".upper())
    print(f"Variance in Human group:\t\t\t {variance_human:.4f}")
    print(f"Standard Deviation in Human group:\t\t {std_dev_human:.4f}")
    print(f"Variance in Machine group:\t\t\t {variance_machine:.4f}")
    print(f"Standard Deviation in Machine group:\t\t {std_dev_machine:.4f}")
    
    # Print ANOVA test results
    if (within_group.statistic < 0):
        print(f"Within-group differences (ANOVA, statistic):\t{within_group.statistic:.4f}")
    else:
        print(f"Within-group differences (ANOVA, statistic):\t {within_group.statistic:.4f}")
    print(f"Within-group differences (ANOVA, p-value):\t {within_group.pvalue:.4f}")
    
    # Print T-test results
    if (between_group.statistic < 0):
        print(f"Between-group differences (T-test, statistic):\t{between_group.statistic:.4f}")
    else:
        print(f"Between-group differences (T-test, statistic):\t {between_group.statistic:.4f}")
    print(f"Between-group differences (T-test, p-value):\t {between_group.pvalue:.4f}")
    
    # Print a separator line for clarity
    print(55*"-")

# Save the updated dataset with calculated scores to a new CSV file
code_comments.to_csv('../Datasets/Code_Comments_BLEU_Evaluation_Filled.csv', index = False, sep = ',', encoding = 'utf-8')
print("File saved (Code_Comments_BLEU_Evaluation_Filled.csv)")