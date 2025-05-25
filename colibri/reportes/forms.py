from django import forms
from django.core.exceptions import ValidationError
from .models import Reporte

class ReporteForm(forms.ModelForm):
    class Meta:
        model = Reporte
        fields = ['tipo_reporte', 'descripcion', 'ubicacion', 'imagen', 'video', 'audio', 'latitud', 'longitud']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 4}),
        }

    def clean_imagen(self):
        imagen = self.cleaned_data.get('imagen')
        if imagen:
            if not imagen.name.lower().endswith(('.jpg', '.jpeg', '.png')):
                raise ValidationError("Solo se permiten archivos JPG o PNG")
            if imagen.size > 5 * 1024 * 1024:
                raise ValidationError("El tamaño máximo permitido es 5MB")
        return imagen

    def clean_video(self):
        video = self.cleaned_data.get('video')
        if video:
            if not video.name.lower().endswith(('.mp4', '.mov')):
                raise ValidationError("Solo se permiten archivos MP4 o MOV")
            if video.size > 50 * 1024 * 1024:
                raise ValidationError("El tamaño máximo permitido es 50MB")
        return video

    def clean_audio(self):
        audio = self.cleaned_data.get('audio')
        if audio:
            if not audio.name.lower().endswith(('.mp3', '.wav')):
                raise ValidationError("Solo se permiten archivos MP3 o WAV")
            if audio.size > 20 * 1024 * 1024:
                raise ValidationError("El tamaño máximo permitido es 20MB")
        return audio
