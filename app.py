import streamlit as st
import instaloader
import numpy as np

def fetch_instagram_profile(username):
    # Create an Instaloader instance
    ig = instaloader.Instaloader()

    # Fetch profile information
    profile = instaloader.Profile.from_username(ig.context, username)

    # Display fetched details
    st.write("### Results:")
    st.write(f"**Username:** {profile.username}")
    st.write(f"**Number of digits in username:** {sum(char.isdigit() for char in profile.username)}")
    st.write(f"**Number of words in username:** {len(profile.username.split())}")
    st.write(f"**Number of digits in full name:** {sum(char.isdigit() for char in profile.full_name)}")
    st.write(f"**Number of words in full name:** {len(profile.full_name.split())}")
    st.write(f"**Full Name:** {profile.full_name}")
    st.write(f"**Number of Posts Uploads:** {profile.mediacount}")
    st.write(f"**Bio:** {profile.biography}")

    # Check if the account has an external URL
    if profile.external_url:
        st.write(f"**External URL:** {profile.external_url}")
    else:
        st.write("**No External URL set.**")

    # Check if the account is private
    st.write(f"**Account is {'private' if profile.is_private else 'not private'}.**")

    # Use the fetched details as input to the machine learning model
    profile_data = {
        'profile_pic': 1 if profile.profile_pic_url else 0,
        'num_by_num': sum(char.isdigit() for char in profile.username) / len(profile.username.split()),
        'full_name': len(profile.full_name.split()),
        'num_by_char': sum(char.isdigit() for char in profile.full_name) / len(profile.full_name),
        'name_username': 1 if profile.full_name.lower() == profile.username.lower() else 0,
        'bio_len': len(profile.biography),
        'url': 1 if profile.external_url else 0,
        'private': 1 if profile.is_private else 0,
        'post': profile.mediacount,
        'followers': profile.followers,
        'follows': profile.followees,
    }

    # Convert the user input to a NumPy array
    user_input = np.array([[profile_data['profile_pic'], profile_data['num_by_num'], profile_data['full_name'],
                            profile_data['num_by_char'], profile_data['name_username'], profile_data['bio_len'],
                            profile_data['url'], profile_data['private'], profile_data['post'],
                            profile_data['followers'], profile_data['follows']]])

    return user_input

def main():
    st.title("Social Media Analyzer")

    # Options on the main page
    social_media_platform = st.selectbox("Select social media platform", ["Twitter", "Instagram"])
    username = st.text_input("Enter username")

    # Buttons
    search_button = st.button("Search")
    predict_button = st.button("Predict")

    # Perform actions based on button clicks
    if search_button and username:
        st.write("Searching...")

        # Fetch and display Instagram profile details
        user_input = fetch_instagram_profile(username)

        # You can use the 'user_input' array for further processing or machine learning predictions

    elif predict_button:
        st.write("Predicting...")  # You can replace this with the actual prediction functionality

if __name__ == "__main__":
    main()
