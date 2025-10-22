# weather_app.py
# Requirements:
# pip install streamlit requests

import streamlit as st
import requests

API_KEY = "5dc78bb007414c1c8e772322252508"  # your WeatherAPI key
BASE_URL = "http://api.weatherapi.com/v1/current.json"

# ---------- Fetch weather data ----------
def fetch_weather(city):
    try:
        url = f"{BASE_URL}?key={API_KEY}&q={city}&aqi=yes"
        resp = requests.get(url, timeout=10)
        data = resp.json()
        if "error" in data:
            return {"error": data["error"]["message"]}
        else:
            return {
                "location": f"{data['location']['name']}, {data['location']['country']}",
                "temp_c": data['current']['temp_c'],
                "condition": data['current']['condition']['text'],
                "humidity": data['current']['humidity'],
                "wind_kph": data['current']['wind_kph'],
                "last_updated": data['current']['last_updated'],
                "icon": data['current']['condition']['icon'],
            }
    except Exception as e:
        return {"error": str(e)}

# ---------- Streamlit UI ----------
st.set_page_config(page_title="🌤 Weather App", page_icon="🌤", layout="centered")

st.markdown(
    """
    <style>
    .main {
        background: linear-gradient(to bottom, #7dd3fc, #60a5fa, #3b82f6, #1e3a8a);
        color: white;
    }
    .stApp {
        background: linear-gradient(to bottom, #7dd3fc, #60a5fa, #3b82f6, #1e3a8a);
    }
    .card {
        background-color: rgba(15, 23, 42, 0.85);
        padding: 2rem;
        border-radius: 1rem;
        text-align: center;
        box-shadow: 0px 4px 20px rgba(0,0,0,0.4);
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown("<h1 style='text-align:center;'>🌤 Weather Lookup</h1>", unsafe_allow_html=True)
st.write("Enter a city name to see the current weather information.")

city = st.text_input("City name", value="Faisalabad")

if st.button("Search"):
    with st.spinner("Fetching weather data..."):
        result = fetch_weather(city)

    if "error" in result:
        st.error(f"⚠️ {result['error']}")
    else:
        # Weather display card
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown(f"### 📍 {result['location']}")
        st.image(f"https:{result['icon']}", width=80)
        st.markdown(f"## 🌡️ {result['temp_c']} °C")
        st.markdown(f"**Condition:** {result['condition']}")
        st.markdown(f"**💧 Humidity:** {result['humidity']}%")
        st.markdown(f"**🌬️ Wind Speed:** {result['wind_kph']} kph")
        st.markdown(f"**🕒 Last Updated:** {result['last_updated']}")
        st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown(
    "<p style='text-align:center; color:#c7d2fe;'>Developed with ❤️ using Streamlit</p>",
    unsafe_allow_html=True,
)
