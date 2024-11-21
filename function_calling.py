# chat gpt function calling for every actions

"""
1- table lamp
2- reminder
3- set_alarm - zaman tarih
4- room_lamp
"""

costum_function = [
    {
        "name": "update_tableLamp_status",
        "description": "Masa lambasının durumunu değiştirir.",
        "parameters": {
            "type": "object",
            "properties": {
                "device_name": {
                    "type": "string",
                    "description": "Masa Lambası."
                },
                "status": {
                    "type": "boolean",
                    "description": "Masa Lambasının yeni durumu (true: açık, false: kapalı)."
                },
                "confirm_msg": {
                    "type": "string",
                    "description": "Kullanıcıya gönderilecek onay mesajı."
                }
            },
            "required": ["device_name", "status"]
        }
    },
    {
        "name": "control_head_movement",
        "description": "Control your head movement up or down.",
        "parameters": {
            "type": "object",
            "properties": {
                "status": {
                    "type": "string",
                    "enum": ["up", "down"],
                    "description": "The direction of your head movement"
                },
                "confirm_msg": {
                    "type": "string",
                    "description": "Kullanıcıya gönderilecek onay mesajı"
                }
            },
            "required": ["status", "confirm_msg"]
        }
    },
    {
        "name": "update_roomLamp_status",
        "description": "Oda lambasının durumunu değiştirir.",
        "parameters": {
            "type": "object",
            "properties": {
                "device_name": {
                    "type": "string",
                    "description": "Oda Lambası."
                },
                "status": {
                    "type": "boolean",
                    "description": "Oda Lambasının yeni durumu (true: açık, false: kapalı)."
                },
                "confirm_msg": {
                    "type": "string",
                    "description": "Kullanıcıya gönderilecek onay mesajı."
                }
            },
            "required": ["device_name", "status"]
        }
    },
    {
        "name": "set_alarm",
        "description": "Kullanıcının belirlediği zaman ve tarihte alarmı ayarlar.",
        "parameters": {
            "type": "object",
            "properties": {
                "alarm_time": {
                    "type": "string",
                    "description": "Alarmın çalacağı zaman. ISO 8601 formatında bir tarih ve saat, örneğin: '2024-08-20T14:00:00Z'.",
                    "format": "date-time"
                },
                "confirm_msg": {
                    "type": "string",
                    "description": "Kullanıcıya gönderilecek onay mesajı."
                }
            },
            "required": ["alarm_time"]
        }
    },
    {
        "name": "set_reminder",
        "description": "Kullanıcının belirlediği zamanı ve konuyu hatırlatıcıya ekler.",
        "parameters": {
            "type": "object",
            "properties": {
                "reminder_text": {
                    "type": "string",
                    "description": "Hatırlatılacak konu veya eylem, örneğin: 'Toplantıyı unutma' veya 'Eczaneye git.'"
                },
                "reminder_time": {
                    "type": "string",
                    "description": "Hatırlatıcıyı tetikleyecek zaman. ISO 8601 formatında bir tarih ve saat, örneğin: '2024-08-20T14:00:00Z'.",
                    "format": "date-time"
                },
                "confirm_msg": {
                    "type": "string",
                    "description": "Kullanıcıya gönderilecek onay mesajı."
                }
            },
            "required": ["reminder_text", "reminder_time"],
        }
    },
    {
        "name": "control_movement",
        "description": "Control your movement, go left, right, forward or backward. Send true just one of them if you use it.",
        "parameters": {
            "type": "object",
            "properties": {
                "turn_left": {
                    "type": "boolean",
                    "description": "Turn your body to left."
                },
                "turn_right": {
                    "type": "boolean",
                    "description": "Turn your body to right.",
                },
                "forward": {
                    "type": "boolean",
                    "description": "Go forward."
                },
                "backward": {
                    "type": "boolean",
                    "description": "Go backward."
                },
                "confirm_msg": {
                    "type": "string",
                    "description": "Kullanıcıya gönderilecek onay mesajı."
                }
            },
        }
    }
]


