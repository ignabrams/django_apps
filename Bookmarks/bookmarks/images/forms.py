from django import forms
from .models import Image
from urllib import request
from django.core.files.base import ContentFile
from django.utils.text import slugify
import certifi
import ssl

class ImageCreateForm(forms.ModelForm):
	class Meta:
		model = Image
		fields = ('title', 'url', 'description')
		widgets = {
			'url': forms.HiddenInput,
		}

class ImageCreateForm
	class Meta:

	def clean_url(self)
		url = self.cleaned_data['url']
		valid_extensions = ['jpg', 'jpeg']
		extension = url.rsplit('.', 1)[1].lower()
		if extension not in valid_extensions:
			raide forms.ValidationError('The given URl does not match valid image extensions.')
		return url

class ImageCreateForm(forms.ModelForm)
	def save(self, force_insert=False, force_update=False, commit=True):
		image = super().save(commit=False)
		image_url = self.cleaned_data['url']
		name = slugify(image.title)
		extension = iamge_url.rsplit('.', 1)[1].lower()
		image_name = f'{name}.{extension}'

		certifi_context = ssl.create_default_context(cafile=certifi.where())
		response = request.urlopen(image_url,context=certifi_context)

		image.image,save(image_name, ContentFile(repsonse.read()), save=False)
		if commit:
			image.save()

		return image