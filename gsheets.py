import pandas as pd

spreadsheet_id = "1rh2HDxoimRo0TK48Pchw3w9VlUpGEh6kV4KgbL3kox0"
worthit_id = "269398112"
recipes_id = "680106006"

worthit = f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/export?format=csv&gid={worthit_id}"
recipes = f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/export?format=csv&gid={recipes_id}"

df_worthit = pd.read_csv(worthit)
print(df_worthit.head())