# from django.db import models

#$$$$$$$$$$$$$$$$$$$$$$$$$$$Reference$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

# # Create your models here.
#from neomodel import (StructuredNode, StringProperty,
# IntegerProperty,UniqueIdProperty, RelationshipTo)

# # Create your models here.


#class City(StructuredNode):
#     code = StringProperty(unique_index=True, required=True)
#     name = StringProperty(index=True, default="city")

#class Person(StructuredNode):
#     uid = UniqueIdProperty()
#     name = StringProperty(unique_index=True)
#     age = IntegerProperty(index=True, default=0)

#     # Relations :
#     city = RelationshipTo(City, 'LIVES_IN')
#     friends = RelationshipTo('Person','FRIEND')

#$$$$$$$$$$$$$$$$$$$$$$$$$$$Reference$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

#!/usr/bin/env python
# coding: utf-8


# BabelNet querying classes
class FriendRel(StructuredRel):
    
    relation_group = StringProperty()



class Babelnet(StructuredNode):
    
    """
    This class specifies node properties and relation

    Inputs:
        page_uid: unique identification for node
        page_name: name of the node
        page_url: url of the node
        relation: connection between the node

    Returns:
        None

    Output:
        Creation of node in Neo4j
    """



    babelnet_uid = UniqueIdProperty()
    babelnet_id = StringProperty(unique_index=True)
    babelnet_name = StringProperty(unique_index=True)
    babelnet_lemma = StringProperty(unique_index=True, default= " ")
    babelnet_pos = StringProperty(unique_index=True, default= " ")
    babelnet_language = StringProperty(unique_index=True, default= " ")
    babelnet_source = StringProperty(unique_index=True, default= " ")
    babelnet_gloss = StringProperty(unique_index=True, default= " ")
    babelnet_gloss_source = StringProperty(unique_index=True, default= " ")
    babelnet_images = StringProperty(unique_index=True, default= " ")

    



    #Relations
    # relation = RelationshipTo('Babelnet', 'LINKED_TO', model=FriendRel)
    


