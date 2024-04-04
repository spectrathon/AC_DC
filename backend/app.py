from collections import Counter
import chromadb
from flask import Flask, request,jsonify
from flask_cors import CORS
# from modules.chromadb import similarity_topics
import spacy
import numpy as np
from chromadb.utils import embedding_functions
from gramformer import Gramformer

from modules.summarizer import summarizer
from modules.grammer import convert_to_question

from transformers import pipeline

pipe = pipeline("text2text-generation", model="HamadML/grammer_correction")


app = Flask(__name__)
cors = CORS(app)


@app.route('/AddDef')
def AddDef():
    CourseCollection.add(
    documents=[
        'Physics course description: Fundamental principles of physics, including mechanics, thermodynamics, electromagnetism, and modern physics.',
        'Chemistry course description: Basic concepts of chemistry, including atomic structure, chemical bonding, reactions, and the periodic table.',
        'Biology course description: Study of living organisms and their interactions with the environment, including cell biology, genetics, evolution, and ecology.',
        'Medical Sciences course description: Overview of medical sciences, including anatomy, physiology, pharmacology, and pathology.',
        'Medicine course description: Study and practice of medicine, including diagnosis, treatment, and prevention of disease.',
        'Religion course description: Study of religions, including their beliefs, practices, and cultural impact.',
        'Art History course description: Study of art and its cultural and historical context.',
        'Music course description: Study of music, including theory, composition, and performance.',
        'Computer Science & Information Technology course description: Study of computer science and information technology, including hardware, software, and networks.',
        'Entrepreneurship course description: Study of entrepreneurship, including starting and managing a business.',
        'Law course description: Study of law, including its principles and applications in society.',
        'Legal Theory course description: Study of legal theory, including the nature of law and its interpretation.',
        'Civil Law course description: Study of civil law, including laws governing relationships between individuals.',
        'Criminal Law course description: Study of criminal law, including laws governing crimes and their punishment.',
        'International Law course description: Study of international law, including laws governing relations between countries.',
         'Computer Science course description: This course covers a wide range of topics in computer science, including algorithms, data structures, programming languages, software development, computer architecture, and operating systems. Students will learn to design and analyze algorithms, implement data structures, and develop software applications. The course also explores computer hardware and system software, providing a comprehensive understanding of how computers work and how they are used in various applications.',
        'Computer Programming course description: This course focuses on programming languages and software development. Students will learn programming concepts, syntax, and techniques for writing efficient and maintainable code. The course covers a variety of programming languages, such as Python, Java, C++, and JavaScript, and emphasizes problem-solving skills and logical thinking.',
        'Data Structures course description: This course explores fundamental data structures, such as arrays, linked lists, stacks, queues, trees, and graphs. Students will learn how to implement and use these data structures to solve real-world problems efficiently. The course also covers algorithms for searching, sorting, and manipulating data, providing a solid foundation for further study in computer science.',
        'Database Management course description: This course focuses on database systems and their management. Students will learn about relational database concepts, database design, SQL programming, and database administration. The course also covers topics such as data modeling, normalization, and transaction management, preparing students for careers in database management and administration.',
        'Computer Networks course description: This course introduces the principles of computer networks, including network architecture, protocols, and technologies. Students will learn how data is transmitted over networks, how networks are structured and managed, and how to troubleshoot network issues. The course also covers topics such as network security, wireless networking, and Internet technologies, providing a comprehensive overview of computer networking.',
        'Operating Systems course description: This course explores the principles of operating systems, including process management, memory management, file systems, and device management. Students will learn how operating systems manage computer resources, provide a user interface, and ensure system security and reliability. The course also covers modern operating systems, such as Windows, macOS, and Linux, and prepares students for careers in system administration and software development.'
    ],
    metadatas=[
        {"name":"Physics","code":"Physics"},
        {"name":"Chemistry","code":"Chemistry"},
        {"name":"Biology","code":"Biology"},
       
        {"name":"Medical Sciences","code":"Medical Sciences"},
        {"name":"Medicine","code":"Medicine"},
        {"name":"Religion","code":"Religion"},
        {"name":"Art History","code":"Art History"},
        {"name":"Music","code":"Music"},
        {"name":"Computer Science & Information Technology","code":"CS & IT"},
        {"name":"Entrepreneurship","code":"Entrepreneurship"},
        {"name":"Law","code":"Law"},
        {"name":"Legal Theory","code":"Legal Theory"},
        {"name":"Civil Law","code":"Civil Law"},
        {"name":"Criminal Law","code":"Criminal Law"},
        {"name":"International Law","code":"International Law"},
          {"name":"Computer Science","code":"Computer Science"},
        {"name":"Computer Programming","code":"Computer Programming"},
        {"name":"Data Structures","code":"Data Structures"},
        {"name":"Database Management","code":"Database Management"},
        {"name":"Computer Networks","code":"Computer Networks"},
        {"name":"Operating Systems","code":"Operating Systems"}
    ],
    ids=['Physics', 'Chemistry', 'Biology',  'Medical Sciences', 'Medicine', 'Religion', 'Art History', 'Music', 'Computer Science & Information Technology', 'Entrepreneurship', 'Law', 'Legal Theory', 'Civil Law', 'Criminal Law', 'International Law','Computer Science', 'Computer Programming', 'Data Structures', 'Database Management', 'Computer Networks', 'Operating Systems']
        ) 
    MCQsCollection.add(
    documents=[
        "What year did Nirvana release their album 'Nevermind'?",
        "Which artist released the hit single 'Baby One More Time' in 1998?",
        "Which band is known for their song 'Wonderwall' released in 1995?",
        "What is the name of the lead singer of the band 'No Doubt'?"
    ],
    metadatas=[
        {"question": "What year did Nirvana release their album 'Nevermind'?", "options": "1991,1992,1993,1994", "correct": "1991"},
        {"question": "Which artist released the hit single 'Baby One More Time' in 1998?", "options": "Britney Spears,Christina Aguilera,Mariah Carey,Whitney Houston", "correct": "Britney Spears"},
        {"question": "Which band is known for their song 'Wonderwall' released in 1995?", "options": "Radiohead,Blur,Oasis,Nirvana", "correct": "Oasis"},
        {"question": "What is the name of the lead singer of the band 'No Doubt'?", "options": "Gwen Stefani,Alanis Morissette,Shirley Manson,Avril Lavigne", "correct": "Gwen Stefani"}
    ],
    ids=["Nirvana", "BabyOneMoreTime", "Wonderwall", "NoDoubt"]
)
    MCQsCollection.add(
    documents=[
        "What does CPU stand for?",
        "Which component is responsible for storing data in a computer system for immediate use?",
        "What is the purpose of an operating system?",
        "Which memory is non-volatile and can be programmed and erased in blocks?",
        "What is the function of an interrupt in a computer system?",
        "Which scheduling algorithm provides the highest average turnaround time?",
        "What is the primary function of the Memory Management Unit (MMU) in a computer?",
        "What is the role of the bootloader in a computer system?",
    ],
    metadatas=[
        {"question": "What does CPU stand for?", "options": "Central Processing Unit,Computer Processing Unit,Central Program Unit,Computer Program Unit", "correct": "Central Processing Unit"},
        {"question": "Which component is responsible for storing data in a computer system for immediate use?", "options": "RAM,CPU,Hard Drive,Cache", "correct": "RAM"},
        {"question": "What is the purpose of an operating system?", "options": "To manage hardware resources,To provide a user interface,To run applications,To connect to the internet", "correct": "To manage hardware resources"},
        {"question": "Which memory is non-volatile and can be programmed and erased in blocks?", "options": "ROM,DRAM,SRAM,Cache", "correct": "ROM"},
        {"question": "What is the function of an interrupt in a computer system?", "options": "To pause the current process and handle a specific event,To speed up the CPU,To increase memory capacity,To connect to external devices", "correct": "To pause the current process and handle a specific event"},
        {"question": "Which scheduling algorithm provides the highest average turnaround time?", "options": "First-Come, First-Served (FCFS),Shortest Job Next (SJN),Round Robin (RR),Priority Scheduling", "correct": "First-Come, First-Served (FCFS)"},
        {"question": "What is the primary function of the Memory Management Unit (MMU) in a computer?", "options": "To translate virtual addresses to physical addresses,To manage the CPU registers,To manage the cache memory,To control the input/output devices", "correct": "To translate virtual addresses to physical addresses"},
        {"question": "What is the role of the bootloader in a computer system?", "options": "To load the operating system into memory during startup,To manage the CPU,To control the input/output devices,To provide a user interface", "correct": "To load the operating system into memory during startup"}
    ],
    ids=["CPU", "RAM", "OS", "ROM", "Interrupt", "Scheduling", "MMU", "Bootloader"]
)
    MCQsCollection.add(
    documents=[
        "What is the study of matter, energy, and the interaction between them called?",
        "Which of the following is a noble gas? A) Helium B) Oxygen C) Nitrogen D) Carbon",
        "What is the powerhouse of the cell?",
        "Which programming language is commonly used for artificial intelligence?",
        "What is the medical term for the voice box?",
        "Which of the following is not a major world religion? A) Christianity B) Islam C) Buddhism D) Hinduism",
        "Who painted the Mona Lisa?",
        "Which era in music is known for its complex harmonies and melodies?",
        "What is the process of converting data into a format that is unreadable without the correct decryption key?",
        "Which of the following is a branch of physics that deals with the behavior of very small particles?",
        "What is the study of the Earth's atmosphere and weather called?",
        "What is the study of the origin, evolution, and eventual fate of the universe called?",
        "Which branch of mathematics deals with the study of quantity, structure, space, and change?",
        "What is the medical specialty that deals with the prevention, diagnosis, and treatment of diseases?",
        "Which of the following is a social science that studies human societies, their interactions, and the processes that preserve and change them? A) Anthropology B) Economics C) Geography D) Biology",
        
    ],
    metadatas=[
        {"question": "What is the study of matter, energy, and the interaction between them called?", "options": "Physics,Chemistry,Biology,Earth Sciences", "correct": "Physics"},
        {"question": "Which of the following is a noble gas?", "options": "Helium,Oxygen, Nitrogen , Carbon", "correct": "Helium"},
        {"question": "What is the powerhouse of the cell?", "options": "Mitochondria,Nucleus,Cytoplasm,Golgi Apparatus", "correct": "Mitochondria"},
        {"question": "Which programming language is commonly used for artificial intelligence?", "options": "Python,Java,C,PHP", "correct": "Python"},
        {"question": "What is the medical term for the voice box?", "options": "Larynx,Trachea,Esophagus,Pharynx", "correct": "Larynx"},
        {"question": "Which of the following is not a major world religion?", "options": " Christianity, Islam, Buddhism, Hinduism", "correct": " Hinduism"},
        {"question": "Who painted the Mona Lisa?", "options": "Leonardo da Vinci,Pablo Picasso,Vincent van Gogh,Claude Monet", "correct": "Leonardo da Vinci"},
        {"question": "Which era in music is known for its complex harmonies and melodies?", "options": "Baroque,Renaissance,Classical,Romantic", "correct": "Baroque"},
        {"question": "What is the process of converting data into a format that is unreadable without the correct decryption key?", "options": "Encryption,Decryption,Encoding,Decoding", "correct": "Encryption"},
        {"question": "Which of the following is a branch of physics that deals with the behavior of very small particles?", "options": "Quantum Physics,Classical Physics,Relativity,Thermodynamics", "correct": "Quantum Physics"},
        {"question": "What is the study of the Earth's atmosphere and weather called?", "options": "Meteorology,Geology,Oceanography,Seismology", "correct": "Meteorology"},
        {"question": "What is the study of the origin, evolution, and eventual fate of the universe called?", "options": "Cosmology,Astronomy,Astrophysics,Geophysics", "correct": "Cosmology"},
        {"question": "Which branch of mathematics deals with the study of quantity, structure, space, and change?", "options": "Mathematics,Statistics,Logic,Computer Science", "correct": "Mathematics"},
        {"question": "What is the medical specialty that deals with the prevention, diagnosis, and treatment of diseases?", "options": "Medicine,Dentistry,Nursing,Pharmacology", "correct": "Medicine"},
        {"question": "Which of the following is a social science that studies human societies, their interactions, and the processes that preserve and change them?", "options": "A) Anthropology B) Economics C) Geography D) Biology", "correct": "A) Anthropology"},
       
    ],
    ids=["Physics", "Chemistry", "Biology", "Computer Science", "Medicine", "Religion", "ArtHistory", "Music", "ComputerScience_IT", "Entrepreneurship", "Law", "LegalTheory", "CivilLaw", "CriminalLaw", "InternationalLaw"]
)

    
    return {"Res":"Done"}




