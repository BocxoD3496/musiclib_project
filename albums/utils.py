import json
import xml.etree.ElementTree as ET
from pathlib import Path
from uuid import uuid4
from django.conf import settings
from django.core.exceptions import ValidationError

ALLOWED_EXT = {'.json', '.xml'}
UPLOAD_DIR = Path(settings.MEDIA_ROOT) / 'uploads'
EXPORT_DIR = Path(settings.MEDIA_ROOT) / 'exports'
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
EXPORT_DIR.mkdir(parents=True, exist_ok=True)

def album_to_json_dict(album_data):
    return {
        'title': album_data['title'],
        'artist': album_data['artist'],
        'year': int(album_data['year']),
        'genre': album_data.get('genre',''),
        'tracks': int(album_data.get('tracks',0)),
    }

def save_as_json(album_data):
    data = album_to_json_dict(album_data)
    filename = f"album_{uuid4().hex}.json"
    path = EXPORT_DIR / filename
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return path.name

def save_as_xml(album_data):
    data = album_to_json_dict(album_data)
    root = ET.Element('album')
    for k,v in data.items():
        el = ET.SubElement(root, k)
        el.text = str(v)
    filename = f"album_{uuid4().hex}.xml"
    path = EXPORT_DIR / filename
    tree = ET.ElementTree(root)
    tree.write(path, encoding='utf-8', xml_declaration=True)
    return path.name

def valid_album_dict(d):
    try:
        title = d['title']
        artist = d['artist']
        year = int(d['year'])
        tracks = int(d.get('tracks',0))
    except Exception:
        raise ValidationError('Поля album должны содержать title, artist и year (число).')
    if year < 1800 or year > 2100:
        raise ValidationError('Неверный год в данных')
    if tracks < 0:
        raise ValidationError('Неверное кол-во треков')
    return {'title': title, 'artist': artist, 'year': year, 'genre': d.get('genre',''), 'tracks': tracks}

def parse_json_file(path: Path):
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return valid_album_dict(data)

def parse_xml_file(path: Path):
    tree = ET.parse(path)
    root = tree.getroot()
    d = {}
    for child in root:
        d[child.tag] = child.text
    return valid_album_dict(d)

def is_allowed_ext(filename):
    return Path(filename).suffix.lower() in ALLOWED_EXT

def save_uploaded_file(file_obj):
    suffix = Path(file_obj.name).suffix.lower()
    if suffix not in ALLOWED_EXT:
        raise ValidationError('Недопустимый тип файла')
    name = f"upload_{uuid4().hex}{suffix}"
    path = UPLOAD_DIR / name
    with open(path, 'wb') as dest:
        for chunk in file_obj.chunks():
            dest.write(chunk)
    return path
