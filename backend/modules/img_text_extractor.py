import pytesseract
from transformers import Pix2StructProcessor, Pix2StructForConditionalGeneration
import requests
from PIL import Image

def img_txt_extract():
    image_path="C:/Users/TERREL BRAGANCA/Desktop/GEC Spectrathon/5.jpg"
    image=Image.open(image_path)

    #text = pytesseract.image_to_string(image)




    processor = Pix2StructProcessor.from_pretrained('google/deplot')
    model = Pix2StructForConditionalGeneration.from_pretrained('google/deplot')
    # url = "https://raw.githubusercontent.com/vis-nlp/ChartQA/main/ChartQA%20Dataset/val/png/5090.png"
    # image = Image.open(requests.get(url, stream=True).raw)

    inputs = processor(images=image, text="Generate underlying data table of the figure below:", return_tensors="pt")
    predictions = model.generate(**inputs, max_new_tokens=512)
    return(processor.decode(predictions[0], skip_special_tokens=True))