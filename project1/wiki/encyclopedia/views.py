from django.shortcuts import render

from . import util

from django import forms
import markdown
import random

# remove after, for testing
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

#index page
def index(request):

    #load all entries
    if request.method == "GET":
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries()
        })

    #if search used
    else:
        searchRequest = request.POST.get("q")

        #if match found, load page for that entry
        for entry in util.list_entries():
            if searchRequest.lower() == entry.lower():
                return render(request, "encyclopedia/entry.html", {
                "content": markdown.markdown(util.get_entry(searchRequest)),
                "entryName": searchRequest.capitalize()
            })

        #if match not found, display a page with possible matches
        else:
            subentryList = []
            for entry in util.list_entries():
                if searchRequest.lower() in entry.lower():
                    subentryList.append(entry)

            subentryList.sort()

            return render(request, "encyclopedia/index.html", {
                "entries": subentryList
            })

#if page access attempted through search bar / eg. /http
def entryName(request, entryName):

    #convert all page names to lowercase
    lowercaseList = []
    for entries in util.list_entries():
        lowercaseList.append(entries.lower())

    #check if new name exists, if not found display not found and possible entries
    if entryName.lower() not in lowercaseList:
        return render(request, "encyclopedia/notfound.html", {
            "entries": util.list_entries()
        })

    #if found, pull page for that entry
    else:
        return render(request, "encyclopedia/entry.html", {
            "content": markdown.markdown(util.get_entry(entryName)),
            "entryName": entryName.capitalize()
        })

#create form for new page
class newContent(forms.Form):
    title = forms.CharField(label="New Title")
    content = forms.CharField(widget=forms.Textarea, label="New Content")

#load new GET for new Page with form for user to fill in
def newPage(request):
    if request.method == "GET":
        return render(request, "encyclopedia/newpage.html", {
            "newPage": newContent()
        })

    #If user submits form
    else:
        form = newContent(request.POST)

        #Check server side that form is valid, decompose data into smaller pieces
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]

            #convert all page names to lowercase
            lowercaseList = []
            for entries in util.list_entries():
                lowercaseList.append(entries.lower())

            #render error if title is already taken
            if title.lower() in lowercaseList:
                return render(request, "encyclopedia/pageexists.html")

            #redirect to new wiki if save is successful
            else:
                util.save_entry(title.capitalize(), content)
                return HttpResponseRedirect(reverse("encyclopedia:entryName", kwargs = {'entryName' : title}))

#create form to edit existing wiki
class editContent(forms.Form):
    content = forms.CharField(widget=forms.Textarea, label="New Content")
    title = forms.CharField(widget=forms.HiddenInput())

def editWiki(request):
    #if navigating to editwiki page from previous page
    if request.method == "GET":
        #get content and title
        content = util.get_entry(request.GET.get("title"))
        title = request.GET.get("title")
        for entries in util.list_entries():
            if title.lower() == entries.lower():
                title = entries

        #display editor for content and title
        return render(request, "encyclopedia/editwiki.html", {
            "newContent": editContent(initial={"content": content, "title": title}),
            "content": content,
            "title": title
        })

    #if user saves new change
    else:
        title = request.POST.get("title")
        content = request.POST.get("content")
        util.save_entry(title.capitalize(), content)
        return HttpResponseRedirect(reverse("encyclopedia:entryName", kwargs = {'entryName' : title}))

#select random page from list of entries
def randomPage(request):
    wikis = util.list_entries()
    randomSelect = random.choice(wikis)
    return HttpResponseRedirect(reverse("encyclopedia:entryName", kwargs = {'entryName' : randomSelect}))