import asyncio
import random

import aiohttp
from flask import flash, redirect, render_template, url_for

from . import app, db
from .constants import AUTH_HEADERS, DOWNLOAD_LINK_URL, REQUEST_UPLOAD_URL
from .forms import YacutForm, YacutUploadForm
from .models import URLMap


def get_unique_short_id(original_link, custom=None):
    symbols = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'

    if custom == 'files':
        flash('Предложенный вариант короткой ссылки уже существует.')
        return None

    if custom is None:
        short_id = ''.join(random.choices(symbols, k=6))

        if URLMap.query.filter_by(short=short_id).first():
            return get_unique_short_id(original_link)

    else:
        short_id = custom

        if URLMap.query.filter_by(short=short_id).first():
            flash('Предложенный вариант короткой ссылки уже существует.')
            return None

    new_data = URLMap(
        original=original_link,
        short=short_id,
    )
    db.session.add(new_data)
    db.session.commit()

    return short_id


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = YacutForm()
    short_link = None

    if form.validate_on_submit():

        short_link = get_unique_short_id(
            form.original_link.data,
            form.custom_id.data or None,
        )

    return render_template(
        'index.html',
        short_link=(
            url_for('redirect_view', short_id=short_link, _external=True)
            if short_link else None
        ),
        form=form,
    )


@app.route('/<string:short_id>')
def redirect_view(short_id):
    url_map = URLMap.query.filter_by(short=short_id).first_or_404()
    return redirect(url_map.original)


async def get_upload_url(session, filename):
    params = {
        'path': f'app:/{filename}',
        'overwrite': 'True',
    }

    async with session.get(
        REQUEST_UPLOAD_URL,
        headers=AUTH_HEADERS,
        params=params,
    ) as response:
        data = await response.json()
        return data['href']


async def upload_file(session, file, upload_url):
    async with session.put(
        upload_url,
        data=file.stream,
        headers=AUTH_HEADERS,
    ) as response:
        response.raise_for_status()

        return {
            'filename': file.filename,
            'location': response.headers['Location'],
        }


async def get_download_url(session, path):
    async with session.get(
        DOWNLOAD_LINK_URL,
        headers=AUTH_HEADERS,
        params={'path': path},
    ) as response:
        response.raise_for_status()
        data = await response.json()
        return data['href']


@app.route('/files', methods=['GET', 'POST'])
async def files_upload_view():
    form = YacutUploadForm()
    results = []

    if form.validate_on_submit():
        files = form.files.data

        async with aiohttp.ClientSession() as session:

            upload_urls = await asyncio.gather(
                *(
                    get_upload_url(session, file.filename)
                    for file in files
                )
            )

            upload_results = await asyncio.gather(
                *(
                    upload_file(session, file, upload_url)
                    for file, upload_url in zip(files, upload_urls)
                )
            )

            download_urls = await asyncio.gather(
                *(
                    get_download_url(
                        session,
                        f'app:/{file.filename}',
                    )
                    for file in files
                )
            )

        for result, download_url in zip(
            upload_results,
            download_urls,
        ):
            short_id = get_unique_short_id(download_url)

            results.append({
                'filename': result['filename'],
                'short_link': url_for(
                    'redirect_view',
                    short_id=short_id,
                    _external=True,
                ),
            })

    return render_template(
        'files.html',
        form=form,
        results=results,
    )