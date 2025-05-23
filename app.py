import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from pathlib import Path
import base64
import time
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image
import plotly.graph_objects as go
from PIL import Image

#to run: streamlit run "D:/MSc Digital Project Management and Consulting/Term III/Live Case Study Inditex/trendai_simulator/app.py"
st.set_page_config(page_title="TrendAI - Inditex", layout="wide")  # ESTA LÍNEA DEBE SER LA PRIMERA DE STREAMLIT


from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "assets"
DATA_DIR = BASE_DIR / "data"



st.markdown("""
    <style>
    /* ==== ZARA-INSPIRED THEME ==== */

    /* Fondo general */
    .stApp {
        background-color: #f8f5f2;
        color: #1e1e1e;
        font-family: 'Segoe UI', sans-serif;
    }

    /* Inputs y textareas */
    input, textarea {
        background-color: #ffffff !important;
        color: #1e1e1e !important;
        border: 1px solid #cccccc !important;
        border-radius: 6px !important;
        padding: 0.5em !important;
    }

    /* Selectbox y dropdowns */
    div[data-baseweb="select"] > div {
        background-color: #ffffff !important;
        color: #1e1e1e !important;
        border-radius: 6px !important;
        border: 1px solid #cccccc !important;
    }

    /* Botones */
    div.stButton > button {
        background-color: #000000;
        color: #ffffff;
        border-radius: 6px;
        padding: 0.6em 1.2em;
        font-weight: bold;
        border: none;
        transition: background-color 0.3s ease;
    }

    div.stButton > button:hover {
        background-color: #3a3a3a;
        color: #ffffff;
    }

    /* Encabezados */
    h1, h2, h3, h4, h5 {
        color: #1e1e1e;
        font-family: 'Segoe UI', sans-serif;
    }

    /* Tablas */
    .stDataFrame, .element-container {
        border-radius: 6px !important;
    }

    /* Cuadros de alerta */
    .stAlert {
        border-left: 5px solid #000000 !important;
    }

    /* Scrollbar minimal */
    ::-webkit-scrollbar {
        width: 6px;
    }
    ::-webkit-scrollbar-thumb {
        background: #999;
        border-radius: 10px;
    }

    </style>
""", unsafe_allow_html=True)



if "a" not in st.session_state:
    st.session_state.a = 0



#-------------------------------Tape of brands logos---------------------------------
# Load and encode image as base64 for inline HTML
def get_image_base64(image_path):
    with open(image_path, "rb") as img_file:
        encoded = base64.b64encode(img_file.read()).decode()
    return f"data:image/png;base64,{encoded}"

# Show animated carousel
def show_logo_carousel():
    image_folder = ASSETS_DIR
    image_files = list(image_folder.glob("*.png"))
    images_html = ""

    for image_path in image_files:
        img_src = get_image_base64(image_path)
        images_html += f'<img src="{img_src}" class="carousel-image">'

    carousel_html = f"""
    <style>
        .carousel-container {{
            white-space: nowrap;
            overflow: hidden;
            background-color: #f8f8f8;
            padding: 5px 0;
            border-radius: 10px;
            margin-bottom: 10px;
        }}
        .carousel-track {{
            display: inline-block;
            animation: scroll 20s linear infinite;
        }}
        .carousel-image {{
            height: 100px;
            margin: 0 25px;
            vertical-align: middle;
        }}
        @keyframes scroll {{
            0% {{ transform: translateX(100%); }}
            100% {{ transform: translateX(-100%); }}
        }}
    </style>
    <div class="carousel-container">
        <div class="carousel-track">{images_html}</div>
    </div>
    """
    st.markdown(carousel_html, unsafe_allow_html=True)

# Show the carousel
show_logo_carousel()
#--------------------------------------------------------------------------------



#------------------------------------------- Ask a Question (simulate AI chat)----------------------------------------------------------------------------
import streamlit.components.v1 as components

st.markdown("---")
st.markdown("🤖 Talk to Caco")

# Toggle voice input
if "voice_triggered" not in st.session_state:
    st.session_state.voice_triggered = False

col1, col2 = st.columns([0.1, 0.9])

with col1:
    mic_label = "Stop Listening" if st.session_state.voice_triggered else "Start Listening"
    if st.button(mic_label):    
        st.session_state.voice_triggered = not st.session_state.voice_triggered

    mic_class = "mic-button blinking" if st.session_state.voice_triggered else "mic-button"
    mic_html = f'<i class="fas fa-microphone {mic_class}"></i>'
    st.markdown(mic_html, unsafe_allow_html=True)

    # Red dot indicator
    if st.session_state.voice_triggered:
        st.markdown('<div class="recording-dot"></div>', unsafe_allow_html=True)

