import pandas as pd

def sales_summary() -> pd.DataFrame:
    sales = pd.DataFrame(
        {
            "product": ["keyboard", "mouse", "monitor", "keyboard", "monitor"],
            "units": [3, 10, 2, 5, 1],
            "price": [45.0, 12.5, 220.0, 45.0, 220.0],
        }
    )

    sales["total"] = sales["units"] * sales["price"]
    return sales.groupby("product", as_index=False)["total"].sum()

if __name__ == "__main__":
    print(sales_summary())
