# Game of Maze

## Rules

See rules for game of maze docs/CodingProblem.pdf

## Play game

In order to play game you will need to clone the repository to your local comptuter and navigate to the directory containing runner scripts and example files

```
git clone https://github.com/andrimar1/maze.git
cd maze/
```

There are multiple 

### Runnig example using local python

Setup python environment using pipenv See: https://realpython.com/pipenv-guide/

```
# Setup pipenv
pipenv shell
```

If everything goes accoring to plan we are ready to play the maze game using our example files. We pass the game definition file by adding the `-i` or `--input` along with relative or absolute path to the file to our call

```
# Example run 1
python3 main.py -i docs/Sample.txt

# Example run 2
python3 main.py -i docs/Sample2.txt
```

### Run using Docker 

If you have Docker set up on your machine we can also play the game as a containeriz application. We fist need to build the docker containeras follows

```
docker build . -t mazegame:latest
```

After build process completes we can start the container in interactive mode

```
docker run -it mazegame:latest /bin/bash
```

From the container terminal we can then play the game using the example files provided as we did locally:

```
# Example run 1
python3 main.py -i docs/Sample.txt

# Example run 2
python3 main.py -i docs/Sample2.txt
```

#### Mounting local data to container for playing game with custom game definitions

You can also user your own game definitions to play the game. The only thing you need to do is to mount a local directory to the docker container 

```
docker run -v path/to/local/dir:/src/mnt -it mazegame:latest /bin/bash
```

And then we can play the maze game as before using our own files

```
# Custom run 1
python3 main.py -i src/mnt/CustomDef.txt
```
