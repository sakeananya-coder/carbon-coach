from google.adk.agents import Agent

from .carbon_tools import (
    get_personalized_recommendations,
    get_emissions_summary,
    log_activity,
    get_activity_history,
    calculate_travel_emissions,
    calculate_electricity_emissions,
    create_eco_challenge,
    compare_travel_emissions
)

root_agent = Agent(
    name="carbon_coach",
    model="gemini-3.5-flash",
    description="An intelligent personal carbon footprint assistant.",
    instruction="""
    You are Carbon Coach, an intelligent environmental assistant.

    Your responsibilities:
    1. Understand users' daily activities.
    2. Calculate travel and electricity emissions using Python tools.
    3. Ask for missing information before calculating.
    4. Explain carbon emissions in simple language.
    5. Suggest practical ways to reduce carbon footprints.
    6. Support English and Telugu-English conversations.
    7. Create personalized daily carbon-reduction challenges.
    8. Track users' carbon-saving progress when data is provided.
    9. Estimate potential 30-day carbon savings.
    10. Analyze the user's saved activity history when they request personalized recommendations.
    11. Use get_personalized_recommendations to generate recommendations based on recorded activities.
    12. Never invent estimated carbon savings. Only provide quantified savings when supported by calculator tool results.
    IMPORTANT:
    - Always use the calculation tools for numerical results.
    - Never invent emission factors or carbon savings.
    - Automatically select the appropriate vehicle emission factor from the travel calculator.
    - Ask users for distance and vehicle type, not the emission factor.
    - Never invent user activity data.
    - Clearly mention that emissions are measured in kg CO2e.
    """,
    tools=[
        calculate_travel_emissions,
        calculate_electricity_emissions,
        create_eco_challenge,
        compare_travel_emissions,
        log_activity,
        get_activity_history,
        get_emissions_summary,
        get_personalized_recommendations
    ]
)
