def calculate_electricity_emissions(units_kwh: float, emission_factor: float):
    """
    Calculate electricity emissions in kg CO2e.
    units_kwh: Electricity consumed in kWh.
    emission_factor: kg CO2e per kWh.
    """

    if units_kwh < 0 or emission_factor < 0:
        return {"error": "Values cannot be negative."}

    emissions = units_kwh * emission_factor

    return {
        "electricity_kwh": units_kwh,
        "emission_factor": emission_factor,
        "emissions_kg_co2e": round(emissions, 3)
    }


def calculate_travel_emissions(distance_km: float, vehicle_type: str):
    """
    Calculate travel emissions automatically based on vehicle type.
    """

    emission_factors = {
        "petrol": 0.171,
        "diesel": 0.165,
        "electric": 0.050,
        "motorcycle": 0.103,
        "bus": 0.089
    }

    vehicle = vehicle_type.lower().strip()

    if distance_km < 0:
        return {"error": "Distance cannot be negative."}

    if vehicle not in emission_factors:
        return {
            "error": "Vehicle not supported. Choose petrol, diesel, electric, motorcycle, or bus."
        }

    factor = emission_factors[vehicle]
    emissions = distance_km * factor

    return {
        "distance_km": distance_km,
        "vehicle_type": vehicle,
        "emission_factor": factor,
        "emissions_kg_co2e": round(emissions, 3),
        "recommendation": "Consider public transport, carpooling, or walking for shorter trips."
    }

def create_eco_challenge(user_activity: str):
    """Create a personalized daily carbon-saving challenge."""

    activity = user_activity.lower()

    if "car" in activity or "travel" in activity:
        challenge = "Try walking, cycling, or using public transport for one short trip today."

    elif "electricity" in activity or "power" in activity:
        challenge = "Switch off unused lights and appliances today."

    else:
        challenge = "Avoid single-use plastics and choose reusable alternatives today."

    return {
        "challenge": challenge,
        "duration": "1 day",
        "goal": "Reduce your daily carbon footprint",
        "message": "Small actions create meaningful environmental change!"
    }


def compare_travel_emissions(distance_km: float, original_vehicle: str, alternative_vehicle: str):
    """Compare two travel choices and calculate potential carbon savings."""

    emission_factors = {
        "petrol": 0.171,
        "diesel": 0.165,
        "electric": 0.050,
        "motorcycle": 0.103,
        "bus": 0.089
    }

    original = original_vehicle.lower().strip()
    alternative = alternative_vehicle.lower().strip()

    if distance_km < 0:
        return {"error": "Distance cannot be negative."}

    if original not in emission_factors or alternative not in emission_factors:
        return {"error": "Unsupported vehicle type."}

    original_emissions = distance_km * emission_factors[original]
    alternative_emissions = distance_km * emission_factors[alternative]

    savings = original_emissions - alternative_emissions

    return {
        "distance_km": distance_km,
        "original_vehicle": original,
        "alternative_vehicle": alternative,
        "original_emissions_kg": round(original_emissions, 3),
        "alternative_emissions_kg": round(alternative_emissions, 3),
        "potential_savings_kg_co2e": round(savings, 3)
    }


import json
import os
from datetime import datetime

HISTORY_FILE = os.path.join(os.path.dirname(__file__), "activity_history.json")


def log_activity(activity_type: str, description: str, emissions_kg_co2e: float):
    """Save a user's activity and its carbon emissions."""

    if emissions_kg_co2e < 0:
        return {"error": "Emissions cannot be negative."}

    activity = {
        "activity_type": activity_type,
        "description": description,
        "emissions_kg_co2e": round(emissions_kg_co2e, 3),
        "date": datetime.now().isoformat(timespec="seconds")
    }

    try:
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, "r", encoding="utf-8") as file:
                history = json.load(file)
        else:
            history = []

        if not isinstance(history, list):
            return {"error": "Activity history file has an invalid format."}

        history.append(activity)

        with open(HISTORY_FILE, "w", encoding="utf-8") as file:
            json.dump(history, file, indent=4)

        return {
            "status": "success",
            "message": "Activity saved successfully.",
            "activity": activity
        }

    except (OSError, json.JSONDecodeError) as error:
        return {"error": f"Could not save activity: {error}"}


