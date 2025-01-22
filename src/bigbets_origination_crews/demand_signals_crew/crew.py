from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
import os
from bigbets_origination_crews.utils.output_utils import print_output
from crewai_tools import SerperDevTool, WebsiteSearchTool
from bigbets_origination_crews.chat_shared import chat_interface
from crewai.tasks.task_output import TaskOutput
from crewai import LLM

@CrewBase
class DemandSignalsCrew():
	"""DemandSignalsCrew crew"""

	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'
	current_step = "3. Demand Signals"
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
	def analysis_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['analysis_agent'],
			#tools=[WebsiteSearchTool()], 
			verbose=True,
			llm=self.llm
		)	

	@agent
	def synthesis_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['synthesis_agent'],
			#tools=[WebsiteSearchTool()], 
			verbose=True
		)

	@agent
	def trends_opportunities_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['trends_opportunities_agent'],
			# tools=[WebsiteSearchTool()], 
			verbose=True,
			llm=self.llm
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
	def final_customers_identification(self) -> Task:
		return Task(
			config=self.tasks_config['final_customers_identification'],
			callback=lambda output: print_output(output, self.output_dir, self.current_step, "1. Customers Identification"),
			human_input=self.human_input
		)

	@task
	def current_demand_behavior_analysis(self) -> Task:
		return Task(
			config=self.tasks_config['current_demand_behavior_analysis'],
			callback=lambda output: print_output(output, self.output_dir, self.current_step, "2. Demand Behavior Analysis"),
			human_input=self.human_input
		)

	@task
	def customer_challenges_pains_analysis(self) -> Task:
		return Task(
			config=self.tasks_config['customer_challenges_pains_analysis'],
			callback=lambda output: print_output(output, self.output_dir, self.current_step, "3. Challenges and Pains Analysis"),
			human_input=self.human_input
		)

	@task
	def social_listening_analysis(self) -> Task:
		return Task(
			config=self.tasks_config['social_listening_analysis'],
			callback=lambda output: print_output(output, self.output_dir, self.current_step, "4. Social Listening Analysis"),
			human_input=self.human_input
		)

	@task
	def current_pains_analysis(self) -> Task:
		return Task(
			config=self.tasks_config['current_pains_analysis'],
   			output_file=f"{self.output_dir}/output_raw/current_pains_analysis_report.md",
			callback=lambda output: print_output(output, self.output_dir, self.current_step, "5. Unmet Needs and Pains of Customers"),
			human_input=self.human_input
		)

	@task
	def current_behavior_changes_analysis(self) -> Task:
		return Task(
			config=self.tasks_config['current_behavior_changes_analysis'],
			callback=lambda output: print_output(output, self.output_dir, self.current_step, "6. Behavior Changes Analysis"),
			human_input=self.human_input
		)

	@task
	def emerging_consumption_needs_analysis(self) -> Task:
		return Task(
			config=self.tasks_config['emerging_consumption_needs_analysis'],
			callback=lambda output: print_output(output, self.output_dir, self.current_step, "7. Emerging Consumption Needs Analysis"),
			human_input=self.human_input
		)

	@task
	def consumption_trends_analysis(self) -> Task:
		return Task(
			config=self.tasks_config['consumption_trends_analysis'],
			output_file=f"{self.output_dir}/output_raw/consumption_trends_analysis_report.md",
			callback=lambda output: print_output(output, self.output_dir, self.current_step, "8. Behavior Change Signals Influencing the Value Chain"),
			human_input=self.human_input
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the DemandSignalsCrew crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)
