from langchain.agents import Tool, initialize_agent, AgentType
from langchain_ollama.llms import OllamaLLM
from langchain.chains.conversation.memory import ConversationBufferMemory
from create_calendar import main
from get_response import get_response


def create_unified_agent():
    # Initialize the tools
    tools = [
        Tool(
            name="Schedule_Appointment",
            func=main,
            description=(
                "Use this tool for scheduling appointments. Pass the appt "
                "message exactly as received. This function will run main "
                "and create a calendar in google calendar."
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
        )
    ]

    # Initialize the memory
    memory = ConversationBufferMemory(
        return_messages=True,
        memory_key="chat_history"
    )

    # Initialize Ollama with the mistral model
    llm = OllamaLLM(model="mistral:7b")

    # Create the agent with ZERO_SHOT_REACT_DESCRIPTION type
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


def process_message(message: str) -> str:
    """Process a message using the unified agent and return the response."""
    agent = create_unified_agent()
    
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
            start_idx = error_str.find("action_input': '") + len("action_input': '")
            end_idx = error_str.rfind("'}")
            if start_idx > -1 and end_idx > -1:
                return error_str[start_idx:end_idx]
        return (
            "I apologize, but I encountered an error processing your request. "
            "Please try again."
        )