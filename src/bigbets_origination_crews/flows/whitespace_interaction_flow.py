import time
import traceback
import os
import shutil
from crewai import Agent, Task, Crew, Process
import bigbets_origination_crews.shared_state as shared_state
from crewai.knowledge.source.crew_docling_source import CrewDoclingSource
from crewai import LLM

def run_whitespace_interaction_flow(output_dir, input_params, chat_interface, job_id):
    try:
        chat_interface.send(
            f"Starting interaction **{input_params['target_industry']}** with whitespace knowledge base...",
            user="Assistant",
            respond=False
        )
        
        # Set human_input to True to force the crew to ask for human input for this flow
        input_params["human_input"] = True
        
        # Set the shared state to capture user input
        shared_state.is_capturing_input = True
        
        # Request user query
        chat_interface.send(
            "Please enter your query to interact with the knowledge base:",
            user="Assistant",
            respond=False
        )
        
        # Wait for user response
        shared_state.user_input = None
        while shared_state.user_input is None:
            time.sleep(1)
        user_query = shared_state.user_input
        shared_state.user_input = None

        # Add query to inputs and start crew
        inputs = input_params.copy()
        inputs["user_query"] = user_query
        
        # List all files in the Job ID output_raw directory to be used as input the Knowledge Source
        source_dir = os.path.join(output_dir, "output_raw")
        source_files = [os.path.join(source_dir, f) for f in os.listdir(source_dir) if os.path.isfile(os.path.join(source_dir, f))]
        
        # Create a copy of the source files in the 'knowledge/{job_id}' directory. Create the directory if it doesn't exist.
        knowledge_dir = os.path.join("knowledge", job_id)
        os.makedirs(knowledge_dir, exist_ok=True)
        for source_file in source_files:
            shutil.copy(source_file, knowledge_dir)
        
        # Create a list of file paths relatative to 'knowledge' to be used as input for the Knowledge Source
        file_paths = [os.path.join(job_id, os.path.basename(f)) for f in source_files]
        
        # Create a knowledge source
        whitespace_content_source = CrewDoclingSource(
            file_paths=file_paths,
        )
        
        llm = LLM(
            model="gpt-4o-mini", 
            temperature=0
        )
        
        # Create an agent with the knowledge store
        agent = Agent(
            role="Whitespace Expert",
            goal="""
                You know everything about {target_industry} whitespaces and can answer any question or queries using your knowledge. 
                You must provide the best possible answers to the user queries.
            """,
            backstory="""
                You are a master in whitespace identification and have access to all the information extracted from the previous researches. 
                You can use this information to answer any question about the whitespace identification process.
            """,
            verbose=True,
            allow_delegation=False,
            llm="gpt-4",
        )
        
        task = Task(
            description="""
                Using the information extracted from the previous researches, answer the user query about whitespace.
                Think about the best way to structure the answer and provide the most relevant information.
                Think step by step to provide a well-structured answer.
                
                The user query is: {user_query}
            """,
            expected_output="""
                A detailed and well-structured answer to the user query.                    
            """,
            agent=agent,
            human_input=input_params["human_input"],
        )

        crew_instance = Crew(
            agents=[agent],
            tasks=[task],
            verbose=True,
            process=Process.sequential,
            knowledge_sources=[
                whitespace_content_source
            ],
        )
        
        shared_state.current_crew = crew_instance
        crew_instance.kickoff(inputs=inputs)
        
        shared_state.current_crew = None
        shared_state.is_capturing_input = False
        
    except Exception as e:
        error_message = traceback.format_exc()
        print(error_message)
        chat_interface.send(f"Error starting interaction: {e}", user="Assistant", respond=False)
        shared_state.current_crew = None
