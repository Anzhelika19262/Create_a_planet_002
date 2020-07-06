from moviepy.editor import VideoFileClip
from game_logic import variables
import pygame


def load_video_file(name):
    clip = VideoFileClip(name)
    clip.preview()
    pygame.display.set_mode(variables.size)
