const alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';  //Creates a constant global variable called alphabet, which is the alphabet
const movingWrapper = '<div class="p-2 bg-light border rounded shadow-sm"></div>';  //Creates a constant global varibale that designs what it looks like when you start moving something

//This subroutine is for opening full screen
function openFullscreen() {
  const elem = document.documentElement;    //finds the object with the full screen function in it
  if (elem.requestFullscreen) {     //checks to make sure that the function (going full screen) exists
    elem.requestFullscreen();   //makes the whole page go fullscreen
  }
}
//This subroutine is for exiting full screen
function exitFullscreen() {
  if (document.fullscreenElement) {     //same as open full screen but for exiting
    document.exitFullscreen();
  }
}

function handleResponse(response, board, msg) {
  console.log('Success:', response);  //deals with the response from python
  if (response.result === true) {
    //If the click is a hit, then it adds a class so that css can colour it
    board.find($('*[data-grid="'+response.target+'"]')).addClass('hit');
  } 
  if (response.result === false) {
    //Same but if it's a miss
    board.find($('*[data-grid="'+response.target+'"]')).addClass('miss');
  }
  if (response.result === 'sunk') {
    // For every part of the specific ship that has been sunk, will turn black
    for (let i = 0; i < response.coordinates.length; i++) {
      console.log('doing:', response.coordinates[i]);
      // Removing the hit class (to remove the red) and replace it with the sunk class (black)
      board.find($('*[data-grid="'+response.coordinates[i]+'"]')).removeClass('hit').addClass('sunk');
    }
    if (response.win === true) {
      // Once someone has won, the hidden messages will show, depending on who won
      msg.show();
      $('.game-board').find($('button')).prop("disabled", true); //Disables all of the opponents boards buttons
    }
  } 
}

