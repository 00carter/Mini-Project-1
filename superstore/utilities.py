import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

sns.set_theme() 

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

    palette = sns.color_palette("rocket_r", n_colors=10)
    
    def __init__(self, df):
        self.df = df

    def plot_most_profitable_products_barplot(self, axes=None):
        most_profitable_products = (
            self.df.groupby("Product Name", as_index=False)["Profit"]
            .sum()
            .sort_values("Profit", ascending=False)
            .head(10)
        )
        if axes is not None:
            sns.barplot(data=most_profitable_products, x="Profit", y="Product Name",
                        orient="h", hue="Product Name", ax=axes[0][0])
            axes[0][0].set_title("Most Profitable Products")
        else:
            sns.barplot(data=most_profitable_products, x="Profit", y="Product Name", orient="h")
            plt.title("Most Profitable Products")
            plt.show()

    def plot_highest_performing_cities_barplot(self, axes=None):
        highest_selling_cities = (
            self.df.groupby("City")["Sales"]
            .sum()
            .sort_values(ascending=False)
            .head(10)
            .reset_index()
        )
        if axes is not None:
            sns.barplot(data=highest_selling_cities, x="Sales", y="City",
                        orient="h", hue="City", ax=axes[0][1])
            axes[0][1].set_title("Highest Selling Cities")
        else:
            sns.barplot(data=highest_selling_cities, x="Sales", y="City", orient="h")
            plt.title("Highest Selling Cities")
            plt.show()

    def plot_sales_overtime_lineplot(self, axes=None):
        sales_change = (
            self.df.resample('ME', on='Order Date')['Sales']
            .sum()
            .reset_index()
        )
        if axes is not None:
            sns.lineplot(data=sales_change, x="Order Date", y="Sales", ax=axes[0][2])
            axes[0][2].set_title("Sales Trend Over Time")
        else:
            sns.lineplot(data=sales_change, x="Order Date", y="Sales")
            plt.title("Sales Trend Over Time")
            plt.show()

    def plot_shipping_insights_pie(self, axes=None):
        ship_mode_counts = self.df["Ship Mode"].value_counts().reset_index()
        if axes is not None:
            axes[1][0].pie(ship_mode_counts["count"], labels=ship_mode_counts["Ship Mode"], autopct="%1.1f%%")
            axes[1][0].set_title("Order Count by Ship Mode")
        else:
            plt.pie(ship_mode_counts["count"], labels=ship_mode_counts["Ship Mode"], autopct="%1.1f%%")
            plt.title("Order Count by Ship Mode")
            plt.show()

    def plot_shipping_insights_boxplot(self, axes=None):
        if axes is not None:
            sns.boxplot(data=self.df, x="Ship Mode", y="Shipping Duration", hue="Ship Mode",
                        ax=axes[1][1],
                        order=["Standard Class", "Second Class", "First Class", "Same Day"])
            axes[1][1].set_title("Shipping Duration by Ship Mode")
        else:
            sns.boxplot(data=self.df, x="Ship Mode", y="Shipping Duration",
                        order=["Standard Class", "Second Class", "First Class", "Same Day"])
            plt.title("Shipping Duration by Ship Mode")
            plt.show()
            
    def plot_top_customers(self, axes=None):
        highest_selling_customers = (
            self.df.groupby(["Customer ID", "Customer Name"])["Sales"].sum()
            .sort_values(ascending=False)
            .head(10)
            .reset_index()
        )
        if axes is not None:
            sns.barplot(data=highest_selling_customers, x="Sales", y="Customer Name",
                        orient="h", hue="Customer Name", ax=axes[1][2])
            axes[1][2].set_title("Highest Purchasing Customers")
        else:
            sns.barplot(data=highest_selling_customers, x="Sales", y="Customer Name", orient="h")
            plt.title("Highest Purchasing Customers")
            plt.show()

    def plot_sales_distribution_violin(self, axes=None):
        if axes is not None:
            sns.violinplot(data=self.df, x="Sales", ax=axes[0][0], color="salmon")
            axes[0][0].set_title("Sales Distribution (Violin)")
            axes[0][0].set_xlabel("Sales")
        else:
            sns.violinplot(data=self.df, x="Sales", color="salmon")
            plt.title("Sales Distribution (Violin)")
            plt.xlabel("Sales")
            plt.show()

    def plot_sales_distribution_box(self, axes=None):
        if axes is not None:
            sns.boxplot(data=self.df, x="Sales", ax=axes[0][1], color="salmon")
            axes[0][1].set_title("Sales Spread & Outliers")
            axes[0][1].set_xlabel("Sales")
        else:
            sns.boxplot(data=self.df, x="Sales", color="salmon")
            plt.title("Sales Spread & Outliers")
            plt.show()

    def plot_quantity_discounts_correlation_scatterplot(self, axes=None):
        if axes is not None:
            sns.scatterplot(data=self.df, x="Discount", y="Quantity", ax=axes[1][0])
            axes[1][0].set_title("Quantity vs. Discount")
        else:
            sns.scatterplot(data=self.df, x="Discount", y="Quantity")
            plt.title("Quantity vs. Discount")
            plt.show()

    def plot_correlation_heatmap(self, axes=None):
        if axes is not None:
            sns.heatmap(self.df[["Quantity", "Discount", "Sales", "Profit"]].corr(), annot=True, cmap="coolwarm", ax=axes[1][1])
            axes[1][1].set_title("Correlation Matrix")
        else:
            sns.heatmap(self.df[["Quantity", "Discount", "Sales", "Profit"]].corr(), annot=True, cmap="coolwarm")
            plt.title("Correlation Matrix")
            plt.show()


    def show_dashboard_1(self, show=True):
        try:
            fig, axes = plt.subplots(2, 3, figsize=(26, 12))
            fig.suptitle("Superstore Performance Dashboard", fontsize=18, fontweight="bold")
            fig.set_facecolor("white")

            self.plot_most_profitable_products_barplot(axes=axes)
            self.plot_highest_performing_cities_barplot(axes=axes)
            self.plot_sales_overtime_lineplot(axes=axes)
            self.plot_shipping_insights_pie(axes=axes)
            self.plot_shipping_insights_boxplot(axes=axes)
            self.plot_top_customers(axes=axes)

            plt.tight_layout(rect=[0, 0, 1, 0.96])

            if show:
                    plt.show()

        except KeyError:
            print("Column is missing")
        except Exception as e:
            print(f"Something went wrong: {e}")

    def show_dashboard_2(self, show=True):
        try:
            fig, axes = plt.subplots(2, 2, figsize=(26, 12))
            fig.suptitle("Sales Distribution & Correlation Overview", fontsize=18, fontweight="bold")
            fig.set_facecolor("white")

            self.plot_sales_distribution_violin(axes=axes)
            self.plot_sales_distribution_box(axes=axes)
            self.plot_quantity_discounts_correlation_scatterplot(axes=axes)
            self.plot_correlation_heatmap(axes=axes)

            plt.tight_layout(rect=[0, 0, 1, 0.96])

            if show:
                plt.show()

        except KeyError:
            print("Column is missing")
        except Exception as e:
            print(f"Something went wrong: {e}")

    def show_all(self, filename="superstore_dashboards.pdf"):
        self.show_dashboard_1()
        self.show_dashboard_2()
        
