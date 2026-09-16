# models.py
# Income & Expenditure Management System
# Author: Kofi John Awarkano | Ghana
# For: Vistula University MSc Data Science and Business Informatics Oct 2026
# Purpose: SME Financial Platform for High Tech Glazing Ltd style business
# Tech: Django + PostgreSQL | BTech Accounting with Computing - Grade A Database

from django.db import models
from django.contrib.auth.models import User

class IncomeCollection(models.Model):
    """Income Collection - Tracks all SME income"""
    INCOME_SOURCES = [
        ('sales', 'Glazing Sales'),
        ('contract', 'Contract Payment'),
        ('service', 'Service Income'),
        ('other', 'Other Income'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    source = models.CharField(max_length=20, choices=INCOME_SOURCES)
    description = models.TextField()
    date = models.DateField()
    location = models.CharField(max_length=100, default='Accra, Ghana')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Income GHS {self.amount} - {self.source} - {self.date}"

    class Meta:
        ordering = ['-date']
        verbose_name = 'Income Collection'

class ExpenditureCollection(models.Model):
    """Expenditure Collection - Tracks all SME expenses"""
    CATEGORIES = [
        ('materials', 'Materials - Glass, Aluminium'),
        ('labor', 'Labor Cost'),
        ('transport', 'Transport'),
        ('rent', 'Office Rent'),
        ('utilities', 'Utilities'),
        ('other', 'Other'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    category = models.CharField(max_length=20, choices=CATEGORIES)
    description = models.TextField()
    receipt_no = models.CharField(max_length=50, unique=True)
    date = models.DateField()
    vendor = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Expense GHS {self.amount} - {self.category}"

    class Meta:
        ordering = ['-date']
        verbose_name = 'Expenditure Collection'

class ReceiptCollection(models.Model):
    """Receipt Collection - Auto-generates receipts for income"""
    income = models.ForeignKey(IncomeCollection, on_delete=models.CASCADE)
    receipt_number = models.CharField(max_length=50, unique=True)
    issued_to = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    pdf_file = models.FileField(upload_to='receipts/', blank=True, null=True)

    def __str__(self):
        return f"Receipt {self.receipt_number} - GHS {self.income.amount}"

class PaymentCollection(models.Model):
    """Payment Collection - Tracks payments to vendors/suppliers"""
    expenditure = models.ForeignKey(ExpenditureCollection, on_delete=models.CASCADE)
    payment_number = models.CharField(max_length=50, unique=True)
    paid_to = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=20, choices=[
        ('cash', 'Cash'),
        ('momo', 'Mobile Money'),
        ('bank', 'Bank Transfer'),
        ('cheque', 'Cheque')
    ])
    is_paid = models.BooleanField(default=False)
    payment_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.payment_number} - {self.paid_to}"

# For Reporting Dashboard - Monthly Profit View
class FinancialReport(models.Model):
    month = models.DateField()
    total_income = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_expenditure = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    @property
    def profit(self):
        return self.total_income - self.total_expenditure
    
    def __str__(self):
        return f"Report {self.month} - Profit GHS {self.profit}"
