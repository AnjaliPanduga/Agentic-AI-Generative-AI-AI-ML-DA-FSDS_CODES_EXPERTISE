import streamlit as st
import pandas as pd
from datetime import datetime
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import inch

# Set page configuration
st.set_page_config(
    page_title="SkyBooker - HYD to GOI",
    page_icon="✈️",
    layout="centered"
)

# --- Data Setup ---
def load_data():
    # Outbound: HYD -> GOI
    outbound_data = {
        "Airline": ["IndiGo", "SpiceJet", "Air India", "Vistara", "Akasa Air"],
        "Flight No": ["6E-532", "SG-102", "AI-889", "UK-992", "QP-114"],
        "Departure": ["06:00 AM", "09:30 AM", "01:15 PM", "05:45 PM", "09:00 PM"],
        "Duration": ["1h 30m", "1h 45m", "1h 35m", "1h 40m", "1h 25m"],
        "Price": [4500, 4200, 5100, 6500, 3900]
    }
    
    # Return: GOI -> HYD
    return_data = {
        "Airline": ["IndiGo", "SpiceJet", "Air India", "Vistara", "Akasa Air"],
        "Flight No": ["6E-539", "SG-108", "AI-892", "UK-995", "QP-118"],
        "Departure": ["08:00 AM", "11:45 AM", "03:30 PM", "07:15 PM", "10:30 PM"],
        "Duration": ["1h 30m", "1h 40m", "1h 35m", "1h 45m", "1h 25m"],
        "Price": [4800, 4300, 5200, 6700, 4100]
    }
    
    df_out = pd.DataFrame(outbound_data)
    df_ret = pd.DataFrame(return_data)
    return df_out, df_ret

df_outbound, df_return = load_data()

# --- Helper Functions ---
def format_option(row):
    return f"{row['Airline']} ({row['Flight No']}) | 🕒 {row['Departure']} | ⏳ {row['Duration']} | ₹{row['Price']}"

def create_pdf(details):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    
    # Header
    c.setFont("Helvetica-Bold", 24)
    c.setFillColor(colors.darkblue)
    c.drawString(50, height - 50, "SkyBooker Ticket Confirmation")
    
    c.setLineWidth(1)
    c.line(50, height - 60, width - 50, height - 60)
    
    # Booking Info
    c.setFont("Helvetica", 12)
    c.setFillColor(colors.black)
    
    y = height - 100
    line_height = 25
    
    c.drawString(50, y, f"Booking Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    y -= line_height * 2
    
    # Outbound
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, "Outbound Flight (Hyderabad -> Goa)")
    y -= line_height
    c.setFont("Helvetica", 12)
    c.drawString(70, y, f"Date: {details['dep_date']}")
    y -= line_height
    c.drawString(70, y, f"Airline: {details['out_airline']} ({details['out_flight']})")
    y -= line_height
    c.drawString(70, y, f"Time: {details['out_time']}")
    y -= line_height
    c.drawString(70, y, f"Price: Rs. {details['out_price']}")
    
    y -= line_height * 2
    
    # Return
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, "Return Flight (Goa -> Hyderabad)")
    y -= line_height
    c.setFont("Helvetica", 12)
    c.drawString(70, y, f"Date: {details['ret_date']}")
    y -= line_height
    c.drawString(70, y, f"Airline: {details['ret_airline']} ({details['ret_flight']})")
    y -= line_height
    c.drawString(70, y, f"Time: {details['ret_time']}")
    y -= line_height
    c.drawString(70, y, f"Price: Rs. {details['ret_price']}")
    
    y -= line_height * 2
    
    # Total
    c.setLineWidth(1)
    c.line(50, y + 10, width - 50, y + 10)
    c.setFont("Helvetica-Bold", 18)
    c.drawString(50, y - 10, f"Total Amount Paid: Rs. {details['total_price']}")
    
    # Footer
    c.setFont("Helvetica-Oblique", 10)
    c.drawString(50, 50, "Thank you for booking with SkyBooker!")
    
    c.save()
    buffer.seek(0)
    return buffer

# --- UI Layout ---
st.title("✈️ SkyBooker: Hyderabad to Goa")
st.markdown("Book your flights easily from **Hyderabad (HYD)** to **Goa (GOI)** and back.")

# Date Selection
st.subheader("📅 Select Dates")
col1, col2 = st.columns(2)
with col1:
    dep_date = st.date_input("Departure Date", min_value=datetime.today())
with col2:
    ret_date = st.date_input("Return Date", min_value=dep_date if dep_date else datetime.today())

st.divider()

# Flight Selection
st.subheader("🛫 Select Outbound Flight (HYD → GOI)")
outbound_options = [format_option(row) for index, row in df_outbound.iterrows()]
selected_outbound_str = st.radio("Choose a flight to Goa:", outbound_options, key="outbound")

st.subheader("🛬 Select Return Flight (GOI → HYD)")
return_options = [format_option(row) for index, row in df_return.iterrows()]
selected_return_str = st.radio("Choose a flight back to Hyderabad:", return_options, key="return")

# --- Calculations ---
selected_outbound_row = df_outbound.iloc[outbound_options.index(selected_outbound_str)]
selected_return_row = df_return.iloc[return_options.index(selected_return_str)]

outbound_price = selected_outbound_row['Price']
return_price = selected_return_row['Price']
total_price = outbound_price + return_price

st.divider()

# --- Booking Section ---
st.subheader("💰 Booking Summary")
st.info(f"**Total Fare:** ₹{total_price}")

if st.button("Book Ticket 🎟️", type="primary"):
    st.success("🎉 Booking Confirmed! Have a safe trip.")
    
    # Prepare details for PDF
    booking_details = {
        "dep_date": dep_date.strftime('%d %b %Y'),
        "ret_date": ret_date.strftime('%d %b %Y'),
        "out_airline": selected_outbound_row['Airline'],
        "out_flight": selected_outbound_row['Flight No'],
        "out_time": selected_outbound_row['Departure'],
        "out_price": outbound_price,
        "ret_airline": selected_return_row['Airline'],
        "ret_flight": selected_return_row['Flight No'],
        "ret_time": selected_return_row['Departure'],
        "ret_price": return_price,
        "total_price": total_price
    }
    
    # Generate PDF
    pdf_file = create_pdf(booking_details)
    
    # Detailed Summary Card
    with st.container():
        st.markdown("### 🧾 Ticket Details")
        
        c1, c2 = st.columns(2)
        
        with c1:
            st.markdown("#### 🛫 Outbound")
            st.write(f"**Date:** {booking_details['dep_date']}")
            st.write(f"**Airline:** {booking_details['out_airline']}")
            st.write(f"**Flight:** {booking_details['out_flight']}")
            st.write(f"**Time:** {booking_details['out_time']}")
            st.write(f"**Price:** ₹{booking_details['out_price']}")
            
        with c2:
            st.markdown("#### 🛬 Return")
            st.write(f"**Date:** {booking_details['ret_date']}")
            st.write(f"**Airline:** {booking_details['ret_airline']}")
            st.write(f"**Flight:** {booking_details['ret_flight']}")
            st.write(f"**Time:** {booking_details['ret_time']}")
            st.write(f"**Price:** ₹{booking_details['ret_price']}")
            
        st.markdown("---")
        st.markdown(f"### **Grand Total: ₹{total_price}**")
        
        # Download Button
        st.download_button(
            label="📄 Download Ticket PDF",
            data=pdf_file,
            file_name="SkyBooker_Ticket.pdf",
            mime="application/pdf"
        )
