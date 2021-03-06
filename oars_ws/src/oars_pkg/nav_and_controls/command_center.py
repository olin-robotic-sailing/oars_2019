#!/usr/bin/env python

"""
Node to control other nodes via the command line. Publishes commands to
repeater.py, which repeatedly publishes them to the relevant topic. Values of
topics not set by this node are not published by it or the repeater.

Commands should be separated by spaces, with '=' separating names from values
and ',' separating individual values.

Set target position and absolute wind direction: `> tp=200,300 aw=180`

@Authors: Jane Sieving
"""

import rospy
from std_msgs.msg import Float32
from geometry_msgs.msg import Point32


class CommandCenter:
    def __init__(self, usingRos=True):
        self.usingRos = True if rospy is not None and usingRos else False
        # Initialize each message. These won't publish if unset.
        self.cp_msg = None
        self.tp_msg = None
        self.ch_msg = None
        self.th_msg = None
        self.aw_msg = None
        self.rw_msg = None
        self.wv_msg = None

        if self.usingRos:
            rospy.init_node('command', anonymous=True)
            print('command node initialized.')
            # Create a publisher to the command topic for each value
            self.pub_current_position = rospy.Publisher('cmd_cp', Point32, queue_size=1)
            self.pub_target_position = rospy.Publisher('cmd_tp', Point32, queue_size=1)
            self.pub_current_heading = rospy.Publisher('cmd_ch', Float32, queue_size=1)
            self.pub_target_heading = rospy.Publisher('cmd_th', Float32, queue_size=1)
            self.pub_abs_wind_dir = rospy.Publisher('cmd_aw', Float32, queue_size=1)
            self.pub_rel_wind_dir = rospy.Publisher('cmd_rw', Float32, queue_size=1)
            self.pub_wind_velocity = rospy.Publisher('cmd_wv', Float32, queue_size=1)

            while not rospy.is_shutdown():
                # wait for commands to send at the command line
                self.getCommands()

    def getCommands(self):
        # example: > cp=0,0 tp=200,200 ch=90
        # get input
        line = raw_input('> ')
        # split into individual commands, and handle each one
        commands = line.split(' ')
        for command in commands:
            # instr[0] is the value name to set, instr[1] is its value
            instr = command.split('=')

            if instr[0] in ['current_position', 'current_pos', 'curr_pos', 'cp']:  # check if command matches
                if instr[1].lower() in ['n', 'x']:
                    self.cp_msg = None
                    print("current_position unset.")
                else:
                    values = instr[1].split(',')                       # split x and y coords
                    if len(values) != 2:                               # make sure 2 were provided
                        print("Wrong number of arguments for current_position: expected 2.\n")
                        continue
                    x = float(values[0])
                    y = float(values[1])
                    print("current_position set to (%f, %f)." % (x, y))
                    self.cp_msg = Point32(x, y, 0)  # create a message and set it in the CommandCenter

            elif instr[0] in ['target_position', 'target_pos', 'tar_pos', 'tp']:
                if instr[1].lower() in ['n', 'x']:
                    self.tp_msg = None
                    print("target_position unset.")
                else:
                    values = instr[1].split(',')
                    if len(values) != 2:
                        print("Wrong number of arguments for target_position: expected 2.\n")
                        continue
                    x = float(values[0])
                    y = float(values[1])
                    print("target_position set to (%f, %f)." % (x, y))
                    self.tp_msg = Point32(x, y, 0)

            elif instr[0] in ['current_heading', 'curr_heading', 'ch']:
                if instr[1].lower() in ['n', 'x']:
                    self.ch_msg = None
                    print("current_heading unset.")
                else:
                    print("current_heading set to %s." % instr[1])
                    self.ch_msg = Float32(float(instr[1]))

            elif instr[0] in ['target_heading', 'tar_heading', 'th']:
                if instr[1].lower() in ['n', 'x']:
                    self.th_msg = None
                    print("target_heading unset.")
                else:
                    print("target_heading set to %s." % instr[1])
                    self.th_msg = Float32(float(instr[1]))

            elif instr[0] in ['abs_wind_dir', 'absolute_wind', 'abs_wind', 'aw']:
                if instr[1].lower() in ['n', 'x']:
                    self.aw_msg = None
                    print("abs_wind_dir unset.")
                else:
                    print("abs_wind_dir set to %s." % instr[1])
                    self.aw_msg = Float32(float(instr[1]))

            elif instr[0] in ['rel_wind_dir', 'relative_wind', 'rel_wind', 'rw']:
                if instr[1].lower() in ['n', 'x']:
                    self.rw_msg = None
                    print("rel_wind_dir unset.")
                else:
                    print("rel_wind_dir set to %s." % instr[1])
                    self.rw_msg = Float32(float(instr[1]))

            elif instr[0] in ['wind_velocity', 'wind_vel', 'wv', 'v']:
                if instr[1].lower() in ['n', 'x']:
                    self.wv_msg = None
                    print("wind_velocity unset.")
                else:
                    print("wind_velocity set to %s." % instr[1])
                    self.wv_msg = Float32(float(instr[1]))

            # no command names were matched for a given command
            else:
                print("Unrecognized command: " + instr[0])
                break  # this is safer than continuing, since the likely cause is incorrect formatting

        # publish whichever values have been set
        self.publishCommands()

    def publishCommands(self):
        n = 0
        if self.usingRos:
            # Publish whichever messages have been set
            if self.cp_msg is not None:
                self.pub_current_position.publish(self.cp_msg)
                n += 1
            if self.tp_msg is not None:
                self.pub_target_position.publish(self.tp_msg)
                n += 1
            if self.ch_msg is not None:
                self.pub_current_heading.publish(self.ch_msg)
                n += 1
            if self.th_msg is not None:
                self.pub_target_heading.publish(self.th_msg)
                n += 1
            if self.aw_msg is not None:
                self.pub_abs_wind_dir.publish(self.aw_msg)
                n += 1
            if self.rw_msg is not None:
                self.pub_rel_wind_dir.publish(self.rw_msg)
                n += 1
            if self.wv_msg is not None:
                self.pub_wind_velocity.publish(self.wv_msg)
                n += 1
            print("%d commands published." % n)


if __name__ == '__main__':
    CommandCenter()
    exit()
