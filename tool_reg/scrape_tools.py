from . import tool_registry  # Import the singleton instance

import os
import json
from squadai.agent import Agent
from squadai.task import Task
from squadai.squad import Squad
from langchain.tools import tool
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from firecrawl.firecrawl import FirecrawlApp

load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")
firecrawl_api_key = os.getenv("FIRECRAWL_API_KEY")
llm = ChatGroq(api_key=groq_api_key, model="llama-3.1-70b-versatile")
firecrawl_app = FirecrawlApp(api_key=firecrawl_api_key)

class BrowserTools():

    @tool("Scrape website content")
    def scrape_and_summarize_website(website):
        """Useful to scrape and summarize website content."""
        
        # Fetch the website content using Firecrawl
        scrape_result = firecrawl_app.scrape_url(website)
        if not scrape_result or 'markdown' not in scrape_result:
            return f"Failed to retrieve content from {website}"
        
        content = scrape_result['markdown']
        
        # Split the content into chunks if it's too long
        content_chunks = [content[i:i + 8000] for i in range(0, len(content), 8000)]
        summaries = []
        
        for chunk in content_chunks:
            # Define the agent and task
            agent = Agent(
                role='Principal Researcher',
                goal='Do amazing research and summaries based on the content you are working with',
                backstory="You're a Principal Researcher at a big company and you need to do research about a given topic.",
                allow_delegation=False,
                llm=llm
            )
            task = Task(
                agent=agent,
                description=f'Analyze and summarize the content below, make sure to include the most relevant information in the summary. Return only the summary, nothing else.\n\nCONTENT\n----------\n{chunk}',
                expected_output="Analysis and summary of scraped web content."
            )
            # Execute the task and get the summary
            squad = Squad(
                    agents=[agent],
                    tasks=[task],
                    verbose=False
                    )
            summary = str(squad.kickoff())
            summaries.append(summary)
        
        return "\n\n".join(summaries)

