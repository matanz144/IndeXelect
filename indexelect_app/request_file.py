import io
import os
import csv
from django.shortcuts import render


class RequestFile(object):
    def __init__(self, request):
        self.request = request
        self.file = None
        self.request_file_name = ''
        self.error = ''

    def get_file(self):
        if self.file is not None:
            return self.file
        files = self.request.FILES
        if not files:
            self.error = 'No file supplied'
            return None
        if len(files) > 1:
            self.error = 'More than one file supplied'
            return None
        file_data = next(files.values())
        self.request_file_name = str(file_data)
        # self.file = io.StringIO(file_data.read().decode())
        self.file = io.TextIOWrapper(file_data.file, encoding='utf-8')
        return self.file

    def get_csv_reader(self):
        csv_file = self.get_file()
        if csv_file is None:
            return None
        return csv.DictReader(csv_file, delimiter=',')

    def save(self, directory, name=None):
        if name is None:
            name = self.request_file_name
        path = os.path.join(directory, name)
        try:
            with open(path, 'w') as disk_file:
                disk_file.write(self.get_file().read())
            return True
        except:
            return False

    def file_name(self):
        return self.request_file_name

    def error_response(self):
        return render(self.request, 'error_form.html', {'error_msg': self.error})
