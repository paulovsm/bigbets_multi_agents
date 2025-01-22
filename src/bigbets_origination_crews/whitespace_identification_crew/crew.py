from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
import os
from bigbets_origination_crews.utils.output_utils import print_output
from crewai_tools import SerperDevTool, WebsiteSearchTool
from bigbets_origination_crews.chat_shared import chat_interface
from crewai.tasks.task_output import TaskOutput
from crewai import LLM

@CrewBase
class WhitespaceIdentificationCrew():
	"""WhitespaceIdentificationCrew crew"""

	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'
	current_step = "4. Whitespaces"
	llm = LLM(
		model=os.getenv('SEARCH_MODEL'),
	)

	def __init__(self, output_dir, human_input=False):
		self.output_dir = output_dir
		self.human_input = human_input

	#################################################### AGENTS ####################################################
	@agent
	def retrieval_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['retrieval_agent'],
			tools=[SerperDevTool()], 
			verbose=True
		)

	@agent
	def website_collector_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['website_collector_agent'],
			tools=[WebsiteSearchTool()], 
			verbose=True
		)

	@agent
	def market_niches_analyst_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['market_niches_analyst_agent'],
			#tools=[WebsiteSearchTool()], 
			verbose=True,
			llm=self.llm
		)	

	@agent
	def opportunity_identification_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['opportunity_identification_agent'],
			#tools=[WebsiteSearchTool()], 
			verbose=True,
			llm=self.llm
		)

	@agent
	def whitespaces_identification_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['whitespaces_identification_agent'],
			#tools=[WebsiteSearchTool()], 
			verbose=True,
			llm=self.llm
		)

	@agent
	def insight_specialist_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['insight_specialist_agent'],
			#tools=[WebsiteSearchTool()], 
			verbose=True
		)

	@agent
	def editorial_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['editorial_agent'],
			verbose=True
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
	def market_niches_analysis_task(self) -> Task:
		return Task(
			config=self.tasks_config['market_niches_analysis_task'],
			callback=lambda output: print_output(output, self.output_dir, self.current_step, "1. Market Niches Analysis"),
			human_input=self.human_input
		)

	@task
	def opportunity_identification_task(self) -> Task:
		return Task(
			config=self.tasks_config['opportunity_identification_task'],
			callback=lambda output: print_output(output, self.output_dir, self.current_step, "2. Opportunities Identification"),
			human_input=self.human_input
		)

	@task
	def whitespaces_identification_task(self) -> Task:
		return Task(
			config=self.tasks_config['whitespaces_identification_task'],
			callback=lambda output: print_output(output, self.output_dir, self.current_step, "3. Whitespaces Identification"),
			human_input=self.human_input
		)

	@task
	def insight_generation_task(self) -> Task:
		return Task(
			config=self.tasks_config['insight_generation_task'],
			callback=lambda output: print_output(output, self.output_dir, self.current_step, "4. Insights and Strategic Implications"),
			human_input=self.human_input
		)

	@task
	def editorial_task(self) -> Task:
		return Task(
			config=self.tasks_config['editorial_task'],
			output_file=f"{self.output_dir}/output_raw/whitespace_identification_report.md",
			callback=lambda output: print_output(output, self.output_dir, self.current_step, "5. Whitespaces Final Report"),
			human_input=self.human_input
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the WhitespaceIdentificationCrew crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)
