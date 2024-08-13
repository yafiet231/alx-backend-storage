#!/usr/bin/env python3
'''Task 10's module.
'''

def update_topics(mongo_collection, name, topics):
    """
    Update the topics of a school document based on the school name.

    Parameters:
    mongo_collection (pymongo.collection.Collection): The pymongo collection object.
    name (str): The school name to update.
    topics (list of str): The list of topics approached in the school.
    """
    mongo_collection.update_many(
        {"name": name},
        {"$set": {"topics": topics}}
    )
