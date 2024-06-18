import pandas as pd
import glob

# Список файлов Excel для импорта
excel_files = glob.glob('foldert/*.xlsx')

# Создание пустого словаря для хранения DataFrames
dataframes = {}

# Чтение данных из каждого файла Excel и сохранение в словарь
for file in excel_files:
    # Получение имени файла без расширения для использования в качестве имени листа
    sheet_name = file.split('/')[-1].replace('.xlsx', '')
    df = pd.read_excel(file)
    dataframes[sheet_name] = df

# Создание нового Excel файла с несколькими листами
output_file = 'combined_excel_file.xlsx'

with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
    for sheet_name, df in dataframes.items():
        df.to_excel(writer, sheet_name=sheet_name, index=False)

print(f"Excel файл '{output_file}' успешно создан с {len(dataframes)} листами.")
