from rest_framework import generics

class SomeView(generics.RetrieveUpdateAPIView):
    def update(self, request, _1, _2):
        # ^^^ no error, even though it overrides the
        # rest_framework.mixins.UpdateModelMixin.update method
        # which has (self, request, *args, **kwargs) as arguments
        return 1

    def retrieve(self, request, _1, _2):
        # ^^^ arguments-differ, because it overrides the
        # rest_famework.mixins.RetrieveModelMixin.retrieve method
        # which has (self, request, *args, **kwargs) as arguments
        return 1
