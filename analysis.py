import streamlit as st

def main():
    st.set_page_config(page_title="Budget Analysis App", page_icon="💸", layout="centered")
    st.markdown(
        """
        <style>
        .main {background-color: #F6F6F6;}
        .stButton>button {background-color: #009688; color:white;}
        .stNumberInput>label {font-weight:bold;}
        </style>
        """, unsafe_allow_html=True
    )

    st.title("💸 Budget Analysis App")
    st.subheader("Easily track your monthly finances 🚀")

    st.markdown("---")
    st.markdown("### Enter your monthly budget and expenses:")

    col1, col2 = st.columns(2)
    with col1:
        input_budget = st.number_input("Monthly Budget ($)", min_value=0.0, format="%.2f", help="Set your total available budget for the month")
        house_expense = st.number_input("🏠 Housing Expenses ($)", min_value=0.0, format="%.2f")
        travel_expense = st.number_input("🚗 Travel Expenses ($)", min_value=0.0, format="%.2f")
    with col2:
        mess_expenses = st.number_input("🍽️ Mess Expenses ($)", min_value=0.0, format="%.2f")

        with st.expander("➕ Add Extra Expenses"):
            extra_expenses = []
            extra_count = st.number_input("How many extra expenses?", min_value=0, max_value=10, step=1)
            for i in range(extra_count):
                amount = st.number_input(f"Extra Expense {i+1} ($)", min_value=0.0, format="%.2f", key=f"extra_{i}")
                extra_expenses.append(amount)
    
    st.markdown("---")
    if st.button("🔍 Analyze Budget", use_container_width=True):
        total_expense = house_expense + travel_expense + mess_expenses + sum(extra_expenses)
        balance = input_budget - total_expense

        st.markdown("## 📊 Results")
        st.metric(label="Total Expenses", value=f"${total_expense:.2f}")
        st.metric(label="Budget Balance", value=f"${balance:.2f}")

        if total_expense < input_budget:
            st.success(f"🎉 You are **under budget** by ${balance:.2f}!")
        elif total_expense > input_budget:
            st.error(f"⚠️ You are **over budget** by ${-balance:.2f}!")
        else:
            st.info(f"✅ You are **exactly on budget**.")

        st.progress(min(total_expense / input_budget, 1.0), text="Budget Usage")

        with st.expander("See Expense Breakdown"):
            st.write(f"- Housing: ${house_expense:.2f}")
            st.write(f"- Travel: ${travel_expense:.2f}")
            st.write(f"- Mess: ${mess_expenses:.2f}")
            for i, amount in enumerate(extra_expenses):
                st.write(f"- Extra {i+1}: ${amount:.2f}")

if __name__ == "__main__":
    main()
