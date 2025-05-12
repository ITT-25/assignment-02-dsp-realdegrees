[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/Vd0qjMAQ)

# Setup

1. Clone the repo
2. `cd` into the root folder
3. Setup a virtual env
4. `pip install -r requirements.txt`

# karaoke_game

## Usage

Help Command: `python ./karaoke_game/karaoke.py --help`

1. Pick one of the available songs  
    `python ./karaoke_game/karaoke.py -s --help`
2. Run the program with the selected song  
    `python karaoke_game/karaoke.py -s "selectedsong"`
3. Select your microphone in the prompt
4. Move the *Frequency Cursor* using your voice:  
     **UP** = High Pitch  
     **DOWN** = Low Pitch  
5. If you have a very high or deep voice and can't hit the notes properly, adjust the octave offset  
    `python ./karaoke_game/karaoke.py -o --help`
6. After you found your octave offset try to hit the notes and get the max score :)

You can restart the song at any time using the `R` key.  
To close the program press `ESC`.

    Since the controls using the frequency of the audio input are not very fine-grained,  
    I added an assist mode that snaps to notes if the frequency is within a certain range.
    The default assist rate is `3`.  

If you want to adjust the difficulty use the parameter `-a`:  
    `python karaoke_game/karaoke.py -o 1.3 -s "selectedsong" -a 4`

If a midi file seems too slow or too fast you can adjust the `--time-scale`.
    `python karaoke_game/karaoke.py -o 1.3 -s "selectedsong" -ts 2`

To see a log of the frequencies, midi notes and octaves use the `-v` flag.

# whistle_input

## Usage

TODO: launch command, controls, description