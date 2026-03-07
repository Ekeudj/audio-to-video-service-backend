import os
import requests
from groq import Groq
from dotenv import load_dotenv

#this looks for a .env file and loads the variables inside it as environment variables
load_dotenv()

#Intilize the clients
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def extract_search_keyword(sentence: str):
    """
    Uses ai to pick the single best noun from sentnce to
    send to the pexels api to search for that way its more accurate
    """
    try:
        response = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                   "role": "system",
                   "content": "You are a helpful assistant that extracts the single most important noun from a sentence. Only return the noun, no explanations."
                },
                {"role":"user","content":f"Setence: {sentence}"}
            ],
            max_tokens=10,
            temperature=0.0 #no distarctions bruv
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"AI Keyword Error: {e}")
        return sentence[:30] #Fallback

def fetch_images_for_transcription(project_id: int, text:str):
    """
    Fetch relevant images from Pexels based on the transcribed text and save them locally.
    """
    print(f"DEBUG: Starting image hunt for project {project_id}...")

    #Create a specific folder for this projects images
    output_dir = f"downloads/project_{project_id}_images"
    os.makedirs(output_dir, exist_ok=True)

    #Split the text into sentences
    sentences = [s.strip() for s in text.split(".") if len(s.strip()) > 5] # This is a simple way to split into sentences. You can get fancier if you want!
    saved_files = []

    # phase 3. We loop through each senetnce to find a matching picture
    # This is a very smart loop coz, it assigsn an index to every sentence, so we can name the images like 'test_0.jpg', 'test_1.jpg' etc. This way we know which image corresponds to which sentence.
    for index, sentence in enumerate(sentences):
        query = extract_search_keyword(sentence)

        #Phase 4. Ask pexels for a photo that matches the sentence
        #per_page=1 means we want the single best match
        search_url = f"https://api.pexels.com/v1/search?query={query}&per_page=1"
        #Pexels requires the API key to be sent in the headers for authentication
        #Without specifying whose asking for the search url pexels api will refuse to rteunr data
        headers = {"Authorization": PEXELS_API_KEY}
        try:
            response = requests.get(search_url, headers=headers, timeout=15)

        #200 is the genral code for sucess.
            if response.status_code == 200:
                data = response.json()

            #basically look for a keyword phots in the json file pexels sent back

                if data.get("photos"):
                # Grab the url of the medium sized image, used 0 coz we already specifed one per page
                #And coz we already asigned each photo an index with emunerator method
                    image_url = data['photos'][0]['src']['medium']

                #Phase. 5 download the image data
                #the .content part reads the actual bits of the image, 1 and 0's
                    image_data_res = requests.get(image_url, timeout=15)
                    if image_data_res.status_code == 200:
                        image_file_path = f"{output_dir}/test_{index}.jpg"

                #Phase 6 save the image to the HD
                    with open(image_file_path, "wb") as f:
                        f.write(image_data_res.content)

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

       