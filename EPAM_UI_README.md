# EPAM Business Intelligence Web UI

A comprehensive web-based interface for analyzing companies and generating EPAM consulting opportunity reports with downloadable Word documents.

## 🚀 Quick Start

### Option 1: Simple Launcher
```bash
python3 launch_epam_ui.py
```
This will automatically:
- Check dependencies
- Start the web server
- Open your browser to the application

### Option 2: Direct Launch
```bash
python3 epam_ui_app.py
```
Then visit: http://localhost:8080

## 📋 Prerequisites

### Required Python Packages
```bash
pip3 install flask python-docx --user
```

### System Components
The application uses the existing multi-agent system:
- `master_agent_chain.py` - Master orchestrator
- `agent_1_sec_filing_retriever.py` - SEC filings analysis
- `agent_2_strategic_opportunity_analyzer.py` - Strategic opportunities
- `agent_3_social_news_intelligence.py` - Social & news intelligence

## 🎯 Features

### 🔍 Company Analysis
- Enter any stock ticker symbol (NVDA, AAPL, MSFT, etc.)
- Comprehensive multi-agent analysis pipeline
- Real-time processing with progress indicators

### 📊 Intelligence Sources
- **SEC Filings**: 10-K and 10-Q document analysis
- **Strategic Analysis**: EPAM opportunity mapping
- **Social Intelligence**: Twitter/X mentions via Grok API
- **Executive Intelligence**: Leadership interviews via Perplexity API

### 📄 Word Report Generation
- Professional business reports in .docx format
- Comprehensive analysis results
- Executive summaries and recommendations
- Downloadable for presentations and client meetings

### 🔑 API Integration
- **Optional Grok API Key**: For real-time Twitter/X data
- **Optional Perplexity API Key**: For real-time news/interview data
- **Mock Data Fallback**: Works without API keys for testing

## 🖥️ User Interface

### Main Page
- Clean, professional interface
- Company ticker input with validation
- Optional API key configuration
- Quick example buttons for popular stocks
- Feature overview and system capabilities

### Results Page
- Executive summary dashboard
- Strategic opportunities breakdown
- Social media intelligence highlights
- Executive interview insights
- Engagement readiness assessment
- Recommended next steps
- **One-click Word document download**

## 📈 Analysis Output

### Strategic Opportunities
- Priority levels (HIGH, MEDIUM, LOW)
- Confidence scores (0.0 - 1.0)
- EPAM service mapping
- Evidence count and indicators

### Social Intelligence
- Twitter/X mentions with relevance scoring
- Executive interviews and insights
- Strategic relevance assessment
- Source links and timestamps

### Business Intelligence Dashboard
- Filing analysis summary
- Opportunity metrics
- Engagement readiness scoring
- Recommended actions

## 🏗️ Architecture

```
Web UI (Flask) → Master Chain → Agent #1 (SEC) → Agent #2 (Strategic) → Agent #3 (Social) → Word Report
```

### Components
- **Flask Web Server**: User interface and API endpoints
- **Master Agent Chain**: Orchestrates the three-agent pipeline
- **Word Document Generator**: Creates professional reports using python-docx
- **Responsive UI**: Bootstrap-based interface with modern design

## 🔒 Security & Privacy

- API keys are handled securely (password input fields)
- No persistent storage of sensitive data
- Temporary files cleaned up automatically
- Local processing (no external data sharing)

## 🚨 Error Handling

- Graceful degradation with mock data when APIs unavailable
- Comprehensive error messages and user feedback
- Fallback mechanisms for SEC filing access issues
- Progress indicators and loading states

## 📊 Output Files

### Word Document Reports Include:
- Executive summary with key metrics
- Detailed strategic opportunities
- Social media intelligence findings
- Executive interview insights
- Intelligence dashboard
- Recommended next steps
- Professional formatting with tables and styling

### File Naming Convention:
`EPAM_Analysis_[TICKER]_[TIMESTAMP].docx`

Example: `EPAM_Analysis_NVDA_20250925_193120.docx`

## 🛠️ Development

### File Structure:
```
/Users/dickgibbons/
├── epam_ui_app.py              # Main Flask application
├── launch_epam_ui.py           # Simple launcher script
├── templates/
│   ├── index.html              # Main input page
│   └── results.html            # Results display page
├── master_agent_chain.py       # Multi-agent orchestrator
├── agent_1_sec_filing_retriever.py
├── agent_2_strategic_opportunity_analyzer.py
└── agent_3_social_news_intelligence.py
```

### API Endpoints:
- `GET /` - Main application interface
- `POST /analyze` - Trigger company analysis
- `GET /download/<file>` - Download Word report
- `POST /api/analyze` - Programmatic analysis API

## 🎯 Use Cases

### Sales Team
- Quick company intelligence gathering
- Professional client presentation materials
- Strategic opportunity identification
- Engagement readiness assessment

### Business Development
- Market research and competitive analysis
- Executive communication insights
- Strategic partnership opportunities
- Client discovery preparation

### Consulting Services
- Rapid company assessment
- Service mapping and opportunity analysis
- Executive stakeholder research
- Proposal preparation support

## ⚡ Performance

- Analysis typically completes in 30-60 seconds
- Concurrent processing of multiple intelligence sources
- Responsive web interface with real-time updates
- Efficient Word document generation

## 🔧 Troubleshooting

### Common Issues:

1. **Port 5000 in use**: Application automatically uses port 8080
2. **Missing packages**: Run pip install commands above
3. **SEC API errors**: System uses fallback metadata when content unavailable
4. **API rate limits**: Mock data provided when API keys not available

### Debug Mode:
The application runs in debug mode for development with detailed error messages and auto-reload.

---

## 🎉 Ready to Use!

Your EPAM Business Intelligence Web UI is complete and ready for production use. The system provides:

✅ **Professional Web Interface**
✅ **Comprehensive Company Analysis**
✅ **Downloadable Word Reports**
✅ **Multi-Agent Intelligence Pipeline**
✅ **Real-time Social & News Monitoring**
✅ **EPAM Service Opportunity Mapping**

Launch the application and start analyzing companies for EPAM consulting opportunities!