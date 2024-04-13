def get_target_location(target_x, target_y, image_width, image_height, latitude, longitude, width_feet, height_feet):
    """
        Translate the coordinate of target (px, px) to coordinate in real life (longtitude, latitude)
        Input:
            target_x, target_y: coordinate of target in image (px, px)
            image_width, image_height: the size of image containing the target (px, px)
            latitude, longtitude: the real coordinate of the drone capturing the image (degree, degree)
            width_feet, height_feet: the size of the area captured in the image (ft)

        Return:
            latitude, longitude of the target (degree, degree)
    """
    # Convert feet to degrees
    latitude_per_foot = 1.0/364000
    longitude_per_foot = 1.0/288200

    # Calculate the number of degrees per pixel
    latitude_per_pixel = latitude_per_foot * height_feet / image_height
    longitude_per_pixel = longitude_per_foot * width_feet / image_width

    # Calculate the target's latitude and longitude
    target_latitude = latitude - (target_y - (image_height / 2)) * latitude_per_pixel
    target_longitude = longitude + (target_x - (image_width / 2)) * longitude_per_pixel

    return (target_latitude, target_longitude)

if __name__ == "__main__":
    target_latitude, target_longitude = get_target_location(100, 200, 3040, 4032, 37.4419, -122.1430, 30, 40)
    print(f"Target latitude: {target_latitude}")
    print(f"Target longitude: {target_longitude}")