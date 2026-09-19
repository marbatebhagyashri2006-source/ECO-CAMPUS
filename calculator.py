from emission_factors import (
    ELECTRICITY_FACTOR,
    PETROL_FACTOR,
    DIESEL_FACTOR,
    COMPOSTED_WASTE_FACTOR,
    LANDFILL_WASTE_FACTOR
)


def calculate_footprint(
    electricity_kwh,
    petrol_litres,
    diesel_litres,
    composted_waste_kg,
    landfill_waste_kg
):

    electricity_emissions = electricity_kwh * ELECTRICITY_FACTOR
    petrol_emissions = petrol_litres * PETROL_FACTOR
    diesel_emissions = diesel_litres * DIESEL_FACTOR

    composted_waste_emissions = (
        composted_waste_kg * COMPOSTED_WASTE_FACTOR
    )

    landfill_waste_emissions = (
        landfill_waste_kg * LANDFILL_WASTE_FACTOR
    )

    total_emissions = (
        electricity_emissions
        + petrol_emissions
        + diesel_emissions
        + composted_waste_emissions
        + landfill_waste_emissions
    )

    return {
        "electricity": electricity_emissions,
        "petrol": petrol_emissions,
        "diesel": diesel_emissions,
        "composted_waste": composted_waste_emissions,
        "landfill_waste": landfill_waste_emissions,
        "total": total_emissions
    }