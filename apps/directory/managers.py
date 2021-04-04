from django.db import models


class TeacherQuerySet(models.QuerySet):
    def last_name_first_letter(self, first_letter):
        """
        Teachers to filtered by first letter of last name.
        """
        return self.filter(last_name__istartswith=first_letter)

    def teach(self, subject_name):
        """
        Teachers to filtered by subject name
        """
        return self.filter(subjects__name__iexact=subject_name)


class TeacherManager(models.Manager):
    """
    To chain use of the methods
    """

    def get_queryset(self):
        return TeacherQuerySet(self.model, using=self._db)

    def last_name_first_letter(self, first_letter):
        return self.get_queryset().last_name_first_letter(first_letter)

    def teach(self, subject_name):
        return self.get_queryset().teach(subject_name)