# BlogVerse


## Problem Statement
Create an web application to facilitate the blog creation capabilities with below mentioned features
1. Create infrastructure in such a way that any user can create their blog.
2. Allow user to use different type of formatting for text
3. Your web application should allow user to generate a link for every blog created at
your application so that user can showcase their blog to real world.
Technology:
• Python (Flask)
• Database (NoSQL)
• HTML
• Javascript, CSS, Bootstrap.


## Introduction
BlogVerse is a Blog Creator Web Application project aimed at facilitating users to showcase their contents, thoughts, skills in the form of Blogs.
This project utilizes Web Development using Python technology and data are stored in NoSQL cloud server.
My motivation behind this project is to enhance my programming skills on Python along with learning various aspects of Web Development followed by building CI/CD pipeline and Could hosted Deployment.


## Features
* Real time blog creation by multple users.
* Real time updation and deletion of blog.
* Secured authentication for each user provides extra level of security.
* CRUD operations - Create Blog, Read Blog, Update Blog, Delete Blog
* Providing option to put comments as well as Ratings on blogs posted by other users.


## Tools
![image](https://github.com/abhijitpaul0212/BlogVerse/assets/9966441/744a3f74-5342-481c-b44b-18a2c89e8e9f)


## Installation
1. Navigate a new folder (e.g. Projects)
2. Intialize Git
   ```
   git init
   ```
4. Clone the repo
   ```
   git clone https://github.com/abhijitpaul0212/BlogVerse.git
   ```
6. Navigate to the BlogVerse folder (root folder)
7. Create virtual environment
   ```
   python3 -m venv .venv
   ```
9. Activate virtual environment
   ```
   source .venv/bin/activate
   ```
11. Install packages
    ```
    pip3 install -r requirements.txt
    ```
13. Setup environment variables as per you (use _.env.example_ file and rename it to _.env_)
14. Run the server
    ```
    python3 application.py_  | _flask run
    ```


## Unit Test
1. Navigate to the root folder
2. Run
   ```
   python -m pytest --disable-warnings
   ```


## Flask Scripts 
Adding single new category
```
python manage.py --name=<category_name>
```

Adding multiple new categories
```
python manage.py --name=<category1_name,category2_name,category3_name>
```


### Project URLs
1. Render: https://blogverse-dhh8.onrender.com/
2. AWS: http://blogverse-env.eba-m3q4hiu7.us-east-1.elasticbeanstalk.com/


## Project Demo
https://github.com/abhijitpaul0212/BlogVerse/assets/9966441/59ac1f31-a155-4c8d-a1dd-ed823538f025


## Project Artifacts
1. High Level Design (HLD): [HLD_BloggingWebsite.pdf](https://github.com/abhijitpaul0212/BlogVerse/files/12819491/HLD_BloggingWebsite.pdf)
2. Low Level Design (LLD): [LLD_BloggingWebsite.pdf](https://github.com/abhijitpaul0212/BlogVerse/files/12819488/LLD_BloggingWebsite.pdf)
3. Architecture Design: [Architechture_BloggingWebsite.pdf](https://github.com/abhijitpaul0212/BlogVerse/files/12819485/Architechture_BloggingWebsite.pdf)
4. Wireframe Document: [Wireframe_BloggingWebsite.pdf](https://github.com/abhijitpaul0212/BlogVerse/files/12819489/Wireframe_BloggingWebsite.pdf)
5. Detailed Project Report (DPR): [DPR_BloggingWebsite.pdf](https://github.com/abhijitpaul0212/BlogVerse/files/12819490/DPR_BloggingWebsite.pdf)
6. Project Demo Video: https://youtu.be/8lv5jNUXcKQ?si=Ff1MIxzQMp9MBvj1


## Project Hierarchy
```
BlogVerse
├── application.py
├── config.py
├── manage.py
├── README.md
├── requirements.txt
├── src
│   ├── extensions.py
│   ├── models
│   │   ├── blog.py
│   │   ├── user.py
│   ├── routes
│   │   ├── blogs
│   │   │   ├── routes.py
│   │   ├── main
│   │   │   ├── routes.py
│   ├── static
│   │   ├── css
│   │   │   └── styles.css
│   │   ├── images
│   │   │   ├── bg.jpg
│   │   │   ├── blogverse.png
│   │   │   └── logo.svg
│   │   └── scripts
│   │       └── message.js
│   ├── templates
│   │   ├── base.html
│   │   ├── blogs
│   │   ├── flask_user
│   │   │   ├── emails
│   │   │   ├── login.html
│   │   │   ├── register.html
│   │   ├── index.html
│   │   ├── layout.html
│   │   └── oops.html
├── tests
│   ├── conftest.py
│   ├── unit
```

## Contributing
Contributions to this project are welcome. If you find any issues or want to enhance the functionality, feel free to open a pull request. Please make sure to follow the coding conventions and provide detailed information about the changes.


## License
This project is licensed under the MIT License.

