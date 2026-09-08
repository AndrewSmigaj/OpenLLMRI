"""File-based help entries (Evennia reads `HELP_ENTRY_DICTS`). The taught grammar and the verb families —
they teach FORMS, never solutions (the hinting policy, ontology-closure.md §5). Tunable content."""

HELP_ENTRY_DICTS = [
    {
        "key": "grammar",
        "aliases": ["commands", "syntax", "how", "howto", "how to play"],
        "category": "Interaction",
        "text": """
            Everything you do is one physical act, in one line:

                VERB thing
                VERB thing WITH tool
                VERB thing RELATION thing [WITH tool]
                VERB thing INTO form [WITH tool]
                GO place

            Examples: 'cut the cover off the seat with the multitool' · 'put the branch on the fire'
            · 'tie the paracord to the frame' · 'carve the branch into a spindle with the knife'
            · 'search the duffel' · 'take the wire from the panel' · 'go to the cockpit'.

            State the ACT, not the aim. 'shake thermos' — not 'shake the thermos to see if there is
            coffee in it'. The world answers physically either way; it never needs to know why.

            Name things the way the room names them ('examine <thing>' shows what you can name,
            including its PARTS: 'cut the seat's cover'). Two of a kind? Add the label ('11b') or
            answer the numbered question.

            'use X on Y' works — the game tells you which verb it did, so next time you can say it.
            'make fire' tells you what a fire is made of; the steps are yours to find.

            # subtopics

            ## relations
            off · from · on · onto · into · in · to · against · between · under · around · over ·
            through · behind · beside. Two-object acts are first-class: 'wedge the seat against the
            door', 'tie the strap between the pole and the tree'.

            ## tools
            'with' or 'using' names the tool. Bare hands are the default. Anything with an edge
            cuts; anything rigid and long levers; anything long and flexible ties.

            ## when it doesn't understand
            An unknown verb gets a nudge naming close ones. A thing it can't see gets 'you don't see
            that here' — examine, search, open, or move closer. A verb that doesn't fit a thing gets
            the physics of why.
        """,
    },
    {
        "key": "verbs",
        "aliases": ["verb", "actions", "verb list"],
        "category": "Interaction",
        "text": """
            The verb families (each verb has everyday synonyms; say it your way):

            cutting & shaping — cut, tear, break, bend, pry (carve, split, notch: coming)
            fire — light, burn, melt, douse
            binding & covering — tie, wrap, put, cover
            moving & carrying — take, put, go, open, close, search, dig
            body & senses — examine, eat, drink, wear, remove, read
            social — say, whisper, call, shout, talk to

            Anything that fits the grammar and is physically sensible resolves — by the materials
            involved, not by a list of allowed pairs. Try the desperate thing; you'll be told why.
        """,
    },
]
