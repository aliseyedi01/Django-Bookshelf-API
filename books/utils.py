import os
from dotenv import load_dotenv
from supabase import create_client, Client
import re

load_dotenv()

url: str = os.getenv('SUPABASE_URL')
key: str = os.getenv('SUPABASE_KEY')


supabase: Client = create_client(url, key)


def upload_to_supabase(image, username, title):
    try:
        filename = re.sub(r'\s+', '-', f"{username}-{title}-{image.name}")

        file_content = image.read()

        storage = supabase.storage.from_("images")

        response = storage.upload(
            file=file_content,
            path=filename,
            file_options={"content-type": image.content_type}
        )

        if not response:
            raise Exception("Error uploading image: No response received")

        if response.status_code != 200:
            raise Exception(f"{response.status_code}Something went wrong while saving profile picture")

        public_url = storage.get_public_url(filename)

        return public_url

    except Exception as e:
        raise Exception(f"Error uploading image: {str(e)}")
