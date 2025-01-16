# 🌟 Project Workflow Guide 🌟

Welcome! Follow these steps to get started with the project.

---

## 1. Initial Setup 🛠️

- **Initialize Git**: Set up a Git repository for version control and commit initial files.
- **Core Files**:
  - `requirements.txt`: Lists project dependencies.
  - `setup.py`: Contains the installation and configuration setup.
  - `README.md`: Overview, setup instructions, and usage guidelines.

---

## 2. Automate Directory and File Creation 🗂️

- Use a template to define the directory structure.
- Create directories and files programmatically:
  - Use `os.mkdir()` for directories.
  - Open missing files with `with open(file_name, "w")`.

---

## 3. Exception Handling & Logging 🔒

- **Exception Handling**:
  - Handle missing files (`FileNotFoundError`) and directories.
- **Logging**:
  - Track actions with timestamps.
  - Store logs for debugging.

---

## 4. Data Exploration & Model Building 📊

- **Notebook Folder**: Save all analysis and modeling tasks.
- **Tasks**:
  - Attach the dataset (`.csv`).
  - Perform EDA and feature engineering.
  - Train models and tune hyperparameters.

---

## 5. MongoDB Database Connection 🌐

- Configure MongoDB in the `config` file.
- Fetch data, convert to a pandas DataFrame, and process as a dictionary.

---

## 6. Export Data to CSV 💾

- Create a `data_access` folder to handle MongoDB data export.
- Save data as a `.csv` file for training/testing.

---

## 7. Workflow Structure 🔄

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

---

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
