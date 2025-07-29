import streamlit as st
import nltk
import speech_recognition as sr
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import string
from nltk.stem import WordNetLemmatizer


with open(r"C:\Users\batta\Desktop\DL_NN_checkpoint\ww2.txt") as file:
    text = file.read().replace('\n', " ")

sentences = sent_tokenize(text)

def preprocessing(sentence):
    word = word_tokenize(sentence)
    stop_words = set(stopwords.words("english"))
    new_list = [i.lower() for i in word if i.lower() not in stop_words and i not in string.punctuation]
    lemmatizer = WordNetLemmatizer()
    lem_list = [lemmatizer.lemmatize(i) for i in new_list ]
    return lem_list

corpus = [preprocessing(sentence) for sentence in sentences]

def speechReco():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        st.info("Speak now...")

        audio = recognizer.listen(source)
    try:
        st.info("Transcribing...")
        text = recognizer.recognize_google(audio)  
        return text
    except:
        return "Error : Sorry, I couldn't get what you said"

def get_most_relevant_sentence(query):
    query_list = preprocessing(query)
    max_similarity = 0
    relevant_sentence = ""

    for i in corpus:
        intersection = set(query_list).intersection(set(i))
        union = set(query_list).union(set(i))
        similarity = len(intersection) / len(union)
        if similarity > max_similarity:
            max_similarity = similarity
            relevant_sentence = " ".join(i)
    return relevant_sentence
    
def chatbot(question):
    return get_most_relevant_sentence(question)

def main():
    st.title("speech-enabled chatbot")
    var = st.selectbox("Choose the mode:", options=["text", "audio"])

    if var == "text":
        input_text = st.text_input("Enter your question")
        if st.button("submit"):
            response = chatbot(input_text)
            st.success(response)

    else:  
        if st.button("Speak and submit"):
            input_audio = speechReco()
            response = chatbot(input_audio)
            st.success(response)


if __name__ == "__main__":
    main()
