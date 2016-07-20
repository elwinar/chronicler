schema = {
        "$schema": "http://json-schema.org/draft-04/schema#",
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string"
                    },
                "faction": {
                    "type": "string"
                    },
                "caster": {
                    "type": "string"
                    },
                "list": {
                    "type": "string"
                    },
                "against": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "player": {
                                "type": "string"
                                },
                            "date": {
                                "type": "string"
                                },
                            "faction": {
                                "type": "string"
                                },
                            "caster": {
                                "type": "string"
                                },
                            "list": {
                                "type": "string"
                                },
                            "result": {
                                "type": "object",
                                "properties": {
                                    "victory": {
                                        "type": "boolean"
                                        },
                                    "type": {
                                        "type": "string"
                                        }
                                    },
                                "required": [
                                    "victory",
                                    "type"
                                    ]
                                },
                            "thoughs": {
                                "type": "string"
                                }
                            },
                        "required": [
                            "player",
                            "date",
                            "faction",
                            "caster",
                            "list",
                            "result",
                            "thoughs"
                            ]
                        }
                    }
                },
    "required": [
            "name",
            "faction",
            "caster",
            "list",
            "against"
            ]
    }
}
