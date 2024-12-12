from PySide6 import QtWidgets
from PySide6.QtCore import Slot, QObject, Signal, QPropertyAnimation, QPoint, QEasingCurve, QSize, Qt
import PySide6.QtCore as Core
from PySide6.QtCore import QRect, QPropertyAnimation, Property, QParallelAnimationGroup, QSequentialAnimationGroup
from src.SlotMachine.slot_generator import Reels, PlayingField
from PySide6.QtGui import QImageReader, QImage, QPixmap, QPicture
from math import *
import numpy as np
import random
import sys