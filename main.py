import pandas as pd
from superstore.utilities import Cleaner, FeatureEngineering, Visualization

try:
    df = pd.read_excel("Superstore 2019.xls", index_col="Row ID")
except FileNotFoundError:
    print("Change file name to Superstore 2019.xls")

cleaner = Cleaner(df)
df = cleaner.clean()

fe = FeatureEngineering(df)
df = fe.add_columns()

v = Visualization(df)
v.show_all()