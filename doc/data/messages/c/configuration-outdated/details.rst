This message is about your pylint configuration, not about your code.

Your configuration file predates a pylint release that renamed options,
removed options, or changed defaults. Run ``pylint-config upgrade`` to
review those changes and update the file. Each run records an
``upgraded-to`` marker so the reminder does not come back.

To always follow pylint's current defaults without being reminded, set
``upgraded-to = latest`` in your configuration.
