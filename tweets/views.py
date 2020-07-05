from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
import random

from .forms import TweetForm
from .models import Tweet


def home_view(request, *args, **kwargs):
    return render(request, "pages/home.html", context={}, status=200)


def tweet_create_view(request, *args, **kwargs):
    form = TweetForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        form = TweetForm()
    return render(request, 'components/form.html', context={"form": form})


def tweet_list_view(request, *args, **kwargs):
    qs = Tweet.objects.all()
    tweet_list = [{"id": x.id, "content": x.content, "likes": random.randint(0, 1000)}
                  for x in qs]
    data = {
        "isUser": False,
        "response": tweet_list
    }
    return JsonResponse(data)


def tweet_detail_view(request, tweet_id, *args, **kwargs):
    """
    REST API VIEW
    Consume by Javascript or Swift/Java/IOS/Android
    return json data
    """
    status = 200
    data = {
        "id": tweet_id,
    }
    # obj = get_object_or_404(Tweet, id=tweet_id)
    try:
        obj = Tweet.objects.get(id=tweet_id)
        data["content"] = obj.content
    except:
        data["message"] = "Not found"
        status = 404

    # return HttpResponse(f"<h1>Hello Django {tweet_id} = {obj.content}</h1>")
    return JsonResponse(data, status=status)
    # return render(request, f"<h1>Hello Django {tweet_id} = {obj}</h1>")