class Summary():

    def __init__(self, df):
        self.df = df

    def calculate_total_sales(self):
        try:
            return round(float(self.df["Sales"].sum()), 2)
        except KeyError:
            print("Column 'Sales' is missing")
        except Exception as e:
            print(f"Something went wrong: {e}")

    def calculate_total_profit(self):
        try:
            return round(float(self.df["Profit"].sum()), 2)
        except KeyError:
            print("Column 'Profit' is missing")
        except Exception as e:
            print(f"Something went wrong: {e}")

    def calculate_average_order_value(self):
        try:
            aov = self.df.groupby(["Order ID"])["Sales"].sum().mean()
            return round(float(aov), 2)
        except KeyError:
            print("Column 'Order ID' or 'Sales' is missing")
        except Exception as e:
            print(f"Something went wrong: {e}")

    def calculate_average_shipping_duration(self):
        try:
            average_shipping_duration = self.df["Shipping Duration"].dt.days.mean()
            return round(float(average_shipping_duration))
        except KeyError:
            print("Column 'Shipping Duration' is missing")
        except Exception as e:
            print(f"Something went wrong: {e}")

    def calculate_top_category(self):
        try:
            tc = self.df.groupby(["Category"])["Sales"].sum()
            return tc.idxmax()
        except KeyError:
            print("Column 'Category' or 'Sales' is missing")
        except Exception as e:
            print(f"Something went wrong: {e}")

    def calculate_top_region(self):
        try:
            tr = self.df.groupby(["Region"])["Sales"].sum()
            return tr.idxmax()
        except KeyError:
            print("Column 'Region' or 'Sales' is missing")
        except Exception as e:
            print(f"Something went wrong: {e}")

    def calculate_average_discount(self):
        try:
            ad = self.df["Discount"].mean()
            return round(float(ad), 2)
        except KeyError:
            print("Column 'Discount' is missing")
        except Exception as e:
            print(f"Something went wrong: {e}")

    def _summary_as_figure(self):
        fig, ax = plt.subplots(figsize=(8.5, 11))
        ax.axis("off")
        ax.text(0.05, 0.95, str(self), fontsize=12, va="top", family="monospace")
        return fig

    def __str__(self):
        return f"""
Summary:

Total Sales
${self.calculate_total_sales():,.2f}

Total Profit
${self.calculate_total_profit():,.2f}

Average Order Value
${self.calculate_average_order_value():,.2f}

Average Shipping Duration
{self.calculate_average_shipping_duration()} days

Top Category (by Sales)
{self.calculate_top_category()}

Top Region (by Sales)
{self.calculate_top_region()}

Average Discount
{self.calculate_average_discount() * 100}%
        """

class Pdf():

    def __init__(self, df):
        self.df = df

    def export_report(self, filename="exports/superstore_report.pdf"):
        v = Visualization(self.df )
        s = Summary(self.df )

        with PdfPages(filename) as pdf:
            fig1 = v.show_dashboard_1(show=False)
            pdf.savefig(fig1)
            plt.close(fig1)

            fig2 = v.show_dashboard_2(show=False)
            pdf.savefig(fig2)
            plt.close(fig2)

            fig3 = s._summary_as_figure()
            pdf.savefig(fig3)
            plt.close(fig3)