import streamlit as st
import pandas as pd

from database import (
    create_tables,
    add_restaurant,
    add_waste,
    get_restaurants,
    get_waste_collections,
    update_collection,
    add_compost,
    get_compost
)

# Create database
create_tables()

# Page configuration
st.set_page_config(
    page_title="Kerala GreenCycle",
    page_icon="🌱",
    layout="wide"
)

st.title("🌱 Kerala GreenCycle")
st.subheader("Smart Organic Waste Management System")

st.write(
    "Connecting restaurants, waste collection, compost processing "
    "and government gardens."
)

# Sidebar
menu = st.sidebar.selectbox(
    "Select Module",
    [
        "🏠 Dashboard",
        "🏨 Restaurant Registration",
        "🥬 Submit Waste",
        "🚛 Waste Collection",
        "🌱 Compost Processing",
        "🏛️ Government Dashboard"
    ]
)


# ---------------------------------------------------
# DASHBOARD
# ---------------------------------------------------

if menu == "🏠 Dashboard":

    st.header("🌱 GreenCycle Dashboard")

    restaurants = get_restaurants()
    waste = get_waste_collections()
    compost = get_compost()

    total_restaurants = len(restaurants)

    total_waste = sum(
        row[3] for row in waste
    ) if waste else 0

    total_reward = sum(
        row[5] for row in waste
    ) if waste else 0

    total_compost = sum(
        row[2] for row in compost
    ) if compost else 0

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "🏨 Restaurants",
        total_restaurants
    )

    col2.metric(
        "🥬 Waste Collected",
        f"{total_waste:.1f} kg"
    )

    col3.metric(
        "💰 Restaurant Rewards",
        f"₹{total_reward:.2f}"
    )

    col4.metric(
        "🌱 Compost Produced",
        f"{total_compost:.1f} kg"
    )

    st.divider()

    st.info(
        "GreenCycle converts biodegradable restaurant waste "
        "into useful compost for gardens and agriculture."
    )


# ---------------------------------------------------
# RESTAURANT REGISTRATION
# ---------------------------------------------------

elif menu == "🏨 Restaurant Registration":

    st.header("🏨 Register Restaurant")

    with st.form("restaurant_form"):

        name = st.text_input(
            "Restaurant Name"
        )

        owner = st.text_input(
            "Owner Name"
        )

        phone = st.text_input(
            "Phone Number"
        )

        district = st.selectbox(
            "District",
            [
                "Alappuzha",
                "Ernakulam",
                "Idukki",
                "Kannur",
                "Kasaragod",
                "Kollam",
                "Kottayam",
                "Kozhikode",
                "Malappuram",
                "Palakkad",
                "Pathanamthitta",
                "Thiruvananthapuram",
                "Thrissur",
                "Wayanad"
            ]
        )

        municipality = st.text_input(
            "Municipality / Panchayat"
        )

        address = st.text_area(
            "Restaurant Address"
        )

        submit = st.form_submit_button(
            "Register Restaurant"
        )

        if submit:

            if not name or not owner or not phone:
                st.error(
                    "Please fill all required fields."
                )

            else:

                add_restaurant(
                    name,
                    owner,
                    phone,
                    district,
                    municipality,
                    address
                )

                st.success(
                    "Restaurant registered successfully! ✅"
                )


# ---------------------------------------------------
# SUBMIT WASTE
# ---------------------------------------------------

elif menu == "🥬 Submit Waste":

    st.header("🥬 Submit Restaurant Waste")

    restaurants = get_restaurants()

    if not restaurants:

        st.warning(
            "Please register a restaurant first."
        )

    else:

        restaurant_names = [
            f"{r[0]} - {r[1]}"
            for r in restaurants
        ]

        selected = st.selectbox(
            "Select Restaurant",
            restaurant_names
        )

        restaurant_id = int(
            selected.split(" - ")[0]
        )

        waste_type = st.selectbox(
            "Waste Type",
            [
                "Vegetable / Food Waste",
                "Fruit Waste",
                "Other Biodegradable Waste",
                "Meat Waste"
            ]
        )

        quantity = st.number_input(
            "Waste Quantity (kg)",
            min_value=0.1,
            step=0.5
        )

        st.info(
            "Prototype reward rate: ₹5 per kg."
        )

        reward = quantity * 5

        st.write(
            f"Estimated reward: **₹{reward:.2f}**"
        )

        if st.button("Submit Waste"):

            add_waste(
                restaurant_id,
                waste_type,
                quantity
            )

            st.success(
                f"Waste submitted successfully! "
                f"Estimated reward: ₹{reward:.2f}"
            )


