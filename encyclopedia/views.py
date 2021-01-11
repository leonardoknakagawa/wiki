from django import forms
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from . import util
from markdown2 import Markdown
import random
import re

wiki_entries_directory = "entries/"


class NewForm(forms.Form):
    title = forms.CharField(label="Title", widget=forms.TextInput(attrs={'size': '30', 'style': 'width:1000px'}))
    content = forms.CharField(label="Content", widget=forms.Textarea(attrs={'style': 'width:1000px'}))



def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry):
    entry_contents = util.get_entry(entry)
    markdowner = Markdown() 
    if entry_contents is None:
        return render (request, "encyclopedia/wiki/errorpage.html")
    else:

        return render(request, "encyclopedia/wiki/entry.html",{
        "entries": markdowner.convert(entry_contents),
        "entry_exists": entry_contents is not None,
        "title": entry if entry_contents is not None else "Error"
    })


def createpage(request):
    if request.method == "POST":
        form = NewForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            util.save_entry(title,content)
            return HttpResponseRedirect(reverse("index"))
        else:

            return render(request, "encyclopedia/createpage.html",{
                "form": form

             })
    return render(request, "encyclopedia/createpage.html", {
        "form": NewForm()
    })

def random_page(request):
    entry_title = random.choice(util.list_entries())
    return HttpResponseRedirect(reverse("entry", args=(entry_title,)))

def edit_page(request, entry):
    entry_contents = util.get_entry(entry)
    if entry_contents is None:
        return HttpResponseRedirect(reverse("index"))

    return render(request, "encyclopedia/createpage.html", {
        'edit_mode': True,
        'edit_page_title': entry,
        'edit_page_contents': entry_contents
    })

def search(request):
    query = request.GET['q']
    if util.get_entry(query):
        
        return HttpResponseRedirect(reverse("entry", args=(query,)))
    else:
        
        return render(request, "encyclopedia/index.html", {
            "entries": [entry for entry in util.list_entries() if query.lower() in entry.lower()],
            "title": f'"{query}" search results',
            "heading": f'Search Results for "{query}"'
        })

def save_page(request, entry=None):
    if request.method == 'GET':
        return HttpResponseRedirect(reverse("index"))
    else:
        assert (request.method == 'POST')
        entry_content = request.POST['entry-content']
        if not entry:
            
            entry = request.POST['title']
            if entry.lower() in [entry.lower() for entry in util.list_entries()]:
                return render(request, "encyclopedia/error.html", {
                    "error_title": "saving page",
                    "error_message": "An entry with that title already exists! Please change the title and try again."
                })

        filename = wiki_entries_directory + entry + ".md"
        with open(filename, "w") as f:
            f.write(entry_content)
        return HttpResponseRedirect(reverse("entry", args=(entry,)))


