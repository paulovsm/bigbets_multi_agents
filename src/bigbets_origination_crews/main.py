#!/usr/bin/env python
import os
import time
import threading
import warnings
import json
import panel as pn
from dotenv import load_dotenv

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

load_dotenv()
pn.extension(design="native")

# Must precede any llm module imports
from langtrace_python_sdk import langtrace
langtrace.init(api_key = '12fc0dc8b514242abad8889e39fb94a5e100c73b9c3110c6a0cb56ff0cb14305')

from crewai.agents.agent_builder.base_agent_executor_mixin import CrewAgentExecutorMixin
from bigbets_origination_crews.value_chain_crew.crew import ResearchCrew
from bigbets_origination_crews.supply_signals_crew.crew import SupplySignalsCrew
from bigbets_origination_crews.demand_signals_crew.crew import DemandSignalsCrew
from bigbets_origination_crews.whitespace_identification_crew.crew import WhitespaceIdentificationCrew
from bigbets_origination_crews.chat_shared import chat_interface
from crewai import LLM
import bigbets_origination_crews.shared_state as shared_state
from bigbets_origination_crews.flows import input_flow  # Import the input_flow module

from bigbets_origination_crews.crew_flow import (
    run_value_chain_crew,
    run_supply_crew,
    run_demand_crew,
    run_whitespace_crew
)

def custom_ask_human_input(self, final_answer: dict) -> str:
    
    # Remove a mensagem "Thinking..." se estiver presente
    if shared_state.loading_message is not None:
        try:
            chat_interface.remove(shared_state.loading_message)
        except:
            pass
        
        shared_state.loading_message = None

    # Mostra a mensagem do agente
    chat_interface.send(final_answer, user=self.agent.role, respond=False)
    
    agent_name = self.agent.role
    # remove spaces, breaklines and special characters
    agent_name = agent_name.replace("\n", "").replace("\r", "").replace("\t", "")    

    prompt = f"Please provide feedback on provided response and the **{agent_name}** will continue the process."
    chat_interface.send(prompt, user=self.agent.role, respond=False)

    while shared_state.user_input is None:
        time.sleep(1)

    human_comments = shared_state.user_input
    shared_state.user_input = None
    return human_comments

CrewAgentExecutorMixin._ask_human_input = custom_ask_human_input

def create_output_directory(target_industry):
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    sanitized_industry = "".join(e for e in target_industry if e.isalnum())
    folder_name = f"Run_{sanitized_industry}_{timestamp}"
    output_dir = os.path.join("output", folder_name)
    os.makedirs(output_dir, exist_ok=True)
    
    return (output_dir, folder_name)

def callback(contents: str, user: str, instance: pn.chat.ChatInterface):
    
    print(f"Current crew: {shared_state.current_crew}")
    print(f"is_capturing_input in callback: {shared_state.is_capturing_input}")  # Log adicional

    # If capture_user_input is running, forward the user's message.
    if shared_state.is_capturing_input:
        shared_state.user_input = contents
        print("Capturing input")
        return

    if shared_state.current_crew is None:
        print("No crew selected")
        def run_flow():
            run_value_chain_crew(contents, chat_interface, create_output_directory, run_supply_crew)
            # run_supply_crew(...)
            # run_demand_crew(...)
            # run_whitespace_crew(...)
        thread = threading.Thread(target=run_flow)
        thread.start()
    else:
        # Crew atual aguardando input humano
        if shared_state.loading_message is not None:
            chat_interface.remove(shared_state.loading_message)
        shared_state.loading_message = chat_interface.send("Agent thinking...", user="Assistant", respond=False)
        shared_state.user_input = contents

chat_interface.callback = callback

chat_interface.send(
    "Welcome! I'm your **Big Bets Origination Assistant**. About what industry would you like me to research?",
    user="Assistant",
    respond=False
)

chat_interface.send(
    "Also let me know if you want to provide feedback on the analysis I will provided or not.",
    user="Assistant",
    respond=False
)

chat_interface.servable()
