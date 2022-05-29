from dataclasses import dataclass, field


@dataclass
class CountryDetails:
    name: str
    code: str
    population: int
    people_fully_vacinated: int
    vacinated_in_percentage: float = field(init=False)

    def __post_init__(self) -> None:
        self.vacinated_in_percentage = (
            self.people_fully_vacinated / self.population) * 100

    def __repr__(self) -> str:
        return f"Country Name: {self.name}, Code: {self.code}"
