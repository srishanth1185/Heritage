import streamlit as st
from PIL import Image
import datetime

# App Configuration
st.set_page_config(
    page_title="Telugu Heritage Collector",
    page_icon="🇮🇳",
    layout="centered"
)

# Initialize session state
if 'contributions' not in st.session_state:
    st.session_state.contributions = []

# Simple "database" (replace with real DB in production)
TELUGU_HERITAGE_DATA = {
    "artifacts": [],
    "stories": [],
    "recipes": []
}

# ======================
# CORE FUNCTIONS
# ======================

def save_artifact(upload, details):
    """Save artifact to our simple database"""
    artifact = {
        "type": "artifact",
        "file": upload.name,
        "title": details.get("title", "Untitled"),
        "description": details.get("description", ""),
        "region": details.get("region", "Unknown"),
        "date": datetime.datetime.now().strftime("%Y-%m-%d"),
        "user": details.get("user", "Anonymous")
    }
    st.session_state.contributions.append(artifact)
    return artifact

def generate_ai_response(query):
    """Simple AI response generator (would connect to LLM in production)"""
    telugu_knowledge = {
        "history": "Telugu civilization dates back to at least 400 BCE with the Andhra Satavahanas. The language has a rich literary tradition spanning over 1000 years.",
        "temples": "Famous Telugu temples include:\n- Tirumala Venkateswara (Tirupati)\n- Srisailam Mallikarjuna\n- Bhadrachalam Sita Ramachandra\n- Lepakshi Veerabhadra",
        "culture": "Telugu culture is known for:\n- Kuchipudi dance\n- Telugu cinema (Tollywood)\n- Ugadi festival\n- Bonalu celebrations\n- Bathukamma floral festival",
        "language": "Telugu is a Dravidian language with 56 unique letters. It's the 3rd most spoken language in India with classical language status.",
        "default": "I'm your Telugu heritage guide. Ask me about:\n- History\n- Temples\n- Festivals\n- Traditional arts\n- Famous personalities"
    }
    
    query = query.lower()
    for key in telugu_knowledge:
        if key in query:
            return telugu_knowledge[key]
    return telugu_knowledge["default"]

# ======================
# PAGE LAYOUT
# ======================

def main():
    st.title("Preserving Telugu Heritage")
    st.markdown("""
    Welcome to our community platform for documenting and celebrating Telugu culture. 
    Contribute artifacts, stories, and recipes, or explore our cultural heritage.
    """)
    
    # Navigation
    tab1, tab2, tab3 = st.tabs(["Contribute", "AI Guide", "Explore"])
    
    with tab1:
        st.header("Share a Piece of Telugu Culture")
        contribution_type = st.radio(
            "What would you like to contribute?",
            ["Cultural Artifact", "Oral Story", "Traditional Recipe"],
            horizontal=True
        )
        
        if contribution_type == "Cultural Artifact":
            with st.form("artifact_form"):
                uploaded_file = st.file_uploader("Upload image of artifact", type=["jpg", "png", "jpeg"])
                title = st.text_input("Title")
                description = st.text_area("Description (significance, materials, etc.)")
                region = st.text_input("Region/Village of origin")
                submitted = st.form_submit_button("Submit")
                
                if submitted and uploaded_file:
                    artifact = save_artifact(
                        uploaded_file,
                        {
                            "title": title,
                            "description": description,
                            "region": region,
                            "user": "User"  # Would replace with actual auth
                        }
                    )
                    st.success(f"Thank you for contributing {artifact['title']}!")
                    st.image(uploaded_file, caption=artifact["title"])
        
        # Similar forms would be added for stories and recipes
    
    with tab2:
        st.header("Telugu Heritage Guide")
        st.caption("Ask me anything about Telugu history, culture, or traditions")
        
        user_query = st.text_input("Your question about Telugu heritage", key="ai_query")
        if user_query:
            response = generate_ai_response(user_query)
            st.markdown(f"**Heritage Guide:**\n\n{response}")
            
            # Example follow-up for temples
            if "temple" in user_query.lower():
                st.button("Show me famous Telugu temples")
                # Would expand with more interactive elements
    
    with tab3:
        st.header("Explore Telugu Heritage")
        
        if st.session_state.contributions:
            st.subheader("Recent Contributions")
            for item in st.session_state.contributions[-3:]:  # Show 3 most recent
                with st.expander(f"{item['title']} from {item['region']}"):
                    st.caption(f"Contributed on {item['date']}")
                    st.write(item["description"])
        else:
            st.info("No contributions yet. Be the first to share!")
        
        # Would add more exploration features here

if __name__ == "__main__":
    main()
