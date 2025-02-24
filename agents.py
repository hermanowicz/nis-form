from agno.agent import Agent
from agno.models.ollama import Ollama
# from agno.models.openai import OpenAIChat
from agno.knowledge.pdf import PDFKnowledgeBase, PDFReader
from agno.vectordb.lancedb import LanceDb
from agno.vectordb.search import SearchType

vector_db = LanceDb(
    table_name="regulatory_docs",
    uri="./lancedb",
    search_type=SearchType.keyword
)

knowledge_base = PDFKnowledgeBase(
    path="pdf_docs/",
    # urls=["./pdf_docs/ustawa_o_cyberbezpieczenstwie.pdf",
    #       "./pdf_docs/CELEX_2022_L2555_Text.pdf", "./pdf_docs/DPA_May_10_2018.pdf",],
    vector_db=vector_db,
    reader=PDFReader(chunk=True),
)

agent = Agent(
    # to be added ollama binding
    model=Ollama(id="command-r7b:latest", host="localhost:11434"),
    knowledge=knowledge_base,
    search_knowledge=True,
    debug_mode=True,
    show_tool_calls=True,
    description="""You are proffesional legal advisor, with knowlage about EU and Ploish regulations About NIS 2 AND GDPR (RODO), always provide clear answear with links and document paragrafs from knowledge base to suppoert your answears. Never Lie and if you are not sure tell that and redirect user to lawyer."""
)

if agent.knowledge is not None:
    agent.knowledge.load(upsert=True)

agent.print_response(
    "Will I need implement NIS 2 as small buisnes providing server administration services to SMB in my city?", markdown=True)
