import logging
import argparse
import sys
import os
from pathlib import Path
import json
import time

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logs/osint_system.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

def setup_environment():
    """Set up the environment and verify all components."""
    try:
        # Add src to path if not already there
        src_path = Path(__file__).parent / "src"
        if str(src_path.absolute()) not in sys.path:
            sys.path.append(str(src_path.absolute()))
            
        logger.info("Environment setup complete")
        return True
    except Exception as e:
        logger.error(f"Environment setup failed: {str(e)}")
        return False

def initialize_system(kb_path=None):
    """
    Initialize the OSINT system with all components.
    
    Args:
        kb_path: Path to the knowledge base data
        
    Returns:
        Dictionary containing all initialized components
    """
    try:
        # Import required components
        from src.agent.agent_manager import AgentManager
        from src.knowledge_base.knowledge_base_manager import KnowledgeBaseManager 
        from src.rag.rag_pipeline import RagPipeline
        from src.llm.claude_service import ClaudeService
        from src.chatbot.chatbot_manager import ChatbotManager
        
        # Set up the knowledge base
        logger.info("Initializing knowledge base")
        kb_path = kb_path or "data"
        kb_manager = KnowledgeBaseManager(base_dir=kb_path)
        
        # Initialize Claude service
        logger.info("Initializing Claude service")
        claude_service = ClaudeService()
        
        # Get API key from the claude service
        api_key = claude_service.api_key if hasattr(claude_service, 'api_key') else None
        logger.info("Setting up RAG pipeline")
        rag_pipeline = RagPipeline(
            knowledge_base_manager=kb_manager,
            api_key=api_key
        )
        
        # Initialize agent manager with tools
        logger.info("Initializing agent manager")
        agent_manager = AgentManager(
            llm_service=claude_service,
            knowledge_base=kb_manager
        )
        
        # Create chatbot manager and set up chatbot
        logger.info("Setting up chatbot")
        chatbot_config = {
            "system_prompt": "I am an OSINT intelligence assistant specialized in cybersecurity. I can help with threat analysis, vulnerability research, and security investigations."
        }
        chatbot_manager = ChatbotManager(config=chatbot_config)
        chatbot = chatbot_manager.setup_chatbot(
            agent_manager=agent_manager,
            rag_pipeline=rag_pipeline,
            claude_service=claude_service
        )
        
        logger.info("OSINT system initialized successfully")
        
        return {
            "knowledge_base": kb_manager,
            "claude_service": claude_service,
            "rag_pipeline": rag_pipeline,
            "agent_manager": agent_manager,
            "chatbot_manager": chatbot_manager
        }
    
    except Exception as e:
        logger.error(f"System initialization failed: {str(e)}")
        return None

def format_response(response_data):
    """Format the response data for display in the CLI."""
    response_text = response_data["response"]
    response_type = response_data.get("type", "unknown")
    confidence = response_data.get("confidence", 0)
    
    # Format confidence as stars with Unicode characters
    confidence_stars = "★" * int(confidence * 5)
    confidence_stars += "☆" * (5 - len(confidence_stars))
    
    # Format sources if available
    sources = response_data.get("sources", [])
    sources_text = ""
    if sources:
        sources_text = "\n\nSources:\n" + "\n".join([f"• {source}" for source in sources[:3]])
        if len(sources) > 3:
            sources_text += f"\n  (and {len(sources) - 3} more sources)"
    
    # Format response type with an appropriate icon
    type_icons = {
        "rag": "🔍",
        "agent": "🤖",
        "fallback": "ℹ️",
        "claude_fallback": "🧠",
        "error": "⚠️",
        "unknown": "❓"
    }
    type_icon = type_icons.get(response_type, "❓")
    
    # Add a divider for visual separation
    divider = "─" * 60
    
    # Format the complete response
    formatted = f"\n{divider}\n"
    
    # Add a header based on response type
    if response_type == "rag":
        formatted += f"🔍 Knowledge Base Response\n\n"
    elif response_type == "agent":
        formatted += f"🤖 Intelligence Analysis\n\n"
    elif response_type == "fallback":
        formatted += f"ℹ️ General Response\n\n"
    elif response_type == "claude_fallback":
        formatted += f"🧠 Claude Intelligence Response\n\n"
    else:
        formatted += f"{type_icon} System Response\n\n"
    
    # Add the main response text
    formatted += f"{response_text}{sources_text}\n\n"
    
    # Add metadata footer
    formatted += f"{type_icon} Response type: {response_type} | "
    formatted += f"Confidence: {confidence_stars} ({confidence:.2f})"
    
    # Add closing divider
    formatted += f"\n{divider}"
    
    return formatted

