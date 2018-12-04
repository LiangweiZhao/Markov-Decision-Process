# Markov-Decision-Process
<h2>MDP Algorithm Problem</h2>

<h3>Description</h3>
<p>The cars can move North, South, East, or West(see directions to the right). The city can be represented in a grid, as below</p>
<img src="https://github.com/LiangweiZhao/Markov-Decision-Process/blob/master/coord.png">
<p>There will be some obstacles, such as buildings, road closings, etc.If a car crashes into a buildingor road closure, SpeedRacerhas to pay $100. You know the locations of these, and they will not change over time. You also spend $1 for gas each time you move. The cars will start fromagiven SpeedRacerparking lot, and will end at another parking lot. When you arrive at your destination parking lot, you will receive $100. Your goal is to make the most money1over time with the greatest likelihood. Your cars haveafaulty turning mechanism, so they havea chance of going in a direction other than the one suggested by your model. Theywill go in the correct direction 70% of the time(10% in each other direction, including along borders).</p>
<p>The first part of your task is to design an algorithm that determines where your cars should try to go in each city grid location givenyour goal of making the most money. Then, to make sure that this is a good algorithm when you present it to the rest of your board, you should simulate the car moving through the city grid. To do this, you will use your policy from your start location. You will then check to see if the car went in the correct direction using a random number generator with specific seeds to make sure you can reproduce your output. You will simulate your car moving through the city grid 10 timesusing the random seeds 0, 1, 2, 3, 4, 5, 6, 7, 8, and 9. You will report the meanover these 10 simulations as an integer after using the floor operation(e.g., numpy.floor(meanResult)).An example of this process is given in detail below.</p>

<h3>Valid_Input</h3>
<div>
  <p><b>Input:</b> The file input.txt in the current directory of your program will be formatted as follows:</p> 
  <p><b>First line:</b> strictly positive 32-bit integer s, size of grid [grid is a square of size sxs]</p>
  <p><b>Second line:</b> strictly positive 32-bit integer n, number of cars</p>
  <p><b>Third line:</b> strictly positive 32-bit integer o, number of obstacles</p>
  <p><b>Next o lines:</b>32-bit integer x, 32-bit integer y, denoting the location of obstacles</p>
  <p><b>Next n lines:</b>32-bit integer x, 32-bit integer y, denoting the start location of each car</p>
  <p><b>Next n lines:</b>32-bit integer x, 32-bit integer y, denoting the terminal location of each car</p>
  <p><b>Output:</b> n lines: 32-bit integer, denoting the meanmoney earned in simulationfor each car, integerresult of floor operation</p></div>

<h3>Example</h3>
<p>For example, say you have a 3x3grid, as follows, with 1 car in start position 2,0(green):</p>
<img src="https://github.com/LiangweiZhao/Markov-Decision-Process/blob/master/probCoord.png">

<p>You determine that based on the locations of certain obstacles, you should move in these directions ineach cell:</p>
<img src="https://github.com/LiangweiZhao/Markov-Decision-Process/blob/master/policy.png">

<p>Then, you should do simulation using this policy. Beginning at the start position, move in the direction suggested by your policy. There is a 10% chance that you will move South,so check your direction using randomgeneration with random seed = 0(see code below). In this case, you actually move West, so you will receive -$1. You will now try to move West againbased on your policy. With the random seed = 0, you successfully move South.Therefore, you now have -$2.Repeat at your next locations, until you end at your terminal state. Record the total money you have at the end. Let’s say that the total is $91. Then, repeat this process 9 more times. You will average $91with the 9 other results, and report the number.If the result is 91.65093, for example, you should record the floor, 91,in your output file.</p>
