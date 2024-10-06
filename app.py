import openai
import os
import json
import streamlit as st

# OpenAI API key setup (replace this with your actual API key)
openai.api_key = os.getenv("OPENAI_API_KEY")

# Set up the knowledge base fallback (as in your Flask example)
FALLBACK_KNOWLEDGE_BASE = [
    {
        "name": "Smile Center Dental Clinic",
        "location": {
            "address": "Ground Floor, Al Babar Plaza, F-8 Markaz, Islamabad",
            "phone": "051-8351111",
            "mobile": "0300-0400041"
        },
        "hours": {
            "open_time": "9:00 AM",
            "close_time": "5:00 PM"
        }
    },
    {
        "dentists": {
            "orthodontist": {
                "name": "Dr. Saeed Mustafa",
                "specialization": "Orthodontist"
            },
            "coo": {
                "name": "Dr. Mahinu",
                "role": "COO"
            },
            "general_dentists": [
                {
                    "name": "Dr. Noor Bajwa",
                    "specialization": "General Dentist"
                },
                {
                    "name": "Dr. Salwan",
                    "specialization": "General Dentist, Associate Professor Oral Biology"
                }
            ],
            "pediatric_dentist": {
                "name": "Dr. Emma",
                "specialization": "Pediatric Dentist"
            },
            "oral_surgery_consultant": {
                "name": "Dr. Harris Saeed",
                "specialization": "Oral Surgery Consultant"
            }
        }
    },
    {
        "services": {
            "aesthetics": {
                "description": "Aesthetics experts available"
            }
        }
    }
]

# Function to generate a response using OpenAI
def get_ai_response(user_input: str) -> str:
    prompt = (
        f"Given the following knowledge base:\n\n{json.dumps(FALLBACK_KNOWLEDGE_BASE, indent=2)}\n\n"
        f"User question: {user_input}\n\n"
        "Please provide a helpful response based on the knowledge base. If the information is not available, "
        "politely suggest connecting to a human representative."
    )
    
    try:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            max_tokens=150
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"Error: {e}"

# Streamlit UI setup
st.title("AI Chatbot for Dental Clinic")
st.write("Ask any question related to our services or general inquiries!")

# Initialize session state to store chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Chat input form
user_input = st.text_input("You:", key="input")

# When user submits a query
if user_input:
    st.session_state["messages"].append({"role": "user", "content": user_input})
    
    # Get AI response
    ai_reply = get_ai_response(user_input)
    st.session_state["messages"].append({"role": "assistant", "content": ai_reply})
    
    # Clear input after submission
    st.experimental_rerun()

# Display the conversation history
for message in st.session_state["messages"]:
    if message["role"] == "user":
        st.write(f"**You:** {message['content']}")
    else:
        st.write(f"**AI:** {message['content']}")

# Clear chat button
if st.button("Clear Chat"):
    st.session_state["messages"] = []
    st.experimental_rerun()
