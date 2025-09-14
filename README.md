# 🏢 MNC Agent Hub

**A Modern Enterprise Document Management System with AI-Powered Intelligence**

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/python-3.7+-blue.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg?style=for-the-badge)](LICENSE)

## 📖 Overview

MNC Agent Hub is a clean, professional document management system designed for enterprises. It provides a unified platform for employees to access company documents, search content with AI assistance, and for administrators to manage the document ecosystem with real-time analytics.

### 🌟 Key Features

- **🔐 Dual Access System**: Separate Employee and Admin portals
- **🤖 AI Integration**: Local LLM integration with Ollama (DeepSeek Coder 6.7B)
- **📊 Real-time Analytics**: Live dashboard with auto-refresh capabilities
- **🔍 Smart Search**: AI-powered document search with relevance scoring
- **📄 Document Summarization**: Configurable AI-generated summaries
- **💬 Q&A System**: Context-aware question answering from documents
- **📈 Employee Tracking**: Activity monitoring and analytics
- **📋 CSV Export**: Query history and analytics export
- **📱 Responsive Design**: Mobile-friendly interface
- **🎨 Clean UI**: Professional styling with no visual clutter

## 🛠️ Technology Stack

### Backend
- **FastAPI**: High-performance Python web framework
- **Uvicorn**: ASGI server for production deployment
- **Pydantic**: Data validation and settings management
- **Requests**: HTTP library for AI service integration

### AI Integration
- **Ollama**: Local LLM deployment platform
- **DeepSeek Coder 6.7B**: Code-focused language model for document processing
- **MCP (Model Context Protocol)**: Standardized AI model integration

### Frontend
- **HTML5/CSS3**: Modern web standards
- **Vanilla JavaScript**: No framework dependencies
- **Responsive Design**: Mobile-first approach

### Features Integration
- **File Upload**: Drag & drop document upload
- **Auto-tagging**: AI-powered document categorization
- **Live Dashboard**: Real-time statistics and monitoring
- **Real-time Updates**: Auto-refresh every 10-25 seconds

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- Git
- Ollama (optional, for AI features)

### Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/Kenway45/MNC-Agent-Hub.git
   cd MNC-Agent-Hub
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the Agent Hub**
   ```bash
   ./Agent_Hub.sh
   ```

4. **Access the System**
   - Open your browser to: `http://localhost:8888`
   - Choose **Employee Access** or **Admin Access**

### AI Setup (Optional)

For full AI capabilities, install Ollama:

```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Pull the DeepSeek Coder model
ollama pull deepseek-coder:6.7b

# Start Ollama service
ollama serve
```

## 📁 Project Structure

```
MNC_Agent_HUB/
├── 🚀 Agent_Hub.sh          # Main startup script
├── ⚡ app.py                # FastAPI application core
├── 🔧 admin_endpoints.py    # Admin API endpoints
├── 📊 admin_dashboard.py    # Admin dashboard HTML/JS
├── 📦 requirements.txt      # Python dependencies
├── 📖 README.md            # This documentation
└── 🗂️  .git/               # Git repository data
```

## 🎯 Usage Guide

### Employee Portal (Green Theme)

1. **Access**: Choose "Employee Access" on the main page
2. **Login**: Enter your Employee ID (e.g., `emp_001`)
3. **Features Available**:
   - 📚 Browse all company documents
   - 🔍 Search documents with AI-powered relevance
   - 📄 Generate AI summaries (configurable length)
   - 💬 Ask questions about document content
   - 📋 View personal activity history

### Admin Dashboard (Blue Theme)

1. **Access**: Choose "Admin Access" on the main page
2. **Features Available**:
   - 📤 Upload new documents (drag & drop supported)
   - 🏷️ AI-powered auto-tagging
   - 📊 Real-time system statistics
   - 👥 Employee activity monitoring
   - 📈 Analytics and reporting
   - 📋 CSV export capabilities
   - 🔄 Live data refresh (auto-updates every 10-25 seconds)

## 🎨 Design Philosophy

