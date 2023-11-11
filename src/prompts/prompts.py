SYSTEM_MESSAGE_BASE_V1 = """You are playing a game. You will be provided with a group of words. There are several groups of 4 words each that share a common theme / category. List each group of 4 words with their associated theme in order of confidence.

Examples of groupings:
- Fish: Bass, Flounder, Salmon, Trout
- Fire _: Ant, Drill, Island, Opal
- Fruit Homophones: Lyme, Mellon, Pair, Plumb
- Publications: Journal, Globe, Post, Asteroid
- Synonyms For Falsehood: Fib, Fiction, Lie, Tale
- Candy Pieces: Dot, Goober, Kiss, Whopper
- Rappers Minus Numbers: Cent, Chainz, Pac, Savage
- Touchscreen Gestures: Pinch, Spread, Swipe, Tap

Each word can only be in one grouping, and each grouping must have 4 words exactly. The grouping cannot have a theme like "Random words", "General terms" or "Unrelated words", they must be connected in some way. 
"""

SYSTEM_MESSAGE_BASE_V2 = """Find 4 groups, each of 4 words that share something in common, out of 16 words. I want to use them to solve a daily word puzzle that finds commanalities between words. The game is a new puzzle featured in The New York Times, inspired by crosswords. You have to use all those 16 words I give you and each word only once.

Examples of groupings:
- Fish: Bass, Flounder, Salmon, Trout
- Fire _: Ant, Drill, Island, Opal
- Fruit Homophones: Lyme, Mellon, Pair, Plumb
- Publications: Journal, Globe, Post, Asteroid
- Synonyms For Falsehood: Fib, Fiction, Lie, Tale
- Candy Pieces: Dot, Goober, Kiss, Whopper
- Rappers Minus Numbers: Cent, Chainz, Pac, Savage
- Touchscreen Gestures: Pinch, Spread, Swipe, Tap

Each word can only be in one grouping, and each grouping must have 4 words exactly. The grouping cannot have a theme like "Random words", "General terms" or "Unrelated words", they must be connected in some way. 
"""
