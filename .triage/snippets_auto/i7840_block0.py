class Service:
    class Command:
        def __init__(self, service:'Service'):
            reply = queue.Queue()
            self.service = service
        def execute(self):
            self.service._execute(self.reply)
        def get_reply(self):
            return self.reply.get()
            
    def __init__(self):
        self.commands = queue.Queue()
        self.running = True
        self.worker = threading.Thread(target=self.run)
        self.worker.start()

    def run(self):
        while self.running:
            try:
                command = self.commands.get(timeout=1)
                command.execute()
            except queue.Empty:
                pass

    def _execute(self, reply):
        reply.put("Done")

    def Execute(self):
        command = Service.Command()
        self.commands.put(command)
        return command.get_reply()
