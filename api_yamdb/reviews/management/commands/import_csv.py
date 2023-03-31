import pandas as pd
from django.core.management.base import BaseCommand

from reviews.models import (
    Category, Comment, Genre, GenreTitle, Review, Title, User,
)


class Command(BaseCommand):

    def handle(self, *args, **options):
        cat_data = pd.read_csv('./static/data/category.csv', sep=",")
        row_iter = cat_data.iterrows()
        category = [
            Category(
                id=row['id'],
                name=row['name'],
                slug=row['slug']
            )
            for index, row in row_iter
        ]
        Category.objects.bulk_create(category)

        genre_data = pd.read_csv('./static/data/genre.csv', sep=",")
        row_iter = genre_data.iterrows()
        genre = [
            Genre(
                id=row['id'],
                name=row['name'],
                slug=row['slug']
            )
            for index, row in row_iter
        ]
        Genre.objects.bulk_create(genre)

        title_data = pd.read_csv('./static/data/titles.csv', sep=",")
        row_iter = title_data.iterrows()
        titles = [
            Title(
                id=row['id'],
                name=row['name'],
                year=row['year'],
                category_id=row['category']
            )
            for index, row in row_iter
        ]
        Title.objects.bulk_create(titles)

        user_data = pd.read_csv("./static/data/users.csv", sep=",")
        # print(tmp_data)
        row_iter = user_data.iterrows()
        users = [
            User(
                id=row['id'],
                username=row['username'],
                email=row['email'],
                first_name=row['first_name'],
                last_name=row['last_name'],
                role=row['role'],
                bio=row['bio']
            )
            for index, row in row_iter
        ]
        User.objects.bulk_create(users)

        rev_data = pd.read_csv('./static/data/review.csv', sep=",")
        row_iter = rev_data.iterrows()
        review = [
            Review(
                id=row['id'],
                title_id=row['title_id'],
                text=row['text'],
                author_id=row['author'],
                score=row['score'],
                pub_date=row['pub_date']
            )
            for index, row in row_iter
        ]
        Review.objects.bulk_create(review)

        tmp_data = pd.read_csv('./static/data/genre_title.csv', sep=",")
        row_iter = tmp_data.iterrows()
        genre_title = [
            GenreTitle(
                id=row['id'],
                genre_id=row['genre_id'],
                title_id=row['title_id']
            )
            for index, row in row_iter
        ]
        GenreTitle.objects.bulk_create(genre_title)

        comm_data = pd.read_csv('./static/data/comments.csv', sep=",")
        row_iter = comm_data.iterrows()
        comments = [
            Comment(
                id=row['id'],
                review_id=row['review_id'],
                text=row['text'],
                author_id=row['author'],
                pub_date=row['pub_date']
            )
            for index, row in row_iter
        ]
        Comment.objects.bulk_create(comments)

    print('Данные успешно импортированы')
