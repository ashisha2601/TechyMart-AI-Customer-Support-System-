# 🤖 TechyMart Customer Support AI Agent

A friendly and intelligent customer support chatbot for TechyMart online shop.

## Features

- 📚 **FAQ Answering**: Uses RAG (Retrieval-Augmented Generation) to answer questions about policies
- 📦 **Order Tracking**: Simulated order status lookup with agentic actions
- 🤝 **Smart Escalation**: Politely escalates complex queries to human agents
- 🎭 **Friendly Personality**: Engaging and humorous responses with emojis

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up environment variables:
   ```bash
   cp .env.example .env
   # Add your OpenAI API key to .env
   ```

3. Run the application:
   ```bash
   python main.py
   ```

4. Open your browser to `http://localhost:8000`

## Usage

- Ask about delivery, returns, warranty policies
- Check order status: "Where's my order #1234?"
- The bot will escalate complex queries to human agents

Enjoy chatting with your friendly TechyMart assistant! 🛒✨
