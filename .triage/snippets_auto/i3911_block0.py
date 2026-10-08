    from rest_framework import generics

    class SomeView(generics.RetrieveUpdateAPIView):
        def update(self, request, *args, **kwargs):  # args and kwargs are flagged as unused-arguments
            return 1
    
