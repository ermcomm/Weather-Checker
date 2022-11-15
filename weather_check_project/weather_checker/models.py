from django.db import models


class api_configs(models.Model):
    api = models.CharField(primary_key=True, null=False,
                           blank=False, max_length=150)
    api_token = models.CharField(null=False, blank=False, max_length=200)


class weather_records(models.Model):
    time_of_search = models.DateTimeField(auto_created=False)
    searched_address = models.CharField(max_length=150)
    # this will be populated by json str
    weather = models.CharField(max_length=500)
    weather_icon = models.CharField(max_length=500)
    temp = models.FloatField()
    feels_like_temp = models.FloatField()
    wind_speed = models.FloatField()
    wind_direction = models.FloatField()
    humidity = models.FloatField()
    cloud_cover = models.FloatField()
    min_temp = models.FloatField()
    max_temp = models.FloatField()


# If you're using Postgres, you can store json with JSONField(read more), but if not, you need parse json to string and save with CharField/TextField using json.dumps(data). To recovery data, use json string to dict with json.loads(json_string)
