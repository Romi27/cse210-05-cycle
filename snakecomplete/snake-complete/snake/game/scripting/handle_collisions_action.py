import constants
from game.casting.actor import Actor
from game.scripting.action import Action
from game.shared.point import Point

class HandleCollisionsAction(Action):
    """
    An update action that handles interactions between the actors.
    
    The responsibility of HandleCollisionsAction is to handle the situation when the snake collides
    with the food, or the snake collides with its segments, or the game is over.
    Attributes:
        _is_game_over (boolean): Whether or not the game is over.
    """

    def __init__(self):
        """Constructs a new HandleCollisionsAction."""
        self._is_game_over = False

    def execute(self, cast, script):
        """Executes the handle collisions action.
        Args:
            cast (Cast): The cast of Actors in the game.
            script (Script): The script of Actions in the game.
        """
        if not self._is_game_over:
            self._handle_food_collision(cast)
            self._handle_segment_collision(cast)
            self._handle_game_over(cast)

    def _handle_food_collision(self, cast):
        """Updates the score nd moves the food if the snake collides with the food.
        
        Args:
            cast (Cast): The cast of Actors in the game.
        """
        score = cast.get_first_actor("scores")
        food = cast.get_first_actor("foods")
        snake = cast.get_first_actor("snakes")
        head = snake.get_head()

        '''This code needs to be deleted eventually, it used to grow the snakes 
           when they ate the food.'''
        # if head.get_position().equals(food.get_position()):
        #     points = food.get_points()
        #     snake.grow_tail(points)
        #     score.add_points(points)
        #     food.reset()

    def _handle_segment_collision(self, cast):
        """Sets the game over flag if the snake collides with one of its segments.
        
        Args:
            cast (Cast): The cast of Actors in the game.
        """
        players = [cast.get_first_actor("snakes"), cast.get_first_actor("snake2")]
        scores = cast.get_actors("scores")
        heads = []
        segments_list = []
        for player in players:
            head = player.get_segments()[0]
            segments = player.get_segments()[1:]
            heads.append(head)
            segments_list.append(segments)
        for segment in segments_list[1]:
            if heads[0].get_position().equals(segment.get_position()):
                self._is_game_over = True
                scores[0].add_points(10)
        for segment in segments_list[0]:
            if heads[1].get_position().equals(segment.get_position()):
                self._is_game_over = True
                scores[1].add_points(10)


    def _handle_game_over(self, cast):
        """Shows the 'game over' message and turns the snake and food white if the game is over.
        
        Args:
            cast (Cast): The cast of Actors in the game.
        """
        if self._is_game_over:
            snake = cast.get_first_actor("snakes")
            segments = snake.get_segments()

            # I added the snake 2 so at game over so snake2 can turn white.
            snake2 = cast.get_first_actor("snake2")
            segment2 = snake2.get_segments()

            food = cast.get_first_actor("foods")

            x = int(constants.MAX_X / 2)
            y = int(constants.MAX_Y / 2)
            position = Point(x, y)

            message = Actor()
            message.set_text("Game Over!")
            message.set_position(position)
            cast.add_actor("messages", message)
            

            for segment in segments:
                segment.set_color(constants.WHITE)

            # I added this so snake 2 can turn white at game over.
            for segment in segment2:
                segment.set_color(constants.WHITE)
