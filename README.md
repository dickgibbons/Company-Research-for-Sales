# 🏢 Company Research for Sales

**A comprehensive multi-agent business intelligence system for sales teams to analyze companies and identify EPAM consulting opportunities.**

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/flask-2.0+-green.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## 🎯 Overview

This system provides **automated company analysis** for sales teams, combining SEC filings, strategic analysis, and social intelligence to identify consulting opportunities and generate professional client reports.

### 🚀 Key Features

- **📊 SEC Filing Analysis** - Automatically retrieves and analyzes 10-K and 10-Q filings
- **🎯 Strategic Opportunity Mapping** - Identifies specific EPAM service opportunities
- **📱 Social Intelligence** - Monitors Twitter/X mentions and executive interviews
- **🌐 Web Interface** - Clean, professional UI for easy company analysis
- **📄 Word Report Generation** - Downloadable business reports for client presentations
- **🔍 Dynamic Company Lookup** - Supports ticker symbols or company names

## 🏗️ System Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Web UI        │───▶│  Master Chain    │───▶│  Word Reports   │
│  (Flask App)    │    │  (Orchestrator)  │    │  (.docx files)  │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │
                ┌───────────────┼───────────────┐
                │               │               │
        ┌───────▼────┐  ┌───────▼────┐  ┌──────▼─────┐
        │  Agent #1  │  │  Agent #2  │  │  Agent #3  │
        │SEC Filings │  │ Strategic  │  │   Social   │
        │ Retriever  │  │Opportunity │  │Intelligence│
        └────────────┘  └────────────┘  └────────────┘
```

## 🤖 The Three-Agent System

### Agent #1: SEC Filing Retriever
- **File**: `agent_1_sec_filing_retriever.py`
- **Purpose**: Retrieves latest 10-K and 10-Q SEC filings
- **Features**:
  - Dynamic CIK lookup for any ticker or company name
  - Supports major companies (AAPL, MSFT, NVDA, STT, etc.)
  - Full-text content extraction and analysis
  - Handles rate limiting and error recovery

### Agent #2: Strategic Opportunity Analyzer
- **File**: `agent_2_strategic_opportunity_analyzer.py`
- **Purpose**: Identifies EPAM consulting opportunities
- **Features**:
  - Analyzes SEC filings for digital transformation signals
  - Maps opportunities to specific EPAM services
  - Provides confidence scores and priority levels
  - Generates actionable recommendations

### Agent #3: Social News Intelligence
- **File**: `agent_3_social_news_intelligence.py`
- **Purpose**: Monitors social media and executive communications
- **Features**:
  - Twitter/X intelligence via Grok API
  - Executive interview analysis via Perplexity API
  - Strategic relevance scoring
  - Real-time market sentiment analysis

## 🌐 Web Interface

### Main Components
- **Flask Application** (`epam_ui_app.py`) - Core web server
- **HTML Templates** (`templates/`) - Professional Bootstrap UI
- **Launch Script** (`launch_epam_ui.py`) - Simple startup utility

### Features
- Clean, professional interface optimized for business use
- Company input with ticker symbol or name support
- Optional API key configuration for enhanced data
- Real-time analysis progress indicators
- One-click Word document download

## 📊 Generated Reports

### Word Document Output
Professional `.docx` reports include:
- **Executive Summary** with key metrics
- **Strategic Opportunities** ranked by priority
- **Social Intelligence** findings
- **Executive Interview** insights
- **EPAM Service Recommendations**
- **Next Steps** and engagement guidance

### Report Structure
```
EPAM_Analysis_[TICKER]_[TIMESTAMP].docx
├── Executive Summary
├── SEC Filing Intelligence
├── Strategic Opportunities (Top 5)
├── Social Media Intelligence
├── Executive Intelligence
└── Recommended Next Steps
```

## 🚀 Quick Start

### Prerequisites
```bash
pip install flask python-docx requests pandas numpy scikit-learn
```

### Option 1: Simple Launch
```bash
python3 launch_epam_ui.py
```

### Option 2: Direct Launch
```bash
python3 epam_ui_app.py
```

Then visit: http://localhost:8080

### Usage
1. **Enter Company**: Ticker symbol (NVDA) or company name (NVIDIA)
2. **Optional**: Add Grok/Perplexity API keys for enhanced data
3. **Analyze**: Click to start comprehensive analysis
4. **Download**: Get professional Word report for client presentation

## 🔑 API Integration

### Required APIs
- **SEC EDGAR API** - Free, no key required
- **Grok API** (Optional) - For Twitter/X social intelligence
- **Perplexity API** (Optional) - For executive interview analysis

### Mock Data Fallback
System works without API keys using simulated data for testing and demonstration.

## 📁 File Structure

```
Company-Research-for-Sales/
├── README.md                           # This file
├── agent_1_sec_filing_retriever.py     # SEC filings analysis
├── agent_2_strategic_opportunity_analyzer.py  # Strategic opportunities
├── agent_3_social_news_intelligence.py # Social intelligence
├── master_agent_chain.py               # Multi-agent orchestrator
├── epam_ui_app.py                      # Flask web application
├── launch_epam_ui.py                   # Simple launcher
├── EPAM_UI_README.md                   # Detailed UI documentation
└── templates/
    ├── index.html                      # Main input page
    └── results.html                    # Results display page
