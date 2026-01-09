import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
pd.set_option('display.max_columns', None)

# Load the Excel file with specified header row
df=pd.read_excel('DATA_DUMP_FORMAT_Mar_2025 - Shared - V7.xlsx',header=5)

# Rows where prepayment charges were applied
pre_payment_df=df[df['Prepayment/ Foreclosure Charges']!=0.0]

pre_payment_df_export=pre_payment_df.copy()
pre_payment_df_export.fillna('NA',inplace=True)
pre_payment_df_export.to_excel("Persons_charged_with_ppc.xlsx")

individual_df=pre_payment_df[pre_payment_df['Borrower Category (Individual, Non-Individual, Employee)']=='Individual']
non_individual_df=pre_payment_df[pre_payment_df['Borrower Category (Individual, Non-Individual, Employee)']=='Non-Individual']
employee_df=pre_payment_df[pre_payment_df['Borrower Category (Individual, Non-Individual, Employee)']=='Employee']

# Convert 'Date of Loan Closure in the system/ books' to datetime, coercing errors to NaT
individual_df['Date of Loan Closure in the system/ books'] = pd.to_datetime(
    individual_df['Date of Loan Closure in the system/ books'],
    errors='coerce'
)

fixed_pp = individual_df[
    individual_df['Sanctioned ROI Type (Fixed, Floating, Special, Dual)'] == 'Fixed'
]

floating_pp = individual_df[
    individual_df['Sanctioned ROI Type (Fixed, Floating, Special, Dual)'] == 'Floating'
]
dual_df = individual_df[
    individual_df['Sanctioned ROI Type (Fixed, Floating, Special, Dual)'] == 'Dual'
]

if dual_df.shape[0]!=0:
    cutoff_date = pd.Timestamp('2024-03-31')

    dual_df = dual_df.assign(
        Final_ROI_Type=lambda df: df.apply(
            lambda row: (
                row['Type of ROI on 31.03.24 (Fixed/Floating/ Dual)']
                if row['Date of Loan Closure in the system/ books'] <= cutoff_date
                else row['Type of ROI on 31.03.25 (Fixed/Floating/ Dual)']
            ),
            axis=1
        )
    )

if dual_df.shape[0]!=0:
    fixed_pp = pd.concat(
        [fixed_pp, dual_df[dual_df['Final_ROI_Type'] == 'Fixed']],
        ignore_index=True
    )

    floating_pp = pd.concat(
        [floating_pp, dual_df[dual_df['Final_ROI_Type'] == 'Floating']],
        ignore_index=True
    )

# Export fixed ROI individuals charged with prepayment penalties
fixed_pp_export=fixed_pp.copy()
fixed_pp_export.fillna('NA',inplace=True)
fixed_pp_export.to_excel("fixed_ROI_ppc_charged.xlsx")

# Export floating ROI individuals charged with prepayment penalties
floating_pp_export=floating_pp.copy()
floating_pp_export.fillna('NA',inplace=True)
floating_pp_export.to_excel("floating_ROI_ppc_charged.xlsx")

fixed_hl=fixed_pp[fixed_pp['Loan Category Sanctioned (Housing or Non-Housing)']
    .str.strip()
    .str.lower()
    .isin(["housing", "hl"])].copy()


fixed_hl_own = fixed_hl[
    fixed_hl["Source of Prepayment/ Foreclosure"]
    .astype(str)
    .str.strip()
    .str.lower()
    # include own
    .str.contains(r"\bown\b", regex=True)
    # exclude negations
    & ~fixed_hl["Source of Prepayment/ Foreclosure"]
        .astype(str)
        .str.lower()
        .str.contains(r"\bother than own\b|\bnot own\b", regex=True)
].copy()

invalid_ppc = pd.concat(
    [fixed_hl_own, floating_pp],
    ignore_index=True
)
invalid_ppc.shape

invalid_ppc_export=invalid_ppc.copy()
invalid_ppc_export=invalid_ppc_export.fillna("NA")
invalid_ppc_export.to_excel('all_invalid_pre_payment_charges.xlsx')