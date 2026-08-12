import pandas as pd

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
            self._replace_missing_postal_code()
            return self.df
        except KeyError:
            print("Column Postal Code is missing")
        except Exception as e:
            print(f"Something went wrong: {e}")

    def get_outliers(self, column_name):
        try:
            Q1, Q3 = self.df[column_name].quantile(0.25), self.df[column_name].quantile(0.75)

            IQR = Q3 - Q1
            lower_limit = Q1 - (1.5 * IQR)
            upper_limit = Q3 + (1.5 * IQR)

            outlier_filter = (self.df[column_name] < lower_limit) | (self.df[column_name] > upper_limit)
            return f"{len(self.df[outlier_filter])} outliers in {column_name} column"
        except KeyError:
            print("Invalid column name")
        except Exception as e:
            print(f"Something went wrong: {e}")

class FeatureEngineering():
    def __init__(self, df):
        self.df = df

    def _calculate_profit_margin(self):
        self.df["Profit Margin"] = (self.df["Profit"] / self.df["Sales"]).round(2)

    def _calculate_shipping_duration(self):
        self.df["Shipping Duration"] = self.df["Ship Date"] - self.df["Order Date"]

    def _categorize_sales_performance(self):
        cutoff = [
            self.df["Sales"].quantile(0),
            self.df["Sales"].quantile(0.25),
            self.df["Sales"].quantile(0.50),
            self.df["Sales"].quantile(0.75),
            self.df["Sales"].quantile(1),
        ]
        labels = ["Low", "Medium", "High", "Very High"]
        self.df["Sales Performance Category"] = pd.cut(
            self.df["Sales"], bins=cutoff, labels=labels, include_lowest=True
        )

    def add_columns(self):
        try:
            self. _calculate_profit_margin()
            self._calculate_shipping_duration()
            self._categorize_sales_performance()
            return self.df
        except KeyError:
            print("Column Postal Code is missing")
        except Exception as e:
            print(f"Something went wrong: {e}")