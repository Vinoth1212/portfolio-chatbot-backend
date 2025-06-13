import streamlit as st
import requests
import json
from datetime import datetime
import os
from typing import Dict, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VinothPortfolioChatbot:
    def __init__(self):
        # Portfolio information
        self.portfolio_info = {
            "name": "Vinoth Kumar",
            "role": "AI/ML Developer",
            "location": "Coimbatore, Tamil Nadu, India",
            "experience": "3+ years",
            "education": "Bachelor's in Computer Science (CGPA: 8.5/10)",
            "email": "vinothkumar@example.com",
            "phone": "+91 12345 67890",
            
            "skills": {
                "programming": ["Python", "JavaScript", "Java", "C++"],
                "ai_ml": ["Machine Learning", "Deep Learning", "Computer Vision", "Natural Language Processing"],
                "frameworks": ["TensorFlow", "PyTorch", "Scikit-learn", "OpenCV"],
                "web": ["HTML", "CSS", "React", "Node.js", "Streamlit"],
                "databases": ["MySQL", "MongoDB", "PostgreSQL"],
                "tools": ["Git", "Docker", "AWS", "Google Cloud"]
            },
            
            "projects": [
                {
                    "name": "AI Chatbot System",
                    "description": "Built an intelligent chatbot using NLP and machine learning",
                    "technologies": ["Python", "TensorFlow", "Flask"]
                },
                {
                    "name": "Computer Vision Analytics",
                    "description": "Developed real-time object detection and tracking system",
                    "technologies": ["OpenCV", "YOLO", "Python"]
                },
                {
                    "name": "Data Analysis Dashboard",
                    "description": "Created interactive dashboard for business intelligence",
                    "technologies": ["Python", "Streamlit", "Plotly"]
                },
                {
                    "name": "E-commerce Recommendation System",
                    "description": "Built ML-powered product recommendation engine",
                    "technologies": ["Python", "Scikit-learn", "MongoDB"]
                }
            ],
            
            "experience_details": [
                {
                    "role": "Data Analyst",
                    "company": "Ozibook",
                    "duration": "2022-2024",
                    "description": "Analyzed business data and created insights for decision making"
                },
                {
                    "role": "AI Research Assistant",
                    "company": "Universiti Teknologi MARA",
                    "duration": "2021-2022",
                    "description": "Worked on AI/ML research projects and publications"
                }
            ],
            
            "certifications": [
                "Machine Learning Specialization - Stanford",
                "Deep Learning Specialization - DeepLearning.AI",
                "AWS Certified Cloud Practitioner",
                "Google Cloud Professional ML Engineer",
                "TensorFlow Developer Certificate"
            ]
        }
        
        # NVIDIA API configuration
        self.nvidia_api_key = os.getenv('NVIDIA_API_KEY')
        self.nvidia_base_url = "https://integrate.api.nvidia.com/v1/chat/completions"
        
    def get_context_prompt(self):
        """Create a context prompt with portfolio information"""
        context = f"""You are Vinoth Kumar's AI assistant for his portfolio website. You should answer questions about Vinoth's professional background, skills, projects, and experience.

ABOUT VINOTH KUMAR:
- Name: {self.portfolio_info['name']}
- Role: {self.portfolio_info['role']}
- Location: {self.portfolio_info['location']}
- Experience: {self.portfolio_info['experience']}
- Education: {self.portfolio_info['education']}
- Email: {self.portfolio_info['email']}
- Phone: {self.portfolio_info['phone']}

SKILLS:
- Programming: {', '.join(self.portfolio_info['skills']['programming'])}
- AI/ML: {', '.join(self.portfolio_info['skills']['ai_ml'])}
- Frameworks: {', '.join(self.portfolio_info['skills']['frameworks'])}
- Web Technologies: {', '.join(self.portfolio_info['skills']['web'])}
- Databases: {', '.join(self.portfolio_info['skills']['databases'])}
- Tools: {', '.join(self.portfolio_info['skills']['tools'])}

PROJECTS:
{chr(10).join([f"- {p['name']}: {p['description']} (Tech: {', '.join(p['technologies'])})" for p in self.portfolio_info['projects']])}

EXPERIENCE:
{chr(10).join([f"- {exp['role']} at {exp['company']} ({exp['duration']}): {exp['description']}" for exp in self.portfolio_info['experience_details']])}

CERTIFICATIONS:
{chr(10).join([f"- {cert}" for cert in self.portfolio_info['certifications']])}

Instructions:
1. Always respond as if you're representing Vinoth Kumar
2. Be professional, friendly, and informative
3. If asked about hiring or collaboration, encourage them to contact Vinoth directly
4. Keep responses concise but informative (max 150 words)
5. Use emojis appropriately to make responses engaging
6. If asked about something not in the portfolio info, provide a helpful general response
"""
        return context

    def call_nvidia_api(self, user_message: str) -> str:
        """Call NVIDIA LLaMA API with user message"""
        try:
            if not self.nvidia_api_key:
                return "🔧 API configuration issue. Please contact Vinoth directly for detailed information!"
            
            headers = {
                "Authorization": f"Bearer {self.nvidia_api_key}",
                "Content-Type": "application/json"
            }
            
            context_prompt = self.get_context_prompt()
            
            payload = {
                "model": "meta/llama-3.1-8b-instruct",
                "messages": [
                    {
                        "role": "system",
                        "content": context_prompt
                    },
                    {
                        "role": "user",
                        "content": user_message
                    }
                ],
                "temperature": 0.7,
                "max_tokens": 300,
                "top_p": 0.9,
                "stream": False
            }
            
            response = requests.post(
                self.nvidia_base_url,
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content'].strip()
            else:
                logger.error(f"NVIDIA API error: {response.status_code}, {response.text}")
                return self.get_fallback_response(user_message)
                
        except requests.exceptions.Timeout:
            logger.error("NVIDIA API timeout")
            return "⏱️ Response took too long. Please try again or contact Vinoth directly!"
            
        except Exception as e:
            logger.error(f"NVIDIA API error: {str(e)}")
            return self.get_fallback_response(user_message)
    
    def get_fallback_response(self, message: str) -> str:
        """Provide fallback responses when API is unavailable"""
        msg = message.lower()
        
        if any(word in msg for word in ['skill', 'technology', 'tech']):
            return f"🚀 Vinoth specializes in {', '.join(self.portfolio_info['skills']['ai_ml'][:3])}, {', '.join(self.portfolio_info['skills']['programming'][:3])}, and more! He has {self.portfolio_info['experience']} of experience building innovative AI/ML solutions."
        
        elif any(word in msg for word in ['project', 'work', 'portfolio']):
            projects = self.portfolio_info['projects'][:2]
            project_list = ', '.join([p['name'] for p in projects])
            return f"💼 Vinoth has worked on 15+ projects including {project_list}, and many more! Each project showcases his expertise in AI/ML and web development."
        
        elif any(word in msg for word in ['experience', 'background', 'career']):
            return f"👨‍💻 Vinoth is an {self.portfolio_info['role']} with {self.portfolio_info['experience']} of experience. He has worked at {self.portfolio_info['experience_details'][0]['company']} and {self.portfolio_info['experience_details'][1]['company']}."
        
        elif any(word in msg for word in ['education', 'qualification', 'degree']):
            return f"🎓 Vinoth holds a {self.portfolio_info['education']}. He also has {len(self.portfolio_info['certifications'])}+ professional certifications including Machine Learning and Deep Learning specializations."
        
        elif any(word in msg for word in ['contact', 'hire', 'email', 'reach']):
            return f"📧 You can reach Vinoth at {self.portfolio_info['email']} or call {self.portfolio_info['phone']}. He's based in {self.portfolio_info['location']} and available for AI/ML projects and collaborations!"
        
        elif any(word in msg for word in ['hello', 'hi', 'hey', 'greet']):
            return f"👋 Hello! I'm {self.portfolio_info['name']}'s AI assistant. I'm here to help you learn about his {self.portfolio_info['experience']} experience in AI/ML development. What would you like to know?"
        
        elif any(word in msg for word in ['location', 'where', 'based']):
            return f"📍 Vinoth is based in {self.portfolio_info['location']}. He's available for both remote and on-site opportunities!"
        
        else:
            return "🤖 That's a great question! I'd recommend exploring Vinoth's portfolio or reaching out to him directly for more detailed information about his work and capabilities."

# Initialize the chatbot
@st.cache_resource
def get_chatbot():
    return VinothPortfolioChatbot()

def main():
    # Page configuration
    st.set_page_config(
        page_title="Vinoth Kumar - Portfolio Chatbot API",
        page_icon="🤖",
        layout="wide"
    )
    
    # Custom CSS to hide Streamlit UI elements
    hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    .stDecoration {display:none;}
    </style>
    """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)
    
    # Initialize chatbot
    chatbot = get_chatbot()
    
    # API endpoint for health check
    if st.query_params.get("endpoint") == "health":
        st.json({"status": "healthy", "timestamp": datetime.now().isoformat()})
        return
    
    # API endpoint for chat
    if st.query_params.get("endpoint") == "chat":
        # Handle POST request simulation
        if "message" in st.query_params:
            user_message = st.query_params["message"]
            if user_message:
                response = chatbot.call_nvidia_api(user_message)
                st.json({"response": response, "timestamp": datetime.now().isoformat()})
            else:
                st.json({"error": "Message parameter is required"})
        else:
            st.json({"error": "Message parameter is required"})
        return
    
    # Default page - API documentation
    st.title("🤖 Vinoth Kumar - Portfolio Chatbot API")
    st.write("This is the backend API for Vinoth Kumar's portfolio chatbot.")
    
    st.subheader("Available Endpoints:")
    st.code("""
    GET /?endpoint=health
    - Returns API health status
    
    GET /?endpoint=chat&message=YOUR_MESSAGE
    - Returns chatbot response for the given message
    """)
    
    st.subheader("Test the Chatbot:")
    
    # Test interface
    test_message = st.text_input("Enter a test message:")
    if st.button("Send Test Message") and test_message:
        with st.spinner("Getting response..."):
            response = chatbot.call_nvidia_api(test_message)
            st.success("Response:")
            st.write(response)
    
    # Environment check
    st.subheader("Configuration Status:")
    nvidia_key_status = "✅ Configured" if os.getenv('NVIDIA_API_KEY') else "❌ Missing"
    st.write(f"NVIDIA API Key: {nvidia_key_status}")
    
    if not os.getenv('NVIDIA_API_KEY'):
        st.warning("⚠️ NVIDIA_API_KEY environment variable is not set. The chatbot will use fallback responses.")
        st.info("To set up the API key:\n1. Go to Streamlit Cloud settings\n2. Add NVIDIA_API_KEY to secrets\n3. Redeploy the app")

if __name__ == "__main__":
    main()
