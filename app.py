import streamlit as st
api_key = st.secrets["gemini_api_key"]
import os
from dotenv import load_dotenv
from google import genai

# 1. Load the secret API key from the .env file
load_dotenv()

# 2. Configure the look and feel of the web page
st.set_page_config(page_title="AI Travel Agent", page_icon="✈️", layout="centered")

# 3. Create a sidebar to collect user inputs
st.sidebar.header("Plan Your Trip")
destination = st.sidebar.text_input("Destination (e.g., Tokyo, Japan)")
days = st.sidebar.slider("Number of Days", 1, 14, 3)
budget = st.sidebar.selectbox("Budget", ["Budget-friendly", "Standard", "Luxury"])
interests = st.sidebar.text_area("Interests (e.g., street food, history, hiking)")

# 4. Main page title and description
st.title("✈️ Tvisha Smart AI Travel Agent")
st.write("Welcome! Tell me where you want to go, and I'll generate a custom itinerary for you.")

# 5. What happens when the user clicks the button?
if st.button("Generate Itinerary"):
    # Check if they actually typed a destination
    if not destination:
        st.warning("Please enter a destination in the sidebar to get started!")
    else:
        # Show a loading spinner while the AI thinks
        with st.spinner("Your AI agent is crafting the perfect trip..."):
            try:
                # Initialize the Gemini client (it automatically finds the API key)
                client = genai.Client(api_key="AIzaSyD6NdcH1WHe5tO13lcgTVL55scoUZc8E4k")
                
                # Construct the specific instructions for the AI
                prompt = f"""
                You are an expert travel agent. Create a highly detailed, {days}-day itinerary for {destination}.
                Budget level: {budget}
                Specific interests: {interests}
                
                Please format the response clearly with day-by-day headings, suggested times, and brief descriptions of why these activities fit the user's interests.
                """
                
                # Send the instructions to the Gemini 2.5 Flash model
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt,
                )
                
                # Display the AI's response on the screen
                st.success("Itinerary Generated!")
                st.markdown(response.text)
                
            except Exception as e:
                # If something breaks (like a missing API key or lost internet), show an error
                st.error(f"An error occurred: {e}")
                st.info("Did you remember to put your GEMINI_API_KEY in the .env file?")
