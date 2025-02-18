# Import the pandas library for data manipulation and analysis
import pandas as pd

# Define the file path for the Qualtrics survey data
FILE_PATH = 'qualtrics_export.csv'

# Load the Qualtrics survey data into a pandas DataFrame
df_responses = pd.DataFrame(pd.read_csv(FILE_PATH))

# Drop unnecessary columns from the DataFrame to focus on relevant data
df_responses.drop(columns = [
    'StartDate',  # Survey start date
    'EndDate',    # Survey end date
    'Status',     # Survey status
    'IPAddress',  # IP address of the respondent
    'Progress',   # Progress of the survey
    'Duration (in seconds)',  # Time taken to complete the survey
    'RecordedDate',  # Date the response was recorded
    'ResponseId',    # Unique response ID
    'RecipientLastName',  # Last name of the recipient
    'RecipientFirstName',  # First name of the recipient
    'RecipientEmail',  # Email of the recipient
    'ExternalReference',  # External reference ID
    'LocationLatitude',  # Latitude of the respondent's location
    'LocationLongitude',  # Longitude of the respondent's location
    'DistributionChannel',  # Channel through which the survey was distributed
    'UserLanguage',  # Language of the respondent
    'Email'  # Email address (if applicable)
], inplace = True)  # Modify the DataFrame in place

# Remove rows where the survey was not finished (Finished == '0')
df_responses.drop(df_responses[df_responses['Finished'] == '0'].index, inplace = True)

# Drop the 'Finished' column as it is no longer needed
df_responses.drop(columns = ['Finished'], inplace = True)

# Drop the first two rows (likely metadata or headers)
df_responses.drop(index = df_responses.index[:2], inplace = True)

# Reset the DataFrame index after dropping rows
df_responses.reset_index(drop = True, inplace = True)

# Clean column names by removing spaces using regex
df_responses.columns = df_responses.columns.str.replace(r"\s+", "", regex = True)

# Convert specific columns to numeric, coercing errors to NaN (Not a Number)
df_responses['Age_1'] = pd.to_numeric(df_responses['Age_1'], errors = 'coerce')  # Age of respondents
df_responses['Education'] = pd.to_numeric(df_responses['Education'], errors = 'coerce')  # Education level
df_responses['Experience'] = pd.to_numeric(df_responses['Experience'], errors = 'coerce')  # Years of experience

# Save the cleaned and processed DataFrame to a new CSV file
df_responses.to_csv('../Datasets/Qualtrics_Responses.csv', index = False, sep = ',', encoding = 'utf-8')

# Print a confirmation message that the file has been saved
print("File saved (Qualtrics_Responses.csv)")