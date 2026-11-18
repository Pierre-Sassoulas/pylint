class MyTestRunner(DiscoverRunner):
    def run_tests(self, test_labels, extra_tests=None, **kwargs):
        my_custom_code()
        super(PaesslerTestRunner, self).run_tests(test_labels, extra_tests=extra_tests, **kwargs)
