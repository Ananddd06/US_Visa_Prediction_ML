# 🌟 **Project Workflow Guide** 🌟

Welcome to the project! Here's your step-by-step guide to get started and understand the workflow.

---

## **Step 1: Initial Setup** 🛠️

Let's kickstart the project with a solid foundation! 🎉

### 1. **Initialize a Git Repository** 📁

- Set up a Git repository to track changes and maintain version control. 🧑‍💻
- Commit all initial files to ensure smooth collaboration.

### 2. **Core Files to Add** 📝

- **`requirements.txt`**: List all the dependencies and libraries required for the project. 📦
- **`setup.py`**: Contains the setup script for installing dependencies and configuring the project. 🏗️
- **`README.md`**: A markdown file that provides an overview of the project, setup instructions, and usage guidelines. 📚

### 3. **Automating Directory and File Creation** 🗂️

- Use a **template file** to define the necessary directory structure and files.
- Iterate over the list of directories and files using a loop:
  - Split the directory and file names with `os.path.split(data_dir, datafile)`.
  - Use `os.mkdir()` to create directories.
  - Check if the file exists and open it using `with open(file_name, "w")` if not.

---

## **Step 2: Setup Script** ⚙️

### 1. **Package Installation** 🧑‍🔧

- Write a function to install all dependencies listed in the `requirements.txt` file.

### 2. **Setup Function** 🔧

- Include key details such as:
  - Author name ✍️
  - Author email 📧
  - Project name 📜
- Call the function to install the required packages.

---

## **Step 3: Exception Handling and Logging** 🔒

### 1. **Exception Handling** 🚨

- Handle exceptions for:
  - Missing files 📂: Raise a `FileNotFoundError` if a specified file is not found.
  - Missing directories 📁: Raise an appropriate error if directories are not found or accessible.

### 2. **Logging** 📖

- Implement a logging system to:
  - Track the workflow 🔍
  - Log timestamps and actions for better traceability 🕒
- Use log files to debug issues efficiently. 🐞

---

## **Step 4: Data Exploration and Model Building** 📊

Create a folder named **`Notebook`** for all analysis and modeling tasks. This will include:

### 1. **Attach the Dataset** 📂

- Include the `.csv` file for the project.

### 2. **Perform Exploratory Data Analysis (EDA)** 🔍

- Understand the dataset structure and uncover insights.

### 3. **Feature Engineering** 🧠

- Engineer new features to improve model performance.

### 4. **Model Training and Hyperparameter Tuning** 🤖

- Train models and tune hyperparameters to achieve the best results.

---

## **Step 5: MongoDB Database Connection** 🌐

In this step, we connect to the MongoDB database.

### 1. **MongoDB URL Configuration** 🗺️

- In the **config** file, under the `US Visa` folder, make the MongoDB URL connection.
- Check if a client connection exists. If not, fetch the URL and connect to MongoDB.
- Convert the data from the MongoDB collection into a pandas dataframe and then to a dictionary format for further processing.

---

## **Step 6: Convert Data Table to CSV File** 💾

Create a **data_access** folder where we connect to MongoDB and export the data to a `.csv` file.

### 1. **Function Creation** 🛠️

- Access the MongoDB database, extract the required data, and save it as a CSV file. This file will be used for training and testing data.

---

## **Step 7: Workflow Steps** 🔄

The overall project follows this workflow:

1. **Entity** 🏢
2. **Artifact** 🏗️
3. **Config** ⚙️
4. **Components** 🔌
5. **Training Pipeline** 🏋️‍♀️

---

## **Step 8: Define Constants** 📍

In the **constants** folder, define all necessary paths and database configurations.

```python
import os
from datetime import date

DATABASE_NAME = "US_VISA"
COLLECTION_NAME = "visa_data"
MONGO_DB_URL = "MONGODB_URL"

PIPELINE_NAME: str = "usvisa"
ARTIFACT_DIR: str = 'artifact'

MODEL_FILE_NAME = "model.pkl"
TRAIN_FILE_NAME: str = "train.csv"
TEST_FILE_NAME: str = "test.csv"
FILE_NAME: str = "usvisa.csv"
MODEL_FILE_NAME = "model.pkl"
TARGET_COLUMN = "case_status"
CURRENT_YEAR = date.today().year
PREPROCESSING_OBJECT_FILE_NAME = "preprocessing.pkl"
SCHEMA_FILE_PATH = os.path.join("config", "schema.yaml")

```

