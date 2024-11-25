from app import create_app

# Create the app instance using the app factory function
app = create_app()

# Run the application
if __name__ == '__main__':
    app.run(debug=True)

