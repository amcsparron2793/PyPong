from pathlib import Path
from pygame import mixer


class Sound:
    SOUNDS_DEFAULT_LOCATION = Path('../Misc_Project_Files/Sounds')
    HIGH_BEEP_FILENAME = 'HighBeep.mp3'
    LOW_BEEP_FILENAME = 'LowBeep.mp3'
    def __init__(self, **kwargs):
        self.sounds_dir = kwargs.get('sounds_dir', self.SOUNDS_DEFAULT_LOCATION)
        self.high_beep_full_path = self.sounds_dir / kwargs.get('high_beep_filename', self.HIGH_BEEP_FILENAME)
        self.low_beep_full_path = self.sounds_dir / kwargs.get('low_beep_filename', self.LOW_BEEP_FILENAME)
        self.sfx_mixer = mixer
        self.sfx_mixer.init()
        self.high_beep = self.sfx_mixer.Sound(str(self.high_beep_full_path))
        self.low_beep = self.sfx_mixer.Sound(str(self.low_beep_full_path))