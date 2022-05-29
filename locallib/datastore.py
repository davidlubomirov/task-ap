from dataclasses import dataclass, field

import sqlite3

from locallib.models import CountryDetails
from locallib.logger import SystemLogger


@dataclass
class CountryDataStorage(SystemLogger):
    data: dict[str, CountryDetails] = field(init=False)
    database_file: str = "zadacha.db"

    def __post_init__(self):
        self.data = {}
        SystemLogger.__init__(self, name=self.__class__.__name__)

    def add(self, country: CountryDetails) -> None:
        self.data[country.code] = country

    def write_to_database(self) -> None:
        self.info(f"writing data to database file: {self.database_file}")

        try:
            database_connection = sqlite3.connect(self.database_file)
            cursor = database_connection.cursor()

            cursor.execute('''CREATE TABLE countries
                        (name text, iso_code text, population int, total_vaccinated int, percentage_vaccinated real)''')

            self.info(f"established database connection")

            sqlite_insert_with_param = """INSERT INTO countries
			(name, iso_code, population,
			total_vaccinated, percentage_vaccinated)
			VALUES (?, ?, ?, ?, ?);"""

            for key, value in self.data.items():
                data_tuple = (value.name, value.code, value.population,
                              value.people_fully_vacinated, value.vacinated_in_percentage)
                cursor.execute(sqlite_insert_with_param, data_tuple)
                database_connection.commit()
                self.debug(f"record inserted in database: {data_tuple}")

            cursor.close()
            self.debug("closed database cursor")
        except sqlite3.Error as err:
            self.error(f"database error, {err}")
        finally:
            if database_connection:
                database_connection.close()
                self.debug("database connection was closed")

            self.info(
                f"data was inserted with success, amount of records inserted: {len(self.data)}")
