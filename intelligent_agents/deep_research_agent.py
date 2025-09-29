"""
Deep Research Agent - Gradio UI for accepting research queries
"""
import gradio as gr
import asyncio
from .orchestrator import Orchestrator


class DeepResearchAgent:
    def __init__(self):
        self.orchestrator_agent = Orchestrator()
    
    def process_research_query(self, query: str, progress=gr.Progress()):
        """
        Process user research query with real-time step-by-step progress
        """
        if not query.strip():
            return "Please provide a valid research query.", "❌ No query provided"
        
        try:
            # Run the async orchestrator in a new event loop
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            try:
                result_parts = []
                progress_logs = []
                current_step = 0
                total_steps = 6  # Total number of steps
                
                # Create async generator with real-time progress updates
                async def run_with_progress():
                    nonlocal current_step
                    async for update in self.orchestrator_agent.run_research(query):
                        result_parts.append(update)
                        
                        # Update progress based on content
                        if "🚀 Starting intelligent research orchestration" in update:
                            current_step = 1
                            progress(current_step / total_steps, desc="🚀 Starting research...")
                        elif "📋 Planning intelligent search strategy" in update:
                            current_step = 2
                            progress(current_step / total_steps, desc="📋 Planning strategy...")
                        elif "🌐 Performing intelligent web searches" in update:
                            current_step = 3
                            progress(current_step / total_steps, desc="🌐 Performing searches...")
                        elif "📝 Synthesizing research findings" in update:
                            current_step = 4
                            progress(current_step / total_steps, desc="📝 Synthesizing results...")
                        elif "🔍 Validating content for safety" in update:
                            current_step = 5
                            progress(current_step / total_steps, desc="🔍 Validating content...")
                        elif "📄 Compiling final report" in update:
                            current_step = 6
                            progress(current_step / total_steps, desc="📄 Compiling report...")
                        
                        # Collect progress logs for display
                        if any(emoji in update for emoji in ["🚀", "📋", "🌐", "🔍", "📝", "📄", "✅"]):
                            progress_logs.append(update.strip())
                        
                        # Add small delay to allow UI updates
                        await asyncio.sleep(0.1)
                
                # Run the async function
                loop.run_until_complete(run_with_progress())
                
                # Final progress update
                progress(1.0, desc="✅ Research completed!")
                
                # Extract markdown report
                full_result = "".join(result_parts)
                report_start = full_result.find("# 🔍 Intelligent Research Report")
                markdown_report = full_result[report_start:] if report_start != -1 else full_result
                
                return markdown_report, "\n".join(progress_logs)
                
            finally:
                loop.close()
            
        except Exception as e:
            return f"Error processing research query: {str(e)}", f"❌ Error: {str(e)}"
    
    def create_ui_interface(self):
        """
        Create Gradio interface for the deep research agent
        """
        with gr.Blocks(title="Intelligent Research Synthesizer", theme=gr.themes.Soft()) as interface:
            gr.Markdown("# 🔍 Intelligent Research Synthesizer")
            
            with gr.Row():
                query_input = gr.Textbox(
                    label="Research Query",
                    placeholder="Enter your research topic or question...",
                    lines=3
                )
                search_button = gr.Button("🔍 Start Research", variant="primary")
            
            # Progress section
            with gr.Row():
                with gr.Column():
                    gr.Markdown("### 📊 Real-time Progress")
                    progress_logs = gr.Textbox(
                        label="Step-by-Step Progress Logs",
                        lines=10,
                        interactive=False,
                        show_copy_button=True,
                        value="Ready to start research...\n\nProgress will be shown here in real-time as each step completes."
                    )
            
            with gr.Row():
                with gr.Column():
                    gr.Markdown("### 📄 Research Report")
                    report_output = gr.Markdown(
                        value="Your research report will appear here...",
                        show_copy_button=True
                    )
            
            # Event handlers
            search_button.click(
                fn=self.process_research_query,
                inputs=[query_input],
                outputs=[report_output, progress_logs],
                show_progress=True
            )
            
            query_input.submit(
                fn=self.process_research_query,
                inputs=[query_input],
                outputs=[report_output, progress_logs],
                show_progress=True
            )
        
        return interface
    
    def launch(self, share: bool = False, debug: bool = False):
        """
        Launch the Gradio interface
        """
        ui_interface = self.create_ui_interface()
        ui_interface.launch(share=share, debug=debug)


if __name__ == "__main__":
    agent = DeepResearchAgent()
    agent.launch(debug=True)
