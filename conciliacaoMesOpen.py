"""
This module contains functions to retrieve bank data and reconciliation data from the ContaAzul API for a list of clients.

The main() function loops through each client, gets their bank data, then loops through each month of the current year to retrieve reconciliation data for that month from the ContaAzul API.

The reconciliation data for each month is appended to a DataFrame, then all DataFrames are concatenated into a single result DataFrame which is exported to Excel at the end.
"""

import pandas as pd
import requests
from datetime import datetime
import calendar
import time


def get_bank_data(client_name, authorization_token):
    url = "https://services.contaazul.com/app/bank/"
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:122.0) Gecko/20100101 Firefox/122.0",
        "Accept": "application/json, text/plain, */*",
        "X-Authorization": authorization_token,
    }
    response = requests.get(url, headers=headers)
    data = response.json()["data"]
    return [
        {
            "NomeCliente": client_name,
            "Nome do Banco": entry["description"],
            "token Banco": entry["uuid"],
        }
        for entry in data
    ]


def get_reconciliation_data(df, start_date, end_date, headers):
    url = "https://services.contaazul.com/goldengate/rest/private/reconciliations/v1/pending-reconciliations/totals"
    dfs_list = []
    for index, row in df.iterrows():
        querystring = {
            "end_date": end_date,
            "financial_account_id": row["token Banco"],
            "start_date": start_date,
        }
        df.at[index, "start_date"] = querystring["start_date"]
        response = requests.get(url, headers=headers, params=querystring)
        response_data = response.json()
        expense = response_data.get("expense", 0)
        total = response_data.get("total", 0)
        revenue = response_data.get("revenue", 0)
        df.at[index, "expense"] = expense
        df.at[index, "total"] = total
        df.at[index, "revenue"] = revenue
    dfs_list.append(df.copy())
    return dfs_list


def main():
    # Ler excel com os authorizations dos clientes
    dfClientes = pd.read_excel("authorization.xlsx")

    # Removendo os espaços em branco
    dfClientes["XAuthorization"] = dfClientes["XAuthorization"].str.strip()

    # Actual date
    today_date = datetime.now()

    # Initialize result_df before the loop
    result_df = pd.DataFrame(
        columns=[
            "NomeCliente",
            "Nome do Banco",
            "token Banco",
            "start_date",
            "expense",
            "total",
            "revenue",
        ]
    )

    # List to store individual DataFrames for each bank
    dfs_list = []

    # Loop over clients
    for client_name, authorization_token in zip(
        dfClientes["NomeCliente"], dfClientes["XAuthorization"]
    ):
        bank_data = get_bank_data(client_name, authorization_token)
        df = pd.DataFrame(bank_data)
        print(df)

        # Loop over the months from January until the current month
        for month in range(1, today_date.month + 1):
            first_day = datetime(today_date.year, month, 1)
            last_day = datetime(
                today_date.year, month, calendar.monthrange(today_date.year, month)[1]
            )
            start_date = first_day.strftime("%Y-%m-%d")
            end_date = last_day.strftime("%Y-%m-%d")
            print(f"Month: {month}, First day: {start_date}, Last day: {end_date}")

            headers = {
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:122.0) Gecko/20100101 Firefox/122.0",
                "Accept": "application/json, text/plain, */*",
                "X-Authorization": authorization_token,
            }

            dfs_list.extend(
                get_reconciliation_data(df.copy(), start_date, end_date, headers)
            )
            time.sleep(2)

    # Concatenate all DataFrames in the list into a single DataFrame
    result_df = pd.concat(dfs_list, ignore_index=True)

    # Display the final DataFrame with new columns after processing all months
    # print(result_df)

    # Export the DataFrame to an Excel file after the loop
    result_df.to_excel("Conciliacao_Abertas_Mes.xlsx", index=False)
    return result_df


if __name__ == "__main__":
    main()
