
class Commands:

    def precise3(self, first, second, third):
        if second - 5 <= first <= second + 5 and third - 5 <= first <= third + 5:
            return True

    def approximate3(self, first, second, third):
        if second - 10 <= first <= second + 10 and third - 10 <= first <= third + 10:
            return True

    def approximate2(self, first, second):
        if second - 10 <= first <= second + 10:
            return True

    def vague2(self, first, second):
        if second - 20 <= first <= second + 20:
            return True

    def drone_takeoff(self, landmarks):
        if landmarks["leftWristY"] < landmarks["noseY"] or landmarks["rightWristY"] < landmarks["noseY"]:
            return True
        else:
            return False

    def drone_lands(self, landmarks):
        """Checks dictionary 'landmarks' to see if the drone needs to land"""
        if landmarks["leftWristX"] < landmarks["rightWristX"] and landmarks["leftWristY"] > landmarks["leftShoulderY"]:
            return True
        else:
            return False

    def drone_right(self, landmarks):
        if self.approximate3(landmarks["leftWristY"], landmarks["leftElbowY"], landmarks["leftShoulderY"]) and \
                self.approximate3(landmarks["rightWristX"], landmarks["rightElbowX"], landmarks["rightShoulderX"]):
            return True
        else:
            return False

    def drone_left(self, landmarks):
        if self.approximate3(landmarks["rightWristY"], landmarks["rightElbowY"], landmarks["rightShoulderY"]) and \
                    self.approximate3(landmarks["leftWristX"], landmarks["leftElbowX"], landmarks["leftShoulderX"]):
            return True
        else:
            return False

    def drone_up(self, landmarks):
        if landmarks["leftWristY"] < landmarks["noseY"] - 10 and landmarks["rightWristY"] < landmarks["noseY"] - 10:
            return True
        else:
            return False

    def drone_forward(self, landmarks):
        if landmarks["leftWristX"] < landmarks["leftShoulderX"] and \
                landmarks["leftShoulderY"] < landmarks["leftWristY"] < landmarks["leftElbowY"] and \
                landmarks["rightWristX"] > landmarks["rightShoulderX"] and landmarks["rightShoulderY"] < \
                landmarks["rightWristY"] < landmarks["rightElbowY"]:
            return True
        else:
            return False

    def drone_backwards(self, landmarks):
        if self.approximate3(landmarks["rightWristX"], landmarks["rightShoulderX"], landmarks["rightElbowX"]) and \
                self.approximate3(landmarks["rightWristY"], landmarks["rightShoulderY"], landmarks["rightElbowY"]):
            return True
        else:
            return False

    def drone_change_mode(self, landmarks):
        if self.approximate2(landmarks["leftWristY"], landmarks["rightWristY"]) and \
                self.vague2(landmarks["leftWristX"], landmarks["rightWristX"]) and \
                landmarks["rightWristY"] < landmarks["rightShoulderY"]:
            return True
        else:
            return False

    def drone_follow_left(self, landmarks, mid):
        if landmarks["noseX"] > mid and (landmarks["noseX"] - mid) > 50:    # the 50 is the "sweet spot"
            return True
        else:
            return False

    def drone_follow_right(self, landmarks, mid):
        if mid > landmarks["noseX"] and (mid - landmarks["noseX"]) > 50:    # the 50 is the "sweet spot"
            return True
        else:
            return False

    def drone_follow_down(self, landmarks, mid_height):
        if landmarks["leftShoulderY"] > mid_height + 30:
            return True
        else:
            return False

    def drone_follow_up(self, landmarks, mid_height):
        if landmarks["leftShoulderY"] < mid_height - 30:
            return True
        else:
            return False

    def drone_stop_moving(self, landmarks, mid_width, mid_height, starting_distance, current_distance):
        if (mid_width - 30) < landmarks["noseX"] < (mid_width + 30):
            print("DRONE STAYS PUT CLOCKWISE")
            return True
        elif (starting_distance + 6) > current_distance > (starting_distance - 6):
            print("DRONE X FOLLOW STOP MOVING")
            return True
        elif mid_height - 15 > landmarks["leftShoulderY"] > mid_height:
            print("DRONE X STOP MOVING HEIGHT")
            return True
        else:
            return FalseS