@app.route("/search", methods=["POST"])
def searchCourse():
    query = request.args.get("query")
    content=""
    file = request.files["file"]
    if file.filename.endswith('.txt'):
        file_contents = file.read().decode('unicode_escape')
        content=file_contents
    
    print(query)
    results = CourseCollection.query(
        query_texts=[query+content],
        
        n_results=8,
        include=["documents", "distances", "metadatas"],
    )

    return jsonify({
        "present": 1 if np.average(results["distances"])>0.3 else 0,
        "courses":[
        {
            "code": obj["code"],
            "name": obj["name"],
        }
        for obj in results["metadatas"][0]
    ],
    }) 
    

@app.route("/CreateMCQ")
def CreateMCQ():
    query = request.args.get("query")
    results = MCQsCollection.query(
        query_texts=[query],
        n_results=10,
        include=["documents", "distances", "metadatas"],
    )
    # print(results['metadatas'])
    # q=[{
    #             "question": x['question'],
    #             "options": x['options'].split(","),
    #             "correct": x['correct']} for x in results['metadatas']]
    return {
        "question": results['metadatas'][0]
        ,"topics":results["ids"]
    }


# @app.route("/SearchMcq")
# def SearchMcq():
#     query = request.args.get("query")
#     results = MCQsCollection.query(
#         query_texts=[query],
#         n_results=3,
#         include=["documents", "distances", "metadatas"],
#     )

