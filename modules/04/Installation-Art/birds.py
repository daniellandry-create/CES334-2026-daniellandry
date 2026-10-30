
import numpy as np
import sounddevice as sd

from enum import Enum
from dataclasses import dataclass, asdict
from typing import Sequence


SAMPLE_RATE = 44100


# ============================================================
# Presets for Bird Types
# ============================================================

class BirdType(Enum):
    SONGBIRD = "songbird"
    WARBLER = "warbler"
    SPARROW = "sparrow"
    CANARY = "canary"
    OWL = "owl"


@dataclass(frozen=True)
class BirdParams:
    octave: int
    sweep_st: float
    end_drop_st: float
    peak_at: float
    warble_hz: float
    warble_cents: float
    harmonic_strength: float
    noise_strength: float
    attack_ms: float
    release_ms: float
    gap_ms: float
    pitch_jitter_st: float


BIRD_TIMBRES = {
    BirdType.SONGBIRD: BirdParams(
        octave=7,
        sweep_st=9,
        end_drop_st=2,
        peak_at=0.30,
        warble_hz=18,
        warble_cents=12,
        harmonic_strength=0.03,
        noise_strength=0.005,
        attack_ms=3,
        release_ms=12,
        gap_ms=22,
        pitch_jitter_st=0.15,
    ),

    BirdType.WARBLER: BirdParams(
        octave=7,
        sweep_st=6,
        end_drop_st=4,
        peak_at=0.50,
        warble_hz=38,
        warble_cents=75,
        harmonic_strength=0.12,
        noise_strength=0.012,
        attack_ms=6,
        release_ms=16,
        gap_ms=35,
        pitch_jitter_st=0.25,
    ),

    BirdType.SPARROW: BirdParams(
        octave=6,
        sweep_st=4,
        end_drop_st=7,
        peak_at=0.20,
        warble_hz=45,
        warble_cents=45,
        harmonic_strength=0.28,
        noise_strength=0.045,
        attack_ms=2,
        release_ms=7,
        gap_ms=16,
        pitch_jitter_st=0.35,
    ),

    BirdType.CANARY: BirdParams(
        octave=7,
        sweep_st=12,
        end_drop_st=1,
        peak_at=0.65,
        warble_hz=24,
        warble_cents=30,
        harmonic_strength=0.07,
        noise_strength=0.006,
        attack_ms=4,
        release_ms=25,
        gap_ms=30,
        pitch_jitter_st=0.32,
    ),

    BirdType.OWL: BirdParams(
        octave=4,
        sweep_st=1,
        end_drop_st=3,
        peak_at=0.45,
        warble_hz=5,
        warble_cents=8,
        harmonic_strength=0.20,
        noise_strength=0.012,
        attack_ms=45,
        release_ms=90,
        gap_ms=140,
        pitch_jitter_st=0.05,
    ),
}


# ============================================================
# Audio Generation Utilities
# ============================================================

def duration_samples(beats, bpm):
    if bpm <= 0 or beats <= 0:
        raise ValueError("BPM and beats must be positive")

    n = round(SAMPLE_RATE * beats * 60 / bpm)

    if n < 1:
        raise ValueError("Note duration is too short")

    return n


def smoothstep(x):
    x = np.clip(x, 0, 1)
    return x * x * (3 - 2 * x)


def play_audio(audio):
    sd.play(audio, SAMPLE_RATE)
    sd.wait()


# ============================================================
# Low-level Synthesizer Function
# ============================================================

