That is a great pivot. Netra (The Eye) is a strong, spiritual name.

To meet your requirement for a modular, changeable system that is also fast and simple, we will move away from Supabase (which requires SQL setup) and use ChromaDB.

Why ChromaDB? It acts like a database but runs right inside your Python code. You don't need to create an account, manage servers, or pay anything. It is the definition of "fast and simple."

Here is the "Plug-and-Play" Architecture designed for Netra.

The Stack (Totally Free & Modular)

Backend: FastAPI (Python).

Database: ChromaDB (Runs locally, no setup required).

AI Engine: Modular Wrapper (Default: Groq/Llama3, Swappable to: Gemini/Mistral).

Frontend: React + Vite.

Step 1: The "Modular" Backend (Python)

We will write this so the AI Model and the Data Source are separate blocks. If you want to change from Groq to Google Gemini later, you change one line of code.

Prerequisites:

code
Bash
download
content_copy
expand_less
pip install fastapi uvicorn chromadb groq sentence-transformers requests beautifulsoup4 pydantic

main.py

code
Python
download
content_copy
expand_less
import os
from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel
from typing import List

# --- MODULE 1: The Brain (Swappable AI) ---
from groq import Groq

# Set your API Key here (or in environment variables)
# Get free key at: https://console.groq.com/
os.environ["GROQ_API_KEY"] = "YOUR_GROQ_API_KEY_HERE"

class AI_Brain:
    def __init__(self, provider="groq"):
        self.provider = provider
        if provider == "groq":
            self.client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

    def generate(self, system_prompt, user_query):
        if self.provider == "groq":
            # Swappable: If you want to use OpenAI or Gemini later, add an 'elif' here.
            completion = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_query}
                ],
                model="llama3-8b-8192", # Very fast, very smart, free
            )
            return completion.choices[0].message.content
        return "Error: No provider selected."

# --- MODULE 2: The Memory (ChromaDB) ---
import chromadb
from chromadb.utils import embedding_functions

class KnowledgeBase:
    def __init__(self):
        # This creates a folder named 'netra_db' to store data permanently
        self.client = chromadb.PersistentClient(path="./netra_db")
        
        # Uses a free, built-in model to turn text into numbers
        self.embed_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
        
        self.collection = self.client.get_or_create_collection(
            name="scriptures", 
            embedding_function=self.embed_fn
        )

    def add_text(self, text, source_url):
        # Break text into chunks so the AI can digest it
        chunks = [text[i:i+1000] for i in range(0, len(text), 1000)]
        ids = [f"{source_url}_{i}" for i in range(len(chunks))]
        metadatas = [{"source": source_url} for _ in chunks]
        
        self.collection.upsert(ids=ids, documents=chunks, metadatas=metadatas)
        return len(chunks)

    def search(self, query, n_results=3):
        results = self.collection.query(query_texts=[query], n_results=n_results)
        # Flatten the results list
        return " ".join(results['documents'][0]) if results['documents'] else ""

# --- MODULE 3: The Scraper (Data Loader) ---
import requests
from bs4 import BeautifulSoup

