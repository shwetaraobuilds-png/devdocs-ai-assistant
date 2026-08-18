from dotenv import load_dotenv
from sklearn.metrics.pairwise import cosine_similarity
import anthropic
import voyageai

# Load API keys from the .env file
load_dotenv()

# --------------------------------------------------
# 1. Read the Stripe developer documentation
# --------------------------------------------------

with open("data/stripe_docs.md", "r", encoding="utf-8") as file:
    documentation = file.read()

# --------------------------------------------------
# 2. Split the documentation into meaningful chunks
# --------------------------------------------------

raw_sections = documentation.split("## ")

chunks = []

for section in raw_sections:
    section = section.strip()

    if section:
        chunks.append("## " + section)

print("Number of chunks:", len(chunks))

# Optional: print only the title of each chunk
for index, chunk in enumerate(chunks):
    print(index, chunk.splitlines()[0])

# --------------------------------------------------
# 3. Create embeddings for the documentation chunks
# --------------------------------------------------

voyage_client = voyageai.Client()

document_embedding_result = voyage_client.embed(
    chunks,
    model="voyage-4-lite",
    input_type="document"
)

knowledge_base_embeddings = document_embedding_result.embeddings

print("\nNumber of embeddings:", len(knowledge_base_embeddings))
print("Embedding dimensions:", len(knowledge_base_embeddings[0]))

# --------------------------------------------------
# 4. Ask the developer a question
# --------------------------------------------------

user_question = input("\nAsk a Stripe API question: ").strip()

# Basic input validation
if not user_question:
    print("\nPlease enter a question.")
    raise SystemExit

# --------------------------------------------------
# 5. Create an embedding for the developer's question
# --------------------------------------------------

question_embedding_result = voyage_client.embed(
    [user_question],
    model="voyage-4-lite",
    input_type="query"
)

question_embedding = question_embedding_result.embeddings[0]

# --------------------------------------------------
# 6. Compare the question with all documentation chunks
# --------------------------------------------------

similarities = cosine_similarity(
    [question_embedding],
    knowledge_base_embeddings
)

best_match_index = similarities[0].argmax()
best_match_score = similarities[0][best_match_index]
best_matching_chunk = chunks[best_match_index]

print("\nSimilarity scores:")
print(similarities)

print("\nBest match index:", best_match_index)
print("Best match score:", best_match_score)

print("\nBest matching documentation section:")
print(best_matching_chunk)

# --------------------------------------------------
# 7. Decide whether the retrieved section is relevant
# --------------------------------------------------

RELEVANCE_THRESHOLD = 0.40

if best_match_score < RELEVANCE_THRESHOLD:
    final_answer = (
        "I could not find that information in the available documentation."
    )
    source_title = "No relevant documentation found"

else:
    # --------------------------------------------------
    # 8. Send the retrieved context to Claude
    # --------------------------------------------------

    claude_client = anthropic.Anthropic()

    prompt = f"""
You are DevDocs AI, an assistant that helps developers understand
Stripe API documentation.

Answer the developer's question using only the documentation context
provided below.

Rules:
1. Use only facts explicitly stated in the documentation context.
2. Do not use outside knowledge.
3. Do not add assumptions or unsupported conclusions.
4. Keep the answer clear and concise.
5. Include relevant technical details such as headers, error codes,
   statuses, or API concepts when they appear in the context.
6. If the context does not contain the answer, respond exactly with:
   "I could not find that information in the available documentation."

Documentation context:
{best_matching_chunk}

Developer question:
{user_question}

Answer:
"""

    response = claude_client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=300,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    final_answer = response.content[0].text
    source_title = best_matching_chunk.splitlines()[0].replace("## ", "")

# --------------------------------------------------
# 9. Display the final answer and source
# --------------------------------------------------

print("\n" + "=" * 60)
print("DevDocs AI answer:")
print(final_answer)

print("\nSource section:")
print(source_title)

