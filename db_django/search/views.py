from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import *
from .serializers import UserSerializer

def index(request):
    data_all = Data.objects

    if request.method == 'POST':
        genre = request.POST.get('genre')
        occupation = request.POST.get('occupation')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        max_rating = request.POST.get('max_rating')
        min_rating = request.POST.get('min_rating')
        sort = request.POST.get('sort')

        query1 = '''select genre.gid, genre.genre_name, genre_movie.mid , movie.title from genre, genre_movie, movie
                    where genre.gid = genre_movie.gid and genre_movie.mid = movie.mid'''

        if genre != 'All genre':
            # qs2 = genre_join.filter(genre_name=genre)
            query1 += ''' and genre.genre_name = "%s" ''' % genre

        query2 = '''select * from user '''

        if occupation != '' and gender is not None and age != 'all':
            query2 += '''where occup = "%s" and gender = "%s" and age >= %d and age <= %d ''' % (occupation, gender, int(age), int(age)+9)

        elif occupation != '' and gender is None and age == 'all':
            query2 += '''where occup = "%s" ''' % occupation
        elif occupation == '' and gender is not None and age == 'all':
            query2 += '''where gender = "%s" ''' % gender
        elif occupation == '' and gender is None and age != 'all':
            query2 += '''where age >= %d and age <= %d ''' % (int(age), int(age)+9)
        elif occupation != '' and gender is not None and age == 'all':
            query2 += '''where occup = "%s" and gender = "%s" ''' % (occupation, gender)
        elif occupation != '' and gender is None and age != 'all':
            query2 += '''where occup = "%s" and age >= %d and age <= %d ''' % (occupation, int(age), int(age)+9)
        elif occupation == '' and gender is not None and age != 'all':
            query2 += '''where gender = "%s" and age >= %d and age <= %d ''' % (gender, int(age), int(age)+9)

        query3 = '''select dd.mid, dd.uid, ud.avg_rate, ud.votes from (select d.mid, dd.uid, avg(dd.rating) as avg_rate, d.votes from (''' + query2 + ''') u , (select mid, count(uid) as votes from data group by mid) d,
        data dd
        where u.uid = dd.uid and d.mid = dd.mid group by mid) ud, data dd where ud.mid = dd.mid '''

        # print(query3)

        if max_rating != '' and min_rating != '':
            query3 += '''and ud.avg_rate >= %f and ud.avg_rate <= %d order by mid ''' % (float(min_rating), float(max_rating))
        elif max_rating != '' and min_rating == '':
            query3 += '''and ud.avg_rate <= %f order by mid ''' % float(max_rating)
        elif max_rating == '' and min_rating != '':
            query3 += '''and ud.avg_rate >= %f order by mid ''' % float(min_rating)

        query_sum = '''select distinct y.mid, x.title, y.votes, y.avg_rate, x.genre_name from (''' + query1 + ''') x, (''' + query3 + ''') y where x.mid = y.mid group by mid'''

        if sort == 'votes':
            query_sum += ''' order by y.votes desc'''
        elif sort == 'title':
            query_sum += ''' order by x.title'''
        elif sort == 'avg_rate':
            query_sum += ''' order by y.avg_rate desc'''
        elif sort == 'mid':
            query_sum += ''' order by y.mid'''
        print(query_sum)

        print(genre, max_rating, min_rating, occupation, gender, age)

        data_all = data_all.raw(query_sum)

        context = {
            'data': data_all,
            'genre': genre,
            'max_rating':max_rating,
            'min_rating': min_rating,
            'occupation': occupation,
            'gender': gender,
            'age': age,
            'sort': sort,
        }

        return render(request, 'search/index.html', context)

    return render(request, 'search/index.html')


@api_view(['GET', 'POST'])
def user(request):
    User_queryset = User.objects.all()
    serializer_class = UserSerializer(User_queryset, many=True)

    if request.method == 'GET':
        return Response(serializer_class.data)
    else:
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@api_view(['GET', 'POST'])
def user_detail(request, no):
    User_queryset = User.objects.all().filter(uid=no)
    serializer_class = UserSerializer(User_queryset, many=True)

    if request.method == 'GET':
        return Response(serializer_class.data)
    else:
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)