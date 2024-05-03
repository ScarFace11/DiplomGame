import pygame
from maze_settings import maze_settings
class GameMusicAndSounds:
    def __init__(self):
        super().__init__()
        self.MusicOn = maze_settings.GameMusicOn
        self.SoundOn = maze_settings.GameSoundOn

    def MusicRun(self):
        if (self.MusicOn == True):
            pygame.mixer.music.load(self.path)
            pygame.mixer.music.play(self.play)
            pygame.mixer.music.set_volume(0.01 * maze_settings.Settings_MusicVolume)

    def SoundRun(self):
        if (self.SoundOn == True):
            pygame.mixer.music.load(self.path)
            pygame.mixer.music.play(self.play)
            pygame.mixer.music.set_volume(0.01 * maze_settings.Settings_SoundVolume)
    #@run_once
    def MusicOff():
        pygame.mixer.music.unload()
    """      
    def run_once(f):
        def wrapper(*args, **kwargs):
                if not wrapper.has_run:
                        wrapper.has_run = True
                        return f(*args, **kwargs)
        wrapper.has_run = False
        return wrapper
    """
class GameSound(GameMusicAndSounds):
    def __init__(self):
        super().__init__()
    #@run_once
    def Finish(self):
        self.path = "Sound/Background/Finish.wav"
        self.play = 0
        #self.volume = 0.5
        self.SoundRun()
        #pygame.mixer.music.load("Sound/Background/Finish.wav")
        #pygame.mixer.music.play(0)
        #pygame.mixer.music.set_volume(0.5)
        
        
    """
    P.S Оказывается можно было обойтись и без этого, run_once уже не нужен
    без декоратора @run_once функция Finish будет производиться в цикле бессконечно раз
    для вызова функции используется
    либо #GameMusic.Finish() либо GameMusic.run_once(GameMusic.Finish()) если они вызываются из других файлов

    для вызова:
    #action = GameMusic.run_once(GameMusic.Finish)   
    #action()
    #action.has_run = False
    """
class GameMusic(GameMusicAndSounds):
    def __init__(self):
        super().__init__()   

    def Background(self):
            self.path = "Sound/Background/BeepBox-Song.wav"
            self.play = -1
            #self.volume = 0.2
            self.MusicRun()

            #pygame.mixer.music.load("Sound/Background/BeepBox-Song.wav")
            #pygame.mixer.music.play(-1)
            #pygame.mixer.music.set_volume(0.2)

    