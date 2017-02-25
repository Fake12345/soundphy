import hashlib

from rest.models import Sound
from rest_framework import generics
from rest.serializers import SoundListCreateSerializer
from rest.serializers import SoundRetrieveUpdateDestroySerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.authentication import BasicAuthentication
from rest_framework.authentication import SessionAuthentication


def hashfile(afile, hasher, blocksize=65536):
    buf = afile.read(blocksize)
    while len(buf) > 0:
        hasher.update(buf)
        buf = afile.read(blocksize)
    return hasher.digest()


class SoundList(generics.ListCreateAPIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticatedOrReadOnly,)

    queryset = Sound.objects.all()
    serializer_class = SoundListCreateSerializer

    def perform_create(self, serializer):
        sound = self.request.FILES['sound']
        codec = sound.content_type.split('/')[-1]
        size = sound._size
        duration = 0.0  # TODO
        sha1 = hashfile(sound.file, hashlib.sha1()).hex()
        sound._name = sha1
        # TODO: validate calculated parameters before saving
        # TODO: if file already uploaded, do not save
        serializer.save(codec=codec, size=size, duration=duration, sha1=sha1)


class SoundDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Sound.objects.all()
    serializer_class = SoundRetrieveUpdateDestroySerializer
