import libtorrent as lt
import loopie

'''
Created on Friday 12/07/2019

@author: yaztown
'''

import loopie
from flask import send_from_directory

class MyMain(loopie.MainLoop):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.i = 0
        self.ses = lt.session()
    
    def loop_logic(self):
        self.i += 1
        print(self.i)
    
    def importRoutes(self):
        # You can override this method to import the route file or create your on url routes
        @self.web_app.route('/')
        def index():
            return self.web_app.send_static_file('index.html')

        @self.web_app.route('/<path:path>')
        def send_file(path):
            return send_from_directory(self.web_app.static_folder, path)

        @self.web_app.route('/hello')
        def hello(**kwargs):
            return 'Hello from overridden importRoutes()'

        @self.json_rpc.method('MyLoop(uuid=String)')
        def MyLoop(uuid: str) -> dict:
            # uuid = kwargs.pop('uuid', 'no uuid')
            return dict(app='loopie_test', status='running', i=self.i, uuid=uuid)

if __name__ == '__main__':
    main = MyMain(name='main', server_root_dir='example/www', enable_web_browsable_api=True, server_port=8765)
    app = loopie.Application(main)
    main.importRoutes()
    
    # @main.json_rpc.method('MyLoop(uuid=String) -> Object')
    # def MyLoop(**kwargs):
    #     uuid = kwargs.pop('uuid', 'no uuid')
    #     return dict(app='loopie_test', status='running', i=main.i, uuid=uuid)
    
    app.start()
    print('application ended')
