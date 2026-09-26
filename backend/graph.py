"""
LangGraph-based conversational AI for the Student Portal.
Uses a StateGraph with input and LLM processing nodes.
"""

from typing import Annotated
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from pydantic import BaseModel
import os
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI


class State(BaseModel):
    """State for the conversation graph"""
    messages: Annotated[list[BaseMessage], add_messages]


def get_llm():
    """
    Get LLM from environment variables.
    Supports:
    - ANTHROPIC_API_KEY for Claude (via ChatAnthropic)
    - OPENAI_API_KEY for GPT (via ChatOpenAI)
    """
    if os.getenv("ANTHROPIC_API_KEY"):
        return ChatAnthropic(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            temperature=0.7
        )
    elif os.getenv("OPENAI_API_KEY"):
        return ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.7,
            max_tokens=1024
        )
    else:
        raise ValueError(
            "No LLM API key found. Set ANTHROPIC_API_KEY or OPENAI_API_KEY"
        )


def input_node(state: State) -> State:
    """
    Input node: Processes incoming messages.
    In a real system, this could validate, clean, or enrich the input.
    """
    # Messages are already in state from the caller
    return state


def llm_node(state: State) -> dict:
    """
    LLM node: Sends messages to the language model and gets a response.
    Returns the assistant's response to be added to the message history.
    """
    llm = get_llm()
    
    system_prompt = """You are Luma, a friendly and helpful AI assistant for students. 
Your role is to help with:
- Academic questions and explanations
- Study tips and time management
- Course guidance and assignments
- Motivation and learning strategies
- General educational support

Be encouraging, clear, and concise. Break down complex topics into understandable parts.
If you don't know something, admit it and suggest where the student might find help.
Keep responses focused and under 200 words when possible."""
    
    # Get all messages except the system prompt
    messages = state.messages
    
    # Call the LLM with system prompt
    response = llm.invoke(
        messages,
        system=system_prompt
    )
    
    # Return the AI message to be added to state
    return {"messages": [response]}


def create_graph():
    """Create and compile the LangGraph StateGraph"""
    graph = StateGraph(State)
    
    # Add nodes
    graph.add_node("input", input_node)
    graph.add_node("llm", llm_node)
    
    # Connect nodes
    graph.add_edge(START, "input")
    graph.add_edge("input", "llm")
    graph.add_edge("llm", END)
    
    return graph.compile()


def chat(user_message: str) -> str:
    """
    Main entry point for chatting with the AI.
    Takes a user message and returns the assistant's response.
    """
    # Initialize the graph
    graph = create_graph()
    
    # Create initial state with user message
    initial_state = State(messages=[HumanMessage(content=user_message)])
    
    # Run the graph
    final_state = graph.invoke(initial_state)
    
    # Extract the last message (which should be the AI response)
    last_message = final_state["messages"][-1]
    
    if isinstance(last_message, AIMessage):
        return last_message.content
    else:
        return "Unable to generate response"


if __name__ == "__main__":
    # Test the graph
    try:
        print("Testing LangGraph chat system...")
        response = chat("What are some effective study techniques?")
        print(f"\nUser: What are some effective study techniques?")
        print(f"Assistant: {response}")
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure to set ANTHROPIC_API_KEY or OPENAI_API_KEY environment variable")
