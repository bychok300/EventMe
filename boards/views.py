import json

from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from .forms import NewTopicForm, CustomCommentForm, EditFormTopic, EditFormPost, DeleteForm
from .models import Board, Topic, Post, Comments, WhoComeOnEvent

# вьюс это представления
# они связаны с урлами, т.е. при переходе по урлу будет показан какой-то вью
#
# в этом методе получают все объекты таблицы board и просто их отрисовывают


def home(request):
    boards = Board.objects.all()
    return render(request, 'home.html', {'boards': boards})

# по аналогии с методом хоум, только сдесь берется объект или 404
# то есть если объект получить не удалось будет ошибка 404
# второй параметор это первичный ключ
# он отображается в урл паттерне


def board_topics(request, pk):
    board = get_object_or_404(Board, pk=pk)
    return render(request, 'topics.html', {'board': board})


# этот метод создает новый топик
def new_topic(request, pk):
    board = get_object_or_404(Board, pk=pk)
    user = request.user    # get the currently logged in user
    if request.method == 'POST':
        #инициализируем форму
        form = NewTopicForm(request.POST, request.FILES)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = user
            topic.save()
            post = Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=user,
            )
            return redirect('board_topics', pk=board.pk)  # redirect to the created topic page
    else:
        form = NewTopicForm()
    return render(request, 'new_topic.html', {'board': board, 'form': form})


def delete_topic(request, pk, id):
    board = get_object_or_404(Board, pk=pk)
    if request.method == 'POST':
        topic = Topic.objects.filter(id=id)
        topic.delete()
        return redirect('board_topics', pk=board.pk)
    return render(request, 'delete_topic.html', {'board': board})


def edit_topic(request, pk, id):
    board = get_object_or_404(Board, pk=pk)
    top = get_object_or_404(Topic, id=id)
    post = Post.objects.get(id=id)
    user = request.user    # get the currently logged in user
    if request.method == 'POST':
        #инициализируем форму
        form_topic = EditFormTopic(request.POST, request.FILES, instance=top)
        form_post = EditFormPost(request.POST, instance=post)
        if form_topic.is_valid() and form_post:
            topic = form_topic.save(commit=False)
            post = form_post.save(commit=False)
            topic.board = board
            topic.starter = user
            topic.save()
            post.save()
            return redirect('board_topics', pk=board.pk)
    else:
        form_topic = EditFormTopic(instance=top)
        form_post = EditFormPost(instance=post)
    return render(request, 'edit_topic.html', {'board': board, 'form_topic': form_topic, 'form_post': form_post})


def p(request, pk):
    user = request.user
    topic = get_object_or_404(Topic, pk=pk)
    post = get_object_or_404(Post, pk=pk)
    comment = Comments.objects.filter(pk=pk)
    who_come = WhoComeOnEvent.objects.filter(which_event=topic.id).distinct('visiter')
    is_already_coming = False

    if request.is_ajax() and request.POST.get('action') == 'joinEvent':
        who_come_obj = WhoComeOnEvent.objects.create(
            visiter=user,
            which_event=post.topic
        )

        visitors_usernames = []
        for w in who_come:
            visitors_usernames.append(w.visiter.username)

        return HttpResponse(json.dumps(visitors_usernames))

    if request.method == 'POST':
        form = CustomCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.creator = user
            # comment.save() #из-за этой блевотины было 2 записи в базу
            comment = Comments.objects.create(
                body=form.cleaned_data.get('body'),
                creator=user,
                post=post
            )

            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            # return render(request, 'post.html', {'post': post, 'topic': topic, 'comment': comment,
            #                                      'form': form, 'who_come': who_come})
    else:

        form = CustomCommentForm()

    return render(request, 'post.html', {'post': post, 'topic': topic, 'comment': comment,
                                         'form': form, 'who_come': who_come, 'is_already_coming': is_already_coming} )

    #     comment_body = request.POST.get('body')
    #     response_data = {}
    #
    #     comment = Comments(body=comment_body, creator=request.user)
    #     comment.save()
    #     response_data['body'] = comment.body
    #     response_data['created_at'] = comment.created_at.strftime('%B %d, %Y %I:%M %p')
    #     response_data['creator'] = comment.creator.username
    #     return HttpResponse(json.dumps(response_data))
    #
    # else:
    #
    #     return HttpResponse(json.dumps({"nothing to see": "this isn't happening"}))
