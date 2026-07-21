from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user    = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    gender  = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return f"{self.user.username} profile"


class Expense(models.Model):
    CATEGORY_CHOICES = [
        ('school',   'School'),
        ('personal', 'Personal'),
        ('other',    'Other'),
    ]
    user        = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expenses')
    date        = models.DateField()
    category    = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    amount      = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} – {self.category} – {self.amount}"


class Income(models.Model):
    TYPE_CHOICES = [
        ('parental', 'Parental Allowance'),
        ('base',     'Base Allowance'),
        ('extra',    'Extra Allowance'),
    ]
    user        = models.ForeignKey(User, on_delete=models.CASCADE, related_name='incomes')
    month       = models.DateField()
    income_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    amount      = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.user.username} – {self.income_type} – {self.amount}"


class Savings(models.Model):
    user            = models.ForeignKey(User, on_delete=models.CASCADE, related_name='savings')
    goal_name       = models.CharField(max_length=100)
    target          = models.DecimalField(max_digits=10, decimal_places=2)
    current_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    monthly_plan    = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    target_date     = models.DateField(null=True, blank=True)
    is_emergency    = models.BooleanField(default=False)

    @property
    def progress_pct(self):
        if self.target > 0:
            return round(min(100, float(self.current_balance) / float(self.target) * 100), 1)
        return 0.0

    def __str__(self):
        return f"{self.user.username} – {self.goal_name}"
