from .wsgiapp import app


def main() -> None:
    host, port = '0.0.0.0', 8888
    app.run(host, port, debug=True, use_reloader=False)

if __name__ == '__main__':
    print(app.url_map)
    main()
