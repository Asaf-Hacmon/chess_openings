"""
Chess openings database as move trees.
Each node: { "move": UCI, "san": SAN, "name": str, "comment": str,
             "popularity": int (% of games, only on multi-branch siblings),
             "children": [...] }
"""

OPENINGS = {
    "Ruy Lopez": {
        "description": "One of the oldest and most respected openings. White attacks Black's e5 defender immediately.",
        "color": "white",
        "tree": {
            "move": None,
            "san": None,
            "name": "Start",
            "comment": "Ruy Lopez begins with 1.e4 e5 2.Nf3 Nc6 3.Bb5",
            "children": [
                {
                    "move": "e2e4",
                    "san": "e4",
                    "name": "1. e4",
                    "comment": "King's pawn opening — controls the center and opens lines for the bishop and queen.",
                    "children": [
                        {
                            "move": "e7e5",
                            "san": "e5",
                            "name": "1...e5",
                            "comment": "Black mirrors White, fighting for central control.",
                            "children": [
                                {
                                    "move": "g1f3",
                                    "san": "Nf3",
                                    "name": "2. Nf3",
                                    "comment": "Develops the knight and attacks e5, forcing Black to defend.",
                                    "children": [
                                        {
                                            "move": "b8c6",
                                            "san": "Nc6",
                                            "name": "2...Nc6",
                                            "comment": "The natural defender of e5.",
                                            "children": [
                                                {
                                                    "move": "f1b5",
                                                    "san": "Bb5",
                                                    "name": "3. Bb5 — Ruy Lopez",
                                                    "comment": "The Ruy Lopez! White pins the Nc6 which defends e5, indirectly pressuring e5.",
                                                    "children": [
                                                        {
                                                            "move": "a7a6",
                                                            "san": "a6",
                                                            "name": "3...a6 — Morphy Defense",
                                                            "popularity": 65,
                                                            "comment": "The most popular response. Black kicks the bishop, forcing White to decide its fate.",
                                                            "children": [
                                                                {
                                                                    "move": "b5a4",
                                                                    "san": "Ba4",
                                                                    "name": "4. Ba4",
                                                                    "comment": "White retreats to maintain the pin. Taking on c6 would give Black the bishop pair.",
                                                                    "children": [
                                                                        {
                                                                            "move": "g8f6",
                                                                            "san": "Nf6",
                                                                            "name": "4...Nf6",
                                                                            "comment": "Black develops and attacks e4.",
                                                                            "children": [
                                                                                {
                                                                                    "move": "e1g1",
                                                                                    "san": "O-O",
                                                                                    "name": "5. O-O",
                                                                                    "comment": "White castles to safety, preparing the Ruy Lopez main line.",
                                                                                    "children": [
                                                                                        {
                                                                                            "move": "f8e7",
                                                                                            "san": "Be7",
                                                                                            "name": "5...Be7 — Closed Ruy Lopez",
                                                                                            "popularity": 60,
                                                                                            "comment": "Solid development, preparing to castle. This leads to the rich Closed Ruy Lopez.",
                                                                                            "children": [
                                                                                                {
                                                                                                    "move": "f1e1",
                                                                                                    "san": "Re1",
                                                                                                    "name": "6. Re1",
                                                                                                    "comment": "Supports e4 and prepares central action.",
                                                                                                    "children": [
                                                                                                        {
                                                                                                            "move": "b7b5",
                                                                                                            "san": "b5",
                                                                                                            "name": "6...b5",
                                                                                                            "comment": "Black gains space on the queenside.",
                                                                                                            "children": [
                                                                                                                {
                                                                                                                    "move": "a4b3",
                                                                                                                    "san": "Bb3",
                                                                                                                    "name": "7. Bb3",
                                                                                                                    "comment": "The bishop retreats to the strong b3 square.",
                                                                                                                    "children": []
                                                                                                                }
                                                                                                            ]
                                                                                                        }
                                                                                                    ]
                                                                                                }
                                                                                            ]
                                                                                        },
                                                                                        {
                                                                                            "move": "f6e4",
                                                                                            "san": "Nxe4",
                                                                                            "name": "5...Nxe4 — Berlin Defense",
                                                                                            "popularity": 40,
                                                                                            "comment": "The Berlin! Black takes the pawn. This leads to the 'Berlin Wall' — a solid, drawish endgame favored by top players.",
                                                                                            "children": [
                                                                                                {
                                                                                                    "move": "d1e2",
                                                                                                    "san": "Re1",
                                                                                                    "name": "6. Re1",
                                                                                                    "comment": "Attacking the knight and e5 simultaneously.",
                                                                                                    "children": [
                                                                                                        {
                                                                                                            "move": "e4f6",
                                                                                                            "san": "Nf6",
                                                                                                            "name": "6...Nf6",
                                                                                                            "comment": "Retreating the knight. The Berlin endgame begins.",
                                                                                                            "children": []
                                                                                                        }
                                                                                                    ]
                                                                                                }
                                                                                            ]
                                                                                        }
                                                                                    ]
                                                                                }
                                                                            ]
                                                                        }
                                                                    ]
                                                                }
                                                            ]
                                                        },
                                                        {
                                                            "move": "g8f6",
                                                            "san": "Nf6",
                                                            "name": "3...Nf6 — Berlin Defense",
                                                            "popularity": 25,
                                                            "comment": "The Berlin Defense — immediately developing and counter-attacking e4.",
                                                            "children": [
                                                                {
                                                                    "move": "e1g1",
                                                                    "san": "O-O",
                                                                    "name": "4. O-O",
                                                                    "comment": "White castles, daring Black to take e4.",
                                                                    "children": [
                                                                        {
                                                                            "move": "f6e4",
                                                                            "san": "Nxe4",
                                                                            "name": "4...Nxe4",
                                                                            "comment": "Black accepts the pawn. Now the Berlin endgame can arise.",
                                                                            "children": []
                                                                        }
                                                                    ]
                                                                }
                                                            ]
                                                        },
                                                        {
                                                            "move": "f8c5",
                                                            "san": "Bc5",
                                                            "name": "3...Bc5 — Classical Defense",
                                                            "popularity": 10,
                                                            "comment": "Classical! Black develops the bishop to its most active square, ignoring the pin.",
                                                            "children": [
                                                                {
                                                                    "move": "c2c3",
                                                                    "san": "c3",
                                                                    "name": "4. c3",
                                                                    "comment": "White prepares d4, pushing for the center.",
                                                                    "children": [
                                                                        {
                                                                            "move": "g8f6",
                                                                            "san": "Nf6",
                                                                            "name": "4...Nf6",
                                                                            "comment": "Black develops with tempo, attacking e4.",
                                                                            "children": []
                                                                        }
                                                                    ]
                                                                },
                                                                {
                                                                    "move": "b5c6",
                                                                    "san": "Bxc6!",
                                                                    "name": "4.Bxc6! — Classical Defense Trap",
                                                                    "trap": True,
                                                                    "trap_name": "The Classical Defense Trap",
                                                                    "trap_description": "Trading bishop for knight destroys Black's pawn cover AND wins the e5 pawn immediately!",
                                                                    "comment": "TRAP! 4.Bxc6! looks anti-positional but is crushing. After 4...dxc6, the Nc6 that was defending e5 is gone — White wins a FREE PAWN with 5.Nxe5! If Black tries 5...Bxf2+? 6.Kxf2 Qd4+ 7.Ke3! the king escapes and White keeps the extra pawn.",
                                                                    "children": [
                                                                        {
                                                                            "move": "d7c6",
                                                                            "san": "dxc6",
                                                                            "name": "4...dxc6 (forced)",
                                                                            "comment": "Black must recapture. The pawn structure is ruined and e5 is now hanging...",
                                                                            "children": [
                                                                                {
                                                                                    "move": "f3e5",
                                                                                    "san": "Nxe5!",
                                                                                    "name": "5.Nxe5! — Winning a free pawn!",
                                                                                    "comment": "White wins a free pawn with no compensation for Black. The Nc6 that defended e5 was traded away on move 4. White is up a pawn with the more solid pawn structure.",
                                                                                    "children": []
                                                                                }
                                                                            ]
                                                                        }
                                                                    ]
                                                                }
                                                            ]
                                                        }
                                                    ]
                                                }
                                            ]
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        }
    },

    "Sicilian Defense": {
        "description": "The most popular response to 1.e4. Black fights for the center asymmetrically, leading to rich, complex positions.",
        "color": "black",
        "tree": {
            "move": None,
            "san": None,
            "name": "Start",
            "comment": "The Sicilian is the most played opening at all levels.",
            "children": [
                {
                    "move": "e2e4",
                    "san": "e4",
                    "name": "1. e4",
                    "comment": "White occupies the center.",
                    "children": [
                        {
                            "move": "c7c5",
                            "san": "c5",
                            "name": "1...c5 — Sicilian Defense",
                            "comment": "The Sicilian! Black fights for d4 without mirroring e5, creating an asymmetry.",
                            "children": [
                                {
                                    "move": "g1f3",
                                    "san": "Nf3",
                                    "name": "2. Nf3",
                                    "comment": "The most common. White prepares d4.",
                                    "children": [
                                        {
                                            "move": "d7d6",
                                            "san": "d6",
                                            "name": "2...d6",
                                            "comment": "Preparing Nf6 without allowing e5.",
                                            "children": [
                                                {
                                                    "move": "d2d4",
                                                    "san": "d4",
                                                    "name": "3. d4",
                                                    "comment": "The Open Sicilian — White opens the center.",
                                                    "children": [
                                                        {
                                                            "move": "c5d4",
                                                            "san": "cxd4",
                                                            "name": "3...cxd4",
                                                            "comment": "Black trades to open the c-file.",
                                                            "children": [
                                                                {
                                                                    "move": "f3d4",
                                                                    "san": "Nxd4",
                                                                    "name": "4. Nxd4",
                                                                    "comment": "White recaptures, centralizing the knight.",
                                                                    "children": [
                                                                        {
                                                                            "move": "g8f6",
                                                                            "san": "Nf6",
                                                                            "name": "4...Nf6",
                                                                            "comment": "Develops and attacks e4.",
                                                                            "children": [
                                                                                {
                                                                                    "move": "b1c3",
                                                                                    "san": "Nc3",
                                                                                    "name": "5. Nc3",
                                                                                    "comment": "Defends e4 and develops.",
                                                                                    "children": [
                                                                                        {
                                                                                            "move": "a7a6",
                                                                                            "san": "a6",
                                                                                            "name": "5...a6 — Najdorf Variation",
                                                                                            "comment": "The Najdorf! Prevents Nb5 and prepares b5. The most popular Sicilian variation, favored by Fischer and Kasparov.",
                                                                                            "children": [
                                                                                                {
                                                                                                    "move": "c1e3",
                                                                                                    "san": "Be3",
                                                                                                    "name": "6. Be3 — English Attack",
                                                                                                    "comment": "The English Attack — preparing f3 and g4 for a kingside attack.",
                                                                                                    "children": [
                                                                                                        {
                                                                                                            "move": "e7e5",
                                                                                                            "san": "e5",
                                                                                                            "name": "6...e5",
                                                                                                            "comment": "Black stakes out space in the center, kicking the Nd4.",
                                                                                                            "children": []
                                                                                                        },
                                                                                                        {
                                                                                                            "move": "d8b6",
                                                                                                            "san": "Qb6",
                                                                                                            "name": "6...Qb6 — The Poisoned Pawn",
                                                                                                            "trap": True,
                                                                                                            "trap_name": "The Poisoned Pawn",
                                                                                                            "trap_description": "Attack b2 AND d4 at once! If White defends poorly, you grab a free pawn with Qxb2.",
                                                                                                            "comment": "TRAP — The Poisoned Pawn! Qb6 attacks both the b2 pawn and the Nd4 simultaneously. This was Kasparov's and Fischer's favorite weapon. If White retreats the knight with 7.Nb3?, you play 7...Qxb2! and escape with a free pawn. White gets attacking chances but Black has the material edge.",
                                                                                                            "children": [
                                                                                                                {
                                                                                                                    "move": "d4b3",
                                                                                                                    "san": "Nb3",
                                                                                                                    "name": "7.Nb3 — Defending badly",
                                                                                                                    "comment": "White retreats the knight but leaves b2 hanging...",
                                                                                                                    "children": [
                                                                                                                        {
                                                                                                                            "move": "b6b2",
                                                                                                                            "san": "Qxb2!",
                                                                                                                            "name": "7...Qxb2! — The pawn is poisoned!",
                                                                                                                            "comment": "Black grabs the pawn! After 8.Nd5 Qa3! 9.Nxf6+ Nxf6 10.Rb1 Black has won a pawn and maintains active piece play. White gets compensation but Black has the material edge.",
                                                                                                                            "children": []
                                                                                                                        }
                                                                                                                    ]
                                                                                                                }
                                                                                                            ]
                                                                                                        }
                                                                                                    ]
                                                                                                }
                                                                                            ]
                                                                                        },
                                                                                        {
                                                                                            "move": "g7g6",
                                                                                            "san": "g6",
                                                                                            "name": "5...g6 — Dragon Variation",
                                                                                            "comment": "The Dragon! Black fianchettoes the bishop, creating a powerful diagonal toward h1.",
                                                                                            "children": [
                                                                                                {
                                                                                                    "move": "c1e3",
                                                                                                    "san": "Be3",
                                                                                                    "name": "6. Be3",
                                                                                                    "comment": "White prepares the Yugoslav Attack.",
                                                                                                    "children": [
                                                                                                        {
                                                                                                            "move": "f8g7",
                                                                                                            "san": "Bg7",
                                                                                                            "name": "6...Bg7",
                                                                                                            "comment": "The Dragon bishop — the key piece of Black's position.",
                                                                                                            "children": []
                                                                                                        }
                                                                                                    ]
                                                                                                }
                                                                                            ]
                                                                                        },
                                                                                        {
                                                                                            "move": "e7e6",
                                                                                            "san": "e6",
                                                                                            "name": "5...e6 — Scheveningen Variation",
                                                                                            "comment": "The Scheveningen — solid and flexible. Black forms a small center with d6+e6.",
                                                                                            "children": [
                                                                                                {
                                                                                                    "move": "g2g4",
                                                                                                    "san": "g4",
                                                                                                    "name": "6. g4 — Keres Attack",
                                                                                                    "comment": "The Keres Attack — White launches an immediate kingside pawn storm!",
                                                                                                    "children": [
                                                                                                        {
                                                                                                            "move": "h7h6",
                                                                                                            "san": "h6",
                                                                                                            "name": "6...h6",
                                                                                                            "comment": "Black slows the g-pawn advance.",
                                                                                                            "children": []
                                                                                                        }
                                                                                                    ]
                                                                                                }
                                                                                            ]
                                                                                        }
                                                                                    ]
                                                                                }
                                                                            ]
                                                                        }
                                                                    ]
                                                                }
                                                            ]
                                                        }
                                                    ]
                                                }
                                            ]
                                        },
                                        {
                                            "move": "b8c6",
                                            "san": "Nc6",
                                            "name": "2...Nc6",
                                            "comment": "Developing the knight, heading toward the Sveshnikov or Classical.",
                                            "children": [
                                                {
                                                    "move": "d2d4",
                                                    "san": "d4",
                                                    "name": "3. d4",
                                                    "comment": "White opens the center.",
                                                    "children": [
                                                        {
                                                            "move": "c5d4",
                                                            "san": "cxd4",
                                                            "name": "3...cxd4",
                                                            "comment": "Black captures.",
                                                            "children": [
                                                                {
                                                                    "move": "f3d4",
                                                                    "san": "Nxd4",
                                                                    "name": "4. Nxd4",
                                                                    "comment": "White recaptures.",
                                                                    "children": [
                                                                        {
                                                                            "move": "e7e5",
                                                                            "san": "e5",
                                                                            "name": "4...e5 — Sveshnikov Variation",
                                                                            "comment": "The Sveshnikov! Black immediately stakes the center, accepting the d5 weakness in exchange for active play.",
                                                                            "children": []
                                                                        }
                                                                    ]
                                                                }
                                                            ]
                                                        }
                                                    ]
                                                }
                                            ]
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        }
    },

    "Queen's Gambit": {
        "description": "A classical opening where White offers a pawn to gain central control. One of the oldest openings in chess.",
        "color": "white",
        "tree": {
            "move": None,
            "san": None,
            "name": "Start",
            "comment": "The Queen's Gambit begins 1.d4 d5 2.c4",
            "children": [
                {
                    "move": "d2d4",
                    "san": "d4",
                    "name": "1. d4",
                    "comment": "Queen's pawn opening — controls e5 and c5.",
                    "children": [
                        {
                            "move": "d7d5",
                            "san": "d5",
                            "name": "1...d5",
                            "comment": "Black fights for the center symmetrically.",
                            "children": [
                                {
                                    "move": "c2c4",
                                    "san": "c4",
                                    "name": "2. c4 — Queen's Gambit",
                                    "comment": "The Queen's Gambit! White offers a pawn to deflect Black's d5 pawn.",
                                    "children": [
                                        {
                                            "move": "d5c4",
                                            "san": "dxc4",
                                            "name": "2...dxc4 — Queen's Gambit Accepted",
                                            "popularity": 25,
                                            "comment": "QGA — Black accepts the gambit! White gets a strong center, Black gets activity.",
                                            "children": [
                                                {
                                                    "move": "e2e4",
                                                    "san": "e4",
                                                    "name": "3. e4",
                                                    "comment": "White immediately grabs the center.",
                                                    "children": [
                                                        {
                                                            "move": "e7e5",
                                                            "san": "e5",
                                                            "name": "3...e5",
                                                            "comment": "Challenging the center.",
                                                            "children": [
                                                                {
                                                                    "move": "g1f3",
                                                                    "san": "Nf3",
                                                                    "name": "4. Nf3",
                                                                    "comment": "Developing and attacking e5.",
                                                                    "children": []
                                                                }
                                                            ]
                                                        }
                                                    ]
                                                },
                                                {
                                                    "move": "g1f3",
                                                    "san": "Nf3",
                                                    "name": "3. Nf3",
                                                    "comment": "Classical development, preparing e3 and Bxc4.",
                                                    "children": [
                                                        {
                                                            "move": "g8f6",
                                                            "san": "Nf6",
                                                            "name": "3...Nf6",
                                                            "comment": "Black develops.",
                                                            "children": [
                                                                {
                                                                    "move": "e2e3",
                                                                    "san": "e3",
                                                                    "name": "4. e3",
                                                                    "comment": "Solid — White will recapture on c4 and develop.",
                                                                    "children": [
                                                                        {
                                                                            "move": "e7e6",
                                                                            "san": "e6",
                                                                            "name": "4...e6",
                                                                            "comment": "Solid structure for Black.",
                                                                            "children": [
                                                                                {
                                                                                    "move": "f1c4",
                                                                                    "san": "Bxc4",
                                                                                    "name": "5. Bxc4",
                                                                                    "comment": "White recaptures the pawn with the bishop, pointing at f7.",
                                                                                    "children": []
                                                                                }
                                                                            ]
                                                                        }
                                                                    ]
                                                                }
                                                            ]
                                                        }
                                                    ]
                                                }
                                            ]
                                        },
                                        {
                                            "move": "e7e6",
                                            "san": "e6",
                                            "name": "2...e6 — Queen's Gambit Declined",
                                            "popularity": 45,
                                            "comment": "QGD — Black declines, solidly supporting d5. The most classical response.",
                                            "children": [
                                                {
                                                    "move": "b1c3",
                                                    "san": "Nc3",
                                                    "name": "3. Nc3",
                                                    "comment": "Developing the knight, supporting the center.",
                                                    "children": [
                                                        {
                                                            "move": "g8f6",
                                                            "san": "Nf6",
                                                            "name": "3...Nf6",
                                                            "comment": "Black's most natural development.",
                                                            "children": [
                                                                {
                                                                    "move": "c1g5",
                                                                    "san": "Bg5",
                                                                    "name": "4. Bg5 — Classical QGD",
                                                                    "comment": "Classical! White pins the Nf6, preparing to double Black's pawns or exchange pieces.",
                                                                    "children": [
                                                                        {
                                                                            "move": "f8e7",
                                                                            "san": "Be7",
                                                                            "name": "4...Be7",
                                                                            "popularity": 80,
                                                                            "comment": "Black unpins quietly. The solid Orthodox Defense.",
                                                                            "children": [
                                                                                {
                                                                                    "move": "e2e3",
                                                                                    "san": "e3",
                                                                                    "name": "5. e3",
                                                                                    "comment": "Solid development, opening the diagonal for the f1 bishop.",
                                                                                    "children": [
                                                                                        {
                                                                                            "move": "e8g8",
                                                                                            "san": "O-O",
                                                                                            "name": "5...O-O",
                                                                                            "comment": "Black castles to safety.",
                                                                                            "children": []
                                                                                        }
                                                                                    ]
                                                                                }
                                                                            ]
                                                                        },
                                                                        {
                                                                            "move": "b8d7",
                                                                            "san": "Nbd7",
                                                                            "name": "4...Nbd7?? — Mistake!",
                                                                            "popularity": 20,
                                                                            "trap_mistake": True,
                                                                            "trap_name": "The Pillsbury Trap",
                                                                            "comment": "A critical mistake! Nbd7 looks natural but overlooks a devastating combination. White can now win material immediately!",
                                                                            "children": [
                                                                                {
                                                                                    "move": "c4d5",
                                                                                    "san": "cxd5!",
                                                                                    "name": "5.cxd5! — Striking in the center!",
                                                                                    "trap": True,
                                                                                    "trap_name": "The Pillsbury Trap — Strike!",
                                                                                    "comment": "TRAP! Open the position while Black is underdeveloped. Now 5...exd5 runs into 6.Nxd5!! forking everything. Black's queen on d8 hangs after Bxd8.",
                                                                                    "children": [
                                                                                        {
                                                                                            "move": "e6d5",
                                                                                            "san": "exd5",
                                                                                            "name": "5...exd5 (forced)",
                                                                                            "comment": "Forced. Now comes the knockout blow...",
                                                                                            "children": [
                                                                                                {
                                                                                                    "move": "c3d5",
                                                                                                    "san": "Nxd5!!",
                                                                                                    "name": "6.Nxd5!! — Winning the queen!",
                                                                                                    "comment": "Devastating! After 6...Nxd5 7.Bxd8 Bb4+ 8.Qd2 Bxd2+ 9.Kxd2 Kxd8, White has won the queen for a bishop and knight — a decisive material advantage. The Pillsbury Trap is complete!",
                                                                                                    "children": []
                                                                                                }
                                                                                            ]
                                                                                        }
                                                                                    ]
                                                                                }
                                                                            ]
                                                                        }
                                                                    ]
                                                                },
                                                                {
                                                                    "move": "g1f3",
                                                                    "san": "Nf3",
                                                                    "name": "4. Nf3",
                                                                    "comment": "Development before committing the bishop.",
                                                                    "children": [
                                                                        {
                                                                            "move": "f8e7",
                                                                            "san": "Be7",
                                                                            "name": "4...Be7",
                                                                            "comment": "Classical development.",
                                                                            "children": []
                                                                        }
                                                                    ]
                                                                }
                                                            ]
                                                        }
                                                    ]
                                                }
                                            ]
                                        },
                                        {
                                            "move": "c7c6",
                                            "san": "c6",
                                            "name": "2...c6 — Slav Defense",
                                            "popularity": 30,
                                            "comment": "The Slav! Black supports d5 with c6, keeping the c8 bishop's diagonal open.",
                                            "children": [
                                                {
                                                    "move": "g1f3",
                                                    "san": "Nf3",
                                                    "name": "3. Nf3",
                                                    "comment": "Development.",
                                                    "children": [
                                                        {
                                                            "move": "g8f6",
                                                            "san": "Nf6",
                                                            "name": "3...Nf6",
                                                            "comment": "Symmetric development.",
                                                            "children": [
                                                                {
                                                                    "move": "b1c3",
                                                                    "san": "Nc3",
                                                                    "name": "4. Nc3",
                                                                    "comment": "White develops and prepares e4.",
                                                                    "children": [
                                                                        {
                                                                            "move": "d5c4",
                                                                            "san": "dxc4",
                                                                            "name": "4...dxc4 — Main Line Slav",
                                                                            "comment": "Now Black can take, since c6 means the pawn can be supported later.",
                                                                            "children": [
                                                                                {
                                                                                    "move": "e2e4",
                                                                                    "san": "e4",
                                                                                    "name": "5. e4",
                                                                                    "comment": "White takes the full center.",
                                                                                    "children": [
                                                                                        {
                                                                                            "move": "b7b5",
                                                                                            "san": "b5",
                                                                                            "name": "5...b5",
                                                                                            "comment": "Black holds the extra pawn, leading to sharp play.",
                                                                                            "children": []
                                                                                        }
                                                                                    ]
                                                                                }
                                                                            ]
                                                                        }
                                                                    ]
                                                                }
                                                            ]
                                                        }
                                                    ]
                                                }
                                            ]
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        }
    }
}
