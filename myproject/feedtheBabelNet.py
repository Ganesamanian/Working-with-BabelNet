#!/usr/bin/env python
# coding: utf-8

# # BabelNet querying in Python via HTTP API

# In[1]:

# Headers
import urllib.request
import time
import json
import gzip
from PIL import Image
from itertools import chain

# from IPython.display import SVG, display
from matplotlib import pyplot as plt
from io import StringIO, BytesIO
import myapp
from myapp.models import *
from neomodel import db
from neomodel import (StructuredNode, StructuredRel, StringProperty, IntegerProperty,
    UniqueIdProperty, RelationshipTo, RelationshipFrom)


# In[2]:


# Retrieve the IDs of the Babel synsets
# FUntion to return the Babelnet ID for the
# Word of interest

def synset(word):
    service_url = 'https://babelnet.io/v6/getSynsetIds'

    lemma = word
    lang = 'EN'
    # Use your account key
    key  = '4d425ff2-1193-4714-abf1-70e2b21ee9f3'
    
    ids = []
    
    params = {
        'lemma' : lemma,
        'searchLang' : lang,
        'key'  : key
    }
    
    url = service_url + '?' + urllib.parse.urlencode(params)
    request = urllib.request.Request(url)
    request.add_header('Accept-encoding', 'gzip')
    response = urllib.request.urlopen(request)
    
    if response.info().get('Content-Encoding') == 'gzip':
        buf = BytesIO( response.read())
        f = gzip.GzipFile(fileobj=buf)
        data = json.loads(f.read())
        for result in data:
            ids.append(result['id'])
    return ids

# Retrieve the information of a given synset
# Using retrieved ID of the word,
# Extract information related to it
def synset_information(synsetid):

    service_url = 'https://babelnet.io/v6/getSynset'

    id = synsetid
    key  = '4d425ff2-1193-4714-abf1-70e2b21ee9f3'
    
    lemmas = []
    glos = []
    urls = []
    captions = []
    pos_ = []
    sources = []
    languages = []
    glos_source = []

    params = {
        'id' : id,
        'key'  : key
    }

    url = service_url + '?' + urllib.parse.urlencode(params)
    request = urllib.request.Request(url)
    request.add_header('Accept-encoding', 'gzip')
    response = urllib.request.urlopen(request)

    if response.info().get('Content-Encoding') == 'gzip':
        buf = BytesIO( response.read())
        f = gzip.GzipFile(fileobj=buf)
        data = json.loads(f.read())

        # retrieving BabelSense data
        senses = data['senses']
        for result in senses:
            id_ = result.get('properties')['synsetID']['id']    
            lemma = result.get('properties')['lemma']['lemma']
            source = result.get('properties')['source']
            pos = result.get('properties')['synsetID']['pos']
            language = result.get('properties')['language']
            
            lemmas.append(lemma)
            pos_.append(pos)
            sources.append(source)
            languages.append(language)        

        # retrieving BabelGloss data
        glosses = data['glosses']
        for result in glosses:
            gloss = result.get('gloss')
            gloss_source = result.get('source')
            glos.append(gloss)
            glos_source.append(gloss_source)

        # retrieving BabelImage data
        images = data['images']    
        for result in images:
            url = result.get('url')
            language = result.get('language')
            name = result.get('name') 
            captions.append(name)
            urls.append(url)

    return {
        
            'lemma' : lemmas,
            'gloss' : glos,
            'gloss_source' : list(set(glos_source)),
            'url' : urls,
            'caption' : captions,
            'images' : zip(urls, captions),
            'pos' : list(set(pos_)), 
            'source' : list(set(sources)),
            'language' : list(set(languages)),
        }

# Retrieve edges of a given BabelNet synset
# Extract relations and target words

def edges(synsetid):
    service_url = 'https://babelnet.io/v6/getOutgoingEdges'

    # id = synsetid
    key  = '4d425ff2-1193-4714-abf1-70e2b21ee9f3'
    targets = []
    relations = []

    params = {
        'id' : synsetid,
        'key'  : key
    }

    url = service_url + '?' + urllib.parse.urlencode(params)
    print(url)
    request = urllib.request.Request(url)
    request.add_header('Accept-encoding', 'gzip')
    response = urllib.request.urlopen(request)

    if response.info().get('Content-Encoding') == 'gzip':
        buf = BytesIO( response.read())
        f = gzip.GzipFile(fileobj=buf)
        data = json.loads(f.read())

        # retrieving Edges data
        for result in data:
            target = result.get('target')
            language = result.get('language')

            # retrieving BabelPointer data
            pointer = result['pointer']
            relation = pointer.get('name')
            group = pointer.get('relationGroup')
            targets.append(target)
            relations.append(relation)
    
    return{
        'target': targets,
        'relation': relations
            
    }


