import os
import traceback
import bigbets_origination_crews.shared_state as shared_state
from bigbets_origination_crews.demand_signals_crew.crew import DemandSignalsCrew

def run_demand_crew(input_params, output_dir, chat_interface, run_whitespace_crew):
    if shared_state.loading_message is not None:
        chat_interface.remove(shared_state.loading_message)
        shared_state.loading_message = None

    try:
        with open(f"{output_dir}/output_raw/value_chain_analysis_report_merged.md", 'r', encoding='utf-8') as file:
            value_chain_report_content = file.read()
            
        with open(f"{output_dir}/output_raw/industry_key_players_report.md", 'r', encoding='utf-8') as file:
            industry_key_players_report_content = file.read()
            
        inputs = {
            "target_industry": input_params["target_industry"],
            "target_region": input_params["target_region"],
            "top_players": input_params["top_players"],
            "value_chain_analysis": value_chain_report_content,
            "industry_key_players": industry_key_players_report_content
        }
        
        if not input_params["demand_signals_step"]:
            chat_interface.send(
                "The **Demand Signals Crew** step will be skipped.",
                user="Assistant",
                respond=False
            )
            # Chamar diretamente run_whitespace_crew pois é o último da cadeia
            run_whitespace_crew(input_params, output_dir, chat_interface)
            return
        else:
            chat_interface.send(
                "Also, using the **Value Chain Analysis**, I will start the **Demand Signals Crew**. Please wait a moment...",
                user="Assistant",
                respond=False
            )

            crew_instance = DemandSignalsCrew(output_dir, input_params["human_input"]).crew()
            shared_state.current_crew = crew_instance
            crew_instance.kickoff(inputs=inputs)

            # Chamar diretamente run_whitespace_crew pois é o último da cadeia
            run_whitespace_crew(input_params, output_dir, chat_interface)

    except Exception as e:
        error_message = traceback.format_exc()
        print(error_message)
        chat_interface.send(f"An error occurred: {e}", user="Assistant", respond=False)
        shared_state.current_crew = None