import chromadb
import spacy
import numpy as np
from transformers import pipeline
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
pipe = pipeline("text2text-generation", model="HamadML/grammer_correction")
from chromadb.utils import embedding_functions


# def get_similar_nouns(noun, num_results=3):
#     try:
#         similar_words = model.most_similar(noun, topn=num_results)
#     except KeyError:
#         similar_words = []
#     return similar_words

    
# def similarity_scores():
#     """
#     convert_to_questions: function|text
#     Converts a sentence into a question based on the English format
#     input: Fractals are complex geometric shapes that exhibit self-similarity at different scales
#     output: What are complex geometric shapes that exhibit self-similarity at different scales
#     """
#     similarities = []
#     for sentence in sentences:
#         sent_doc = nlp(sentence)
#         for topic in topics:
#             topic_doc = nlp(topic)
#             sim_score = sent_doc.similarity(topic_doc)
#     avg_sim_score = np.mean(sim_score)  
#     similarities.append((sentence, topic, sim_score))


# """
# convert_to_questions: function|text
# Converts a sentence into a question based on the English format
# input: Fractals are complex geometric shapes that exhibit self-similarity at different scales
# output: What are complex geometric shapes that exhibit self-similarity at different scales
# """
# gf = Gramformer(models = 1, use_gpu=True) # 1=corrector, 2=detector
# def _convert_to_question(sentence):
#     nlp= spacy.load('en_core_web_sm')
#     # tool = language_tool_python.LanguageTool('en-US')
#     # Check for grammar errors and correct the sentence
#     # matches = tool.check(sentence)
#     corrected_sentence = gf.correct(sentence)
#     print(corrected_sentence)
#     # Tokenize and tag the sentence using spaCy
#     doc = nlp(corrected_sentence)

#     # Identify question word based on dependency tags and sentence structure
#     question_word = None
#     is_followed_by_noun = False
#     for i, token in enumerate(doc):
#         if token.dep_ in ('nsubj', 'dobj'):
#             # Noun subject or object (who/what)
#             question_word = "Who" if token.pos_ == 'PRON' else "What"
#         elif token.dep_ == 'advmod':
#             # Adverbial modifier (when/where/how)
#             if token.text in ('when', 'how long'):
#                 question_word = "When"
#             elif token.text in ('where', 'in what place'):
#                 question_word = "Where"
#             elif token.text in ('how', 'in what way'):
#                 question_word = "How"
#         elif token.dep_ == 'ROOT' and token.pos_ == 'VERB':
#             # Special case for sentences starting with a verb (Do/Does/Did)
#             if token.text.lower() in ('do', 'does'):
#                 question_word = "Do" if token.text.lower() == 'do' else "Does"
#             elif token.text.lower() == 'did':
#                 question_word = "Did"
#         elif token.text == "is" and i + 1 < len(doc) and doc[i + 1].pos_ in ("NOUN", "PROPN"):
#             is_followed_by_noun = True
#             # Special case for "is + noun phrase"
#             question_word = "What"

#         if question_word:
#             break

#     # Identify the verb (considering auxiliary verbs)
#     verb = None
#     for token in doc:
#         if token.pos_ in ('VERB', 'AUX'):
#             verb = token.text
#             break

#     # Rearrange the sentence to form a question (handle different cases)
#     if question_word and verb:
#         if is_followed_by_noun:
#             question = f"{question_word} {verb} {doc[i + 1].text}?"  # Use noun phrase after "is"
#         elif question_word in ('Do', 'Does', 'Did'):
#             question = f"{question_word} {' '.join(token.text for token in doc[1:])}?"  # Handle sentences starting with a verb
#         else:
#             question = f"{question_word} {verb} {np.array(corrected_sentence).split(verb,1)[1].strip()}?"
#         return {"question":question}
#     else:
#         return None


def get_nouns(sentence):
    tokens = word_tokenize(sentence)
    tagged = pos_tag(tokens)
    nouns = [word for word, tag in tagged if tag.startswith('N')]
    return nouns

# def rankSentences(sentences):
#     # Load pre-trained model and tokenizer
#     model_name = 'bert-base-uncased'
#     tokenizer = BertTokenizer.from_pretrained(model_name)
#     model = BertForMaskedLM.from_pretrained(model_name)

#     # Initialize variables to keep track of the most sensible sentence and its score
#     best_sentence = None
#     best_score = float('-inf')

