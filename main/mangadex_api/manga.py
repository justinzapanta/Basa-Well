import requests


def manga(limit = 18, page = 1, title = '', genre = 'all', status = 'updated') -> dict :
    params={
        'limit' : limit,
        'offset' : limit * page,
        'contentRating[]' : ["safe", "suggestive", "erotica"],
    }
    
    if status != 'updated':
        params['status[]'] = status
    if genre != 'all':
        params['includedTags[]'] = genre

    response = requests.get(f'https://api.mangadex.org/manga?{title}', params=params) #title='manga name'
    results = response.json()
    
    manga_info = {} 
    for number, result in enumerate(results['data']): #filtering the data from mangadex api and storing it to manga_info dict
        manga_title = list(result['attributes']['title'].values())[0]
        
        manga_info[manga_title] = {}
        manga_info[manga_title]['id'] = result['id']
        manga_info[manga_title]['description'] = result['attributes']['description']
        manga_info[manga_title]['status'] = result['attributes']['status']
        manga_info[manga_title]['year'] = result['attributes']['year']
        manga_info[manga_title]['latest_chapter'] = result['attributes']['latestUploadedChapter']
        manga_info[manga_title]['author'] = []


        #get manga cover and storing it on manga_info dict
        try:
            params = {
                'manga[]' : manga_info[manga_title]['id'],
                'limit' : 1
            }
            manga_cover = requests.get('https://api.mangadex.org/cover', params=params)
            cover_json = manga_cover.json()
            cover = cover_json['data'][0]
            
            manga_info[manga_title]['cover'] = f'https://uploads.mangadex.org/covers/{manga_info[manga_title]['id']}/{cover['attributes']['fileName']}.512.jpg'
            
            #authors
            authors = result['relationships']

            for author in authors:
                if author['type'] == 'author':
                    author_info = requests.get(f'https://api.mangadex.org/author/{author['id']}')
                    author_info_json = author_info.json()
                    manga_info[manga_title]['author'].append(author_info_json['data']['attributes']['name'])
                    manga_info[manga_title]['author'].append(author_info_json['data']['attributes']['biography'])
        except:
            del manga_info[manga_title]
            continue
        
        #chapter
        try:
            get_chapter = requests.get(f'https://api.mangadex.org/chapter/{manga_info[manga_title]['latest_chapter']}')
            chapter_json = get_chapter.json()

            chapter = chapter_json['data']
            manga_info[manga_title]['chapter'] = {}
            manga_info[manga_title]['chapter']['volume'] = chapter['attributes']['volume']
            manga_info[manga_title]['chapter']['chapter'] = chapter['attributes']['chapter']
        except:
            del manga_info[manga_title] 
            continue




    return manga_info



def thumbnail(manga_list):
    card_list = []
    for index, manga in enumerate(manga_list):
        card_list.append([])
        card_list[index].append(manga_list[manga]['id'])
        card_list[index].append(manga_list[manga]['cover'])
        card_list[index].append(manga)
        card_list[index].append(manga_list[manga]['chapter'])

    return card_list


def genre():
    return [
        ['391b0423-d847-456f-aff0-8b0cfc03066b', 'Action'],
        ['87cc87cd-a395-47af-b27a-93258283bbc6', 'Adventure'],
        ['4d32cc48-9f00-4cca-9b5a-a839f0764984', 'Comedy'],
        ['5ca48985-9a9d-4bd8-be29-80dc0303db72', 'Crime'],
        ['b9af3a63-f058-46de-a9a0-e0c13906197a', 'Drama'],
        ['cdc58593-87dd-415e-bbc0-2ec27bf404cc', 'Fantasy'],
        ['33771934-028e-4cb3-8744-691e866a923e', 'Historical'],
        ['ee968100-4191-4968-93d3-f82d72be7e46', 'Mystery'],
        ['3b60b75c-a2d7-4860-ab56-05f391bb889c', 'Psychological'],
        ['423e2eae-a7a2-4a8b-ac03-a8351462d71d', 'Romance'],
        ['256c8bd9-4904-4360-bf4f-508a76d67183', 'Sci-Fi'],
        ['e5301a23-ebd9-49dd-a0cb-2add944c7fe9', 'Slice of life'],
        ['f8f62932-27da-4fe4-8ee1-6779a8c5edba', 'Tragedy']
    ]



def status_list():
    return ['Updated', 'Ongoing', 'Completed', 'Hiatus', 'Cancelled']



def manga_chapter(id):
    params = {
        'manga' : id,
        'translatedLanguage[]' : ['en'],
        'limit' : 100,
        'order[chapter]' : 'asc'
    }
    req_chapters = requests.get('https://api.mangadex.org/chapter', params=params)
    chapters_json = req_chapters.json()
    
    chapter_list = []
    chapter_checker = []
    start = True
    print(len(chapters_json['data']))
    for chapter in chapters_json['data']:
        if start:
            chapter_checker.append(chapter['attributes']['chapter'])
            chapter_list.append(chapter)
            start = False
        elif chapter['attributes']['chapter'] not in chapter_checker:
            chapter_checker.append(chapter['attributes']['chapter'])
            chapter_list.append(chapter)


    params = {
        'manga' : id,
        'translatedLanguage[]' : ['en'],
        'limit' : 100,
        'offset' : 100,
        'order[chapter]' : 'asc'
    }
    req_chapters = requests.get('https://api.mangadex.org/chapter', params=params)
    chapters_json = req_chapters.json()

    for chapter in chapters_json['data']:
        if start:
            chapter_checker.append(chapter['attributes']['chapter'])
            chapter_list.append(chapter)
            start = False
        elif chapter['attributes']['chapter'] not in chapter_checker:
            chapter_checker.append(chapter['attributes']['chapter'])
            chapter_list.append(chapter)

    return chapter_list