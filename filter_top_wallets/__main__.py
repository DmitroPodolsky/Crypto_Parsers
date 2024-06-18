from datetime import datetime
import requests
import pandas as pd
from config import settings

responce = requests.get(f'https://api.w3w.ai/linea/v2/explorer/token/{settings.TOKEN}/top_holders?page=1&size=50000')
data = responce.json()

# Преобразование данных в DataFrame
df = pd.DataFrame(data['data'])

# Преобразование столбца 'balance' в числовой формат
df['balance'] = pd.to_numeric(df['balance'])

# Фильтрация данных по балансу
filtered_df = df[df['balance'] * 1.75 > 25000]

# Сохранение отфильтрованных данных в Excel файл
date_str = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
data_dir = settings.DATA_DIR / date_str
data_dir.mkdir(parents=True, exist_ok=True) 
file_path = data_dir / "output.xlsx"
filtered_df.to_excel(file_path, index=False)

print(f"Данные сохранены в файл: output.xlsx")