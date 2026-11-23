# Pokémon Klondike Version online

A web page that runs the game in the browser, with a small server that lets people
in the same room see each other walk around on the overworld.

## What is in here

- `server.js`: serves the page and relays where each player is (a web socket at `/ws`).
  It holds no game, patch or save. Rooms live in memory only.
- `public/index.html`: the page. The player drops their own FireRed (US 1.0) and the
  `.bps` patch. The page makes the game in the browser (CRC checks first), starts
  the emulator and joins a room.
- `public/mgba.js`, `public/mgba.wasm`: the mGBA emulator built for the web
  (`@thenick775/mgba-wasm` 2.6.0, mGBA is MPL 2.0, https://mgba.io). Not changed.
- `render.yaml`: for Render.

## How other players get into the game

The ROM has a small block of memory (`gHanMailbox`, `src/han_multiplayer.c`) that
starts with the letters KLNDKMBX. Every frame on the overworld the game writes where
the player is (map, tile, facing, walking, picture) and draws up to four other
players as sprites from the same block. The page finds the block in the emulator's
memory, sends "mine" to the server about 20 times a second and writes what the
server sends into "others". The game itself has no link to the internet.

Walking, running and the bike show; nothing else is shared. No talking, trading or
battling yet. Trading and battling would need the link cable to be carried over the
net, which is a separate job.

## Put it on Render

1. Put this folder in a GitHub repository (no game files: `public/` holds only the
   emulator and the page).
2. On render.com, New > Web Service, pick the repository. Render reads `render.yaml`
   (Node, `npm install`, `npm start`).
3. Open the address Render gives. Players use it with their own game file and the
   patch file you give them.

The free plan sleeps after a quiet while and the first visit then takes a minute.
Rooms are lost when it sleeps. The page needs `https`, which Render gives.

## Run it on your own computer

    npm install
    npm start
    # open http://localhost:3000

## The patch file

It is a difference between the original game and the hack, so it holds the new
pictures and the music. Give it only to people you mean to play with. Do not put it
in the repository or on the page.
