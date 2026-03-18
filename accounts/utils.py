import numpy as np
import pdfplumber
import torch

import requests
import io
import re

import nltk
import os

os.environ["HF_HOME"] = "C:/hf_cache"
os.environ["TRANSFORMERS_CACHE"] = "C:/hf_cache/models"
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
    nltk.download('punkt_tab')
from nltk.tokenize import sent_tokenize, word_tokenize

from nltk.corpus import stopwords
nltk.download('stopwords')

from nltk.stem import PorterStemmer
stemmer = PorterStemmer()

from nltk.stem import WordNetLemmatizer
nltk.download('wordnet')
nltk.download('omw-1.4')
lemmatizer = WordNetLemmatizer()

from sklearn.feature_extraction.text import TfidfVectorizer

from transformers import PegasusTokenizer, PegasusForConditionalGeneration
import torch
# adjust based on CPU cores


MAX_PAGES = 40          # hard limit for PDF pages
MAX_WORDS = 10000      # max words processed
MAX_CHUNKS = 4       # max chunks summarized

def extract_text_from_pdf(pdf_url):
    response = requests.get(pdf_url, timeout=20)
    response.raise_for_status()

    pdf_bytes = io.BytesIO(response.content)
    text=""

    with pdfplumber.open(pdf_bytes) as pdf:
        for i, page in enumerate(pdf.pages):
            if i >= MAX_PAGES:
                break

            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

    return text

def clean_pdf_text(text):
    # convert to lowercase
    text = text.lower()

    # Remove enumeration junk
    text = re.sub(r'\(\s*[a-zA-Z0-9]\s*\)', ' ', text)
    text = re.sub(r'<[^>]+>', ' ', text)

    # remove citation patterns
    text = re.sub(r'\[\d+\]', ' ', text)
    text = re.sub(r'\([A-Za-z]+,\s*\d{4}\)', ' ', text)
   # remove bullet symbols
    text = re.sub(r'[•▪●■►]', ' ', text)

    # remove page numbers
    text = re.sub(r'page\s*\d+', ' ', text, flags=re.IGNORECASE)
    # remove numbers
    text = re.sub(r'\d+', '', text)
    # remove hyphen line breaks
    text = re.sub(r'-\s+', '', text)
    # Merge broken lines
    text = re.sub(r'\n+', ' ', text)
    # Fix spaced hyphens
    text = re.sub(r"\s-\s", "-", text)
    # Fix spaced parentheses
    text = re.sub(r"\(\s+", "(", text)
    text = re.sub(r"\s+\)", ")", text)
    # Remove isolated punctuation
    text = re.sub(r'\s+[.,;:]\s+', ' ', text)

    # Remove <n> markers
    text = text.replace("<n>", " ")

    # Remove multiple spaces
    text = re.sub(r"\s+", " ", text)

    # remove dotted table of contents
    text = re.sub(r'\.{3,}', ' ', text)
    # remove section numbers
    text = re.sub(r'\b\d+\.\s*', ' ', text)

    text = re.sub(r'\.{2,}\s*\d*', ' ', text)
    return text.strip()

def sentence_tokenization(text):
    sentences = sent_tokenize(text)
    return sentences

def word_tokenization(text):
    words = word_tokenize(text)
    return words
def remove_stopwords(text):
    stop_words = set(stopwords.words("english"))
    words = word_tokenize(text)
    filtered_words = []

    for word in words:
        if word.lower() not in stop_words:
            filtered_words.append(word)
    return filtered_words

def apply_stemming(text):
    words = word_tokenize(text)
    stemmed_words = []
    for word in words:
        stemmed_words.append(stemmer.stem(word))
    return stemmed_words

def apply_lemmatization(text):
    words = word_tokenize(text)
    lemmas = []
    for word in words:
        lemmas.append(lemmatizer.lemmatize(word))
    return lemmas


def get_pdf_page_count(pdf_url):
    response = requests.get(pdf_url)
    response.raise_for_status()
    pdf_bytes = io.BytesIO(response.content)

    with pdfplumber.open(pdf_bytes) as pdf:
        return len(pdf.pages)


def calculate_target_words(page_count):
    # Academic heuristic
    min_words = 150
    max_words = 900

    target = page_count * 40  # 50 words per page
    return max(min_words, min(target, max_words))

def chunk_text_by_words(text, chunk_size=800):
    words = text.split()
    chunks = []

    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start = end

    return chunks




from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

def generate_adaptive_summary(text, num_sentences=3):
    sentences = [s.strip() for s in text.split(". ") if len(s.strip()) > 30]

    # SAFETY CHECK 1: no valid sentences
    if not sentences:
        return ""
    vectorizer = TfidfVectorizer(stop_words="english")
    try:
        tfidf = vectorizer.fit_transform(sentences)
    except ValueError:
        return sentences[0] + "."
    scores = tfidf.sum(axis=1).A1
    ranked = np.argsort(scores)[::-1]
    selected = [sentences[i] for i in ranked[:num_sentences]]
    paragraphs = []
    for s in selected:
        paragraphs.append(s.strip() + ".")

    return "\n\n".join(paragraphs)



def generate_topics(text):
    vectorizer = TfidfVectorizer(stop_words="english", max_features=15)
    X = vectorizer.fit_transform([text])
    return "\n".join(f"• {w}" for w in vectorizer.get_feature_names_out())


def generate_exam_questions(text):
    sentences = sent_tokenize(text)
    questions = []

    for s in sentences[:10]:
        if len(s.split()) > 8:
            questions.append(f"• Explain: {s}")

    return "\n".join(questions)


def is_pdf_truncated(actual_pages):
    return actual_pages > MAX_PAGES
def trim_text_by_words(text, max_words=25000):
    words = text.split()
    if len(words) <= max_words:
        return text
    return " ".join(words[:max_words])

def is_bad_extraction(text):
    if not text:
        return True

    junk_ratio = sum(1 for c in text if not c.isalnum() and c not in " .,;:\n") / max(len(text), 1)

    # Too many symbols / broken tokens
    if junk_ratio > 0.25:
        return True

    # Too many short fragments
    words = text.split()
    if len(words) > 0 and sum(1 for w in words if len(w) <= 2) / len(words) > 0.4:
        return True

    return False
def merge_short_pages(pages, min_words=20):
    merged_pages = []
    skip_next = False

    for i in range(len(pages)):
        if skip_next:
            skip_next = False
            continue

        current_page = pages[i]
        word_count = len(current_page.split())

        # If page is short and next page exists, merge forward
        if word_count <= min_words and i + 1 < len(pages):
            combined = current_page + " " + pages[i + 1]
            merged_pages.append(combined)
            skip_next = True
        else:
            merged_pages.append(current_page)

    return merged_pages
def generate_page_wise_summary(pdf_url, sentences_per_page=3):
    # Step 1: extract page-wise text
    pages = extract_text_from_pdf(pdf_url)

    if not pages:
        return "No readable content found in PDF."

    # Step 2: merge very short pages forward
    pages = merge_short_pages(pages, min_words=20)

    output = []
    page_number = 1

    for page_text in pages:
        if is_bad_extraction(page_text):
            continue

        summary = generate_adaptive_summary(
            page_text,
            num_sentences=sentences_per_page
        )

        if summary.strip():
            output.append(
                f"{summary}"
            )

    return "\n".join(output)

