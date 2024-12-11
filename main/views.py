from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.db import transaction
from django.contrib.auth import login
from .models import User_Room
from .mangadex_api.manga import manga, thumbnail, genre, status_list, manga_chapter

import requests
import uuid
import json

# Create your views here.
def home(request, status='updated', genreType='all', page = 1):
    title = ''
    if request.method == 'POST':
        title = f'title={request.POST['search']}'
        status = 'updated'
        genreType = 'all'
        page = 1

    
    manga_list = manga(
        status = status.lower(),
        genre = genreType.lower(),
        title = title,
        page = page
    )
    request.session['manga_list'] = manga_list
    
    thumbnail_list = thumbnail(manga_list)
    genre_list = genre()

    pagination = list(range(page, (page + 5)))
    return render(
        request,
        'main/views/home.html',
        {'genre_list' : genre_list, 'thumbnail_list' : thumbnail_list, 'status' : status, 'type' : genreType, 'status_list' : status_list, 'pagination' : pagination}
    )


def sign_in(request):
    if not request.user.is_authenticated:
        return render(request, 'main/views/login.html')
    return redirect('home')



def sign_up(request):
    if not request.user.is_authenticated:
        data = {}
        if request.method == 'POST':
            with transaction.atomic():
                user_exist = User.objects.filter(username = request.POST['email']).exists()

                if not user_exist: #checking if the email not exists
                    register = User.objects.create_user(
                        username= request.POST['email'],
                        password = request.POST['password'],
                        )


                    create_room = User_Room(room_host = register)
                    create_room.save()

                    login(request, register)
                    return redirect('sign-in')
                else:
                    data['warning'] = 'Email already used'

        return render(request, 'main/views/register.html', data)
    return redirect('home')



def detail(request, id, title):
    if request.session.get('manga_list'):
        if request.session.get('manga_info') and id == request.session.get('manga_id'):
            return render(request, 'main/views/detail.html', {
                'manga_info' :request.session['manga_info'], 
                'title' : request.session['title'],
                'chapters' : request.session['chapters']
                })
        else:
            manga_info = request.session['manga_list'][title]
            chapters = manga_chapter(id)
            request.session['chapters'] = chapters
            request.session['title'] = title
            request.session['manga_id'] = id
            request.session['manga_info'] = manga_info
            request.session['latest'] = request.session['manga_list'][title]['chapter']['chapter']

            return render(request, 'main/views/detail.html', {
                'manga_info' : manga_info, 
                'title' : title,
                'chapters' : chapters
                })
    return redirect('home')



def chapter(request, id, index):
    if request.session.get('chapters'):
        try:
            id = request.session['chapters'][index - 1]['id']
            current_chapter = request.session['chapters'][index - 1]['attributes']['chapter']
        
            chapters = requests.get(f'https://api.mangadex.org/at-home/server/{id}')
            chapters = chapters.json()
            chapters = chapters['chapter']
            chapters_list = chapters['dataSaver']
            hash = chapters['hash']

            
            return render(request, 'main/views/chapter.html', {
                'chapters' : chapters_list,
                'hash' : hash,
                'next' : index + 1,
                'prev' : index - 1,
                'id' : id,
                'current_chapter' : current_chapter,
                'title' : request.session['title'],
                'manga_id' : request.session['manga_id'],
                'latest' : int(request.session['latest'])
            })
        except:
            redirect(home)
    return redirect('home')