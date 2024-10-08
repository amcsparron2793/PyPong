from pathlib import Path
from pygame import mixer


class Sound:
    SOUNDS_DEFAULT_LOCATION = Path('../Misc_Project_Files/Sounds')
    HIGH_BEEP_FILENAME = 'HighBeep.mp3'
    LOW_BEEP_FILENAME = 'LowBeep.mp3'
    PLAYER_MISSED_FILENAME = 'PlayerMissed.mp3'
    def __init__(self, **kwargs):
        self._initialize_files(kwargs)
        self._initialize_mixer()
        self._initialize_sounds()

    def _initialize_files(self, kwargs=None):
        self._sounds_dir = kwargs.get('sounds_dir', self.SOUNDS_DEFAULT_LOCATION)
        self._high_beep_full_path = self._sounds_dir / kwargs.get('high_beep_filename', self.HIGH_BEEP_FILENAME)
        self._low_beep_full_path = self._sounds_dir / kwargs.get('low_beep_filename', self.LOW_BEEP_FILENAME)
        self._player_missed_full_path = self._sounds_dir / kwargs.get('player_missed_filename',
                                                                      self.PLAYER_MISSED_FILENAME)

    def _initialize_mixer(self):
        self.sfx_mixer = mixer
        self.sfx_mixer.init()

    def _initialize_sounds(self):
        self.high_beep = self.sfx_mixer.Sound(str(self._high_beep_full_path))
        self.low_beep = self.sfx_mixer.Sound(str(self._low_beep_full_path))
        self.player_missed = self.sfx_mixer.Sound(str(self._player_missed_full_path))