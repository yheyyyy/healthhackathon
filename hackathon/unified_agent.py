from langchain.agents import Tool, initialize_agent, AgentType
from langchain.chains.conversation.memory import ConversationBufferMemory
from ocr_tool import ocr_tool_function
from create_calendar import main
from get_response import get_response
from rag_service import RAGService
from openrouter_client import ChatOpenRouter


def initialize_llm():
    "Initialize LLM from Openrouter"
    return ChatOpenRouter(model_name='google/gemini-2.0-flash-exp:free')


def create_unified_agent():
    # Initialize the tools
    rag_service = RAGService()  
    tools = [
        Tool(
            name="OCR_Tool",
            func=ocr_tool_function,
            description="Use this tool to extract text from images."
        ),
        Tool(
            name="Schedule_Appointment",
            func=main,
            description=(
                "Use this tool for scheduling appointments. Pass the appt "
                "message exactly as received. This function will run main "
                "and create a calendar in Google Calendar."
                "The message must be in format: "
                "'Dear [Name], You have a [Appointment Type] at [Location] on "
                "[Date] at [Time].'"
            )
        ),
        Tool(
            name="General_Chat",
            func=get_response,
            description=(
                "Use this for general chat interactions about mental health "
                "services, appointments, and other healthcare related queries."
            )
        ),
        Tool(
            name="RAG_Tool",
            func= rag_service.rag_tool_function,
            description=(
                "Use this tool to query the knowledge base for specific appointment re-scheduling"
                "and appointment details "
                "about healthcare referral queries. This tool provides "
                "accurate answers based on the stored documentation and serves as a ground truth."
            )
        )
    ]

    # Initialize the memory
    memory = ConversationBufferMemory(
        return_messages=True,
        memory_key="chat_history"
    )

    llm = initialize_llm()
    # Create the agent using the Runnable instance
    agent = initialize_agent(
        tools,
        llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        memory=memory,
        handle_parsing_errors=True
    )

    return agent

def format_appointment_response(appt: dict) -> str:
    """Format appointment details with proper line breaks."""
    return (
        "✅ Appointment created!\n"
        f"**Appointment Name:**\n{appt['appointment']}\n"
        f"**Location:**\n{appt['location']}\n"
        f"**Date:**\n{appt['date']}\n"
        f"**Time:**\n{appt['time']}"
    )

def process_message(message: str, image_bytes: bytes = None) -> str:
    """Process a message using the unified agent and return the response."""
    # Initialize the agent
    agent = create_unified_agent()

    # Handle OCR if image_bytes is provided
    if image_bytes:
        extracted_text = agent.invoke({"input": image_bytes})
        message = extracted_text  # Replace the original message with OCR result

    # Handle appointment scheduling if the message starts with "Dear"
    if message.startswith("Dear"):
        try:
            appointment_details = main(message)
            return format_appointment_response(appointment_details)
        except Exception as e:
            return f"Error scheduling appointment: {str(e)}"

    # For other messages, use the agent
    try:
        response = agent.invoke({"input": message})
        return response["output"]
    except Exception as e:
        error_str = str(e)
        if "Could not parse LLM output:" in error_str:
            # Extract the action input from the error message
            start_idx = error_str.find("action_input': '") + len("action_input': '")
            end_idx = error_str.rfind("'}")
            if start_idx > -1 and end_idx > -1:
                return error_str[start_idx:end_idx]
        return (
            "I apologize, but I encountered an error processing your request. "
            "Please try again."
        )
        
if __name__ == "__main__":
    # Example usage
    #message = "Dear Ms. DIANE, You have a First Visit Consultation at ENT-Head & Neck Surg Ctr - 15C, NUH Medical Centre, Zone B, Level 15, 15c, Lift Lobby B2 on 19 Mar 2025 at 3:45 pm."
    rag_service = RAGService()
    rag_service.initialise_docs()
    message = "What is the phone number of the National University Hospital Referral?"
    response = process_message(message)
    print(response)