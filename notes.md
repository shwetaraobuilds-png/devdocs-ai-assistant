# DevDocs AI — Day 1 Notes

Today, I created a separate repository for **DevDocs AI**, a RAG-based developer documentation assistant focused on Stripe APIs.

The idea is to help developers ask questions in natural language and retrieve relevant information from Stripe documentation without manually searching through multiple pages.

I created a small knowledge base with six topics:

- API Authentication
- Test Mode and Live Mode
- PaymentIntents
- Idempotency
- API Errors
- Webhooks

The documentation was split into meaningful sections using Markdown headings. Each section became one chunk. This helped me understand that chunking is not just a technical step—it directly affects retrieval quality. A chunk should contain one complete topic and enough context to be useful on its own.

I used Voyage AI to create embeddings for all documentation chunks:

```text
6 documentation chunks
→ 6 embeddings
→ 1024 dimensions per embedding


I then created a separate query embedding for the developer’s question and used cosine similarity to compare it with all document embeddings.

The retrieval flow is:

Developer question
→ query embedding
→ cosine similarity
→ highest-scoring documentation section

The system successfully retrieved the correct section for questions about authentication, idempotency, API errors, PaymentIntents, test mode, and webhooks.

After retrieval, I passed the developer’s question and the best matching documentation chunk to Claude. Claude then generated a concise answer using only the retrieved context.

The complete RAG flow is:

Stripe documentation
→ chunking
→ document embeddings

Developer question
→ query embedding
→ semantic similarity
→ best matching chunk

Best matching chunk
+
developer question
→ Claude
→ grounded answer


I also tested an unsupported question:

Does Stripe support payments in Indian rupees?

The closest retrieved section was PaymentIntents, but the similarity score was low and the documentation did not contain the answer. The system correctly returned:

I could not find that information in the available documentation.

To improve this behavior, I added a relevance threshold:

RELEVANCE_THRESHOLD = 0.40

If the highest similarity score is below the threshold, the application does not treat the retrieved section as a valid source.

One important learning is that a vector search system will always return the closest result, even when none of the results are actually relevant. This means retrieval systems need an additional relevance check instead of blindly trusting the top result.

I faced and resolved a few technical issues:

Installed scikit-learn for cosine similarity.
Loaded API keys from .env using python-dotenv.
Corrected the active virtual environment.
Protected API keys using .gitignore.
Fixed duplicate answer output.
Fixed the source label for unsupported questions.
Hit Voyage AI rate limits because document embeddings were being recreated on every application run.

The next technical improvement is to separate ingestion from retrieval:

One-time ingestion:
Documentation
→ chunks
→ embeddings
→ save locally


Every developer question:
Question
→ query embedding
→ compare with saved embeddings
→ retrieve context
→ Claude answer

This will reduce API calls, avoid repeated document embedding, and move the project closer to a real production RAG architecture.

My key takeaway is that RAG is not simply sending documents to an LLM. It is a pipeline made up of chunking, embeddings, retrieval, relevance evaluation, prompt construction, grounded generation, and fallback handling.

The project is still small, but it already demonstrates an important developer-platform use case: reducing documentation search effort and helping developers find relevant integration guidance faster.


