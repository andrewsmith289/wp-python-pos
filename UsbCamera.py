from os import system
from SharedUtilities import generate_random, ensure_path_exists, delete_old_files


class UsbCamera:

    device_id = 0
    save_path = ""
    file_type = ""
    resolution = None

    def __init__(self, save_path, file_type="jpg", device_id=1, resolution=(1280, 720)):
        self.set_save_path(save_path)
        self.device_id = device_id
        self.format = format
        self.file_type = file_type
        self.resolution = resolution

    def set_save_path(self, path):
        if path[-1] is not "/":
            path += "/"
        self.save_path = path

    def save_image(self, title, name):
        ensure_path_exists(self.save_path)

        name = str.replace(name, ' ', '_')
        rand = generate_random(12)
        full_path = str(self.save_path) + str(name) + '_' + rand + '.' + self.file_type
        dev_id = self.device_id

        resolution = "%sx%s" % self.resolution
        cmd = "fswebcam -d /dev/video%s -r %s --title '%s' %s" % (dev_id, resolution, title, full_path)
        system(cmd)

        return full_path

    def remove_old_captures(self, days_old=30):
        delete_old_files(self.save_path, days_old)
