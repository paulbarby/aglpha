class AIManager:
    def __init__(self):
        self.ai_players = {}  # {ai_id: AIPlayer}

    def add_ai_player(self, ai_player):
        self.ai_players[ai_player.id] = ai_player

    def update_ai(self):
        for ai in self.ai_players.values():
            ai.make_decision()