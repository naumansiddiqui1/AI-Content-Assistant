import streamlit as st
from groq import Groq

# 1. Setup the Page
st.set_page_config(page_title="AI Content Assistant", page_icon="✍️", layout="centered")
st.title("✍️ AI Content Assistant")
st.write("Generate high-quality posts for your social media using AI.")

# 2. Securely Load API Key
api_key = st.secrets.get("GROQ_API_KEY") 

if not api_key:
    st.error("GROQ_API_KEY is missing! Please add it to your Streamlit secrets.")
    st.stop()

# Initialize Groq client
client = Groq(api_key=api_key)

# 3. User Interface Controls
col1, col2 = st.columns(2)

with col1:
    platform = st.selectbox("Platform", ["LinkedIn", "Twitter/X", "Instagram", "Facebook"])
    content_type = st.selectbox("Content Type", ["Short Post", "Detailed Thread/Article", "Promotional", "Educational"])

with col2:
    audience = st.selectbox("Target Audience", ["Professionals", "Beginners", "Students", "General Public"])
    tone = st.selectbox("Tone", ["Professional", "Casual & Friendly", "Humorous", "Inspirational"])

topic = st.text_area("What is the topic of your post?", placeholder="e.g., The benefits of learning Artificial Intelligence...")

# 4. Generate Button & AI Logic
if st.button("Generate Content 🚀"):
    if not topic:
        st.warning("Please enter a topic first.")
    else:
        with st.spinner("Generating your post..."):
            # Construct the instructions for the AI
            prompt = f"""
            You are an expert social media manager. Create a {content_type} for {platform}.
            Topic: {topic}
            Target Audience: {audience}
            Tone: {tone}
            
            Please provide:
            1. The complete post text with an engaging hook.
            2. 5-10 highly relevant hashtags at the end.
            """
            
            try:
                # Send the request to Groq
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "You are a helpful AI content creation assistant."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                )
                
                # Display the result
                generated_text = response.choices[0].message.content
                st.success("Post generated successfully!")
                st.markdown(generated_text)
                
            except Exception as e:
                st.error(f"An error occurred: {e}")