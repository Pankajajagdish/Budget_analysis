import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(page_title="Budget Analyzer", layout="centered")

st.title("Budget Analyzer")

# Initialize session state
if "categories" not in st.session_state:
    st.session_state.categories = ["Food", "Transport", "Shopping", "Bills"]
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=["date", "type", "category", "amount"])

# Category management
st.subheader("Manage Expense Categories")
new_cat = st.text_input("Add new category")
if st.button("Add Category") and new_cat and new_cat not in st.session_state.categories:
    st.session_state.categories.append(new_cat)
    st.success(f"Added category: {new_cat}")

remove_cat = st.selectbox("Remove category", [""] + st.session_state.categories)
if st.button("Remove Category") and remove_cat:
    st.session_state.categories.remove(remove_cat)
    st.success(f"Removed category: {remove_cat}")

st.markdown("---")

# Entry form
st.subheader("Enter Daily Income/Expense")
entry_date = st.date_input("Date", value=date.today())
entry_type = st.radio("Type", ["Income", "Expense"])
entry_cat = ""
if entry_type == "Expense":
    entry_cat = st.selectbox("Category", st.session_state.categories)
else:
    entry_cat = "Income"
entry_amt = st.number_input("Amount (₹)", min_value=0.0, step=0.01)
if st.button("Add Entry"):
    new_entry = {
        "date": entry_date,
        "type": entry_type,
        "category": entry_cat,
        "amount": entry_amt
    }
    st.session_state.data = pd.concat([st.session_state.data, pd.DataFrame([new_entry])], ignore_index=True)
    st.success(f"Added {entry_type} entry for {entry_date}")

st.markdown("---")

# Show all entries
st.subheader("All Entries This Month")
current_month = date.today().month
current_year = date.today().year
df = st.session_state.data
df_month = df[(pd.to_datetime(df["date"]).dt.month == current_month) & (pd.to_datetime(df["date"]).dt.year == current_year)]
st.dataframe(df_month)

st.markdown("---")

# Monthly Analysis
st.subheader("Monthly Analysis")
income = df_month[df_month["type"] == "Income"]["amount"].sum()
expenses_by_cat = df_month[df_month["type"] == "Expense"].groupby("category")["amount"].sum()
total_expense = expenses_by_cat.sum()

if not df_month.empty:
    st.write(f"**Total Income:** ₹{income:.2f}")
    st.write(f"**Total Expenses:** ₹{total_expense:.2f}")

    if not expenses_by_cat.empty:
        max_cat = expenses_by_cat.idxmax()
        max_spent = expenses_by_cat.max()
        st.write(f"**Highest Spending Category:** {max_cat} (₹{max_spent:.2f})")

        # Cost-cutting suggestion
        if total_expense > income:
            st.warning(f"Expenses exceed income! Consider reducing spending in '{max_cat}' and other non-essential categories.")
        else:
            st.success("Your spending is within budget! Great job!")
    else:
        st.info("No expenses entered yet.")
else:
    st.info("No entries for the current month.")
