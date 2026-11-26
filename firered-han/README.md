# Hän letters in pokefirered

This folder adds the Hän alphabet to the game's four Latin fonts.

## What is here

| file | what it does |
|---|---|
| `han_font.py` | Draws the glyphs into `graphics/fonts/latin_*.png`, sets their widths in `src/text.c`, and writes their lines in `charmap.txt`. Safe to run again. |
| `han_preview.py` | Renders a sheet of every glyph to a PNG without building the game. |
| `glyph_chart.py` | Swaps Professor Oak's first lines for a test card of every glyph (`on`), or puts them back (`off`). |
| `han_text.py` | Moves text between one workbook and the source files, and builds the game. |
| `han_labels.py` | Redraws the type labels (pictures) from the type names. `han_text.py` runs it at every build. |
| `han_title.py` | Redraws the blinking prompt on the title screen, which is a picture. Run by hand: `python3 tools/han/han_title.py "START K'ÄDÄNDEY"`. |
| `han_unown_letters.py` | Draws the 180 syllabics letters that fly at the foe in the UNOWN's move: the Carrier table at ydli.org, without the finals. Run by hand. It needs GNU Unifont. |
| `han_unown_trio.py` | Puts the game's own pictures of UNOWN J, C and ? into one picture, for CHAMPION JANE's UNOWN. The three touch and do not overlap, and the script checks that. `make` runs it. |
| `han_sylveon.py` | Makes the pictures of MANDI's SYLVEON from a picture that whoever builds supplies. `han_emerald.py` runs it. |
| `han_klondike.py` | Makes the title screen: KLONDIKE VERSION under the POKéMON logo and an UNOWN D where the CHARIZARD stood, from the game's own files. `han_emerald.py` runs it. Output is in `graphics/title_screen/klondike/`, not in git. |
| `han_pok3.py` | Puts a trainer together from the layers of the Pokémon Gen 3 Trainer pack (Jordan Bunke, itch.io) the way the pack's own manifest does, and writes test pictures. The pack is not in the repository: put the folder `pok3` next to `pokefirered`. |
| `han_theme.py` | Puts CHAMPION JANE's battle theme into the build if whoever builds has the music, as a MIDI file or as a recording. The music is in neither git nor the patch. `make` and `han_text.py` run it. |
| `han_theme_midi.py` | Arranges the MIDI file for the game: where it starts, which parts are kept, their instruments and volumes. `han_theme.py` uses it. |
| `han_theme_prepare.py` | The other way: turns a recording into one long sound for the game. Run by hand. It needs ffmpeg, and numpy and scipy to turn the drums down. |
| `han_syllabics.py` | Draws the syllabics font for the game from Jane's own font, and writes the tables that turn Latin Hän letters into syllables. Run by hand, with the path of her `_HanSyllabics.ttf`. |
| `syllabics_test.c` | Runs the game's syllabics converter on a computer, outside the game. |
| `han_syllabics_check.py`, `syllabics_ref.js` | Compare that converter with Jane's word processor on every piece of Hän text in a workbook. |
| `proper_names.txt` | Proper names the game's own lists do not have, for the asterisk in syllabics. `han_syllabics.py` reads it. |
| `han_english_sounds.py` | Spells every English word of the game by its sound, for syllabics, and writes `english_sounds.txt`. Run by hand. It needs the Python package `cmudict` and the file `checkpoint20.npz` of g2p_en. |
| `english_sounds.txt` | The list: each English word of the game, its sound in syllables, and where the sound came from. Lines can be changed by hand. |
| `cmudict_LICENSE.txt` | The licence of the CMU Pronouncing Dictionary, which most sounds in the list come from. |
| `han_english_table.py` | Turns the list into the table the game uses (`src/data/han_english_sounds.h`), without the words that are Hän in the translation. `han_text.py` and `make` run it. |
| `english_test.c`, `han_english_check.py` | Run the game's own word lookup on a computer and check it against every word of the list. |
| `han_emerald.py` | Brings the Pokémon pictures and animations of Emerald into the build, from a copy of the pokeemerald source. Nothing it writes is in git. `make` and `han_text.py` run it. |
| `han_animalese.py` | Cuts the letter sounds of animalese.js into samples for the UNOWN's move and turns each one up to full scale. Run by hand. |
| `translator_template.html` | The page behind `han_text.py tool`, which writes the HTML translator. |
| `old_tool_offsets.json` | Lets `han_text.py` read sheets exported by the old browser tool. |
| `shot/harness.c` | Runs a built ROM in mGBA with no window and saves real screenshots. |

## Translating: the workbook

    python3 tools/han/han_text.py workbook OUT.xlsx --from OLD.xlsx
    python3 tools/han/han_text.py build BOOK.xlsx --report OUT.xlsx
    python3 tools/han/han_text.py restore

`workbook` writes every string in the game to one sheet. `build` puts the Hän
column into the source files and runs `make`. `--report` writes the workbook
back out with its In game, Source and Notes columns brought up to date.
`restore` puts the English files back. `--from` and `build` both read this
workbook, a save file (`.json`) from the translator page, or a sheet exported
by the old browser tool.

    python3 tools/han/han_text.py tool PAGE.html --from SAVED.json

`tool` writes the translator page: one offline HTML file to type into, with the
strings still to do ranked by how much they matter in play. Its Save file
button makes the `.json` that `build` reads. Copy English on a row keeps the
English for that line.

