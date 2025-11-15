from datetime import datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
import uuid


# Exceptions
class ReservationConflictError(Exception):
    pass

class PriceCalculationError(Exception):
    pass

class InvalidTimezoneError(Exception):
    pass

class CancellationNotAllowed(Exception):
    pass


# Classe Room
class Room:
    def __init__(self, name, base_price, capacity, timezone):
        self.name = name
        self.base_price = base_price
        self.capacity = capacity
        
        try:
            ZoneInfo(timezone)
            self.timezone = timezone
        except ZoneInfoNotFoundError:
            raise InvalidTimezoneError(f"Fuseau horaire invalide: {timezone}")


# Classe Reservation
class Reservation:
    def __init__(self, room, start, end, client, final_price, special_conditions=None):
        if start >= end:
            raise ValueError("start doit être avant end")
        
        self.reservation_id = str(uuid.uuid4())
        self.room = room
        self.client = client
        self.created_at = datetime.now(ZoneInfo("UTC"))
        self.final_price = final_price
        self.special_conditions = special_conditions or []
        
        tz = ZoneInfo(room.timezone)
        self.start = start if start.tzinfo else start.replace(tzinfo=tz)
        self.end = end if end.tzinfo else end.replace(tzinfo=tz)
        
        self.start_utc = self.start.astimezone(ZoneInfo("UTC"))
        self.end_utc = self.end.astimezone(ZoneInfo("UTC"))


# Classe BookingSystem
class BookingSystem:
    def __init__(self):
        self.rooms = {}
        self.reservations = []
    
    def add_room(self, room):
        self.rooms[room.name] = room
    
    def calculate_price(self, room, start, end, special_conditions=None):
        duration = (end - start).total_seconds() / 3600
        price = room.base_price * duration
        
        special_conditions = special_conditions or []
        if "VIP" in special_conditions:
            price *= 1.5
        if "last-minute" in special_conditions:
            price *= 1.3
        if "non-refundable" in special_conditions:
            price *= 0.8
        
        return round(price, 2)
    
    def make_reservation(self, room_name, start, end, client, special_conditions=None):
        if room_name not in self.rooms:
            raise ValueError(f"Salle {room_name} introuvable")
        
        room = self.rooms[room_name]
        tz = ZoneInfo(room.timezone)
        
        if not start.tzinfo:
            start = start.replace(tzinfo=tz)
        if not end.tzinfo:
            end = end.replace(tzinfo=tz)
        
        start_utc = start.astimezone(ZoneInfo("UTC"))
        end_utc = end.astimezone(ZoneInfo("UTC"))
        
        # Vérifier conflits
        for res in self.reservations:
            if res.room.name == room_name:
                if start_utc < res.end_utc and end_utc > res.start_utc:
                    raise ReservationConflictError("Conflit avec une réservation existante")
        
        price = self.calculate_price(room, start, end, special_conditions)
        
        reservation = Reservation(room, start, end, client, price, special_conditions)
        self.reservations.append(reservation)
        return reservation
    
    def cancel_reservation(self, reservation_id):
        reservation = None
        for res in self.reservations:
            if res.reservation_id == reservation_id:
                reservation = res
                break
        
        if not reservation:
            raise ValueError("Réservation introuvable")
        
        if "non-refundable" in reservation.special_conditions:
            raise CancellationNotAllowed("Réservation non-remboursable")
        
        self.reservations.remove(reservation)
    
    def convert_currency(self, amount, currency="EUR"):
        return amount
    
    def revenue_report(self, start_date, end_date):
        if not start_date.tzinfo:
            start_date = start_date.replace(tzinfo=ZoneInfo("UTC"))
        if not end_date.tzinfo:
            end_date = end_date.replace(tzinfo=ZoneInfo("UTC"))
        
        start_utc = start_date.astimezone(ZoneInfo("UTC"))
        end_utc = end_date.astimezone(ZoneInfo("UTC"))
        
        reservations = []
        total = 0
        revenue_by_room = {}
        
        for res in self.reservations:
            if res.start_utc < end_utc and res.end_utc > start_utc:
                reservations.append(res)
                total += res.final_price
                
                if res.room.name not in revenue_by_room:
                    revenue_by_room[res.room.name] = {"count": 0, "revenue": 0}
                revenue_by_room[res.room.name]["count"] += 1
                revenue_by_room[res.room.name]["revenue"] += res.final_price
        
        return {
            "total_reservations": len(reservations),
            "total_revenue": round(total, 2),
            "revenue_by_room": revenue_by_room
        }


# Exemple
if __name__ == "__main__":
    system = BookingSystem()
    
    room1 = Room("Salle A", 100, 50, "Europe/Paris")
    system.add_room(room1)
    
    res = system.make_reservation(
        "Salle A",
        datetime(2025, 12, 1, 10, 0),
        datetime(2025, 12, 1, 14, 0),
        "Alice"
    )
    print(f"Réservation créée: {res.final_price}€")
    
    report = system.revenue_report(
        datetime(2025, 12, 1),
        datetime(2025, 12, 2)
    )
    print(f"Revenus: {report['total_revenue']}€")