# bingo

A rather simple, multiplayer, Bingo game!

## Features
- Bingo!
- Multiplayer
- Great for quarantines!

## Usage
### Playing
Try it out online at [https://bingo.cazier.xyz](https://bingo.cazier.xyz)!

### Deployment
Run in a "development" environment super easily!

```
# Clone the files
git clone https://github.com/cazier/bingo

# Enter the directory
cd bingo

# Install requirements
pipenv install

# (Optional) Set debug flag to see requests and details
export DEBUG_APP=1

# Run!
uvicorn bingo.web:app --host 0.0.0.0 --port 5000

# or with gunicorn (This only works with one worker at this time)
gunicorn bingo.web:app -w 1 -k uvicorn.workers.UvicornWorker -b '0.0.0.0:5000'
```

Alternatively, you can run it using Docker pretty easily too! This is how I run it in "production". Make sure to forward port 5000 from the container as needed!

```
docker run -p 5000:5000 -it cazier/bingo:latest
```
