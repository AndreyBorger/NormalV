from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum

class Author(models.Model):

    # Модель содержащая объекты всех авторов

    user = models.OneToOneField(User, on_delete=models.CASCADE)  # ID пользователя, который является автором
    author_rating = models.IntegerField(default=0)

    def update_rating(self):

        # Обновление и расчёт рейтинга
        author_posts_rating = Post.objects.all().filter(author_id=self.pk).aggregate(posts_rating_sum =Sum('post_rating') * 3)
        author_comments_rating = Comment.objects.all().filter(user_id=self.pk).aggregate(comments_rating_sum = Sum('comment_rating'))
        others_comments_rating = Comment.objects.all().aggregate(other_comments_rating_sum = Sum('comment_rating'))

        print(others_comments_rating['other_comments_rating_sum'])

        self.author_rating = author_posts_rating['posts_rating_sum'] + author_comments_rating['comments_rating_sum'] + others_comments_rating['other_comments_rating_sum']
        self.save()

class Category(models.Model):

    # Категории новостей/статей

    category_name = models.CharField(max_length=25, unique=True)  # Название категории


class Post(models.Model):

    # Содержит в себе статьи/новости

    ART = 'С'
    NEWS = 'Н'

    TYPES = [(ART, 'Статья'), (NEWS, 'Новость')]

    # ID автора поста
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    # Тип поста (статья/новость)
    post_type = models.CharField(max_length=10, choices=TYPES)
    # Дата и время создания поста
    created_at = models.DateTimeField(auto_now_add=True)
    # Категория поста
    post_category = models.ManyToManyField(Category)
    # Заголовок статьи/новости
    post_title = models.CharField(max_length=120)
    # Текст статьи/новости
    post_text = models.TextField()
    # Рейтинг статьи/новости
    post_rating = models.IntegerField(default=0)

    def like(self):
        self.post_rating += 1
        self.save()


    def dislike(self):
        self.post_rating -= 1
        self.save()


    def preview(self):
        return self.post_text[:125] + '...'


class PostCategory(models.Model):

    # Промежуточная модель для связи "многие ко многим"

    category_PostCategory = models.ManyToManyField(Category)
    post_PostCategory = models.ForeignKey(Post, on_delete=models.CASCADE)


class Comment(models.Model):

    # Комментарии к постам

    # ID поста
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    # ID пользователя, оставившего комментарий
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Текст комментария
    comment_text = models.CharField(max_length=255)
    # Время создания комментария
    created_at = models.DateTimeField(auto_now_add=True)
    comment_rating = models.IntegerField(default=0)

    def like(self):
        self.comment_rating += 1
        self.save()


    def dislike(self):
        self.comment_rating -= 1
        self.save()

