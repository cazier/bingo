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
git clone https://git.cazier.xyz/bcazier/bingo

# Enter the directory
cd bingo

# Install requirements
python -m pip install -r requirements.txt

# (Optional) Set debug flag to see requests and details
export DEBUG_APP=1

# Run!
python app.py
```

Alternatively, you can run it using Docker pretty easily too! This is how I run it in "production". Make sure to forward port 5000 from the container as needed!

```
docker run -p 8080:5000 -it cazier/bingo:latest
```