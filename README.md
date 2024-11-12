# DevBlog-Django - A Professional Django Blog Website

Welcome to the **DevBlog** project! This is a fully functional blog website built using **Django** that allows users to post, view, and manage blog entries. Whether you're a writer or a developer, **DevBlog** is designed to serve as a powerful and easy-to-use platform to share content and interact with readers.

![DevBlog UI](media/DevBlog%20UI.png)


## Features

- **User Authentication**: Register, log in, and manage your profile.
- **CRUD Operations for Blogs**: Create, read, update, and delete blog posts.
- **Categories**: Organize blog posts by categories for easy navigation.
- **Search**: Search for posts by title, content, or tags.
- **Admin Panel**: Full control over blog posts, users, and content from the Django admin interface.

## Technologies Used

- **Django**: Web framework for building the app.
- **Python 3.x**: Programming language used.
- **SQLite**: Database for data storage.
- **Bootstrap**: Front-end framework for responsive design.
- **Django Allauth**: For user authentication and social login.

# Setup & Installation

### Prerequisites

Make sure you have the following installed:

- Python 3.x
- pip (Python package installer)
- Git

### Clone the Repository

Clone this repository to your local machine using Git:

```bash
git clone https://github.com/ganeshsriprasad/Devblog-Django.git
```

# Create and Activate a Virtual Environment
A virtual environment is recommended to isolate the project dependencies. Follow the steps below:

## Navigate to the project directory:
```shell
cd Devblog-Django
```

## Create a virtual environment.
```bash
python -m venv myenv
myenv\Scripts\activate
```

Once activated, your terminal prompt will change to show the virtual environment name.
## Install Dependencies
With the virtual environment activated, install the required dependencies using pip:
```bash
pip install -r requirements.txt
```

## Run the Development Server
To start the development server, use the following command:
```bash
python -m manage runserver
```


### You can now access the website at http://127.0.0.1:8000/ in your browser.

### Usage
Once the server is up and running, you can:
Register a new user or log in using your credentials.
Create, view, and manage blog posts through the interface.
Administer your blog through the Django admin panel (/admin).

### Contribution
Feel free to fork the repository and contribute by creating pull requests. Whether it's bug fixes, feature requests, or improving documentation, all contributions are welcome!

### License
This project is licensed under the MIT License.







