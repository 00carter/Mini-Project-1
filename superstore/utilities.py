class Cleaner():
    def __init__(self, df):
        self.df = df

    def _remove_duplicates(self):
        self.df.drop_duplicates(inplace=True)

    def _fix_postal_code(self):
        self.df["Postal Code"] = self.df["Postal Code"].astype('Int64')

    def _replace_missing_postal_code(self):
        self.df["Postal Code"] = self.df["Postal Code"].fillna(5401)

    def clean(self):
        try:
            self._remove_duplicates()
            self._fix_postal_code()
            self._replace_missing_values()
            return self.df
        except KeyError:
            print("Column Postal Code is missing")
        except Exception as e:
            print(f"Something went wrong: {e}")