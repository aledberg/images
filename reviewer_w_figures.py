## the idea here is to check how well GPT-4 can assist as a reviewer. 

import os
import openai

## enter the key
openai.api_key = "put-your-KEY-here"
from openai import OpenAI
client = OpenAI(api_key=openai.api_key)

## function to append the response of the AI
def appendme(response):
    return({"role":"assistant","content":
            response.choices[0].message.content})

## set up the instructions for the "reviewer"

mymess=[{"role":"system","content":"You are a reviewer of scientific articles and you will criticize the text I am about to submit, both with respect to the content and the form. Try in particular to assess if the data material and methods used are appropriate for the research question at hand. You might also suggest references to previous works that you think should have been mentioned. Please start the review with a very short summary of the main contribution of the paper. This should be followed by a short assessment of the quality of the contribtion in relation to previous reserach in the topic. Then please provide your critique in terms of major and minor points, where you, for each point, suggest improvements in terms of changes to the text or additional analysis that should be made. Please also suggest improvements to fix typos and grammatical errors if you find any. And please be very detailed and firm in your critique, but not unfair. And please refrain from include warning messages such as: As an LLM I cannot ... ."},
        {"role":"user","content":"Can you help me review an article if I input the content of the article as text to you? I will upload both the actual text, and a detailed interpretation of the figures. The figure interpretations comes after the main text (and references)."}]

## specify the model to use
mmodel="gpt-4-1106-preview"	

## send the message to openai
response = client.chat.completions.create(
    model=mmodel,
    messages=mymess,
    max_tokens=4000,
)

## check response 
print(response.choices[0].message.content)

## append this response to the message 
mymess.append(appendme(response))


## here the text we want to get reviewed is appended to the message
## this typically take some editing work, extracting text and images
## from a pdf. 

## in this example I will read the pdf-file and then remove the first
## 1720 characters to just start at the Abstract

import fitz ## fitz is provided by PyMuPDF 
import io

## name (and path) of pdf-file
##fn = "qian_wehby2023.pdf"
##fn = "ledberg2020.pdf"
##fn = "kanamori_etal2023.pdf"
fn = "kelly_etal2023.pdf"
pdf_file=fitz.open(fn)

# iterate over PDF pages and extract text
the_text=" "
for page_index in range(len(pdf_file)): 
    
    # get the page itself 
    page = pdf_file[page_index] 
    ##image_list = page.getImageList()

    the_text +=page.get_text() + chr(12)

## this is the figure interpretations
##with open('ledberg2020/figs_interpreted.txt') as f:
with open('kelly2023/figs_interpreted.txt') as f:
    the_figs = f.read()

dum=the_text + "\n Here follows a description of the figures referred to in the paper\n" + the_figs

##with open("gugge.txt", "w") as outfile:
with open("kelly2023/text_plus_figures.txt", "w") as outfile:
    outfile.write(dum)


    ## if you have a local txt file  you can read it like this
##with open('manus5bmc.txt') as f:
##    the_text = f.read()

## append the text to the message, here we also read the interpreted figures
## and add them as well. 
##tt=the_text[1720:50000]
mymess.append({"role":"user","content": dum})



## send this to openai
response = client.chat.completions.create(
    model=mmodel,
    messages=mymess,
    max_tokens=4000,
)

## print the reply
print(response.choices[0].message.content)

## save reply to a txt file
fn=open("kelly_etal2023_AIreveiwer2.txt","w")
fn.write(response.choices[0].message.content)
fn.close()

