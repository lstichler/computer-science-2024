import streamlit as st

def main():
    st.title("Displaying Text with Streamlit")
    st.header("St. Gallo")
    
if __name__ == "__main__":
    main()

import streamlit as st

def main():
    # Custom style for the dark green box
    st.markdown("""
    <style>
    .dark-green-box {
        background-color: #004225;  /* Dark green color */
        color: white;               /* White text color */
        padding: 10px;              /* Padding inside the box */
        border-radius: 10px;        /* Rounded corners */
    }
    </style>
    """, unsafe_allow_html=True)

    # Creating a container with the custom style
    with st.container():
        st.markdown('<div class="dark-green-box">This is a dark green box in Streamlit!</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
