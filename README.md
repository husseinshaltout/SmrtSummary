
# SmrtSummary

SmrtSummary, provides a visual slice vertical of a video highlighting changing patterns of the video frames, generating a report for the user showing a summary events timestamps allowing a quicker method for reviewing long CCTVs footage. 
## Demo

https://smrtsummary.herokuapp.com/


## Development

## Install and Run

Clone the project

```bash
  git clone https://github.com/husseinshaltout/SmrtSummary.git
```

Go to the project directory

```bash
  cd SmrtSummary
```
## Create virtual environment
```
python -m venv <env_name>
```
## Activate virtual environment
- ### Mac/Linux
    ``` bash
    source ./venv/bin/activate
    ```
- ### Windows
    ``` bash
    venv\Scripts\activate.bat
    ```
    You may need to add full path (c:\users\....venv\Scripts\activate.bat)

## Install requirements

```bash
pip install -r requirements.txt
```

### Start database migration
```bash
python manage.py migrate
```

### Start the development server
```bash
python manage.py runserver
```


## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`DJANGO_SECRET_KEY`



## Authors

- [@husseinshaltout](https://www.github.com/husseinshaltout)

## License

[MIT](https://choosealicense.com/licenses/mit/)
