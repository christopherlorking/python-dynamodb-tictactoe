import boto3, time, uuid

# Basic Tic Tac Toe game.
# Mix of global and local variables for learning purposes.

# Symbols to represent Player 1, Player 2, and a shortcut for a space to make things more readable.
p1, p2, blank = 'X', 'O', ' '
# Game will operate whilst turn_count is within normal bounds - cannot have a 10th turn.
turn_count = 1
# Track the current player during turns.
current_player = p1
# List to hold the game board and what the value of each position is.
board = []
# Initiate DynamoDB resources
dynamodb_service = boto3.resource('dynamodb')
dynamodb_client = boto3.client('dynamodb')

# Returns a new 'board' for playing the game on - consists of nine indexes which represent the positions on the board.
# Positions on the board are labelled as:
# 1,2,3
# 4,5,6
# 7,8,9
def new_board():
  global board
  board = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ]

# Function to print the current board (game state) out. Not super pretty.
# Example:
# -------
# |X| | |
# |-+-+-|
# | |X| |
# |-+-+-|
# | |O|O|
# -------
def print_board():
  global board
  print('-------')
  print('|' + board[0] + '|' + board[1] + '|' + board[2] + '|')
  print('|-+-+-|')
  print('|' + board[3] + '|' + board[4] + '|' + board[5] + '|')
  print('|-+-+-|')
  print('|' + board[6] + '|' + board[7] + '|' + board[8] + '|')
  print('-------')

# Set the current player to the other player.
def swap_to_other_player():
  global p1, p2, current_player
  if current_player == p1:
    current_player = p2
  else:
    current_player = p1

# Check to see whether either player has met any of the victory conditions.
def check_if_game_is_won(board):
  gameWon = False
  # three horitzonal all the same (and not blank)
  if board[0] == board[1] == board[2] and board[0] != blank: gameWon = True
  if board[3] == board[4] == board[5] and board[3] != blank: gameWon = True
  if board[6] == board[7] == board[8] and board[6] != blank: gameWon = True
  # three vertical all the same (and not blank)
  if board[0] == board[3] == board[6] and board[0] != blank: gameWon = True
  if board[1] == board[4] == board[7] and board[1] != blank: gameWon = True
  if board[2] == board[5] == board[8] and board[2] != blank: gameWon = True
  # three diagonal all the same (and not blank)
  if board[0] == board[4] == board[8] and board[0] != blank: gameWon = True
  if board[2] == board[4] == board[6] and board[2] != blank: gameWon = True
  return gameWon

def turn():
  global turn_count, board
  print('===============')
  print('Turn: ' + str(turn_count))
  print('===============')
  print_board()
  print('===============')
  print('It is currently ' + current_player + "'s turn")
  print('Please enter where you would like to go...')
  
  # Take player's input as their move - options are 1-9
  # If the position on the board is blank then the move can go ahead.
  # move - 1 matches the position on the board to the index of the position within the board)
  # TODO try catch for non int?
  move = int(input()) 
  if move > 9 or move < 0:
    print('********That move is outside the board - try again, any position on the board between 1 and 9********')
    turn()
    return
  if board[move - 1] == blank:
    board[move - 1] = current_player
  else:
    print('********That move is invalid as that position on the board is already filled.********')
    turn()
    return
  turn_count = turn_count + 1

def create_dynamodb_table():
  table = dynamodb_service.create_table(
    TableName='python-dynamodb-tictactoe',
    KeySchema=[
        {
            'AttributeName': 'game_id',
            'KeyType': 'HASH'
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'game_id',
            'AttributeType': 'S'
        }
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 1,
        'WriteCapacityUnits': 1
    }
  )

  # Wait until the table exists.
  # TODO
  table.meta.client.get_waiter('table_exists').wait(TableName='python-dynamodb-tictactoe')
  print('DynamoDB table created.')

# Saves aspects of the game to AWS DynamoDB.
def save_game():
  # Check to see if table already exists, create if not.
  if not 'python-dynamodb-tictactoe' in dynamodb_client.list_tables()['TableNames']:
    print("DynamoDB table not detected - creating....")
    create_dynamodb_table()

  table = dynamodb_service.Table('python-dynamodb-tictactoe')

  # Gather further details from user.
  print('What is the name of the first player (X)?')
  player_1_name = input()
  print('What is the name of the second player (O)?')
  player_2_name = input()

  # Put data in to table
  # UUID was time based, int(time.time()), but values in table would be overwritted if two items put within same rounded second.
  table.put_item(
    Item={
          'game_id': str(uuid.uuid1()),
          'player_1_name': player_1_name,
          'player_2_name': player_2_name,
          'victor': current_player,
      }
  )

def tic_tac_toe():
  # Symobls to represent Player 1, Player 2, and a shortcut for a space to make things more readable.
  global p1, p2, blank, turn_count, current_player, board
  p1, p2, blank = 'X', 'O', ' '
  turn_count = 1
  current_player = p1
  new_board()

  print('Welcome to Tic Tac Toe - two-player-hot-seat-Python-based-saving-game-results-to-DynamoDB version...\n')
  print('The game board has the traditional 3 x 3 layout, but each position is marked by a number 1-9.')
  print('-------')
  print('|1|2|3|')
  print('|-+-+-|')
  print('|4|5|6|')
  print('|-+-+-|')
  print('|7|8|9|')
  print('-------')
  print('When the game is live, please enter the number that corresponds with the position you would like to go.')

  while turn_count < 10:
    turn()
    if check_if_game_is_won(board):
      break
    swap_to_other_player()

  print('\n\n--Game is over!--')

  if check_if_game_is_won(board) == False:
    print('--No one has won - the result is a tie!')
  else:
    print('--Winning player: ' + current_player + '--')
  
  print_board()

  print('--Thanks for playing!--')

  print('Would you like to save this game result? (y/n)')
  response = input()
  if response == 'y' or response == 'Y':
    save_game()
  
  # TODO Asks user if they want to play again, resets the game if yes.
  print('\n\n--Would you like to play again?--')


  

if __name__ == "__main__":
  tic_tac_toe()