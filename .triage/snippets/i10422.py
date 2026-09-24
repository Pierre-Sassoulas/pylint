class MyClass:
    meth_name = "test"

    def _call_test(self):
        pass

    def _call_provider(self):
        method = getattr(self, f"_call_{self.meth_name}", None)
        method()
        method2 = getattr(self, "_call_%s" % self.meth_name, None)
        method2()
