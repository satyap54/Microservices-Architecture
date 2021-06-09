from tortoise import fields, models


class Event(models.Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=100)
    image = fields.CharField(max_length=200)
    

class EventUser(models.Model):
    # use auto-generated id as pk
    user_id = fields.IntField()
    event_id = fields.IntField()

    class Meta:
        unique_together = (("user_id", "event_id"), )