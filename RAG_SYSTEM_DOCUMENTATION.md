# RAG-Enhanced Customer Support Chatbot

## Overview

This project implements a comprehensive RAG (Retrieval-Augmented Generation) system for customer support, integrating with the existing TechyMart chatbot infrastructure. The system provides advanced semantic search, conversation memory, and context-aware responses using modern AI technologies.

## Architecture

### Core Components

1. **Data Ingestion Pipeline** (`rag_data_ingestion.py`)
   - Handles ingestion of FAQs, documents, product manuals
   - Supports multiple file formats (PDF, DOCX, Markdown, TXT)
   - Chunks documents for optimal retrieval
   - Creates LangChain Document objects

2. **Vector Store** (`rag_vector_store.py`)
   - FAISS and Pinecone support
   - Hugging Face sentence-transformers embeddings
   - Similarity search with configurable thresholds
   - Document storage and retrieval

3. **LangChain Integration** (`rag_langchain_integration.py`)
   - Query processing with LangChain
   - Response generation using OpenAI/Hugging Face models
   - Tool integration for enhanced capabilities
   - Agent-based conversation handling

4. **Conversation Memory** (`rag_conversation_memory.py`)
   - LangGraph-powered state management
   - Conversation history tracking
   - Intent detection and topic classification
   - Smart escalation logic

5. **Enhanced Chatbot** (`rag_enhanced_chatbot.py`)
   - Integrates all RAG components
   - Fallback mechanisms for reliability
   - Analytics and performance tracking
   - Multi-modal response generation

## Features

### RAG Capabilities
- **Semantic Search**: Advanced vector-based document retrieval
- **Context Enhancement**: Responses enriched with retrieved context
- **Multi-Source RAG**: Combines multiple knowledge sources
- **Conversation Memory**: LangGraph-powered state management
- **Intelligent Escalation**: Smart routing based on confidence and context

### Data Sources
- FAQ Database (existing)
- Product Manuals
- Policy Documents
- Technical Support Guides
- User-generated Content

### Vector Database Options
- **FAISS**: Local vector storage (default)
- **Pinecone**: Cloud-based vector database
- **ChromaDB**: Alternative local option

## Installation

### Prerequisites
```bash
pip install -r requirements.txt
```

### Environment Variables
```bash
# Optional: OpenAI API Key for enhanced responses
export OPENAI_API_KEY="your_openai_api_key"

# Optional: Pinecone configuration
export PINECONE_API_KEY="your_pinecone_api_key"
export PINECONE_ENVIRONMENT="your_pinecone_environment"
```

## Usage

### Starting the Server
```bash
python advanced_main.py
```

### Available Interfaces
- **Premium Interface**: http://localhost:8000
- **Classic Interface**: http://localhost:8000/classic
- **RAG Interface**: http://localhost:8000/rag
- **API Documentation**: http://localhost:8000/docs

### API Endpoints

#### Chat Endpoints
- `POST /chat/rag` - RAG-enhanced chat
- `POST /chat/advanced` - Advanced AI chat
- `POST /chat` - Classic chat

#### RAG Management
- `GET /rag/status` - RAG system status
- `GET /rag/analytics` - RAG analytics
- `POST /rag/clear-conversation` - Clear conversation memory
- `POST /rag/add-documents` - Add documents to knowledge base
- `GET /rag/conversation/{session_id}` - Get conversation history

## Configuration

### Vector Store Configuration
```python
# FAISS (default)
rag_vector_store = RAGVectorStore(
    embedding_model="all-MiniLM-L6-v2",
    vector_store_type="faiss"
)

# Pinecone
rag_vector_store = RAGVectorStore(
    embedding_model="all-MiniLM-L6-v2",
    vector_store_type="pinecone",
    pinecone_api_key="your_key",
    pinecone_environment="your_env"
)
```

### RAG System Configuration
```python
# Confidence thresholds
rag_enhanced_chatbot = RAGEnhancedChatbot()
rag_enhanced_chatbot.escalation_threshold = 0.3
rag_enhanced_chatbot.rag_confidence_threshold = 0.7
```

## Data Ingestion

### Adding New Documents
```python
from rag_data_ingestion import rag_data_ingestion

# Ingest a single file
documents = rag_data_ingestion.ingest_pdf_file("manual.pdf")

# Ingest a directory
documents = rag_data_ingestion.ingest_directory("./knowledge_base/")

# Add to vector store
rag_vector_store.add_documents(documents)
```

### Supported File Types
- PDF files (`.pdf`)
- Word documents (`.docx`)
- Markdown files (`.md`)
- Text files (`.txt`)

## Conversation Memory

### LangGraph State Management
The system uses LangGraph for advanced conversation state management:

```python
@dataclass
class ConversationState:
    messages: List[BaseMessage]
    current_query: str
    context_documents: List[Dict]
    response: str
    confidence: float
    escalated: bool
    session_id: str
    user_intent: str
    conversation_topic: str
```

### Intent Detection
- Greeting
- Order Inquiry
- Return Inquiry
- Product Inquiry
- Support Request
- General Inquiry

## Performance Optimization

### Caching
- Vector embeddings are cached
- Conversation states are stored in memory
- Document chunks are optimized for retrieval

### Scalability
- FAISS supports large-scale vector operations
- Pinecone provides cloud scalability
- Conversation memory can be persisted to database

## Monitoring and Analytics

### Metrics Tracked
- Total conversations
- RAG vs keyword responses
- Escalation rates
- Confidence scores
- Context usage
- Response times

### Analytics Endpoints
- `/rag/analytics` - Detailed RAG analytics
- `/analytics/global` - Global system analytics
- `/analytics/session/{session_id}` - Session-specific analytics

## Troubleshooting

### Common Issues

1. **RAG System Not Loading**
   - Check dependencies: `pip install -r requirements.txt`
   - Verify vector store initialization
   - Check logs for import errors

2. **Low Confidence Scores**
   - Adjust confidence thresholds
   - Add more relevant documents
   - Check embedding model quality

3. **Memory Issues**
   - Clear conversation memory regularly
   - Optimize document chunk sizes
   - Use Pinecone for large datasets

### Debug Mode
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Extending the System

### Adding New Data Sources
1. Create ingestion function in `rag_data_ingestion.py`
2. Add to supported file types
3. Update document metadata schema

### Custom Embedding Models
```python
from sentence_transformers import SentenceTransformer

# Use custom model
custom_model = SentenceTransformer('your-model-name')
rag_vector_store = RAGVectorStore(embedding_model='your-model-name')
```

### Custom Tools for LangChain
```python
from langchain.tools import Tool

custom_tool = Tool(
    name="custom_function",
    description="Description of what this tool does",
    func=your_custom_function
)
```

## Security Considerations

- API keys are stored in environment variables
- Conversation data is stored in memory (consider persistence for production)
- Input validation on all endpoints
- Rate limiting recommended for production

## Production Deployment

### Recommended Setup
1. Use Pinecone for vector storage
2. Implement conversation persistence
3. Add rate limiting and authentication
4. Set up monitoring and alerting
5. Use production-grade LLM services

### Environment Variables for Production
```bash
OPENAI_API_KEY=your_production_key
PINECONE_API_KEY=your_production_key
PINECONE_ENVIRONMENT=production
LOG_LEVEL=INFO
```

## Contributing

1. Follow the existing code structure
2. Add comprehensive tests
3. Update documentation
4. Ensure backward compatibility

## License

This project is part of the TechyMart Customer Support AI system.

## Support

For issues and questions:
- Check the troubleshooting section
- Review logs for error messages
- Create an issue with detailed information
