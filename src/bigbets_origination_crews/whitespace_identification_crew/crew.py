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
		model=os.getenv('MODEL'),
	)

	search_llm = LLM(
		model=os.getenv('SEARCH_MODEL'),
	)

	def __init__(self, output_dir, human_input=False):
		self.output_dir = output_dir
		self.human_input = human_input

	#################################################### AGENTS ####################################################
	@agent
	def industry_expert_consultant(self) -> Agent:
		return Agent(
			config=self.agents_config['industry_expert_consultant'],
			#tools=[SerperDevTool()], 
			verbose=True,
			llm=self.llm
		)

	@agent
	def financial_modeling_specialist(self) -> Agent:
		return Agent(
			config=self.agents_config['financial_modeling_specialist'],
			#tools=[WebsiteSearchTool()],
			#allow_code_execution=True,
			verbose=True,
			llm=self.search_llm
		)

	@agent
	def editorial_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['editorial_agent'],
			verbose=True,
			llm=self.llm
		)

	#################################################### Tasks ####################################################

	@task
	def identify_niche_emerging_markets(self) -> Task:
		return Task(
			config=self.tasks_config['identify_niche_emerging_markets'],
			callback=lambda output: print_output(output, self.output_dir, self.current_step, "1. Identify Niche and Emerging Markets (Potential Whitespaces)"),
			human_input=self.human_input
		)

	@task
	def qualify_potential_whitespaces(self) -> Task:
		return Task(
			config=self.tasks_config['qualify_potential_whitespaces'],
			callback=lambda output: print_output(output, self.output_dir, self.current_step, "2. Qualify Potential Whitespaces"),
			human_input=self.human_input
		)

	@task
	def calculate_potential_addressable_market(self) -> Task:
		return Task(
			config=self.tasks_config['calculate_potential_addressable_market'],
			callback=lambda output: print_output(output, self.output_dir, self.current_step, "3. Calculate Potential Addressable Market"),
			human_input=self.human_input
		)

	@task
	def complete_report_mapped_whitespaces(self) -> Task:
		return Task(
			config=self.tasks_config['complete_report_mapped_whitespaces'],
			output_file=f"{self.output_dir}/output_raw/whitespace_complete_report.md",
			callback=lambda output: print_output(output, self.output_dir, self.current_step, "4. Mapped Whitespaces Complete Report"),
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
