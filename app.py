import streamlit as st
import requests
import json
import os
from datetime import datetime

# Set page configuration
st.set_page_config(
    page_title="Vinoth Kumar - Portfolio Chatbot API",
    page_icon="🤖",
    layout="wide"
)

# Initialize session state for messages
if 'messages' not in st.session_state:
    st.session_state.messages = []

def get_nvidia_response(user_message):
    """
    Get response from NVIDIA API
    """
    try:
        # Get API key from secrets
        api_key = st.secrets.get("NVIDIA_API_KEY")
        if not api_key:
            return "Error: NVIDIA API key not found in secrets. Please add it to your Streamlit app secrets."
        
        # NVIDIA API endpoint
        url = "https://integrate.api.nvidia.com/v1/chat/completions"
        
        # System prompt for the chatbot
        system_prompt = """You are Vinoth Kumar's personal AI assistant for his portfolio website. You are knowledgeable, friendly, and professional.

About Vinoth Kumar:
- Full Stack Developer specializing in React, Node.js, Python, and modern web technologies
- Computer Science Engineering student
- Passionate about creating innovative web applications and solving complex problems
- Experience with databases (MongoDB, MySQL), cloud platforms, and DevOps
- Strong problem-solving skills and attention to detail
- Always eager to learn new technologies and take on challenging projects

Your role:
- Answer questions about Vinoth's skills, experience, and projects
- Provide information about his technical expertise
- Help visitors understand his capabilities as a developer
- Be enthusiastic about his work and achievements
- If asked about specific projects, mention that visitors can check his portfolio for detailed examples
- For contact inquiries, guide them to reach out through the contact form or provided contact details

Keep responses conversational, helpful, and professional. Show enthusiasm for Vinoth's work and capabilities."""

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "meta/llama3-8b-instruct",
            "messages": [
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user", 
                    "content": user_message
                }
            ],
            "temperature": 0.7,
            "top_p": 0.9,
            "max_tokens": 512,
            "stream": False
        }
        
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            response_data = response.json()
            if 'choices' in response_data and len(response_data['choices']) > 0:
                return response_data['choices'][0]['message']['content']
            else:
                return "I apologize, but I'm having trouble generating a response right now. Please try again."
        else:
            return f"I'm experiencing some technical difficulties (Error {response.status_code}). Please try again in a moment."
            
    except requests.exceptions.Timeout:
        return "The request timed out. Please try again."
    except requests.exceptions.RequestException as e:
        return "I'm having trouble connecting right now. Please try again later."
    except Exception as e:
        return "Something went wrong. Please try again."

def handle_chat_request(message):
    """
    Handle incoming chat requests and return response
    """
    if not message or not message.strip():
        return {
            "response": "Please provide a message to get a response.",
            "timestamp": datetime.now().isoformat()
        }
    
    try:
        # Get response from NVIDIA API
        bot_response = get_nvidia_response(message.strip())
        
        return {
            "response": bot_response,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        return {
            "response": "I apologize, but I'm having some technical difficulties. Please try again later.",
            "timestamp": datetime.now().isoformat()
        }

def main():
    # Custom CSS for better styling
    st.markdown("""
    <style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .chat-container {
        max-width: 800px;
        margin: 0 auto;
    }
    .test-section {
        background-color: #f8f9fa;
        padding: 2rem;
        border-radius: 10px;
        margin: 2rem 0;
        border-left: 4px solid #667eea;
    }
    .api-info {
        background-color: #e8f4f8;
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
        border: 1px solid #b8e6f0;
    }
    .status-success {
        color: #28a745;
        font-weight: bold;
    }
    .status-error {
        color: #dc3545;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Check if this is an API endpoint request
    try:
        # Try different methods to get query parameters for compatibility
        query_params = None
        
        # Method 1: Modern Streamlit
        if hasattr(st, 'query_params'):
            try:
                query_params = dict(st.query_params)
            except:
                pass
        
        # Method 2: Experimental query params
        if not query_params:
            try:
                query_params = dict(st.experimental_get_query_params())
            except:
                pass
        
        # Method 3: Check URL manually
        if not query_params:
            query_params = {}
        
        # Handle health check endpoint
        if query_params.get("endpoint") == "health":
            st.json({
                "status": "healthy",
                "timestamp": datetime.now().isoformat(),
                "service": "Portfolio Chatbot API"
            })
            st.stop()
        
        # Handle chat endpoint
        if query_params.get("endpoint") == "chat":
            message = query_params.get("message", "").strip()
            if message:
                response = handle_chat_request(message)
                st.json(response)
                st.stop()
            else:
                st.json({
                    "error": "Message parameter is required",
                    "timestamp": datetime.now().isoformat()
                })
                st.stop()
    
    except Exception as e:
        # If query params handling fails, continue with normal UI
        pass
    
    # Main UI
    st.markdown("""
    <div class="main-header">
        <h1>🤖 Vinoth Kumar - Portfolio Chatbot API</h1>
        <p>AI-powered assistant for portfolio inquiries</p>
    </div>
    """, unsafe_allow_html=True)
    
    # API Status Check
    st.markdown("""
    <div class="api-info">
        <h3>📡 API Status</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Check API key status
    api_key = st.secrets.get("NVIDIA_API_KEY")
    if api_key:
        st.markdown('<p class="status-success">✅ NVIDIA API Key: Configured</p>', unsafe_allow_html=True)
    else:
        st.markdown('<p class="status-error">❌ NVIDIA API Key: Not Found</p>', unsafe_allow_html=True)
        st.error("⚠️ Please add your NVIDIA_API_KEY to Streamlit secrets!")
    
    # API Endpoints
    st.markdown("### 🔗 Available Endpoints")
    base_url = f"https://{st.get_option('browser.serverAddress') or 'localhost'}:{st.get_option('server.port') or 8501}"
    
    col1, col2 = st.columns(2)
    with col1:
        st.code(f"{base_url}/?endpoint=health", language="text")
        st.caption("Health check endpoint")
    
    with col2:
        st.code(f"{base_url}/?endpoint=chat&message=Hello", language="text")
        st.caption("Chat endpoint (GET request)")
    
    # Interactive Test Section
    st.markdown("""
    <div class="test-section">
        <h3>🧪 Test Your Chatbot</h3>
        <p>Try asking questions about Vinoth Kumar's skills, experience, or projects:</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Chat interface
    with st.container():
        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Chat input
        if prompt := st.chat_input("Ask me anything about Vinoth Kumar..."):
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Get bot response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = get_nvidia_response(prompt)
                    st.markdown(response)
                    
                    # Add assistant response to chat history
                    st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Usage Instructions
    st.markdown("---")
    st.markdown("### 📋 How to Use This API")
    
    with st.expander("For Developers"):
        st.markdown("""
        **Frontend Integration Example:**
        ```javascript
        async function sendMessage(message) {
            const response = await fetch(`YOUR_STREAMLIT_URL/?endpoint=chat&message=${encodeURIComponent(message)}`);
            const data = await response.json();
            return data.response;
        }
        ```
        
        **Health Check:**
        ```javascript
        const healthCheck = await fetch('YOUR_STREAMLIT_URL/?endpoint=health');
        const status = await healthCheck.json();
        ```
        """)
    
    # Clear chat button
    if st.button("🧹 Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

if __name__ == "__main__":
    main()