//Where you would put javascript functions to change the page
$(document).ready(function () {

  $('.game-board table') //Finds all game boards and targets the table inside it
  .each(function(index, item) {  //For every table inside game-board, this funtion will execute
    let gameBoard = $(item);  //Creating a variable that refers to the table
    const boardSize = GRID_SIZE;  //How big the board will be
    for (let row = 0; row < boardSize + 2; row++) { //Begins a for loop that starts at 0, increments by 1 each time and goes until board size + 2
      let rowElement = $('<tr/>'); //Creating rows
      for (let col = 0; col < boardSize + 2; col++) { //Same as 2 lines above, but for columns instead
        if (row == 0 || row == boardSize + 1) {   //If it's the first or last row, then don't label it
          if (col == 0 || col == boardSize + 1) { //If it's the first or last column, then don't label it
            rowElement.append('<th>&nbsp;</th>');    //Creating the space for the corners of the grid
          } else{
            rowElement.append('<th>'+alphabet[col-1]+'</th>');    //Adds the column heading (alphabet)
          }      
        } else {  //If it's not the first or last row, then creates buttons unless it's the first or last column
          if (col == 0 || col == boardSize + 1) {
            rowElement.append('<th>'+row+'</th>');   //If it's the first or last column, then label with numbers 
          } else{
            rowElement.append('<td><button data-grid="'+alphabet[col-1]+row+'"></button></td>');  //Adding the buttons to everything else
          }       
        }
      }
      gameBoard.append(rowElement); //Adds the row that's just been created
    }
  });

  $('.game-board.opponent').on('click', 'button', function() { //Looks for any button inside game-board and when it's clicked do this function
    let $this = $(this);  //Assigining a variable to the jquery version of the button you clicked on
    $this.prop("disabled", true); //Disables button after clicking it
    $.ajax({  //A way of sending a request to python
      url: '/take-turn',  //The path to get to python
      type: 'POST',
      contentType: 'application/json',  //json is a convenient way of passing information back and forth
      dataType: 'json',
      data: JSON.stringify({  //Making 'turn' into json
        id: GAME_ID,  //Passing the gameId back to python
        turn: $this.data('grid')  //'this' is the button the user clicked on and data('grid') is its coordinates
      }),
      success: function(response) {
        // Tells the function 'handleResponse' that the user has made a turn on the opponent's board and a win message might need to be shown
        handleResponse(response.userTurn, $('.opponent'), $(".win-message-user"));
        if (!response.userTurn.win) {
          // This does the same thing, but will not run if the user has won
          handleResponse(response.computerTurn, $('.user'), $(".win-message-opponent"));
        }
      }
    });
  });

  //Defines a class called unit, which has the atrributes name, width, length and radiobutton
  class Unit {
    constructor(name, width, length, radioButton) {
      this.name = name;
      this.width = width;
      this.length = length;
      this.radioButton = radioButton;   //This is to enable and disable the unit after dragging or dropping it
    }
  }

  if (typeof UNITS != "undefined") {
    let $units = $('#units')
    for (let index = 0; index < UNITS.length; index++) {      // For each unit, adds it to the setup page
      let wrapper = $('<div class="row unit"/>');   //Creates a wrapper to hold the radio button
      let unitName = UNITS[index][0];   //Assigns unitName to the first unit in the 'sea' category
      let radio = $('<input type="radio" id="'+unitName+'" name="unit" value="'+unitName+'" />');   // Each unit is a radio button so that you can select it, it displays the name, width and length of the unit
      let unit = new Unit(unitName, UNITS[index][1], UNITS[index][2], radio);   //Creates a unit instance
      radio.data('unit', unit);   //Attaches the unit to the radio button
      wrapper
        .append(radio)    //Adds the radio button to the wrapper
        .append('<label for="'+unitName+'">'+unitName+' ('+unit.width+','+unit.length+')</label>');    //Creates a label holding the name, width and length of the unit (The part that displays on the screen)
      $units.append(wrapper);   //Adds the wrapper the unit column
    }
    $('.game-board.setup button').each(function(index, item) {    //Initiales an array on each button on the grid to hold the dropped units
      $(item).data('units-array', []);   //The array
    });
  }

  $('.unit').draggable({  //defines what you can pick up
    helper: function() {  //helper wraps the item you grabbed into the thing you can move around
      const radio = $(this).find('input[type=radio]');  //sets the variable "radio" as the radio button that's been grabbed
      if (!radio.is(':checked') && !radio.prop('disabled')) radio.prop('checked', true); //select the unit being grabbed if it's not already been used
      const move = $(movingWrapper); //creates the wrapper (the thing you can move)
      move.text('X'); //sets the text in the wrapper to the unit name
      move.data('unit', radio.data('unit')); //creates a reference to the unit that was grabbed (so it can be disabled when successfully dropped)
      return move; //returns the wrapper to the javascript that controls the movement
    },
    cursor: "move", //changes the cursor to a "move" icon
    start: function(event, ui) { //method that is called before dragging can begin
      const radio = $(this).find('input[type=radio]'); //sets the variable "radio" as the radio button that's been grabbed
      if (radio.prop('disabled')) { //if it has already been dragged succesfully then it will be disabled...
        return false; //so prevent dragging
      }
    }
  });

  $('.game-board.setup td').droppable({   //defines where you can drop (only on the grid)
    accept: ".unit",  //allows you to drop any of the units but nothing else 
    drop: function(event, ui) {   //method that is called when the unit is dropped
      const unit = ui.helper.data('unit');  //getting the reference of the unit
      const $place = $(this);   //where you dropped
      const width = unit.width;   //Creates the constant width as the units specific width
      const length = unit.length;   //Creates the constant length as the units specific length
      const board = $('.game-board.setup');   //Creates the constant board as the setup game board
      const currentSquare = $place.find('button');    //Creates the constant currentSquare as the button you've dropped on
      let col = alphabet.indexOf(currentSquare.data('grid').substring(0, 1)) + 1;   //Makes col the number associated to the letter that the unit was dropped on (A becomes 1, D becomes 4. Because of the +1)
      let row = Number(currentSquare.data('grid').substring(1));    //Makes row equivalent to the number on the same line as the button dropped on
      for (let y = 0; y < width; y++) {   //A for loop for the width of the unit
        if (row + y > GRID_SIZE) break;   //Prevents the units from appearing outside of the grid on the y axis
        for (let x = 0; x < length; x++) {    //A for loop for the length of the unit
          if (col + x > GRID_SIZE) break;   //Prevents the units from appearing outside of the grid on the x axis
          let square = board.find('*[data-grid="'+alphabet[col+x-1]+(row+y)+'"]');    //Finds the square with the new grid refrences
          square.addClass('unit');    //Making the new square a unit as well
          square.data('units-array').push(unit);    //Puts the new unit into the unit array for that square
          square.draggable({    //Making the square draggable so the unit can be moved around
            cancel: false,    //This allows buttons to be moved
            helper: function() {    //What to do once you start moving the unit
              const units = $(this).data('units-array');    //Creates a constant variable called units to get the all the units in the square
              const unitToMove = units.pop();   //Gets specifically the last unit that's placed
              units.push(unitToMove);   //Puts the unit picked up back in the array to allow the other functions to remove it
              const move = $(movingWrapper);    //Creates a constant variable called move that creats an instance of the global wrapper
              move.text('X');   //And displays the text 'X' in the wrapper
              move.data('unit', unitToMove);    //Adds a reference to the unit to the thing being moved
              return move;    //Returns move to the library thats allowing the unit to be moved
            },
            cursor: "move",   //Changes the pointer into a move curser
            stop: function(event, ui) {   //Defines the function, that's triggered when you stop dragging
              const unit = ui.helper.data('unit');  //Creates a constant variable called unit which becomes the data of the unit being moved
              let stillOnBoard = false;
              $('.game-board.setup td button').each(function() {    //Finds each button and runs the following function
                if (($(this).data('units-array') || []).includes(unit)) {   //Checks to see if the unit being moved is still on the board (in the array)
                  stillOnBoard = true;
                  return;
                }
              });
              if (!stillOnBoard) {
                unit.radioButton.prop('disabled', false);   //Makes it so that the radio button is renabled
              }
            }
          });
        }
      }
      unit.radioButton.prop('disabled', true); //disable the unit so that it cannot be selected again
      unit.radioButton.prop('checked', false); //unselect the unit
    }
  });

  //This function is to remove the unit off the board when you pick it up
  $('.game-board.setup').on('dragstart', '.unit', function (event, ui) {    //When you start moving a unit that's already on the board, do this function
    const draggedUnit = $(this).data('units-array').pop(); //Creates a constant variable called draggedUnit that is the last unit to be placed down
     $(this).data('units-array').push(draggedUnit);   //Puts the unit picked up back in the array to allow the other functions to remove it
    const board = $('.game-board.setup');

    //Look at all buttons on the grid to find if they have the dragged unit in their data
    board.find('.unit').each(function () { 
      const $btn = $(this);   //Reference to the button
      const units = $btn.data('units-array') || [];   //Gets the units that are in that button

      if (units.includes(draggedUnit)) { //If this button has the dragged unit
        $btn.addClass('moving');
        const newUnits = units.filter(u => u !== draggedUnit);    //Removing the dragged unit from the specific button that's it's looking at (will look from them all using the function above)
        $btn.data('units-array', newUnits);   //Giving the modified array back to the button (without the dragged unit)

        //If no units remain in this square, make the button undraggable
        if (newUnits.length === 0) {
          $btn.draggable('destroy');    //Make the button undraggable
        }
      }
    });
  });

  //When you stop draggin a unit, remove evidence of where it used to be
  $('.game-board.setup').on('dragstop', '.moving', function () {
    const board = $('.game-board.setup');
    board.find('.moving').each(function() {
      $(this).removeClass('moving');    //Takes away the blue squares (but if there's still a ship remaining then you still want that square to look like a unit)
      if ($(this).data('units-array').length == 0) {    //If there are no ships left over then
        $(this).removeClass('unit');    //Remove the unit from the class
      //If all ships are gone from this square then it shouldn't look like a unit anymore
      }
    });
  });
});
