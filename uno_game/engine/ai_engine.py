"""Advanced AI engine for UNO game with strategic decision making."""

from typing import List, Dict, Optional
from ..models.card import Card, CardColor, CardType
from ..models.player import Player


class SimpleAI:
    """Enhanced AI engine with strategic decision making."""
    
    def __init__(self, difficulty: str = "medium"):
        """Initialize AI engine.
        
        Args:
            difficulty: AI difficulty level (easy, medium, hard)
        """
        self.difficulty = difficulty
        self.strategy_weights = self._get_strategy_weights()
    
    def _get_strategy_weights(self) -> Dict[str, float]:
        """Get strategy weights based on difficulty.
        
        Returns:
            Dictionary of strategy weights
        """
        weights = {
            "easy": {
                "color_preference": 0.3,
                "action_card_timing": 0.2,
                "wild_card_conservation": 0.1,
                "opponent_hand_awareness": 0.1
            },
            "medium": {
                "color_preference": 0.6,
                "action_card_timing": 0.5,
                "wild_card_conservation": 0.4,
                "opponent_hand_awareness": 0.3
            },
            "hard": {
                "color_preference": 0.8,
                "action_card_timing": 0.7,
                "wild_card_conservation": 0.6,
                "opponent_hand_awareness": 0.5
            }
        }
        return weights.get(self.difficulty, weights["medium"])
    
    def choose_best_card(self, ai_player: Player, valid_cards: List[Card], 
                        top_card: Card, opponent: Player, 
                        game_state: dict) -> Optional[Card]:
        """Choose the best card to play using strategic analysis.
        
        Args:
            ai_player: The AI player
            valid_cards: List of valid cards to play
            top_card: Current top card
            opponent: The opponent player
            game_state: Current game state information
            
        Returns:
            Best card to play or None if should draw
        """
        if not valid_cards:
            return None
        
        # Score each valid card
        card_scores = []
        for card in valid_cards:
            score = self._score_card(card, ai_player, top_card, opponent, game_state)
            card_scores.append((card, score))
        
        # Sort by score (highest first)
        card_scores.sort(key=lambda x: x[1], reverse=True)
        
        # Return the best card
        return card_scores[0][0]
    
    def _score_card(self, card: Card, ai_player: Player, top_card: Card, 
                   opponent: Player, game_state: dict) -> float:
        """Score a card based on strategic value.
        
        Args:
            card: Card to score
            ai_player: AI player
            top_card: Current top card
            opponent: Opponent player
            game_state: Game state
            
        Returns:
            Score for the card (higher is better)
        """
        score = 0.0
        
        # Base score for playability
        score += 10.0
        
        # Color matching bonus
        if card.color == top_card.color:
            score += 5.0 * self.strategy_weights["color_preference"]
        
        # Number matching bonus (lower than color)
        if card.value == top_card.value and card.color != top_card.color:
            score += 3.0
        
        # Action card strategy
        if card.card_type == CardType.ACTION:
            score += self._score_action_card(card, ai_player, opponent, game_state)
        
        # Wild card strategy
        elif card.card_type == CardType.WILD:
            score += self._score_wild_card(card, ai_player, opponent, game_state)
        
        # Hand composition bonus
        score += self._score_hand_composition(card, ai_player)
        
        # Opponent awareness
        score += self._score_opponent_awareness(card, opponent, game_state)
        
        return score
    
    def _score_action_card(self, card: Card, ai_player: Player, 
                          opponent: Player, game_state: dict) -> float:
        """Score action cards based on timing and strategy.
        
        Args:
            card: Action card to score
            ai_player: AI player
            opponent: Opponent
            game_state: Game state
            
        Returns:
            Action card score
        """
        score = 0.0
        timing_weight = self.strategy_weights["action_card_timing"]
        
        opponent_cards = opponent.card_count()
        ai_cards = ai_player.card_count()
        
        if card.value == "skip":
            # Skip is more valuable when opponent has few cards
            if opponent_cards <= 3:
                score += 8.0 * timing_weight
            else:
                score += 4.0 * timing_weight
        
        elif card.value == "reverse":
            # In 2-player game, reverse acts like skip
            if opponent_cards <= 3:
                score += 8.0 * timing_weight
            else:
                score += 4.0 * timing_weight
        
        elif card.value == "draw_two":
            # Draw Two is very valuable when opponent has few cards
            if opponent_cards <= 2:
                score += 12.0 * timing_weight
            elif opponent_cards <= 4:
                score += 8.0 * timing_weight
            else:
                score += 5.0 * timing_weight
        
        return score
    
    def _score_wild_card(self, card: Card, ai_player: Player, 
                        opponent: Player, game_state: dict) -> float:
        """Score wild cards based on conservation strategy.
        
        Args:
            card: Wild card to score
            ai_player: AI player
            opponent: Opponent
            game_state: Game state
            
        Returns:
            Wild card score
        """
        conservation_weight = self.strategy_weights["wild_card_conservation"]
        
        # Wild cards are powerful but should be conserved
        base_score = 2.0
        
        # Use wild cards more aggressively when AI has many cards
        ai_cards = ai_player.card_count()
        if ai_cards > 5:
            base_score += 3.0 * conservation_weight
        elif ai_cards > 3:
            base_score += 1.0 * conservation_weight
        else:
            # Conserve when hand is small
            base_score -= 2.0 * conservation_weight
        
        # Wild Draw Four is more powerful
        if card.value == "wild_draw_four":
            opponent_cards = opponent.card_count()
            if opponent_cards <= 3:
                base_score += 10.0 * conservation_weight
            else:
                base_score += 5.0 * conservation_weight
        
        return base_score
    
    def _score_hand_composition(self, card: Card, ai_player: Player) -> float:
        """Score based on hand composition after playing card.
        
        Args:
            card: Card being considered
            ai_player: AI player
            
        Returns:
            Hand composition score
        """
        score = 0.0
        
        # Count colors in hand (excluding the card being played)
        color_counts = {color: 0 for color in CardColor}
        for hand_card in ai_player.hand:
            if hand_card != card and hand_card.color in color_counts:
                color_counts[hand_card.color] += 1
        
        # Prefer playing cards that leave balanced colors
        if card.color != CardColor.WILD:
            remaining_of_color = color_counts[card.color]
            if remaining_of_color > 2:
                score += 2.0  # Good to reduce dominant color
            elif remaining_of_color == 0:
                score -= 1.0  # Avoid eliminating a color completely
        
        return score
    
    def _score_opponent_awareness(self, card: Card, opponent: Player, 
                                 game_state: dict) -> float:
        """Score based on opponent's likely hand composition.
        
        Args:
            card: Card being considered
            opponent: Opponent player
            game_state: Game state
            
        Returns:
            Opponent awareness score
        """
        awareness_weight = self.strategy_weights["opponent_hand_awareness"]
        score = 0.0
        
        opponent_cards = opponent.card_count()
        
        # Be more aggressive when opponent has few cards
        if opponent_cards == 1:
            # Opponent might win next turn - play aggressively
            if card.card_type in [CardType.ACTION, CardType.WILD]:
                score += 15.0 * awareness_weight
        elif opponent_cards <= 3:
            # Opponent is close to winning
            if card.card_type in [CardType.ACTION, CardType.WILD]:
                score += 8.0 * awareness_weight
        
        return score
    
    def choose_wild_color_strategic(self, ai_player: Player, 
                                   opponent: Player) -> CardColor:
        """Choose wild card color strategically.
        
        Args:
            ai_player: AI player
            opponent: Opponent player
            
        Returns:
            Best color choice
        """
        # Count colors in AI's hand
        color_counts = {
            CardColor.RED: 0,
            CardColor.BLUE: 0,
            CardColor.GREEN: 0,
            CardColor.YELLOW: 0
        }
        
        for card in ai_player.hand:
            if card.color in color_counts:
                color_counts[card.color] += 1
        
        # Choose color with most cards, but add some randomness for easy mode
        if self.difficulty == "easy":
            # Sometimes choose randomly for easier gameplay
            import random
            if random.random() < 0.3:
                return random.choice(list(color_counts.keys()))
        
        # Choose the color with the most cards
        best_color = max(color_counts, key=color_counts.get)
        
        # If no clear winner, choose red as default
        if color_counts[best_color] == 0:
            return CardColor.RED
        
        return best_color