```

## 🎯 Use Cases

### Sales Teams
- **Quick company intelligence** gathering
- **Professional client presentation** materials
- **Strategic opportunity** identification
- **Engagement readiness** assessment

### Business Development
- **Market research** and competitive analysis
- **Executive communication** insights
- **Strategic partnership** opportunities
- **Client discovery** preparation

### Consulting Services
- **Rapid company assessment**
- **Service mapping** and opportunity analysis
- **Executive stakeholder** research
- **Proposal preparation** support

## 🔧 Configuration

### Environment Variables
```bash
export GROK_API_KEY="your-grok-key"          # Optional
export PERPLEXITY_API_KEY="your-perplexity-key"  # Optional
```

### Supported Companies
The system includes pre-configured CIK mappings for major companies:
- **Technology**: AAPL, MSFT, GOOGL, AMZN, NVDA, META
- **Financial**: JPM, BAC, WFC, C, GS, STT
- **Enterprise**: IBM, ORCL, INTC, CSCO
- **Plus dynamic lookup** for any public company

## 📈 Performance

- **Analysis Time**: Typically 30-60 seconds per company
- **Concurrent Processing**: Multiple intelligence sources processed in parallel
- **Scalability**: Handles any public company via dynamic SEC lookup
- **Output**: Professional reports ready for client meetings

## 🛡️ Security & Privacy

- **API Keys**: Securely handled via password input fields
- **No Persistent Storage**: Sensitive data not retained
- **Local Processing**: No external data sharing beyond API calls
- **Temporary Files**: Automatically cleaned up

## 🚨 Error Handling

- **Graceful Degradation**: Mock data when APIs unavailable
- **Comprehensive Feedback**: Clear error messages and user guidance
- **Fallback Mechanisms**: Alternative data sources for SEC filing issues
- **Progress Indicators**: Real-time status updates during processing

## 📄 License

MIT License - See LICENSE file for details

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📞 Support

For questions or issues:
- Review the detailed documentation in `EPAM_UI_README.md`
- Check the troubleshooting section for common issues
- Submit issues via GitHub Issues

---

## 🎉 Ready for Business!

This comprehensive business intelligence system provides sales teams with:

✅ **Professional Company Analysis**
✅ **Strategic Opportunity Identification**
✅ **Social Intelligence Monitoring**
✅ **Executive Communication Insights**
✅ **Downloadable Client Reports**
✅ **EPAM Service Opportunity Mapping**

Transform your sales process with automated company intelligence! 🚀