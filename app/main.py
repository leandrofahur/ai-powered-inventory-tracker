import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# TODO: Move this to a separate file helper.py
def highlight_low_stock(row):
    """
    Highlight rows where Quantity < Reorder Level.

    Args:
        row (pd.Series): A row of the DataFrame.

    Returns:
        list: A list of CSS styles to apply to the row.
    """

    quantity = row["Quantity"]
    reorder_level = row["Reorder Level"]

    if quantity < reorder_level:
        return ['background-color: rgba(255, 99, 71, 0.1)'] * len(row)  # Light red background
    else:
        return [''] * len(row)

# TODO: Move this to a separate file helper.py
def highlight_suggested_reorder(row):
    """
    Highlight the suggested reorder quantity.

    Args:
        row (pd.Series): A row of the DataFrame.

    Returns:
        list: A list of CSS styles to apply to the row.
    """

    suggested_reorder_quantity = row["Suggested Reorder Quantity"]

    styles = [''] * len(row)
    if suggested_reorder_quantity is not None:
        # Get the index of the "Suggested Reorder Quantity" column
        col_idx = row.index.get_loc("Suggested Reorder Quantity")
        styles[col_idx] = 'background-color: rgba(255, 255, 0, 0.1)'  # Light yellow background
    return styles


# TODO: Move this to a separate file helper.py
def add_warning_emoji(df):
    """
    Add warning emoji to items with low stock.

    Args:
        df (pd.DataFrame): The DataFrame to add warning emoji to.

    Returns:
        pd.DataFrame: The DataFrame with warning emoji added.
    """

    df = df.copy()
    for index, row in df.iterrows():        
        if row["Quantity"] < row["Reorder Level"]:
            df.at[index, "Item Name"] = f"⚠️ {row['Item Name']}"
    return df

def get_mock_inventory_data():
    """
    Get mock inventory data.

    Returns:
        pd.DataFrame: The inventory data.
    """
    data = {
            "Item Name": ["Coca-Cola 330ml", "Pepsi 330ml", "Water Bottle 500ml", "Energy Drink"],
            "SKU": ["CC-330", "PP-330", "WB-500", "ED-250"],
            "Category": ["Beverage", "Beverage", "Beverage", "Beverage"],
            "Quantity": [25, 15, 60, 8],
            "Reorder Level": [20, 20, 50, 10],
            "Supplier": ["Supplier A", "Supplier B", "Supplier C", "Supplier D"],
            "Expiration Date": ["2025-01-10", "2025-02-15", "2024-12-01", "2024-11-20"],
        }
    
    inventory_df = pd.DataFrame(data)

    return inventory_df

def main():
    st.set_page_config(page_title="Inventory Tracking", page_icon="📦", layout="wide")

    st.title("📦 Smart Inventory Tracking")
    st.subheader("Manage your inventory intelligently with AI agents 🤖")

    st.markdown("---")

    st.header("Dashboard Overview")
    st.subheader("Inventory Summary")
    
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(label="Total Items", value="150")
    with col2:
        st.metric(label="Low Stock Alerts", value="5")
    with col3:
        st.metric(label="Upcoming Expirations", value="2")
    
    st.markdown("---")

    st.subheader("Inventory Trends")

    st.header("Actions")
    st.write("👉 Select an action below:")

    action = st.selectbox(
        "What would you like to do?",
        ("View Inventory", "Restock Suggestions", "Analytics", "Chat with Assistant")
    )

    inventory_df = get_mock_inventory_data()

    if action == "View Inventory":
        st.subheader("📋 Inventory List")
                
        inventory_df = add_warning_emoji(inventory_df)
        
        # Highlight low stock items
        inventory_df = inventory_df.style.apply(highlight_low_stock, axis=1)

        # Display DataFrame nicely
        st.dataframe(
            inventory_df,
            use_container_width=True,
            hide_index=True
        )

    if action == "Restock Suggestions":
        st.subheader("🚚 Restock Suggestions")
        
        low_stock_df = inventory_df[inventory_df["Quantity"] < inventory_df["Reorder Level"]]        

        if low_stock_df.empty:
            st.success("🎉 All items are sufficiently stocked!")
        else:
            # Suggest reorder quantity (example: reorder to double the reorder level)
            low_stock_df["Suggested Reorder Quantity"] = (low_stock_df["Reorder Level"] * 2) - low_stock_df["Quantity"]
            low_stock_df = low_stock_df.style.apply(highlight_suggested_reorder, axis=1)
            st.dataframe(low_stock_df, use_container_width=True, hide_index=True)
    
    if action == "Analytics":
        st.subheader("📊 Inventory Analytics")

        st.write("Overview of your inventory data.")
        
        inventory_df = get_mock_inventory_data()

        st.markdown("### 📦 Quantity per Item")

        # Simple Bar Chart:
        st.bar_chart(data=inventory_df, x="Item Name", y="Quantity", use_container_width=True)

        st.markdown("---")

        st.markdown("### 🧃 Stock Distribution (Pie Chart)")

        # Pie Chart:
        fig, ax = plt.subplots()
        ax.pie(inventory_df["Quantity"], labels=inventory_df["Item Name"], autopct='%1.1f%%', startangle=90)
        ax.axis('equal')  # Equal aspect ratio makes the pie chart circular
        st.pyplot(fig)

        st.markdown("---")
        st.info("ℹ️ More analytics coming soon: Fastest movers, Expirations, Forecasts!")
    
    if action == "Chat with Assistant":
        st.subheader("🧠 Chat with Inventory Assistant")
        st.write("Here will be the chatbot interface...")


    # st.sidebar.title("Navigation")
    # st.sidebar.subheader("Inventory")
    # inventory_name = st.sidebar.text_input("Inventory Name", value="Inventory")

    # st.sidebar.subheader("Model")
    # model_name = st.sidebar.selectbox("Model", ["GPT-4", "GPT-3.5"])

if __name__ == "__main__":
    main()