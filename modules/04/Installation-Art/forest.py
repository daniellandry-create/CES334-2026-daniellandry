from birds import *
import sound_lib

import numpy as np
from dataclasses import dataclass, asdict
from typing import Sequence
import random
import json
import time
from urllib.request import urlopen
from urllib.parse import urlencode

"""
Derived from bird genes:
    - Pitches
    - Beats
    - Type

Derived from branch:
    - BPM
    - Tweets

Derived from light sensor:
    - Volume

"""

MATING_THRESHOLD = 100

BRANCH_MATCH_SCORE = 5
BRANCH_DIFF_SCORE = 3
GENE_MATCH_SCORE = 0
GENE_DIFF_SCORE = 5

DIST_BAND_1_THRESH = 3
DIST_BAND_2_THRESH = 7

DIST_BAND_1_MULT = 1
DIST_BAND_2_MULT = 0.75
DIST_BAND_3_MULT = 0.5

HTTP_PORT = "8080"

# ============================================================
# Bird Class Definition
# ============================================================

@dataclass
class BirdMelody:
    bird_type: BirdType
    bpm: float
    beats: Sequence[float]
    pitches: Sequence[int | None]
    tweets: Sequence[int]
    volume: float

class Bird:
    id: int
    melody_obj: BirdMelody
    melody_sample: np.ndarray
    on_branch: bool
    x_loc: float
    y_loc: float

    # Set by the forest manager
    index: int

    def __init__(self, id: int):
        self.id = id
        self.x_loc = 0
        self.y_loc = 0
        self.melody_obj = get_random_melody()
        self.melody_sample = get_sample_from_melody(self.melody_obj)
        self.on_branch = False

    def sing(self):
        play_audio(self.melody_sample)

    def mate(self, other: "Bird"):
        # Reassign pitches, beats, and type for each bird
        pitches_1 = self.melody_obj.pitches
        pitches_2 = other.melody_obj.pitches

        beats_1 = self.melody_obj.beats
        beats_2 = other.melody_obj.beats

        type_1 = self.melody_obj.bird_type
        type_2 = other.melody_obj.bird_type

        assign_mated_traits(self, pitches_1, pitches_2, beats_1, beats_2, type_1, type_2)
        assign_mated_traits(other, pitches_1, pitches_2, beats_1, beats_2, type_1, type_2)

        time.sleep(1)
        play_audio(MATING_MELODY)

    def calculate_score(self, other: "Bird"):
        # Calculate mating score based on the compatibility of the two birds
        score = 0

        # Branch trait scores

        # BPM Check
        if self.melody_obj.bpm == other.melody_obj.bpm:
            score += BRANCH_MATCH_SCORE
        else:
            score += BRANCH_DIFF_SCORE

        # Tweets Check
        if self.melody_obj.tweets == other.melody_obj.tweets:
            score += BRANCH_MATCH_SCORE
        else:
            score += BRANCH_DIFF_SCORE

        # Gene trait scores

        # Pitches Check
        if self.melody_obj.pitches == other.melody_obj.pitches:
            score += GENE_MATCH_SCORE
        else:
            score += GENE_DIFF_SCORE

        # Beats Check
        if self.melody_obj.beats == other.melody_obj.beats:
            score += GENE_MATCH_SCORE
        else:
            score += GENE_DIFF_SCORE

        # Type Check
        if self.melody_obj.bird_type == other.melody_obj.bird_type:
            score += GENE_MATCH_SCORE
        else:
            score += GENE_DIFF_SCORE

        # Score scaling

        # Distance scaling
        distance = ((self.x_loc - other.x_loc) ** 2 + (self.y_loc - other.y_loc) ** 2) ** 0.5

        if distance < DIST_BAND_1_THRESH:
            score *= DIST_BAND_1_MULT
        elif distance < DIST_BAND_2_THRESH:
            score *= DIST_BAND_2_MULT
        else:
            score *= DIST_BAND_3_MULT

        # Volume scaling
        score *= self.melody_obj.volume

        return score

# ============================================================
# Branch Class Definition
# ============================================================

@dataclass
class Branch:
    id: int
    x_loc: float
    y_loc: float
    bpm: int
    tweets: Sequence[int]

# ============================================================
# Forest Manager Class Definition
# ============================================================

