import streamlit as st

def main():
    st.title("Budget Analysis App")

    st.write("Enter your monthly budget and expenses below:")

    input_budget = st.number_input("Monthly Budget ($)", min_value=0.0, format="%.2f")
    house_expense = st.number_input("Housing Expenses ($)", min_value=0.0, format="%.2f")
    travel_expense = st.number_input("Travel Expenses ($)", min_value=0.0, format="%.2f")
    mess_expenses = st.number_input("Mess Expenses ($)", min_value=0.0, format="%.2f")

    extra_expenses = []
    add_extra = st.checkbox("Add Extra Expenses?")
    while add_extra:
        extra_expense = st.number_input(f"Extra Expense {len(extra_expenses)+1} ($)", min_value=0.0, format="%.2f", key=f"extra_{len(extra_expenses)}")
        if extra_expense > 0:
            extra_expenses.append(extra_expense)
        add_more = st.checkbox("Add another extra expense?", key=f"add_more_{len(extra_expenses)}")
        if not add_more:
            break

    if st.button("Analyze Budget"):
        total_expense = house_expense + travel_expense + mess_expenses + sum(extra_expenses)
        if total_expense < input_budget:
            st.success(f"You are under budget by ${input_budget - total_expense:.2f}\nTotal monthly expenses = ${total_expense:.2f}")
        elif total_expense > input_budget:
            st.error(f"You are over budget by ${total_expense - input_budget:.2f}\nTotal monthly expenses = ${total_expense:.2f}")
        else:
            st.info(f"You are on budget. Total expenses = ${total_expense:.2f}")

if __name__ == "__main__":
    main()
