# 🔍 Intelligent Research Synthesizer

An advanced agentic AI system that performs comprehensive topic research using intelligent web search strategies, AI-powered synthesis, and content validation. Built with a modern agent-based architecture using OpenAI's GPT models and Google's Gemini for content validation.

## 🌟 What This Project Does

The Intelligent Research Synthesizer is a sophisticated AI research assistant that:

- **🧠 Plans Intelligent Search Strategies**: Analyzes your query and creates two complementary search approaches
- **🌐 Performs Dual Web Searches**: Executes two strategically planned web searches for comprehensive coverage
- **📝 Synthesizes Findings**: Combines and analyzes search results using advanced AI reasoning
- **📊 Generates Structured Reports**: Creates comprehensive, well-formatted research reports
- **🛡️ Validates Content**: Ensures all content is appropriate using Gemini's safety checks
- **📱 Provides Real-time Progress**: Shows step-by-step progress with a beautiful Gradio interface

## 🏗️ Architecture Overview

This project uses a modern **agent-based architecture** with the following components:

### Core Agents
- **QueryPlannerAgent**: Plans intelligent search strategies with reasoning
- **WebSearcherAgent**: Executes web searches using OpenAI's WebSearchTool
- **SynthesisAgent**: Combines and analyzes search results
- **OutputGuardrailsAgent**: Validates content for safety and appropriateness

### Key Components
- **Runner**: Orchestrates agent execution and flow control
- **Orchestrator**: Manages the complete research workflow
- **DeepResearchAgent**: Provides the Gradio UI interface
- **Tracing System**: Built-in tracing for debugging and monitoring

## 🚀 Quick Start

### Prerequisites
- Python 3.13.5 or higher
- UV package manager
- OpenAI API key
- Google Gemini API key

### Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd intelligent-synthesizer-ai
   ```

2. **Install dependencies**:
   ```bash
   uv sync
   ```

3. **Set up environment variables**:
   ```bash
   cp env.example .env
   ```

4. **Configure your API keys** in `.env`:
   ```bash
   # Required API Keys
   OPENAI_API_KEY=your_openai_api_key_here
   GEMINI_API_KEY=your_gemini_api_key_here
   
   # Optional Configuration
   DEBUG_MODE=false
   ```

5. **Run the application**:
   ```bash
   uv run python main.py
   ```

6. **Access the interface**:
   - Open your browser to `http://127.0.0.1:7860`
   - Enter your research query
   - Click "🔍 Start Research"

## 📁 Project Structure

```
intelligent-synthesizer-ai/
├── main.py                          # Application entry point
├── agents.py                        # Tracing functionality
├── env.example                      # Environment variables template
├── pyproject.toml                   # Project dependencies and configuration
├── README.md                        # This documentation
├── uv.lock                          # Dependency lock file
├── models/
│   ├── __init__.py
│   └── research_models.py           # Pydantic data models
└── intelligent_agents/
    ├── __init__.py                  # Package initialization
    ├── agent.py                     # Base Agent class
    ├── decorators.py                # Function decorators (@function_tool, @agent_tool)
    ├── deep_research_agent.py      # Gradio UI interface
    ├── orchestrator.py              # Research workflow orchestration
    ├── runner.py                    # Agent execution runner
    ├── query_planner_agent.py       # Query planning agent
    ├── web_searcher_agent.py        # Web search agent
    ├── synthesis_agent.py           # Report synthesis agent
    ├── output_guardrails_agent.py   # Content validation agent
    └── web_search_tool.py           # Web search tool implementation
```

## 🔧 Development Setup

### Local Development

1. **Install development dependencies**:
   ```bash
   uv sync --group dev
   ```

2. **Enable debug mode**:
   ```bash
   # Set in .env file
   DEBUG_MODE=true
   ```

3. **Run with debugging**:
   ```bash
   uv run python main.py
   ```

### Code Quality

```bash
# Format code with Black
uv run black .

# Note: Additional linting and type checking tools can be added as needed
```

## 🐛 Debugging Guide

### Common Issues

1. **API Key Errors**:
   ```
   ❌ Error: OPENAI_API_KEY not found in environment variables
   ```
   **Solution**: Ensure your `.env` file contains valid API keys

2. **Import Errors**:
   ```
   ModuleNotFoundError: No module named 'intelligent_agents'
   ```
   **Solution**: Run `uv sync` to install dependencies

