import json
import os
from crewai import LLM

def capture_user_input(initial_request, chat_interface, create_output_directory):
    """
    Captura e processa os inputs do usuário usando LLM.
    Retorna um dicionário de parâmetros, o diretório de saída e o job_id.
    """
    llm = LLM(
        model="openrouter/google/gemini-2.0-flash-lite-preview-02-05:free",
        response_format={ "type": "json_object" }
    )
        
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
                    "target_industry": "Food & Beverages", # Required
                    "target_region": "Brazil", #Required
                    "top_players": 10, # Default is 10
                    "human_input": true, # Default is false
                    "value_chain_step": true, # Default is true
                    "demand_signals_step": true, # Default is true
                    "supply_signals_step": true, # Default is true
                    "whitespace_identification_step": true, # Default is true
                    "job_id": "Run_FoodBeverages_20250117143434" # Optional
                }
                
                If you could not extract the information for a field, you must fill with the default values.
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
    target_region = llm_response.get("target_region") or "Brazil"
    top_players = int(llm_response["top_players"]) if "top_players" in llm_response and int(llm_response["top_players"]) > 0 else 10
    human_input = bool(llm_response.get("human_input", False))
    value_chain_step = bool(llm_response.get("value_chain_step", True))
    demand_signals_step = bool(llm_response.get("demand_signals_step", True))
    supply_signals_step = bool(llm_response.get("supply_signals_step", True))
    whitespace_identification_step = bool(llm_response.get("whitespace_identification_step", True))
    job_id = llm_response.get("job_id")
    
    if job_id is not None and job_id.strip() != "":
        output_dir = os.path.join("output", job_id)
    else:
        output_dir, job_id = create_output_directory(target_industry)
    
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
    
    print(f"Input parameters: {input_params}")
    
    return input_params, output_dir, job_id
