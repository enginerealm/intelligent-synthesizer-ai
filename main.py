"""
Main application entry point for Intelligent Research Synthesizer
"""
import os
from dotenv import load_dotenv
from intelligent_agents.deep_research_agent import DeepResearchAgent


def main():
    """
    Main function to launch the Intelligent Research Synthesizer
    """
    print("🚀 Starting Intelligent Research Synthesizer...")

    # Load environment variables
    load_dotenv(override=True)
    
    # Check for required API keys
    openai_key = os.getenv("OPENAI_API_KEY")
    gemini_key = os.getenv("GEMINI_API_KEY")
    
    if not openai_key:
        print("❌ Error: OPENAI_API_KEY not found in environment variables")
        print("Please set your OpenAI API key in the .env file")
        return
    
    if not gemini_key:
        print("❌ Error: GEMINI_API_KEY not found in environment variables")
        print("Please set your Gemini API key in the .env file")
        return
    
    print("✅ API keys found")
    
    # Create and launch the deep research agent
    deep_research_agent = DeepResearchAgent()
    
    # Check if debug mode is enabled
    debug_mode = os.getenv("DEBUG_MODE", "false").lower() == "true"
    
    print(f"🔧 Debug mode: {'Enabled' if debug_mode else 'Disabled'}")
    print("🌐 Launching Gradio interface...")
    
    try:
        deep_research_agent.launch(debug=debug_mode)
    except Exception as e:
        print(f"❌ Error launching application: {e}")
        print("Please check your API keys and try again")


if __name__ == "__main__":
    main()