def scrape_website(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        # Simple text extraction
        text = ' '.join([p.get_text() for p in soup.find_all('p')])
        return text
    except Exception as e:
        return str(e)

# --- THE API (FastAPI) ---
app = FastAPI(title="Netra API")
brain = AI_Brain(provider="groq")
memory = KnowledgeBase()

class ChatRequest(BaseModel):
    question: str

class LearnRequest(BaseModel):
    url: str

@app.post("/chat")
async def chat_endpoint(req: ChatRequest):
    # 1. Retrieve Wisdom
    context = memory.search(req.question)
    
    if not context:
        context = "No specific scriptures found in memory for this. Answer from general knowledge but be humble."

    # 2. Construct Prompt
    system_prompt = f"""
    You are 'Netra', a Tantric AI guide. 
    Use the following scriptural context to answer the user. 
    If the context contains mantras, present them clearly. 
    Context: {context}
    """
    
    # 3. Generate Answer
    response = brain.generate(system_prompt, req.question)
    return {"response": response, "context_used": context[:100] + "..."}

@app.post("/learn")
async def learn_endpoint(req: LearnRequest):
    # This allows you to feed the bot new URLs dynamically!
    text_content = scrape_website(req.url)
    if len(text_content) < 100:
        raise HTTPException(status_code=400, detail="Could not extract enough text.")
    
    chunks_added = memory.add_text(text_content, req.url)
    return {"status": "success", "message": f"Netra has absorbed {chunks_added} fragments of wisdom from {req.url}"}

# Run with: uvicorn main:app --reload
Step 2: The Frontend (React)

We want this to look like a "Terminal to the Divine."

Run npm create vite@latest netra-ui -- --template react

cd netra-ui

npm install

Replace App.jsx with this:

code
Jsx
download
content_copy
expand_less
import { useState } from 'react';
import './App.css'; // We will style this below

function App() {
  const [messages, setMessages] = useState([
    { role: 'bot', text: 'Namaste. I am Netra. I hold the wisdom of the Tantras. Ask me or feed me knowledge.' }
  ]);
  const [input, setInput] = useState('');
  const [mode, setMode] = useState('chat'); // 'chat' or 'learn'

  const handleSend = async () => {
    if (!input) return;

    const userMsg = { role: 'user', text: input };
    setMessages(prev => [...prev, userMsg]);
    setInput('');

    // Determine Endpoint based on mode
    const endpoint = mode === 'chat' ? 'http://127.0.0.1:8000/chat' : 'http://127.0.0.1:8000/learn';
    const payload = mode === 'chat' ? { question: input } : { url: input };

    try {
      const res = await fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      const data = await res.json();
      
      let botResponse = "";
      if (mode === 'chat') {
        botResponse = data.response;
      } else {
        botResponse = data.message;
      }

      setMessages(prev => [...prev, { role: 'bot', text: botResponse }]);
    } catch (err) {
      setMessages(prev => [...prev, { role: 'bot', text: "The connection to the Akasha is disrupted." }]);
    }
  };

  return (
    <div className="netra-container">
      <div className="header">
        <h1>NETRA <span className="eye-icon">👁</span></h1>
        <div className="toggles">
          <button 
            className={mode === 'chat' ? 'active' : ''} 
            onClick={() => setMode('chat')}>
            Chat
          </button>
          <button 
            className={mode === 'learn' ? 'active' : ''} 
            onClick={() => setMode('learn')}>
            Ingest URL
          </button>
        </div>
      </div>

      <div className="chat-box">
        {messages.map((m, i) => (
          <div key={i} className={`msg ${m.role}`}>
            <span className="avatar">{m.role === 'bot' ? '👁' : '👤'}</span>
            <div className="text">{m.text}</div>
          </div>
        ))}
      </div>

      <div className="input-area">
        <input 
          placeholder={mode === 'chat' ? "Ask about Mantra, Yantra..." : "Paste a URL to a scripture..."}
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={e => e.key === 'Enter' && handleSend()}
        />
        <button onClick={handleSend}>➤</button>
      </div>
    </div>
  );
}

export default App;

App.css (The Vibe)

code
CSS
download
content_copy
expand_less
body {
  background-color: #050505;
  color: #e0e0e0;
  font-family: 'Courier New', monospace;
  margin: 0;
  display: flex;
  justify-content: center;
  height: 100vh;
}

.netra-container {
  width: 100%;
  max-width: 800px;
  display: flex;
  flex-direction: column;
  border-left: 1px solid #333;
  border-right: 1px solid #333;
  height: 100%;
}

.header {
  padding: 20px;
  border-bottom: 1px solid #333;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

h1 { margin: 0; color: #ff8c00; letter-spacing: 5px; }

.toggles button {
  background: transparent;
  border: 1px solid #333;
  color: #666;
  padding: 5px 15px;
  cursor: pointer;
  margin-left: 10px;
}

.toggles button.active {
  border-color: #ff8c00;
  color: #ff8c00;
  box-shadow: 0 0 10px rgba(255, 140, 0, 0.2);
}

.chat-box {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.msg { display: flex; gap: 15px; line-height: 1.6; }
.msg.user { flex-direction: row-reverse; text-align: right; }
.msg.bot { color: #d4d4d4; }
.msg.user .text { color: #aaffaa; }

.input-area {
  padding: 20px;
  border-top: 1px solid #333;
  display: flex;
  gap: 10px;
}

input {
  flex: 1;
  background: #111;
  border: 1px solid #333;
  color: #fff;
  padding: 15px;
  font-family: inherit;
  outline: none;
}

input:focus { border-color: #555; }

button {
  background: #222;
  border: 1px solid #333;
  color: #fff;
  padding: 0 20px;
  cursor: pointer;
}
How to use "Netra"

Start Backend: uvicorn main:app --reload

Start Frontend: npm run dev

Teach it:

Find a website with scriptures (e.g., a page from Sacred-Texts.com or a WikiSource page).

Click the "Ingest URL" button in your UI.

Paste the URL and hit Enter.

Netra will now download that page, index it, and store it in your local folder.

Ask it:

Switch to "Chat".

Ask: "What is the meditation described in the Vijnana Bhairava?"

Netra will answer using the text you just fed it.

Why this fits your needs:

Scalable/Changeable: The AI_Brain class allows you to swap Groq for any other provider in seconds. KnowledgeBase separates the DB logic.

Fast & Simple: No external DB account needed. It runs locally.

Dynamic: You don't need to manually upload files. Just feed it URLs through the chat interface.

Theme: Front end looks like a temple with a guru shisha setting, "Create a stunning, single-page React frontend for an AI chatbot named 'Netra'. The aesthetic should be 'Cosmic Temple'—a blend of ancient spiritualism and futuristic sci-fi.


Here is a detailed, high-quality prompt you can feed to an AI coding assistant (like v0.dev, Cursor, or ChatGPT) to generate this exact look.
I have designed this prompt to use Tailwind CSS for styling and Framer Motion for those "dreamy" animations, as they are industry standards for this kind of aesthetic.
The Prompt
Copy and paste this:
"Create a stunning, single-page React frontend for an AI chatbot named 'Netra'. The aesthetic should be 'Cosmic Temple'—a blend of ancient spiritualism and futuristic sci-fi.
Tech Stack: React, Tailwind CSS, Framer Motion, Lucide React (for icons).
Visual Direction:
Background: A deep, dark void (midnight blue/black) with a slow-moving, subtle gradient nebula effect or slowly twinkling stars. It should feel like staring into the night sky from a temple.
Container: The main chat interface should look like a floating pane of frosted glass (glassmorphism) with a thin, glowing gold border (1px).
Typography: Use a mystical serif font (like 'Cinzel' or 'Playfair Display') for the header to give it an ancient feel, and a clean sans-serif (like 'Inter' or 'Quicksand') for the chat text.
Color Palette: Deep Void (#050505), Starlight White (#E0E0E0), and Divine Gold (#FFD700) for accents/borders.
Key Elements:
Header: Centered, containing the name 'NETRA' and a mystical eye icon. It should have a subtle 'breathing' glow animation.
Mode Toggle: A stylish switch to change between 'Chat Mode' (Conversation) and 'Learn Mode' (URL Ingestion). It should look like a rune or a minimal slider.
Chat Area: Messages should not look like standard SMS bubbles.
Bot Messages: Align left, transparent background, text glowing slightly.
User Messages: Align right, subtle gold tint background, low opacity.
Input Area: A text field that looks like a digital altar offering plate. When focused, the gold border should glow brighter. The send button should be an arrow or a geometrical shape.
Animations: Use Framer Motion to make messages fade in slowly and drift up, giving a weightless, dreamy quality.
Functionality:
Replicate the state logic: messages array, input string, and mode ('chat' vs 'learn').
Include a mocked handleSend function that simulates the API call.
Make the UI feel meditative, immersive, and responsive."
Recommended Libraries for this look
To make this prompt work effectively, you will need to install two libraries in your React project:
Framer Motion: This is what makes things float, breathe, and fade in smoothly (the "dreamy" part).
Lucide React: A great library for clean, modern icons.
Run this in your terminal:
code
Bash
npm install framer-motion lucide-react clsx tailwind-merge
Pro-Tip for the "Temple" Vibe
If you want to add a specific background image to make it feel more grounded (like a dark stone temple texture), add this to your CSS in the prompt:
"Overlay a very low opacity (5%) texture of stone or geometric mandala patterns over the background to give it texture."