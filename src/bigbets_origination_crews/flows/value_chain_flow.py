import os
import json
import traceback
import bigbets_origination_crews.shared_state as shared_state
from bigbets_origination_crews.value_chain_crew.crew import ResearchCrew
from bigbets_origination_crews.flows.demand_flow import run_demand_crew
from bigbets_origination_crews.flows.whitespace_flow import run_whitespace_crew
from bigbets_origination_crews.flows.input_flow import capture_user_input
from crewai import LLM

def run_value_chain_crew(initial_request, chat_interface, create_output_directory, run_supply_crew):
    try:
        # Capture user inputs using the new flow
        input_params, output_dir, job_id = capture_user_input(initial_request, chat_interface, create_output_directory)
        
        chat_interface.send(
            f"Your Job ID is: **{job_id}**. You can use this ID to continue or resume the process later.",
            user="Assistant",
            respond=False
        )
        
        if not input_params["value_chain_step"]:
            chat_interface.send(
                "The Value Chain step will be skipped.",
                user="Assistant",
                respond=False
            )
            
            run_supply_crew(input_params, output_dir, chat_interface,
                           lambda input_params, output_dir, chat_interface, next_step: run_demand_crew(input_params, output_dir, chat_interface, run_whitespace_crew))
            return
        else:
            chat_interface.send(
                "Now starting the Value Chain process. Please wait a moment...",
                user="Assistant",
                respond=False
            )
            
            inputs = {
                "target_industry": input_params["target_industry"],
                "target_region": input_params["target_region"],
                "top_players": input_params["top_players"]
            }
            crew_instance = ResearchCrew(output_dir, input_params["human_input"]).crew()
            shared_state.current_crew = crew_instance
            crew_instance.kickoff(inputs=inputs)

            run_supply_crew(input_params, output_dir, chat_interface,
                           lambda input_params, output_dir, chat_interface, next_step: run_demand_crew(input_params, output_dir, chat_interface, run_whitespace_crew))

    except Exception as e:
        # Print the full error stack trace
        error_message = traceback.format_exc()
        print(error_message)
        chat_interface.send(f"An error occurred: {e}", user="Assistant", respond=False)
        shared_state.current_crew = None