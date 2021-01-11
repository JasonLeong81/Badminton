from Intro import create_app # import the function create_app instead of current_app

app = create_app()
if __name__ == '__main__': # another way to run rather than using cmd
    app.run(debug=True)








