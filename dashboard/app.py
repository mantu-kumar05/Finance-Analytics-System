import os

import streamlit as st
import requests
import plotly.express as px


# ================= API URL =================

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")


# ================= PAGE CONFIG =================

st.set_page_config(
    page_title="Finance Analytics Dashboard",
    page_icon="💰",
    layout="wide"
)


st.title("💰 Finance Analytics Dashboard")


# ================= TOKEN STORAGE =================

if "token" not in st.session_state:
    st.session_state.token = None


# ============================================================
# LOGIN / REGISTER
# ============================================================

if st.session_state.token is None:

    login_tab, register_tab = st.tabs(
        ["🔐 Login", "📝 Register"]
    )


    # ========================================================
    # LOGIN
    # ========================================================

    with login_tab:

        st.subheader("Login")

        email = st.text_input(
            "Email",
            key="login_email"
        )

        password = st.text_input(
            "Password",
            type="password",
            key="login_password"
        )


        if st.button(
            "Login",
            key="login_button"
        ):

            try:

                # OAuth2 login requires form data
                response = requests.post(
                    f"{API_URL}/login",
                    data={
                        "username": email,
                        "password": password
                    }
                )


                if response.status_code == 200:

                    data = response.json()

                    st.session_state.token = data["access_token"]

                    st.success(
                        "Login successful!"
                    )

                    st.rerun()


                else:

                    st.error(
                        f"Login failed: {response.text}"
                    )


            except requests.exceptions.ConnectionError:

                st.error(
                    "FastAPI server is not running. "
                    "Please start uvicorn first."
                )


            except Exception as e:

                st.error(
                    f"Error: {str(e)}"
                )


    # ========================================================
    # REGISTER
    # ========================================================

    with register_tab:

        st.subheader("Create New Account")

        name = st.text_input(
            "Name",
            key="register_name"
        )

        register_email = st.text_input(
            "Email",
            key="register_email"
        )

        register_password = st.text_input(
            "Password",
            type="password",
            key="register_password"
        )


        if st.button(
            "Create Account",
            key="register_button"
        ):

            # Basic validation

            if not name:

                st.warning(
                    "Please enter your name."
                )

            elif not register_email:

                st.warning(
                    "Please enter your email."
                )

            elif not register_password:

                st.warning(
                    "Please enter a password."
                )

            else:

                try:

                    response = requests.post(
                        f"{API_URL}/register",
                        json={
                            "name": name,
                            "email": register_email,
                            "password": register_password
                        }
                    )


                    if response.status_code == 200:

                        st.success(
                            "Account created successfully! "
                            "Please login."
                        )


                    else:

                        st.error(
                            f"Registration failed: "
                            f"{response.text}"
                        )


                except requests.exceptions.ConnectionError:

                    st.error(
                        "FastAPI server is not running. "
                        "Please start uvicorn first."
                    )


                except Exception as e:

                    st.error(
                        f"Error: {str(e)}"
                    )


    # Stop here until user logs in
    st.stop()


# ============================================================
# AUTH HEADER
# ============================================================

headers = {
    "Authorization": f"Bearer {st.session_state.token}"
}


# ============================================================
# FINANCIAL SUMMARY
# ============================================================

st.subheader("📊 Financial Summary")


try:

    analytics_response = requests.get(
        f"{API_URL}/analytics",
        headers=headers
    )


    if analytics_response.status_code == 200:

        analytics = analytics_response.json()


        col1, col2, col3 = st.columns(3)


        col1.metric(
            "💰 Total Income",
            analytics["total_income"]
        )


        col2.metric(
            "💸 Total Expense",
            analytics["total_expense"]
        )


        col3.metric(
            "💵 Savings",
            analytics["savings"]
        )


    elif analytics_response.status_code == 401:

        st.error(
            "Session expired. Please login again."
        )

        st.session_state.token = None

        st.rerun()


    else:

        st.error(
            analytics_response.text
        )


except requests.exceptions.ConnectionError:

    st.error(
        "Cannot connect to FastAPI server."
    )


# ============================================================
# TRANSACTIONS
# ============================================================

st.subheader("💳 Transactions")


try:

    transaction_response = requests.get(
        f"{API_URL}/transactions",
        headers=headers
    )


    if transaction_response.status_code == 200:

        transactions = transaction_response.json()


        if transactions:

            st.dataframe(
                transactions,
                use_container_width=True
            )


            # ================================================
            # EXPENSE CHART
            # ================================================

            expenses = [
                transaction
                for transaction in transactions
                if transaction["transaction_type"] == "Expense"
            ]


            if expenses:

                st.subheader(
                    "📈 Expense Category Analysis"
                )


                fig = px.pie(
                    expenses,
                    names="category",
                    values="amount",
                    title="Expense Category"
                )


                st.plotly_chart(
                    fig,
                    use_container_width=True
                )


            else:

                st.info(
                    "No expense transactions available."
                )


        else:

            st.info(
                "No transactions found."
            )


    elif transaction_response.status_code == 401:

        st.error(
            "Session expired. Please login again."
        )

        st.session_state.token = None

        st.rerun()


    else:

        st.error(
            transaction_response.text
        )


except requests.exceptions.ConnectionError:

    st.error(
        "Cannot connect to FastAPI server."
    )


# ============================================================
# ADD TRANSACTION
# ============================================================

st.subheader("➕ Add Transaction")


amount = st.number_input(
    "Amount",
    min_value=0.0,
    step=100.0
)


category = st.text_input(
    "Category",
    placeholder="Food, Travel, Shopping..."
)


transaction_type = st.selectbox(
    "Transaction Type",
    [
        "Income",
        "Expense"
    ]
)


transaction_date = st.date_input(
    "Date"
)


if st.button(
    "Add Transaction",
    key="add_transaction_button"
):

    if amount <= 0:

        st.warning(
            "Amount must be greater than 0."
        )

    elif not category:

        st.warning(
            "Please enter a category."
        )

    else:

        try:

            response = requests.post(
                f"{API_URL}/transactions",
                headers=headers,
                json={
                    "amount": amount,
                    "category": category,
                    "transaction_type": transaction_type,
                    "transaction_date": str(
                        transaction_date
                    )
                }
            )


            if response.status_code == 200:

                st.success(
                    "Transaction added successfully!"
                )

                st.rerun()


            elif response.status_code == 401:

                st.error(
                    "Session expired. Please login again."
                )

                st.session_state.token = None

                st.rerun()


            else:

                st.error(
                    response.text
                )


        except requests.exceptions.ConnectionError:

            st.error(
                "Cannot connect to FastAPI server."
            )


# ============================================================
# LOGOUT
# ============================================================

st.sidebar.title("👤 Account")


if st.sidebar.button(
    "Logout"
):

    st.session_state.token = None

    st.rerun()
