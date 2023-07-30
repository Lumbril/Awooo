from geopy.distance import geodesic


def get_distance(points):
    distance = 0

    for i in range(len(points) - 1):
        point_curr = (points[i].latitude, points[i].longitude)
        point_next = (points[i + 1].latitude, points[i + 1].longitude)
        distance += geodesic(point_curr, point_next).km

    return distance
