
# Deficit-API

Deficit-API is a Django-based RESTful API designed to track and manage dietary intake, specifically focusing on caloric intake and expenditure. It allows users to maintain a log of foods consumed and exercises performed to manage their caloric deficit effectively.

## Live Hosting
This API is hosted live using pythonanywhere to [MotiDivya Deficit API](https://divyeshdeficit.pythonanywhere.com/)

## Features

1. **Food Management**: Users can add, update, and delete food items along with their caloric values and units.
2. **Exercise Tracking**: Allows users to log their physical activities along with calories burned.
3. **Caloric Deficit Calculation**: Automatically calculates daily caloric deficits based on food intake and exercise.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

What things you need to install the software:

- Python 3.x
- Django
- Django Rest Framework

### Installing

A step-by-step series of examples that tell you how to get a development environment running:

1. Clone the repository:

   ```sh
   git clone https://github.com/divyesh1099/Deficit-API.git
   ```

2. Install required packages:

   ```sh
   pip install -r requirements.txt
   ```

3. Migrate the database:

   ```sh
   python manage.py migrate
   ```

4. Run the server:

   ```sh
   python manage.py runserver
   ```

### Using the API

Here's a summary of the API endpoints for managing user-added foods, formatted in a tabular view. This table assumes you are running the Django server locally and using the default development URL (`http://127.0.0.1:8000/`). Adjust as necessary for your actual environment, especially when deployed:

| Method | API Endpoint                | Body                                              | Headers                 | Description                                  |
|--------|-----------------------------|---------------------------------------------------|-------------------------|----------------------------------------------|
| POST   | `/userfoods/`           | `{ "food": 1, "amount": 100 }`                    | `Authorization: Token <your_token>` <br> `Content-Type: application/json` | Create a new user food entry.                |
| GET    | `/userfoods/`           | None                                              | `Authorization: Token <your_token>`         | Retrieve a list of all food entries for the authenticated user. |
| GET    | `/userfoods/<int:id>/`  | None                                              | `Authorization: Token <your_token>`         | Retrieve a specific user food entry by its ID. |
| PUT    | `/userfoods/<int:id>/`  | `{ "food": 1, "amount": 150 }`                    | `Authorization: Token <your_token>` <br> `Content-Type: application/json` | Update an entire specific user food entry.  |
| PATCH  | `/userfoods/<int:id>/`  | `{ "amount": 120 }`                               | `Authorization: Token <your_token>` <br> `Content-Type: application/json` | Partially update a specific user food entry.|
| DELETE | `/userfoods/<int:id>/`  | None                                              | `Authorization: Token <your_token>`         | Delete a specific user food entry.          |


(exercise APIs are yet to be added)


**Notes**:

- Replace `<int:id>` with the actual ID of the user food entry you want to interact with.
- Replace `<your_token>` with the actual authentication token of the logged-in user.
- The `food` value in the body should be the ID of an existing food in your database.
- For `Authorization`, you might need to replace `'Token'` with `'Bearer'` or another prefix depending on your authentication setup.
- The actual URL path may vary depending on your project's `urls.py` configuration.
- This table assumes you are using token-based authentication. If you are using a different method, the `Authorization` header may vary.
- The `Content-Type: application/json` header is important when sending a body payload; it tells the server to expect JSON data.

## Deployment

Instructions on how to deploy the project on a live system like PythonAnywhere:

1. Set up your PythonAnywhere account and web app.
2. Upload your project files or clone your repository.
3. Set up your virtual environment and install dependencies.
4. Configure static and media files.
5. Reload your web app.

Detailed instructions are available on [PythonAnywhere Help](https://help.pythonanywhere.com/pages/).

## Built With

- [Django](https://www.djangoproject.com/) - The web framework used
- [Django Rest Framework](https://www.django-rest-framework.org/) - Toolkit for building Web APIs

## Contributing

Please read [CONTRIBUTING.md](./CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

## Authors

- **Divyesh Nandlal Vishwakarma** - *Initial work* - [LinkedIn Divyesh Vishwakarma](https://www.linkedin.com/in/divyesh-vishwakarma-621197175/)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Divyesh Vishwakarma's Body that said, ITS TIME TO FEEL GOOD BABY.
- Moti❤️.
