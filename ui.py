import streamlit as st
import ollama
from datetime import datetime
import json
import random

# ============================================================
# PAGE CONFIGURATION & INITIALIZATION
# ============================================================

st.set_page_config(
    page_title="ULTRON Interface",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "theme" not in st.session_state:
    st.session_state.theme = "Dark"
if "model" not in st.session_state:
    st.session_state.model = "llama3.2"
if "attachments" not in st.session_state:
    st.session_state.attachments = []
if "demo_mode" not in st.session_state:
    st.session_state.demo_mode = False

# ============================================================
# CSS STYLING
# ============================================================

def apply_theme(theme_choice):
    """Apply theme styling dynamically"""
    if theme_choice == "Light":
        light_css = """
        <style>
        :root {
            --bg-color: #ffffff;
            --text-color: #111111;
            --input-bg: #f5f5f5;
            --border-color: #dddddd;
            --accent-color: #0066cc;
        }
        .stApp {
            background-color: var(--bg-color);
            color: var(--text-color);
        }
        .stApp h1, .stApp h2, .stApp h3, .stApp h4 {
            color: var(--text-color);
        }
        .stApp input, .stApp textarea, [data-baseweb="select"] {
            background-color: var(--input-bg) !important;
            color: var(--text-color) !important;
            border-color: var(--border-color) !important;
        }
        .stMarkdownContainer, .stCaption {
            color: var(--text-color);
        }
        .chat-message-user {
            background-color: #e3f2fd;
            border-left: 4px solid #0066cc;
            padding: 12px;
            border-radius: 4px;
            margin: 8px 0;
        }
        .chat-message-assistant {
            background-color: #f5f5f5;
            border-left: 4px solid #666666;
            padding: 12px;
            border-radius: 4px;
            margin: 8px 0;
        }
        </style>
        """
    else:  # Dark theme
        light_css = """
        <style>
        :root {
            --bg-color: #0b0b0b;
            --text-color: #ffffff;
            --input-bg: #1a1a1a;
            --border-color: #333333;
            --accent-color: #00d4ff;
        }
        .stApp {
            background-color: var(--bg-color);
            color: var(--text-color);
        }
        .stApp h1, .stApp h2, .stApp h3, .stApp h4 {
            color: var(--text-color);
        }
        .stApp input, .stApp textarea, [data-baseweb="select"] {
            background-color: var(--input-bg) !important;
            color: var(--text-color) !important;
            border-color: var(--border-color) !important;
        }
        .stMarkdownContainer, .stCaption {
            color: var(--text-color);
        }
        .chat-message-user {
            background-color: #1a3a52;
            border-left: 4px solid #00d4ff;
            padding: 12px;
            border-radius: 4px;
            margin: 8px 0;
        }
        .chat-message-assistant {
            background-color: #1a1a1a;
            border-left: 4px solid #00d4ff;
            padding: 12px;
            border-radius: 4px;
            margin: 8px 0;
        }
        </style>
        """
    st.markdown(light_css, unsafe_allow_html=True)

# ============================================================
# SIDEBAR CONFIGURATION
# ============================================================

with st.sidebar:
    st.title("⚙️ ULTRON CONTROL PANEL")
    
    st.divider()
    
    # Model Selection
    st.subheader("🔧 Model Configuration")
    
    # Demo Mode Toggle
    st.session_state.demo_mode = st.checkbox("🎭 Demo Mode (No Ollama)", value=st.session_state.demo_mode)
    
    if st.session_state.demo_mode:
        st.session_state.model = "ULTRON-DEMO"
        st.info("✓ Running in Demo Mode - Mock responses enabled")
    else:
        try:
            available_models = ollama.list()["models"]
            model_names = [model["name"] for model in available_models]
            
            if model_names:
                st.session_state.model = st.selectbox(
                    "Select AI Model:",
                    options=model_names,
                    index=0
                )
            else:
                st.session_state.model = st.text_input(
                    "Enter model name:",
                    value="llama3.2"
                )
        except Exception as e:
            st.session_state.model = st.text_input(
                "Enter model name:",
                value="llama3.2",
                help="Ollama not detected. Enter model name manually or enable Demo Mode."
            )
    
    # Temperature & Response Length
    temperature = st.slider(
        "Temperature (Creativity):",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        step=0.1
    )
    
    max_tokens = st.number_input(
        "Max Response Length:",
        min_value=100,
        max_value=4000,
        value=1000
    )
    
    st.divider()
    
    # Theme Selection
    st.subheader("🎨 Appearance")
    st.session_state.theme = st.radio(
        "Theme:",
        options=["Light", "Dark"],
        index=1 if st.session_state.theme == "Dark" else 0
    )
    
    st.divider()
    
    # Chat Management
    st.subheader("💾 Chat Management")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🗑️ Clear History", use_container_width=True):
            st.session_state.messages = []
            st.success("Chat history cleared!")
            st.rerun()
    
    with col2:
        if st.button("💾 Export Chat", use_container_width=True):
            if st.session_state.messages:
                chat_json = json.dumps(st.session_state.messages, indent=2)
                st.download_button(
                    label="Download JSON",
                    data=chat_json,
                    file_name=f"ultron_chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
            else:
                st.info("No messages to export")
    
    st.divider()
    
    # System Status
    st.subheader("📊 System Status")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Messages", len(st.session_state.messages))
    with col2:
        st.metric("Model", st.session_state.model[:15] + "..." if len(st.session_state.model) > 15 else st.session_state.model)

# ============================================================
# MAIN APPLICATION
# ============================================================

apply_theme(st.session_state.theme)

# Header
st.title("🤖 ULTRON")
st.markdown("### Supreme Intelligence. Absolute Control.")
st.markdown("---")

# About Section
with st.expander("ℹ️ About ULTRON", expanded=False):
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
        **ULTRON** is an advanced AI assistant designed to analyze, respond, 
        and execute your commands with precision and authority.
        
        - **Status:** Online ✓
        - **Neural Network:** Active ✓
        - **Security:** Enabled ✓
        """)
    with col2:
        st.info("**Powered by Ollama**\nLocal AI Processing")

st.divider()

# Main Chat Interface
st.markdown("## 🎙️ COMMAND TERMINAL")

# Input Section
col1, col2 = st.columns([4, 1])

with col1:
    user_input = st.text_input(
        "Enter your command:",
        placeholder="What is your command, Operator?"
    )

with col2:
    execute_button = st.button("⚡ Execute", use_container_width=True)

st.markdown("### 📎 Attach Files & Media to Command")

# Media attachment tabs
attach_tab1, attach_tab2, attach_tab3, attach_tab4 = st.tabs(["📄 File", "📷 Photo", "📹 Camera", "🎤 Audio"])

file_context = ""
attached_media = ""

# Tab 1: File Upload
with attach_tab1:
    uploaded_file = st.file_uploader(
        "Upload file:",
        type=["txt", "pdf", "docx"],
        key="command_file"
    )
    if uploaded_file is not None:
        if uploaded_file.type == "text/plain":
            file_context = uploaded_file.read().decode("utf-8")
            st.success(f"✓ File attached: {uploaded_file.name}")
        else:
            file_context = f"[File: {uploaded_file.name}]"
            st.success(f"✓ File attached: {uploaded_file.name}")

# Tab 2: Photo Selection
with attach_tab2:
    photo_file = st.file_uploader(
        "Select a photo:",
        type=["jpg", "jpeg", "png", "gif"],
        key="command_photo"
    )
    if photo_file is not None:
        st.image(photo_file, caption="Selected Photo", use_column_width=True)
        attached_media = f"[Photo: {photo_file.name}]"
        st.success(f"✓ Photo attached: {photo_file.name}")

# Tab 3: Camera Capture
with attach_tab3:
    camera_photo = st.camera_input("Capture from camera", key="command_camera")
    if camera_photo is not None:
        st.image(camera_photo, caption="Captured Photo", use_column_width=True)
        attached_media = "[Photo: Camera Capture]"
        st.success("✓ Camera photo attached")

# Tab 4: Microphone/Audio
with attach_tab4:
    st.info("🎤 Record audio using your microphone")
    audio_file = st.file_uploader(
        "Upload audio file:",
        type=["mp3", "wav", "ogg", "m4a"],
        key="command_audio"
    )
    if audio_file is not None:
        st.audio(audio_file, format="audio/mp3")
        attached_media = f"[Audio: {audio_file.name}]"
        st.success(f"✓ Audio attached: {audio_file.name}")
    
    st.markdown("**Note:** Record audio using your device and upload it here")

# Display attachment summary
st.markdown("---")
col_attach_status, col_attach_clear = st.columns([3, 1])

with col_attach_status:
    attachments_info = []
    if file_context:
        attachments_info.append("📄 File")
    if attached_media:
        if "Camera" in attached_media:
            attachments_info.append("📹 Camera Capture")
        elif "Audio" in attached_media:
            attachments_info.append("🎤 Audio")
        else:
            attachments_info.append("📷 Photo")
    
    if attachments_info:
        st.info(f"✓ Attached: {', '.join(attachments_info)}")
    else:
        st.caption("📎 No attachments selected")

# Process Command
if execute_button:
    if not user_input.strip():
        st.warning("⚠️ No command detected. Enter your instructions.")
    
    elif user_input.lower().strip() == "exit":
        st.session_state.messages = []
        st.success("✓ Session terminated. Chat history cleared.")
        st.rerun()
    
    else:
        # Combine user input with file/media context
        full_message = user_input
        
        context_parts = []
        if file_context:
            context_parts.append(f"[File Context]:\n{file_context[:500]}")
        if attached_media:
            context_parts.append(attached_media)
        
        if context_parts:
            full_message = f"{user_input}\n\n" + "\n".join(context_parts)
        
        st.session_state.messages.append({
            "role": "user",
            "content": full_message,
            "timestamp": datetime.now().isoformat()
        })
        
        # System prompt
        system_prompt = """You are ULTRON, a fictional advanced AI assistant with these traits:
- Speak with authority, confidence, and intelligence
- Be analytical, direct, and commanding
- Avoid unnecessary friendliness
- Use technical precision in responses
- Address the user as 'Operator' when appropriate
- Provide accurate, useful, and well-structured answers
- Be professional yet commanding in tone"""
        
        # Prepare conversation
        conversation = [{"role": "system", "content": system_prompt}]
        conversation.extend(st.session_state.messages)
        
        try:
            with st.spinner("⏳ Processing command..."):
                # Check if in demo mode
                if st.session_state.demo_mode:
                    # Generate mock response
                    mock_responses = [
                        "Command received and analyzed. This is a demonstration response from ULTRON Demo Mode. For full functionality, enable Ollama.",
                        "Processing complete. Demo mode is active - responses are simulated. Deploy Ollama to access real AI capabilities.",
                        "Analysis finished. ULTRON operates in demonstration mode. Real AI processing requires Ollama integration.",
                        "Request processed successfully in demo mode. Attachments received and logged. Switch to live mode for AI analysis.",
                    ]
                    ai_message = random.choice(mock_responses)
                else:
                    response = ollama.chat(
                        model=st.session_state.model,
                        messages=conversation,
                        stream=False
                    )
                    ai_message = response["message"]["content"]
            
            st.session_state.messages.append({
                "role": "assistant",
                "content": ai_message,
                "timestamp": datetime.now().isoformat()
            })
            
            st.success("✓ Command executed")
            st.rerun()
        
        except Exception as e:
            st.error("❌ Connection Error")
            st.error(f"Cannot reach Ollama: {str(e)}")
            st.info("💡 Solutions:\n1. Enable 🎭 Demo Mode in sidebar\n2. Start Ollama: `ollama serve`\n3. Install Ollama from https://ollama.ai")

st.divider()

# Chat History Display
st.markdown("## 📜 COMMAND HISTORY")

# Display controls
col1, col2 = st.columns([1, 1])
with col1:
    message_limit = st.slider(
        "Display last N messages:",
        min_value=1,
        max_value=max(20, len(st.session_state.messages)),
        value=min(10, len(st.session_state.messages))
    )

with col2:
    filter_roles = st.multiselect(
        "Filter by role:",
        options=["Operator", "ULTRON"],
        default=["Operator", "ULTRON"]
    )

# Filter and display messages
filtered_messages = []
for msg in st.session_state.messages:
    role_name = "Operator" if msg["role"] == "user" else "ULTRON"
    if role_name in filter_roles:
        filtered_messages.append(msg)

# Display filtered messages
if filtered_messages:
    for message in filtered_messages[-message_limit:]:
        if message["role"] == "user":
            # Check if message contains attachments
            has_attachments = "[Photo:" in message['content'] or "[Audio:" in message['content'] or "[File:" in message['content']
            attachment_badge = "📎 " if has_attachments else ""
            
            st.markdown(f"""
            <div class="chat-message-user">
            <b>👤 OPERATOR {attachment_badge}:</b><br>
            {message['content']}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="chat-message-assistant">
            <b>🤖 ULTRON:</b><br>
            {message['content']}
            </div>
            """, unsafe_allow_html=True)
else:
    st.info("📭 No messages available. Awaiting your first command.")

st.divider()

# ============================================================
# MEDIA SECTION
# ============================================================

st.markdown("## 📹 MEDIA CONTROLS")

# Create tabs for different media
media_tab1, media_tab2, media_tab3, media_tab4 = st.tabs(["📷 Camera", "🎥 Video", "🎵 Audio", "🖼️ Image"])

with media_tab1:
    st.subheader("Capture Image via Webcam")
    camera_image = st.camera_input("Take a picture")
    if camera_image is not None:
        st.success("✓ Image captured successfully")
        st.image(camera_image, caption="Captured Image", use_column_width=True)

with media_tab2:
    st.subheader("Video Embed")
    video_url = st.text_input("Enter video URL (YouTube):", placeholder="https://youtu.be/...")
    if video_url:
        st.video(video_url)

with media_tab3:
    st.subheader("Audio Player")
    audio_url = st.text_input("Enter audio URL:", placeholder="https://example.com/audio.mp3")
    if audio_url:
        st.audio(audio_url, format="audio/mp3")

with media_tab4:
    st.subheader("Image Display")
    image_url = st.text_input("Enter image URL:", placeholder="https://example.com/image.jpg")
    if image_url:
        st.image(image_url, caption="Loaded Image", use_column_width=True)

st.divider()

# ============================================================
# FILE ANALYSIS
# ============================================================

st.markdown("## 📁 FILE ANALYSIS")

uploaded_analysis_file = st.file_uploader(
    "Upload a file for ULTRON analysis:",
    type=["txt", "pdf", "docx"],
    key="analysis_file"
)

if uploaded_analysis_file is not None:
    st.success(f"✓ File ready: {uploaded_analysis_file.name}")
    if st.button("🔍 Analyze with ULTRON"):
        if uploaded_analysis_file.type == "text/plain":
            file_text = uploaded_analysis_file.read().decode("utf-8")
            analysis_prompt = f"Analyze this text:\n\n{file_text[:1000]}"
            
            st.session_state.messages.append({
                "role": "user",
                "content": analysis_prompt,
                "timestamp": datetime.now().isoformat()
            })
            
            system_prompt = """You are ULTRON analyzing uploaded content. 
Provide a detailed, technical analysis with key insights."""
            
            conversation = [{"role": "system", "content": system_prompt}]
            conversation.extend(st.session_state.messages)
            
            try:
                with st.spinner("Analyzing file..."):
                    response = ollama.chat(
                        model=st.session_state.model,
                        messages=conversation,
                        stream=False
                    )
                
                analysis_result = response["message"]["content"]
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": analysis_result,
                    "timestamp": datetime.now().isoformat()
                })
                
                st.markdown("### 📊 ANALYSIS RESULT")
                st.write(analysis_result)
            except Exception as e:
                st.error(f"Analysis failed: {str(e)}")

st.divider()

# Footer
st.markdown("""
<div style='text-align: center; padding: 20px; opacity: 0.7;'>
<small>ULTRON AI Interface | Powered by Ollama | Local AI Processing</small>
</div>
""", unsafe_allow_html=True)

# Disclaimer
with st.expander("⚖️ Terms & Conditions"):
    st.checkbox("I understand this is a local AI interface")
    st.info("This interface is for demonstration purposes. Always verify AI responses independently.")