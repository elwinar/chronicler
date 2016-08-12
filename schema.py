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
          },
          "list": {
            "type": "string"
          }
        },
        "required": [
          "faction",
          "caster",
          "list"
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
          },
          "list": {
            "type": "string"
          }
        },
        "required": [
          "player",
          "faction",
          "caster",
          "list"
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
      },
      "thoughs": {
        "type": "string"
      }
    },
    "required": [
      "player",
      "opponent",
      "result",
      "thoughs"
    ]
  }
}
