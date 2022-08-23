from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from myapp.models import *
from neomodel import db
from itertools import chain


def home(request):
    # return HttpResponse('<h1> Myapp Home </h1>')
    return render(request, 'myapp/home.html')
    
def about(request):
    # return HttpResponse('<h1> Myapp About </h1>')
    return render(request, 'myapp/about.html')

# Create your views here.

# class tableview(generic.ListView):
#     template_name = 'myapp/home.html'
#     context_object_name = 'run_list'

#     def get_queryset(self):

#         all_nodes = Page.nodes.all()
#         query_page = list(chain.from_iterable(db.cypher_query("MATCH (n:Page) RETURN n.page_uid")[0]))
#         query_resultpage = list(chain.from_iterable(db.cypher_query("MATCH (n:Resultpage) RETURN n.resultpage_uid")[0]))
#         uid = query_page + query_resultpage
        
#         url_list = []
#         name_list = []
#         image_list = []
#         image_list2 = []

#         # for uid1 in query_page:
#         #     url_list.append(Page.nodes.get(page_uid = uid1).page_url)
#         #     name_list.append(Page.nodes.get(page_uid = uid1).page_name)


#         for uid2 in query_resultpage:
#             url_list.append(Resultpage.nodes.get(resultpage_uid = uid2).resultpage_url)
#             name_list.append(Resultpage.nodes.get(resultpage_uid = uid2).resultpage_name)
#             image_list.append(Resultpage.nodes.get(resultpage_uid = uid2).resultpage_test_image_url)

#         for image in image_list:
#             strings_ = image.replace("[", "")
#             strings_ = strings_.replace("]", "")
#             strings_ = strings_.replace("\'", "")

#             letter_list = strings_.split(",")        
#             image_list2.append(letter_list)

#         run_list=zip(name_list, url_list, image_list2)
        
#         return run_list



class tableview(generic.ListView):
    template_name = 'myapp/home.html'
    context_object_name = 'run_list'

    def get_queryset(self):

        all_nodes = Page.nodes.all()
        query_page = list(chain.from_iterable(db.cypher_query("MATCH (n:Page) RETURN n.page_uid")[0]))
        query_resultpage = list(chain.from_iterable(db.cypher_query("MATCH (n:Resultpage) RETURN n.resultpage_uid")[0]))
        uid = query_page + query_resultpage
        
        url_list = []
        name_list = []
        image_list_t = []
        image_list_ao = []
        image_list_pd = []
        image_list_sf = []
        image_list = []



        # for uid1 in query_page:
        #     url_list.append(Page.nodes.get(page_uid = uid1).page_url)
        #     name_list.append(Page.nodes.get(page_uid = uid1).page_name)


        for uid2 in query_resultpage:
            url_list.append(Resultpage.nodes.get(resultpage_uid = uid2).resultpage_url)
            name_list.append(Resultpage.nodes.get(resultpage_uid = uid2).resultpage_name)
            image_list_t.append(Resultpage.nodes.get(resultpage_uid = uid2).resultpage_test_image_url)
            image_list_pd.append(Resultpage.nodes.get(resultpage_uid = uid2).resultpage_pedestrain_image_url)
            image_list_ao.append(Resultpage.nodes.get(resultpage_uid = uid2).resultpage_adultoccupant_image_url)
            image_list_sf.append(Resultpage.nodes.get(resultpage_uid = uid2).resultpage_safety_image_url)

        for count in range(len(image_list_t)):
            image = image_list_t[count]+image_list_pd[count]+image_list_ao[count]+image_list_sf[count]   
            strings_ = image.replace("[", "")
            strings_ = strings_.replace("]", "")
            strings_ = strings_.replace("\'", "")
            letter_list = strings_.split(",")        
            image_list.append(letter_list)

        run_list=zip(name_list, url_list, image_list)
        
        return run_list