### Color Scheme
- **Employee Interface**: Green (#4CAF50) - Representing growth and accessibility
- **Admin Interface**: Blue (#2196F3) - Representing trust and management
- **Backgrounds**: Clean whites and light grays
- **Text**: Professional dark grays (#333)

### UI Principles
- **Minimalist**: Clean, distraction-free interface
- **Professional**: Business-appropriate styling
- **Responsive**: Works on desktop, tablet, and mobile
- **Accessible**: High contrast ratios and semantic HTML

## 🔧 API Documentation

### Core Endpoints

#### Employee Endpoints
- `GET /` - Main hub page
- `GET /employee/{employee_id}` - Employee portal
- `GET /documents` - List all documents
- `POST /employee/query` - Search and question endpoints
- `GET /employee/{employee_id}/history` - Activity history

#### Admin Endpoints
- `GET /admin` - Admin dashboard
- `POST /admin/upload-document` - Document upload
- `GET /admin/stats` - System statistics
- `GET /admin/documents` - Document management
- `GET /admin/employee-stats` - Employee analytics
- `GET /admin/query-history` - Query history with filters
- `GET /admin/analytics` - Advanced analytics

#### AI Endpoints
- `GET /summarize/{doc_id}` - Generate document summaries
- Integration with Ollama API for LLM capabilities

## 🤖 AI Integration Details

### MCP (Model Context Protocol) Integration

The system uses MCP standards for AI model integration, providing:
- **Standardized Communication**: Consistent API interface with AI models
- **Context Management**: Proper context passing for document-based queries
- **Model Flexibility**: Easy switching between different LLM providers
- **Error Handling**: Graceful degradation when AI services are unavailable

### AI Features Implementation

1. **Document Summarization**
   - Configurable summary length (2, 3, or 5 sentences)
   - Context-aware summaries using full document content
   - JSON-structured responses with key points extraction

2. **Question Answering**
   - Context injection from relevant documents
   - Natural language processing for user queries
   - Source attribution and confidence scoring

3. **Auto-tagging**
   - Keyword-based intelligent categorization
   - Content analysis for tag generation
   - Fallback mechanisms for edge cases

## 📊 Analytics & Monitoring

### Real-time Metrics
- Total documents in system
- Active employee count
- Query volume (total and daily)
- Peak usage patterns

### Employee Analytics
- Individual activity tracking
- Query type distribution
- Document interaction patterns
- Usage frequency analysis

### System Health
- Auto-refresh capabilities
- Error tracking and logging
- Performance monitoring
- Data export functionality

## 🔒 Security Features

- **Input Validation**: Pydantic models for all data validation
- **Error Handling**: Comprehensive exception management
- **Local Processing**: AI processing can be done entirely locally
- **No External Dependencies**: Core functionality works without internet
- **Activity Logging**: Complete audit trail of all operations

## 🚀 Deployment

### Development
```bash
./Agent_Hub.sh
```

### Production
```bash
# Using Uvicorn directly
uvicorn app:app --host 0.0.0.0 --port 8888 --workers 4

# Or with Gunicorn
gunicorn app:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8888
```

### Docker (Coming Soon)
```dockerfile
# Dockerfile will be added for containerized deployment
FROM python:3.11-slim
# ... deployment configuration
```

## 🧪 Testing

### Manual Testing Scripts

1. **Employee Flow Test**
   ```bash
   # Start system
   ./Agent_Hub.sh
   
   # Test employee portal
   # 1. Go to http://localhost:8888
   # 2. Choose "Employee Access"
   # 3. Enter ID: emp_001
   # 4. Test all features
   ```

2. **Admin Flow Test**
   ```bash
   # Test admin dashboard
   # 1. Go to http://localhost:8888
   # 2. Choose "Admin Access" 
   # 3. Upload test document
   # 4. Check all analytics tabs
   # 5. Export CSV data
   ```

### Sample Data
The system includes sample documents for immediate testing:
- Employee Handbook
- IT Security Policy
- Remote Work Guidelines

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 Python style guide
- Write comprehensive docstrings
- Add tests for new features
- Update documentation as needed

## 📋 Roadmap

### Version 2.0 (Planned)
- [ ] User authentication and role management
- [ ] Advanced PDF/Word document parsing
- [ ] Integration with external document stores (SharePoint, Google Drive)
- [ ] WebSocket real-time updates
- [ ] Advanced analytics dashboard
- [ ] Mobile app development
- [ ] Multi-language support

### Version 1.5 (In Progress)
- [ ] Docker containerization
- [ ] Automated testing suite
- [ ] API documentation with Swagger
- [ ] Performance optimization
- [ ] Enhanced error handling

## 🐛 Known Issues

- PDF/Word file parsing is placeholder implementation
- AI service requires manual Ollama setup
- No user authentication (single-tenant design)
- Limited to in-memory data storage

## 📞 Support

For support and questions:
- **GitHub Issues**: [Create an issue](https://github.com/Kenway45/MNC-Agent-Hub/issues)
- **Documentation**: Check this README
- **Email**: Contact through GitHub

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **FastAPI Team**: For the excellent web framework
- **Ollama Project**: For making local LLM deployment accessible
- **DeepSeek**: For the high-quality code-focused language model
- **MCP Standards**: For standardized AI integration protocols

## 📈 Project Stats

![GitHub stars](https://img.shields.io/github/stars/Kenway45/MNC-Agent-Hub)
![GitHub forks](https://img.shields.io/github/forks/Kenway45/MNC-Agent-Hub)
![GitHub issues](https://img.shields.io/github/issues/Kenway45/MNC-Agent-Hub)

---

**Built with ❤️ for modern enterprises seeking intelligent document management solutions.**

## 🖼️ Screenshots

### Main Hub Selection
Clean interface allowing users to choose between Employee and Admin access.

### Employee Portal
Professional green-themed interface for document access and AI assistance.

### Admin Dashboard
Comprehensive blue-themed dashboard for system management and analytics.

---

**Ready to revolutionize your document management? Get started in under 5 minutes!** 🚀