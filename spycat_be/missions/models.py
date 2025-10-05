from django.db import models
from cats.models import SpyCat


class Mission(models.Model):
    cat = models.ForeignKey(SpyCat, on_delete=models.SET_NULL, null=True, blank=True, related_name="missions")
    name = models.CharField(max_length=100)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} ({'Completed' if self.completed else 'In Progress'})"

    def update_completed_status(self):
        """Mark mission as completed if all targets completed."""
        if self.targets.exists() and all(t.completed for t in self.targets.all()):
            self.completed = True
            self.save()
        else:
            self.completed = False
            self.save()


class Target(models.Model):
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE, related_name="targets")
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    notes = models.TextField(blank=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} ({'Completed' if self.completed else 'Pending'})"

    def save(self, *args, **kwargs):
        """Prevent notes update if target or mission is completed."""
        if self.pk:
            old = Target.objects.get(pk=self.pk)
            if (old.completed or self.mission.completed) and self.notes != old.notes:
                raise ValueError("Cannot update notes: target or mission is completed.")
        super().save(*args, **kwargs)
        self.mission.update_completed_status()