class ForestManager:
    birds: list[Bird]
    branches: dict[int, Branch]
    num_birds: int
    mating_scores: list[list[float]]

    def __init__(
        self,
        birds: list[Bird],
        branches: list[Branch]
    ):
        self.birds = birds

        self.branches = {}

        for branch in branches:
            self.branches[branch.id] = branch
    
        self.num_birds = len(self.birds)
        self.mating_scores = [[0] * self.num_birds for _ in range(self.num_birds)]

        for i, bird in enumerate(self.birds):
            bird.index = i

    def update_bird_data(self):
        for bird in self.birds:
            # Get data by id
            data = get_state_http(bird.id)

            print(f"Data: {data}")

            # Bird not on branch
            if data.get("branch") is None or data.get("branch") == -1:
                bird.on_branch = False
                bird.melody_sample = get_sample_from_melody(bird.melody_obj)

                continue

            branch = self.branches[data.get("branch", 0)]

            bird.on_branch = True
            bird.x_loc = branch.x_loc
            bird.y_loc = branch.y_loc
            bird.melody_obj.bpm = branch.bpm
            bird.melody_obj.tweets = branch.tweets
            bird.melody_obj.volume = data.get("volume", 0.0)

            bird.melody_sample = get_sample_from_melody(bird.melody_obj)

    def update_mating_scores(self, source_bird: Bird):
        # Iterate through all birds (not matching id of source bird) and add calculated score
        # If any bird is over the threshold, mate, clear all other mating scores for the mated birds, and break

        for bird in self.birds:
            if bird.id == source_bird.id:
                continue

            if not bird.on_branch:
                continue

            score = source_bird.calculate_score(bird)

            # Update score in one direction
            self.mating_scores[source_bird.index][bird.index] += score

            # Check for mate
            if self.mating_scores[source_bird.index][bird.index] >= MATING_THRESHOLD:
                # These two birds should mate
                source_bird.mate(bird)

                # Reset their scores with all other birds
                for i in range(self.num_birds):
                    self.mating_scores[bird.index][i] = 0
                    self.mating_scores[i][bird.index] = 0
                    self.mating_scores[source_bird.index][i] = 0
                    self.mating_scores[i][source_bird.index] = 0

                # Break from update loop
                break

            # Update in the other
            self.mating_scores[bird.index][source_bird.index] += score

    def select_bird(self) -> Bird:
        return random.choice(self.birds)

def get_state_http(bird_id: int):
    params = urlencode({"bird_id": bird_id})

    try:
        with urlopen(f"http://127.0.0.1:{HTTP_PORT}/birds?{params}") as response:
            return json.load(response)
    except:
        return {}

def assign_mated_traits(
        bird: Bird, 
        pitches_1: Sequence[int | None],
        pitches_2: Sequence[int | None],
        beats_1: Sequence[float],
        beats_2: Sequence[float],
        type_1: BirdType,
        type_2: BirdType
):
    pitch_parent = random.random()
    beat_parent = random.random()
    type_parent = random.random()

    # Assign pitch
    if pitch_parent < 0.4:
        # Inherit from parent 1
        bird.melody_obj.pitches = pitches_1
        print("Pitch parent 1")
    elif pitch_parent < 0.8:
        # Inherit from parent 2
        bird.melody_obj.pitches = pitches_2
        print("Pitch parent 2")
    else:
        # Get random
        notes = random.choice(sound_lib.NOTES)
        key = random.choice(sound_lib.KEYS)
    
        bird.melody_obj.pitches = tuple(key[note] for note in notes)
        print("Pitch random")

    # Assign beats
    if beat_parent < 0.4:
        # Inherit from parent 1
        bird.melody_obj.beats = beats_1
        print("Beat parent 1")
    elif beat_parent < 0.8:
        # Inherit from parent 2
        bird.melody_obj.beats = beats_2
        print("Beat parent 2")
    else:
        # Get random
        bird.melody_obj.beats = random.choice(sound_lib.RHYTHMS)
        print("Beat random")

    # Assign type
    if type_parent < 0.4:
        # Inherit from parent 1
        bird.melody_obj.bird_type = type_1
        print("Type parent 1")
    elif type_parent < 0.4:
        # Inherit from parent 2
        bird.melody_obj.bird_type = type_2
        print("Type parent 2")
    else:
        # Get random
        bird.melody_obj.bird_type = random.choice(sound_lib.BIRD_TYPES)
        print("Type random")

    bird.melody_sample = get_sample_from_melody(bird.melody_obj)

def get_sample_from_melody(melody: BirdMelody):
    return synth_melody(
        melody.bpm,
        melody.beats,
        melody.pitches,
        melody.tweets,
        melody.bird_type,
        melody.volume,
        False
    )

def get_random_melody():
    rhythm = random.choice(sound_lib.RHYTHMS)

    # Construct pitches from notes and key
    notes = random.choice(sound_lib.NOTES)
    key = random.choice(sound_lib.KEYS)

    pitches = tuple(key[note] for note in notes)
    
    tweets = random.choice(sound_lib.TWEETS)
    tempo = random.choice(sound_lib.TEMPOS)

    bird_type = random.choice(sound_lib.BIRD_TYPES)
    volume = random.random()

    return BirdMelody(
        bird_type=bird_type,
        bpm=tempo,
        beats=rhythm,
        pitches=pitches,
        tweets=tweets,
        volume=volume
    )