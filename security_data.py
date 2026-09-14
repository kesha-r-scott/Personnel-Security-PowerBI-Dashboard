# Import pandas for working with tables and CSV files.

import pandas as pd
# Import random so the script can generate realistic fictional data.
import random
# --------------------------------------------------
# LOAD EXISTING DATASETS
# --------------------------------------------------
# Load the People, Clearance, and Incidents CSV files
# into pandas DataFrames so they can be used in Python.
people = pd.read_csv("people.csv")
clearance = pd.read_csv("clearance.csv")
incident = pd.read_csv("incidents.csv")
# Display the first five rows of each dataset.
# This provides a quick check that the CSV files loaded correctly.
print("People:")
print(people.head())

print("\nClearance:")
print(clearance.head())

print("\nIncidents:")
print(incident.head())
training = pd.DataFrame()
# --------------------------------------------------
# TRAINING TABLE
# --------------------------------------------------
# Create a new DataFrame that will store fictional
# personnel security training records.
# Create 50 unique training record IDs.
training["TrainingID"] = range(8001, 8051)
# Assign each training record to a fictional person.
# CACNumber acts as the foreign key connecting Training to People.
training["CACNumber"] = random.choices(
    people["CACNumber"].tolist(),
    k=50
)
# Define the types of security training that can be assigned.
training_types = [
    "Annual Security Awareness Training",
    "Insider Threat Awareness",
    "Cybersecurity Awareness",
    "Controlled Unclassified Information (CUI) Training",
    "Foreign Travel Security Training"
]# Randomly assign one training type to each training record.

training["TrainingType"] = random.choices(
    training_types,
    k=50
)
# Generate 50 training assignment dates across the selected date range.
training["AssignedDate"] = pd.date_range(
    start="2025-01-01",
    end="2026-06-30",
    periods=50
)
# Set each training due date to 90 days after its assigned date.
training["DueDate"] = training["AssignedDate"] + pd.to_timedelta(
    90,
    unit="D"
)
# Define possible training completion statuses.
# Repeating "Completed" makes completed training more common
# in the fictional dataset.
training_statuses = [
    "Completed",
    "Completed",
    "Completed",
    "In Progress",
    "Overdue"
]
# Randomly assign a status to each training record.
training["TrainingStatus"] = random.choices(
    training_statuses,
    k=50
)
# Generate a fictional training score between 75 and 100
# for each training record.
training["Score"] = [
    random.randint(75, 100) for _ in range(50)
]
# Display the first 10 training records for review.
# Export the completed Training table to CSV for use in Power BI.
# index=False prevents pandas row numbers from becoming a CSV column.
print(training.head(10))
training.to_csv("training.csv", index=False)
# --------------------------------------------------
# BADGE / ACCESS TABLE
# --------------------------------------------------
# Create fictional badge and facility-access records
# that connect back to the People table through CACNumber.
# Create an empty DataFrame for badge and access information.
badge_access = pd.DataFrame()
# Create 50 unique badge record IDs.
badge_access["BadgeID"] = range(9001, 9051)
# Assign one badge record to each person using CACNumber.
badge_access["CACNumber"] = people["CACNumber"]
# Define the possible lifecycle states for a badge.
# Repeating "Active" makes active badges more common.
badge_statuses = [
    "Active",
    "Active",
    "Active",
    "Suspended",
    "Expired",
    "Lost"
]
# Generate fictional badge issue dates across several years.
badge_access["BadgeStatus"] = random.choices(
    badge_statuses,
    k=50
)

badge_access["BadgeIssueDate"] = pd.date_range(
    start="2022-01-01",
    end="2026-01-31",
    periods=50
)
# Set each badge expiration date to three years after issue.
badge_access["BadgeExpirationDate"] = (
    badge_access["BadgeIssueDate"] + pd.DateOffset(years=3)
)
# Define fictional facility access levels.
access_levels = [
    "General Access",
    "Restricted Area",
    "Secure Area",
    "Executive Area"
]
# Randomly assign an access level to each badge holder.
badge_access["AccessLevel"] = random.choices(
    access_levels,
    k=50
)
# Define fictional facility locations used by the dashboard.
facilities = [
    "San Diego Facility",
    "El Segundo Facility",
    "Palmdale Facility",
    "Riverside Facility",
    "Huntsville Facility",
    "Arlington Facility",
    "Colorado Springs Facility"
]
# Randomly assign each badge holder to a facility.
badge_access["Facility"] = random.choices(
    facilities,
    k=50
)
# Set the last access review to one year after the badge issue date.
badge_access["LastAccessReviewDate"] = (
    badge_access["BadgeIssueDate"] + pd.DateOffset(years=1)
)
# Display the first 10 Badge / Access records for review.
print("\nBadge / Access:")
print(badge_access.head(10))
# Export the Badge / Access table to CSV for Power BI.
badge_access.to_csv("badge_access.csv", index=False)
# --------------------------------------------------
# DATA VALIDATION / AUDIT CHECKS
# --------------------------------------------------
# Perform quality checks before loading the datasets into Power BI.
# These checks verify row counts, primary-key uniqueness,
# missing keys, and foreign-key relationships.-----------------------------   
print("\n--- Validation Results ---")

print("\nPeople:", len(people))
print("Clearance:", len(clearance))
print("Incidents:", len(incident))
print("Training:", len(training))
print("Badge / Access:", len(badge_access))

print("\nDuplicate CAC numbers in people:")
print(people["CACNumber"].duplicated().sum())

print("\nMissing CAC numbers:")
print("People:", people["CACNumber"].isna().sum())
print("Clearance:", clearance["CACNumber"].isna().sum())
print("Incidents:", incident["CACNumber"].isna().sum())
print("Training:", training["CACNumber"].isna().sum())
print("Badge / Access:", badge_access["CACNumber"].isna().sum())

valid_cacs = set(people["CACNumber"])
print("\nInvalid CAC numbers in Clearance:")
print((~clearance["CACNumber"].isin(valid_cacs)).sum())
print("\nInvalid CAC numbers in Incidents:")
print((~incident["CACNumber"].isin(valid_cacs)).sum())      
print("\nInvalid CAC numbers in Training:")
print((~training["CACNumber"].isin(valid_cacs)).sum())
print("\nInvalid CAC numbers in Badge / Access:")
print((~badge_access["CACNumber"].isin(valid_cacs)).sum())

print("\nUnique people:")
print(people["CACNumber"].nunique())

      