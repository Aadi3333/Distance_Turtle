#!/usr/bin/env python3

# Import Dependencies
import rospy 
from geometry_msgs.msg import Twist
from std_msgs.msg import Float64
from turtlesim.msg import Pose
import math

class DistanceReader:
    def __init__(self):
        # Initialize the node
        rospy.init_node('turtlesim_distance_node', anonymous=True)

        # Initialize subscriber: input the topic name, message type and callback signature  
        rospy.Subscriber("/turtle1/pose", Pose, self.callback)

        # Initialize publisher: input the topic name, message type and msg queue size
        self.distance_publisher = rospy.Publisher('/turtle_dist', Float64, queue_size=10)

        # Store previous position of the turtle
        self.prev_x = 0
        self.prev_y = 0

        # Initialize total distance traveled
        self.total_distance = 0.0

        # Initialize flag to track whether the turtle is moving
        self.turtle_moving = False

        # Initialize time when the turtle last stopped
        self.last_stop_time = rospy.Time.now()

        # Printing to the terminal, ROS style
        rospy.loginfo("Initialized node!")

        # This blocking function call keeps python from exiting until node is stopped
        rospy.spin()

    # Whenever a message is received from the specified subscriber, this function will be called
    def callback(self, msg):
        rospy.loginfo("Turtle Position: %s %s", msg.x, msg.y)

        ########## YOUR CODE GOES HERE ##########
        # Calculate the distance between current and previous position
        distance = math.sqrt((msg.x - self.prev_x)**2 + (msg.y - self.prev_y)**2)

        # Check if the turtle is moving
        if distance > 0.01:  # You can adjust this threshold as needed
            # Update total distance traveled
            self.total_distance += distance

            # Set turtle moving flag to True
            self.turtle_moving = True

            # Update the last stop time
            self.last_stop_time = rospy.Time.now()

        else:
            # If the turtle was moving previously and has now stopped for more than 1 second, publish the total distance
            if self.turtle_moving and (rospy.Time.now() - self.last_stop_time).to_sec() > 1.0:
                self.distance_publisher.publish(self.total_distance)

            # Reset total distance and turtle moving flag
            self.total_distance = 0.0
            self.turtle_moving = False

        # Update previous position
        self.prev_x = msg.x
        self.prev_y = msg.y
        ###########################################

if __name__ == '__main__': 
    try: 
        distance_reader_class_instance = DistanceReader()
    except rospy.ROSInterruptException: 
        pass

