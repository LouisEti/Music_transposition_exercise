
import mido
import keyboard
import sys
import random
import time


def choose_ports_name(string_to_identify: str, port_type: str) -> str:
    """
    Among port_type ("input" or "output"), retrieve all the names and if the string_to_identify is in one of the name, return it 
    """
    if port_type == "input":
        port_names = mido.get_input_names()
    elif port_type == "output":
        port_names = mido.get_output_names()
    else:
        sys.exit("port_type is unvalid")

    if port_names == []:
        sys.exit(f"There is no {port_type} names")

    for name in port_names:
        if string_to_identify in name: 
            print(f"{port_type} selected: {name}")
            return name 
        else: 
            continue
    
    for name in port_names:
        print(name)
    sys.exit(f"{string_to_identify} doesn't appear in {port_type} names") 

    
def close_ports(input, output):
    input.close()
    output.close()


dict_transposition = {
    "E": -4,
    "E♭": -3,
    "D": -2, 
    "D♭": -1,
    "C": 0,
    "B": 1,
    "B♭": 2,
    "A": 3,
    "A♭": 4,
    "G": 5,
    "F#": 6,
    "F": 7
}


def note_after_transpo(dict_transpo, current_note, previous_note):

    global non_played_notes

    non_played_notes.remove(previous_note)
    if non_played_notes != []:
        new_note = random.choice(non_played_notes)
    else:
        non_played_notes = list(dict_transposition.keys())
        new_note = random.choice(non_played_notes)
    print(f"List of non played notes: {non_played_notes}")
    
    new_note_value = dict_transpo[new_note]
    old_note_value = dict_transpo[current_note]

    transpo_value = new_note_value - old_note_value

    return new_note, transpo_value


def event_keys_keyboard(event_name, tonic_note, previous_note):

    global non_played_notes

    if event_name not in ["esc", "backspace", "0"]:
        return None, None 
    
    elif event_name == "backspace":
        new_note, transpo_value = note_after_transpo(dict_transposition, tonic_note, previous_note)
        print(new_note, transpo_value)
        return new_note, transpo_value

    elif event_name == "esc": 
        raise KeyboardInterrupt  # Raise KeyboardInterrupt to stop the loop
    
    elif event_name == "0":
        transpo_value = dict_transposition["C"] 
        new_note = tonic_note
        non_played_notes = list(dict_transposition.keys())
        print(f"List of non played notes: {non_played_notes}")
        print(new_note, transpo_value)
        return new_note, transpo_value


def warm_up_input_buffer(input_port, warm_up_duration=1):
    """
    Wait for a warm-up duration and discard any MIDI messages received during this period.
    """
    start_time = time.time()
    while time.time() - start_time < warm_up_duration:
        for msg in input_port.iter_pending():
            pass  # Discard the MIDI message


def transposition(note_gamme_majeure) -> None:
    """ 
    Play the MIDI messages that are sent through your input port (MIDI controller). 
    This function allows MIDI messages to be transposed 
    Some keyboard keys correspond to an action
    """
    
    global non_played_notes

    input_name = choose_ports_name("HAVIAN", "input")
    output_name = choose_ports_name("loopMIDI Port 1", "output")

    input_port = mido.open_input(input_name)
    output_port = mido.open_output(output_name)

    transpo_value = 0   
    key_pressed = False 
    previous_note = note_gamme_majeure

    non_played_notes = list(dict_transposition.keys())

    try:
        # Warm up input buffer
        warm_up_input_buffer(input_port)
        while True:
            for msg in input_port.iter_pending():
                if msg.type == "note_on" or msg.type == "note_off":
                    msg.note += transpo_value
                    output_port.send(msg)
                elif msg.type == "control_change" and msg.control == 64:
                    # Sustain pedal (CC64) message
                    output_port.send(msg)  # Forward the pedal message without modification
                else:
                    print(f"Ignoring MIDI message: {msg.type}")

            if keyboard.is_pressed('esc') and key_pressed == False:
                key_pressed = True
                previous_note, transpo_value = event_keys_keyboard("esc", note_gamme_majeure, previous_note)
                
            elif keyboard.is_pressed('backspace') and key_pressed == False:
                previous_note, transpo_value = event_keys_keyboard("backspace", note_gamme_majeure, previous_note)
                key_pressed = True

            elif keyboard.is_pressed('0') and key_pressed == False:
                previous_note, transpo_value = event_keys_keyboard("0", note_gamme_majeure, previous_note)
                key_pressed = True

            elif not keyboard.is_pressed('backspace') and not keyboard.is_pressed('esc') and not keyboard.is_pressed('0'):
                key_pressed = False


    except KeyboardInterrupt:
        print("KeyboardInterrupt: Closing input and output ports...")
        close_ports(input_port, output_port)
    
transposition("A") #♭
