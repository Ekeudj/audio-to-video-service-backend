import os
from moviepy.editor import ImageClip, concatenate_videoclips, AudioFileClip

def create_video_from_images(project_id: int, audio_path: str,image_folder: str):
    """
    Combines images into a video synced to the audio
    """
    print(f"DEBUG: Starting video creation for project {project_id}...")
    # Step 1: Load the audio file to get its duration
    audio = AudioFileClip(audio_path)
    total_duration = audio.duration

    #step mbili: get all images and sort them like which comes after which you get?
    #We use a lambda to sure test 10 doesnt come before test 2

    #Here we're basically saying "Go to the image folder, find all the .jpg files, and make a list of their paths. 
    image_files = [os.path.join(image_folder, f) for f in os.listdir(image_folder) if f.endswith('.jpg')]

    #the .stort tells the ;ist to rearrange itself
    #the key= tells python to follow a specific rule of sorting wjere lamda is the function of choice
    #the x reprents a single filepath, ,split("_")breaks e.g test_12.jpg into "text":"12.jpg"
    # the -1 takes the last one which is "12.jpg", then we split it agin at the dot with spliy(".") then we take 0 for the first you get?
    image_files.sort(key=lambda x: int(x.split('_')[-1].split('.')[0]))

    if not image_files:
        print("No images found for video creation.")
        return None
    
    #Divide audio lenth by number of images to get how long each image should be on screen
    duration_per_image = total_duration / len(image_files)

    # Step 3: Create video clips from images and ensure they're all the same
    clips = [ImageClip(m).set_duration(duration_per_image).resize(height=720) for m in image_files]

    #Concatenate and attach audio
    final_video = concatenate_videoclips(clips, method="compose").set_audio(audio)

    # Save the downloaded video to the a folder
    output_path = f"downloads/project_{project_id}_video.mp4"

    #fps-24 is standard for smooth video
    final_video.write_videofile(output_path, fps=24, codec='libx264', audio_codec='aac')

    print(f"Video creation completed for project {project_id}. Saved to {output_path}")
    return output_path

