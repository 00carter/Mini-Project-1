import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

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
            print("Column is missing")
        except Exception as e:
            print(f"Something went wrong: {e}")

class Visualization():
    def __init__(self, df):
        self.df = df

    def _plot_top_products(self):
        highest_selling_products = (
            self.df.groupby("Product Name", as_index=False)["Sales"]
            .sum()
            .sort_values("Sales", ascending=False)
            .head(10)
        )
        sns.barplot(data=highest_selling_products, x="Sales", y="Product Name", orient="h")
        plt.title("Top 10 Selling Products")
        plt.show()

    def _plot_top_cities(self):
        highest_selling_cities = (
            self.df.groupby("City")["Sales"]
            .sum()
            .sort_values(ascending=False)
            .head(10)
            .reset_index()
        )
        sns.barplot(data=highest_selling_cities, x="Sales", y="City", orient="h")
        plt.title("Top 10 Selling Cities")
        plt.show()

    def _plot_sales_trend(self):
        sales_change = (
            self.df.resample('ME', on='Order Date')['Sales']
            .sum()
            .reset_index()
        )
        sns.lineplot(data=sales_change, x="Order Date", y="Sales")
        plt.title("Sales Over Time")
        plt.show()

    def _plot_top_customers(self):
        highest_selling_customers = (
            self.df.groupby(["Customer ID", "Customer Name"])["Sales"].sum()
            .sort_values(ascending=False)
            .head(10)
            .reset_index()
        )
        sns.barplot(data=highest_selling_customers, x="Sales", y="Customer Name", orient="h")
        plt.title("Top 10 Purchasing Customers")
        plt.show()

    def _plot_sales_distribution(self):
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        sns.histplot(data=self.df, x="Sales", kde=True, ax=axes[0])
        axes[0].set_title("Sales Distribution")
        sns.boxplot(data=self.df, x="Sales", ax=axes[1])
        axes[1].set_title("Sales Spread & Outliers")
        plt.tight_layout()
        plt.show()

    def _plot_shipping_duration(self):
        self.df["Shipping Duration Days"] = self.df["Shipping Duration"].dt.days
        sns.boxplot(data=self.df, x="Ship Mode", y="Shipping Duration Days")
        plt.title("Shipping Duration by Ship Mode")
        plt.show()

    def _plot_shipping_mode(self):
        ship_mode_counts = self.df["Ship Mode"].value_counts().reset_index()
        sns.barplot(data=ship_mode_counts, x="count", y="Ship Mode")
        plt.title("Order Count by Ship Mode")
        plt.xlabel("Number of Orders")
        plt.show()

    def _plot_quantity_discount_correlation(self):
        sns.scatterplot(data=self.df, x="Discount", y="Quantity")
        plt.title("Quantity vs. Discount")
        plt.show()

    def show_all(self):
        try:
            self._plot_top_products()
            self._plot_top_cities()
            self._plot_sales_trend()
            self._plot_top_customers()
            self._plot_sales_distribution()
            self._plot_shipping_duration()
            self._plot_shipping_mode()
            self._plot_quantity_discount_correlation()
        except KeyError:
            print("Column is missing")
        except Exception as e:
            print(f"Something went wrong: {e}")