import os
import requests
from dotenv import load_dotenv

#this looks for a .env file and loads the variables inside it as environment variables
load_dotenv()

#Grab the Pexels API key from the environment variables
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")

def fetch_images_for_transcription(project_id: int, text:str):
    """
    Fetch relevant images from Pexels based on the transcribed text and save them locally.
    """
    print(f"DEBUG: Starting image hunt for project {project_id}...")

    #Create a specific folder for this projects images
    output_dir = f"downloads/project_{project_id}_images"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    #Split the text into sentences
    sentences = text.split(".") # This is a simple way to split into sentences. You can get fancier if you want!
    saved_files = []

    # phase 3. We loop through each senetnce to find a matching picture
    # This is a very smart loop coz, it assigsn an index to every sentence, so we can name the images like 'test_0.jpg', 'test_1.jpg' etc. This way we know which image corresponds to which sentence.
    for index, sentence in enumerate(sentences):
        query = sentence.strip() #Remove extra spaces

        #Skip empty sentences or very short ones (like just ' ')
        if len(query) < 5:
            continue
        try:
        #Phase 4. Ask pexels for a photo that matches the sentence
        #per_page=1 means we want the single best match
            search_url = f"https://api.pexels.com/v1/search?query={query}&per_page=1"
        #Pexels requires the API key to be sent in the headers for authentication
        #Without specifying whose asking for the search url pexels api will refuse to rteunr data
            headers = {"Authorization": PEXELS_API_KEY}

            response = requests.get(search_url, headers=headers, timeout=20)

        #200 is the genral code for sucess.
            if response.status_code == 200:
                data = response.json()

            #basically look for a keyword phots in the json file pexels sent back

                if data.get("photos"):
                # Grab the url of the medium sized image, used 0 coz we already specifed one per page
                #And coz we already asigned each photo an index with emunerator method
                    image_url = data['photos'][0]['src']['tiny']

                #Phase. 5 download the image data
                #the .content part reads the actual bits of the image, 1 and 0's
                    image_response = requests.get(image_url, timeout=20)
                    image_data = requests.get(image_url).content

                #Create a filename like 'test_1.jpg'
                    image_file_path = f"{output_dir}/test_{index}.jpg"

                #Phase 6 save the image to the HD
                    with open(image_file_path, "wb") as f:
                        f.write(image_data)

                    saved_files.append(image_file_path)
                    print(f"Sucessfully saved image {index}")
                else:
                    print(f"No photos found for query: {query}")
        except Exception as e:
            # This is the slow-internet safety net
            print(f"DEBUG: Skipping sentence {index} due to connection server error {e}")
            continue
    print(f"DeBUG: Finished! Total images saved: {len(saved_files)}")
    return saved_files

       