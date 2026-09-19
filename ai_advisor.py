def generate_recommendations(results):

    # Emission categories
    emissions = {
        "Electricity": results["electricity"],
        "Petrol": results["petrol"],
        "Diesel": results["diesel"],
        "Composted Waste": results["composted_waste"],
        "Landfill Waste": results["landfill_waste"]
    }

    total = results["total"]

    # Find largest emission source
    largest_source = max(emissions, key=emissions.get)
    largest_value = emissions[largest_source]

    percentage = (largest_value / total) * 100 if total > 0 else 0

    recommendations = []

    # Electricity
    if largest_source == "Electricity":
        recommendations.append(
            (
                "⚡ Improve Energy Efficiency",
                "Electricity is the largest contributor to the campus "
                "footprint. Prioritize LED lighting, energy-efficient "
                "equipment, and optimized operating schedules."
            )
        )

    # Transportation
    elif largest_source in ["Petrol", "Diesel"]:
        recommendations.append(
            (
                "🚌 Promote Low-Carbon Transportation",
                "Transportation is the largest contributor to the campus "
                "footprint. Encourage public transport, carpooling, "
                "cycling, and efficient campus transportation."
            )
        )

    # Waste
    elif largest_source == "Landfill Waste":
        recommendations.append(
            (
                "♻️ Reduce Landfill Waste",
                "Landfilled waste is a major contributor. Strengthen waste "
                "segregation and divert suitable organic waste toward "
                "composting."
            )
        )

    else:
        recommendations.append(
            (
                "🌱 Strengthen Waste Management",
                "Continue improving source segregation and explore ways "
                "to reduce the amount of waste generated on campus."
            )
        )

    # Always provide additional practical actions
    recommendations.extend([
        (
            "💡 Monitor High-Impact Areas",
            f"{largest_source} currently contributes approximately "
            f"{percentage:.1f}% of the calculated footprint. "
            "Focus monitoring and improvement efforts here first."
        ),
        (
            "📊 Track Progress Over Time",
            "Record the campus footprint regularly to identify trends "
            "and measure whether sustainability initiatives are "
            "reducing emissions."
        )
    ])

    # Build formatted response
    output = f"""
### 🌿 Carbon Insight

Your current estimated campus footprint is **{total:,.2f} kg CO₂e**.

The largest emission source is **{largest_source}**, contributing
approximately **{percentage:.1f}%** of the calculated footprint.

### 🎯 Recommended Actions
"""

    for i, (title, explanation) in enumerate(recommendations, start=1):
        output += f"""
**{i}. {title}**

{explanation}

"""

    output += """
### 💡 Priority

Start by addressing **""" + largest_source + """**, since it currently
represents the largest share of the calculated campus footprint.
"""

    return output