#     for sentence in sentences:
#         # Tokenize sentence
#         tokenized_sentence = tokenizer.encode(sentence, add_special_tokens=True, return_tensors="pt")

#         # Generate predictions for masked tokens
#         with tokenizer.as_target_tokenizer():
#             masked_index = tokenized_sentence[0].tolist().index(tokenizer.mask_token_id)
#             outputs = model(tokenized_sentence)
#             predictions = outputs[0]

#             # Get the predicted token ID for the masked position
#             predicted_token_id = torch.argmax(predictions[0, masked_index]).item()

#             # Get the predicted token
#             # predicted_token = tokenizer.convert_ids_to_tokens([predicted_token_id])[0]

#             # Score the sentence based on the predicted token (higher is better)
#             score = predictions[0, masked_index, predicted_token_id].item()

#             # Update the best sentence if the current sentence has a higher score
#             if score > best_score:
#                 best_sentence = sentence
#                 best_score = score

#     return best_sentence

client = chromadb.PersistentClient(path="public/vector")
sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L12-v2")

nounsCollection = client.get_or_create_collection(name="nouns",embedding_function=sentence_transformer_ef,metadata={'hnsw:space':'cosine'})


W_Words=["Where","Who","When"]
def convert_to_question(sentence:str):
    noun=get_nouns(sentence)[0]
    parse1=[]
    # for noun in nouns:
    sentence.replace(noun," ")
    parse1.extend([w+" "+sentence for w in W_Words])
    parse2=[pipe(word) for word in parse1]
    
    return {
        "question":parse2[0],
        "answers":nounsCollection.query(query_texts=noun,n_results=3)['metadatas'].extend([noun]),
        "correct":noun
    }



    
        
        
    # # sim = spacy.load("en_core_web_lg")
    # # nlp = spacy.load('en_core_web_sm')
    # # txt = "Fractals are complex geometric shapes that exhibit self-similarity at different scales. This means that as you zoom into a fractal, you'll see smaller copies of the overall shape, repeating infinitely. Fractals are not limited to simple shapes like squares or circles; they can have intricate and infinitely detailed patterns.One of the most famous fractals is the Mandelbrot set, discovered by mathematician Benoit Mandelbrot in the 1970s. The Mandelbrot set is generated by iterating a simple mathematical formula and determining whether the resulting sequence remains bounded or tends to infinity. Points within the Mandelbrot set are colored black, while points outside the set are colored based on how quickly they diverge to infinity."

    # # Alternately a txt file
    # # path = //content/sample_data
    # # 




    # # Load the English language model
    # nlp = spacy.load("en_core_web_sm")
    # similarity = spacy.load('en_core_web_lg')
    # # Define the list of topics and the text
    # topics = ['Physics', 'Chemistry', 'Biology', 'Mathematics', 'Computer Science', 'Medicine', 'Art History', 'Computer Science & Information Technology', 'Law']
    # txt = "Fractals are complex geometric shapes that exhibit self-similarity at different scales. This means that as you zoom into a fractal, you'll see smaller copies of the overall shape, repeating infinitely. Fractals are not limited to simple shapes like squares or circles; they can have intricate and infinitely detailed patterns. One of the most famous fractals is the Mandelbrot set, discovered by mathematician Benoit Mandelbrot in the 1970s. The Mandelbrot set is generated by iterating a simple mathematical formula and determining whether the resulting sequence remains bounded or tends to infinity. Points within the Mandelbrot set are colored black, while points outside the set are colored based on how quickly they diverge to infinity."

    # # Process the text to obtain a Doc object
    # doc = nlp(txt)

    # """
    # input: This is a sunny day. It is very hot today
    # sentences: string|list
    # ouput: This is a sunny day.,It is very hot today.,
    # """
    # # Extract sentences from the Doc object
    # sentences = [sent.text for sent in doc.sents]

    # # Calculate similarities between each sentence and each topic
    # """
    # similarites: integer|list
    # """


    # question = convert_to_question(sent_doc)
    # if question:
    #     print(f"Converted Question: {question}")
    # else:
    #     print("Unable to convert the sentence into a question.")
    # # Print the similarity scores
    # for sentence, topic, similarity_score in similarities:
    #     print(f"Similarity Score: {similarity_score}")

    # max_score = max(similarities, key=lambda x: x[1])

    # print(f"Sentence with maximum average similarity score: '{max_score[0]}' | Average Similarity Score: {max_score[1]}")
