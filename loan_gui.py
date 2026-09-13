import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# ----------------------------------------------------
# EMI AUR ELIGIBILITY CALCULATIONS LOGIC
# ----------------------------------------------------
def verify_eligibility():
    try:
        # User input dynamically fetch aur parse karna
        credit_history = float(entry_credit.get())
        applicant_inc = float(entry_base_inc.get())
        co_applicant_inc = float(entry_co_inc.get())
        loan_value = float(entry_loan_val.get())
        tenure_months = float(entry_tenure.get())
        
        # Scaling validation check: Agar value choti hai (jaise UI me 300 hai), toh utilize as Thousands
        if loan_value < 10000:
            loan_amount = loan_value * 1000
        else:
            loan_amount = loan_value
            
        total_monthly_income = applicant_inc + co_applicant_inc
        
        # 1. CRITERIA CHECK: Credit History Check
        if credit_history < 1.0:
            show_rejection("Risk profile is high. Evaluation model declined parameters due to weak Credit History.")
            return

        # 2. PROCESSING: Calculate Equated Monthly Installment (EMI)
        # Assuming a standard annual interest rate of 9.5%
        annual_rate = 0.095 
        monthly_rate = annual_rate / 12
        
        # EMI Calculation Mathematical Formula
        emi = loan_amount * monthly_rate * ((1 + monthly_rate) ** tenure_months) / (((1 + monthly_rate) ** tenure_months) - 1)
        
        # 3. CRITERIA CHECK: Debt-to-Income (FOIR) standard max 50%
        if emi > (total_monthly_income * 0.50):
            show_rejection(f"Declined. Calculated EMI (₹{int(emi):,}) exceeds 50% capacity of your combined household income.")
            return

        # SUCCESS STATE: System approved matching parameters
        messagebox.showinfo("Application Status", "Loan Application Provisionally Approved successfully!")
        decision_label.config(text="APPROVED ✅", fg="#2F855A")
        result_value_label.config(text=f"EMI: ₹{int(emi):,}/Mo", fg="#2B6CB0")
        
    except ValueError:
        messagebox.showerror("Input Error", "Please ensure all financial input fields contain valid numerical numbers.")

def show_rejection(message_text):
    messagebox.showwarning("Application Warning", message_text)
    decision_label.config(text="NOT ELIGIBLE X", fg="#E53E3E")
    result_value_label.config(text="N/A", fg="#A0AEC0")


# ----------------------------------------------------
# MAIN WINDOW CONFIGURATION
# ----------------------------------------------------
root = tk.Tk()
root.title("Predictive Loan Approval & Risk Assessment Module")
root.geometry("950x670")
root.configure(bg="#FFFFFF")


# ----------------------------------------------------
# TOP HEADER BAR
# ----------------------------------------------------
header_frame = tk.Frame(root, bg="#1A365D", height=60)
header_frame.pack(fill="x", side="top")
header_frame.pack_propagate(False)

header_title = tk.Label(
    header_frame, 
    text="PREDICTIVE LOAN APPROVAL & RISK ASSESSMENT MODULE", 
    font=("Helvetica", 13, "bold"), 
    fg="#FFFFFF", 
    bg="#1A365D"
)
header_title.pack(expand=True)


# ----------------------------------------------------
# MAIN SPLIT GRID (LEFT VS RIGHT FRAMES)
# ----------------------------------------------------
content_frame = tk.Frame(root, bg="#FFFFFF", padx=20, pady=20)
content_frame.pack(fill="both", expand=True)

content_frame.columnconfigure(0, weight=1, uniform="group1")
content_frame.columnconfigure(1, weight=1, uniform="group1")
content_frame.rowconfigure(0, weight=1)


# ----------------------------------------------------
# LEFT PANEL: DATA TRANSFORMATION FIELDS
# ----------------------------------------------------
left_labelframe = tk.LabelFrame(
    content_frame, 
    text="Data Transformation Matrix Fields", 
    font=("Helvetica", 10, "bold"),
    bg="#FFFFFF", 
    padx=15, 
    pady=15
)
left_labelframe.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

left_labelframe.columnconfigure(0, weight=1)
left_labelframe.columnconfigure(1, weight=1)

