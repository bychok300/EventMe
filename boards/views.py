from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404

from .forms import NewTopicForm, CustomCommentForm
from .models import Board, Topic, Post, Comments

# вьюс это представления
# они связаны с урлами, т.е. при переходе по урлу будет показан какой-то вью
#
# в этом методе получают все объекты таблицы board и просто их отрисовывают


def home(request):
    boards = Board.objects.all()
    return render(request, 'home.html', {'boards': boards})

# по аналогии с методом хоум, только сдесь берется объект или 404
# то есть если объект получить не удалось будет ошибка 404
# второй параметор это первичный ключь
# хз как описать его влияние
# типо по нему обращаются к таблице


def board_topics(request, pk):
    board = get_object_or_404(Board, pk=pk)
    return render(request, 'topics.html', {'board': board})


# этот метод создает новый топик
def new_topic(request, pk):
    board = get_object_or_404(Board, pk=pk)
    user = request.user    # get the currently logged in user
    if request.method == 'POST':
        #инициализируем форму
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = user
            topic.save()
            post = Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=user
            )
            return redirect('board_topics', pk=board.pk)  # TODO: redirect to the created topic page
    else:
        form = NewTopicForm()
    return render(request, 'new_topic.html', {'board': board, 'form': form})


def p(request, pk):
    user = request.user
    topic = get_object_or_404(Topic, pk=pk)
    post = get_object_or_404(Post, pk=pk)
    comment = Comments.objects.filter(pk=pk)
    if request.method == 'POST':
        form = CustomCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.creator = user
            comment.save()
            comment = Comments.objects.create(
                body=form.cleaned_data.get('body'),
                creator=user,

            )
            return render(request, 'post.html', {'post': post, 'topic': topic, 'comment': comment, 'form': form})
    else:
        form = CustomCommentForm()
    return render(request, 'post.html', {'post': post, 'topic': topic, 'comment': comment, 'form': form})