## **Step 9: Define Data Ingestion Path in Config** 🔄

### 1. **Data Ingestion Path Configuration** 🛤️

- Add a key in the **config** file to store the path where data ingestion files (`train.csv`, `test.csv`) will be saved.
- Define the paths and file names for the ingested data to align with the project structure.

---

## **Step 10: Data Ingestion Workflow** 📈

The **DataIngestion** class handles data extraction, transformation, and storage.

### 1. **Feature Store Function** 🏪

- In the **DataIngestion** class, create a function to fetch MongoDB data, convert it to CSV, and store it in the feature store.
- Interact with MongoDB, fetch required data, and save it in `.csv` format for further processing.

### 2. **Train-Test Split** 🔪

- Implement functionality to split the data into training and testing sets.
- The split data will be saved in the **ingested** folder under `train.csv` and `test.csv` files, referenced dynamically from the **config** file.

### 3. **Initiate Data Ingestion Workflow** 🚀

- Use the **DataIngestion** class to execute the ingestion process and save the resulting data (like `train.csv` and `test.csv`) in the **artifact** folder.

---

## **Step 11: Update Training Pipeline** ⚙️

1. **TrainingPipeline Class** 💼

   - In the **TrainingPipeline** class, import the necessary config and call the **DataIngestion** class to set up the ingestion process.

2. **Start Function** 🏁

   - Create a function named **start** to initiate the data ingestion process and call the **DataIngestion** class to load data.

3. **Run Pipeline Function** 🏃‍♂️
   - The **run_pipeline** function will initiate the **start** method from **DataIngestion**, launching the entire pipeline.

---

## **Step 12: Data Validation Workflow** ✅

Data validation ensures that the incoming data is clean, error-free, and adheres to the defined schema.

### 1. **Config and Artifact Updates** 📂

- Add necessary configuration to the **config** file for storing validation rules.
- Ensure that the artifact files for storing the validation results are properly created and logged.

### 2. **Schema Validation** 📊

- Use a schema validation library like **Cerberus** or **pydantic** to validate incoming data.
- Define rules to ensure the data matches the required structure (column names, data types, ranges, etc.).
- Raise errors for invalid data to prevent further processing.

### 3. **Log Validation Results** 📝

- Store validation results in a separate **log file** for debugging and record-keeping purposes.
- Track the number of valid and invalid entries.

---

## **Step 13: Model Training and Hyperparameter Tuning** 🤖

Now that the data has been ingested, cleaned, and validated, it's time to move to the next phase: **Model Training**.

### 1. **Train Models** 📚

- Use a variety of algorithms (e.g., logistic regression, decision trees, random forests) to train the model on the processed data.
- Ensure that the model selection aligns with the problem (classification, regression, etc.).

### 2. **Hyperparameter Tuning** 🔧

- Apply techniques such as grid search or random search to tune the hyperparameters of the model.
- Use cross-validation to evaluate the performance of the model during training.

### 3. **Evaluate Model Performance** 📈

- Track important metrics like accuracy, precision, recall, F1-score, etc., to assess the performance of the model.
- Generate confusion matrices and ROC curves to evaluate the model visually.

### 4. **Save the Best Model** 💾

- Once the model is trained and optimized, save it in the **artifact** folder using `joblib` or `pickle`.
- The best model will be used for future predictions.

---

## **Next Steps** 🚀

After completing these stages, continue with the following steps in the project lifecycle:

1. **Model Deployment** 🚀
   - Deploy the model in a production environment using Flask, FastAPI, or a cloud-based solution.
2. **Monitoring and Maintenance** 🔄

   - Set up monitoring for the deployed model to track its performance over time.
   - Periodically retrain the model with fresh data to keep it up to date.

3. **Integration with APIs** 🌐
   - Integrate the model with external systems, APIs, or user interfaces for real-time predictions and insights.

---
