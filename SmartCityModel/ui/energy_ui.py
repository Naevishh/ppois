from ..city import SmartCity


class EnergyUI:
    def __init__(self, city: SmartCity) -> None:
        self.city = city

    def generate_report(self) -> str:
        result = self.city.energy_grid.optimize_all()
        """Форматирует результат оптимизации энергии для вывода"""
        output = []
        output.append("=" * 50)
        output.append("        РЕЗУЛЬТАТЫ ОПТИМИЗАЦИИ ЭНЕРГИИ")
        output.append("=" * 50)
        output.append(f"  Производство:    {result['production']} кВт·ч")
        output.append(f"  Потребление:     {result['consumption']} кВт·ч")
        output.append(f"  Избыток/Дефицит: {result['surplus']} кВт·ч")
        output.append("-" * 50)
        output.append(f"  {result['result']}")
        output.append("=" * 50)
        return "\n".join(output)