def create_dropdown(parent, label_text, options, row, col):
    frame = tk.Frame(parent, bg="#FFFFFF")
    frame.grid(row=row, column=col, padx=10, pady=8, sticky="ew")
    lbl = tk.Label(frame, text=label_text, font=("Helvetica", 9, "bold"), bg="#FFFFFF", anchor="w")
    lbl.pack(fill="x")
    combo = ttk.Combobox(frame, values=options, state="readonly", font=("Helvetica", 10))
    combo.current(0)
    combo.pack(fill="x", pady=(2, 0))
    return combo

def create_entry(parent, label_text, default_val, row, col):
    frame = tk.Frame(parent, bg="#FFFFFF")
    frame.grid(row=row, column=col, padx=10, pady=8, sticky="ew")
    lbl = tk.Label(frame, text=label_text, font=("Helvetica", 9, "bold"), bg="#FFFFFF", anchor="w")
    lbl.pack(fill="x")
    entry = tk.Entry(frame, font=("Helvetica", 10), bd=1, relief="solid")
    entry.insert(0, default_val)
    entry.pack(fill="x", ipady=3, pady=(2, 0))
    return entry

# UI Dropdowns & Text Entry Boxes setup
combo_gender       = create_dropdown(left_labelframe, "Gender", ["1-Male", "0-Female"], 0, 0)
combo_married      = create_dropdown(left_labelframe, "Married Status", ["1-Yes", "0-No"], 0, 1)
combo_dependents   = create_dropdown(left_labelframe, "Dependents Count", ["1-One", "0-Zero", "2-Two", "3+"], 1, 0)
combo_education    = create_dropdown(left_labelframe, "Education Standard", ["0-Graduate", "1-Not Graduate"], 1, 1)
combo_employment   = create_dropdown(left_labelframe, "Self Employment Status", ["0-No", "1-Yes"], 2, 0)
combo_property     = create_dropdown(left_labelframe, "Property Zone Type", ["2-Urban", "1-Semiurban", "0-Rural"], 2, 1)

entry_base_inc     = create_entry(left_labelframe, "Applicant Base Income (₹)", "70000", 3, 0)
entry_co_inc       = create_entry(left_labelframe, "Co-Applicant Income (₹)", "30000", 3, 1)
entry_loan_val     = create_entry(left_labelframe, "Requested Loan Value (₹)", "300", 4, 0)
entry_tenure       = create_entry(left_labelframe, "Amortization Tenure (Months)", "360", 4, 1)
entry_credit       = create_entry(left_labelframe, "Credit History Metric", "1.0", 5, 0)

verify_btn = tk.Button(
    left_labelframe, 
    text="Verify Eligibility & Generate Plan", 
    font=("Helvetica", 11, "bold"), 
    fg="#FFFFFF", 
    bg="#2B6CB0", 
    activebackground="#1A365D",
    relief="flat",
    command=verify_eligibility
)
verify_btn.grid(row=6, column=0, columnspan=2, padx=10, pady=(25, 5), sticky="ew", ipady=8)


# ----------------------------------------------------
# RIGHT PANEL: LIVE DECISION MATRIX RESULTS
# ----------------------------------------------------
right_labelframe = tk.LabelFrame(
    content_frame, 
    text="Live Decision Matrix Results", 
    font=("Helvetica", 10, "bold"),
    bg="#FFFFFF", 
    padx=15, 
    pady=15
)
right_labelframe.grid(row=0, column=1, sticky="nsew", padx=(10, 0))

system_dec_lbl = tk.Label(
    right_labelframe, 
    text="SYSTEM APPROVAL DECISION:", 
    font=("Helvetica", 10, "bold"), 
    fg="#718096", 
    bg="#FFFFFF"
)
system_dec_lbl.pack(anchor="center", pady=(40, 5))

decision_label = tk.Label(
    right_labelframe, 
    text="NOT ELIGIBLE X", 
    font=("Helvetica", 22, "bold"), 
    fg="#E53E3E", 
    bg="#FFFFFF"
)
decision_label.pack(anchor="center", pady=(0, 40))

result_value_label = tk.Label(
    right_labelframe, 
    text="N/A", 
    font=("Helvetica", 18, "bold"), 
    fg="#A0AEC0", 
    bg="#FFFFFF"
)
result_value_label.pack(anchor="center", pady=20)

root.mainloop()
