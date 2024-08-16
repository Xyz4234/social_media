#3. Social Media Platform
#Description: Design a simple social media platform where a User class can post Post objects, like Post, 
# and comment on Post. The User class should contain 
# a list of Post objects representing the user's posts,
#  and the Post class should contain a list of Comment objects representing the comments on a post.
#Classes:
#User: Contains user information and a list of Post objects.
#Post: Represents a post with attributes like content and a list of Comment objects.
#Comment: Represents a comment with attributes like content and author.



import streamlit as st
from PIL import Image
from st_supabase_connection import SupabaseConnection

# Supabase connection setup
url = "https://hgaxxesnbfrmebnfkaku.supabase.co"  # Replace with your Supabase project URL
api_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhnYXh4ZXNuYmZybWVibmZrYWt1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjM4MTM5MzIsImV4cCI6MjAzOTM4OTkzMn0.bQKAg-P7r3Uq9pkkTXZDCp8N9MSMckNq26XFX4DGqr0"  # Replace with your Supabase API key
supabase: Client = create_client(url, api_key)

# Function to upload images to Supabase Storage
def upload_image(image_file, folder="posts"):
    # Define the path where the image will be stored
    image_name = f"{folder}/{image_file.name}"
    # Upload image to Supabase Storage
    response = supabase.storage.from_("images").upload(image_name, image_file)
    if response:
        # Return the public URL of the image
        return f"{url}/storage/v1/object/public/{image_name}"
    return None

# Function to fetch posts from the database
def fetch_posts():
    response = supabase.table('posts').select("*").execute()
    return response.data if response.data else []

# Function to fetch stories from the database
def fetch_stories():
    response = supabase.table('stories').select("*").execute()
    return response.data if response.data else []

# Function to add a new post to the database
def add_post(username, content, image_url=None):
    data = {"username": username, "content": content, "image_url": image_url}
    supabase.table('posts').insert(data).execute()

# Function to add a new story to the database
def add_story(username, content, image_url=None):
    data = {"username": username, "content": content, "image_url": image_url}
    supabase.table('stories').insert(data).execute()

# Streamlit app layout
st.title("Social Media App for Kerwens VIP people😎")

# Ask for username
username = st.text_input("Enter your username:")

if username:
    if username in ["iesezenna", "kesasindar"]:
        st.session_state.current_user = username
        
        # Display the feed
        st.subheader("Welcome to the feed!")
        
        # Display stories
        st.write("### Stories")
        stories = fetch_stories()
        if stories:
            for story in stories:
                st.write(f"- {story['content']} (Posted by: {story['username']})")
                if story['image_url']:
                    st.image(story['image_url'], use_column_width=True)
        else:
            st.write("No stories available.")
        
        # Display posts
        st.write("### Posts")
        posts = fetch_posts()
        if posts:
            for post in posts:
                st.write(f"- {post['content']} (Posted by: {post['username']})")
                if post['image_url']:
                    st.image(post['image_url'], use_column_width=True)
                comment = st.text_input(f"Comment on {post['content']}:", key=f"comment_{post['content']}")
                if comment:
                    st.write(f"Comment: {comment}")
        else:
            st.write("No posts available.")
        
        # Add a post
        post_content = st.text_area("Share a post:")
        post_image = st.file_uploader("Upload an image for your post:", type=["jpg", "jpeg", "png"], key="post_image")
        if post_image:
            image_url = upload_image(post_image)
        if st.button("Add Post"):
            if post_content or post_image:
                add_post(username, post_content, image_url)
                st.success("Post added!")
            else:
                st.error("Post cannot be empty.")
        
        # Add a story
        story_content = st.text_area("Share a story:")
        story_image = st.file_uploader("Upload an image for your story:", type=["jpg", "jpeg", "png"], key="story_image")
        if story_image:
            image_url = upload_image(story_image)
        if st.button("Add Story"):
            if story_content or story_image:
                add_story(username, story_content, image_url)
                st.success("Story added!")
            else:
                st.error("Story cannot be empty.")
    else:
        st.error("Unauthorized user. Please enter a valid username.")

