import os
import json
import traceback
import bigbets_origination_crews.shared_state as shared_state
from bigbets_origination_crews.value_chain_crew.crew import ResearchCrew
from bigbets_origination_crews.flows.demand_flow import run_demand_crew
from bigbets_origination_crews.flows.whitespace_flow import run_whitespace_crew

def run_value_chain_crew(initial_request, llm, chat_interface, create_output_directory, run_supply_crew):
    try:
        llm_response = llm.call(
            messages=[
                { 
                 "content": """
                    Your task is to extract from the user input the following information: 
                    - target industry
                    - target region
                    - top X players 
                    - if human input is expected
                    - if value chain step is expected
                    - if demand signals step is expected
                    - if supply signals step is expected
                    - if whitespace identification step is expected
                    - Job ID (previous execution ID)
                    
                    You MUST respond as a JSON object. 
                    
                    Sample JSON response: 
                    {
                        "target_industry": "Food & Beverages",
                        "target_region": "Brazil",
                        "top_players": 10, 
                        "human_input": true,
                        "value_chain_step": true,
                        "demand_signals_step": true,
                        "supply_signals_step": true,
                        "whitespace_identification_step": true}",
                        "job_id": "Run_FoodBeverages_20250117143434"
                    """,
                 "role": "system" 
                },
                {
                    "content": initial_request,
                    "role": "user"
                }
                ]
            )
        
        llm_response = json.loads(llm_response)
        
        target_industry = llm_response["target_industry"]
        target_region = llm_response["target_region"] if "target_region" in llm_response and llm_response["target_region"] not in [None, ""] else "Brazil"
        top_players = llm_response["top_players"] if "top_players" in llm_response and llm_response["top_players"] not in [None, ""] and int(llm_response["top_players"]) > 0 else 10
        human_input = bool(llm_response["human_input"]) if "human_input" in llm_response and llm_response["human_input"] not in [None, ""] else False
        value_chain_step = bool(llm_response["value_chain_step"]) if "value_chain_step" in llm_response and llm_response["value_chain_step"] not in [None, ""] else True
        demand_signals_step = bool(llm_response["demand_signals_step"]) if "demand_signals_step" in llm_response and llm_response["demand_signals_step"] not in [None, ""] else True
        supply_signals_step = bool(llm_response["supply_signals_step"]) if "supply_signals_step" in llm_response and llm_response["supply_signals_step"] not in [None, ""] else True
        whitespace_identification_step = bool(llm_response["whitespace_identification_step"]) if "whitespace_identification_step" in llm_response and llm_response["whitespace_identification_step"] not in [None, ""] else True
        job_id = llm_response["job_id"] if "job_id" in llm_response and llm_response["job_id"] not in [None, ""] else None
       
        input_params = {
            "target_industry": target_industry,
            "target_region": target_region,
            "top_players": top_players,
            "human_input": human_input,
            "value_chain_step": value_chain_step,
            "demand_signals_step": demand_signals_step,
            "supply_signals_step": supply_signals_step,
            "whitespace_identification_step": whitespace_identification_step
        }
        
        (output_dir, job_id) = (os.path.join("output", job_id), job_id) if job_id is not None else create_output_directory(target_industry)
        
        chat_interface.send(
            f"Your Job ID is: **{job_id}**. You can use this ID to continue or resume the process later.",
            user="Assistant",
            respond=False
        )
        
        if not value_chain_step:
            chat_interface.send(
                "The **Value Chain Crew** step will be skipped.",
                user="Assistant",
                respond=False
                )
            
            run_supply_crew(input_params, output_dir, chat_interface, 
                           lambda input_params, output_dir, chat_interface, next_step: run_demand_crew(input_params, output_dir, chat_interface, run_whitespace_crew))
            return
        else:
            chat_interface.send(
                "Now I will start the **Value Chain Crew**. Please wait a moment...",
                user="Assistant",
                respond=False
            )
            
            inputs = {"target_industry": target_industry, "target_region": target_region, "top_players": top_players}
            crew_instance = ResearchCrew(output_dir, human_input).crew()
            shared_state.current_crew = crew_instance
            crew_instance.kickoff(inputs=inputs)

            run_supply_crew(input_params, output_dir, chat_interface,
                           lambda input_params, output_dir, chat_interface, next_step: run_demand_crew(input_params, output_dir, chat_interface, run_whitespace_crew))

    except Exception as e:
        # Print the error complete stack trace
        error_message = traceback.format_exc()
        print(error_message)
        chat_interface.send(f"An error occurred: {e}", user="Assistant", respond=False)
        shared_state.current_crew = None