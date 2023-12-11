## code to use GPT4-V to decode (describe the content of) a number of
## figures from research papers.

import base64
import requests

# OpenAI API Key
api_key = "your key here"

# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

headers = {
  "Content-Type": "application/json",
  "Authorization": f"Bearer {api_key}"
}

## assume the figures and the captions are given as files in two lists detailing the local path the figures and captions

figlist=["kanamori2023/kanamori_etal2023figure_1.jpeg","kanamori2023/kanamori_etal2023figure_2.jpeg","kanamori2023/kanamori_etal2023figure_3.jpeg"]

caplist=["kanamori2023/kanamori_etal2023figure_1c.txt","kanamori2023/kanamori_etal2023figure_2c.txt","kanamori2023/kanamori_etal2023figure_3c.txt"]

figcontents=list()

for i in range(len(figlist)):
    
    ## system message, instruct the AI what it should do
    sysmess=[{"role":"system","content":"You are a helpful expert reviewer and scientist and you will help me interpreting a figures from scientific papers that I will upload/direct you to. To your help I will also provide a figure caption corresponding to the figure. Please provide detailed descriptions and interpretations of the content of each figure. Use the format Figure X: ... in your response, where you take 'X' from the provided figure caption. And please do not include warning messages such as: as an LLM I cannot ... ."}]
    
    ## convert the images to base 64
    currim=encode_image(figlist[i])
    
    ## add the captions
    with open(caplist[i]) as f:
        cap = f.read()
    ## format to a dict
    tmp={"role": "user",
         "content" : cap}
    sysmess.append(tmp)

    ## and the image
    tmp={"role": "user",
         "content" : [
             {
                 "type" : "image_url",
                 "image_url" : {
                     "url": f"data:image/jpeg;base64,{currim}"
                 }
             }
         ]
         }
    sysmess.append(tmp)
    
    payload = {
        "model": "gpt-4-vision-preview",
        "messages": sysmess,
        "max_tokens": 2000
    }
    ## send the request
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    ##print(response.json())
    ##print(response.json()['choices'][0]['message']['content'])
    figcontents.append(response.json()['choices'][0]['message']['content'])

## save the interpretations 

with open("kanamori2023/figs_interpreted.txt", "w") as outfile:
    for line in figcontents:
        outfile.write(f"{line}\n\n")

