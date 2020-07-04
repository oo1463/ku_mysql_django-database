
from django.db import models


class Data(models.Model):
    mid = models.OneToOneField('Movie', models.DO_NOTHING, primary_key=True, null=False, db_column='mid')
    uid = models.ForeignKey('User', models.DO_NOTHING, null=False, db_column='uid')
    rating = models.IntegerField()
    timestamp = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'data'
        unique_together = (('uid', 'mid'),)


class Genre(models.Model):
    gid = models.IntegerField(primary_key=True)
    genre_name = models.CharField(unique=True, max_length=12)

    class Meta:
        managed = False
        db_table = 'genre'


class GenreMovie(models.Model):
    gid = models.OneToOneField(Genre, models.DO_NOTHING, primary_key=True, related_name='related_genre', db_column='gid')
    mid = models.ForeignKey('Movie', models.DO_NOTHING, related_name='related_movie', db_column='mid')

    class Meta:
        managed = False
        db_table = 'genre_movie'
        unique_together = (('gid', 'mid'),)


class Movie(models.Model):
    mid = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=100)
    r_date = models.CharField(max_length=20, blank=True, null=True)
    v_date = models.CharField(max_length=20, blank=True, null=True)
    url = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'movie'


class User(models.Model):
    uid = models.IntegerField(primary_key=True)
    age = models.IntegerField()
    gender = models.CharField(max_length=1)
    zipcode = models.CharField(max_length=5)
    occup = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'user'