3. **Port Already in Use**:
   ```
   Address already in use: 127.0.0.1:7860
   ```
   **Solution**: Kill the existing process or use a different port

### Debug Mode

Enable debug mode for detailed logging:
```bash
# In .env file
DEBUG_MODE=true
```

### Tracing and Monitoring

The system includes built-in tracing for debugging:
- Console output shows real-time progress
- Each agent operation is traced
- Performance metrics are displayed
- Error tracking with detailed stack traces

## 🎯 Usage Examples

### Basic Research Query
```
"What are the latest trends in artificial intelligence?"
```

### Specific Industry Research
```
"How is machine learning being applied in healthcare in 2024?"
```

### Comparative Analysis
```
"What are the differences between GPT-4 and Claude-3 for code generation?"
```

### Technical Deep Dive
```
"What are the security implications of using large language models in enterprise applications?"
```

## 🔄 Research Process Flow

1. **🚀 Initialization**: System starts and validates API keys
2. **📋 Query Planning**: AI analyzes your question and creates search strategy
3. **🌐 Web Search 1**: First complementary search with specific focus
4. **🌐 Web Search 2**: Second search with different angle/approach
5. **📝 Synthesis**: AI combines and analyzes all search results
6. **🔍 Validation**: Content is checked for appropriateness
7. **📄 Report Generation**: Final structured report is created
8. **✅ Delivery**: Report is presented with progress logs

## 🛠️ Configuration Options

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `OPENAI_API_KEY` | OpenAI API key for GPT models | - | ✅ |
| `GEMINI_API_KEY` | Google Gemini API key for validation | - | ✅ |
| `DEBUG_MODE` | Enable debug logging | `false` | ❌ |

### Model Configuration

The system uses the following models by default:
- **GPT-4**: For query planning, synthesis, and web search simulation
- **Gemini Pro**: For content validation and safety checks

## 🚀 Deployment

### Local Deployment
```bash
# Standard deployment
uv run python main.py

# With public sharing (for demos)
# Modify main.py to add share=True to launch()
```

### Production Considerations

1. **API Rate Limits**: Monitor OpenAI and Gemini API usage
2. **Error Handling**: Implement proper error recovery
3. **Logging**: Set up structured logging for production
4. **Monitoring**: Use the built-in tracing system
5. **Security**: Ensure API keys are properly secured

## 📊 Performance Metrics

The system tracks:
- **Query Planning Time**: ~5-8 seconds
- **Web Search Time**: ~20-30 seconds per search
- **Synthesis Time**: ~10-15 seconds
- **Validation Time**: ~1-2 seconds
- **Total Processing Time**: ~60-90 seconds per research query

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes
4. Format code: `uv run black .`
5. Commit changes: `git commit -m 'Add amazing feature'`
6. Push to branch: `git push origin feature/amazing-feature`
7. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

### Getting Help

1. **Check the logs**: Look for error messages in the console output
2. **Verify API keys**: Ensure your OpenAI and Gemini API keys are valid
3. **Check dependencies**: Run `uv sync` to ensure all packages are installed
4. **Debug mode**: Enable `DEBUG_MODE=true` for detailed logging

### Common Solutions

- **Slow performance**: This is normal for AI research - the system performs multiple API calls
- **Empty results**: Check your internet connection and API key validity
- **UI not loading**: Ensure port 7860 is available and not blocked by firewall

## 🔮 Future Enhancements

- [ ] Support for more search engines
- [ ] Custom model configurations
- [ ] Batch processing capabilities
- [ ] Export to different formats (PDF, Word, etc.)
- [ ] Integration with external databases
- [ ] Advanced filtering and search options
- [ ] Multi-language support
- [ ] API endpoint for programmatic access

## 📚 Technical Details

### Dependencies
- **Gradio**: Modern web UI framework
- **OpenAI**: GPT models and API integration
- **Google Generative AI**: Content validation
- **Pydantic**: Data validation and models
- **Python 3.13.5+**: Modern Python features

### Architecture Patterns
- **Agent-Based Architecture**: Modular, scalable design
- **Orchestration Pattern**: Centralized workflow management
- **Decorator Pattern**: Function and method enhancement
- **Generator Pattern**: Real-time progress updates
- **Context Manager Pattern**: Resource management and tracing

---

**Built with ❤️ using modern AI technologies and best practices.**