with col2:
    if st.session_state.voice_triggered:
        st.info("🎙️ Listening...")

        # Simulated typing effect using Python (char-by-char)
        if st.session_state.a == 0:
            query = "Caco, please start the store scan".lower()
        elif st.session_state.a == 1:
            query = "Caco, show me inventory levels for SKU M123".lower()
        elif st.session_state.a == 2:
            query = "Caco, show me stock turnover rate for the Aura Spring Collection".lower()
        else:
            query = ""
            
        typed_text = ""
        placeholder = st.empty()  # reserve space in the UI

        for char in query:
            typed_text += char
            placeholder.markdown(f"**📝 Transcribing:** `{typed_text}_`")
            time.sleep(0.2)  # adjust speed here

        # Finalize input after typing
        st.session_state.simulated_input = query
        st.session_state.a += 1  # Cada vez que se presiona, avanza al siguiente comando

    else:
        st.text_input("Ask TrendAI something", placeholder="e.g. Summarize the current inventory levels", key="simulated_input")

query = st.session_state.simulated_input.lower()

#Answer of AI Scan initianing
if query:
    st.markdown("💬 TrendAI Response")

    if "caco, please start the store scan" in query:
        st.success("🛰️ Store scan initiating...")

        # Progress bar and messages
        progress_bar = st.progress(0)
        section_message = st.empty()

        sections = [
            ("🧥 Scanning Men’s section...", 33),
            ("👗 Scanning Women’s section...", 66),
            ("🧸 Scanning Kids’ section...", 100),
        ]

        for message, progress in sections:
            time.sleep(1.5)
            section_message.info(message)
            progress_bar.progress(progress)
            time.sleep(1.5)

        section_message.success("✅ All sections scanned successfully!")
    
        # 🔍 Simulated misplaced items
        misplaced_data = {
            "Section": ["Men", "Men", "Women", "Women", "Kids"],
            "SKU": ["M123", "M456", "W789", "W101", "K112"],
            "Item": ["Slim Fit Jeans", "Denim Jacket", "Sleevs Ruffle Pink Shirt", "Vaquero Wide Leg", "Cartoon Hoodie"],
            "Detected Location": [
                "Aisle 7, Floor 1, Women's Section, Shelf 2",
                "Floor 2, Kids Area, Shelf 4",
                "Aisle 1, Men's Entry, Floor 1",
                "Kids Section, Aisle 5, Shelf 1",
                "Women's Section, Floor 1, Back Wall"
            ],
            "Correct Location": [
                "Aisle 3, Floor 1, Men's Section, Shelf 5",
                "Aisle 3, Floor 1, Men's Section, Shelf 5",
                "Aisle 4, Floor 1, Women's Section, Shelf 2",
                "Aisle 2, Floor 2, Women's Section, Shelf 6",
                "Aisle 5, Floor 2, Kids Section, Shelf 1"
            ],
            "Recommended Action": [
                "Relocate to Aisle 3, Floor 1, Men's Section, Shelf 5",
                "Relocate to Aisle 3, Floor 1, Men's Section, Shelf 5",
                "Relocate to Aisle 4, Floor 1, Women's Section, Shelf 2",
                "Relocate to Aisle 2, Floor 2, Women's Section, Shelf 6",
                "Return to warehouse: Aisle 12, Rack 4"
            ],
            "Map X": [0.75, 0.17, 0.72, 0.85, 0.27],
            "Map Y": [0.3, 0.75, 0.68, 0.72, 0.3]

        }


        df_misplaced = pd.DataFrame(misplaced_data)

        # 📸 Misplaced Items Summary with Images
        st.markdown("### 🧾 Misplaced Items Summary")


        map_path = ASSETS_DIR / "Store" / "store_map.png"
        map_img = Image.open(map_path)


        # 🔽 Dropdown to filter section
        section_options = ["All"] + sorted(df_misplaced["Section"].unique())
        selected_section = st.selectbox("🔍 Filter by Section", section_options)

        # Filter the dataframe based on selection
        if selected_section != "All":
            filtered_df = df_misplaced[df_misplaced["Section"] == selected_section]
        else:
            filtered_df = df_misplaced.copy()

        # Set plot dimensions
        fig = go.Figure()

        # Background map
        fig.add_layout_image(
            dict(
                source=map_img,
                xref="x", yref="y",
                x=0, y=1,
                sizex=1, sizey=1,
                sizing="stretch",
                layer="below"
            )
        )

        # Prepare zoom boundaries
        if selected_section != "All":
            min_x = filtered_df["Map X"].min() - 0.1
            max_x = filtered_df["Map X"].max() + 0.1
            min_y = 1 - filtered_df["Map Y"].max() - 0.1
            max_y = 1 - filtered_df["Map Y"].min() + 0.1
        else:
            min_x, max_x = 0, 1
            min_y, max_y = 0, 1

        # Add clickable markers
        for i, row in filtered_df.iterrows():
            fig.add_trace(go.Scatter(
                x=[row["Map X"]],
                y=[row["Map Y"]],
                mode="markers+text",
                marker=dict(size=12, color="red"),
                text=[row["SKU"]],
                textposition="top center",
                name=row["Item"],
                hovertext=row["Item"],
                customdata=[row["SKU"]]
            ))

        # Layout
        fig.update_layout(
            title="📍 Misplaced Item Locations",
            xaxis=dict(showgrid=False, visible=False, range=[min_x, max_x]),
            yaxis=dict(showgrid=False, visible=False, range=[min_y, max_y]),
            width=800,
            height=500,
            margin=dict(l=10, r=10, t=40, b=10)
        )

        # Show interactive chart
        selected_point = st.plotly_chart(fig, use_container_width=True)

        # Clickable item simulation (manual selection fallback)
        sku_options = ["Select a SKU"] + filtered_df["SKU"].tolist()
        clicked_sku = st.selectbox("🖱️ Select SKU to view detected image", sku_options)

        if clicked_sku != "Select a SKU":
            img_path = ASSETS_DIR / "assets/item_images" / f"{clicked_sku}.jpg"
            try:
                st.image(img_path, caption=f"Detected image for SKU {clicked_sku}", use_container_width=True)
            except:
                st.warning("⚠️ No image found for this SKU.")
                
        for section in ["Men", "Women", "Kids"]:
            st.subheader(f"🗂️ {section} Section")
            section_df = df_misplaced[df_misplaced["Section"] == section]

            for _, row in section_df.iterrows():
                with st.expander(f"📦 SKU {row['SKU']} — {row['Item']}"):
                    st.write(f"**Detected in:** {row['Detected Location']}")
                    st.write(f"**Correct location:** {row['Correct Location']}")
                    st.write(f"**Recommended action:** {row['Recommended Action']}")

                    # Button to show image
                    image_path = f"D:/MSc Digital Project Management and Consulting/Term III/Live Case Study Inditex/trendai_simulator/assets/item_images/{row['SKU']}.jpg"
                    try:
                        with open(image_path, "rb") as img_file:
                            st.image(img_file.read(), caption=f"Detected misplaced item: {row['Item']}", use_container_width=True)
                    except FileNotFoundError:
                        st.warning("⚠️ Camera image not available for this item.")


    #Section for inventory levels
    elif "inventory" in query and "m123" in query:
        st.markdown("### 📦 Inventory Levels - SKU M123")
        df_inventory = pd.DataFrame({
            "SKU": ["M123"],
            "Item": ["Slim Fit Jeans"],
            "Stock Level": [4],
            "Status": ["⚠️ Low Stock"]
        })
        st.dataframe(df_inventory, use_container_width=True)
        
    elif "turnover" in query or "aura" in query:
        st.markdown("🧺 Stock Turnover - *Aura Spring Collection* (Last 7 Days)")

        turnover_data = {
            "SKU": ["BS101", "BS102", "BS103"],
            "Item": ["Aura Fringe Dress", "Crochet Crop Top", "Flowy Printed Skirt"],
            "Units Sold": [58, 42, 35],
            "Avg Inventory": [120, 90, 85],
            "Turnover Rate": [0.48, 0.47, 0.41]
        }

        df_turnover = pd.DataFrame(turnover_data)

        st.dataframe(df_turnover, use_container_width=True)

        # Añadir gráfico
        st.markdown(" 📊 Turnover Rate per SKU")
        st.bar_chart(df_turnover.set_index("Item")["Turnover Rate"])

        # Recomendación visual
        st.info("📝 *Suggestion*: BS103 (Flowy Printed Skirt) shows the slowest turnover. Consider repositioning or promotional push.")

        
#----------------------------------------------------------------------------
