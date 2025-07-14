import streamlit as st
from PIL import Image
from pymongo import MongoClient
from datetime import datetime

# --- Streamlit Config ---
st.set_page_config(page_title="Donate to Nature 🌱", layout="centered")

# --- MongoDB Setup ---
MONGO_URI = "mongodb+srv://dummy:1234@cluster0.6wr4bga.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(MONGO_URI)
db = client["CarbonApp"]
donation_col = db["donations"]
feedback_col = db["feedback"]

# --- Logo ---
logo = Image.open("./media/download.jpg")
st.image(logo, width=150)

# --- University Info ---
st.markdown("## 🌱 Srinivas University - Campus Tree Plantation Initiative")
st.markdown("""
[Srinivas University](https://srinivasuniversity.edu.in/) in Mangalore is a Private Research and Skill-Focused University established in 2013 by the Karnataka State Act.  
It is the flagship of 18 institutions founded by the A. Shama Rao Foundation, a charitable trust started in 1988.

The university offers 160+ undergraduate, postgraduate, and research programs across 10 faculties, and is deeply committed to sustainability and environmental responsibility.

As part of our commitment, **we aim to plant trees across our university campuses** — fostering a greener, cleaner, and healthier learning environment.
""")

# --- Why Donate ---
st.markdown("---")
st.markdown("## 🌿 Why Donate?")
st.markdown("""
**🌱 Plant Trees**  
Your donation directly funds tree planting activities across our campus and local communities.

**💚 Support Education + Environment**  
You're helping a university build a sustainable future for students and nature.

**🌍 Combat Climate Change**  
Trees absorb CO2, helping to mitigate the effects of global warming.

**💸 Tax Benefits**  
All donations are eligible for tax benefits under Section 80G.
""")

# --- Donation Form ---
st.markdown("---")
st.markdown("## 🤝 Make a Donation")

with st.form("donation_form"):
    name = st.text_input("Full Name")
    email = st.text_input("Email Address")
    phone = st.text_input("Phone Number")
    amount_option = st.radio("Donation Amount (₹)", [500, 1000, 2000, 5000, 10000, "Custom"])

    if amount_option == "Custom":
        custom_amount = st.number_input("Enter custom amount", min_value=1)
        donation_amount = custom_amount
    else:
        donation_amount = amount_option

    submit = st.form_submit_button("🌳 Donate Now")

if submit:
    if name and email and phone:
        # Save donation
        donation_record = {
            "name": name,
            "email": email,
            "phone": phone,
            "amount": donation_amount,
            "timestamp": datetime.now()
        }
        donation_col.insert_one(donation_record)

        # Success Message
        st.success(f"Thank you, {name}! Please scan the QR code below to donate ₹{donation_amount}.")
        qr_image = Image.open("./media/GooglePay_QR.webp")
        st.image(qr_image, caption="Scan to Pay", use_container_width=False)
    else:
        st.warning("Please fill in all fields before submitting.")

# --- Total Trees Planted ---
st.markdown("---")
st.markdown("## 🌳 Trees You've Helped Plant")

donations = donation_col.find()
total_amount = sum(d.get("amount", 0) for d in donations)
trees_planted = total_amount // 100

st.success(f"🎉 Thanks to your support, we've planted **{trees_planted} trees**!")

# --- Feedback Section ---
st.markdown("---")
st.markdown("## ✍️ Share Your Feedback")

with st.form("feedback_form"):
    fb_name = st.text_input("Your Name", key="fb_name")
    fb_message = st.text_area("Your Feedback", key="fb_msg")
    fb_submit = st.form_submit_button("Send Feedback")

if fb_submit:
    if fb_name and fb_message:
        feedback_col.insert_one({
            "name": fb_name,
            "message": fb_message,
            "timestamp": datetime.now()
        })
        st.success("Thank you for your feedback!")
    else:
        st.warning("Please fill in all fields before submitting.")

# --- Contact Info ---
st.markdown("---")
st.markdown("## 📞 Contact Us")

st.markdown("""
📧 Email: papreddy@gmail.com
📞 Phone: +91 9632082737  
🌐 Website: [srinivasuniversity.edu.in](https://srinivasuniversity.edu.in/)
""")

# --- Footer ---
st.markdown("---")
st.markdown("<center>© 2025 Srinivas University • Tree Plantation Initiative</center>", unsafe_allow_html=True)
