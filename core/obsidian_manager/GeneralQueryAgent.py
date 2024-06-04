from pathlib import Path
from typing import List
from langchain.agents import Tool, initialize_agent, AgentType
from langchain.chat_models import ChatOpenAI
from langchain.prompts import MessagesPlaceholder, PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.schema import SystemMessage
from core.obsidian_manager.Constants import Constants
from core.obsidian_manager.MemgraphManager import MemgraphManager

constants = Constants()



class GeneralQueryAgent:
    def __init__(self, repo_path: str, tools: List[Tool]) -> None:
        self.repo_path = repo_path
        self.system_message = ''
        self._init_system_message()

        self.llm = ChatOpenAI(
            temperature=constants.LLM_MODEL_TEMPERATURE,
            openai_api_key=constants.OPENAI_API_KEY,
            model_name=constants.LLM_MODEL_NAME
        )

        self.agent_kwargs = {
            "extra_prompt_messages": [MessagesPlaceholder(variable_name="memory")],
            "system_message": self.system_message,
        }

        self.memory = ConversationBufferMemory(memory_key="memory", return_messages=True)

        self.run_cypher_query = Tool.from_function(
            func=MemgraphManager.select_query_tool,
            name="run_cypher_query",
            description="""Useful when you want to run Cypher queries on the knowledge graph. 
                            Note that the input has to be valid Cypher. Consult the graph schema in order to know how to write correct queries. 
                            Pay attention to the repo_path attribute.
                            Returns results of executing the query."""
        )

        self.tools = tools + [self.run_cypher_query]
        self._init_agent(self.tools)

    def _init_agent(self, tools: List[Tool]) -> None:
        self.agent = initialize_agent(
            tools,
            self.llm,
            agent=AgentType.OPENAI_FUNCTIONS,
            verbose=True,
            agent_kwargs=self.agent_kwargs,
            memory=self.memory
        )

    def _init_system_message(self) -> None:
        # Define the path to your prompt file explicitly
        prompt_name = 'system_message_query'
        prompt_path = Path('./core/knowledgebase/prompts') / prompt_name
        prompt_text = prompt_path.read_text()
        prompt_template = PromptTemplate.from_template(prompt_text)

        mm = MemgraphManager()
        schema = mm.get_schema_for_repo(self.repo_path)
        self.system_message = SystemMessage(
            content=prompt_template.format(schema=schema, repo_path=self.repo_path)
        )

    def ask(self, question: str) -> str:
        return self.agent.run(question)
