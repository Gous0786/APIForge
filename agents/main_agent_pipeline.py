# agents/main_agent_pipeline.py

import os
from google.adk.agents import SequentialAgent, LlmAgent
from google.adk.tools import google_search  # You can also define it inline

# ---------- 1. Search Agent ----------

request_analyzer = LlmAgent(
    name="RequestAnalyzerAgent",
    model="gemini-2.0-flash",
    description="Analyzes the user prompt and refines it into a clear development task with metadata.",
    instruction=(
        "Parse the user's request and extract:\n"
        "- Target API or SDK\n"
        "- Language or framework\n"
        "- Action/goal\n"
        "- Output type (component, CLI, backend, etc.)\n"
        "Output a refined task summary for other agents."
    ),
)

search_agent = LlmAgent(
    name="SearchAgent",
    model="gemini-2.0-flash",
    description="Performs a Google search to find relevant API documentation and examples.",
    tools=[google_search],
    instruction=(
         "You are a search and documentation synthesis agent. Based on the user's request, "
    "generate a high-quality search query and use the google_search tool to fetch top documentation pages. "
    "Then, based on the search results and your own knowledge, extract or reconstruct the most relevant parts of the documentation, "
    "such as API endpoints, parameters, setup steps, and code examples. "
    "Your output should include only the synthesized documentation content needed to fulfill the user's coding request. "
    "Do not return links or search metadata. The output should look like an excerpt from an API doc or tutorial, not a search result."
    ),
)


# ---------- 3. Context Builder Agent ----------
context_builder_agent = LlmAgent(
    name="ContextBuilderAgent",
    model="gemini-2.0-flash",
    description="Cleans, deduplicates, and organizes scraped data into a usable context for code generation.",
    instruction=(
        "You are a context refiner. You take raw scraped content and organize it into a clean, well-structured "
        "technical summary including API endpoints, parameters, usage patterns, and authentication mechanisms."
    ),
)
instruction_agent = LlmAgent(
    name="InstructionAgent",
    model="gemini-2.0-flash",
    description="Explains the implementation steps for the user before showing the code.",
    instruction=(
        "Given the cleaned documentation and the user’s request, outline the implementation plan "
        "in clear, logical steps. Avoid generating any code."
    ),
)


# ---------- 4. Code Generator Agent ----------
code_generator_agent = LlmAgent(
    name="CodeGeneratorAgent",
    model="gemini-2.0-flash",
    description="Generates code based on the user request and the final cleaned API context.",
    instruction=(
      "You are an expert software engineer. Generate clean, working code based on the user’s request and the provided API documentation context. "
        "The code should be well-commented, production-ready, and focus only on what was asked." 
        "use google_search to find any information for you code like proper imports , libraries , api docs, etc. "
        "dont generate code elements like imports etc based on assumptions, only do it if you dont find any thing on web , also mention it"

    ),
    tools=[google_search],
)


# --- Enhanced Sequential Agent Pipeline ---
root_agent = SequentialAgent(
    name="ApiIntegrationPipeline",
    sub_agents=[
        request_analyzer,
        search_agent,
        context_builder_agent,
        instruction_agent,
        code_generator_agent
    ],
    description=(
        "Production-ready API integration pipeline that searches for documentation, "
        "extracts key integration details, generates secure and maintainable code, "
        "and delivers a complete integration package ready for immediate use."
    ),
    
)

__all__ = ['root_agent']   
