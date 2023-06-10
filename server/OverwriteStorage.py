from django.core.files.storage import FileSystemStorage

class OverwriteStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        """
        Returns the name of the file that doesn't already exist in the storage
        and doesn't contain a hash appended to the end of the filename.
        """
        return name