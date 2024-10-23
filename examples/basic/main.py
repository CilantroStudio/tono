import openai
from tono import Agent, OpenAICompletionClient
from tono.tools import http_request, write_code_to_file

# Instantiate an openai client using our adapter
client = OpenAICompletionClient(openai.Client(api_key="abc"))
# agent creation
Agent.group_chat = ["some general messages"]
agent = Agent(client, tools=[write_code_to_file, http_request])
# run the agent
agent.start(
    "Use google to find the top 10 news items for today and write a summary for me in markdown."
)
