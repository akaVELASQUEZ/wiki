from logging import PlaceHolder
from django.shortcuts import render, HttpResponse
import markdown2
from . import util
from django import forms
from random import randint


class NewEntryForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={
        "name":"title", "PlaceHolder":"Title", "class":"title col-lg-9"
        }), label="")
    content = forms.CharField(widget=forms.Textarea(attrs={
        "name":"content", "PlaceHolder":"Markdown",  "class":"content col-lg-9"
        }),label="")

class EditEntryForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={
        "name":"title", "PlaceHolder":"Title", "class":"title col-lg-9"
        }), label="")
    content = forms.CharField(widget=forms.Textarea(attrs={
        "name":"content", "PlaceHolder":"Markdown",  "class":"content col-lg-9"
        }),label="")


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def wiki(request, title):
    if title in util.list_entries():
        return render(request, "encyclopedia/wiki.html", {
            "content": markdown2.markdown(util.get_entry(title)), "title": title
        })
    else:
        return render(request, "encyclopedia/error.html", {
            "title": title
        })

def new(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            return render(request, "encyclopedia/index.html", {
                "entries": util.list_entries()
            })

    else:
        return render(request, "encyclopedia/new.html", {
            "form": NewEntryForm()
    })

def random(request):
    entries = util.list_entries()
    index = randint(0,len(entries)-1)
    title = entries[index]
    return render(request, "encyclopedia/wiki.html", {
        "content": markdown2.markdown(util.get_entry(title)), "title": title
    })

def search(request):
    substring = []
    search = request.GET.get("q")
    entries = util.list_entries()
    for entry in entries:
        if search.lower() == entry.lower():
            return render(request, "encyclopedia/wiki.html", {
                "content": markdown2.markdown(util.get_entry(entry)), "title": entry
            })
        elif search.lower() in entry.lower():
            substring.append(entry)
        
    if len(substring) == 0:
        HttpResponse("No match")

    else:
        return render(request, "encyclopedia/search.html", {
            "entries": substring
        })

def edit(request, title):

    if request.method == "POST":
        edit = EditEntryForm(request.POST)
        if edit.is_valid():
            title = edit.cleaned_data["title"]
            content = edit.cleaned_data["content"]
            util.save_entry(title, content)
            return render(request, "encyclopedia/index.html", {
                "entries": util.list_entries()
            })
    else:
        edit = EditEntryForm(initial={"title" : title, "content" : util.get_entry(title)})
        return render(request, "encyclopedia/edit.html", {
            "form": edit, "title":title
        })