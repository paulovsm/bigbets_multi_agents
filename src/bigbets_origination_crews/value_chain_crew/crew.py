from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
import os
from bigbets_origination_crews.utils.output_utils import print_output
from crewai_tools import SerperDevTool, WebsiteSearchTool, DirectorySearchTool
from bigbets_origination_crews.chat_shared import chat_interface
from crewai.tasks.task_output import TaskOutput
from crewai import LLM

@CrewBase
class ResearchCrew():

	"""ResearchCrew crew"""

	def __init__(self, output_dir, human_input=False):
		self.output_dir = output_dir
		self.human_input = human_input

	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'
	current_step = "1. Value Chain"
	llm = LLM(
		model=os.getenv('SEARCH_MODEL'),
	)

	#################################################### AGENTS ####################################################
	@agent
	def retrieval_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['retrieval_agent'],
			tools=[SerperDevTool()], 
			verbose=True,
		)

	@agent
	def website_collector_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['website_collector_agent'],
			#tools=[OnlineContentReadTool(directory="scraped_pages")], 
			verbose=True
		)

	@agent
	def industry_research_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['industry_research_agent'],
			# tools=[self.directory_search_tool], 
			verbose=True,
			llm=self.llm
		)

	@agent
	def data_analyst_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['data_analyst_agent'],
			# tools=[WebsiteSearchTool()], 
			verbose=True,
   			llm=self.llm
		)

	@agent
	def value_chain_specialist_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['value_chain_specialist_agent'],
			# tools=[WebsiteSearchTool()], 
			verbose=True,
			llm=self.llm
		)

	@agent
	def editorial_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['editorial_agent'],
			verbose=True,
			#llm=self.llm
		)

	#################################################### Tasks ####################################################

	# @task
	# def retrieval_task(self) -> Task:
	# 	return Task(
	# 		config=self.tasks_config['retrieval_task'],
	# 		callback=print_output,
	# 		human_input=True
	# 	)

	# @task
	# def website_collection_task(self) -> Task:
	# 	return Task(
	# 		config=self.tasks_config['website_collection_task'],
	# 		callback=print_output,
	# 		human_input=True
	# 	)

	@task
	def industry_key_players_task(self) -> Task:
		return Task(
			config=self.tasks_config['industry_key_players_task'],
			output_file=f"{self.output_dir}/output_raw/industry_key_players_report.md",
			callback=lambda output: print_output(output, self.output_dir, self.current_step, "1. Top Players"),
			human_input=self.human_input
		)

	@task
	def industry_research_task(self) -> Task:
		return Task(
			config=self.tasks_config['industry_research_task'],
			output_file=f"{self.output_dir}/output_raw/industry_research_task.md",
			callback=lambda output: print_output(output, self.output_dir, self.current_step, "2. Industry Research Report"),
			human_input=self.human_input
		)

	# @task
	# def data_analysis_task(self) -> Task:
	# 	return Task(
	# 		config=self.tasks_config['data_analysis_task'],
	# 		callback=print_output,
	# 		human_input=True
	# 	)

	@task
	def value_chain_analysis_task(self) -> Task:
		return Task(
			config=self.tasks_config['value_chain_analysis_task'],
   			output_file=f"{self.output_dir}/output_raw/value_chain_analysis_task.md",
			callback=lambda output: print_output(output, self.output_dir, self.current_step, "3. Value Chain Analysis"),
			human_input=self.human_input
		)

	@task
	def editorial_task(self) -> Task:
		return Task(
			config=self.tasks_config['editorial_task'],
			output_file=f"{self.output_dir}/output_raw/value_chain_analysis_report.md",
			callback=lambda output: print_output(output, self.output_dir, self.current_step, "4. Value Chain Final Report"),
			human_input=self.human_input
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the ResearchCrew crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			#process=Process.hierarchical,
			verbose=True,
			output_log_file="logs/value_chain_crew_logs.log",
			#planning=True,
			manager_llm="gemini/gemini-exp-1206",#ChatOpenAI(temperature=0, model="gpt-4o-mini"),
			#process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)
