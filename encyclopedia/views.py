from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django import forms
from markdown2 import markdown

from . import util

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
    })

def renderSubPage(request,title):
    if util.get_entry(title):
        content=markdown(util.get_entry(title))
        return render(request,"encyclopedia/subPage.html",{
            "title":title.capitalize(),
            "body":content,
            "error_msg":None
        })
    else:
        content=None
    return render(request,"encyclopedia/result.html",{
        "query":title,
        "error_msg":"Requested Page Not Found."
    })

def search(request):
    query=request.GET.get('q').lower()
    entries=util.list_entries()
    matched_entries=[]
    for entry in entries:
        entry=entry.lower()
        if query == entry:
            content=markdown(util.get_entry(query))
            return render(request,"encyclopedia/subPage.html",{
                "title":query,
                "body":content
            })
        if query in entry:
            matched_entries.append(entry)
    return render(request,"encyclopedia/result.html",{
        "query":query,
        "match_list":matched_entries,
        "error_msg":"Requested Page Not Found."
    })

class newEntry(forms.Form):
    title=forms.CharField(label="Title",max_length=50,
    widget=forms.TextInput(attrs={'class':'form-control col-md-10 col-lg-10'}))
    content=forms.CharField(widget=forms.Textarea(attrs={
        'class':'form-control col-md-10 col-lg-10'
    }))

def create(request):
    if request.method == 'POST':
        Form=request.POST
        form=newEntry(Form)
        if form.is_valid():
            title=form.cleaned_data["title"]
            content=form.cleaned_data["content"]
            entries=util.list_entries()
            if title not in entries:
                util.save_entry(title,content) 
                return HttpResponseRedirect(reverse('subPage',args=[title]))
            else:
                return render(request,'encyclopedia/subPage.html',{
                    'title':"Can't create an entry",
                    'error_msg':"File already exists.",
                })
    else:
        return render(request,'encyclopedia/create.html',{
            'form':newEntry()
        })

class editExistEntry(forms.Form):
    content=forms.CharField(widget=forms.Textarea(attrs={
        'class':'form-control col-md-10 col-lg-10'
    }))

def edit(request,title):
    if request.method=="POST":
        form=editExistEntry(request.POST)
        if form.is_valid():
            content=form.cleaned_data["content"]
            util.save_entry(title,content)
            fp=util.get_entry(title)
            html=markdown(fp)
            return render(request,'encyclopedia/subPage.html',{
                "title":title,
                "body":html,
            })
    else:
        body=util.get_entry(title)
        return render(request,'encyclopedia/edit.html',{
            'title':title,
            'form':editExistEntry(initial={'content':body})
        })

import random 

def randomEntry(request):
    chosen=random.sample(util.list_entries(),1)
    html=markdown(util.get_entry(chosen[0]))
    return render(request,'encyclopedia/subPage.html',{
        'title':chosen,
        'body':html,
    })
