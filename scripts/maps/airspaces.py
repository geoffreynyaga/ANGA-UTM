import json
import os

from django.contrib.gis.geos import Point, Polygon

from maps.models import AirportLocations, AirspaceFrequencies, AirspaceLocation

script_dir = os.path.dirname(__file__)


def open_and_create_airspaces(file_name):
    geojson_path = os.path.join(script_dir, file_name)

    # Load the GeoJSON file
    with open(geojson_path, "r") as f:
        geojson_data = json.load(f)
        # print(geojson_data)

    # # Loop through each feature in the GeoJSON data
    for feature in geojson_data["features"]:
        properties = feature["properties"]
        geometry = feature["geometry"]

        # Extract the coordinates (assuming Point geometry)
        if geometry["type"] == "Polygon":
            print("==========")
            coords = geometry["coordinates"][0]

            geom_polygon = Polygon(coords)

            name = properties["name"]

            airspaces_qs = AirspaceLocation.objects.filter(name=name)

            if airspaces_qs.exists():
                print(f"{name} already exists")
                continue
            else:
                print("################")

            airspace_type = properties["type"]
            icaoClass = properties["icaoClass"]
            upperLimitValue = properties["upperLimit"]["value"]
            lowerLimitValue = properties["lowerLimit"]["value"]
            upperLimitUnit = properties["upperLimit"]["unit"]
            lowerLimitUnit = properties["lowerLimit"]["unit"]

            try:
                remarks = properties["remarks"]
            except KeyError:
                remarks = None

            print(name, "name")
            # print(airspace_type, "airspace_type")
            # print(icaoClass, "icaoClass")
            # print(upperLimitValue, "upperLimitValue")
            # print(lowerLimitValue, "lowerLimitValue")
            # print(upperLimitUnit, "upperLimitUnit")
            # print(lowerLimitUnit, "lowerLimitUnit")
            # print(remarks, "remarks")

            # # Create and save the Location object
            airspace_obj = AirspaceLocation(
                name=name,
                geom=geom_polygon,
                icao_class=icaoClass,
                upper_limit=upperLimitValue,
                upper_limit_unit=upperLimitUnit,
                lower_limit=lowerLimitValue,
                lower_limit_unit=lowerLimitUnit,
                remarks=remarks,
            )

            print(airspace_obj, "airspace_obj")

            airspace_obj.save()
            print(f"Saved location: {airspace_obj.name}")


def open_and_create_airports(file_name):
    geojson_path = os.path.join(script_dir, file_name)

    # Load the GeoJSON file
    with open(geojson_path, "r") as f:
        geojson_data = json.load(f)
        # print(geojson_data)

    # # Loop through each feature in the GeoJSON data
    for feature in geojson_data["features"]:
        properties = feature["properties"]
        geometry = feature["geometry"]

        # Extract the coordinates (assuming Point geometry)
        if geometry["type"] == "Point":
            # print("==========")
            coords = geometry["coordinates"]

            centroid = Point(coords)

            airport_name = properties["name"]

            airports_qs = AirportLocations.objects.filter(name=airport_name)

            if airports_qs.exists():
                print(f"{airports_qs} already exists")
                continue
            else:
                print("################")

            try:
                icao_code = properties["icaoCode"]
            except KeyError:
                icao_code = None

            magnetic_declination = properties["magneticDeclination"]
            elevation = properties["elevation"]["value"]
            is_private = properties["private"]

            new_airport_obj = AirportLocations(
                name=airport_name,
                icao_code=icao_code,
                elevation=elevation,
                centroid=centroid,
                is_private=is_private,
                magnetic_declination=magnetic_declination,
            )

            new_airport_obj.save()

            # new_airport_obj = AirportLocations.objects.filter(
            #     name=airport_name,
            #     icao_code=icao_code,
            # ).first()

            # get or create airspace frequencies

            # frequency
            try:
                frequencies = properties["frequencies"]

                if len(frequencies) > 0:
                    for frequency in frequencies:
                        print(frequency)
                        print("==== saving frequency ======")
                        name = frequency["name"]
                        value = float(frequency["value"])
                        primary = frequency["primary"]
                        public_use = frequency["publicUse"]
                        type_code = frequency["type"]

                        try:
                            print("are we here")
                            x = AirspaceFrequencies(
                                name=name,
                                value=value,
                                is_primary=primary,
                                public_use=public_use,
                                type_number=type_code,
                            )
                            x.save()

                            new_airport_obj.airspace_frequencies.add(x)
                        except Exception as e:
                            print(e, "error saving")

            except Exception as e:
                # print("xxxxxxx no frequencies")
                print(e, "error1")

            # # Create and save the Location object

            # print(f"Saved location: {new_airport_obj.name}")
            # print("Saved location")


if __name__ == "__main__":
    open_and_create_airspaces("ke_asp.geojson")
    open_and_create_airports("ke-apt.geojson")

"""
from scripts.maps import airspaces

airspaces_file_name = "ke_asp.geojson"
airports_file_name = "ke_apt.geojson"

airspaces.open_and_create_airspaces(airspaces_file_name)
airspaces.open_and_create_airports(airports_file_name)

"""
