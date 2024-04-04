import torch
import wikipedia
from transformers import AutoTokenizer, AutoModelWithLMHead

def summarizer(param):
    tokenizer = AutoTokenizer.from_pretrained('t5-base')
    model = AutoModelWithLMHead.from_pretrained('t5-base', return_dict=True)

    sequence = wikipedia.summary(param, sentences=8)
    #print(sequence)
    inputs = tokenizer.encode("summarize: " + sequence, return_tensors='pt', max_length=512, truncation=True)

    summary_ids = model.generate(inputs, max_length=300, min_length=80, length_penalty=5., num_beams=5)

    summary = tokenizer.decode(summary_ids[0])

    return(summary)