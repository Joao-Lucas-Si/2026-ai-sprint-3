from dotenv import load_dotenv
load_dotenv()
from evals.comparativo import avaliar_comparativo
from evals.ragas import avaliar


avaliar_comparativo()