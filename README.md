# Book Reviewer Flask Application
## Overview

## Requirements
### Platforms
### Artifacts / Tools
| Artifact |  Version | Description |
|:---------|---------:|:------------|
| Python   | \>= 3.10 |             |
| Poetry   |          |             |

## Build and Deploy
### Build Instructions
### Deploy Instructions
## Questions and Issues
## Tasks
- [x] Create project in github
- [x] Install Nginx proxy to front Flask server
- [ ] Use docker-compose secrets for passwords and other sensitive data. See [Docker Secrets](https://docs.docker.com/compose/use-secrets/)
- [ ] Refactor to use consistent names in JSON request and response
- [ ] Allow multiple authors for a book
- [ ] Database Tasks
  - [ ] Add init-db to create and update schemas. See [Define and Access the Database](https://flask.palletsprojects.com/en/2.3.x/tutorial/database/)
  - [ ] Remove all tables
  - [ ] Use init-db to create schema and tables
- [ ] Use Flask-SqlAlchemy. See [Flask SQL Alchemy](https://flask-sqlalchemy.palletsprojects.com/en/3.1.x/)
- [ ] FIX: Flask redirects to Mac's local address -- Flask does not redirect through Nginx
