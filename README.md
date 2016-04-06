# SERC - Software Engineering Research Center

![SERC Logo](https://raw.githubusercontent.com/skbly7/serc/master/website/static/images/logo_big.jpg)

Official website for Software Engineering Research Center, IIIT-Hyderabad. http://serc.iiit.ac.in/


### Lanch development server

1. Clone this repo using  `git clone git@github.com:skbly7/serc.git` (recommended) or `git clone https://github.com/skbly7/serc.git`
2. Install the packages given in [package.txt](https://github.com/skbly7/serc/blob/master/package.txt) (centos) or equivalent depending on your linux distribution.
3. Create new virtualenv using `virtualenv deploy`
4. Install dependencies `pip install -r requirement.txt`
5. Go to `website` folder, and run `python manage.py runserver`


### Production deployment

- Nginx configuration is available [here](https://github.com/skbly7/serc/blob/master/nginx_serc.conf). Change the absolute directory paths as per your system
- Change directory information according to your setup in [startup.sh](https://github.com/skbly7/serc/blob/master/startup.sh), and add it as crontab entry `@reboot /absolute/path/to/startup.sh`

### Screenshot

| ![Screenshot](https://raw.githubusercontent.com/skbly7/serc/master/website/static/images/screenshot/website_screenshot_1.png) |  ![Screenshot](https://raw.githubusercontent.com/skbly7/serc/master/website/static/images/screenshot/website_screenshot_2.png) |
|----|----|
| ![Screenshot](https://raw.githubusercontent.com/skbly7/serc/master/website/static/images/screenshot/website_screenshot_3.png) |  ![Screenshot](https://raw.githubusercontent.com/skbly7/serc/master/website/static/images/screenshot/website_screenshot_4.png) |

