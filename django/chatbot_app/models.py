from django.db import models

# Create your models here.
class TBL_DISEASE_INFO(models.Model):
    #symptom = models.CharField(max_length=100)
    disease = models.CharField(max_length=50)
    def __str__(self):
        return self.disease

class TBL_MEDICINE_INFO(models.Model):
    medicine = models.CharField(max_length=100)
    imgurl = models.URLField(max_length=512)
    manufacturer = models.CharField(max_length=50)
    effect = models.TextField()
    usage = models.TextField()
    precautions = models.TextField()
    reference = models.URLField(max_length=512)
    disease = models.ForeignKey(
            TBL_DISEASE_INFO,
            on_delete=models.CASCADE,
            null=False
            )

    def __str__(self):
        return self.medicine

class TBL_MEDLIST_INFO(models.Model):
    medicine = models.CharField(max_length=100)
    effect = models.TextField()
    usage = models.TextField()
    precautions = models.TextField()
    reference = models.URLField(max_length=512)

    def __str__(self):
        return self.medicine

class TBL_FOOD_INFO(models.Model):
    food1 = models.CharField(max_length=50, null=True)
    food2 = models.CharField(max_length=50, null=True)
    food3 = models.CharField(max_length=50, null=True)
    youtube1 = models.URLField(max_length=512, null=True)
    youtube2 = models.URLField(max_length=512, null=True)
    imgurl1 = models.URLField(max_length=512, null=True)
    imgurl2 = models.URLField(max_length=512, null=True)
    disease = models.ForeignKey(
        TBL_DISEASE_INFO,
        on_delete=models.CASCADE,
        null=False
    )

    def __str__(self):
        return self.food1

class TBL_IMG_INFO(models.Model):
    image = models.ImageField(blank=True, null=True)

    def __str__(self):
        return str(self.id)

class TBL_BERT_INFO(models.Model):
    symptom = models.TextField()

    def __str__(self):
        return self.symptom
