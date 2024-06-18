import pandas as pd

WALLETS_INFO =[]

excel_data = pd.read_excel("wallets_info.xlsx")
    
for index, row in excel_data.iterrows():
    # Запись информации в словарь WALLETS_INFO
    WALLETS_INFO.append(float(row['Liquidity Pool USD']))
    
print(sum(WALLETS_INFO))
