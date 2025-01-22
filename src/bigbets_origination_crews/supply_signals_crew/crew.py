from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
import os
from bigbets_origination_crews.utils.output_utils import print_output
from crewai_tools import SerperDevTool, WebsiteSearchTool
from bigbets_origination_crews.chat_shared import chat_interface
from crewai.tasks.task_output import TaskOutput
from crewai import LLM

@CrewBase
class SupplySignalsCrew():
	"""SupplySignalsCrew crew"""

	def __init__(self, output_dir, human_input=False):
		self.output_dir = output_dir
		self.human_input = human_input

	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'
	current_step = "2. Supply Signals"
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
			llm=self.llm
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
	def market_players_analysis(self) -> Task:
		return Task(
			config=self.tasks_config['market_players_analysis'],
			callback=lambda output: print_output(output, self.output_dir, self.current_step, "1. Market Players Analysis"),
			human_input=self.human_input
		)

	@task
	def porter_six_forces_analysis(self) -> Task:
		return Task(
			config=self.tasks_config['porter_six_forces_analysis'],
			callback=lambda output: print_output(output, self.output_dir, self.current_step, "2. Porter Six Forces Analysis"),
			human_input=self.human_input
		)

	@task
	def strategic_priorities_investments_analysis(self) -> Task:
		return Task(
			config=self.tasks_config['strategic_priorities_investments_analysis'],
			callback=lambda output: print_output(output, self.output_dir, self.current_step, "3. Strategic Priorities and Investments Analysis"),
			human_input=self.human_input
		)

	@task
	def global_vs_local_outlook_analysis(self) -> Task:
		return Task(
			config=self.tasks_config['global_vs_local_outlook_analysis'],
			callback=lambda output: print_output(output, self.output_dir, self.current_step, "4. Global vs Local Outlook Analysis"),
			human_input=self.human_input
		)

	@task
	def value_chain_current_oportunities_task(self) -> Task:
		return Task(
			config=self.tasks_config['value_chain_current_oportunities_task'],
			callback=lambda output: print_output(output, self.output_dir, self.current_step, "5. Major Pressures, Challenges, and Opportunities"),
			human_input=self.human_input
		)
  
	@task
	def ma_movements_analysis(self) -> Task:
		return Task(
			config=self.tasks_config['ma_movements_analysis'],
			callback=lambda output: print_output(output, self.output_dir, self.current_step, "6. M&A Movements Analysis"),
			human_input=self.human_input
		)
  
	@task
	def investment_vc_movements_analysis(self) -> Task:
		return Task(
			config=self.tasks_config['investment_vc_movements_analysis'],
			callback=lambda output: print_output(output, self.output_dir, self.current_step, "7. Investment and VC Movements Analysis"),
			human_input=self.human_input
		)
  
	@task
	def new_entrants_disruptors_analysis(self) -> Task:
		return Task(
			config=self.tasks_config['new_entrants_disruptors_analysis'],
			callback=lambda output: print_output(output, self.output_dir, self.current_step, "8. New Entrants and Disruptors Analysis"),
			human_input=self.human_input
		)
  
	@task
	def follow_the_money_task(self) -> Task:
		return Task(
			config=self.tasks_config['follow_the_money_task'],
			callback=lambda output: print_output(output, self.output_dir, self.current_step, "9. Follow the Money"),
			human_input=self.human_input
		)
  
	@task
	def future_trends_analysis(self) -> Task:
		return Task(
			config=self.tasks_config['future_trends_analysis'],
			callback=lambda output: print_output(output, self.output_dir, self.current_step, "10. Future Trends Analysis"),
			human_input=self.human_input
		)
  
	@task
	def regulatory_changes_analysis(self) -> Task:
		return Task(
			config=self.tasks_config['regulatory_changes_analysis'],
			callback=lambda output: print_output(output, self.output_dir, self.current_step, "11. Regulatory Changes Analysis"),
			human_input=self.human_input
		)
  
	@task
	def emerging_technologies_analysis(self) -> Task:
		return Task(
			config=self.tasks_config['emerging_technologies_analysis'],
			callback=lambda output: print_output(output, self.output_dir, self.current_step, "12. Emerging Technologies Analysis"),
			human_input=self.human_input
		)
  
	@task
	def inspiring_startups_analysis(self) -> Task:
		return Task(
			config=self.tasks_config['inspiring_startups_analysis'],
			callback=lambda output: print_output(output, self.output_dir, self.current_step, "13. Inspiring Startups Analysis"),
			human_input=self.human_input
		)
  
	@task
	def future_trends_task(self) -> Task:
		return Task(
			config=self.tasks_config['future_trends_task'],
			callback=lambda output: print_output(output, self.output_dir, self.current_step, "14. Analysis of Key Trends"),
			human_input=self.human_input
		)
  
	@task
	def current_future_opportunities_analysis(self) -> Task:
		return Task(
			config=self.tasks_config['current_future_opportunities_analysis'],
			output_file=f"{self.output_dir}/output_raw/current_future_opportunities_analysis_report.md",
			callback=lambda output: print_output(output, self.output_dir, self.current_step, "15. Major Current and Future Opportunities Analysis"),
			human_input=self.human_input
		)
  
	@task
	def ongoing_changes_signals_analysis(self) -> Task:
		return Task(
			config=self.tasks_config['ongoing_changes_signals_analysis'],
			output_file=f"{self.output_dir}/output_raw/ongoing_changes_signals_analysis_report.md",
			callback=lambda output: print_output(output, self.output_dir, self.current_step, "16. Signals of Ongoing Changes Analysis"),
			human_input=self.human_input
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
