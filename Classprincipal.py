from WIIN import RecordViewer,API

if __name__ == "__main__":

    url = "https://671be4f02c842d92c381abd3.mockapi.io/test"
    api = API(url)
    app = RecordViewer(api)
    app.mainloop()


