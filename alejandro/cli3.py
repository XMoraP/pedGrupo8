import os
import sys

def cli3(fifo_name):
    try:
        # Open the FIFO for writing
        with open(fifo_name, "w") as fifo:
            fifo.write("Request\n")

        # Open the FIFO for reading
        with open(fifo_name, "r") as fifo:
            # Read the response from the server
            server_response = fifo.readline().strip()

            # Display the response
            print("Server Response:", server_response)

    except Exception as e:
        print("Error in the client:", e)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python cli3.py <fifo_name>")
        sys.exit(1)

    fifo_name = sys.argv[1]
    cli3(fifo_name)
