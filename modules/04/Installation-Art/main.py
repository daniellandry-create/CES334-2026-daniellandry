from forest import *
import sound_lib
import time
import random
import sounddevice as sd

branches = [
    Branch(
        id=0,
        x_loc=2.0,
        y_loc=2.0,
        bpm=sound_lib.TEMPOS[0],
        tweets=sound_lib.TWEETS[1]
    ),
    Branch(
        id=1,
        x_loc=5.0,
        y_loc=5.0,
        bpm=sound_lib.TEMPOS[1],
        tweets=sound_lib.TWEETS[1]
    ),
    Branch(
        id=2,
        x_loc=3.0,
        y_loc=5.5,
        bpm=sound_lib.TEMPOS[2],
        tweets=sound_lib.TWEETS[1]
    ),
    Branch(
        id=3,
        x_loc=8.0,
        y_loc=8.0,
        bpm=sound_lib.TEMPOS[2],
        tweets=sound_lib.TWEETS[0]
    ),
    Branch(
        id=4,
        x_loc=9.0,
        y_loc=1.0,
        bpm=sound_lib.TEMPOS[3],
        tweets=sound_lib.TWEETS[0]
    ),
    Branch(
        id=5,
        x_loc=2.0,
        y_loc=2.0,
        bpm=sound_lib.TEMPOS[0],
        tweets=sound_lib.TWEETS[1]
    ),
    Branch(
        id=6,
        x_loc=5.0,
        y_loc=5.0,
        bpm=sound_lib.TEMPOS[1],
        tweets=sound_lib.TWEETS[1]
    ),
    Branch(
        id=7,
        x_loc=3.0,
        y_loc=5.5,
        bpm=sound_lib.TEMPOS[2],
        tweets=sound_lib.TWEETS[1]
    ),
    Branch(
        id=8,
        x_loc=8.0,
        y_loc=8.0,
        bpm=sound_lib.TEMPOS[2],
        tweets=sound_lib.TWEETS[0]
    ),
    Branch(
        id=9,
        x_loc=9.0,
        y_loc=1.0,
        bpm=sound_lib.TEMPOS[3],
        tweets=sound_lib.TWEETS[0]
    ),
    Branch(
        id=10,
        x_loc=2.0,
        y_loc=2.0,
        bpm=sound_lib.TEMPOS[0],
        tweets=sound_lib.TWEETS[1]
    ),
    Branch(
        id=11,
        x_loc=5.0,
        y_loc=5.0,
        bpm=sound_lib.TEMPOS[1],
        tweets=sound_lib.TWEETS[1]
    )
]

birds = [
    Bird(id=0), 
    Bird(id=1)
]

forest_manager = ForestManager(birds, branches)

MIN_WAIT = 1
MAX_WAIT = 3

# def wait_for_audio(timeout=60):
#     start = time.time()
#     while time.time() - start < timeout:
#         try:
#             sd.query_devices(kind="output")   # raises if there is no output device
#             return
#         except Exception:
#             time.sleep(1)
#     raise RuntimeError("No audio output device found")

# wait_for_audio()

print(sd.query_devices())

# Execution loop
while True:
    # Step 1: Sync bird info with socket script
    forest_manager.update_bird_data()

    # Step 2: Choose a bird
    bird = forest_manager.select_bird()

    # Step 3: Skip invalid birds
    if not bird.on_branch or bird.melody_obj.volume == 0:
        time.sleep(0.5)
        continue

    # Step 4: Play bird melody
    bird.sing()

    # Step 5: Update mating scores and execute mating
    forest_manager.update_mating_scores(bird)

    # Step 6: Wait random duration
    time.sleep((random.random() * (MAX_WAIT - MIN_WAIT)) + MIN_WAIT)