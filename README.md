To hear the sound remove the top two lines from sound.py. Make sure your system has acces to a sound device or it will crash. The lines are:

import os
os.environ['SDL_AUDIODRIVER'] = 'dummy'
