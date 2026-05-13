import streamlit as st
import base64
import json
from urllib.parse import quote, unquote

st.set_page_config(
    page_title="Wisher App",
    page_icon="🎉",
    layout="centered"
)

# =========================================================
# STYLES
# =========================================================

st.markdown(
    """
    <style>

    .main {
        background: linear-gradient(135deg, #0f172a, #1e293b);
        color: white;
    }

    .title {
        text-align: center;
        font-size: 3rem;
        font-weight: 800;
        margin-top: 10px;
        color: #ffffff;
        animation: glow 2s infinite alternate;
    }

    @keyframes glow {
        from {
            text-shadow: 0 0 10px #ff4d6d;
        }
        to {
            text-shadow: 0 0 25px #ffd166;
        }
    }

    .wish-card {
        background: rgba(255,255,255,0.08);
        backdrop-filter: blur(12px);
        border-radius: 24px;
        padding: 40px;
        margin-top: 30px;
        text-align: center;
        border: 1px solid rgba(255,255,255,0.15);
        box-shadow: 0 8px 30px rgba(0,0,0,0.35);
        animation: floatCard 4s ease-in-out infinite;
    }

    @keyframes floatCard {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-8px); }
        100% { transform: translateY(0px); }
    }

    .wish-type {
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 10px;
        color: #ffd166;
    }

    .wish-message {
        font-size: 1.3rem;
        line-height: 1.8;
        margin-top: 20px;
        color: #ffffff;
    }

    .wish-from {
        margin-top: 30px;
        font-size: 1.1rem;
        color: #f1f5f9;
        font-weight: 600;
    }

    .footer {
        text-align: center;
        margin-top: 30px;
        color: #cbd5e1;
    }

    .creator-box {
        background: rgba(255,255,255,0.06);
        padding: 25px;
        border-radius: 18px;
        border: 1px solid rgba(255,255,255,0.08);
        margin-top: 20px;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# =========================================================
# HELPERS
# =========================================================


def encode_data(data):
    json_data = json.dumps(data)
    encoded = base64.urlsafe_b64encode(json_data.encode()).decode()
    return encoded



def decode_data(encoded):
    decoded = base64.urlsafe_b64decode(encoded.encode()).decode()
    return json.loads(decoded)


# =========================================================
# QUERY PARAMS
# =========================================================

params = st.query_params
wish_data = params.get("wish")

# =========================================================
# IF LINK OPENED
# =========================================================

if wish_data:

    try:
        data = decode_data(unquote(wish_data))

        occasion = data.get("occasion")
        sender = data.get("sender")
        receiver = data.get("receiver")
        message = data.get("message")
        emoji = data.get("emoji")

        # Animations
        st.balloons()

        st.markdown(
            f"""
            <div class='title'>✨ Special Wish ✨</div>

            <div class='wish-card'>
                <div class='wish-type'>
                    {emoji} {occasion} {emoji}
                </div>

                <h2>Dear {receiver},</h2>

                <div class='wish-message'>
                    {message}
                </div>

                <div class='wish-from'>
                    ❤️ From {sender}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <div class='footer'>
                Made with ❤️ using Streamlit
            </div>
            """,
            unsafe_allow_html=True
        )

    except:
        st.error("Invalid or corrupted wish link.")

# =========================================================
# WISH CREATOR
# =========================================================

else:

    st.markdown(
        """
        <div class='title'>🎉 Wisher App 🎉</div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### Create a Beautiful Wish Link")

    with st.container():

        st.markdown("<div class='creator-box'>", unsafe_allow_html=True)

        occasion = st.selectbox(
            "Select Occasion",
            [
                "Birthday",
                "Anniversary",
                "Graduation",
                "Congratulations",
                "New Year",
                "Custom"
            ]
        )

        emoji_map = {
            "Birthday": "🎂",
            "Anniversary": "💖",
            "Graduation": "🎓",
            "Congratulations": "🎉",
            "New Year": "🎆",
            "Custom": "✨"
        }

        sender = st.text_input("Your Name")
        receiver = st.text_input("Receiver Name")

        default_messages = {
            "Birthday": "Wishing you happiness, success, laughter, and endless joy on your special day!",
            "Anniversary": "May your love continue to grow stronger with each passing year.",
            "Graduation": "Congratulations on your achievement and best wishes for your future journey.",
            "Congratulations": "You did it! Wishing you even more success ahead.",
            "New Year": "May the new year bring happiness, peace, and success into your life.",
            "Custom": "Write your own message here..."
        }

        message = st.text_area(
            "Wish Message",
            value=default_messages[occasion],
            height=180
        )

        if st.button("Generate Wish Link", use_container_width=True):

            if not sender or not receiver or not message:
                st.warning("Please fill all fields.")

            else:

                payload = {
                    "occasion": occasion,
                    "sender": sender,
                    "receiver": receiver,
                    "message": message,
                    "emoji": emoji_map[occasion]
                }

                encoded = encode_data(payload)

                app_url = st.secrets.get(
                    "APP_URL",
                    "https://wish-app.streamlit.app"
                )

                share_link = f"{app_url}/?wish={quote(encoded)}"

                st.success("Wish link generated successfully!")

                st.code(share_link, language="text")

                st.markdown("### Preview")

                st.markdown(
                    f"""
                    <div class='wish-card'>
                        <div class='wish-type'>
                            {emoji_map[occasion]} {occasion}
                        </div>

                        <h2>Dear {receiver},</h2>

                        <div class='wish-message'>
                            {message}
                        </div>

                        <div class='wish-from'>
                            ❤️ From {sender}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        st.markdown("</div>", unsafe_allow_html=True)
