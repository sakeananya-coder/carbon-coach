# Carbon Coach 🌱

**AI-powered personal carbon footprint assistant**

Carbon Coach helps people understand and reduce their daily carbon footprint using conversational AI and Python calculation tools.

## Features
- Travel emissions calculation
- Electricity emissions calculation
- Comparison of transport options
- Activity logging and history
- Daily and weekly emissions summaries
- Personalized carbon-reduction recommendations
- Daily eco challenges

## Technology
- Python
- Google Agent Development Kit (ADK)
- Google Gemini API
- JSON-based activity storage

## How to Run
1. Install dependencies: `pip install -r requirements.txt`
2. Add your Google Gemini API key to `carbon_coach/.env`.
3. Run `adk web` from the project root.
4. Open `http://localhost:8000`.
5. Select `carbon_coach`.

## Limitations
- Travel emission factors are illustrative and need validation against reliable regional sources.
- Activity history is stored locally.
- Gemini free-tier API quota may limit live demonstrations.

## Future Scope
- Verified regional emission factors
- Telugu and Hindi support
- Campus carbon leaderboard
- Cloud deployment and multi-user tracking

Built for a sustainability-focused AI hackathon.
