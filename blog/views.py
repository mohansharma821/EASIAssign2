from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post
from .forms import PostForm
import json
from watson_developer_cloud import ToneAnalyzerV3
from watson_developer_cloud import LanguageTranslatorV2 as LanguageTranslator


# def post_list(request):
#   posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
#  return render(request, 'blog/post_list.html', {'posts': posts})

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    tone_analyzer = ToneAnalyzerV3(
        username='a9fb8a45-e00f-4ab6-8e69-0570d2999555',
        password='APYmbTFKZlwz',
        version='2016-05-19')

    language_translator = LanguageTranslator(
        username='cac9c73e-89f1-455a-a350-2c93ca5f9cb7',
        password='ctlJDlbc0jtK')

    # print(json.dumps(translation, indent=2, ensure_ascii=False))

    for post in posts:
        data = json.dumps(tone_analyzer.tone(text=post.text), indent=1)  # converting to string and storing in the data
        j = json.loads(data);
        post.info = j['document_tone']['tone_categories'][0]['tones']
        # post.info = json.dumps(post.info);
        post.angerScore = post.info[0]['score']
        post.disgustScore = post.info[1]['score']
        post.fearScore = post.info[2]['score']
        post.joyScore = post.info[3]['score']
        post.sadScore = post.info[4]['score']
        # print(post.info[0]['tone_name'])
        translation = language_translator.translate(
            text=post.text,
            source='en',
            target='ar')
        post.translatedText = json.dumps(translation, indent=2, ensure_ascii=False)
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    # Post.objects.get(pk=pk)
    tone_analyzer = ToneAnalyzerV3(
        username='a9fb8a45-e00f-4ab6-8e69-0570d2999555',
        password='APYmbTFKZlwz',
        version='2016-05-19')

    language_translator = LanguageTranslator(
        username='cac9c73e-89f1-455a-a350-2c93ca5f9cb7',
        password='ctlJDlbc0jtK')
    data = json.dumps(tone_analyzer.tone(text=post.text), indent=1)  # converting to string and storing in the data
    j = json.loads(data);
    post.info = j['document_tone']['tone_categories'][0]['tones']
    # post.info = json.dumps(post.info);
    post.angerScore = post.info[0]['score']
    post.disgustScore = post.info[1]['score']
    post.fearScore = post.info[2]['score']
    post.joyScore = post.info[3]['score']
    post.sadScore = post.info[4]['score']
    # print(post.info[0]['tone_name'])
    translation = language_translator.translate(
        text=post.text,
        source='en',
        target='ar')
    post.translatedText = json.dumps(translation, indent=2, ensure_ascii=False)
    return render(request, 'blog/post_detail.html', {'post': post})


def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})