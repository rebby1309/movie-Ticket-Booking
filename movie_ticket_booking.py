from queue import Queue
import time
import random
import string
import threading

class MovieTicketBooking:
    def __init__(self, total_tickets, movie_name):
        self.total_tickets = total_tickets
        self.available_seats = list(range(1, total_tickets + 1))
        self.seat_allotments = {}
        self.lock = threading.Lock()
        self.max_seats_per_user = 10
        self.movie_name = movie_name

    def generate_ticket_code(self):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

    def book_ticket(self, user_name, seat_choices):
        with self.lock:
            if len(seat_choices) > self.max_seats_per_user:
                print(f"{user_name}, you cannot book more than {self.max_seats_per_user} seats at a time.")
                return False

            unavailable_seats = [seat for seat in seat_choices if seat not in self.available_seats]
            if not unavailable_seats:
                print(f"\nSeats chosen by {user_name} for {self.movie_name}: {seat_choices}")
                confirmation = input(f"{user_name}, do you want to confirm booking for seats {seat_choices}? (yes/no): ").strip().lower()
                if confirmation == 'yes':
                    ticket_code = self.generate_ticket_code()
                    for seat in seat_choices:
                        self.available_seats.remove(seat)  # Remove booked seats from available list
                    self.seat_allotments[user_name] = {"seats": seat_choices, "ticket_code": ticket_code}
                    print(f"Successfully booked seats {seat_choices} for {user_name} to watch {self.movie_name}. Your ticket code is: {ticket_code}")
                    return True
                else:
                    print(f"Booking for {user_name} has been cancelled.")
                    return False
            else:
                print(f"Sorry {user_name}, the following seats are not available: {unavailable_seats}")
                return False

    def retry_booking(self, user_name):
        while True:
            retry = input(f"{user_name}, do you want to retry with different seats? (yes/no): ").strip().lower()
            if retry == 'yes':
                new_seat_choices = input(f"Enter new seat numbers for {user_name} (comma separated): ")
                new_seat_choices = list(map(int, new_seat_choices.split(',')))

                unavailable_seats = [seat for seat in new_seat_choices if seat not in self.available_seats]
                if not unavailable_seats:
                    success = self.book_ticket(user_name, new_seat_choices)
                    if success:
                        return True
                else:
                    print(f"Sorry {user_name}, the following seats are still not available: {unavailable_seats}")
            else:
                print(f"Booking process for {user_name} has been cancelled.")
                return False

    def display_tickets(self):
        print(f"Available Seats for '{self.movie_name}': {self.available_seats}")


def fcfs_booking(ticket_booking, booking_queue):
    while not booking_queue.empty():
        user_name, seat_choices = booking_queue.get()  # Get the next user in line
        print(f"\nProcessing booking for {user_name}...")
        success = ticket_booking.book_ticket(user_name, seat_choices)
        if not success:

            ticket_booking.retry_booking(user_name)
        time.sleep(1)


if __name__ == "__main__":
    total_tickets = 10
    movie_name = input("Enter the movie name: ")  # Get the movie name
    ticket_booking = MovieTicketBooking(total_tickets, movie_name)

    booking_queue = Queue()

    num_users = int(input("Enter the number of users: "))

    for i in range(num_users):
        user_name = input(f"Enter name for user {i + 1}: ")

        ticket_booking.display_tickets()

        seat_choices = list(map(int, input(f"Enter the seat numbers for {user_name} (comma separated): ").split(',')))
        booking_queue.put((user_name, seat_choices))  # Add the booking to the queue

    print("\nStarting ticket booking process (FCFS)...\n")
    fcfs_booking(ticket_booking, booking_queue)

    print("\nFinal Seat Allotments:")
    for user, details in ticket_booking.seat_allotments.items():
        print(f"{user} -> Seats: {details['seats']}, Ticket Code: {details['ticket_code']}")
