from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
#from langchain_openai import ChatOpenAI

from markdown import markdown
import pdfkit

# Uncomment the following line to use an example of a custom tool
# from research_crew.tools.custom_tool import MyCustomTool

# Check our tools documentations for more information on how to use them
from crewai_tools import SerperDevTool, WebsiteSearchTool

from bigbets_origination_crews.chat_shared import chat_interface

from crewai.tasks.task_output import TaskOutput

def print_output(output: TaskOutput):

	message = output.raw
	chat_interface.send(message, user=output.agent, respond=False)
	
	html_content = markdown(output.raw, extensions=['markdown_tables_extended'])
 
	agent_name = output.agent
	# remove spaces, breaklines and special characters
	agent_name = agent_name.replace("\n", "").replace("\r", "").replace("\t", "") 
	
	output_pdf_path = f"output/Supply Signals_{agent_name}.pdf" 
	
	# Save the PDF
	pdfkit.from_string(html_content, output_pdf_path)


@CrewBase
class SupplySignalsCrew():
	"""SupplySignalsCrew crew"""

	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

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
	def market_intelligence_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['market_intelligence_agent'],
			#tools=[WebsiteSearchTool()], 
			verbose=True
		)	

	@agent
	def disruption_analyst_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['disruption_analyst_agent'],
			#tools=[WebsiteSearchTool()], 
			verbose=True
		)

	@agent
	def supply_distribution_analyst_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['supply_distribution_analyst_agent'],
			#tools=[WebsiteSearchTool()], 
			verbose=True
		)

	@agent
	def trend_analyst_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['trend_analyst_agent'],
			#tools=[WebsiteSearchTool()], 
			verbose=True
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
	def market_intelligence_analysis_task(self) -> Task:
		return Task(
			config=self.tasks_config['market_intelligence_analysis_task'],
			callback=print_output,
			human_input=True
		)

	@task
	def disruption_analysis_task(self) -> Task:
		return Task(
			config=self.tasks_config['disruption_analysis_task'],
			callback=print_output,
			human_input=True
		)

	@task
	def supply_distribution_analysis_task(self) -> Task:
		return Task(
			config=self.tasks_config['supply_distribution_analysis_task'],
			callback=print_output,
			human_input=True
		)

	@task
	def trend_analysis_task(self) -> Task:
		return Task(
			config=self.tasks_config['trend_analysis_task'],
			callback=print_output,
			human_input=True
		)

	@task
	def insight_generation_task(self) -> Task:
		return Task(
			config=self.tasks_config['insight_generation_task'],
			callback=print_output,
			human_input=True
		)

	@task
	def editorial_task(self) -> Task:
		return Task(
			config=self.tasks_config['editorial_task'],
			output_file='output_raw/supply_signals_report.md',
			callback=print_output,
			human_input=True
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the SupplySignalsCrew crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			#planning=True,
			#manager_llm=ChatOpenAI(temperature=0, model="gpt-4o-mini"),
			#process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)
