from webapi import create_app

if __name__ == "__main__":
    app = create_app('DEVELOPMENT')
    app.run()