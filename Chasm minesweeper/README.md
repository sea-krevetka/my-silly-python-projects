### this is python code ~~(totally not edited by deepseek?)~~ for solving chasm minesweeper. It fills the field from (0,0) aka left top square. Square map:  
(0,0) (0,1) (0,2) (0,3) (0,4)  
(1,0) (1,1) (1,2) (1,3) (1,4)  
(2,0) (2,1) (2,2) (2,3) (2,4)  
(3,0) (3,1) (3,2) (3,3) (3,4)  
(4,0) (4,1) (4,2) (4,3) (4,4)   
  
It fills out bombs and chooses safe squares to fill out where chest is using bomb squares. The bot tries to choose the squares with the least probability of finding a bomb.  

## How to use the bot:
1. Run the program
2. The bot will suggest the next digging hole in the format (row, column)
3. Enter what you found in this hole:
   - space - empty hole  
   - C - cabbage  
   - P - potatoes  
   - I - iron ore  
   - X - Powder keg (game ends)
   - T - Chest (win!)
4. The bot analyzes the information and suggests the next hole
  
  
I tested this bot on my acc and it, ~~(in fact and to my dearest surprise)~~, sucessfully found all three chests in <10 moves, though chests may've been hidden in some lucky way. (and it felt like it was hidden in a same place every time?) but on [ws i used to see the rules of the game](https://wotpack.ru/genshin-impact-kak-vyigrat-u-stariny-chou-ta-dam-u-nas-snova-pobeditel-dostizhenie/) in example the chest was hidded in a down left corner. probably should make a bot to create such fields to check this bot- cause that sure sounds fun. 
