import common
import filters
import pygame_io

evoutput = pygame_io.PygameOutput(0)
evfilter = filters.DelayFilter(output)
evinput  = pygame_io.PygameInput(0)
