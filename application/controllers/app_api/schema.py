allowed_choices = ['ms', 'integer', 'float']

add_tracker_schema = {
    "type": "object",
    "properties": {
        "name": { 
            "type": "string",
            "minLength": 5,
            "maxLength": 55
            },
        "description": {
            "type": "string",
            "maxLength": 255
            },
        "settings": {
            "type": "array", 
            "items": {
                "type": "string",
                "maxLength": 255
                }
            },
        "type": {"type":"string"},
        "choices": {
            "type": ["array", "null"],
            "items": {
                "type": "string",
                "maxLength": 255
                }
            }
    },
    "required": ["name", "settings", "type"]
    }

patch_tracker_schema = {
    "type": "object",
    "properties": {
        "name": { 
            "type": "string",
            "minLength": 5,
            "maxLength": 55
            },
        "description": {
            "type": "string",
            "maxLength": 255
            },
        "settings": {
            "type": "array", 
            "items": {
                "type": "string",
                "maxLength": 255
                }
            },
        "type": {"type":"string"},
        "delete_choices": {"type": "boolean"},
        "choices": {
            "type": ["array", "null"],
            "items": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": ["integer", "null"]
                        },
                    "new_name": {
                        "type": ["string", "null"],
                        "maxLength": 255
                        }
                    },
                "required": ["new_name"]
                }
            }
    }
    }

add_logs_schema = {
    "type": "object",
    "properties": {
        "timestamp": { 
            "type": "string"
            },
        "note": {
            "type": "string",
            "maxLength": 255
            },
        "value": {
            "type": ["array", "number"], 
            "items": {
                "type": "integer"
                }
            }        
    },
    "required": ["value"]
    }

patch_logs_schema = {
    "type": "object",
    "properties": {
        "timestamp": { 
            "type": "string"
            },
        "note": {
            "type": "string",
            "maxLength": 255
            },
        "value": {
            "type": ["array", "number"], 
            "items": {
                "type": "integer"
                }
            }        
    }
    }



# based on date we get from JavaScript, DO NOT CHANGE
date_format = '%m/%d/%Y, %I:%M:%S %p'