The page counts progress against the plan: everything except side features,
trainer classes and names, item names, Pokémon names, abilities and natures.
Text outside the plan stays English unless somebody types it, and the page
lists it only when it is typed or when "Show text outside the plan" is ticked.
Text from scenes that were taken out of the game (Oak's lesson in the first
battle, the old man's catching lesson, the POKé DUDE) is outside the plan too.
The plan is the lists above `in_plan` in `han_text.py`.

The page keeps its work in the browser, and that work wins over what the page
was made from. So when a save file is corrected by hand, make the page with
`--was OLDER.json` as well: a browser that still holds the older text of a
corrected row then takes the new text, and rows changed since are left alone.
Give every older save file the browser may still hold, with commas between
them.

How rows work:

- One row for each distinct English string in each kind of text. All dialogue
  is one kind, so a line used in ten places is one row and fills all ten. Each
  name table (moves, types, items, Pokédex and so on) is its own kind.
- If a string has no Hän of its own but the same English was typed on another
  row, it takes that Hän. An identical string comes first, then the same words
  with different line breaks. Source says `repeat`. Type on the row to
  override. The translator page fills these the same way as you type.
- Then the word rules on the Rules sheet. Source says `rule`.
- Where the English is in ALL CAPS, the Hän is put in capitals, however it was
  typed. Otherwise a translation typed in one case takes the case of the
  English, and mixed case is left as typed.
- A letter typed twice in a row is shown once: aa as a, yy as y, nn as n. A
  vowel typed twice with different marks keeps the first one: ìi as ì. tth and
  ddh stay, because they are single sounds. English words are left alone: a
  word is English when the game's own English text has it, or when the whole
  line is English. The few such words that are Hän where Jane types them are
  listed in `HAN_NOT_ENGLISH` in `han_text.py`. The workbook's Notes column
  lists every word changed.
- A piece of a sentence that the game joins to a name or a number ("Wild ",
  " is", " points") keeps the spaces the English has at its ends, whatever was
  typed. Without them the piece would touch the name.
- "'s nickname?" is printed straight after a name. A space typed in front of
  its translation is kept, because it is the only thing between the two.
- Neither rule changes what was typed. The save file and the Hän column keep
  it. Only the text that goes into the game is changed.
- Lines are wrapped by pixel width with the game's own glyph widths. Text box
  dialogue wraps at 196 px, two lines a box, with `{PARA}` between boxes. Other
  screens keep their own line count.
- A name too long for its slot is left in English in that place and noted.
  Nothing is ever shortened.

The English files are kept in `.han_orig/` while translated text is in place,
so `build` can be run again and again.

Change game code only after `restore`. If a file is edited while the Hän text
is in place, the tool sets it aside as `*.edited` and stops, so the change is
not lost.

Name slots: the tool reads the slot sizes from the source (`MOVE_NAME_LENGTH`
and the others). A name longer than its slot is noted in the workbook.

Three things in the game have a Hän name and no English one: the UNOWN's move,
its ability and the item it holds. The source calls them NEW MOVE, NEW ABILITY
and NEW ITEM, and Jane's names are typed rows in the workbook like any other.

## The game's text in syllabics

Up, Up, Up, Up, Select on the title screen or on the main menu shows all the
game's text in Jane's Hän syllabics. The same keys turn it off again. It also
ends when the game is reset. Nothing is saved.

The text itself is not changed. `RenderText` and `GetStringWidth` in
`src/text.c` read the same Latin letters and draw syllables instead, with
`HanSyl_Next` in `src/han_syllabics_core.h`.

- The shapes are Jane's. `han_syllabics.py` draws every syllable and final
  from her font at 12 pixels into `graphics/fonts/han_syllabics.png`, and
  writes `src/data/han_syllabics.h`. The font file is not in this repository.
- The rules follow her word processor as it starts: the Eagle way of writing
  finals, a tilde for a nasal vowel, a dot for a consonant plus y.
- The nasal tilde, the low tone mark and the dot sit on top of the syllable,
  in the two top rows of its cell. A syllable with marks is exactly as wide
  as without. The font picture has every syllable eight times, once for each
  set of marks, and the script checks each one: the marks are whole, inside
  the cell, and one clear row above the syllable. A text line is 14 pixels
  high, so 103 tall syllables are drawn one or two pixels lower when they
  have marks.
- The naming screen stays in Latin letters, so a name can be read while it is
  typed (`DoNamingScreen` in `src/naming_screen.c`). The name shows in
  syllabics once the screen is left.
- English words are spelled by their sound: see the next part. A word that
  is neither Hän nor in the list of English words (a name the player types)
  is read letter by letter, and a letter with no syllabic, such as c, f, p,
  v or x, stays a Latin letter.
- th, dh, tth, ddh, sr, zr, tr, dr and zh have no final in the font. At the
  end of a syllable they are written as two finals.

### English words are spelled by their sound

Read letter by letter, the way Hän is read, an English word comes out wrong:
TRAINER has no "ai" sound in it, and c, f, p, v and x stayed Latin letters.
So in syllabics the game looks every word up in a list of English words and
draws the sound the list gives. TRAINER is drawn tre, y, në, r.

This is English written with Jane's syllables. It is not Hän, and none of it
is Hän text. Which syllable stands for which English sound was chosen by the
assistant, as well as it could: the table is at the top of
`han_english_sounds.py`. Jane's font has no p, f, v or r syllables, so p is
written b, f is hw, v is w and r is zr, and so on. The weak vowel of English
(the, about, the end of trainer) is written ë, and so is the vowel of cup
and duck, as in Tr'ondëk. POKéMON is said with the weak vowel: bo, kë, ma, n.

The list, `english_sounds.txt`, has 7769 words: every word of the game's own
English text, and the English words of the rows Jane wrote in English. Each
line says where its sound came from:

| in the list | how many | what it is |
|---|---|---|
| `dictionary` | 6618 | the CMU Pronouncing Dictionary |
| `dictionary, with its ending` | 117 | the same, for a word the dictionary has without its ending |
| `fixed` | 517 | written by hand in the script: all the Pokémon names the guess got wrong, places, badges, berries, words the game writes as one (THUNDERBADGE), short forms said in full (LV, SP., PKMN), the game's laughs and cries |
| `letters` | 74 | said as letters: TM, HP, PP, PC |
| `guess` | 443 | a guess by a letter-to-sound model, for names and made-up words. These are the lines to check. |

To change a word, change its sound in the list and write `hand` in the third
column. `han_english_sounds.py` keeps such lines when it is run again.

How the game finds a word (`HanEng_Find` in `src/han_english_core.h`):

- A word is looked up when all of it is plain a to z, in capitals or not.
  é counts as e, and it may have apostrophes inside (don't). A word with any
  Hän letter in it (ä, ë, a nasal hook, a tone mark, ł) is Hän and is never
  looked up.
- NAME's is found when the list has NAME. The game adds the sound of the 's
  itself: s, z, or a syllable when the name ends in s, z, sh or ch.
- One letter with nothing after it is not a word. That is a key of a
  keyboard, or one letter of a name being typed.
- Each glyph of an English word is drawn on a visit of its own, like the
  asterisk of a name, so the text still appears a glyph at a time.

A Hän word must never be read as English. The game cannot tell a Hän word
from an English word that is spelled the same, so `han_text.py` takes such
words out of the table at every build, and the game then reads them as Hän
everywhere (`han_words` in `han_english_table.py`). The rule errs on the Hän
side. A plain word in a translated row is taken to be English only when

- the English of that row has the same word (a name the row keeps: POKéMON, TV),
- or the English of that row has it with another ending (BALL where the
  English has BALLS, save where it has saved),
- or the whole row is written in English: six words or more, three in four
  of them English words of the list. Jane's notice at the start of the game
  is three such rows.

Every other plain word in a translated row or a word rule is Hän. With the
text of 16 November 2026 the words taken out are cho, chu, ha, in, kay, w and
we. The build prints them each time. The cost is small: English "we" is then
read letter by letter too.

`A` is always read as the word "a", also in "A Button".

    python3 tools/han/han_english_check.py

runs the game's own lookup on a computer, on every word of the list in small
letters and in capitals, on every word with 's, on the words taken out and on
words with a Hän letter. It needs gcc.

The CMU Pronouncing Dictionary is (c) 1993-2015 Carnegie Mellon University.
Its licence is in `cmudict_LICENSE.txt` and must stay with the list. The
guesses are from the model of g2p_en by Kyubyong Park and Jongseok Kim
(Apache licence 2.0, https://github.com/Kyubyong/g2p). Neither is needed to
build the game: only the list is.

### Proper names start with an asterisk

In syllabics there are no capitals, so a proper name starts with an asterisk,
as in Carrier syllabics. Proper names are people, Pokémon and places. Nothing
is added to the text: the game draws the asterisk when the text at the start
of a word is a name it knows (`HanSyl_NameStartsAt` in `src/text.c`). It knows:

- the Pokémon names, the trainer names and the map names, as they are in the
  game after the build
- the names in `proper_names.txt`: people and places the lists do not have
  (BILL, KANTO), or have only inside a longer name (OAK, PALLET)
- the player's name, the rival's name, and the nicknames of the Pokémon in
  the player's party and the foe's

Lines in `proper_names.txt` that start with `-` take a name out: GRUNT and
ADMIN are in the trainer list and are not names, and RED and LEAF are also
ordinary words of the game (RED SHARD, LEAF STONE).

A name is found only where it is written exactly as in the list, as a whole
word. A nickname of a Pokémon in a PC box gets no asterisk unless it is the
Pokémon's own name. If the player is called RED, RED SHARD gets one.

To check the converter against the word processor:

    NODE_PATH=... python3 tools/han/han_syllabics_check.py BOOK.json PATH/TO/han-word-processor.html

It needs gcc, node and playwright. With Jane's text of 16 November 2026, 412
of 477 pieces of Hän come out the same. The other 65 differ in one of four
ways that are meant, and the script counts each kind.

## Pokémon pictures and animations from Emerald

Jane asked for the sprites and animations from Emerald. In Emerald a
Pokémon's front picture has two frames, and each Pokémon moves in its own
way when it comes out. Both are in this game now.

What the player sees:

- Every Pokémon has Emerald's front picture, back picture and colours: 414
  pictures, counting each UNOWN letter. For 165 of them the front picture is
  not the one FireRed had, and for 53 the back picture. Those are mostly the
  Pokémon of Kanto and Johto.
- A foe's Pokémon, when it comes out of its ball or out of the grass, shows
  its second frame for a moment and moves the way that species does in
  Emerald: a squash, a hop, a shake, a glow. Its cry comes with it. For a wild
  Pokémon that is a little later than in FireRed, where the cry came as soon
  as it had slid in.
- The player's Pokémon moves too when it comes out. A back picture has one
  frame. The way it moves is picked by species and nature, as in Emerald.
- The battle's next step waits until the animation is over, about a second.
- With the battle scene set to off in the options there is no animation.

Where it comes from. None of Emerald's pictures or code is in the patch.
`han_emerald.py` copies what is needed out of a copy of the pokeemerald
source, https://github.com/pret/pokeemerald, each time the game is built:

    git clone https://github.com/pret/pokeemerald ../pokeemerald
    git -C ../pokeemerald checkout 9103e529c2fbdd7add4a1ff3350c6c1f92112c42

The copy has to be next to this folder, or its path in the `POKEEMERALD`
environment variable, or given to the script. `setup.sh` gets it. The files
the script writes are listed at its top. All of them are ignored by git:
the pictures (`graphics/pokemon/NAME/emerald_*`), the list of picture files
(`src/data/graphics/pokemon_emerald.h`), where each picture stands and how
high it floats, which frame shows when, which way each Pokémon moves
(`src/data/pokemon_graphics/emerald_*.h`), and Emerald's own code for moving
a picture (`src/pokemon_animation.c`, `include/pokemon_animation.h`). That
code compiles here as it is.

FireRed's own pictures stay for four things. DEOXYS and CASTFORM show their
forms with a picture layout of FireRed's that Emerald's pictures do not fit.
The ghost of POKéMON TOWER and CHAMPION JANE's three UNOWN are not in
Emerald. The three UNOWN move like an UNOWN when they come out.

What was changed in FireRed's own code, all marked "Hän build":

- `src/pokemon.c`: `DoMonFrontSpriteAnimation`, `BattleAnimateFrontSprite`
  and `BattleAnimateBackSprite` start an animation, as in Emerald.
  `SetMultiuseSpriteTemplateToPokemon` gives a front picture its own frames.
- `src/battle_main.c`: a wild Pokémon animates once it has its colours
  (`SpriteCB_WildMonAnimate`). `SpriteCB_OpponentMonFromBall` and
  `SpriteCB_PlayerMonFromBall` animate one that came out of a ball.
  `BattleMainCB1` holds the battle's next step while an entrance animation
  runs. It gives up after ten seconds, whatever happens to a picture.
- `src/pokeball.c`: a released Pokémon gets one of those two callbacks.
- `src/battle_gfx_sfx_util.c`: `SpriteCB_WaitForBattlerBallReleaseAnim` no
  longer resets the Pokémon's picture, which would stop the animation. This
  is how Emerald has it.
- `include/pokemon_storage_system_internal.h`: the PC's picture buffer holds
  two frames. A front picture is now twice the size when unpacked, and this
  was the one buffer in the game too small for it.
- `src/data.c`, `src/graphics.c`, `ld_script.ld`, `Makefile`, `.gitignore`.

Not done: outside battles a Pokémon's picture stands still on its first
frame. In Emerald it also animates on the summary screen, in the Pokédex,
after it evolves or hatches, and in the Hall of Fame.

The game is 268 KB bigger. It uses 15.7 MB of 16 MB.

## Seven trainers changed, and a third button code

Jane asked for these on 16 and 17 November 2026.

| was | is now | picture in a battle | on the map | team |
|---|---|---|---|---|
| GIOVANNI, all three battles | the twins, with a name of Jane's | TWINS | two of Emerald's TWIN, side by side | below |
| LT. SURGE | JEM | the male PSYCHIC | the sprite the male psychics of SAFFRON's gym have | WOBBUFFET 21, SNORLAX 24, SABLEYE 21 |
| SABRINA | TERESA | SABRINA's, as it was | as it was | below |
| MISTY | MANDI | the female ace trainer (COOLTRAINER) | the female ace trainer | JOLTEON 18, FLAREON 20, VAPOREON 21 |
| KOGA | BRANDON | Emerald's STEVEN | Emerald's STEVEN | below |
| BLAINE | PROF. PAT | BLAINE's, as it was | as it was | BLAINE's, as it was |
| ERIKA | ERIKA | as it was | as it was | below |

The badges, the prizes and the TMs are as they were. JEM's and MANDI's
Pokémon have the moves of their level.

**The names in the text.** The gym signs, the gym statues, what other people
say and the FAME CHECKER say the new names:

- MISTY, LT. SURGE, SABRINA, KOGA and BLAINE were changed to MANDI, JEM,
  TERESA, BRANDON and PROF. PAT in the English source (108 places in `data/maps/*/text.inc`,
  `data/text/fame_checker.inc` and `src/strings.c`). Nothing else in those
  lines was changed, so a sign still reads "The Lightning American!", MANDI
  still speaks of WATER types and BRANDON of poison. BRANDON and PROF. PAT
  are longer than KOGA and BLAINE: in nine lines a word or two was moved
  down to the next line so that they fit.
- GIOVANNI becomes the twins' name by a word rule in the workbook (Rules
  sheet: GIOVANNI, with Jane's whole phrase). The tool puts it in 16 lines
  and lays them out again. Deleting the rule puts GIOVANNI back.
- Two small boxes of the FAME CHECKER have no room for her phrase: its list
  of names (about nine letters wide) and the label that says who spoke. Both
  show the row `GIOVANNI` in Dialogue, which still reads GIOVANNI. A short
  name typed in that row would show in both.
- The FAME CHECKER's pictures and little sprites of the five are the new
  ones (`sFameCheckerTrainerPicIdxs` and the list of sprites in
  `src/fame_checker.c` for MANDI and JEM; the twins and BRANDON get theirs
  with the pictures below).
- The twins' lines at SILPH CO. are red like their other lines
  (`textcolor` in `data/maps/SilphCo_11F/scripts.inc`).

The twins' teams. Every Pokémon holds an item and has four set moves.

| battle | team |
|---|---|
| ROCKET HIDEOUT | PICHU 24, CLEFFA 25, KANGASKHAN 29 |
| SILPH CO. | PIKACHU 37, PICHU 35, TOGEPI 35, CLEFFA 37, KANGASKHAN 41 |
| VIRIDIAN GYM | PIKACHU 45, PICHU 42, AERODACTYL 47, TOGEPI 43, CLEFFA 43, KANGASKHAN 50 |

| Pokémon | item | moves |
|---|---|---|
| PIKACHU | LIGHT BALL | THUNDER, SURF, THUNDER WAVE, QUICK ATTACK |
| PICHU | SITRUS BERRY | VOLT TACKLE, THUNDERBOLT, ENCORE, SWEET KISS |
| AERODACTYL | CHOICE BAND | ROCK SLIDE, DOUBLE-EDGE, AERIAL ACE, STEEL WING |
| TOGEPI | SITRUS BERRY | FOLLOW ME, SOFTBOILED, THUNDER WAVE, SEISMIC TOSS |
| CLEFFA | SITRUS BERRY | ENCORE, SOFTBOILED, ICE BEAM, FLAMETHROWER |
| KANGASKHAN | LEFTOVERS | FAKE OUT, BODY SLAM, BRICK BREAK, SHADOW BALL |

None of them has EARTHQUAKE, which would hit the partner in a battle of two
against two.

TERESA's team, also with items and set moves:

| Pokémon | item | moves |
|---|---|---|
| ARCANINE 38 | LEFTOVERS | FLAMETHROWER, EXTREMESPEED, CRUNCH, IRON TAIL |
| WINGULL 37, with DRIZZLE | MYSTIC WATER | SURF, ICE BEAM, SHOCK WAVE, AERIAL ACE |
| SWELLOW 38 | CHOICE BAND | AERIAL ACE, DOUBLE-EDGE, FACADE, QUICK ATTACK |
| MURKROW 38 | SHARP BEAK | DRILL PECK, SHADOW BALL, THUNDER WAVE, FAINT ATTACK |
| ALAKAZAM 43, shiny | LUM BERRY | PSYCHIC, CALM MIND, THUNDERPUNCH, ICE PUNCH |
| STANTLER 40 | SILK SCARF | DOUBLE-EDGE, EARTHQUAKE, SHADOW BALL, HYPNOSIS |

BRANDON's team. Jane gave the six sets, with natures and EVs. Every IV is 31.

| Pokémon | item | nature | EVs | moves |
|---|---|---|---|---|
| PILOSWINE 38, SNOW WARNING | NEVERMELTICE | BRAVE | 252 HP, 252 ATTACK, 4 SP. ATK | EARTHQUAKE, ICE BEAM, ROCK SLIDE, TOXIC (Jane's set had ENDURE; she changed it on 17 November 2026) |
| MIGHTYENA 39, SLUSH RUSH | LEFTOVERS | TIMID | 4 HP, 252 SP. ATK, 252 SPEED | ICE BEAM, CRUNCH, SPIKES, EXPLOSION |
| GYARADOS 40, shiny, ICE SCALES | CHESTO BERRY | MODEST | 252 HP, 4 DEFENSE, 252 SP. ATK | SURF, ICE BEAM, BODY SLAM, REST |
| STANTLER 40, SNOW CLOAK | TWISTEDSPOON | MILD | 128 ATTACK, 128 SP. ATK, 252 SPEED | RETURN, PSYCHIC, HYPNOSIS, CONFUSE RAY |
| NINETALES 41 | CHARCOAL | TIMID | 4 HP, 252 SP. ATK, 252 SPEED | FLAMETHROWER, WEATHER BALL, WILL-O-WISP, SAFEGUARD |
| URSARING 43 | SITRUS BERRY | ADAMANT | 252 HP, 252 ATTACK, 4 DEFENSE | SLASH, EARTHQUAKE, BRICK BREAK, BULK UP |

Jane first gave a GLALIE and a WALREIN, then asked for the MIGHTYENA and the
GYARADOS in their places. She gave no new sets, so the two kept the sets of
the ones they replaced.

ERIKA's team. Jane gave the six sets. Every IV is 31.

| Pokémon | item | nature | EVs | moves |
|---|---|---|---|---|
| ZIGZAGOON 24, PICKUP | ORAN BERRY | JOLLY | 4 HP, 252 ATTACK, 252 SPEED | HEADBUTT, SAND-ATTACK, PIN MISSILE, TAIL WHIP |
| SWELLOW 25, GUTS | SHARP BEAK | ADAMANT | 4 HP, 252 ATTACK, 252 SPEED | WING ATTACK, QUICK ATTACK, FOCUS ENERGY, DOUBLE TEAM |
| DIGLETT 26, ARENA TRAP | SOFT SAND | JOLLY | 4 HP, 252 ATTACK, 252 SPEED | MAGNITUDE, ROCK TOMB, MUD-SLAP, SCRATCH |
| BARBOACH 27, OBLIVIOUS | CHESTO BERRY | QUIET | 252 HP, 128 ATTACK, 128 SP. ATK | WATER PULSE, MAGNITUDE, AMNESIA, REST |
| GROWLITHE 28, INTIMIDATE | CHARCOAL | NAUGHTY | 252 ATTACK, 4 SP. ATK, 252 SPEED | FLAME WHEEL, BITE, TAKE DOWN, ROAR |
| TROPIUS 29, CHLOROPHYLL | SITRUS BERRY | MODEST | 252 HP, 4 DEFENSE, 252 SP. ATK | GIGA DRAIN, GUST, MAGICAL LEAF, SYNTHESIS |

What the leaders give now, on top of what they gave:

- **BRANDON** gives TM13 (ICE BEAM) where KOGA gave TM06 (TOXIC), and a
  fossil. The fossil's name is Jane's: the English source says `NEW ITEM 2`
  and the workbook row holds her two words. It is in an item slot that was
  unused (`ITEM_NUN_CHO_FOSSIL`), with the ROOT FOSSIL's picture. The doctor
  in the CINNABAR lab brings it back as a SWINUB with SNOW WARNING
  (`data/maps/CinnabarIsland_PokemonLab_ExperimentRoom/scripts.inc`,
  `ScriptGiveMon`). His three lines about TOXIC now speak of ICE BEAM.
- **ERIKA** gives five each of nine BERRIES after her TM: LUM, SITRUS,
  CHESTO, LEPPA, SALAC, PETAYA, LIECHI, GANLON, APICOT.
- **The twins** give an EGG after their TM in the gym, if there is a free
  place in the party. If not, they keep it and stay until the player comes
  back for it (`FLAG_GOT_TWINS_EGG`, a flag that was unused). A female
  PIKACHU that knows SURF comes out of it (`ScriptGiveEgg`). The two lines
  for it are new English rows.

Four abilities this game did not have, all in `include/constants/abilities.h`:

| ability | what it does | who has it |
|---|---|---|
| SNOW WARNING | hail when it comes out, and the hail does not stop by itself | BRANDON's PILOSWINE; the SWINUB from the fossil, and the PILOSWINE it grows into |
| SLUSH RUSH | twice the SPEED in hail | BRANDON's MIGHTYENA |
| ICE SCALES | half the damage from moves of a special type | BRANDON's GYARADOS |
| SNOW CLOAK | harder to hit in hail, and hail does not hurt it | BRANDON's STANTLER |

SNOW WARNING is the second ability of SWINUB and PILOSWINE, but one that is
caught or hatched always has the first (`CreateBoxMon`). The other three are
given to BRANDON's Pokémon only (`GetBattlerStartAbility`).

**The ability sign and the item sign.** When an ability or a held item does
something, a small sign with its name slides in, stays a moment and slides
out: a yellow stripe for an ability, a green one for an item. It is at the
top left for the foe and at the bottom left for the player; with two a side
the foes' signs are at the top right. The idea and the sliding are those of
the ability pop-up of the open-source pokeemerald-expansion project
(https://github.com/rh-hideout/pokeemerald-expansion). The code is this
build's own, at the end of `src/battle_interface.c`: the sign has no picture
file and is drawn with the game's text printer, so Hän letters and syllabics
come out right. It is shown from the end of `AbilityBattleEffects` and
`ItemBattleEffects` in `src/battle_util.c` and wherever
`src/battle_script_commands.c` notes that an ability or an item acted.

**What the four new abilities say.** Jane asked that the text box say what
an ability is doing, and that a sign come up when the ability acts, not
when its Pokémon comes out (17 November 2026). Each of the four has a line,
and its sign comes with the line. The four lines are new English rows.

| ability | when | line |
|---|---|---|
| SNOW WARNING | its Pokémon comes out | `PILOSWINE's SNOW WARNING made it hail!` (it had the line of the move HAIL) |
| SLUSH RUSH | its Pokémon comes out while it hails | `MIGHTYENA's SLUSH RUSH makes it faster in hail!` |
| SNOW CLOAK | its Pokémon comes out while it hails | `STANTLER's SNOW CLOAK hides it in the hail!` |
| ICE SCALES | each time a move of a special type has hurt its Pokémon | `GYARADOS's ICE SCALES weakened the attack!` |

SLUSH RUSH and SNOW CLOAK say their line once each time the Pokémon comes
out (`hanHailAbilityShown` in `struct DisableStruct`), and say nothing if
there is no hail then. The scripts are `BattleScript_HanHailAbilityActs`
and `BattleScript_IceScalesActs` in `data/battle_scripts_1.s`; the cases
are in `AbilityBattleEffects`.

**BRANDON takes PILOSWINE back on the first turn.** Jane asked that he
switch to another Pokémon with an ice ability once PILOSWINE has come in
and started the hail (17 November 2026). On the first turn of his battle,
if PILOSWINE is out and it hails, he switches to the first of MIGHTYENA,
GYARADOS and STANTLER that can still fight
(`ShouldSwitchBrandonsPiloswine` in `src/battle_ai_switch_items.c`). After
the first turn he switches as any trainer does.

**The FAME CHECKER is not given any more.** Jane asked for it to be taken
out (17 November 2026). The rival gave it in CERULEAN CITY after his battle
there, with two lines about it: he now leaves without it
(`data/maps/CeruleanCity/scripts.inc`). The game still keeps its notes on
famous people, but there is no item to read them with.

**A female PIKACHU has a heart-shaped tail.** `tools/han/han_emerald.py`
makes the two pictures at build time from Emerald's PIKACHU by cutting a
notch into the end of the tail (`HEART_TAIL`), and `IsHeartTailPikachu` in
`src/decompress.c` picks them. ROWAN's PIKACHU was female already.

How it is done:

- `src/data/trainers.h` and `src/data/trainer_parties.h` hold the pictures,
  the names and the teams.
- **The twins' name is Jane's.** A trainer's name holds 24 letters now, where
  it held 12 (`include/battle.h`). Her phrase is in two rows of the workbook.
  Its first word is the row `NEW CLASS` (Battle messages): the game shows it
  where it shows a trainer's class, for these three battles only
  (`IS_HAN_TWINS` in `include/battle_util.h`, used in
  `src/battle_message.c`). The rest is the row `GIOVANNI` (Trainer names). A
  third row, `GIOVANNI` in Dialogue, keeps the word GIOVANNI as it is where a
  line of text says it. Without that row the workbook would put the twins'
  name there too, because the same English gets the same Hän.
- **Two against two.** The three trainers have `.doubleBattle = TRUE`.
  `CreateNPCTrainerParty` in `src/battle_main.c` makes the battle two against
  two if the player has two Pokémon that can fight. With one, it is one
  against one: a battle of two against two cannot start with one Pokémon.
- **The PIKACHU is ROWAN's**, the one the fourth starter gives:
  `CreateRowansPikachu` in `src/script_pokemon_util.c`. It is shiny, has the
  best IVs and the 50 extra points on each stat, and its THUNDER never
  misses. That last rule is in `src/battle_script_commands.c` and now holds
  for a marked Pokémon on either side.
- **TERESA's ALAKAZAM is shiny** (`CreateNPCTrainerParty`), and **her WINGULL
  has DRIZZLE** (`GetBattlerStartAbility` in `src/battle_util.c`). No other
  WINGULL has it.
- The little sprites of JEM and MANDI are set in the `map.json` of
  `VermilionCity_Gym` and `CeruleanCity_Gym`.
- **Two twins on the map.** The little picture is the TWIN of Pokémon
  Emerald, in the place of GIOVANNI's (`gObjectEventPic_Giovanni`), with the
  colours Emerald gives it. `ViridianCity_Gym`, `RocketHideout_B4F` and
  `SilphCo_11F` each have a second twin beside the first, with the same
  script and the same flag, so talking to either starts the battle and both
  leave together. At SILPH CO. both walk up to the player
  (`SilphCo_11F_Movement_SecondTwinApproach`).
- **BRANDON's pictures are Emerald's STEVEN**, in the place of KOGA's: the
  big one for a battle (`gTrainerFrontPic_LeaderKoga`) and the little one for
  the map (`gObjectEventPic_Koga`, nine frames now).
- **These pictures are not in the patch.** `tools/han/han_emerald.py` copies
  them from the copy of the pokeemerald source at each build, as it does the
  Pokémon pictures: `emerald_twin.png`, `emerald_steven.png` and their
  colours, and `emerald_steven_front_pic.png`.
- **BRANDON's natures and EVs** are in `sBrandonTeam` in
  `src/battle_main.c`. The six are made the way CHAMPION JANE's are
  (`CreateJaneMon`), and they are as friendly as can be so that RETURN is at
  full power.
- **SNOW WARNING** is an ability this game did not have
  (`ABILITY_SNOW_WARNING`). Only BRANDON's PILOSWINE has it
  (`GetBattlerStartAbility`). When it comes out it starts to hail, with a
  line of its own, and the hail does not stop by itself, like the rain
  from DRIZZLE (`B_WEATHER_HAIL_PERMANENT`). Its name and its one line of
  description are new English rows in the workbook.

**The third button code.** Up, Down, Left, Right, Up, Select on the title
screen or on the main menu starts the twins' gym battle with the test team.
A fourth, Down, Down, Down, Down, Select, starts BRANDON's battle the same way.
It needs no save file, and the game restarts when the battle ends. The three
codes are in `sCheatCodes` in `src/main_menu.c`. The game remembers the last
six keys, and a code with five keys accepts any key before them, so the old
codes work as before. `StartCheatBattle` in `src/battle_setup.c` starts the
battle.

**CHAMPION JANE's ODDISH and SOLAR BEAM.** A trainer's Pokémon that knows
the ODDISH's own move uses SOLAR BEAM whenever the sun is out and its SP. ATK
is above normal (`WantsSolarBeam` in `src/battle_util.c`). It does not do
this against a foe SOLAR BEAM cannot hurt.

**The ODDISH's own move** (`MOVE_ODDISH_SMOKE`, `EFFECT_ODDISH_SMOKE`; its
name is Jane's and Hän only). The user hits itself: FIRE type, 40 power.
Its SPEED falls one step, its SP. ATK goes to the top, and it becomes
confused. It looks like SMOKESCREEN's smoke around itself (the move's
target is its user): `Move_ODDISH_SMOKE` in `data/battle_anim_scripts.s` is
SMOKESCREEN's script without the ball that SMOKESCREEN throws, and the
smoke is a light grey-green in place of black. No colours are added for
that: `AnimTask_OddishSmokeImpact` in `src/battle_anim_effects_3.c` mixes
the smoke's own colours toward one grey-green each time the move is used.
When the smoke has cleared, an ODDISH's eyes are red, and they stay red for
the rest of the battle. The ODDISH's picture has two pixels for eyes; they
are set to the colour of its mouth, in the copy of the picture the battle
holds in memory, so no picture is added (`HanRedOddishEyes` in
`src/battle_gfx_sfx_util.c`; the pixels' places are those of Emerald's
picture, which this build uses). If its picture is loaded again, after it
was taken back or stood behind a SUBSTITUTE, the eyes are red again if it
has used the move (it has less than all the move's PP). With battle
animations switched off in the options, the eyes change only then.
Jane asked for all of this on 17 November 2026. Before that it was GRASS
type, raised SP. ATK two steps and had a green cloud made from SMOG's; the
cloud, its colours and the script that made them (`han_green_smog.py`) are
gone.

- FIRE is super effective on an ODDISH and the sun makes it stronger, so
  the hit costs JANE's ODDISH about a third of its HP (53 of 174 in the
  test). As GRASS it cost almost nothing.
- "To the top" is a rise of six steps in the script
  (`setstatchanger STAT_SPATK, 6, FALSE`). `ChangeStatBuffs` in
  `src/battle_script_commands.c` reads six or more as "to the top from
  wherever the stat is". The game has no line for that, so it says
  `SP. ATK sharply rose!`, the line for two steps, which is translated.

**CHAMPION JANE's battle theme.** Her battle plays a tune Jane chose in
place of the ELITE FOUR's battle music (17 November 2026). It is someone
else's music, so it is in neither git nor the patch, and the zip does not
hold it. Whoever builds supplies it, as one of two files next to the
`pokefirered` folder (or with `HAN_JANE_THEME` set to the file's path):

- `jane_theme.mid`, the tune as notes. This is what Jane's game has.
  `tools/han/han_theme_midi.py` arranges it and the game's own `mid2agb`
  turns it into a song, at each build.
- `jane_theme.wav`, the tune as one recorded sound, made with
  `tools/han/han_theme_prepare.py MUSIC.mp3 ../jane_theme.wav`. The song is
  then one held note. If both files are there, the MIDI is used.

Without either the game builds all the same and her battle has the ELITE
FOUR's battle music, as it had before. `tools/han/han_theme.py` writes
`sound/songs/mus_han_jane.s`, `include/han_jane_theme.h` and the sample at
each build; none of the three is in git. The song is `MUS_HAN_JANE`,
picked in `GetBattleBGM` in `src/pokemon.c`. `ld_script.ld` lists the songs
by name, so it has a line there too.

From the MIDI (Jane's file is the whole tune, 9:08, a band of seventeen
tracks):

- Jane asked that it start "just a few verses before the famous solo". It
  starts at bar 133, the second half of the last chorus: three sung lines,
  27 seconds, then the solo. It fades in over six beats. It runs to the end
  of the MIDI, which fades out, and then comes in again from bar 133: 4:38
  each time round.
- The game plays ten tracks at most. Nine are used, in this order: the two
  solo guitars, the bass, the drum kit, the sung line (a flute), the slide
  guitar, a few extra solo notes, the strummed guitar, and the ride and
  hi-hats on the noise channel. Two more guitars that play the same chords
  as the strummed one are left out. When more notes sound than the game can
  play, it drops them from the tracks later in that order.
- The instruments are the game's own (`voicegroup250` in
  `sound/voice_groups.inc`), with the settings the game's songs use.
- Jane asked for the drums to be turned down: they are at 0.6 of what the
  MIDI says.
- **Eight sounds at once.** The game plays five sampled sounds at a time.
  While this song is the music it plays eight (`HanSetSoundChannels` in
  `src/m4a.c`), and five again as soon as any other music starts, so no
  other music is changed. Tested: with eight, the battle's first load takes
  3 frames (a twentieth of a second) longer, and after that every step of
  the battle comes at the same frame as with five.
- The volumes of the parts were set by measuring each part alone in the
  game, not by ear. See the note in `han_theme_midi.py`.
- Everything the arrangement decides is in the tables at the top of
  `han_theme_midi.py`. They are written for Jane's file and will not fit
  another.

From a recording (the first version of this theme, kept as a second way):
the file is 83 seconds from 3:21, fading in, thinned to one channel, 8
bits, 10512 samples a second so that the game stays 16 MB, turned up with a
limiter, and with the drums turned down as far as one recording allows
(`--drums`: the struck sounds are split from the held ones and mixed back
lower).

**The ice cave in the SAFARI ZONE** (Jane, 17 November 2026). The way in
is a cave mouth in the south face of the raised ground in the east area, at
(29, 12). The area's map file is not changed: the one tile is swapped when
the map loads (`SafariZone_East_OnLoad`). The cave is a new map,
`SafariZone_IceCave`, added at the end of its map group so that no other
map's number changes. It has no layout of its own: it uses the layout of
the back room of ICEFALL CAVE, with its own door, wild Pokémon and a
MIGHTYENA. Jane pointed to a picture of someone's remade SAFARI ZONE on the
web; the assistant could not open that page, so the cave does not follow
it.

- Wild Pokémon, from the teams of ERIKA, BRANDON and TERESA before they
  evolve. On the ground: SWINUB and POOCHYENA (20 in 100 each), ZIGZAGOON,
  TAILLOW, DIGLETT, TEDDIURSA (10 each), VULPIX, GROWLITHE (5 each),
  MURKROW, ABRA (4 each), STANTLER, TROPIUS (1 each). On the water:
  WINGULL, BARBOACH, MAGIKARP and, 1 in 100, GYARADOS. Fishing: MAGIKARP,
  BARBOACH, and GYARADOS with the SUPER ROD. In the SAFARI ZONE these are
  SAFARI battles, as everywhere in it.
- The MIGHTYENA stands at (12, 16), level 35. It is fought as the game's
  other standing Pokémon are, not with SAFARI BALLS. If the player wins or
  catches it, it is gone; if the player runs, it stays. It has SLUSH RUSH:
  that is MIGHTYENA's second ability now, and only this one has it
  (`CreateScriptedWildMon`; `CreateBoxMon` gives every other MIGHTYENA the
  first, as for SWINUB).
- Its picture on the map is its picture from the party list, with that
  picture's colours (`OBJ_EVENT_GFX_MIGHTYENA`). No picture is added.
- The flag is `FLAG_HIDE_SAFARI_ICE_CAVE_MIGHTYENA` (0x022, unused before).

**Which Pokémon comes next.** `GetMostSuitableMonToSwitchInto` in
`src/battle_ai_switch_items.c` is the game's own choice with two things
Jane asked for (17 November 2026): CHAMPION JANE sends the UNOWN half of
the time when one of hers has fainted, if the UNOWN can fight; BRANDON does
not send PILOSWINE while it hails, if he has another.

**The menu of boss fights** (Jane, 17 November 2026). On the title screen or
the main menu, Up, Down, Left, Right, Select opens a list of the changed
trainers by the names the game has for them: CHAMPION JANE, the twins,
BRANDON, MANDI, JEM, ERIKA, TERESA, PROF. PAT. Up and Down move, A starts
the fight with the test team, B goes back. It takes the place of the three
button codes that each started one fight. The code for syllabics (Up four
times, Select) is as it was. `CB2_InitBossMenu` in `src/main_menu.c`; the
list is `sCheatBosses` in `src/battle_setup.c`.

The test team follows the boss. Its first five take the level of the boss's
highest Pokémon minus 3 (never under 5, never over 100), and each takes the
stage of its line that fits that level: TOTODILE, CROCONAW, FERALIGATR; MAREEP,
FLAAFFY, AMPHAROS; ZUBAT, GOLBAT, CROBAT; EEVEE, ESPEON. AERODACTYL has no line.
The set of moves is given only in the last stage. MEWTWO is always level 100:
the game cannot hold more. `BossTopLevel` in `src/battle_setup.c`;
`sJaneCheatTeam` and `GiveJaneCheatTeam(bossLevel)` in `src/script_pokemon_util.c`.

**BRANDON's URSARING** (Jane, 17 November 2026). Its ability is
`ABILITY_ICE_BEARD`; its name is Jane's and Hän only (the English row is
`NEW ABILITY2`).

- Hail does not hurt it. At the end of a turn of hail it freezes, if it has
  no other trouble (`Cmd_weatherdamage`), with a line and the sign.
- It moves while frozen and does not thaw by itself. A FIRE move thaws it,
  and the next hail freezes it again. BRANDON does not use a FULL HEAL on it.
- It has what GUTS has: ATTACK is half as much again while it has any
  trouble, and a burn does not lower it.
- Its picture is not changed: it looks like any URSARING. Jane had a white
  picture and a fused picture made for it and then asked for them to be taken out.

**MANDI's six, and SYLVEON** (Jane, 17 November 2026). MANDI has EEVEE 18,
SYLVEON 21, VULPIX 19 in its rare colours, ESPEON 19, VAPOREON 20,
JOLTEON 20, each with the moves its kind knows at that level. (First it
was a NINETALES in rare colours and a FLAREON; Jane swapped them the same
day. The rare colours stayed with the fox.)

- This game has no SYLVEON. It is put in the first of the game's unused
  Pokémon places (`SPECIES_SYLVEON`, number 252), with the numbers it has
  in later games, EEVEE's cry, and a list of moves this game has. It is
  NORMAL type, as Jane asked.
- Its ability is `ABILITY_PIXILATE`: its NORMAL moves are good and bad
  against what FAIRY moves are in later games. Good against FIGHTING,
  DRAGON and DARK; weak against FIRE, POISON and STEEL; and they hit GHOST.
  The game has no FAIRY type: the six rows sit in the type table under the
  unused type `???` (`HanChartType` in `src/battle_script_commands.c`). The
  move is NORMAL in every other way.
- **Its pictures are later games' art, so they are in neither git nor the
  patch.** Whoever builds puts Jane's picture next to the `pokefirered`
  folder as `sylveon.png`; `tools/han/han_sylveon.py` makes the game's four
  files from it at each build. Without it the SYLVEON is shown as `??`.
- Nothing gives the player a SYLVEON. Its party-list picture is still `?`.

## The letter sounds of the UNOWN's move

Each letter that lands plays one letter sound, picked at random, instead of
the Bullet Seed sound. The sounds are from animalese.js by Josh Simmons,
https://github.com/Acedio/animalese.js. Its sound library `animalese.wav` is
(c) 2014 Josh Simmons, licence CC BY 4.0,
https://creativecommons.org/licenses/by/4.0/.

Changes made to it, three of them: `han_animalese.py` cuts each letter out,
resamples it to 13379 Hz, and turns it up until its loudest point is full
scale. The letters of the library are very uneven: O needs nothing, M is
turned up 6.9 times. It is one gain for a whole letter. Pitch and speed are
not changed. Six letters that are almost silent (F, S, T, V, X, Z) are left
out. The 20 others are `sound/direct_sound_samples/animalese_*.wav`.

How loud a letter is in the game, `PlayLetterSEWithPanning` in `src/sound.c`:

- The music drops to a third while a letter sounds and comes back 10 frames
  after the last letter started. The game does the same for a cry.
- With SOUND set to MONO, the setting a new game starts with, a letter plays
  in the middle at full strength on both sides. In MONO the game sends both
  sides to both speakers at half strength, so a sound on one side is only
  heard at part strength. In STEREO a letter keeps its place on the target's
  side.
- The game's mixer adds its channels with no limit. A sum past 127 wraps
  round and crackles. The battle music alone reaches 115. A letter reaches
  86 on a side and the low music 38, so there is room. Do not turn the
  letters up further, or play one on two channels, without making the music
  lower still.

Each letter is one voice in `voicegroup_animalese` (`sound/voice_groups.inc`)
and one short song in `sound/songs/se_animalese.s`. The songs are numbers
`SE_ANIMALESE_FIRST` and up. `AnimBulletSeed_Step1` in
`src/battle_anim_effects_2.c` plays them through `PlayLetterSEWithPanning`.

## Typing Hän in the source

Type the letters normally inside any `.string "..."` or `_("...")`. Precomposed
letters, combining marks, or a mix all work. The build folds a letter plus its
grave, diaeresis and ogonek into one byte. A double grave typed by accident
counts as one.

If a letter has a combination the font does not have, the build stops and names
it. Nothing is dropped silently.

## The glyphs

Each letter is one byte and one cell. Both cases exist for every form.

| | plain | grave | diaeresis | ogonek | ogonek + grave | diaeresis + grave | ogonek + diaeresis | all three |
|---|---|---|---|---|---|---|---|---|
| a | stock | stock | stock | 37 / 87 | 38 / 88 | 39 / 89 | 3A / 8A | 3B / 8B |
| e | stock | stock | stock | 3C / 8C | 3D / 8D | 3E / 8E | 3F / 8F | 40 / 90 |
| o | stock | stock | stock | 41 / 91 | 42 / 92 | 43 / 93 | 44 / 94 | 45 / 95 |
| i | stock | stock | | 46 / 96 | 47 / 97 | | | |
| u | stock | stock | | 48 / 98 | 49 / 99 | | | |

Codes are hex, lowercase / capital. Also: ł 4A, Ł 9A, ǹ 4B, Ǹ 9B, * 4C.
The modifier apostrophe ʼ uses the game's own ’ (B4).

"Stock" means the game already had the glyph.

## How the glyphs are built

- The base letter, the grave and the diaeresis are copied from the game's own
  glyphs, so weight and height match.
- The ogonek is a small hook under the letter: two pixels down, one to the right.
- A capital with both a diaeresis and a grave is one pixel shorter than a normal
  capital. Two marks do not fit above a full height capital.
- Free cells left for later: 2F to 33, 4D to 50, 5E to 67, 69 to 6E, 70 to 78,
  7D to 83, 9C to 9F.

## Changing a glyph

Either edit the PNG by hand in a pixel editor, or change the recipe in
`han_font.py` and run it again. If you edit by hand, do not run the script
afterwards, because it redraws its own cells.

Keep the four palette colours as they are: outside the letter, ink, shadow,
inside the letter.

## Screenshots

    sudo apt install libmgba-dev
    gcc -O2 -o harness tools/han/shot/harness.c -lmgba
    ./harness pokefirered.gba script.txt

A script is lines like `wait 300`, `press A 6`, `shot out.ppm`. It can also
read and set memory for tests (`peek`, `poke8`, `poke16`, `peekptr`,
`peekpath`, `pokeptr8`) and save or load a state. `press A+B` holds keys together. `reset`
restarts the game and keeps the save file, which is how to reach the main menu
in a test. `trace` prints a value each time it changes. `watch` runs one
instruction at a time until a word of memory changes and prints where the
game was, which finds the code that overwrites something. `audio out.raw`
records the game's sound (16 bit, two channels, 32768 Hz, no header).
`callson ADDR` notes the first two arguments of every call of the function
at ADDR from then on, `callsdump NAME` prints them, and `callsoff` stops.
With the address of `DecompressGlyph_HanSyllabics` that gives every glyph
the game draws in syllabics, in order. `keys A` holds a key without running
a frame.

## A note on the use of an LLM (AI assistant)

An AI assistant (Claude) wrote the scripts in this folder, the change to the
text preprocessor, and this page. It did not write any Hän. The test card is
letters only, not words. All Hän text in this project comes from Jane Coulson.
Contact: jcouls.ling@gmail.com

## The title screen (22 November 2026)

Jane asked for "Pokémon Klondike Version" and an UNOWN D where the CHARIZARD is.
Both are made at build time by `han_klondike.py` from the games' pictures, so they
are in neither git nor the patch. The letters of KLONDIKE VERSION are drawn by the
script from ten small bitmaps (it is not a font). The UNOWN D is the game's own
picture of it, on the lower right. `src/graphics.c` reads both from
`graphics/title_screen/klondike/`.

## The patcher page (22 November 2026)

`haa_firered-klondike-patcher_coulson_2026-11-22.html` is one file. Whoever plays
drops their own FireRed (US, version 1.0) and a `.bps` patch on it, and the game
is made in the browser and downloaded from it. The patch is made by
`pkg/make_bps.py SOURCE.gba TARGET.gba OUT.bps`. The page checks the game's size and
CRC32 before it patches.

## Other players on the overworld (22 November 2026)

`src/han_multiplayer.c` and `include/han_multiplayer.h`. A 76-byte block in EWRAM
(`gHanMailbox`) starts with the letters KLNDKMBX (set one letter at a time so that the
ROM itself does not hold the word). Each frame on the overworld the game writes
"mine" (map group and number, tile, facing, walking, picture) and draws "others"
(four slots) as sprites on the same map, walking towards the tile they were sent.
Nothing fills "others" unless a program writes into the emulator's memory, so the game
is the same without one. The web page in `klondike-online/` does that. Called from
`OverworldBasic` in `src/overworld.c`. EWRAM had under 1 KB free before this; about 900 bytes remain.

## The character customizer (started 22 November 2026)

Jane asked for a customizer on the boy or girl screen. Step 1 is done: `han_pok3.py` puts a
look together from the pack's layers (body, head, eyes, 30 hairs, 12 hats, tops, bottoms,
shoes, combined outfits) and recolours it as the pack's manifest does. Checked by eye on
skin tones, hairs, hats and eyes. The pack is someone else's art (Jordan Bunke, itch.io,
no licence terms on its page), so it stays out of git, the patch and the zip and goes in at
build time from the `pok3` folder. Found: the walking and standing frames use 11 to 18
colours, and a sprite has 15, so the game will need fixed rules for merging shades. Not yet
done: the screen, the saved choice, and putting the sprite together in the game.

### Quick start code (22 November 2026)

Jane asked: Select, Select, Select, Up skips to the bedroom with a randomized character and the default name. On the title screen or on the main menu this starts a new game with no Oak speech. The boy or girl is chosen at random, the name is the first one the game offers (RED for a boy, LEAF for a girl), the rival is GREEN, text speed is medium. `HanQuickStart()` in `src/main_menu.c` sets these, clears the screen registers the title screen leaves (windows, blending, sprites, palettes) and calls `CB2_NewGame`. Code row `CHEAT_QUICK_START` (3) in `include/main_menu.h`; `TitleScreenCheat` in `src/title_screen.c` returns it and the load path calls `HanQuickStart`. Only the gender is random for now; the look will be random once the customizer is in the game. Tested in the emulator from the title screen: the game starts in the bedroom. Latest ROM sha1: 58c4e2b53b3f0235b42f46eda361234614f4c0b9 (`haa_firered-han_coulson_2026-11-22.gba`).

### Ghosts on different maps, and a Restart button (22 November 2026)

Jane ran two windows: one saw the other at "map 255-255" and no ghost. The group and number in `gSaveBlock1Ptr->location` cannot be trusted (not found why; a fresh new game reads correctly). `src/han_multiplayer.c` now sends a 16-bit id made from the address of the map's event list (`gMapHeader.events`), the same for every copy of this ROM, in the two bytes that held group and number. The page's "map N-N" shows these ids now. Tested in two browsers through the server with the quick start code: the second player's ghost shows in the first one's bedroom. Two windows in one browser share one save file (same page storage); real players do not. The page has a Restart button (`Module.quickReload()`) that goes back to the title screen; before this there was no way back to it.

### Restart, refresh and syllabics in the game (22 November 2026)

Jane: Restart did not go to the title screen, a refresh should come back to the game's start and not ask for the files, and syllabics got stuck on with no way back while playing. Done: the page's Restart button now presses A, B, Start and Select together for 0.4 s (the game's own soft reset; tested: bedroom, Game Freak screen, title screen); the made game is kept in this browser's IndexedDB (`klondike-own-copy`, never uploaded) so a refresh starts it again, with the save kept in the page's storage as before (the game's own Save is still manual); "Forget my game file" deletes it; Leave goes to `?setup`, which does not start it. In the ROM, the syllabics code (Up, Up, Up, Up, Select) now also works while walking, in `HanMultiplayerFrame` (tested: off, on, off).

### Character customizer in the game (22 November 2026)

Jane asked for the customizer and a visible sign that it exists. On the boy or girl screen of Oak's speech a sign reads "LOOK" with an arrow, and a small preview of the player stands beside the menu. Press Right to open the list instead of choosing; Up and Down move the arrow to a part (look set, head, eyes, hair, hat, outfit, skin, hair colour, eye colour, colours A, B, C); A picks the part, Left and Right slide through its choices, A or B lets go; B leaves the list; A on boy or girl confirms as before. The choice is 12 bytes (`hanLook`, later 16) in the save's spare bytes (`include/global.h`). The quick start code now gives a random look as well as a random gender.

How it works: `tools/han/han_custom.py` reads the `pok3` pack (Jordan Bunke's Pokemon Gen 3 Trainer, someone else's art, never in the git patch) next to `pokefirered` and writes `src/data/han_custom_data.h`, `graphics/han_custom/body.bin` and `head.bin` (all gitignored). `src/han_custom.c` builds the player's 18 standing, walking and running frames in memory from the chosen parts (`HanCustomMake`) and a 16-colour palette; `src/event_object_movement.c` points the Red and Green normal pictures and palettes at those arrays. The heap copy is made again after every `InitHeap` (`HanCustomHeapReset` in `src/malloc.c`). Without the pack the build still works and the player keeps the game's own look.

Limits: bike, surfing, fishing and item-get pictures are still the game's own frames, so they use the original player palette (tags `OBJ_EVENT_PAL_TAG_PLAYER_RED_ORIG` and `GREEN_ORIG`). That last change only compiled and has not been seen in the emulator. Trainer pictures (battle, the big naming picture) are unchanged. Other online players show as plain trainers. Eye white, the hat mask and the brow colour (same as hair) are guesses. Labels are English and still need Hän from Jane: LOOK, HEAD, EYES, HAIR, HAT, OUTFIT, SKIN, HAIR COLOR, EYE COLOR, COLOR A, COLOR B, COLOR C, PICTURE, and the sign "LOOK" with its arrow. Tested in the emulator: the editor, the preview, quick start, standing, walking, the bedroom.

### Big pictures and the eye colours (22 November 2026)

The player's front picture (trainer card, naming, Hall of Fame, mugshot) and back picture (battle) follow the look. The first try enlarged the overworld sprite and Jane said it did not look like a battle picture, so it was dropped. Now the big pictures are the game's own trainer pictures, recoloured. A new row PICTURE (`HAN_LOOK_PIC`, byte 12 of the look, which is now 16 bytes) chooses the figure: 0 is the game's Red or Leaf, 1 to 16 are Misty, Lass, Cooltrainer F, Beauty, Erika, Lorelei, Blue (the late rival), School Kid F, Wally, Brock, Psychic M, Lt. Surge, RS May, RS Brendan, Youngster and Picnicker, whatever the player's gender. The whole figure comes with its hair style, clothes and pose; skin, hair colour and colours A, B, C recolour it (A the top, B the trousers or skirt, C shoes or bag). Jane asked for hair and clothes to be chosen separately; cutting heads off one picture and putting them on another did not work out (the heads and poses differ and the places to cut have to be found by eye), so the figures come whole.

How: `tools/han/han_custom.py` (`BIG_FRONT`, `BIG_BACK`, `BACK_OF`, `big_tables`) says which palette entries of each picture are skin, hair, A, B or C (guessed from the pictures; the shared ones are noted in the file) and writes `sHanBigFam`, `sHanBigCol`, `sHanDonor`, `sHanBackPal`, `sHanBackOf` into `src/data/han_custom_data.h` (no pictures are copied; the donors' pictures are the ones already in the game). `HanCustomPicData` in `src/han_custom.c`, called from `HanUncomp` in `src/decompress.c`, gives the donor's picture and the recoloured palette when the game loads the player's own picture or palette. The battle picture is one of the game's back pictures (Red, Leaf, RS Brendan, RS May, Pokedude) that goes with the figure (`BACK_OF`); `HanBackId` in `src/pokemon.c`'s `SetMultiuseSpriteTemplateToTrainerBack` swaps the sprite and its animation, and the palette hook follows. On the PICTURE row the editor shows the front picture beside the list (`hanPic` in `src/oak_speech.c`). Limits: only the colours of the small overworld sprite follow hair, hat and outfit; the PICTURE row does not change the small sprite. A picture's own shapes cannot be mixed. Which entry is which family is a guess. The battle pictures are 5 (4 for RS and Pokedude), so there are fewer back figures than front ones. New label to translate: PICTURE.

Eye colours are now joined last when the small sprites' colours are cut to 15 (`prot` in `HanTemp`), so a change of hair or skin colour no longer changes the eyes. Tested in the emulator: all 17 front pictures on the trainer card, all battle pictures in battle, and the editor row.


## Palette swap of any character (22 November 2026, replaces the 16 donor pictures above)

The PICTURE row now picks any of the game's own 148 trainer pictures (0 = the game's own Red or Leaf, which still uses the
skin, hair and colour A, B, C rows). The new PALETTE row (look byte 13) picks one of 12 palettes for that picture: 0 the
original, 1 to 7 red, orange, yellow, green, blue, indigo, violet, 8 black, 9 white, 10 and 11 two that suit the character
(the opposite of its main colour, and a third of the way round from each colour). Skin colours and greys are left alone,
except that black and white also darken and lighten the colourful parts.

- `tools/han/han_pics.py` reads the game's own `.4bpp.lz` and `.gbapal.lz` files and makes `graphics/han_custom/pics.bin`
  (148 pictures, uncompressed, 0x800 each, about 300 KB of ROM) and `sHanPicPal[148][12][16]` in `han_custom_data.h`.
- The battle sprite of a chosen character is its front picture (5 identical frames pointing into ROM), set through
  `HanBackImages()` in `SetMultiuseSpriteTemplateToTrainerBack`. For PICTURE 0 the Red or Leaf back picture is recoloured as before.
- `HanBackId`, the donor list and the back-picture list are gone. New label to translate: PALETTE.
- ROM used is now about 16.47 MB of 32 MB; EWRAM 99.77%.

## Follower Pokémon (22 November 2026)

The first Pokémon of the party that can still fight walks one tile behind the player (not while surfing or diving).
`src/han_follower.c` draws it as a plain sprite, like the other players in `src/han_multiplayer.c`: it blocks nothing,
cannot be talked to, is not in the save, and is made again on every map load. Pictures: `tools/han/han_follow.py`
reads the overworld pictures of pokeemerald-expansion (rh-hideout, `graphics/pokemon/<species>/overworld.png`,
other people's art, credit to that project) and writes `graphics/han_follow/sheets.bin`, `pal.bin` (normal and shiny)
and `src/data/han_follow_data.h`: 387 species, 1.2 MB of ROM, so the ROM is now about 17.7 MB. Seven big Pokémon
(STEELIX, LUGIA, HO-OH, WAILORD, KYOGRE, GROUDON, RAYQUAZA) are shrunk from 64 x 64. Frame order: south, south,
north, north, west, west (east is west turned round). Not done: talking to the follower, its ball, ledges and
stairs special cases, bike speed tuning.

## Walking picture is a palette swap too (22 November 2026)

The character editor only has PICTURE and PALETTE. The overworld (walking and running) picture is the game's own
overworld sprite for the chosen character, with the same palette swap: `OW_OF` in `tools/han/han_pics.py` names the
overworld graphics of each trainer picture (about 80 have one; the others take Youngster, or Lass for women), and
`sHanOwPal` has 12 palettes of each of the 8 overworld palettes. Bike, surfing and fishing still use the game's
own pictures and colours. Changing the look shows at once (`HanPlayerLookEnsure` runs every frame).

## Other players with their character and follower (22 November 2026)

The mailbox (`include/han_multiplayer.h`) now carries, for each player, the PICTURE, the PALETTE and the follower's
species (a player is 16 bytes, not 12: others start at byte 28). Other players on foot are drawn as the overworld
sprite of that picture in that palette, and their follower stands one tile behind them. A sprite palette is needed for
each (`LoadSpritePalette`), and only four are free on a map, so with more than about two other players the later ones
are drawn in plain colours and without a follower. The page (`klondike-online/public/index.html`) and the relay
(`server.js`) pass the three new numbers on; they have to be deployed together with this ROM.

## Trading (other players)

Face another player's character and press A: "Trade POKéMON with this player?" → pick a Pokémon → the other player is asked, picks one back → you confirm → both swap. Messages go through the mailbox (`out`/`in` in `han_multiplayer.h`), the page relays them as `trade` messages (server.js). Code: `src/han_trade.c`, `data/scripts/han_trade.inc`, specials at the end of `data/specials.inc` (they must stay *above* `gSpecialsEnd`). Tested in the emulator with faked messages only; needs a real two-browser test. If the connection drops between ACCEPT sent and received, a Pokémon can be duplicated or lost. Texts are English placeholders (Han_Trade_Text_*). Not built: trade evolutions, animation.

## Battling (other players)

Face another player, press A, say No to trading, Yes to battling. The other player is asked. Both then play the game's own single link battle (the Cable Club one: same rules, party restored afterwards), with the cable replaced by the web page.

- `src/han_link.c`: the bottom of the link. `link.c` asks it (when `gHanMailbox.link.on`) for the player number, sending a block, standby and close. Blocks (up to 256 bytes) go through `gBlockSendBuffer` / `gBlockRecvBuffer`; `struct HanLinkCtl` in `han_multiplayer.h` is the handshake with the page. `main.c` calls `HanLinkFrame()` every frame, also in battle.
- `src/han_trade.c` (HanBattle* specials) and `data/scripts/han_trade.inc` (Han_Battle_*): challenge, answer, launch, return to the field.
- Page: `pumpLink` / `gotLink` in `index.html`; relay: `lnk` messages in `server.js` (block, standby count, ready to close).
- Tested with two real emulators through the page and relay (Playwright, headless Chromium): a whole single battle, a double battle, one side leaving, and a trade.
- Trading cannot lose a Pokémon (the sender swaps first); a drop in the instant between the two swaps can duplicate one. Removing that needs a referee on the server.
- The challenger chooses single or double (double needs two Pokémon that can fight on both sides). PICTURE and PALETTE travel in `struct LinkPlayer` (`neverRead` = PIC, `progressFlagsCopy` = PAL), so the opponent is drawn as they chose (`HanLinkOppPic/Palette`, hook in `battle_controller_link_opponent.c`). Your own side shows the game's back picture in your PALETTE.
- If the other player leaves (page sets `link.gone`), `HanLinkAbortBattle()` ends the battle as a draw and closes the link.
- Not done: multi battles; the new texts are English (Hän must be written by a person).
- Bug worth remembering: copying 32 bytes into a 28 byte `struct LinkPlayer` crashed only one of the two sides. `sizeof`, always.


## Walking picture matches the chosen character

The player's walking picture follows the PICTURE row. Hoenn characters have no walking picture in FireRed, so
`tools/han/han_people.py` brings 27 from Emerald (Team Aqua and Magma members, Archie, Maxie, Wally, Wallace, the Hoenn
gym leaders and Elite Four, and others) next to the copy of pokeemerald that `han_emerald.py` already reads. Emerald's
gym leaders and Elite Four have three frames, so their walking steps are drawn from the standing frames (one foot lifts at a time).
Pictures with no Emerald match take the nearest of FireRed's own, by sex and kind (`OW_OF` and `EM_OF` in han_pics.py).
The new pictures are graphics ids 154 and up (`OBJ_EVENT_GFX_HAN_PEOPLE`, room for 40).

The walking colours are changed by the numbers of the big picture (main hue, brightness range), so PALETTE looks the
same on both. PALETTE 12 is the trans flag (light blue, pink, white; `trans_flag` in han_pics.py). The palette count is
`N_VARIANTS` there (13 now).

### Quick start: random name, picture and palette (23 November 2026)

Select, Select, Select, Up on the title screen (or main menu) starts a new game in the bedroom with a random boy or girl,
a random name (27 in `sQuickNames`, `src/main_menu.c`), a random look, and now always a random PICTURE (the game's own
Red or Leaf, or any other) and PALETTE. The walking sprite follows the picture. Tested in the emulator three times from
the title screen: different names (WREN, FINCH, EMBER), pictures and palettes each time.

### Version number on the title screen (23 November 2026)

The title screen shows "VER .67" in small white letters under KLONDIKE VERSION, so you can tell which patch you are on.
It is drawn into the logo by `tools/han/han_klondike.py` (`VERSION = "VER .67"` at the top; change that line for the next patch; it has the digits 6 and 7 and a dot, so a new digit needs a glyph added to GLYPHS).

### Customizer in the boy and girl dialog (23 November 2026)

The customizer is no longer a separate LOOK screen. The boy or girl dialog is now one window with three lines: BOY or GIRL
(Left or Right swaps it), PICTURE and PALETTE (Left or Right slide them). Up and Down move the arrow, A takes what is
shown. The chosen character stands beside the dialog in the chosen palette, and on the screens after it (the name
question) the big picture is the chosen character in its palette too (`HanOakPic` in `src/han_custom.c` puts the 64 by 64
picture into the Oak speech's 64 by 96, 256 colour tile data, at the bottom). The game's own Red or Leaf picture stays
when nothing was chosen. Code: `Task_HanBoyGirl_Input` and friends in `src/oak_speech.c`.

### Walking animation for standing pictures (23 November 2026)

FireRed's gym leaders and Elite Four (Brock, Misty, Lt. Surge, Erika, Sabrina, Blaine, Bruno, Agatha, Lance) and OLD MAN 2
have three standing frames only, so a player who chose one of them slid without moving their legs. `han_people.py` now
draws nine frames for them (the same drawing as Emerald's leaders: one foot lifts at a time and the body rises a pixel
on each step) and adds them as new walking pictures (graphics ids from 154; 37 in all of 40 places).

## 24 November 2026: cheat codes off, SYLLABICS in the OPTION menu, HMs, ROWAN

- The three button-code cheats (boss menu, syllabics, quick start) are turned off (`CheatCodeEntered` in `src/main_menu.c` returns at once).
- OPTION has an eighth row, SYLLABICS (ON/OFF). The window shows seven rows and scrolls. The choice is kept in the save
  (`optionsHanSyllabics` in `SaveBlock2`) and read again when a saved game is continued (`CB2_ContinueSavedGame`).
- A Pokémon on your team that could learn an HM counts as knowing it: `HanCanUseHM` (`src/party_menu.c`) is used by the script
  command `checkpartymove` and by `PartyHasMonWithSurf`, and the party menu lists such HMs as field moves (up to four in all).
- A player named ROWAN (or Rowan) starts a new game as a girl (the LASS picture, palette 3) in Pallet Town with eight badges, every fly point and six level 100
  Pokémon (Snorlax, Ho-Oh, Starmie, Nidoking, Aerodactyl, Chansey) with competitive Generation 3 sets (`src/han_rowan.c`, called at the end of `NewGameInitData`). The TRAINER TOWER
  is offered by every POKéMON CENTER nurse, so it needs no unlocking.
- The follower comes out of a Poké Ball as in the pack its pictures come from (pokeemerald-expansion): the ball for 9 frames,
  then the Pokémon white and squeezed thin, widening in 4 frames. It goes back in the same way when the player steps into a door,
  or if it would stand on one (`PhaseFrame` in `src/han_follower.c`). After a door or stairs it comes out only once the player is two
  tiles from the door, one tile behind her (`HanWarpDistance` in `src/field_control_avatar.c`). Crossing from route to route keeps
  it where it is, with no ball.
- Fix: ROWAN's team had wrong HP (full HP was kept in a one-byte variable; `GiveMon` in `src/han_rowan.c` now uses a `u32`).
  Anyone with a ROWAN save made before 24 November 2026 (c) can heal at a POKéMON CENTER.
- The TRAINER TOWER is offered by an attendant upstairs in every POKéMON CENTER (`Han_Tower_Attendant`, `data/scripts/han_tower.inc`),
  at any number of badges. The nurse no longer offers it. ROWAN starts with both Sevii maps on the fly map, so Seven Island can be flown to.
- HOENN, step 1: Dewford Town (outside, Pokémon Center 1F and 2F) is brought across from pokeemerald with `port_dewford.py` and
  `port_dewford_maps.py` (in the `hoenn` folder; they show how, and need pokeemerald next to pokefirered). Emerald's primary tileset is
  `gTileset_HoennGeneral`: tiles and metatiles are kept, secondary tile and metatile numbers move up by 128 (FireRed's primary has 640 tiles,
  Emerald's 512), and the 16-bit tile attributes are rewritten as FireRed's 32-bit ones (behaviour by name; doors become plain warps). Water
  does not animate yet. The ship uses the Seagallop scene: `SEAGALLOP_DEWFORD` (`src/seagallop.c`), a second sailor on the pier at Seven Island
  (Cinnabar or Dewford) and a sailor on the Dewford pier (Seven Island or Cinnabar). Dewford's other buildings have no doors yet, and its
  lines are placeholders ("Han text to come").
- HOENN, whole region (patch 24f): `hoenn/port_hoenn.py` brings every Hoenn map across from pokeemerald (289 maps, 206 layouts, 47 tilesets; it needs
  pokeemerald next to pokefirered and replaces `port_dewford*.py`). FireRed's primary tileset has 640 tiles and Emerald's 512, so Hoenn
  tilesets carry an `isHoenn` flag and `HanPrimaryTiles()`/`HanPrimaryPals()` (`include/fieldmap.h`) give the right sizes; the 16-bit tile
  attributes are rewritten as 32-bit ones by behaviour name (doors become plain warps). Water, flowers, flags, balloons and the Rustboro fountain
  animate (`gen_anim.py`, written into `src/tileset_anims.c`). Warps, connections, buildings, Pokémon Centers (FireRed's nurse and the attendant
  upstairs), signs, wild Pokémon (`wild_encounters.json`) and Poké Marts (item lists from Emerald) are all there.
  Trainers: `port_trainers.py` brings 407 Hoenn trainers (numbers from 768, `src/data/han_hoenn_trainers.h`, classes and pictures mapped to
  FireRed's own where Emerald's are missing). Kanto's flag space has no room, so their defeated flags and the eight Hoenn badges live in
  `gSaveBlock1Ptr->hanHoenn` (64 bytes that were unused; `src/han_hoenn.c`, `battle_setup.c`). The eight gym leaders give a badge there
  (`special HanHoennBadge`). All people, signs, trainer lines and place names (shown in English) are placeholders ("Han text to come") for the
  Hän to be written.
  Not done: Fly and the town map for Hoenn, the Hoenn badges on the trainer card, TMs and story events of the gyms, Hoenn story gates (Cut, Surf
  and the rest work as in FireRed), special buildings (Contest Hall, Game Corner, Battle Frontier), items on the ground, berry trees.

## 2026-11-24g
- Real Emerald trainer pictures for 14 Hoenn trainers (Juan, Wallace, Steven and others) instead of the nearest FireRed ones.
- Fly map for Hoenn: open Fly, press SELECT to switch between the Kanto map and the Hoenn map (16 towns, Emerald map picture). SELECT again goes back. All towns are unlocked for now.
- Not done yet: Hoenn badges on the trainer card, gym TMs and story events, Contest Hall / Game Corner / Battle Frontier, items on the ground, berry trees.

## 2026-11-24h
- Level caps. A gym leader (Kanto or Hoenn) will not battle you if a Pokémon in your party is over the cap for the badges you hold from that region. Kanto caps by badges 0 to 8: 14, 21, 24, 29, 43, 43, 47, 50, 100. Hoenn: 15, 19, 24, 29, 31, 33, 42, 46, 100.
- Dewford story: on your first arrival Professor Birch gives you a Treecko, Torchic or Mudkip at level 14, 10 Great Balls, and points you to the Wild Area. Placeholder English text.
- Wild Area: a field on Dewford's west shore. Common Pokémon walk about in the open; bump into one for a normal wild battle. Roaming Pokémon are drawn again every time you enter or come back from a battle.
- Gym leaders Wattson and Norman can now be battled. Every Hoenn leader gives a badge and their TM.
- Trainer card shows the Hoenn badges while you are in Hoenn.
- Items on the ground (133) and berry trees (88, as bushes that give 3 berries once; FireRed has no berry planting).
- Mauville Game Corner: the clerk gives the Coin Case, coins and slot machines work as in Celadon. Roulette and the prize counter are not done.
- Not done: Contest Hall (the building is there, contests are not), Battle Frontier, Hoenn hidden items.

## 2026-11-24i
- Hoenn people use their own Emerald walking pictures: Professor Birch, Roxanne and the other leaders, Aqua and Magma members, swimmers and so on. Before, they borrowed Kanto pictures (Birch was Prof. Oak).

## 2026-11-24j
- The Kanto fly map shows SELECT HOENN on its top bar, so the switch to the Hoenn map can be found. (The top bar window is wider; the move hint keeps its place.)

## 2026-11-24k
- A Rowan save now gets every Kanto fly town, the Sevii Islands and their maps each time it loads (`HanRowanContinue` in `src/han_rowan.c`), so an older Rowan save made before those flags existed can fly to the Sevii Islands. The seed save already had them. Hoenn fly towns need no flag.

## 2026-11-24l
- Hoenn fly towns now unlock when you stand in them (16 flags, 480 to 495 in the Hoenn flag range). The Hoenn fly map only moves between unlocked towns and A on a locked one does nothing. Rowan gets all of them, on a new game and on each load.
- Tested: the first Hoenn badge is given after beating Roxanne (level cap passes at level 12); the Hoenn trainer card shows badge pictures for the badges held.

## 2026-11-24m
- Hoenn hidden items (77 of Emerald's): face the spot and press A, as in Kanto. They use their own flags in the Hoenn range (300 to 479). A hidden item with a quantity of 127 in the map data means "a Hoenn one, quantity 1" (`GetHiddenItemAttr` in `src/field_specials.c`). Tested on Route 104.

## 2026-11-24n
- Mauville Game Corner: the two prize counters use Celadon's prize scripts (TMs, and the other prizes). The roulette tables say they are closed; Emerald's roulette is its own program and is not brought across. Placeholder English text.

## 2026-11-25a
- Battle Frontier, outside only: both outdoor areas, the reception gate, Pokémon Center, Mart, Scott's house, the lounges, the exchange corner and the ranking hall are in. The ship from Dewford has a third stop, BATTLE FRONTIER, and a sailor at the reception gate sails home. The facilities (Tower, Dome, Factory, Palace, Arena, Pike, Pyramid) are not brought across: their doors do nothing. No Battle Points yet. Placeholder English text.

## 2026-11-25b
- Rowan's team is made without a loop that could stall (the nature is built into the personality).
- A test build switch: add `#define HAN_CHEAT` to `include/han_rowan.h` and B+SELECT on the overworld becomes Rowan: whole team, all Kanto and Hoenn badges, the fly and Game Corner flags, money, coins, HMs, balls. It is off in the real build. The cheat ROM is a separate BPS, `haa_firered-han-cheat_coulson_*`, not for the web page.

## 2026-11-25e
- **Professor Birch** walks up to you on the Dewford pier (or stands next to you if the pier is too short), says hello, and opens the same choose-a-Poké-Ball screen as the start of Emerald (`src/han_starter.c`, Emerald's own pictures are copied in at build time by the Hoenn porter). Torchic, Treecko or Mudkip is yours at level 14, plus 10 Great Balls. Then he flies away on a bird. Placeholder English text.
- **The ship goes everywhere.** One list of ports for every sailor: Vermilion, One to Seven Island, Cinnabar, Dewford, Battle Frontier and the Wild Area, two pages (OTHER turns the page), the port you are standing in is left out. New sailors on Cinnabar's dock and at the Wild Area's dock; the Seven Island, Dewford and Frontier sailors use the same list. No story gate: travel is open from the start.
- **Hoenn to Kanto and Sevii.** The Hoenn fly map shows `SELECT SWITCH REGION` in the corner (SELECT already switched maps, but nothing said so); the Kanto fly map shows the same. The Sevii switch on the Kanto map is the way on to the islands, and the ship reaches all seven.
- **The Wild Area** is a snowy island (32x64, laid out like Jane's picture) in the north-east sea, where the red circle was on the Hoenn map. Winter tiles (a recoloured copy of Hoenn's tileset), falling snow, ice patches that slide you, tree ridges, a plank deck, a harbour fence with the ferry dock at the bottom (the sailor takes you to any port). No shops and no Pokémon Center. You get there by the ship, by Fly (it joins the fly map once you have stood on it), or by surfing north off the top of Route 124 (and south off the island to come back).
- **The building in the north** holds one Pokémon standing in the room: any species with a base stat total of 350 or more, drawn on the same rarity scale (350 is the likeliest, Mewtwo the rarest). Walk into it to battle. It is a new draw each time you walk in from outside, and it is gone for that visit once you have met it.
- **Walk off the east side** of the island and you come to a river bank. The river flows south (it looks like plain water; it pushes you), you need Surf to cross it, and on the far bank is a cabin with an old man. He is always ready to battle again. His team: as many Pokémon as you have (3 to 6) at the average level of yours, picked at random from the Wild Area Pokémon whose base stat total is nearest to the average total of your party.
- **Caught and party Pokémon change the odds** (roaming and building alike): a species you have caught is half as likely to show up, unless it is in your party, in which case it is four times as likely.
- **Shiny Pokémon show as shiny** on the field, and the battle is shiny too. **Rowan** now owns the SHINY CHARM (key item): shiny chance 1 in 5 for every wild Pokémon, the Wild Area's included (it is 1 in 8192 without).
- **Its Pokémon** are the ones you cannot meet in the wild in FireRed, LeafGreen or Emerald (every Kanto, Johto and Hoenn starter and its evolutions, and the rest of Gen 1-3 that only come by gift, trade, fossil or evolution, legendary and mythical ones too) plus everything those games give by fishing or surfing: 221 species. Fifteen walk about at a time, in kinds of three (a legendary or mythical one comes alone). The draw is by rarity: weight = ((720 - base stat total) / 10) squared, at least 1, so the higher the total the rarer, and none is ever impossible. A species with nothing to evolve into and a total under 350 (only Shedinja) is 5% rarer again (the full table is in wild_area_spawn_chances.csv). Walk into one to battle it; level is about your best Pokémon's.
- **The same fifteen stay** until an hour of play time has passed (the page runs in real time, so that is about an hour at the screen). Leaving the island, a battle, saving and reloading all bring the same ones back (they are kept in the save); after the hour there is a new draw. A legendary or mythical Pokémon is met once, then some other Pokémon takes its place. The one in the north building is kept the same way until you have met it.
- **Pokémon that cannot walk on land** (the fish and other swimmers, 37 species) only appear on the field in the sea south of the island, and only walk there.
- **The frozen pond** in the middle of the island is ice, and you slide across it. Boulders in it stop you. **DIG** on the ice, facing more ice, opens a hole: the tile in front turns to water. Face a hole and press A to dive, down to the sea floor: a winding way through kelp, where the Pokémon you meet are the ones that live in water, and it comes out behind the north end of the island. (Dive here is not the Emerald move: no Pokémon needs to know it, you just press A at the hole.) Holes are kept in the save.
- Fixed: Pokémon far from the player no longer show up on the other side of the screen (sprite coordinates wrap at 256).
- The Hän text for Birch, the ship menu and the Wild Area is English placeholder for now.

## 2026-11-25f
- **The north building is a cave.** The outside is a rock face with a cave mouth (Hoenn's Route 106 piece); inside is a cave room (Granite Cave's back room, cave music). The Pokémon waits in the room facing the entrance.
- **The rocks in the pond are plain rocks**, not Strength boulders: they cannot be pushed.
- **The frozen pond is bigger** (about 16 by 11 tiles, with more rocks to stop the sliding).
- **Pokémon now walk about the harbour yard** by the dock too, so some are in view when you arrive.
- **No random encounters on the sea floor.** The water Pokémon swim about down there and you meet them by walking into them, like everywhere else on the island.

## 2026-11-25g
- **Fixed: only some of the Wild Area Pokémon were drawn.** The game has only a few free sprite palettes, and a kind that did not get one was left out silently (so you might see two kinds of three and nothing else, and walk into one you could not see). Every kind now gets a palette (extra ones use unused reflection slots), so all fifteen show.
- Pokémon that are not drawn can no longer start a battle.
- Walking into a Pokémon while sliding or carried by a current also starts the battle now.

## 2026-11-25h
- **Pokémon only live where you can walk to.** At each visit the game works out which land you can reach on foot from where you stand (not behind fences, trees or water) and the walking Pokémon spawn and stay in that area, so none is out of reach.
- **Easier to touch:** a land Pokémon next to you starts the battle (before, you had to be almost on top of it), and a water Pokémon can be reached from the shore.

## 2026-11-25i
- **Cheat code for the SHINY CHARM on any save:** in the overworld, press UP, DOWN, LEFT, RIGHT, SELECT (each within a second of the last). A jingle means the charm is in the bag (key items); a buzz means you already have it or the bag is full. Rowan saves still get it by themselves.

## 2026-11-25j
- The SHINY CHARM code is now UP, DOWN, LEFT, RIGHT, SELECT (the L+R+SELECT code of 2026-11-25i is gone).

## 2026-11-25k
- **The Pokémon in the cave is gone once the battle is over** (it stayed on screen before). The next visit has a new one.
- **Sea floor:** the swimmers (20 of them) only live in the parts of the maze you can walk to, and walking into one starts the battle (checked in the emulator).

## 2026-11-25l
- Swimming Pokémon (the water-only ones, and everything on the sea floor) now float a few pixels above the ground and bob up and down, so they no longer look like they stand on it.

## 2026-11-25m
- The land Pokémon's walkable area is now worked out from several fixed points as well as from where you stand, so a bad starting spot can no longer leave the island with only water Pokémon.
- Water Pokémon now swim right up to the shore (the first row of sea), so you can start a battle from the beach without Surf.

## 2026-11-25n
- **Every kind has a spawn point.** Each kind of three starts together, a few tiles from a point picked for it, and every tile on the island is searched, so no Pokémon is dropped at spawn (all 15 spawned in the test).
- **Temperament from base stat total:** under 300 runs away from you (walking, or running two times in three); 300 to 449 is unsure, going slowly towards you or away; 450 and up comes up to you, walking or running.

## 2026-11-25o
- **The sea floor uses the same spawn points:** each kind starts together, and every tile of the maze is searched, so no swimmer is dropped (all 20 spawned in the test).

## 2026-11-25p
- **Cheat code on the START menu:** press UP, DOWN, LEFT, RIGHT, SELECT (each within a second of the last) with the start menu open. MEWTWO (level 70) joins the party (in the last place if it is full) and you are taken to the Wild Area's dock. The same code in the overworld still gives the SHINY CHARM.

## 2026-11-25q
- **The start-menu cheat sends MEWTWO (level 70) to the PC when the party is full**, instead of replacing your last Pokémon. (Rowan's team fills the party, so it goes to the PC.)

## 2026-11-25r
Checked against how the Wild Area works in Sword and Shield (symbol encounters: you only battle by touching a Pokémon; each species flees, ignores you, comes up to greet you or chases you; a Pokémon reacts only once it has noticed you; shinies look normal on the field) and tested in the emulator.
- **Pokémon notice you within 7 tiles.** Further away they wander. Inside that range: under 300 base stat total runs away (walking or running), 450 and up comes at you (walking or running), in between slowly comes, goes away or ignores you.
- Over 14 checks (about 4000 frames) all 15 Pokémon were there each time, none on a wall or tree tile, and no water Pokémon on land.
- Water Pokémon on the surface sit on the water and bob a little; on the sea floor they float higher.
- Checked in the emulator: a brave Pokémon walked up and the battle started; the cave Pokémon is gone after the battle; the sea-floor swimmers can be touched.

## 2026-11-25s
- **A new game named TEST** (or Test, or test) starts at the Wild Area dock with a level 100 MEWTWO. Any other name starts as before. `HanTestStart` in `src/han_rowan.c`, called from `NewGameInitData` in `src/new_game.c`.

## 2026-11-25t
The Wild Area's spawning, rebuilt from first principles. What was wrong, found from the game itself:
- Only 2 sprite palettes are free on the island (FireRed keeps 0-11 for people and their reflections; snow and the follower take 12 and 13). The old fallback put two kinds on one borrowed palette, so Pokémon showed in each other's colours, and kinds with no palette never appeared.
- Species with no overworld picture were drawn into the roster and then skipped.
- Entering froze for 25-50 seconds: each spawn flood-filled the map, and each species pick read (decrypted) the whole party once per species.

How it works now:
- **Land and sea from the map.** `hoenn/wildtiles/classify.py` reads `data/layouts/HanWildArea/map.bin` and the tilesets and writes `src/data/han_wild_tiles.h`: 672 land tiles (snow reachable from the dock, crossing the ice; no ice, trees, fences, lake or ledges) and 232 sea tiles. Run it again if the map changes.
- **Each roster slot is land or sea for good**: slots 0-7 are four land kinds (two each), slots 8-14 four sea kinds (the last alone). A land slot only draws land species and only steps on land; a sea slot only sea. Only species with a picture are drawn.
- **Home grounds.** Each kind lives around its own spot, apart from the others, and wanders up to 7 tiles from it. Two Pokémon never share a tile.
- **Palettes.** The Pokémon use sprite palettes 4, 8, 10 and 11 (people none of the wild maps has), and one free palette when two are free. The kinds nearest the player get them; a kind far off the screen gives its palette back. A palette that anything else is using is skipped.
- **Walking into a Pokémon starts the battle**: you step onto its tile, it steps onto yours, or you push against a sea Pokémon from the shore. Standing next to one does nothing.
- **After a battle** the one you met is replaced by another species of the same class, away from you; the rest come back where they were.
- Tested in the emulator: entering takes the usual fade (about 90 frames, was 1500-3000); 540 checks of all 15 Pokémon with none on the wrong ground or stacked; all five touch cases right; Psyduck met and run from, Elekid took its place; temple and sea floor still spawn; the TEST start lands at the dock with MEWTWO at level 100.

## 2026-11-26a
Jane's game (25t) had no Pokémon in sight. Her ROM was exactly the 25t build and the Pokémon were there, but only 8 land ones in 4 herds, so most of the island had none near. Now, as in Sword and Shield's Wild Area:
- **Pokémon appear around you as you go**, just off the screen, and go when they are far behind. Up to 7 on land and 3 in the sea are out at once; a few are put near you when you arrive.
- **More species**: each draw has 11 that live on land and 4 that live in the sea, all different (was 4 and 4). New draw every hour of play, as before.
- Meeting one sends its species off the island and brings another of the same class (land or sea) in its place.
- A roster saved by an older patch is drawn again on the new layout.
- Tested in the emulator from the island's east edge (where Jane was): 4 out on arrival, 7 within seconds, 2-5 on the screen while walking; none ever on the wrong ground; walking into one started the battle; after running away the others were back where they were and the met species was gone. Temple and sea floor unchanged.

## 2026-11-26b
- **Spread over the whole island.** The Pokémon are spread over all the land and all the sea, apart from each other, not only near the player: 10 on land and 4 in the sea, 14 at most.
- **Always some in the sea**: never fewer than 4.
- **None in sight**: when none is on the screen or near it, one appears just off the screen; the next such one waits 5 seconds. With 14 out, the one farthest away makes room (never taking the sea below 4).
- A gap left by a battle is filled again off the screen, one every 1.5 seconds.
- Each new one's species is chosen so that no part of the island has more than 4 species close together, so every one in view can be drawn.
- Tested: 14 out spread from row 7 to the sea, 4 in the sea throughout; walking from the east edge, at most a few seconds with none in view; none ever on the wrong ground; after a battle the rest came back where they were.

## 2026-11-26c
Jane at the dock (26b) saw only sea Pokémon: the old rule put one near only when none at all was near, and the sea ones counted.
- **Always some near**: at least 3 Pokémon within about 15 tiles across or 10 up and down of the player, and at least 1 of them on land wherever there is land about. Short of that, one appears just off the screen every 2 seconds until there are enough (the one farthest away makes room when 14 are out; the sea keeps 4).
- Tested: standing at the dock, 3-4 near (1-2 on land) the whole time; walking from the dock and from the east edge, never fewer than 3 near and never without land ones, until walking into one started a battle.
