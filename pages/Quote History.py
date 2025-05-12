
import streamlit as st
from app.quote_storage import get_all_quotes, delete_quote

st.set_page_config(page_title="Quote History", layout="wide")
st.title("Quote History")

quotes = get_all_quotes()

if quotes:
    st.subheader("Saved Quotes")
    st.table([
        {
            "ID": q[0],
            "Builder": q[1],
            "Job": q[2],
            "Date": q[3],
            "Total ($)": f"{q[4]:,.2f}"
        } for q in quotes
    ])

    st.subheader("Delete a Quote")
    quote_id = st.number_input("Enter Quote ID to delete", min_value=1, step=1)

    if st.button("Delete Quote"):
        confirm = st.checkbox("Confirm delete")
        if confirm:
            delete_quote(quote_id)
            st.success(f"Quote ID {quote_id} deleted. Please refresh the page.")
        else:
            st.warning("Please confirm before deleting.")
else:
    st.info("No quotes found.")
