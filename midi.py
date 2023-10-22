import pygame as pg
import pygame.midi


def midi_init(input_id=None):
    if input_id is None:
        input_id = pg.midi.get_default_input_id()

    return pg.midi.Input(input_id)


def midi_close(input):
    input.close()


def midi(input, bindings_dict):
    if input.poll():
        i = input.read(1)[0][0]

        status, note, _, _ = i

        print(i, status, 0x90, bindings_dict)

        if status==0x90:
            if note in bindings_dict:
                print(note, bindings_dict[note])
                # return playlsit_id
                return bindings_dict[note]

    return None
