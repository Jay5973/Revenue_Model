import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

def calculate_dependent_params(installs, cpi, i2fc, fc2fr, fc_rate, first_trxn_size, astro_commission, contribution_1st_recharges):
    install_cost = installs * cpi
    fc = installs * i2fc
    fc_cost = fc * fc_rate
    first_rechargers = fc * fc2fr
    first_cash_load = first_rechargers * first_trxn_size
    total_cash_load = first_cash_load / (contribution_1st_recharges / 100)
    astrologer_earning = first_cash_load * (astro_commission / 100)
    oneastro_earning = first_cash_load - astrologer_earning
    cash_load_after_first_recharge = total_cash_load - first_cash_load
    oneastro_earning_for_1plus = cash_load_after_first_recharge * (astro_commission / 100)
    
    return {
        "Installs": installs,
        "CPI": cpi,
        "Install Cost": install_cost,
        "I2FC %": i2fc * 100,
        "FC2FR %": fc2fr * 100,
        "FC": fc,
        "FC Rate": fc_rate,
        "FC Cost": fc_cost,
        "1st Rechargers": first_rechargers,
        "1st Trxn Size": first_trxn_size,
        "1st Cash Load": first_cash_load,
        "Astro Commission %": astro_commission,
        "Astrologer Earning": astrologer_earning,
        "OneAstro Earning": oneastro_earning,
        "Contribution of 1st Recharges %": contribution_1st_recharges,
        "Total Cash Load": total_cash_load,
        "Cash Load After 1st Recharge": cash_load_after_first_recharge,
        "OneAstro Earning for 1+ Recharges": oneastro_earning_for_1plus
    }

st.title("Dynamic Financial Model")

# Sidebar Inputs
st.sidebar.header("Input Parameters")
installs = st.sidebar.number_input("Installs", value=1000)
cpi = st.sidebar.number_input("CPI", value=6)
i2fc = st.sidebar.number_input("I2FC %", value=65) / 100
fc2fr = st.sidebar.number_input("FC2FR %", value=11) / 100
fc_rate = st.sidebar.number_input("FC Rate", value=5)
first_trxn_size = st.sidebar.number_input("1st Transaction Size", value=65)
astro_commission = st.sidebar.number_input("Astro Commission %", value=50)
contribution_1st_recharges = st.sidebar.number_input("Contribution of 1st Recharges in total %", value=55)

# Calculate dependent parameters
dependent_params = calculate_dependent_params(installs, cpi, i2fc, fc2fr, fc_rate, first_trxn_size, astro_commission, contribution_1st_recharges)

# Arrange table in requested format
df_main = pd.DataFrame(list(dependent_params.items()), columns=["Parameter", "Value"])

# User Spends Calculation
user_spends = {
    "Acquisition Cost": dependent_params["Install Cost"],
    "FC Cost": dependent_params["FC Cost"],
    "Bonus Amount": "nil",
    "Total Spends": dependent_params["Install Cost"] + dependent_params["FC Cost"]
}

df_user_spends = pd.DataFrame(list(user_spends.items()), columns=["Parameter", "Value"])

# Cash Loads by User Calculation
cash_loads = {
    "OneAstro Profit 1st Recharge": dependent_params["OneAstro Earning"],
    "OneAstro Profit after 1st Recharge": dependent_params["OneAstro Earning for 1+ Recharges"],
    "Gross Profit": dependent_params["OneAstro Earning"] + dependent_params["OneAstro Earning for 1+ Recharges"]
}

df_cash_loads = pd.DataFrame(list(cash_loads.items()), columns=["Parameter", "Value"])

# Net Profit Calculation
net_profit = cash_loads["Gross Profit"] - user_spends["Total Spends"]
df_net_profit = pd.DataFrame([["Net Profit", net_profit]], columns=["Parameter", "Value"])

# Display Tables
st.subheader("Financial Summary")
st.table(df_main)

st.subheader("User Spends")
st.table(df_user_spends)

st.subheader("Cash Loads by User")
st.table(df_cash_loads)

st.subheader("Net Profit")
st.table(df_net_profit)

# Function to calculate dependent parameters, including Net Profit
def calculate_dependent_params(installs, cpi, i2fc, fc2fr, fc_rate, first_trxn_size, astro_commission, contribution_1st_recharges):
    install_cost = installs * cpi
    fc = installs * cpi * i2fc
    fc_cost = fc * fc_rate
    first_rechargers = fc * fc2fr
    first_cash_load = first_rechargers * first_trxn_size
    total_cash_load = first_cash_load / (contribution_1st_recharges / 100)
    astrologer_earning = first_cash_load * (astro_commission / 100)
    oneastro_earning = first_cash_load - astrologer_earning
    cash_load_after_first_recharge = total_cash_load - first_cash_load
    oneastro_earning_for_1plus = cash_load_after_first_recharge * (astro_commission / 100)
    
    gross_profit = oneastro_earning + oneastro_earning_for_1plus
    total_spends = install_cost + fc_cost
    net_profit = gross_profit - total_spends

    return net_profit

# Independent Parameters
default_values = {
    "Installs": 1000,
    "CPI": 6,
    "I2FC": 65,  # Percentage
    "FC2FR": 11,  # Percentage
    "FC Rate": 5,
    "1st Transaction Size": 65,
    "Astro Commission": 50,  # Percentage
    "Contribution of 1st Recharges in total": 55  # Percentage
}

# Define ranges for each parameter (without normalization)
parameter_ranges = {
    "Installs": np.linspace(500, 5000, 20),  # Example: 500 to 5000 in 20 steps
    "CPI": np.linspace(1, 15, 20),
    "I2FC": np.linspace(10, 90, 20),  # Percentage
    "FC2FR": np.linspace(5, 50, 20),  # Percentage
    "FC Rate": np.linspace(1, 10, 20),
    "1st Transaction Size": np.linspace(20, 200, 20),
    "Astro Commission": np.linspace(10, 90, 20),  # Percentage
    "Contribution of 1st Recharges in total": np.linspace(10, 90, 20)  # Percentage
}

# Streamlit app
st.title("Impact of Independent Parameters on Net Profit")

# Generate individual graphs for each parameter
for param, values in parameter_ranges.items():
    net_profits = []

    # Iterate over the range of values for the current parameter
    for val in values:
        temp_values = default_values.copy()
        temp_values[param] = val  # Update only the current parameter
        
        # Convert percentage values to decimal before calculation
        net_profit = calculate_dependent_params(
            installs=temp_values["Installs"],
            cpi=temp_values["CPI"],
            i2fc=temp_values["I2FC"] / 100,
            fc2fr=temp_values["FC2FR"] / 100,
            fc_rate=temp_values["FC Rate"],
            first_trxn_size=temp_values["1st Transaction Size"],
            astro_commission=temp_values["Astro Commission"],
            contribution_1st_recharges=temp_values["Contribution of 1st Recharges in total"]
        )
        net_profits.append(net_profit)

    # Create a Plotly line chart
    fig = px.line(x=values, y=net_profits, labels={"x": param, "y": "Net Profit"},
                  title=f"Effect of {param} on Net Profit")

    # Display the graph in Streamlit
    st.plotly_chart(fig)
