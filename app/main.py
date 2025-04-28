import streamlit as st
import pandas as pd

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
        return ['background-color: rgba(255, 99, 71, 0.4)'] * len(row)  # Light red background
    else:
        return [''] * len(row)

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

    if action == "View Inventory":
        st.subheader("📋 Inventory List")
        
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
        st.write("Here will be the AI-powered restocking recommendations...")
    
    if action == "Analytics":
        st.subheader("📊 Inventory Analytics")
        st.write("Here will be graphs and reports...")
    
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