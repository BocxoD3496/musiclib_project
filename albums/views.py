from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from .forms import AlbumForm
from . import utils
from pathlib import Path

EXPORT_DIR = Path(settings.MEDIA_ROOT) / 'exports'
UPLOAD_DIR = Path(settings.MEDIA_ROOT) / 'uploads'

def album_create(request):
    if request.method == 'POST':
        form = AlbumForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            album_data = {
                'title': cd['title'],
                'artist': cd['artist'],
                'year': cd['year'],
                'genre': cd['genre'],
                'tracks': cd['tracks'],
            }
            fmt = cd['export_format']
            if fmt == 'json':
                fname = utils.save_as_json(album_data)
            else:
                fname = utils.save_as_xml(album_data)
            messages.success(request, f'Файл сохранён: {fname}')
            return redirect('albums:album_create')
    else:
        form = AlbumForm()
    return render(request, 'albums/album_form.html', {'form': form})

def files_list(request):
    files = []
    for p in sorted(EXPORT_DIR.glob('*')):
        if p.suffix.lower() in ['.json','.xml']:
            files.append(p.name)
    if not files:
        messages.info(request, 'Файлов экспорта не найдено')
    return render(request, 'albums/file_list.html', {'files': files})

def upload_file(request):
    if request.method == 'POST' and request.FILES.get('datafile'):
        f = request.FILES['datafile']
        try:
            saved_path = utils.save_uploaded_file(f)
            try:
                if saved_path.suffix.lower() == '.json':
                    parsed = utils.parse_json_file(saved_path)
                else:
                    parsed = utils.parse_xml_file(saved_path)
            except Exception as e:
                saved_path.unlink(missing_ok=True)
                messages.error(request, f'Файл не валиден: {e}')
                return render(request, 'albums/upload_result.html', {'ok': False, 'message': str(e)})
            return render(request, 'albums/upload_result.html', {'ok': True, 'filename': saved_path.name, 'parsed': parsed})
        except Exception as e:
            messages.error(request, str(e))
    return render(request, 'albums/upload_result.html')

def show_all_uploaded_contents(request):
    items = []
    for p in sorted(UPLOAD_DIR.glob('*')):
        try:
            if p.suffix.lower() == '.json':
                d = utils.parse_json_file(p)
            elif p.suffix.lower() == '.xml':
                d = utils.parse_xml_file(p)
            else:
                continue
            items.append({'name': p.name, 'data': d})
        except Exception:
            continue
    if not items:
        messages.info(request, 'Загруженных файлов с корректными данными не найдено')
    return render(request, 'albums/file_list.html', {'uploaded_items': items})
