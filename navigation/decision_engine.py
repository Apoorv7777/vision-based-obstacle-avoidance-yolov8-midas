class DecisionEngine:

    def __init__(self):

        # Above this → dangerous
        self.danger_threshold = 100

    def decide(
        self,
        zone_distances,
        zone_has_object
    ):

        left = zone_distances["LEFT"]
        center = zone_distances["CENTER"]
        right = zone_distances["RIGHT"]

        left_has = zone_has_object["LEFT"]
        center_has = zone_has_object["CENTER"]
        right_has = zone_has_object["RIGHT"]

        # If center safe
        if center < self.danger_threshold:
            return "FORWARD"

        # Prefer empty lane
        if not left_has:
            return "MOVE LEFT"

        if not right_has:
            return "MOVE RIGHT"

        # Choose safer lane (lower depth safer)
        if left < right and left < self.danger_threshold:
            return "MOVE LEFT"

        if right < left and right < self.danger_threshold:
            return "MOVE RIGHT"

        return "STOP"