#     dist = np.average(results["distances"])  
#     return jsonify({
#         "present": 1 if dist>0.3 else 0,
#         "course":[
#         {
#             "question": obj["question"],
#             "summary": obj["summary"],
#             "options": obj["options"].split(','),
#             "correct": obj["correct"],
#         }
#         for obj in results["metadatas"][0]
#     ],
#     })


# @app.route("/createCourse",methods=["POST"])
# def createCourse():
#     content=""
#     file = request.files["file"]
#     if file.filename.endswith('.txt'):
#         file_contents = file.read().decode('unicode_escape')
#         content=file_contents
    
    
#     new_content=pipe(content)
#     doc = nlp(new_content)


#     word_counts = Counter()
#     for token in doc:
#         if token.pos_.startswith("N") and token.is_alpha:
#             word = token.text.lower()
#             word_counts[word] += 1

#         top_nouns = word_counts.most_common(5)

#     sentences = [sent.text for sent in doc.sents]
#     sentence_similarities = []

#     top_nouns = [token.text for token in doc if token.pos_ == "NOUN"][:5]

#     for sentence in sentences:
#         sentence_doc = nlp(sentence)
#         similarities = [sentence_doc.similarity(nlp(noun)) for noun in top_nouns]
#         max_similarity = max(similarities)
#         sentence_similarities.append((sentence, max_similarity))
#     sentence_similarities.sort(key=lambda x: x[1], reverse=True)
#     resp=[]

