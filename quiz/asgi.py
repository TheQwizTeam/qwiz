import os
import channels.layers

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "quiz.settings")
channel_layer = channels.layers.get_channel_layer()
