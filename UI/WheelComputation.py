__author__ = 'Matt'

import cmath
from MathHelpers import *
import numpy
from UI.RobotData import ManualControlData

# hard coded
FL_WHEEL_POS = (-67/2.0, -49)
ML_WHEEL_POS = (-67/2.0, 0.0)
RL_WHEEL_POS = (-67/2.0, 49)

FR_WHEEL_POS = (67/2.0, -49)
MR_WHEEL_POS = (67/2.0, 0.0)
RR_WHEEL_POS = (67/2.0, 49)


WHEEL_MATRIX = numpy.matrix([
    [-2, -2],
    [-2,  2],
    [2.5,  2],
    [2.5,  10.5],
    [30,  10.5],
    [30, -10.5],
    [2.5, -10.5],
    [2.5, -2]
])

WHEEL_POS_MATRIX = numpy.matrix([
    [-33.5, -67],   # FL
    [33.5, -67],    # FR
    [-33.5, 0],     # ML
    [33.5, 0],      # MR
    [-33.5, -67],   # RL
    [33.5, -67],    # RR
])

WHEEL_CENTER_OFFSET = 16.75


##
# Computes the angle that a given wheel needs to drive at for the entire system to drive along an arc
#
##
def calc_articulation_angle(wheel_position, arc_center, go_forward):

    adjacent = wheel_position[0]-arc_center[0]
    # tangent = cmath.pi
    articulation_theta = 90

    if not go_forward:
        if adjacent != 0:
            opposite = wheel_position[1]-arc_center[1]

            tangent = opposite/float(adjacent)

            articulation_theta = cmath.atan(tangent)

            articulation_theta = articulation_theta/cmath.pi*180

    return articulation_theta.real


##
# Computes the speed that a given wheel needs to drive at for the entire system to drive along an arc
#
##
def calc_wheel_speed(wheel_position, arc_center, go_forward):

    if go_forward:
        wheel_drive_speed = 1
    else:
        wheel_arc_radius = dist(*wheel_position+arc_center)

        if wheel_position[0] < 0 and arc_center[0] < wheel_position[0]:
            wheel_arc_radius += WHEEL_CENTER_OFFSET
        if wheel_position[0] > 0 and arc_center[0] > wheel_position[0]:
            wheel_arc_radius += WHEEL_CENTER_OFFSET

        if wheel_position[0] > 0 and arc_center[0] < wheel_position[0]:
            wheel_arc_radius -= WHEEL_CENTER_OFFSET
        if wheel_position[0] < 0 and arc_center[0] > wheel_position[0]:
            wheel_arc_radius -= WHEEL_CENTER_OFFSET


        wheel_drive_speed = 1/float(wheel_arc_radius)

    return wheel_drive_speed


##
# normalizes the speeds of each wheel so that the maximum is one, and all others are some fraction.
#   Still maintains speed ratios needed for driving in an arc
#
##
def normalize_wheel_speeds(data):

    values = [data.fl_drive_speed,
              data.fr_drive_speed,
              data.ml_drive_speed,
              data.mr_drive_speed,
              data.rl_drive_speed,
              data.rr_drive_speed]

    maxValue = float(max(values))

    data.fl_drive_speed /= maxValue
    data.fr_drive_speed /= maxValue
    data.ml_drive_speed /= maxValue
    data.mr_drive_speed /= maxValue
    data.rl_drive_speed /= maxValue
    data.rr_drive_speed /= maxValue

    return