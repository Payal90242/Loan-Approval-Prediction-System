import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import messagebox
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

# =====================================================================
# 1. DATA PREPROCESSING & MODEL TRAINING
# =====================================================================
print("Loading data and training model... Please wait...")

try:
    df = pd.read_csv("Loan-Approval-Prediction.csv")
except FileNotFoundError:
    print("Error: 'Loan-Approval-Prediction.csv' file nahi mili! Please check current folder.")
    input("Press Enter to exit...")
    exit()

# Drop Loan_ID if it exists
if 'Loan_ID' in df.columns:
    df = df.drop(['Loan_ID'], axis=1)

# Handling Missing Values properly
categorical_cols = ['Gender', 'Married', 'Dependents', 'Self_Employed', 'Credit_History']
for col in categorical_cols:
    df[col] = df[col].fillna(df[col].mode()[0])
    
df['LoanAmount'] = df['LoanAmount'].fillna(df['LoanAmount'].median())
df['Loan_Amount_Term'] = df['Loan_Amount_Term'].fillna(df['Loan_Amount_Term'].mode()[0])

# Strict Hardcoded Mapping (Alphabetical order exactly matching LabelEncoder)
mapping = {
    'Gender': {'Female': 0, 'Male': 1},
    'Married': {'No': 0, 'Yes': 1},
    'Dependents': {'0': 0, '1': 1, '2': 2, '3+': 3},
    'Education': {'Graduate': 0, 'Not Graduate': 1},
    'Self_Employed': {'No': 0, 'Yes': 1},
    'Property_Area': {'Rural': 0, 'Semiurban': 1, 'Urban': 2},
    'Loan_Status': {'N': 0, 'Y': 1}
}

# Apply mappings to dataset
for col, map_dict in mapping.items():
    if col in df.columns:
        df[col] = df[col].astype(str).map(map_dict)

# Credit history handling explicitly as numeric float
df['Credit_History'] = df['Credit_History'].astype(float)

# Split features and target
X = df.drop(['Loan_Status'], axis=1)
y = df['Loan_Status']
feature_order = X.columns.tolist()

# Train Random Forest Model
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

print("Model training complete! Launching GUI...")

# =====================================================================
# 2. TKINTER GUI IMPLEMENTATION
# =====================================================================
root = tk.Tk()
root.title("Loan Approval Predictor")
root.geometry("480x650")
root.configure(bg="#f4f6f9")

# Title Label
lbl_title = tk.Label(root, text="Loan Approval Prediction System", font=("Arial", 16, "bold"), bg="#f4f6f9", fg="#2c3e50")
lbl_title.pack(pady=20)

# Form Frame
frame = tk.Frame(root, bg="#f4f6f9")
frame.pack(pady=10)

# UI Dropdown Options Mapping Definition
options = {
    'Gender': ['Male', 'Female'],
    'Married': ['Yes', 'No'],
    'Dependents': ['0', '1', '2', '3+'],
    'Education': ['Graduate', 'Not Graduate'],
    'Self_Employed': ['Yes', 'No'],
    'ApplicantIncome': "numeric",
    'CoapplicantIncome': "numeric",
    'LoanAmount': "numeric",
    'Loan_Amount_Term': "numeric",
    'Credit_History': ['1.0', '0.0'],
    'Property_Area': ['Urban', 'Semiurban', 'Rural']
}

inputs = {}

# Build Form Elements Layout
for i, feature in enumerate(feature_order):
    lbl = tk.Label(frame, text=f"{feature}:", font=("Arial", 10, "bold"), bg="#f4f6f9", anchor="w", width=18)
    lbl.grid(row=i, column=0, sticky="w", padx=10, pady=6)
    
    opt = options[feature]
    if opt == "numeric":
        ent = tk.Entry(frame, font=("Arial", 10), width=20, bd=2, relief="groove")
        ent.grid(row=i, column=1, padx=10, pady=6)
        inputs[feature] = ent
    else:
        var = tk.StringVar(root)
        var.set(opt[0])  # Set default option element
        drop = tk.OptionMenu(frame, var, *opt)
        drop.config(font=("Arial", 9), width=17, bg="white", relief="groove")
        drop.grid(row=i, column=1, padx=10, pady=6)
        inputs[feature] = var

# Prediction Processing logic function block
def predict_status():
    try:
        data = {}
        for feature in feature_order:
            val = inputs[feature].get()
            
            if options[feature] == "numeric":
                if val.strip() == "":
                    raise ValueError(f"{feature} empty nahi ho sakta.")
                data[feature] = float(val)
            elif feature == 'Credit_History':
                data[feature] = float(val)
            else:
                # Direct conversion using standard format structural parameters maps
                data[feature] = mapping[feature][val]
        
        # Prepare inputs exactly as feature order expected by scikit-learn
        input_df = pd.DataFrame([data])[feature_order]
        
        # Classifier Evaluation execution
        prediction = rf_model.predict(input_df)[0]
        
        # UI alert triggers depending upon binary output configurations
        if prediction == 1:
            messagebox.showinfo("Prediction Result", "🎉 Congratulations!\nYour Loan is likely to be APPROVED.")
        else:
            messagebox.showwarning("Prediction Result", "❌ Sorry!\nYour Loan request is likely to be REJECTED.")
            
    except ValueError as ve:
        messagebox.showerror("Input Error", str(ve))
    except Exception as e:
        messagebox.showerror("Error", f"Koshish nakam rahi: {str(e)}")

# Submit Trigger Button Design
btn_predict = tk.Button(root, text="Predict Loan Status", font=("Arial", 12, "bold"), bg="#2ecc71", fg="white", padx=20, pady=8, bd=0, command=predict_status)
btn_predict.pack(pady=25)

root.mainloop()
