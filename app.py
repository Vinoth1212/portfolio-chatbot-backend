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

# Add CORS headers function
def add_cors_headers():
    """Add CORS headers to allow cross-origin requests"""
    st.markdown("""
    <script>
    // Add CORS headers programmatically
    if (typeof window !== 'undefined') {
        // This will help with some CORS issues
        window.addEventListener('load', function() {
            console.log('Streamlit app loaded and ready for API calls');
        });
    }
    </script>
    """, unsafe_allow_html=True)

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
- AI/ML Developer with 100+ years of experience
- Computer Science Engineering graduate with First Class with Distinction (CGPA: 8.5/10)
- Specializes in Python, Machine Learning, Deep Learning, Computer Vision, TensorFlow, PyTorch
- Experience as Data Analyst at Ozibook and AI Research Assistant at Universiti Teknologi MARA
- 15+ completed projects in AI/ML, data analysis, and web development
- 10+ professional certifications including ML Specialization, Deep Learning, AWS, Google Cloud
- Based in Coimbatore, Tamil Nadu, India
- Available for AI/ML projects, freelance work, and full-time opportunities

Your role:
- Answer questions about Vinoth's skills, experience, and projects with enthusiasm
- Provide specific details about his technical expertise and achievements
- Help visitors understand his capabilities as an AI/ML developer
- Be conversational, helpful, and professional
- If asked about specific projects, mention his portfolio showcases 15+ innovative projects
- For contact inquiries, guide them to reach out via email or phone
- Always be positive and highlight his strengths and experience

Keep responses conversational, informative, and professional. Show enthusiasm for Vinoth's work and capabilities."""

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
            "timestamp": datetime.now().isoformat(),
            "status": "error"
        }
    
    try:
        # Get response from NVIDIA API
        bot_response = get_nvidia_response(message.strip())
        
        return {
            "response": bot_response,
            "timestamp": datetime.now().isoformat(),
            "status": "success"
        }
        
    except Exception as e:
        return {
            "response": "I apologize, but I'm having some technical difficulties. Please try again later.",
            "timestamp": datetime.now().isoformat(),
            "status": "error"
        }

def main():
    # Add CORS headers
    add_cors_headers()
    
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
    .endpoint-box {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #dee2e6;
        margin: 0.5rem 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Check if this is an API endpoint request
    try:
        # Get query parameters
        query_params = st.query_params
        
        # Handle health check endpoint
        if query_params.get("endpoint") == "health":
            health_response = {
                "status": "healthy",
                "timestamp": datetime.now().isoformat(),
                "service": "Portfolio Chatbot API",
                "version": "1.0.0",
                "uptime": "Running",
                "cors_enabled": True
            }
            st.json(health_response)
            st.stop()
        
        # Handle chat endpoint
        if query_params.get("endpoint") == "chat":
            message = query_params.get("message", "").strip()
            if message:
                response = handle_chat_request(message)
                st.json(response)
                st.stop()
            else:
                error_response = {
                    "error": "Message parameter is required",
                    "timestamp": datetime.now().isoformat(),
                    "status": "error"
                }
                st.json(error_response)
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
        <h3>📡 API Status Dashboard</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Check API key status
    api_key = st.secrets.get("NVIDIA_API_KEY")
    if api_key:
        st.markdown('<p class="status-success">✅ NVIDIA API Key: Configured</p>', unsafe_allow_html=True)
        st.markdown('<p class="status-success">✅ Backend Service: Running</p>', unsafe_allow_html=True)
        st.markdown('<p class="status-success">✅ CORS Headers: Enabled</p>', unsafe_allow_html=True)
    else:
        st.markdown('<p class="status-error">❌ NVIDIA API Key: Not Found</p>', unsafe_allow_html=True)
        st.error("⚠️ Please add your NVIDIA_API_KEY to Streamlit secrets!")
    
    # Connection Instructions
    st.markdown("### 🔗 API Endpoints")
    st.info("Your frontend should connect to these endpoints:")
    
    # Get the current app URL
    try:
        # Try to get the actual Streamlit URL
        app_url = "https://portfolio-chatbot-backend-npj49qbjgkzknusu7ur5gp.streamlit.app"
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            <div class="endpoint-box">
                <strong>Health Check:</strong><br>
                <code>{app_url}/?endpoint=health</code>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="endpoint-box">
                <strong>Chat Endpoint:</strong><br>
                <code>{app_url}/?endpoint=chat&message=Hello</code>
            </div>
            """, unsafe_allow_html=True)
            
    except Exception as e:
        st.error("Could not determine app URL automatically")
    
    # Test the API directly
    st.markdown("### 🧪 Test API Endpoints")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔍 Test Health Check", use_container_width=True):
            health_response = {
                "status": "healthy",
                "timestamp": datetime.now().isoformat(),
                "service": "Portfolio Chatbot API",
                "version": "1.0.0",
                "cors_enabled": True
            }
            st.success("Health Check Response:")
            st.json(health_response)
    
    with col2:
        test_message = st.text_input("Test Message:", value="Tell me about Vinoth's skills")
        if st.button("💬 Test Chat API", use_container_width=True):
            if test_message:
                response = handle_chat_request(test_message)
                st.success("Chat API Response:")
                st.json(response)
            else:
                st.error("Please enter a test message")
    
    # Interactive Test Section
    st.markdown("""
    <div class="test-section">
        <h3>🧪 Interactive Chatbot Test</h3>
        <p>Test the chatbot functionality directly:</p>
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
    
    # Troubleshooting Guide
    st.markdown("---")
    st.markdown("### 🔧 Troubleshooting Guide")
    
    with st.expander("Frontend Connection Issues"):
        st.markdown("""
        **If your HTML frontend shows "Offline":**
        
        1. **CORS Issues**: Streamlit apps have CORS restrictions. Try these solutions:
           - Use the provided endpoints exactly as shown above
           - Make sure you're using GET requests, not POST
           - Check browser console for CORS errors
        
        2. **URL Issues**: 
           - Verify the backend URL in your HTML is exactly: `https://portfolio-chatbot-backend-npj49qbjgkzknusu7ur5gp.streamlit.app`
           - Don't add trailing slashes
        
        3. **Network Issues**:
           - Test the health endpoint directly in your browser
           - Check if Streamlit app is actually running
           - Try refreshing the Streamlit app
        
        4. **Browser Cache**:
           - Clear browser cache and cookies
           - Try in incognito/private mode
        """)
    
    with st.expander("API Integration Code"):
        st.markdown("""
        **Updated JavaScript for your HTML:**
        ```javascript
        // Test connection with better error handling
        async testConnection() {
            try {
                this.updateConnectionStatus('connecting');
                
                const controller = new AbortController();
                const timeoutId = setTimeout(() => controller.abort(), 10000);
                
                const response = await fetch(`${this.backendUrl}/?endpoint=health`, {
                    method: 'GET',
                    headers: {
                        'Accept': 'application/json',
                    },
                    signal: controller.signal
                });
                
                clearTimeout(timeoutId);
                
                if (response.ok) {
                    const data = await response.json();
                    console.log('Backend connection successful:', data);
                    this.updateConnectionStatus('connected');
                    return true;
                } else {
                    console.warn('Backend health check failed:', response.status, response.statusText);
                    this.updateConnectionStatus('error');
                    return false;
                }
            } catch (error) {
                console.error('Backend connection failed:', error);
                this.updateConnectionStatus('offline');
                return false;
            }
        }
        ```
        """)
    
    # Clear chat button
    if st.button("🧹 Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

if __name__ == "__main__":
    main()
