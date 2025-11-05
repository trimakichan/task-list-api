from flask import abort, make_response
from ..db import db


def validate_model(cls,model_id):
    try:
        model_id = int(model_id)
    except ValueError:
        invalid = {"message": f"{cls.__name__} ({model_id}) is invalid."}
        abort(make_response(invalid, 400))
    
    query = db.select(cls).where(cls.id == model_id)
    model = db.session.scalar(query)

    if not model:
        not_found = {"message" : f"{cls.__name__} ({model_id}) is not found."}  
        abort(make_response(not_found, 404))

    return model

def create_model(cls, model_data):
    try:
        new_model =cls.from_dict(model_data)
    except KeyError as error:
        invalid_msg = {"details": "Invalid data"}
        abort(make_response(invalid_msg, 400))
    
    db.session.add(new_model)
    db.session.commit()

    return new_model.to_dict(), 201

# finish this later
def get_models_with_filters(cls, filters=None):
    query = db.select(cls)

    if filters:
        for attribute, value in filters.items():
            if attribute == "sort":
                query = apply_sort_to_query(cls, query, value)
            elif hasattr(cls, attribute):
                # other logics
                pass     

    models = db.session.scalars(query)
    models_response = [model.to_dict() for model in models]
    return models_response

def apply_sort_to_query(cls, query, sort_type):
    valid_sort = {
        "asc": cls.title,
        "desc": cls.title.desc()
    }
    sort_type = sort_type.casefold().strip()
    if sort_type not in valid_sort:
        invalid_msg = {"message": "Invalid sort value. Valid options: asc, desc."}
        abort(make_response(invalid_msg, 400))

    return query.order_by(valid_sort[sort_type])

