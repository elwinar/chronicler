schema = {
  "$schema": "http://json-schema.org/draft-04/schema#",
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "player": {
        "type": "object",
        "properties": {
          "faction": {
            "type": "string"
          },
          "caster": {
            "type": "string"
          }
        },
        "required": [
          "faction",
          "caster"
        ]
      },
      "opponent": {
        "type": "object",
        "properties": {
          "player": {
            "type": "string"
          },
          "faction": {
            "type": "string"
          },
          "caster": {
            "type": "string"
          }
        },
        "required": [
          "player",
          "faction",
          "caster"
        ]
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
      }
    },
    "required": [
      "player",
      "opponent",
      "result"
    ]
  }
}
