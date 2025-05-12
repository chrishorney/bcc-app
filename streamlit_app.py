
import streamlit as st
import datetime
from app.quote_logic import calculate_quote
from app.deepseek_ai import ask_deepseek, build_quote_prompt
from app.quote_storage import create_quotes_table, save_quote

st.set_page_config(page_title="Concrete Quote Generator", layout="wide")
st.session_state["quote_date"] = datetime.date.today()
create_quotes_table()

st.title("Concrete Quote Generator")
st.markdown("Enter the job details below:")

with st.form("quote_form"):
    builder_name = st.text_input("Builder Name", value="ABC Luxury Builders")
    discount_percent = st.number_input("Builder Discount (%)", min_value=0.0, max_value=100.0, value=5.0)

    st.subheader("Slab Details")
    slab_sqft = st.number_input("Slab Area (sqft)", min_value=0.0, value=2500.0)
    thickness = st.number_input("Concrete Thickness (inches)", min_value=0.0, value=6.0)

    st.subheader("Piers")
    num_piers = st.number_input("Number of Piers", min_value=0, value=20)
    pier_price = st.number_input("Price per Pier", min_value=0.0, value=350.0)

    st.subheader("Rebar")
    rebar_feet = st.number_input("Estimated Rebar (feet)", min_value=0.0, value=1000.0)

    st.subheader("Dirt Work")
    dirt_yards = st.number_input("Estimated Dirt Work (cubic yards)", min_value=0.0, value=300.0)
    dirt_price = st.number_input("Dirt Price per Yard", min_value=0.0, value=12.0)

    st.subheader("Labor Hours")
    labor_hours = {}
    labor_roles = ["Forming Carpenter", "Concrete Finisher", "Dirt Work Operator"]
    for role in labor_roles:
        labor_hours[role] = st.number_input(f"{role} Hours", min_value=0.0, value=0.0)

    st.subheader("Equipment Hours")
    equipment_hours = {}
    equipment_list = ["Pump Truck", "Bobcat Rental"]
    for eq in equipment_list:
        equipment_hours[eq] = st.number_input(f"{eq} Hours", min_value=0.0, value=0.0)

    use_ai = st.checkbox("Use AI to generate quote instead of manual breakdown?")
    api_key = st.text_input("DeepSeek API Key", type="password") if use_ai else None

    submitted = st.form_submit_button("Generate Quote")

if submitted:
    if use_ai and api_key:
        prompt = build_quote_prompt(builder_name, slab_sqft, thickness, num_piers, rebar_feet, dirt_yards)
        ai_response = ask_deepseek(prompt, api_key)
        st.subheader("AI-Generated Quote")
        st.markdown(ai_response)
    else:
        job_details = {
            "slab_sqft": slab_sqft,
            "concrete_thickness_in": thickness,
            "num_piers": num_piers,
            "pier_price": pier_price,
            "rebar_feet": rebar_feet,
            "dirt_yards": dirt_yards,
            "dirt_price_per_yard": dirt_price,
            "labor_hours": labor_hours,
            "equipment_hours": equipment_hours,
            "builder_discount_percent": discount_percent
        }

        breakdown = calculate_quote(job_details)
        total = sum(breakdown.values())

        st.subheader("Manual Quote Breakdown")
        for category, cost in breakdown.items():
            st.write(f"**{category}:** ${cost:,.2f}")
        st.write(f"**Total Quote:** ${total:,.2f}")

        save_quote(
            builder=builder_name,
            job_name=f"Slab {int(slab_sqft)} sqft with {num_piers} piers",
            date=str(st.session_state.get("quote_date")),
            job_details=str(job_details),
            quote_breakdown=str(breakdown),
            total_price=total
        )

        st.success("Quote saved to database!")
