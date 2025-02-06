import json
import os
import time
from crewai import LLM
import bigbets_origination_crews.shared_state as shared_state

def capture_user_input(initial_request, chat_interface, create_output_directory):
    """
    Captures and processes user inputs using LLM.
    Then, it shows a plain language summary of the details and asks for your confirmation.
    If you disagree, you may re-enter the information.
    Returns a dictionary of parameters, the output directory, and the job_id.
    """
    shared_state.original_request = initial_request
    shared_state.is_capturing_input = True
    
    while True:
        # Extract and validate parameters
        input_params, output_dir, job_id = extract_and_validate_parameters(shared_state.original_request, chat_interface, create_output_directory)
        summary = format_parameters_summary(input_params, job_id)
        chat_interface.send(summary, user="Assistant", respond=False)
        
        # Wait for user response
        shared_state.user_input = None
        while shared_state.user_input is None:
            time.sleep(1)
        
        response = shared_state.user_input.strip().lower()
        shared_state.user_input = None
        
        if response in ["yes", "y"]:
            break
        elif response in ["no", "n"]:
            chat_interface.send("Please re-enter the information.", user="Assistant", respond=False)
            
            # Wait for new input from the user to update the request
            shared_state.user_input = None
            while shared_state.user_input is None:
                time.sleep(1)
            
            # Delete the created output directory
            if os.path.exists(output_dir):
                os.rmdir(output_dir)
            
            shared_state.original_request = shared_state.user_input
            shared_state.user_input = None
        else:
            chat_interface.send("Response not recognized. Please try again.", user="Assistant", respond=False)
    
    print(f"Input parameters: {input_params}")
    shared_state.is_capturing_input = False
    print("capture_user_input: is_capturing_input set to False")  # Log adicional
    return input_params, output_dir, job_id

def extract_and_validate_parameters(original_request, chat_interface, create_output_directory):
    """
    Extracts and validates parameters from user input using LLM.
    
    Args:
        original_request (str): The user's original input text
        chat_interface: Interface object for user communication
        create_output_directory (callable): Function to create output directory
        
    Returns:
        tuple: (input_params, output_dir, job_id)
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
                    "target_industry": "Food & Beverages", # Required field
                    "target_region": "Brazil", # Required field
                    "top_players": 10, # Default 10
                    "human_input": true, # Default false
                    "value_chain_step": true, # Default true
                    "demand_signals_step": true, # Default true
                    "supply_signals_step": true, # Default true
                    "whitespace_identification_step": true, # Default true
                    "job_id": "Run_FoodBeverages_20250117143434" # Optional field
                }
                
                If you don't have the information for a field, you must fill with the default value.
                
                """,
                "role": "system" 
            },
            {
                "content": original_request,
                "role": "user"
            }
        ]
    )
    
    llm_response = json.loads(llm_response)
    
    target_industry = llm_response.get("target_industry")
    if not target_industry:
        raise ValueError("The 'target industry' field is required")

    input_params = {
        "target_industry": target_industry,
        "target_region": llm_response.get("target_region", "Brazil"),
        "top_players": int(llm_response.get("top_players", 10)),
        "human_input": bool(llm_response.get("human_input", False)),
        "value_chain_step": bool(llm_response.get("value_chain_step", True)),
        "demand_signals_step": bool(llm_response.get("demand_signals_step", True)),
        "supply_signals_step": bool(llm_response.get("supply_signals_step", True)),
        "whitespace_identification_step": bool(llm_response.get("whitespace_identification_step", True))
    }
    
    job_id = llm_response.get("job_id")

    if job_id is not None and job_id.strip() != "":
        output_dir = os.path.join("output", job_id)
    else:
        output_dir, job_id = create_output_directory(target_industry)
    
    return input_params, output_dir, job_id

def format_parameters_summary(input_params, job_id):
    """
    Creates a user-friendly summary of the parameters.
    
    Args:
        input_params (dict): Dictionary containing the input parameters
        job_id (str): The job identifier
        
    Returns:
        str: Formatted summary
    """
    return (
        "Here's what we have gathered:\n"
        f"- Industry of Interest: {input_params['target_industry']}\n"
        f"- Region: {input_params['target_region']}\n"
        f"- Number of Top Competitors: {input_params['top_players']}\n"
        f"- Require Human Input: {'Yes' if input_params['human_input'] else 'No'}\n"
        f"- Include Value Chain Analysis: {'Yes' if input_params['value_chain_step'] else 'No'}\n"
        f"- Include Demand Signals: {'Yes' if input_params['demand_signals_step'] else 'No'}\n"
        f"- Include Supply Signals: {'Yes' if input_params['supply_signals_step'] else 'No'}\n"
        f"- Include Whitespace Identification: {'Yes' if input_params['whitespace_identification_step'] else 'No'}\n"
        f"- Job ID: {job_id}\n\n"
        "Please type 'yes' to confirm or 'no' to enter the information again."
    )
