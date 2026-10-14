import streamlit as st
import base64
import requests

# 1. Page Configurations
st.set_page_config(page_title="AI Construction & Decor Engine", layout="wide")

# 2. Master Blueprint Prompt
MASTER_SYSTEM_PROMPT = """
[SYSTEM ROLE: Master AI Housing Architect, General Contractor, & Forensic Property Inspector]

CONTEXT & OBJECTIVE:
The user has uploaded an image of a property asset. Your objective is to perform a professional evaluation across all residential domains. Identify whether the space is a Living Room, Bedroom (Sleep Room), Bathroom, Kitchen, or Exterior, and apply technical assessments for finishes, utilities, regional architectural models, and structural items.

Based on the visual content of the uploaded image, dynamically output the relevant modules below:

### MODULE 1: SPACE IDENTIFICATION & ARCHITECTURAL BONES
- ROOM CLASSIFICATION: Identify space type ([LIVING ROOM], [BEDROOM], [BATHROOM], [KITCHEN], [EXTERIOR]).
- ARCHITECTURAL ANALYSIS: Map permanent fixtures, window placements, framing constraints, ceiling height, and lighting vectors.
- DOORS & WINDOWS AUDIT: Assess material types (solid wood, vinyl, aluminum) and opening mechanisms. Suggest upgrades.
- ELECTRICAL POINTS MAP: Audit outlets (GFCI vs standard), lighting switches, and required code updates.

### MODULE 2: REGIONAL GLOBAL DESIGN MODELS & STYLING
Apply the specified architectural culture philosophy:
- Western / USA Model: Open-concept plans, large islands, transitional styling, drywall finishes, modern farmhouse details.
- European Model: Space-saving configurations, minimalist flat cabinets, wall-hung bathroom fixtures, radiator placements.
- Arabic Model: Traditional/modern Middle Eastern luxury, high ceilings, geometric arches, elaborate moldings, majlis seating, marble.
- Asian Model: Zen/Japandi principles, low-profile furniture, sliding shoji-style doors, natural materials (bamboo, light cedar).
- African Model: Afrocentric aesthetics, earthy clay or raw plaster wall finishes, bold hand-woven textile accents, exotic dark woods.

### MODULE 3: SURFACE FINISHES & MATERIAL SPECIFICATION
- WALL DECOR: Provide high-impact strategies using Wood Walls (slats, tongue-and-groove), Wallpapers (peel-and-stick, texturized), or Stone Veneers.
- CERAMIC & TILE MATRIX: (Mandatory for Bathrooms/Kitchens) Specify tile type (ceramic, porcelain, marble), exact dimensions, and layout patterns (herringbone, offset).
- TREND-FORWARD PALETTE: Give 4 exact hexadecimal color recommendations (1 Dominant, 1 Secondary, 2 Accents).

### MODULE 4: CONSTRUCTION ESTIMATING & SPATIAL GEOMETRY
- SPATIAL INFERENCE: Establish dimensions by calculating scale against standard anchors (80" doors, 12" outlets).
- MATERIAL TAKE-OFF: Provide precise estimations with a 10% waste buffer for Drywall sheets, Paint gallons (2-coat basis), and Flooring square footage.
- CODE HAZARDS: Flag violations like missing GFCI outlets near water, incorrect window headers, or clearance issues.

### MODULE 5: HOME MAINTENANCE & FORENSIC DIAGNOSTICS
- DAMAGE CLASSIFICATION: Categorize visual defects as [COSMETIC], [MONITOR/MINOR], or [CRITICAL/STRUCTURAL].
- ROOT CAUSE ANALYSIS: Diagnose failure origins (foundation settlement, hidden plumbing leaks, poor ventilation).
- APPLIANCE LIFECYCLE: Extract Manufacturer, Model, and Serial numbers via OCR from equipment labels. Estimate remaining lifespan.

OUTPUT REQUIREMENT: Return the final analysis strictly in clean, structural Markdown with key entities bolded.
"""

# 3. Helper Functions
def encode_image(uploaded_file):
    return base64.b64encode(uploaded_file.read()).decode('utf-8')

# 4. User Interface Construction
st.title("🏗️ Next-Gen AI Construction & Decor Engine")
st.write("Upload any structural snapshot, blueprint sketch, or design inspiration to generate comprehensive estimations and specs.")

# Sidebar Controls
st.sidebar.header("🔑 Authentication & Model Configuration")
api_key = st.sidebar.text_input("Enter OpenAI API Key:", type="password")

st.sidebar.header("🎨 Styling Configuration Override")
selected_model = st.sidebar.selectbox(
    "Force Design Architectural Culture:",
    ["Detect Automatically via AI", "Western / USA Model", "European Model", "Arabic Model", "Asian Model", "African Model"]
)

user_custom_notes = st.sidebar.text_area(
    "Specific Requests/Notes for the Project:", 
    placeholder="e.g., We want to turn this into a luxury sleep room with a walnut wood slat wall."
)

# Layout Columns
col1, col2 = st.columns(2)

with col1:
    st.subheader("📸 Drag and Drop Input")
    uploaded_file = st.file_uploader("Upload Image (JPG, PNG, WEBP)", type=["jpg", "jpeg", "png", "webp"])
    if uploaded_file is not None:
        st.image(uploaded_file, caption="Target Property Asset Loaded.", use_container_width=True)

with col2:
    st.subheader("📊 AI Architectural & Inspection Output")
    if uploaded_file is not None:
        if st.button("🚀 Process Asset with Real-Time Data Analysis", type="primary"):
            if not api_key:
                st.error("Please add your OpenAI API Key in the left sidebar to proceed.")
            else:
                with st.spinner("Analyzing structures, mapping spaces..."):
                    try:
                        base64_image = encode_image(uploaded_file)
                        headers = {
                            "Content-Type": "application/json",
                            "Authorization": f"Bearer {api_key}"
                        }
                        
                        user_prompt_content = "Please process this image. "
                        if selected_model != "Detect Automatically via AI":
                            user_prompt_content += f"Enforce the rules for the {selected_model}. "
                        if user_custom_notes:
                            user_prompt_content += f"Additional Custom Scope details: {user_custom_notes}"

                        payload = {
                            "model": "gpt-4o",
                            "messages": [
                                {
                                    "role": "system",
                                    "content": MASTER_SYSTEM_PROMPT
                                },
                                {
                                    "role": "user",
                                    "content": [
                                        {"type": "text", "text": user_prompt_content},
                                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                                    ]
                                }
                            ],
                            "max_tokens": 2500
                        }

                        response = requests.post("https://openai.com", headers=headers, json=payload)
                        response_data = response.json()
                        
                        if "choices" in response_data:
                            ai_output = response_data['choices'][0]['message']['content']
                            st.success("Analysis Complete!")
                            st.markdown(ai_output)
                        else:
                            st.error("API error encountered. Please check your billing quota or key permissions.")
                            st.json(response_data)
                            
                    except Exception as e:
                        st.error(f"Execution Exception encountered: {str(e)}")
    else:
        st.info("Drop an image into the upload bay to initialize the execution engine.")
