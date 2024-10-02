import requests
#import streamlit as st
import io
from PIL import Image
import io
from io import BytesIO
from dotenv import load_dotenv
load_dotenv()
token = st.secrets['HUGGINGFACE_TOKEN_KEY']
st.set_page_config(
        page_title="Generative Image",
)
display_Anime_df(token)


def Anime_df(token,inputs_value,height_value,width_value,guidance_scale_value,num_inference_steps_value,max_sequence_length_value):
  API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
  headers = {"Authorization": f"Bearer {token}"}
  payload = {
    "inputs": inputs_value,
    "height": height_value,
    "width" : width_value,
    "guidance_scale" : guidance_scale_value,
    "num_inference_steps" : num_inference_steps_value,
    "max_sequence_length" : max_sequence_length_value,
    #"negative_prompt":Negative
  }
  response = requests.post(API_URL, headers=headers, json=payload)
  image_bytes = response.content
  return image_bytes
#prompt="An astronaut riding a green horse"
#image_bytes = Anime_df(token,prompt,1024,1024,5,50,512)
#image = Image.open(io.BytesIO(image_bytes))



def display_Anime_df(token):
    st.markdown("<h1 style='text-align:center;'>Anime Diffusion</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>You can download the image with right click > save image</p>", unsafe_allow_html=True)

    with st.sidebar:
        st.title("Parameters Tuning")
        st.session_state.GS_val3 = st.slider("Select Guidencescale", key="slider1", min_value=0.1, max_value=10.0, value=9.0, step=0.1, help="how much your prompt effect your image")
        if st.session_state.GS_val3 > 9.9:
            st.session_state.GS_val3 = 10
        st.write('Guidence scale:', st.session_state.GS_val3)

        st.session_state.inference_steps_val3 = st.slider("Select Inference Steps", key="slider2", min_value=50, max_value=200, value=100, step=1, help="Number of inference steps for image generation")
        st.write('Inference Steps:', st.session_state.inference_steps_val3)

        st.session_state.Negative4 = st.text_input("enter Negative prompt",help="Things you dont want to see in image")

        st.subheader("Usage Manual (must Read !)")
        st.markdown("""<ul>
                        <li>Anime Diffusion</l1>
                        <li>It convert your text prompts into image</l1>
                        <li>When your prompts contains any hateful or malicious text it wont give you image, instead it might give you error or a blank image so dont do it !</l1>
                        <li>Sometimes it migth give you error even when you give legit prompt in that case try changing prompt a little or clear cache data from above settings</l1>
                        <li>There is only 8000 char input allowed in a single prompt so write wisely</li>
                        <li>when your chat history is long it might get Stuck or takes more time to render page (will fix in future), If you encounter this start another session by refreshing page</li>
                        </ul>
                    
                    """,unsafe_allow_html=True)
        st.success("You are Good to go !")

    if "messages_anime" not in st.session_state:
        st.session_state["messages_anime"] = [
            {"role": "assistant", "content": "What kind of image do you need me to generate? (example: cute anime couple enjoying holidays)"}]

    # Display previous prompts and results
    for message in st.session_state.messages_anime:
        st.chat_message(message["role"]).write(message["content"])
        if "image" in message:
            st.chat_message("assistant").image(message["image"], caption=message["prompt"], use_column_width=True)

    # Prompt Logic
    prompt = st.chat_input("Enter your prompt:")

    if prompt:
    # Input prompt
        st.session_state.messages_anime.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        try:
        # Call the SDF_Runway_ML function with updated parameters
            image_bytes = Anime_df(token, prompt,1024,1024, st.session_state.GS_val3, st.session_state.inference_steps_val3,st.session_state.Negative4)

        # Open the image using PIL
            image = Image.open(io.BytesIO(image_bytes))
            msg = f'Here is your image related to "{prompt}"'

        # Show the result
            st.session_state.messages_anime.append({"role": "assistant", "content": msg, "prompt": prompt, "image": image})
            st.chat_message("assistant").write(msg)
            st.chat_message("assistant").image(image, caption=prompt, use_column_width=True)
    
        except Exception as e:
            st.chat_message("assistant").write("Our Server is at Max Capacity Try using Different Model !")
