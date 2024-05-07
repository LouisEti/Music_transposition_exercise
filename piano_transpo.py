import mido

# Function to capture MIDI messages
def capture_midi_messages():
    # List all available MIDI input devices
    input_names = mido.get_input_names()
    print("Available MIDI input devices:")
    for i, name in enumerate(input_names):
        print(f"{i + 1}: {name}")

    # Ask user to select MIDI input device
    while True:
        try:
            choice = int(input("Enter the number corresponding to your MIDI input device: "))
            if 1 <= choice <= len(input_names):
                selected_input = input_names[choice - 1]
                break
            else:
                print("Invalid choice. Please enter a number within the range.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    print(f"Selected MIDI input device: {selected_input}")

    # Open connection to selected MIDI input device
    with mido.open_input(selected_input) as inport:
        print("Press a button or key on your MIDI controller...")
        print("Press Ctrl+C to stop the program.")
        try:
            for msg in inport:
                print("Message received:", msg)
        except KeyboardInterrupt:
            print("\nProgram stopped by user.")

# Run the function to capture MIDI messages
capture_midi_messages()