#     for sentence in sentences:
#         resp.extend(convert_to_question(sentence))

  
    
   


#     CourseCollection.add(
#     documents=[summarizer(q) for q in top_nouns],
#     metadatas=[ {
#             "code": noun,
#             "name": noun,
#         } for noun in top_nouns],
#     ids=top_nouns
#     )  
#     MCQsCollection.add(
#     documents=[summarizer(q["question"]) for q in resp],
#     metadatas=resp,
#     ids=[q["question"] for q in resp]
#     )  

#     return {"result": "courseID"}


# @app.route("/courseData", methods=["GET"])
# def courseData():
#     Course = {
#         "name": "Operating Systems",
#         "topics": ["registers", "busses"],
#         "code": "OSX034",
#     }
#     Course["code"] = request.args.get("code")

#     return jsonify(Course)




if __name__ == "__main__":
    client = chromadb.PersistentClient(path="public/vector")
    sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L12-v2")

    nounsCollection = client.get_or_create_collection(name="nouns",embedding_function=sentence_transformer_ef,metadata={'hnsw:space':'cosine'})
    MCQsCollection = client.get_or_create_collection(name="MCQ",embedding_function=sentence_transformer_ef,metadata={'hnsw:space':'cosine'})
    CourseCollection = client.get_or_create_collection(name="CourseCollection",embedding_function=sentence_transformer_ef,metadata={'hnsw:space':'cosine'})
    nlp = spacy.load("en_core_web_sm")
    app.run(debug=True)