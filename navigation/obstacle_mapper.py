class ObstacleMapper:

    def __init__(self):

        # No object → safest
        self.default_distance = 0

    def get_zone(self, x_center, frame_width):

        left_limit = frame_width * 0.33
        right_limit = frame_width * 0.66

        if x_center < left_limit:
            return "LEFT"

        elif x_center > right_limit:
            return "RIGHT"

        return "CENTER"

    def analyze_obstacles(
        self,
        detections,
        depth_map,
        frame_width
    ):

        zone_distances = {
            "LEFT": self.default_distance,
            "CENTER": self.default_distance,
            "RIGHT": self.default_distance
        }

        zone_has_object = {
            "LEFT": False,
            "CENTER": False,
            "RIGHT": False
        }

        for det in detections:

            x1, y1, x2, y2 = det["bbox"]

            x_center = int((x1 + x2) / 2)
            y_center = int((y1 + y2) / 2)

            depth_value = depth_map[
                y_center,
                x_center
            ]

            zone = self.get_zone(
                x_center,
                frame_width
            )

            zone_has_object[zone] = True

            # Keep nearest obstacle
            zone_distances[zone] = max(
                zone_distances[zone],
                depth_value
            )

        return zone_distances, zone_has_object
    