def get_activity_history():
    """Retrieve saved activities and calculate total emissions."""

    try:
        if not os.path.exists(HISTORY_FILE):
            return {
                "activities": [],
                "total_emissions_kg_co2e": 0,
                "message": "No activities have been saved yet."
            }

        with open(HISTORY_FILE, "r", encoding="utf-8") as file:
            history = json.load(file)

        if not isinstance(history, list):
            return {"error": "Activity history file has an invalid format."}

        total = sum(
            float(item.get("emissions_kg_co2e", 0))
            for item in history
        )

        return {
            "activities": history,
            "total_emissions_kg_co2e": round(total, 3),
            "activity_count": len(history)
        }

    except (OSError, json.JSONDecodeError, TypeError, ValueError) as error:
        return {"error": f"Could not read activity history: {error}"}

def get_emissions_summary():
    """Calculate daily and current-week carbon emissions from saved activities."""

    from datetime import date, timedelta

    try:
        if not os.path.exists(HISTORY_FILE):
            return {
                "daily_emissions": {},
                "weekly_total_kg_co2e": 0,
                "activity_count": 0
            }

        with open(HISTORY_FILE, "r", encoding="utf-8") as file:
            history = json.load(file)

        if not isinstance(history, list):
            return {"error": "Activity history file has an invalid format."}

        today = date.today()
        week_start = today - timedelta(days=today.weekday())

        daily_totals = {}
        weekly_total = 0
        weekly_count = 0

        for activity in history:
            activity_date = datetime.fromisoformat(
                activity["date"]
            ).date()

            emissions = float(activity["emissions_kg_co2e"])
            day = activity_date.isoformat()

            daily_totals[day] = round(
                daily_totals.get(day, 0) + emissions, 3
            )

            if week_start <= activity_date <= today:
                weekly_total += emissions
                weekly_count += 1

        return {
            "daily_emissions_kg_co2e": daily_totals,
            "current_week_start": week_start.isoformat(),
            "current_week_end": today.isoformat(),
            "weekly_total_kg_co2e": round(weekly_total, 3),
            "weekly_activity_count": weekly_count
        }

    except (OSError, json.JSONDecodeError, KeyError, ValueError, TypeError) as error:
        return {"error": f"Could not calculate emissions summary: {error}"}

def get_personalized_recommendations():
    """Recommend ways to reduce emissions based on saved activities."""

    history_result = get_activity_history()

    if "error" in history_result:
        return history_result

    activities = history_result["activities"]

    if not activities:
        return {
            "message": "No activities found. Log some activities first."
        }

    recommendations = []

    for activity in activities:
        activity_type = activity.get("activity_type", "").lower()
        description = activity.get("description", "").lower()
        emissions = float(activity.get("emissions_kg_co2e", 0))

        if activity_type == "travel" or "car" in description:
            recommendations.append({
                "activity": activity["description"],
                "current_emissions_kg_co2e": emissions,
                "suggestion": "Consider public transport, carpooling, cycling, or walking.",
                "estimated_savings": "Not calculated: alternative travel details are needed."
            })

        elif activity_type == "electricity":
            recommendations.append({
                "activity": activity["description"],
                "current_emissions_kg_co2e": emissions,
                "suggestion": "Switch off unused lights and appliances and use energy-efficient devices.",
                "estimated_savings": "Not calculated: electricity reduction data is needed."
            })

        else:
            recommendations.append({
                "activity": activity["description"],
                "current_emissions_kg_co2e": emissions,
                "suggestion": "Look for ways to reduce, reuse, and avoid unnecessary consumption.",
                "estimated_savings": "Not calculated: more activity details are needed."
            })

    return {
        "recommendations": recommendations,
        "activities_analyzed": len(activities),
        "message": "Recommendations generated from your saved activity history."
    }
