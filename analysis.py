import streamlit as st
import pandas as pd
from datetime import date
import hashlib

st.set_page_config(page_title="Budget Analyzer", layout="centered")

st.title("Budget Analyzer")

# --- USER AUTHENTICATION ---
def hash_pw(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

if "users" not in st.session_state:
    # username -> {"password": hashed, "shared_with": {user: access}, "data": DataFrame, "categories": [str]}
    st.session_state.users = {}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = None

def signup_form():
    st.subheader("Sign Up")
    new_user = st.text_input("Choose Username", key="signup_user")
    new_pw = st.text_input("Choose Password", type="password", key="signup_pw")
    if st.button("Sign Up"):
        if new_user in st.session_state.users:
            st.error("Username already exists.")
        elif not new_user or not new_pw:
            st.error("Username and password required.")
        else:
            st.session_state.users[new_user] = {
                "password": hash_pw(new_pw),
                "shared_with": {},
                "data": pd.DataFrame(columns=["date", "type", "category", "amount"]),
                "categories": ["Food", "Transport", "Shopping", "Bills"]
            }
            st.success("Account created. Please log in.")

def login_form():
    st.subheader("Log In")
    user = st.text_input("Username", key="login_user")
    pw = st.text_input("Password", type="password", key="login_pw")
    if st.button("Log In"):
        if user not in st.session_state.users:
            st.error("User not found.")
        elif hash_pw(pw) != st.session_state.users[user]["password"]:
            st.error("Incorrect password.")
        else:
            st.session_state.logged_in = user
            st.success(f"Logged in as {user}")

if not st.session_state.logged_in:
    signup_form()
    login_form()
    st.stop()

user = st.session_state.logged_in

# --- SHARING LOGIC ---
st.sidebar.header("Share Your Budget Data")
share_with = st.sidebar.text_input("Share with user (username):")
access_type = st.sidebar.selectbox("Access Type", ["View", "Update"])
if st.sidebar.button("Grant Access"):
    if share_with not in st.session_state.users:
        st.sidebar.error("No such user.")
    elif share_with == user:
        st.sidebar.error("Cannot share with yourself.")
    else:
        st.session_state.users[user]["shared_with"][share_with] = access_type
        st.sidebar.success(f"Access granted to {share_with} ({access_type})")

# --- SWITCH TO ANOTHER USER'S SHARED DATA ---
st.sidebar.header("Access Shared Data")
shared_by = []
for u, info in st.session_state.users.items():
    if user in info["shared_with"]:
        shared_by.append(u)
selected_shared_user = st.sidebar.selectbox("View data shared by", [""] + shared_by)
if selected_shared_user:
    access_level = st.session_state.users[selected_shared_user]["shared_with"][user]
    st.info(f"Viewing {selected_shared_user}'s data ({access_level} access)")
    data_owner = selected_shared_user
    can_edit = access_level == "Update"
else:
    data_owner = user
    can_edit = True

# --- CATEGORY MANAGEMENT ---
st.subheader("Manage Expense Categories")
categories = st.session_state.users[data_owner]["categories"]
if can_edit:
    new_cat = st.text_input("Add new category")
    if st.button("Add Category"):
        if new_cat and new_cat not in categories:
            categories.append(new_cat)
            st.success(f"Added category: {new_cat}")
    remove_cat = st.selectbox("Remove category", [""] + categories)
    if st.button("Remove Category") and remove_cat:
        categories.remove(remove_cat)
        st.success(f"Removed category: {remove_cat}")

# --- ENTRY FORM ---
st.markdown("---")
st.subheader("Enter Daily Income/Expense")
entry_date = st.date_input("Date", value=date.today())
entry_type = st.radio("Type", ["Income", "Expense"])
entry_cat = ""
if entry_type == "Expense":
    entry_cat = st.selectbox("Category", categories)
else:
    entry_cat = "Income"
entry_amt = st.number_input("Amount (₹)", min_value=0.0, step=0.01)
if can_edit and st.button("Add Entry"):
    new_entry = {
        "date": entry_date,
        "type": entry_type,
        "category": entry_cat,
        "amount": entry_amt
    }
    st.session_state.users[data_owner]["data"] = pd.concat(
        [st.session_state.users[data_owner]["data"], pd.DataFrame([new_entry])],
        ignore_index=True
    )
    st.success(f"Added {entry_type} entry for {entry_date}")

# --- SHOW DATA ---
st.markdown("---")
st.subheader(f"All Entries This Month ({data_owner})")
current_month = date.today().month
current_year = date.today().year
df = st.session_state.users[data_owner]["data"]
df_month = df[(pd.to_datetime(df["date"]).dt.month == current_month) & (pd.to_datetime(df["date"]).dt.year == current_year)]
st.dataframe(df_month)

# --- ANALYSIS ---
st.markdown("---")
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
        if total_expense > income:
            st.warning(f"Expenses exceed income! Consider reducing spending in '{max_cat}' and other non-essential categories.")
        else:
            st.success("Your spending is within budget! Great job!")
    else:
        st.info("No expenses entered yet.")
else:
    st.info("No entries for the current month.")
