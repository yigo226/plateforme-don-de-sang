

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django import forms
from .models import Utilisateur

# Formulaire pour créer un utilisateur dans l'admin
class UtilisateurCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirmation mot de passe", widget=forms.PasswordInput)

    class Meta:
        model = Utilisateur
        fields = ('email', 'first_name', 'last_name', 'role')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password1 != password2:
            raise forms.ValidationError("Les mots de passe ne correspondent pas")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])  # 🔑 crypte le mot de passe
        if commit:
            user.save()
        return user

# Formulaire pour modifier un utilisateur
class UtilisateurChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(label="Mot de passe")

    class Meta:
        model = Utilisateur
        fields = ('email', 'password', 'first_name', 'last_name', 'role', 'is_active', 'is_staff', 'is_superuser')

    def clean_password(self):
        return self.initial["password"]

# Admin personnalisé
class UtilisateurAdmin(BaseUserAdmin):
    form = UtilisateurChangeForm
    add_form = UtilisateurCreationForm

    list_display = ('email', 'first_name', 'last_name', 'role', 'is_staff', 'is_superuser')
    list_filter = ('role', 'is_staff', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Informations personnelles', {'fields': ('first_name', 'last_name', 'role')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'role', 'password1', 'password2'),
        }),
    )
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    filter_horizontal = ()


# Enregistrer l’admin
admin.site.register(Utilisateur, UtilisateurAdmin)
