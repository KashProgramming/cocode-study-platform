from transformers import pipeline
from nltk.tokenize import sent_tokenize
summarizer=pipeline("summarization",model="sshleifer/distilbart-cnn-12-6",revision="a4f8f3e",device=-1)
def chunk_text(text,max_words=300):
    sentences=sent_tokenize(text)
    chunks=[]
    current_chunk=[]
    current_length=0
    for sentence in sentences:
        words=sentence.split()
        if current_length+len(words)<=max_words:
            current_chunk.append(sentence)
            current_length+=len(words)
        else:
            chunks.append(" ".join(current_chunk))
            current_chunk=[sentence]
            current_length=len(words)
    if current_chunk:
        chunks.append(" ".join(current_chunk))
    return chunks
def summarize_content(text_list,max_length=150):
    full_text=" ".join(text_list)
    chunks=chunk_text(full_text,max_words=300)
    summaries=[summarizer(chunk,max_length=max_length,min_length=50,do_sample=False)[0]["summary_text"] for chunk in chunks]
    return summaries