# ---------------------------------------------------
# WASTE COLLECTION
# ---------------------------------------------------

elif menu == "🚛 Waste Collection":

    st.header("🚛 Waste Collection Management")

    waste = get_waste_collections()

    if not waste:

        st.info(
            "No waste collection requests yet."
        )

    else:

        df = pd.DataFrame(
            waste,
            columns=[
                "ID",
                "Restaurant",
                "Waste Type",
                "Quantity (kg)",
                "Status",
                "Reward",
                "Collection Date"
            ]
        )

        st.dataframe(
            df,
            use_container_width=True
        )

        st.subheader(
            "Mark Collection as Completed"
        )

        collection_id = st.number_input(
            "Collection ID",
            min_value=1,
            step=1
        )

        if st.button(
            "Mark as Collected"
        ):

            update_collection(
                collection_id
            )

            st.success(
                "Collection completed successfully! 🚛"
            )

            st.rerun()


# ---------------------------------------------------
# COMPOST PROCESSING
# ---------------------------------------------------

elif menu == "🌱 Compost Processing":

    st.header("🌱 Compost Processing Centre")

    st.write(
        "Record the conversion of biodegradable waste "
        "into compost."
    )

    waste_quantity = st.number_input(
        "Processed Waste (kg)",
        min_value=1.0,
        step=1.0
    )

    compost_quantity = st.number_input(
        "Produced Compost (kg)",
        min_value=0.1,
        step=0.5
    )

    if st.button(
        "Record Compost Production"
    ):

        add_compost(
            waste_quantity,
            compost_quantity
        )

        st.success(
            "Compost production recorded! 🌱"
        )

    st.divider()

    compost = get_compost()

    if compost:

        df = pd.DataFrame(
            compost,
            columns=[
                "ID",
                "Waste Processed (kg)",
                "Compost Produced (kg)",
                "Date"
            ]
        )

        st.dataframe(
            df,
            use_container_width=True
        )


# ---------------------------------------------------
# GOVERNMENT DASHBOARD
# ---------------------------------------------------

elif menu == "🏛️ Government Dashboard":

    st.header(
        "🏛️ Municipality / Government Dashboard"
    )

    restaurants = get_restaurants()
    waste = get_waste_collections()
    compost = get_compost()

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Registered Restaurants",
        len(restaurants)
    )

    total_waste = sum(
        x[3] for x in waste
    ) if waste else 0

    col2.metric(
        "Total Waste",
        f"{total_waste:.1f} kg"
    )

    total_compost = sum(
        x[2] for x in compost
    ) if compost else 0

    col3.metric(
        "Total Compost",
        f"{total_compost:.1f} kg"
    )

    st.divider()

    st.subheader(
        "🏨 Registered Restaurants"
    )

    if restaurants:

        restaurant_df = pd.DataFrame(
            restaurants,
            columns=[
                "ID",
                "Restaurant",
                "Owner",
                "Phone",
                "District",
                "Municipality",
                "Address"
            ]
        )

        st.dataframe(
            restaurant_df,
            use_container_width=True
        )

    st.subheader(
        "📊 Waste Collection Records"
    )

    if waste:

        waste_df = pd.DataFrame(
            waste,
            columns=[
                "ID",
                "Restaurant",
                "Waste Type",
                "Quantity",
                "Status",
                "Reward",
                "Collection Date"
            ]
        )

        st.dataframe(
            waste_df,
            use_container_width=True
        )

    st.success(
        "Government can use this dashboard to monitor "
        "organic waste management."
    )
