import sqlite3

def get_prices_from_db(db_path="database/jobs.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT material_name, price_per_unit FROM Materials")
    materials = {row[0]: row[1] for row in cursor.fetchall()}

    cursor.execute("SELECT labor_type, hourly_rate FROM LaborRates")
    labor_rates = {row[0]: row[1] for row in cursor.fetchall()}

    cursor.execute("SELECT equipment_name, hourly_rate FROM EquipmentRates")
    equipment_rates = {row[0]: row[1] for row in cursor.fetchall()}

    conn.close()
    return materials, labor_rates, equipment_rates

def calculate_quote(job_details, db_path="database/jobs.db"):
    materials, labor_rates, equipment_rates = get_prices_from_db(db_path)

    # Extract input details
    sqft = job_details.get("slab_sqft", 0)
    thickness = job_details.get("concrete_thickness_in", 4)  # inches
    piers = job_details.get("num_piers", 0)
    pier_price = job_details.get("pier_price", 350)
    rebar_feet = job_details.get("rebar_feet", 0)
    dirt_yards = job_details.get("dirt_yards", 0)
    dirt_price_per_yard = job_details.get("dirt_price_per_yard", 10)
    labor_hours = job_details.get("labor_hours", {})
    equipment_hours = job_details.get("equipment_hours", {})
    builder_discount = job_details.get("builder_discount_percent", 0)

    # Concrete volume in cubic yards
    cubic_yards = (sqft * (thickness / 12)) / 27
    concrete_cost = round(cubic_yards * materials.get("Concrete", 0), 2)

    rebar_cost = round(rebar_feet * materials.get("Rebar", 0), 2)
    pier_cost = round(piers * pier_price, 2)
    dirt_cost = round(dirt_yards * dirt_price_per_yard, 2)

    total_labor = sum(labor_hours[role] * labor_rates.get(role, 0) for role in labor_hours)
    total_equipment = sum(equipment_hours[eq] * equipment_rates.get(eq, 0) for eq in equipment_hours)

    subtotal = sum([
        concrete_cost,
        rebar_cost,
        pier_cost,
        dirt_cost,
        total_labor,
        total_equipment
    ])

    discount = round(subtotal * (builder_discount / 100), 2)
    total = round(subtotal - discount, 2)

    breakdown = {
        "Concrete": concrete_cost,
        "Rebar": rebar_cost,
        "Piers": pier_cost,
        "Dirt Work": dirt_cost,
        "Labor": round(total_labor, 2),
        "Equipment": round(total_equipment, 2),
        "Subtotal": round(subtotal, 2),
        "Builder Discount": discount,
        "Total Quote": total
    }

    return breakdown
