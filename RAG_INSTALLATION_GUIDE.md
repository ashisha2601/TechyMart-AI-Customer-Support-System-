# RAG System Installation Guide

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Start the Server
```bash
python advanced_main.py
```

### 3. Access the Interfaces
- **RAG Interface**: http://localhost:8000/rag
- **Premium Interface**: http://localhost:8000
- **Classic Interface**: http://localhost:8000/classic
- **API Documentation**: http://localhost:8000/docs

## Detailed Installation

### Prerequisites
- Python 3.8+
- pip package manager

### Step 1: Install Core Dependencies
```bash
# Install all dependencies from requirements.txt
pip install -r requirements.txt
```

### Step 2: Optional - Install Additional Dependencies
If you encounter import errors, install these packages individually:

```bash
# For document processing
pip install python-docx pypdf markdown beautifulsoup4

# For vector operations
pip install faiss-cpu numpy

# For LangChain and LangGraph
pip install langchain langchain-community langchain-openai langchain-huggingface langgraph

# For sentence transformers
pip install sentence-transformers

# For Pinecone (optional)
pip install pinecone-client

# For additional features
pip install tiktoken
```

### Step 3: Environment Variables (Optional)
Create a `.env` file for API keys:

```bash
# Optional: OpenAI API Key for enhanced responses
OPENAI_API_KEY=your_openai_api_key_here

# Optional: Pinecone configuration
PINECONE_API_KEY=your_pinecone_api_key_here
PINECONE_ENVIRONMENT=your_pinecone_environment_here
```

### Step 4: Test the Installation
```bash
python test_rag_system.py
```

## Troubleshooting

### Common Issues

#### 1. Import Errors
**Error**: `Import "langchain" could not be resolved`

**Solution**: Install the missing package:
```bash
pip install langchain
```

#### 2. FAISS Installation Issues
**Error**: `Import "faiss" could not be resolved`

**Solution**: Install FAISS CPU version:
```bash
pip install faiss-cpu
```

#### 3. Sentence Transformers Issues
**Error**: `Import "sentence_transformers" could not be resolved`

**Solution**: Install sentence transformers:
```bash
pip install sentence-transformers
```

#### 4. Memory Issues
**Error**: Out of memory when loading models

**Solution**: Use smaller models or increase system memory:
```python
# In rag_vector_store.py, change the model
rag_vector_store = RAGVectorStore(embedding_model="all-MiniLM-L6-v2")
```

### Platform-Specific Issues

#### Windows
- Install Microsoft Visual C++ Build Tools
- Use `pip install --upgrade pip` before installing packages

#### macOS
- Install Xcode command line tools: `xcode-select --install`
- Use `pip3` instead of `pip` if needed

#### Linux
- Install build essentials: `sudo apt-get install build-essential`
- Install Python development headers: `sudo apt-get install python3-dev`

## Verification

### 1. Run the Test Suite
```bash
python test_rag_system.py
```

Expected output:
```
🧪 Testing RAG System Components...
✅ Ingested X FAQ documents
✅ Created X sample documents
✅ Documents added to vector store
✅ Similarity search returned X results
✅ LangChain query processing works
✅ Conversation memory works
✅ Enhanced RAG chatbot works
🎉 All tests passed! RAG system is working correctly.
```

### 2. Test the Web Interface
1. Start the server: `python advanced_main.py`
2. Open http://localhost:8000/rag
3. Try asking: "What is your return policy?"
4. Verify you get a response with sources and confidence score

### 3. Test API Endpoints
```bash
# Test RAG status
curl http://localhost:8000/rag/status

# Test RAG chat
curl -X POST http://localhost:8000/chat/rag \
  -d "message=What are your shipping options?" \
  -d "session_id=test"
```

## Performance Optimization

### For Development
- Use FAISS with CPU (default)
- Use smaller embedding models
- Limit conversation memory size

### For Production
- Use Pinecone for vector storage
- Use GPU-accelerated models
- Implement conversation persistence
- Add caching layers

## Next Steps

1. **Customize Knowledge Base**: Add your own documents to the knowledge base
2. **Configure Models**: Adjust embedding models and LLM settings
3. **Add Authentication**: Implement user authentication for production
4. **Monitor Performance**: Set up logging and monitoring
5. **Scale Up**: Deploy to cloud infrastructure

## Support

If you encounter issues:

1. Check the troubleshooting section above
2. Run the test suite to identify specific problems
3. Check the logs for detailed error messages
4. Ensure all dependencies are properly installed
5. Verify your Python version (3.8+)

## Additional Resources

- [RAG System Documentation](RAG_SYSTEM_DOCUMENTATION.md)
- [API Documentation](http://localhost:8000/docs)
- [Feature Demo](http://localhost:8000/demo/features)
- [RAG Analytics](http://localhost:8000/rag/analytics)