# In[3]:

# Function to have variable relations 
def relationship_type(name1, name2, relation):
    print("MATCH (n:Babelnet), (m:Babelnet) where n.babelnet_name=\"" + str(name1) + \
                      "\" and m.babelnet_name=\"" + str(name2) +"\" create (n)-[:"+ str(relation).replace(" ", "_")+"]->(m)")

    db.cypher_query("MATCH (n:Babelnet), (m:Babelnet) where n.babelnet_name=\"" + str(name1) + \
                      "\" and m.babelnet_name=\"" + str(name2) +"\" create (n)-[:"+ str(relation).replace(" ", "_")+"]->(m)")

    return


if __name__ == '__main__':

    id_list = []
    synsetid_list = []
    
    # Establish the connection with Neo4j
    db.set_connection('bolt://neo4j:babelnet@localhost:3687')
    # Delete all the existing nodes
    db.cypher_query("MATCH (n) DETACH Delete n")

    synsetids = synset("passive safety")
    syssetinfo = synset_information(synsetids[1])
    print("Lemma associated with ", synsetids[1])
    print("\n")
    lemma = [lemma for lemma in syssetinfo['lemma']]     
    root_node = Babelnet(babelnet_id= synsetids[1],
                         babelnet_name=lemma[0], 
                         babelnet_lemma=lemma[:-2],
                         babelnet_pos = syssetinfo['pos'],
                         babelnet_language = syssetinfo['language'],
                         babelnet_source= syssetinfo['source'],
                         babelnet_gloss= syssetinfo['gloss'],
                         babelnet_gloss_source = syssetinfo['gloss_source'],
                         babelnet_images = [img for img in syssetinfo['images']]).save()

    synsetid_list.append(synsetids[1])
    

# In[4]:

    # Getting relations of for single lemma
    edgeinfo = edges(synsetids[1])
    print("Edges information")
    for count in range(len(edgeinfo['target'])):

        try:

            syssetinfo = synset_information(edgeinfo['target'][count])

            if edgeinfo['target'][count] not in synsetid_list:

                synsetid_list.append(edgeinfo['target'][count])
                next_node = Babelnet(babelnet_id =  edgeinfo['target'][count],
                                     babelnet_name= syssetinfo['lemma'][0],
                                     babelnet_lemma= syssetinfo['lemma'],
                                     babelnet_pos = syssetinfo['pos'],
                                     babelnet_language = syssetinfo['language'],
                                     babelnet_source= syssetinfo['source'],
                                     babelnet_gloss= syssetinfo['gloss'],
                                     babelnet_gloss_source = syssetinfo['gloss_source'],
                                     babelnet_images = [img for img in syssetinfo['images']]).save()

            
            relationship_type(root_node.babelnet_name, next_node.babelnet_name, edgeinfo['relation'][count])
            

        except:
            pass

    

    # query all the nodes
    query = db.cypher_query("MATCH (a:Babelnet) RETURN a.babelnet_id, a.babelnet_name")[0]     
    node_list = [q for q in query if q[1] != "Automotive_safety"]
    ids = [i[0] for i in node_list]

    for count, i_d in enumerate(ids):
        edgeinfo = edges(i_d)
        for idx, target in enumerate(edgeinfo['target']):
            if target in ids:
                index = ids.index(target)

                # Get all the nodes in database at present
                all_nodes = Page.nodes.all()

                # Getting the root node
                source = Babelnet.nodes.get(babelnet_id=ids[count])
                dest = Babelnet.nodes.get(babelnet_id=target)

                query1 = db.cypher_query("Match (a:Babelnet{babelnet_name : \"" + str(source.babelnet_name) + \
                                        "\"})-[r]->(b:Babelnet{babelnet_name : \"" + str(dest.babelnet_name) + \
                                        "\"}) return type(r)")[0]

                query2 = db.cypher_query("Match (a:Babelnet{babelnet_name : \"" + str(dest.babelnet_name) + \
                                        "\"})-[r]->(b:Babelnet{babelnet_name : \"" + str(source.babelnet_name) + \
                                        "\"}) return type(r)")[0]


                if query1 == [] and query2 == []:
                    if source != dest:
                        edgeinfo['relation'][idx] = edgeinfo['relation'][idx].replace("(", "")
                        edgeinfo['relation'][idx] = edgeinfo['relation'][idx].replace(")", "")
                        edgeinfo['relation'][idx] = edgeinfo['relation'][idx].replace(",", "")

                        relationship_type(source.babelnet_name, dest.babelnet_name, edgeinfo['relation'][idx])

    

                

         

      