def run_interactive_mode(chatbot_manager):
    """
    Run the OSINT system in interactive mode.
    
    Args:
        chatbot_manager: Initialized chatbot manager
    """
    # Clear screen and show welcome banner
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print("\n╔═══════════════════════════════════════════════════════════════╗")
    print("║                                                               ║")
    print("║                OSINT FUZZY INTELLIGENCE                       ║")
    print("║                                                               ║")
    print("╚═══════════════════════════════════════════════════════════════╝")
    print("\nSecure Intelligence Analysis Engine")
    print("\nAvailable commands:")
    print("  • /exit or /quit - Exit the system")
    print("  • /clear - Clear conversation history")
    print("  • /help - Show available commands")
    print("  • /status - Display system status")
    print("\nType your query below to begin your intelligence analysis...\n")
    
    while True:
        try:
            # Get user input with custom prompt
            user_input = input("\n> ").strip()
            
            # Check for command prefix
            if user_input.startswith('/'):
                cmd = user_input[1:].lower()
                
                # Check for exit commands
                if cmd in ['exit', 'quit']:
                    print("\nExiting OSINT system. Goodbye!")
                    break
                    
                # Check for clear command
                elif cmd == 'clear':
                    chatbot_manager.get_chatbot().clear_conversation()
                    print("Conversation history cleared.")
                    continue
                    
                # Check for help command
                elif cmd == 'help':
                    print("\nAvailable Commands:")
                    print("  • /exit or /quit - Exit the system")
                    print("  • /clear - Clear conversation history")
                    print("  • /help - Show this help message")
                    print("  • /status - Display system status")
                    continue
                
                # Check for status command
                elif cmd == 'status':
                    print("\nSystem Status:")
                    print("  • Chatbot: Active")
                    print("  • Messages: " + str(len(chatbot_manager.get_chatbot().get_conversation_history())))
                    print("  • Mode: Interactive CLI")
                    continue
                    
                # Unknown command
                else:
                    print(f"Unknown command: {cmd}. Type /help for available commands.")
                    continue
            
            # Process regular query
            if not user_input:
                continue
                
            # Show processing indicator
            print("\nProcessing your intelligence query... Please wait.")
            start_time = time.time()
            
            # Process the query
            response_data = chatbot_manager.process_query(user_input)
            processing_time = time.time() - start_time
            
            # Display the response
            print(format_response(response_data))
            print(f"Processing time: {processing_time:.2f} seconds")
                
        except KeyboardInterrupt:
            print("\n\nOperation interrupted by user. Exiting.")
            break
        except Exception as e:
            logger.error(f"Error in interactive mode: {str(e)}")
            print(f"\nAn error occurred: {str(e)}")

def main():
    """Main entry point for the OSINT CLI."""
    parser = argparse.ArgumentParser(description='OSINT System CLI')
    parser.add_argument('--kb_path', type=str, help='Path to knowledge base')
    args = parser.parse_args()
    
    # Setup environment
    if not setup_environment():
        print("Failed to set up environment. Exiting.")
        return
    
    # Initialize system
    system = initialize_system(kb_path=args.kb_path)
    if not system:
        print("Failed to initialize OSINT system. Exiting.")
        return
    
    # Run interactive mode
    run_interactive_mode(system["chatbot_manager"])

if __name__ == "__main__":
    main()