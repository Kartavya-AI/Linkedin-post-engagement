from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from src.crew.tools.linkedin import (
    linkedin_get_profile, 
    linkedin_get_posts, 
    linkedin_share_post
)
from dotenv import load_dotenv
import os

load_dotenv()

# Set the API key for Gemini
os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")

llm = LLM(
    model="gemini/gemini-2.0-flash"
)
@CrewBase
class LinkedinCrew:
    """LinkedIn automation crew for content discovery and engagement strategy."""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def linkedin_query_strategist(self) -> Agent:
        """Create LinkedIn query strategist agent."""
        return Agent(
            config=self.agents_config['linkedin_query_strategist'],
            tools=[],  # No tools needed for query creation
            verbose=True,
            llm=llm
        )

    @agent
    def linkedin_data_collector(self) -> Agent:
        """Create LinkedIn data collector agent."""
        return Agent(
            config=self.agents_config['linkedin_data_collector'],
            tools=[linkedin_get_posts],  # Only the posts collection tool
            verbose=True,
            llm=llm
        )

    @agent
    def linkedin_engagement_creator(self) -> Agent:
        """Create LinkedIn engagement creator agent."""
        return Agent(
            config=self.agents_config['linkedin_engagement_creator'],
            tools=[],  # No tools needed for comment creation
            verbose=True,
            llm=llm
        )

    @task
    def query_strategy_task(self) -> Task:
        """Create LinkedIn query strategy task."""
        return Task(
            config=self.tasks_config['query_strategy_task'],
            agent=self.linkedin_query_strategist()
        )

    @task
    def data_collection_task(self) -> Task:
        """Create LinkedIn data collection task."""
        return Task(
            config=self.tasks_config['data_collection_task'],
            agent=self.linkedin_data_collector(),
            context=[self.query_strategy_task()]
        )

    @task
    def engagement_creation_task(self) -> Task:
        """Create LinkedIn engagement creation task."""
        return Task(
            config=self.tasks_config['engagement_creation_task'],
            agent=self.linkedin_engagement_creator(),
            context=[self.data_collection_task()]
        )

    @crew
    def crew(self) -> Crew:
        """Create the LinkedIn automation crew."""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            memory=False,  # Disable memory to avoid OpenAI dependency
            manager_llm=llm  # Use Gemini for any crew-level operations
        )
