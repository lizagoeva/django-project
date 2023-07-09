from django.core.files.storage import FileSystemStorage
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def handle_file_upload(request: HttpRequest) -> HttpResponse:
    max_size_mb = 1
    if request.method == 'POST' and request.FILES.get('uploaded_file'):
        uploaded_file = request.FILES['uploaded_file']
        file_size_mb = uploaded_file.size / 1024 / 1024
        if file_size_mb > max_size_mb:
            print('Uploaded file is too big: {:.2f} Mb (max {} Mb)'.format(file_size_mb, max_size_mb))
            context = {
                'max_size_mb': max_size_mb,
                'uploaded_file_size_mb': file_size_mb,
            }
            return render(request, 'fileupload/file-too-big.html', context=context)

        file_sys_storage = FileSystemStorage()
        file_name = file_sys_storage.save(uploaded_file.name, uploaded_file)
        print(f'Был сохранён файл "{file_name}"')
    return render(request, 'fileupload/file-upload.html')
