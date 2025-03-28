import os
import openai
from dotenv import load_dotenv #To load environment variables from a .env file
from nltk.tokenize import word_tokenize #Natural Language Toolkit for text processing (tokenization, stopwords)
from nltk.corpus import stopwords
import numpy as np
from PyPDF2 import PdfReader 
from pylatex import Document, Section, Command #o modify LaTeX documents (the resume)
import re #Regular expressions(used to clean the text)
import nltk #Natural Language Toolkit
nltk.download('punkt') #Download the Punkt tokenizer
nltk.download('stopwords') #Download the stopwords

# Load OpenAI API key
load_dotenv()
openai.api_key = os.getenv("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")

class ResumeProcessor: #Initializes the class with English stopwords (common words like "the", "and" that are filtered out).
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        
    def extract_text_from_pdf(self, pdf_path): #Reads a PDF file (job description) and extracts all text, joining pages with spaces.
        """Extract text from PDF job descriptions"""
        with open(pdf_path, "rb") as f:
            reader = PdfReader(f)
            text = " ".join([page.extract_text() for page in reader.pages])
        return text
    
    def preprocess_text(self, text):
        """Clean and tokenize text"""
        text = text.lower()
        text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
        tokens = word_tokenize(text)
        return [word for word in tokens if word not in self.stop_words and len(word) > 2]
    
    def get_embeddings(self, text):
        """Get OpenAI embeddings for text"""
        response = openai.embeddings.create(
            input=text,
            model="text-embedding-3-small"
        )
        return response.data[0].embedding
    #Converts text into a numerical vector representation (embedding) using OpenAI's API.
    
    def calculate_similarity(self, vec1, vec2):
        """Cosine similarity between two vectors"""
        return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
    
    def extract_key_skills(self, job_desc_text, num_skills=10): #Purpose: Extracts the most frequently mentioned skills from a job description.


        """Identify most important skills from job description"""
        tokens = self.preprocess_text(job_desc_text)
        freq_dist = nltk.FreqDist(tokens)
        return [word for word, _ in freq_dist.most_common(num_skills)]
    
    def modify_latex_resume(self, latex_path, key_skills):
        """Update LaTeX resume to highlight key skills"""
        with open(latex_path, 'r') as f:
            content = f.read()
        
        # Add skills section if not exists
        if "\\section{Key Skills}" not in content:
            skills_section = "\\section{Key Skills}\n" + ", ".join(key_skills) + "\n"
            content = content.replace("\\begin{document}", "\\begin{document}\n" + skills_section)
        
        # Highlight skills in experience section
        for skill in key_skills:
            content = content.replace(skill, f"\\textbf{{{skill}}}")
        
        return content