def synth_bird(
    pitch: int,
    beats: float = 0.5,
    bpm: float = 120,
    tweets: int = 2,
    volume: float = 0.3,
    *,
    octave: int = 7,
    sweep_st: float = 7,
    end_drop_st: float = 3,
    peak_at: float = 0.35,
    warble_hz: float = 25,
    warble_cents: float = 20,
    harmonic_strength: float = 0.08,
    noise_strength: float = 0.01,
    attack_ms: float = 5,
    release_ms: float = 20,
    gap_ms: float = 25,
    pitch_jitter_st: float = 0.15,
    _play: bool = True,
) -> np.ndarray:
    """
    Synthesize a single bird note, returning the sample as an ndarray

    pitch: Half-steps relative to C (0=C, 2=D, 4=E, ...)
    beats: Duration in quarter-note beats
    bpm: Tempo
    tweets: Number of chirps within the note
    volume: Amplitude between 0 and 1

    Other parameters control the timbre of the bird.

    _play=False returns samples without playing them.
    """

    if tweets < 1:
        raise ValueError("tweets must be at least 1")

    if not 0 <= volume <= 1:
        raise ValueError("volume must be between 0 and 1")

    if not 0 < peak_at < 1:
        raise ValueError("peak_at must be between 0 and 1")

    total_samples = duration_samples(beats, bpm)

    # Convert semitone pitch to frequency.
    base_freq = 440 * 2 ** (
        (pitch - 9 + 12 * (octave - 4)) / 12
    )

    # Allocate time for tweets and gaps.
    gap_n = round(gap_ms / 1000 * SAMPLE_RATE)

    if tweets > 1:
        # Keep at least half the duration available for chirps.
        gap_n = min(
            gap_n,
            total_samples // (2 * (tweets - 1))
        )
    else:
        gap_n = 0

    chirp_samples = total_samples - gap_n * (tweets - 1)
    base_n, remainder = divmod(chirp_samples, tweets)

    if base_n < 2:
        raise ValueError("Too many tweets for note duration")

    rng = np.random.default_rng()
    parts = []

    for i in range(tweets):
        n = base_n + (1 if i < remainder else 0)

        t = np.arange(n) / SAMPLE_RATE
        p = np.linspace(0, 1, n)

        # Pitch rises to a peak, then falls.
        rise = smoothstep(p / peak_at)
        fall = smoothstep((p - peak_at) / (1 - peak_at))

        sweep = (
            sweep_st * rise
            - (sweep_st + end_drop_st) * fall
        )

        # Rapid periodic frequency modulation.
        warble = (
            (warble_cents / 100)
            * np.sin(2 * np.pi * warble_hz * t)
            * np.sin(np.pi * p)
        )

        # Small random pitch variation between tweets.
        jitter = rng.normal(0, pitch_jitter_st)

        frequency = base_freq * 2 ** (
            (sweep + warble + jitter) / 12
        )

        # Integrate instantaneous frequency into phase.
        phase = 2 * np.pi * np.cumsum(frequency) / SAMPLE_RATE

        # Fundamental and harmonics.
        wave = (
            np.sin(phase)
            + harmonic_strength * np.sin(2 * phase)
            + 0.4 * harmonic_strength * np.sin(3 * phase)
        )

        # Breathiness / noisy components.
        wave += noise_strength * rng.standard_normal(n)

        # Attack envelope.
        if attack_ms > 0:
            attack = np.clip(
                t / (attack_ms / 1000), 0, 1
            ) ** 2
        else:
            attack = np.ones(n)

        # Release envelope.
        if release_ms > 0:
            release = np.clip(
                (t[-1] - t) / (release_ms / 1000),
                0, 1
            ) ** 2
        else:
            release = np.ones(n)

        # Rounded overall chirp shape.
        shape = np.sin(np.pi * p) ** 0.5

        wave *= attack * release * shape

        parts.append(wave)

        if i < tweets - 1:
            parts.append(np.zeros(gap_n))

    # Create sample as an ndarray
    audio = np.concatenate(parts).astype(np.float32)

    # Limit peaks to prevent clipping.
    peak = np.max(np.abs(audio))
    audio *= volume / max(1.0, float(peak))

    # Blocking
    if _play:
        play_audio(audio)

    return audio


# ============================================================
# Per-family Synthesizer Function 
# ============================================================

def synth_bird_from_family(
    bpm: float,
    beats: float,
    pitch: int | None,
    tweets: int,
    bird_type: BirdType,
    volume: float = 0.3,
    *,
    _play: bool = True,
) -> np.ndarray:
    """
    Play one note using a predefined bird timbre.

    Wraps around synth_bird to abstract low-level parameters. Retains the following:

    pitch: Half-steps relative to C (0=C, 2=D, 4=E, ...)
    beats: Duration in quarter-note beats
    bpm: Tempo
    tweets: Number of chirps within the note
    volume: Amplitude between 0 and 1

    pitch=None indicates a rest
    """

    if pitch is None:
        # A rest is an array of silence.
        audio = np.zeros(
            duration_samples(beats, bpm),
            dtype=np.float32
        )

        if _play:
            play_audio(audio)

        return audio

    # Simply index by bird type
    params = BIRD_TIMBRES[bird_type]

    return synth_bird(
        pitch=pitch,
        beats=beats,
        bpm=bpm,
        tweets=tweets,
        volume=volume,
        _play=_play,
        **asdict(params),
    )


# ============================================================
# Per-family melody synthesizer
# ============================================================

def synth_melody(
    bpm: float,
    beats: Sequence[float],
    pitches: Sequence[int | None],
    tweets: Sequence[int],
    bird_type: BirdType,
    volume: float = 0.3,
    _play: bool = True,
) -> np.ndarray:
    """
    Play a melody with a single bird timbre.

    pitch (sequence): Half-steps relative to C (0=C, 2=D, 4=E, ...)
    beats (sequence): Duration in quarter-note beats
    bpm: Tempo
    tweets (sequence): Number of chirps within the note
    volume: Amplitude between 0 and 1

    beats, pitches, and tweets must have equal lengths.
    Each index corresponds to one note or rest, played sequentially.
    """

    if not (len(beats) == len(pitches) == len(tweets)):
        raise ValueError(
            "beats, pitches, and tweets must have equal lengths"
        )

    if len(beats) == 0:
        raise ValueError("Melody must contain at least one note")

    audio_parts = []

    for note_beats, pitch, note_tweets in zip(
        beats, pitches, tweets
    ):
        audio = synth_bird_from_family(
            bpm=bpm,
            beats=note_beats,
            pitch=pitch,
            tweets=note_tweets,
            bird_type=bird_type,
            volume=volume,
            _play=False,
        )

        audio_parts.append(audio)

    # Concatenate notes to preserve precise timing.
    melody_audio = np.concatenate(audio_parts)

    if _play:
        play_audio(melody_audio)

    return melody_audio