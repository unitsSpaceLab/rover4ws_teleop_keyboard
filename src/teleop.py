#!/usr/bin/env python3.8

import rospy
from geometry_msgs.msg import Twist
from pynput import keyboard

def clip(x,min_val,max_val):
    if x < min_val:
        x = min_val
    elif x > max_val:
        x = max_val

    return x

def on_press(key):
    global current_msg
    try:
        if key.char == 'w':
            current_msg.linear.x += delta_x

        if key.char == 'x':
            current_msg.linear.x -= delta_x

        if key.char == 'a':
            current_msg.linear.y += delta_y

        if key.char == 'd':
            current_msg.linear.y -= delta_y

        if key.char == 'q':
            current_msg.angular.z += delta_theta
        
        if key.char == 'e':
            current_msg.angular.z -= delta_theta
        if key.char == 's':
            current_msg = Twist()

        #Clipping
        current_msg.linear.x = clip(current_msg.linear.x, -max_vel_lin, max_vel_lin)
        current_msg.linear.y = clip(current_msg.linear.y, -max_vel_lin, max_vel_lin)
        current_msg.angular.z = clip(current_msg.angular.z, -max_vel_ang, max_vel_ang)
        
    except:
        pass

def on_release(key):
    msg_to_print = 'Current commanded velocity is: linear x: %f; \t linear y: %f; \t angular z: %f;\n' % (current_msg.linear.x, current_msg.linear.y, current_msg.angular.z)
    rospy.loginfo(msg_to_print)


if __name__ == '__main__':
    rospy.init_node('teleop_node', anonymous=True) #Start ROS node
    vel_publisher = rospy.Publisher('/cmd_vel', Twist,queue_size=1) #Create publisher on /cmd_vel topic
    global current_msg
    current_msg = Twist() #Initialize empty message

    # Load Teleop ROS package parameters
    delta_x = rospy.get_param("delta_x_speed", default=0.1)
    delta_y = rospy.get_param("delta_y_speed", default=0.1)
    delta_theta = rospy.get_param("delta_theta_speed", default=0.1)
    max_vel_lin = rospy.get_param("max_lin_vel", default=1e9)
    max_vel_ang = rospy.get_param("max_ang_vel", default=1e9)
    cmd_publish_rate = rospy.get_param("cmd_publish_rate", default=10)




    #Start keyboard listener
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()


    time_start = rospy.Time.now().to_sec()
    period = 1/cmd_publish_rate

    debug_time = False

    while not rospy.is_shutdown():
        if (rospy.Time.now().to_sec() - time_start >= period):
            vel_publisher.publish(current_msg)
            time_start=rospy.Time.now().to_sec()

        if debug_time:
            print(rospy.Time.now().to_sec() - time_start)

    rospy.spin()

    if rospy.is_shutdown():
        listener.stop()
        rospy.loginfo('Shutting down the teleop node...')
        








