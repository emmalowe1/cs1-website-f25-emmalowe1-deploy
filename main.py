drafter import *
from bakery import assert_equal
from dataclasses import dataclass

FIELD_IMG  = "https://raw.githubusercontent.com/emmalowe1/finalproject/main/images/field.png"
CAVE_IMG = "https://raw.githubusercontent.com/emmalowe1/finalproject/main/images/cavecave.png"
WOODS_IMG = "https://raw.githubusercontent.com/emmalowe1/finalproject/main/images/woodswoods.png"
VICTORY_IMG = "https://raw.githubusercontent.com/emmalowe1/finalproject/main/images/victoryfortheOGs.png"

set_website_style("sakura")
add_website_css("body", "background-color: #ffd6e7;")
add_website_css("body", "color: #d63384;")

set_site_information(
    author="emmalowe@udel.edu",
    description="""My website is an adventure game. You start in a field and then 
    are given the choice to go into a cave or the woods. If you go to the cave, you see a locked door
    that requires a key. You go back to the field to go to the woods and get the key so you can 
    unlock the treasure.""",
    sources=["None"]
    planning=["planning doc.pdf"],
    links=["https://github.com/UD-F25-CS1/cs1-website-f25-emmalowe1"]
)
hide_debug_information()
set_website_title("Find The Secret Treasure!")
set_website_framed(False)

@dataclass
class State:
    name: str = ""
    has_key: bool = False
    inventory: list[str] = None 

@route
def index(state: State) -> Page:
    return Page(
        state=state,
        content=[
            "Welcome to the adventure! What is your name?",
            TextBox(name="name", kind="text", default_value="Adventurer"),
            Button(text="Begin", url="/begin"),
        ],
    )

@route
def begin(state: State, name: str) -> Page:
    s = State(name=name.strip() or "Adventurer", has_key=False)
    return Page(
        state=s,
        content=[
            f"You are {s.name}.",
            "You are in a small field.",
            "You see paths to the woods and a cave.",
            Button(text="Cave", url="/cave"),
            Button(text="Woods", url="/woods"),
            Image(url=FIELD_IMG, width=None, height=None),
        ],
    )

@route
def small_field(state: State) -> Page:
    return Page(
        state=state,
        content=[
            f"You are {state.name}.",
            "You are in a small field.",
            "You see paths to the woods and a cave.",
            Button(text="Cave", url="/cave"),
            Button(text="Woods", url="/woods"),
            Image(url=FIELD_IMG, width=None, height=None),
        ],
    )

@route
def cave(state: State) -> Page:
    items = [
        "You enter the cave.",
        "You see a locked door. You need a key to unlock it",
    ]
    if state.has_key:
        items.append(Button(text="Unlock door", url="/ending"))
    items += [
        Button(text="Leave", url="/small_field"),
        Image(url=CAVE_IMG, width=None, height=None),
    ]
    return Page(state=state, content=items)

@route
def woods(state: State) -> Page:
    items = ["You are in the woods."]
    if not state.has_key:
        items += [
            "You see a key on the ground.",
            Button(text="Take key", url="/take_key"),
        ]
    items += [
        Button(text="Leave", url="/small_field"),
        Image(url=WOODS_IMG, width=None, height=None),
    ]
    return Page(state=state, content=items)

@route
def take_key(state: State) -> Page:
    s = State(name=state.name, has_key=True)
    return Page(
        state=s,
        content=[
            "You are in the woods.",
            Button(text="Leave", url="/small_field"),
            Image(url=WOODS_IMG, width=None, height=None),
        ],
    )

@route
def ending(state: State) -> Page:
    return Page(
        state=state,
        content=[
            "You unlock the door.",
            "You find a treasure chest.",
            "You win!",
            Image(url=VICTORY_IMG, width=None, height=None),
            Button(text="Play again", url="/"),
        ],
    )

assert_equal(
    index(State()),
    Page(
        state=State(),
        content=[
            "Welcome to the adventure! What is your name?",
            TextBox(name="name", kind="text", default_value="Adventurer"),
            Button(text="Begin", url="/begin"),
        ],
    ),
)

assert_equal(
    begin(State(), "Ada"),
    Page(
        state=State(name="Ada", has_key=False),
        content=[
            "You are Ada.",
            "You are in a small field.",
            "You see paths to the woods and a cave.",
            Button(text="Cave", url="/cave"),
            Button(text="Woods", url="/woods"),
            Image(url=FIELD_IMG, width=None, height=None),
        ],
    ),
)

assert_equal(
    small_field(State(name="Ada", has_key=True)),
    Page(
        state=State(name="Ada", has_key=True),
        content=[
            "You are Ada.",
            "You are in a small field.",
            "You see paths to the woods and a cave.",
            Button(text="Cave", url="/cave"),
            Button(text="Woods", url="/woods"),
            Image(url=FIELD_IMG, width=None, height=None),
        ],
    ),
)

assert_equal(
    woods(State(name="Ada", has_key=False)),
    Page(
        state=State(name="Ada", has_key=False),
        content=[
            "You are in the woods.",
            "You see a key on the ground.",
            Button(text="Take key", url="/take_key"),
            Button(text="Leave", url="/small_field"),
            Image(url=WOODS_IMG, width=None, height=None),
        ],
    ),
)

assert_equal(
    woods(State(name="Ada", has_key=True)),
    Page(
        state=State(name="Ada", has_key=True),
        content=[
            "You are in the woods.",
            Button(text="Leave", url="/small_field"),
            Image(url=WOODS_IMG, width=None, height=None),
        ],
    ),
)

assert_equal(
    take_key(State(name="Ada", has_key=False)),
    Page(
        state=State(name="Ada", has_key=True),
        content=[
            "You are in the woods.",
            Button(text="Leave", url="/small_field"),
            Image(url=WOODS_IMG, width=None, height=None),
        ],
    ),
)

assert_equal(
    cave(State(name="Ada", has_key=False)),
    Page(
        state=State(name="Ada", has_key=False),
        content=[
            "You enter the cave.",
            "You see a locked door.",
            Button(text="Leave", url="/small_field"),
            Image(url=CAVE_IMG, width=None, height=None),
        ],
    ),
)

assert_equal(
    cave(State(name="Ada", has_key=True)),
    Page(
        state=State(name="Ada", has_key=True),
        content=[
            "You enter the cave.",
            "You see a locked door.",
            Button(text="Unlock door", url="/ending"),
            Button(text="Leave", url="/small_field"),
            Image(url=CAVE_IMG, width=None, height=None),
        ],
    ),
)

assert_equal(
    ending(State(name="Ada", has_key=True)),
    Page(
        state=State(name="Ada", has_key=True),
        content=[
            "You unlock the door.",
            "You find a treasure chest.",
            "You win!",
            Image(url=VICTORY_IMG, width=None, height=None),
            Button(text="Play again", url="/"),
        ],
    ),
)

start_server(State())
