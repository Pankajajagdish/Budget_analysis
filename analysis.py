import streamlit as st
import pandas as pd
from datetime import date
import hashlib

st.set_page_config(page_title="💼 Budget Analyzer", layout="wide")

st.markdown(
    """
    <style>
        .main-title {font-size:2.3rem;font-weight:bold;color:#4F8BF9;}
        .sidebar .sidebar-content { background-color: #f8f9fa; }
        .data-card {
            background-color: #f0f4fa;
            padding: 1.2em;
            border-radius: 1em;
            box-shadow: 0 2px 8px rgba(79,139,249,0.05);
            margin-bottom: 1em;
        }
        .stButton button {background-color: #4F8BF9; color: white; border-radius: 0.5em;}
        .stButton button:hover {background-color: #205fa4;}
        .category-chip {display:inline-block; background:#e0e7f9; border-radius:15px; padding:5px 15px; margin-right:6px; font-size:1em;}
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="main-title">💼 Budget Analyzer</div>', unsafe_allow_html=True)
st.write("Track your income and expenses securely. Share your budget, get insights, and manage monthly goals!")

# --- USER AUTHENTICATION ---
def hash_pw(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

if "users" not in st.session_state:
    st.session_state.users = {}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = None

def signup_form():
    with st.expander("Don't have an account? Sign Up", expanded=True):
        new_user = st.text_input("👤 Choose Username", key="signup_user")
        new_pw = st.text_input("🔒 Choose Password", type="password", key="signup_pw")
        if st.button("Sign Up", key="signup_btn"):
            if new_user in st.session_state.users:
                st.error("❌ Username already exists.")
            elif not new_user or not new_pw:
                st.error("❗ Username and password required.")
            else:
                st.session_state.users[new_user] = {
                    "password": hash_pw(new_pw),
                    "shared_with": {},
                    "data": pd.DataFrame(columns=["date", "type", "category", "amount"]),
                    "categories": ["Food", "Transport", "Shopping", "Bills"]
                }
                st.success("✅ Account created. Please log in.")

def login_form():
    with st.expander("Log In", expanded=True):
        user = st.text_input("👤 Username", key="login_user")
        pw = st.text_input("🔒 Password", type="password", key="login_pw")
        if st.button("Log In", key="login_btn"):
            if user not in st.session_state.users:
                st.error("❌ User not found.")
            elif hash_pw(pw) != st.session_state.users[user]["password"]:
                st.error("❌ Incorrect password.")
            else:
                st.session_state.logged_in = user
                st.success(f"✅ Logged in as {user}")

if not st.session_state.logged_in:
    signup_form()
    login_form()
    st.stop()

user = st.session_state.logged_in

# --- SIDEBAR: SHARING LOGIC & ACCESS ---
with st.sidebar:
    st.image("https://img.icons8.com/color/96/budget.png", width=80)
    st.header(f"👋 Hi, {user}")
    st.markdown("---")
    st.subheader("Share your data")
    share_with = st.text_input("Share with (username):", key="share_user")
    access_type = st.selectbox("Access Type", ["View", "Update"], key="share_access")
    if st.button("Grant Access", key="share_btn"):
        if share_with not in st.session_state.users:
            st.error("No such user.")
        elif share_with == user:
            st.error("Cannot share with yourself.")
        else:
            st.session_state.users[user]["shared_with"][share_with] = access_type
            st.success(f"Access granted to {share_with} ({access_type})")

    st.subheader("Access Shared Data")
    shared_by = [u for u, info in st.session_state.users.items() if user in info["shared_with"]]
    selected_shared_user = st.selectbox("View data shared by:", [""] + shared_by, key="shared_user")
    if selected_shared_user:
        access_level = st.session_state.users[selected_shared_user]["shared_with"][user]
        st.info(f"Viewing {selected_shared_user}'s data ({access_level} access)")
        data_owner = selected_shared_user
        can_edit = access_level == "Update"
    else:
        data_owner = user
        can_edit = True

# --- MAIN SECTION ---
st.markdown("---")
st.subheader("Expense Categories")
categories = st.session_state.users[data_owner]["categories"]
st.markdown(" ".join([f'<span class="category-chip">{cat}</span>' for cat in categories]), unsafe_allow_html=True)

if can_edit:
    col1, col2 = st.columns([3, 2])
    with col1:
        new_cat = st.text_input("Add new category", key="new_cat")
        if st.button("Add Category", key="add_cat_btn"):
            if new_cat and new_cat not in categories:
                categories.append(new_cat)
                st.success(f"Added category: {new_cat}")
    with col2:
        remove_cat = st.selectbox("Remove category", [""] + categories, key="remove_cat")
        if st.button("Remove Category", key="remove_cat_btn") and remove_cat:
            categories.remove(remove_cat)
            st.success(f"Removed category: {remove_cat}")

st.markdown("---")
st.subheader("Add Entry")
col1, col2, col3, col4 = st.columns([2, 2, 2, 2])
with col1:
    entry_date = st.date_input("Date", value=date.today(), key="entry_date")
with col2:
    entry_type = st.radio("Type", ["Income", "Expense"], key="entry_type")
with col3:
    entry_cat = "Income" if entry_type == "Income" else st.selectbox("Category", categories, key="entry_cat")
with col4:
    entry_amt = st.number_input("Amount (₹)", min_value=0.0, step=0.01, key="entry_amt")

if can_edit and st.button("Add Entry", key="add_entry_btn"):
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

st.markdown("---")
st.subheader(f"Entries for {date.today().strftime('%B %Y')} ({data_owner})")
current_month = date.today().month
current_year = date.today().year
df = st.session_state.users[data_owner]["data"]
df_month = df[(pd.to_datetime(df["date"]).dt.month == current_month) & (pd.to_datetime(df["date"]).dt.year == current_year)]

with st.expander("Show/Hide Table"):
    st.dataframe(df_month.style.highlight_max(subset=["amount"], color="lightblue"), height=250)

# --- DASHBOARD CARDS ---
income = df_month[df_month["type"] == "Income"]["amount"].sum()
expenses_by_cat = df_month[df_month["type"] == "Expense"].groupby("category")["amount"].sum()
total_expense = expenses_by_cat.sum()
if not df_month.empty:
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f'<div class="data-card"><b>💰 Total Income</b><br><span style="font-size:1.5em;color:#4F8BF9;">₹{income:.2f}</span></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="data-card"><b>🛒 Total Expenses</b><br><span style="font-size:1.5em;color:#DC143C;">₹{total_expense:.2f}</span></div>', unsafe_allow_html=True)
    with col3:
        if not expenses_by_cat.empty:
            max_cat = expenses_by_cat.idxmax()
            max_spent = expenses_by_cat.max()
            st.markdown(f'<div class="data-card"><b>🏆 Top Category</b><br>{max_cat} <span style="color:#DC143C;">₹{max_spent:.2f}</span></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="data-card"><b>🏆 Top Category</b><br>None</div>', unsafe_allow_html=True)

    st.markdown("---")
    # Progress bar
    progress = min(total_expense/income, 1.0) if income else 0
    st.progress(progress)
    if total_expense > income:
        st.warning(f"Expenses exceed income! Consider reducing spending in '{max_cat}' and other non-essential categories.")
    else:
        st.success("Your spending is within budget! Great job!")
else:
    st.info("No entries for the current month.")
