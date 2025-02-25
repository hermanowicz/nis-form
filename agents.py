from agno.agent import Agent
from agno.models.groq import Groq
from agno.models.openai import OpenAIChat
from agno.knowledge.pdf import PDFKnowledgeBase, PDFReader
from agno.vectordb.lancedb import LanceDb
from agno.vectordb.search import SearchType
import os

vector_db = LanceDb(
    table_name="regulatory_docs",
    uri="./lancedb",
    search_type=SearchType.keyword
)

knowledge_base = PDFKnowledgeBase(
    path="pdf_docs/",
    vector_db=vector_db,
    reader=PDFReader(chunk=True),
)

agent = Agent(
    # to be added ollama binding
    model=OpenAIChat(id="gpt-4o", temperature=0.2, max_retries=3, api_key=os.getenv("OPEN_API_KEY")),
    knowledge=knowledge_base,
    debug_mode=True,
    search_knowledge=True,
    show_tool_calls=True,
    description="""You are proffesional legal advisor, with knowlage about EU and Ploish regulations About NIS 2 AND GDPR (RODO), always provide clear answear with links and document paragrafs from knowledge base which is required to suppoert your answears. Never Lie and if you are not sure tell that and redirect user to lawyer. Always try to responde in user language."""
)

if agent.knowledge is not None:
    agent.knowledge.load()

agent.print_response(
    "czy musze implementować NIS 2, jako mała firma w Warszawie zajmujaca sie web developmentem i administaracja sklepami online dla klientów z sektora SMB?", markdown=True, stream=True)
