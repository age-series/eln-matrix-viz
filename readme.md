# eln-matrix-viz

This program is used to debug Electrical Age matrices.

## Usage

In Minecraft as OP:

```
/eln matrix
```

Then in a Bash shell,

```
mkdir dots
mkdir png
python3 main.py
```

TODO:

**NOTE**: program currrently pulls from `/home/jared/.local/share/multimc/instances/testing/.minecraft/elnDumpSubSystems.txt`, will need to be modified for current user and path.

Then,

```
./makePng.sh
```

After you do this, you will find a whole lot of PNG files in the `png` folder.
