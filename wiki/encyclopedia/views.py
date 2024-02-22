from django.shortcuts import render,HttpResponseRedirect
from markdown2 import Markdown
from . import util
from django import forms
import random

class Add_Page_Form(forms.Form):
    title= forms.CharField(max_length=100,widget=forms.TextInput(attrs={'placeholder':'Title'}))
    content = forms.CharField(widget=forms.TextInput(attrs={'rows':30,'cols':30}))
    


def convert_md_to_html(title):
    content = util.get_entry(title)
    markdown = Markdown()
    if content is None:
        return None
    else:
        return markdown.convert(content)

def convert_form_to_md(title,content):
    util.save_entry(title,content)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    md = convert_md_to_html(title)  # Pass the title argument
    if md is None:
        return render(request, "encyclopedia/error.html",
                    {
                        'status':404,
                        'message':'The requested page was not found.'
                    }) 
    else:
        return render(request, "encyclopedia/entry.html",
                    {
                        'markdown': md,
                        'title':title
                    })
    
def search(request):
    if request.method == "POST":
        entry_search = request.POST['q']
        # ... rest of your search logic
        md = convert_md_to_html(entry_search)  # Pass the title argument
    if md is not None:
        return render(request, "encyclopedia/entry.html",
                    {
                        'markdown': md,
                        'title':entry_search
                    })
        
    else:
        return render(request, "encyclopedia/error.html",
                    {
                        'status':404,
                        'message':'The requested page was not found.'
                    }) 
    
def add_page(request):
    if request.method == 'POST':
        form = Add_Page_Form(request.POST)
        if form.is_valid():
            new_title = form.cleaned_data['title']
            new_content = form.cleaned_data['content']
            
            try:
                convert_form_to_md(new_title, new_content)   # Save to markdown file
                return render(request, "encyclopedia/index.html", {
                    "entries": util.list_entries()})
            except Exception as e:
                return render(request, "encyclopedia/error.html", {
                    'status': 404,
                    'message': 'Error saving page: ' + str(e)})
    else:
        return render(request, "encyclopedia/add_page.html", {'form':Add_Page_Form()})
    
def randomPage(request):
    entries = util.list_entries()
    rand_page = random.choice(entries)
    md = convert_md_to_html(rand_page)
    return render(request, "encyclopedia/entry.html",
                    {
                        'markdown': md,
                        'title':rand_page
                    })

def edit_page(request):
    return