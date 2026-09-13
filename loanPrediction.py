
import pandas as pd
import joblib
df=pd.read_csv("Loan-Approval-Prediction.csv")
print(df.columns.tolist())

df.head()
df.columns
df.isnull().sum()
categorical_cols=['Gender', 'Married', 'Dependents', 'Self_Employed', 'Credit_History']
for col in categorical_cols:
    df[col]=df[col].fillna(df[col].mode()[0])
    
df['LoanAmount']=df['LoanAmount'].fillna(df['LoanAmount'].median())
df['Loan_Amount_Term']=df['Loan_Amount_Term'].fillna(df['Loan_Amount_Term'].mode()[0])
print(df.isnull().sum())
import matplotlib.pyplot as plt
import seaborn as sns
sns.countplot(x='Loan_Status', data=df)
plt.title('Loan Approval Distribution')
plt.show()
sns.countplot(x='Credit_History',hue='Loan_Status', data=df)
plt.title("Loan Approval by Credit History")
plt.show()
from sklearn.preprocessing import LabelEncoder
le=LabelEncoder()
label_cols=['Gender', 'Married', 'Education', 'Self_Employed', 'Property_Area', 'Loan_Status', 'Dependents']
for col in label_cols:
    df[col]=le.fit_transform(df[col].astype(str))
print(df.head())
X=df.drop(['Loan_ID','Loan_Status'], axis=1)
y=df['Loan_Status']
print("Features shape:", X.shape)
print("Target shape:",y.shape)
from sklearn.model_selection import train_test_split
X_train, X_test,y_train,y_test=train_test_split(X, y, test_size=0.2, random_state=42)
print("Training data:", X_train.shape)
print("Testing data:", X_test.shape)
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
rf_model=RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)
rf_preds=rf_model.predict(X_test)
accuracy=accuracy_score(y_test, rf_preds)
print("Model Accuracy:", accuracy)
from sklearn.metrics import confusion_matrix
cm=confusion_matrix(y_test, rf_preds)
sns.heatmap(cm,annot=True, fmt='d', cmap='Blues')
plt.title("Confusion Matrix - Random Forest")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.show()
importances=pd.Series(rf_model.feature_importances_, index=X.columns)
importances.sort_values(ascending=False).plot(kind='bar', figsize=(10,5))
plt.title("Feature Importance - What affects Loan Approval most")
plt.ylabel("Importance Score")
plt.show()
def calculate_emi(loan_amount, annual_interest_rate, tenure_months):
    monthly_rate = annual_interest_rate / (12 * 100)
    emi = (loan_amount * monthly_rate * (1 + monthly_rate)**tenure_months) / ((1 + monthly_rate)**tenure_months - 1)
    emi = round(emi, 2)
    
    total_payment = round(emi * tenure_months, 2)
    total_interest = round(total_payment - loan_amount, 2)
    
    print("---- Loan Details ----")
    print(f"Loan Amount Sanctioned : ₹{loan_amount}")
    print(f"Interest Rate          : {annual_interest_rate}% per annum")
    print(f"Loan Tenure             : {tenure_months} months")
    print(f"Monthly EMI             : ₹{emi}")
    print(f"Total Payment (Principal + Interest) : ₹{total_payment}")
    print(f"Total Interest Payable : ₹{total_interest}")
    
    return emi

# Example test - tum yaha values badal sakti ho
calculate_emi(loan_amount=200000, annual_interest_rate=9.5, tenure_months=120)