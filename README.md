[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/Vd0qjMAQ)

# Setup

1. Clone the repo
2. `cd` into the root folder
3. Setup a virtual env
4. `pip install -r requirements.txt`

# karaoke_game

This program launches a game that attempts to recreate the game logic of singstar.  
The CLI can be used for several options like song selection or octave offsets.  

Once the game is launched the selected midi file is converted to notes that are displayed on the screen and fly from the right side 
of the screen to the left side. While they cross the play line on the left side of the screen, the user can use their voice to move the frequency cursor 
up and down the playline to score points if a note and the user's voice match.  

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

This program emulates up/down key presses based on a directional change of the user's voice pitch.  
It includes a demo mode with several rectangles that can be selected using the arrow keys, which are also emulated via voice input.  

## Usage

Help Command: `python ./whistle_input/whistle-input.py --help`

1. Run the application in demo mode to view the demo UI
    `python ./whistle_input/whistle-input.py -d`
2. Select your microphone in the prompt 
3. Make a `ooouuuiii` sound (low to high pitch) to emulate `Key.UP`
4. Make a `iiiuuuooo` sound (high to low pitch) to emulate `Key.DOWN`

The button presses are emulated using `pynput` and are broadcasted to the entire system.  
You can **omit** the `-d` flag to run the program in the background.  
Use the `-v` flag for logs.

Depending on the microphone used and background noise level, the `--sensitivity` might need to be adjusted.  
The sensitivity can range from `0` to `10` and defaults to `6`. 

After testing with a studio microphone at my PC setup both whistling and `ìioouu/oouuii` sound worked reliable to emulate arrow keys.  
Speech and "non pitch-changing" were mostly filtered out as well.  
