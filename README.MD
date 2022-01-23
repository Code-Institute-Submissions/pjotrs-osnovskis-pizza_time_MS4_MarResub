# PIZZA TIME

## DO NOT FORGET

1. Switch off development mode
2. Remove EMAIL_BACKEND from project folder settings.py

## Tech used

*  Allauth - command: `django-allauth` - used for authentication
* [Glassmorphism](https://hype4.academy/tools/glassmorphism-generator) - used to achieve frosted effects gor navigation
* [Bootstrap](https://getbootstrap.com/) - for grid and some styling


## Difficulties faced

1. Project folder settings.py had automatically generated SECRET KEY, I pushed it accidentally with Initial Commit. Resolved by: Changed secret key and moving it to env.py file. Env.py file was added to .gitignore and SECRET_KEY variable linked to Env.py in project's settings.py file.



