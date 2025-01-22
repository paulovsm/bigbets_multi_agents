
import os
import traceback
import bigbets_origination_crews.shared_state as shared_state
from bigbets_origination_crews.whitespace_identification_crew.crew import WhitespaceIdentificationCrew

def run_whitespace_crew(input_params, output_dir, chat_interface):
    if shared_state.loading_message is not None:
        chat_interface.remove(shared_state.loading_message)
        shared_state.loading_message = None

    try:
        with open(f"{output_dir}/output_raw/value_chain_analysis_report_merged.md", 'r', encoding='utf-8') as file:
            value_chain_report_content = file.read()
            
        with open(f"{output_dir}/output_raw/current_future_opportunities_analysis_report.md", 'r', encoding='utf-8') as current_future_opportunities_analysis_report_file:
            current_future_opportunities_analysis_report_content = current_future_opportunities_analysis_report_file.read()

        with open(f"{output_dir}/output_raw/ongoing_changes_signals_analysis_report.md", 'r', encoding='utf-8') as ongoing_changes_signals_analysis_report_file:
            ongoing_changes_signals_analysis_reportcontent = ongoing_changes_signals_analysis_report_file.read()
            
        with open(f"{output_dir}/output_raw/current_pains_analysis_report.md", 'r', encoding='utf-8') as current_pains_analysis_report_file:
            current_pains_analysis_report_content = current_pains_analysis_report_file.read()
            
        with open(f"{output_dir}/output_raw/consumption_trends_analysis_report.md", 'r', encoding='utf-8') as consumption_trends_analysis_report_file:
            consumption_trends_analysis_report_content = consumption_trends_analysis_report_file.read()

        inputs = {
            "target_industry": input_params["target_industry"],
            "target_region": input_params["target_region"],
            "top_players": input_params["top_players"],
            "value_chain_analysis": value_chain_report_content,
            "current_future_opportunities": current_future_opportunities_analysis_report_content,
            "ongoing_changes_signals": ongoing_changes_signals_analysis_reportcontent,
            "current_pains": current_pains_analysis_report_content,
            "consumption_trends": consumption_trends_analysis_report_content
        }
        
        if not input_params["whitespace_identification_step"]:
            chat_interface.send(
                "The **Whitespace Identification Crew** step will be skipped.",
                user="Assistant",
                respond=False
            )
            chat_interface.send(
                "I have finished the Big Bets Origination process. You can start a new process by typing a new industry.",
                user="Assistant",
                respond=False
            )
            shared_state.current_crew = None
            return
        else:
            chat_interface.send(
                "Now using the **Supply and Demand Signals**, I will start the **Whitespace Identification Crew**. Please wait a moment...",
                user="Assistant",
                respond=False
            )

            crew_instance = WhitespaceIdentificationCrew(output_dir, input_params["human_input"]).crew()
            shared_state.current_crew = crew_instance
            crew_instance.kickoff(inputs=inputs)
            chat_interface.send(
                "I have finished the Big Bets Origination process. You can start a new process by typing a new industry.",
                user="Assistant",
                respond=False
            )
            shared_state.current_crew = None

    except Exception as e:
        error_message = traceback.format_exc()
        print(error_message)
        chat_interface.send(f"An error occurred: {e}", user="Assistant", respond=False)
        shared_state.current_crew = None