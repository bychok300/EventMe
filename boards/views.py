from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404

from .forms import NewTopicForm, CustomCommentForm
from .models import Board, Topic, Post, Comments


def home(request):
    boards = Board.objects.all()
    return render(request, 'home.html', {'boards': boards})


def board_topics(request, pk):
    board = get_object_or_404(Board, pk=pk)
    return render(request, 'topics.html', {'board': board})


def new_topic(request, pk):
    board = get_object_or_404(Board, pk=pk)
    user = request.user    # TODO: get the currently logged in user
    if request.method == 'POST':
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
    topic = get_object_or_404(Topic, pk=pk)
    post = get_object_or_404(Post, pk=pk)
    #comment = get_object_or_404(Comments, pk=pk)
    # if request.method == 'POST':
    #     form = CustomCommentForm(request.POST)
    #     if form.is_valid():
    #         comment = form.save(commit=False)
    #         comment.save()
    #         comment = Comments.objects.create(
    #             comment=form.cleaned_data.get('comment'),
    #
    #         )
    #         return redirect('board_topics', pk=comment.pk)  # TODO: redirect to the created topic page
    # else:
    #     form = CustomCommentForm()
    return render(request, 'post.html', {'post': post, 'topic': topic})


