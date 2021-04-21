from random import choice
from markdown2 import markdown
from django.http.response import HttpResponseNotFound
from django.shortcuts import redirect, render
from django.urls import reverse

from . import util
from . import forms


def index(request):
    if title := request.GET.get('q', ''):
        entry = util.get_entry(title)
        if entry:
            return render(request, "encyclopedia/entry.html", {
                "entry": entry
            })

        entries = util.list_entries()
        matches = [match for match in entries if match.startswith(title)]

        return render(request, "encyclopedia/index.html", {
            "entries": matches
        })

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, title: str):
    entry = util.get_entry(title)
    if not entry:
        return HttpResponseNotFound("Couldn't find an entry with this name")

    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "entry": markdown(entry),
    })


def new_page(request):
    if request.method == "POST":
        entry_form = forms.NewEntryFrom(request.POST)
        if entry_form.is_valid():
            title = entry_form.cleaned_data["title"]
            body = entry_form.cleaned_data["body"]
            util.save_entry(title, body)
            return redirect(reverse("entry", kwargs={"title": title}))
    else:
        entry_form = forms.NewEntryFrom()
    return render(request, "encyclopedia/edit_form.html", {
        "entry_form": entry_form,
        "url": reverse("new_page"),
    })


def edit_page(request, title):
    if request.method == "POST":
        entry_form = forms.EditEntryFrom(request.POST)
        if entry_form.is_valid():
            title = entry_form.cleaned_data["title"]
            body = entry_form.cleaned_data["body"]
            util.save_entry(title, body)
            return redirect(reverse("entry", kwargs={"title": title}))
    else:
        entry = util.get_entry(title)
        entry_form = forms.EditEntryFrom({"title": title, "body":entry})
    return render(request, "encyclopedia/edit_form.html", {
        "entry_form": entry_form,
        "url": reverse("edit_page", kwargs={"title": title}),
    })


def random(request):
    entry_title = choice(util.list_entries())
    return redirect(reverse("entry", kwargs={"title": entry_title}))