import argparse

import pandas as pd

from locallib.logger import SystemLogger, update_debug_enabled
from locallib.models import CountryDetails
from locallib.datastore import CountryDataStorage


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", dest="debug_enabled",
                        action="store_true", default=False, help="Enable debug log messages that will be written to STDOUT")

    args = parser.parse_args()

    update_debug_enabled(args.debug_enabled)

    country_file_df = pd.read_csv("data/country_populations.csv")
    vacination_file_df = pd.read_csv("data/vaccinations.csv")

    logger = SystemLogger(name="Main")

    logger.info("setting up data frames")

    country_file_df.drop(country_file_df.index[country_file_df['Country Code'].str.contains(
        "OWID") == True], inplace=True)
    vacination_file_df.drop(vacination_file_df.index[vacination_file_df['iso_code'].str.contains(
        "OWID") == True], inplace=True)

    logger.debug("replacing NaN in vacination dataframe")
    vacination_file_df.fillna(value=0, inplace=True)

    country_ready_df = country_file_df[[
        "Country Name", "Country Code", "2020"]]

    country_data_store = CountryDataStorage()

    for index, row in country_ready_df.iterrows():
        country_name = row["Country Name"]
        country_code = row["Country Code"]

        selected_country_df = vacination_file_df[vacination_file_df["iso_code"] == country_code].sort_values(by=[
            "date"])

        if not selected_country_df.empty:
            people_fully_vacinated = int(vacination_file_df[vacination_file_df["iso_code"] == country_code].sort_values(
                by=["date"]).iloc[-1]["people_fully_vaccinated"])
            population = int(row["2020"])

            country_with_details = CountryDetails(
                name=country_name,
                code=country_code,
                population=population,
                people_fully_vacinated=people_fully_vacinated
            )
            logger.debug(f"new country with details: {country_with_details}")

            country_data_store.add(country_with_details)

    country_data_store.write_to_database()


if __name__ == "__main__":
    main()
