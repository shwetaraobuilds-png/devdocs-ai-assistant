# DevDocs AI Assistant

DevDocs AI is a RAG-powered assistant that helps developers find answers from Stripe API documentation using natural-language questions.

The application retrieves the most relevant documentation section, checks whether the match is relevant enough, and then uses Claude to generate an answer grounded in the retrieved context.

## Problem

Developers often spend time searching across documentation pages, understanding unfamiliar terminology, and contacting support for repeated integration questions.

DevDocs AI explores how semantic retrieval and generative AI can make developer documentation easier to navigate.

## Current Features

- Curated Stripe developer documentation knowledge base
- Documentation chunking by topic
- Document and query embeddings using Voyage AI
- Semantic retrieval using cosine similarity
- Claude-generated answers grounded in retrieved documentation
- Source-section display
- Relevance threshold for low-confidence matches
- Fallback response for unsupported questions

## Documentation Topics

The current knowledge base includes:

- API Authentication
- Test Mode and Live Mode
- PaymentIntents
- Idempotency
- API Errors
- Webhooks

## Architecture

```text
Stripe documentation
→ meaningful chunks
→ document embeddings

Developer question
→ query embedding
→ cosine similarity
→ most relevant documentation section

Retrieved documentation
+
developer question
→ Claude
→ grounded answer


Example

Developer question:

How do I verify that a webhook really came from Stripe?

Retrieved section:

Webhooks

Generated answer:

Verify the signature in the Stripe-Signature header using the webhook
endpoint's signing secret before processing the event.

For unsupported questions, the assistant returns:

I could not find that information in the available documentation.
Tech Stack
Python
Voyage AI embeddings
Anthropic Claude
scikit-learn
python-dotenv
Project Structure
devdocs-ai-assistant/
├── app.py
├── README.md
├── notes.md
├── requirements.txt
├── .gitignore
└── data/
    └── stripe_docs.md
Setup

Create and activate a virtual environment:

python3 -m venv .venv
source .venv/bin/activate

Install dependencies:

pip install -r requirements.txt

Create a .env file:

VOYAGE_API_KEY=your_voyage_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key

Run the application:

python app.py
Current Limitation

The application currently recreates document embeddings every time it runs.

The next improvement is to generate the documentation embeddings once, save them locally, and reuse them for future questions.

Planned Improvements
Save and reload document embeddings
Retrieve multiple relevant sections
Build a larger evaluation dataset
Improve the relevance threshold
Add a Streamlit interface
Display documentation source links
Add helpful and not-helpful feedback
Capture unanswered questions as documentation gaps
Product Vision

In a real developer portal, DevDocs AI could help:

Reduce repeated support questions
Improve documentation discovery
Shorten time to first successful API call
Surface common integration problems
Identify missing or unclear documentation
Improve the developer onboarding experience
Disclaimer

This is an independent educational project using curated information from publicly available Stripe documentation. It is not affiliated with or endorsed by Stripe.
