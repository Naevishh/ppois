from typing import Optional

from .models import TransportRoute, PublicTransportVehicle, RouteStop


class TransportMonitoringSystem:
    def __init__(self) -> None:
        self.routes = {}
        self.vehicles = {}

        self.physical_stops = {}

    def register_route(self, route: TransportRoute) -> None:
        self.routes[route.route_id] = route
        for route_stop in route.stops:

            if route_stop.bus_stop.device_id not in self.physical_stops:
                self.physical_stops[route_stop.bus_stop.device_id] = route_stop.bus_stop
        for vehicle in route.vehicles:
            self.vehicles[vehicle.device_id] = vehicle

    def register_vehicle(self, vehicle: PublicTransportVehicle) -> None:
        self.vehicles[vehicle.device_id] = vehicle
        if vehicle.route_id in self.routes:
            self.routes[vehicle.route_id].add_vehicle(vehicle)

    def calculate_eta(self, vehicle: PublicTransportVehicle, stop: RouteStop, route: TransportRoute) -> Optional[float]:
        current_idx = vehicle.get_last_stop_index
        target_idx = stop.index

        if current_idx == -1 or current_idx > target_idx:
            return None
        elif current_idx == target_idx:
            return 0

        stops_remaining = target_idx - current_idx
        minutes_remaining = stops_remaining * route.avg_time_between_stops

        import random
        minutes_remaining += random.randint(0, 2)
        return round(minutes_remaining, 1)

    def get_arrival_info(self, stop_id: str) -> dict:

        if stop_id not in self.physical_stops:
            return {"error": "Остановка не найдена"}

        physical_stop = self.physical_stops[stop_id]
        arrivals = []

        for route in self.routes.values():

            route_stop = None
            for rs in route.stops:
                if rs.bus_stop.device_id == stop_id:
                    route_stop = rs
                    break

            if not route_stop:
                continue

            for vehicle in route.vehicles:
                eta = self.calculate_eta(vehicle, route_stop, route)
                if eta is not None and eta >= 0:
                    arrivals.append({
                        "vehicle_id": vehicle.device_id,
                        "type": vehicle.vehicle_type.value,
                        "route": route.route_id,
                        "eta_minutes": eta
                    })

        arrivals.sort(key=lambda x: x["eta_minutes"])

        if arrivals:
            next_arrival = arrivals[0]
            physical_stop.set_display(
                f"{next_arrival['type'].upper()} №{next_arrival['route']}: {next_arrival['eta_minutes']} мин")
        else:
            physical_stop.set_display("Нет данных")

        return {
            "stop_id": stop_id,
            "stop_name": physical_stop.name,
            "arrivals": arrivals
        }
