//Creates a constant global variable called alphabet, which is the alphabet
const alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';  

//Helper function to create a drag helper for a unit
function createUnitDragHelper(unit) {
  if (!unit) return false; // Abort drag if no unit
  const move = $('<div class="bg-transparent opacity-25 z-3"></div>');
  move.append('<img src="/static/img/sea/'+unit.name.toLowerCase()+'.png" alt="'+unit.name+'" ' +
    'class="unit-drag-image '+unit.name.toLowerCase()+(unit.rotated ? ' rotated' : '')+'" />');
  //creates a reference to the unit that was grabbed (so it can be disabled when successfully dropped)
  move.data('unit', unit);
  return move;
}

//Helper function to make a square draggable (used when placing units on the board)
function makeSquareDraggable(square) {
  if (square.data('ui-draggable')) return; // Already draggable
  square.draggable({
    cancel: false,
    helper: function() {
      const units = $(this).data('units-array');
      const unitToMove = units.pop();
      units.push(unitToMove);
      return createUnitDragHelper(unitToMove);
    },
    cursor: "move",
    cursorAt: { left: 10, top: 10 },
    stop: function(event, ui) {
      const unit = ui.helper.data('unit');
      let stillOnBoard = false;
      $('.game-board.setup td button').each(function() {
        if (($(this).data('units-array') || []).includes(unit)) {
          stillOnBoard = true;
          return;
        }
      });
      if (!stillOnBoard) {
        if (unit.rotated) {
          unit.rotate();
        }
        unit.radioButton.prop('disabled', false);
        unit.radioButton.closest('.unit').removeClass('opacity-50');
      }
    }
  });
}

//Helper function to find all board squares that contain a specific unit and remove it
function removeUnitFromBoard(board, unit, perButtonCallback) {
  //Look at all buttons on the grid to find if they have the unit in their data
  board.find('.unit').each(function () {
    const $btn = $(this);   //Reference to the button
    const units = $btn.data('units-array') || [];   //Gets the units that are in that button

    if (units.includes(unit)) { //If this button has the unit
      //Removing the unit from the specific button that it's looking at
      //(will look from them all using the function above)
      const newUnits = units.filter(u => u !== unit);
      //Giving the modified array back to the button (without the unit)
      $btn.data('units-array', newUnits);
      perButtonCallback($btn, newUnits);
      //If no units remain in this square, make the button undraggable
      if (newUnits.length === 0) {
        // Only destroy if it was initialized as draggable
        if ($btn.data('ui-draggable')) {
          $btn.draggable('destroy');   //Make the button undraggable
        }
      }
    }
  });
}

// Helper function to highlight all squares that contain the same unit as the one on the selected button
function selectUnit(board, selectedButton) {
  //Removes the selected class from all units on the board
  $('.unit.selected', board).each(function() {
    $(this).removeClass('selected');
  });
  const selectedUnit = selectedButton.data('units-array').pop();
  //Puts the unit picked up back in the array to allow the other functions to remove it
  selectedButton.data('units-array').push(selectedUnit);

  //Look at all buttons on the grid to find if they have the selected unit in their data
  board.find('.unit').each(function () {
    const $btn = $(this);   //Reference to the button
    const units = $btn.data('units-array') || [];   //Gets the units that are in that button
    if (units.includes(selectedUnit)) { //If this button has the selected unit
      $btn.addClass('selected'); //Highlight it
    }
  });
}

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
  $('html').css('--grid-size', GRID_SIZE);
  $('.game-board table') //Finds all game boards and targets the table inside it
  .each(function(index, item) {  //For every table inside game-board, this funtion will execute
    let gameBoard = $(item);  //Creating a variable that refers to the table
    const boardSize = GRID_SIZE;  //How big the board will be
    for (let row = 0; row < boardSize + 2; row++) { //Begins a for loop that starts at 0, increments by 1 each time 
                                                    //and goes until board size + 2
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
            //Adding the buttons to everything else
            rowElement.append('<td><button data-grid="'+alphabet[col-1]+row+'"></button></td>');  
          }       
        }
      }
      gameBoard.append(rowElement); //Adds the row that's just been created
    }
  });

  $('.game-board.opponent').on('click', 'button', function() { //Looks for any button inside game-board 
                                                               //and when it's clicked do this function
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
        // Tells the function 'handleResponse' that the user has made a turn on the opponent's board 
        // and a win message might need to be shown
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

    rotate() {
      // Swap width and length
      const tempLength = this.length;
      this.length = this.width;
      this.width = tempLength;
      // Toggle rotation state
      this.rotated = !this.rotated;
    }
  }

  if (typeof UNITS != "undefined") {
    // Add CSS for unit dimensions
    let unitStyles = '<style>';
    for (let i = 0; i < UNITS.length; i++) {
      const name = UNITS[i][0].toLowerCase();
      const width = UNITS[i][1];
      const length = UNITS[i][2];
      unitStyles += '.'+name+' { --unit-length: '+length+'; --unit-width: '+width+'; }';
    }
    unitStyles += '</style>';
    $('head').append(unitStyles);

    let $units = $('#units')

    // Set --cell-size on html so it's inherited everywhere
    const board = $('.game-board.setup');
    const cellSize = board.width() / (GRID_SIZE + 2);
    $('html').css('--cell-size', cellSize + 'px');

    for (let index = 0; index < UNITS.length; index++) {      // For each unit, adds it to the setup page
      let wrapper = $('<div class="unit"/>');   //Creates a wrapper to hold the radio button
      let unitName = UNITS[index][0];   //Assigns unitName to the first unit in the 'sea' category
      // Each unit is a radio button so that you can select it, it displays the name, width and length of the unit
      let radio = $('<input type="radio" id="'+unitName+'" name="unit" value="'+unitName+'" />');   
      let unit = new Unit(unitName, UNITS[index][1], UNITS[index][2], radio);   //Creates a unit instance
      radio.data('unit', unit);   //Attaches the unit to the radio button
      wrapper
        .append(radio)    //Adds the radio button to the wrapper
        //Creates a label holding the name, width and length of the unit (The part that displays on the screen)
        .append('<label for="'+unitName+'">' +
          '<img src="/static/img/sea/'+unitName.toLowerCase()+'.png" alt="'+unitName+'" class="unit-image '+unitName.toLowerCase()+'" />' +
          '<span>'+unitName+' ('+unit.width+','+unit.length+')</span>' +
          '</label>');
      $units.append(wrapper);   //Adds the wrapper the unit column
    }
    //Initiales an array on each button on the grid to hold the dropped units
    $('.game-board.setup button').each(function(index, item) {    
      $(item).data('units-array', []);   //The array
    });
  }

  $('.unit').draggable({  //defines what you can pick up
    helper: function() {  //helper wraps the item you grabbed into the thing you can move around
      //sets the variable "radio" as the radio button that's been grabbed
      const radio = $(this).find('input[type=radio]');  
      //select the unit being grabbed if it's not already been used
      if (!radio.is(':checked') && !radio.prop('disabled')) radio.prop('checked', true); 
      return createUnitDragHelper(radio.data('unit'));
    },
    cursor: "move", //changes the cursor to a "move" icon
    cursorAt: { left: 10, top: 10 },
    start: function(event, ui) { //method that is called before dragging can begin
      //sets the variable "radio" as the radio button that's been grabbed
      const radio = $(this).find('input[type=radio]'); 
      if (radio.prop('disabled')) { //if it has already been dragged succesfully then it will be disabled...
        return false; //so prevent dragging
      }
    }
  });

  $('.game-board.setup td').droppable({   //defines where you can drop (only on the grid)
    accept: ".unit",  //allows you to drop any of the units but nothing else
    tolerance: "pointer",
    over: function(event, ui){  //When a draggable enters a table cell, add a visual clue to the button.
      $(this).find('button').addClass('hover-shadow');
    },
    out: function(event, ui){ //Remove the visual clue when the draggable leaves
      $(this).find('button').removeClass('hover-shadow');
    },
    drop: function(event, ui) {   //method that is called when the unit is dropped
      const unit = ui.helper.data('unit');  //getting the reference of the unit
      const $place = $(this);   //where you dropped
      const width = unit.width;   //Creates the constant width as the units specific width
      const length = unit.length;   //Creates the constant length as the units specific length
      const board = $('.game-board.setup');   //Creates the constant board as the setup game board
      //Creates the constant currentSquare as the button you've dropped on
      const currentSquare = $place.find('button'); 
      //When the draggable is dropped, the hover shadow is removed   
      currentSquare.removeClass('hover-shadow');
      //Makes col the number associated to the letter that the unit was dropped on 
      //(A becomes 1, D becomes 4. Because of the +1)
      let col = alphabet.indexOf(currentSquare.data('grid').substring(0, 1)) + 1;   
      //Makes row equivalent to the number on the same line as the button dropped on
      let row = Number(currentSquare.data('grid').substring(1));
      // Add the unit image to the drop square (top-left)
      currentSquare.append('<img src="/static/img/sea/'+unit.name.toLowerCase()+'.png" alt="'+unit.name+'" ' +
        'class="placed-unit-image '+unit.name.toLowerCase()+(unit.rotated ? ' rotated' : '')+'" />');

      for (let y = 0; y < width; y++) {   //A for loop for the width of the unit
        if (row + y > GRID_SIZE) break;   //Prevents the units from appearing outside of the grid on the y axis
        for (let x = 0; x < length; x++) {    //A for loop for the length of the unit
          if (col + x > GRID_SIZE) break;   //Prevents the units from appearing outside of the grid on the x axis
          //Finds the square with the new grid refrences
          let square = board.find('*[data-grid="'+alphabet[col+x-1]+(row+y)+'"]');    
          square.addClass('unit');    //Making the new square a unit as well
          square.data('units-array').push(unit);    //Puts the new unit into the unit array for that square
          makeSquareDraggable(square);    //Making the square draggable so the unit can be moved around
        }
      }
      unit.radioButton.prop('disabled', true); //disable the unit so that it cannot be selected again
      unit.radioButton.prop('checked', false); //unselect the unit
      unit.radioButton.closest('.unit').addClass('opacity-50'); // Visual clue that unit is placed
      selectUnit(board, currentSquare);

      //If all the units are disabled (on the board)
      if ($('#units input[name="unit"]').length === $('#units input[name="unit"]:disabled').length) {  
        $('#play').prop('disabled', false); //Then renable
      }
    }
  });

  //This function is to remove the unit off the board when you pick it up
  //When you start moving a unit that's already on the board, do this function
  $('.game-board.setup').on('dragstart', '.unit', function (event, ui) {    
    //Creates a constant variable called draggedUnit that is the last unit to be placed down
    const draggedUnit = $(this).data('units-array').pop(); 
    //Puts the unit picked up back in the array to allow the other functions to remove it
     $(this).data('units-array').push(draggedUnit);   
    const board = $('.game-board.setup');
    removeUnitFromBoard(board, draggedUnit, function ($btn) {
      $btn.addClass('moving');
      // Remove the ship image from this button
      $btn.find('.placed-unit-image.'+draggedUnit.name.toLowerCase()).remove();
    });
  });

  //When you stop draggin a unit, remove evidence of where it used to be
  $('.game-board.setup').on('dragstop', '.moving', function () {
    const board = $('.game-board.setup');
    board.find('.moving').each(function() {
      //Takes away the blue squares 
      //(but if there's still a ship remaining then you still want that square to look like a unit)
      $(this).removeClass('moving');    
      if ($(this).data('units-array').length == 0) {    //If there are no ships left over then
        $(this).removeClass('unit');    //Remove the unit from the class
      //If all ships are gone from this square then it shouldn't look like a unit anymore
      }
    });
  });

  //When you click on the board, select a unit if there is one there
  $('.game-board.setup').on('click', 'button', function() { //Looks for any button inside game-board
    const board = $('.game-board.setup');
    const selectedButton = $(this);
    selectUnit(board, selectedButton);
  });

  //When you click the rotate button, it rotates the currently selected unit (if there is one)
  $('#rotate').click(function (e) {
    const board = $('.game-board.setup');
    const btn = $('.unit.selected', board)[0]; //Finds the first button with the selected class
    if (!btn) return; //If there isn't one, then do nothing

    // Finds the last unit placed on the selected button
    const selectedUnit = $(btn).data('units-array').pop();

    // Rotate the unit image on the button
    $(btn).find('.placed-unit-image.'+selectedUnit.name.toLowerCase()).toggleClass('rotated');

    selectedUnit.rotate();

    removeUnitFromBoard(board, selectedUnit, function ($btn, newUnits) {
      $btn.removeClass('selected');
      if (newUnits.length === 0) {
        $btn.removeClass('unit');
      }
    });

    // Re-place the unit at the same top-left position with new dimensions
    const grid = $(btn).data('grid');
    let col = alphabet.indexOf(grid.substring(0, 1)) + 1;
    let row = Number(grid.substring(1));

    // Re-add unit to all covered squares
    for (let y = 0; y < selectedUnit.width; y++) {
      if (row + y > GRID_SIZE) break;
      for (let x = 0; x < selectedUnit.length; x++) {
        if (col + x > GRID_SIZE) break;
        let square = board.find('*[data-grid="'+alphabet[col+x-1]+(row+y)+'"]');
        square.addClass('unit selected');
        square.data('units-array').push(selectedUnit);
        makeSquareDraggable(square);
      }
    }
  });

  // Only allowed to submit the form if there are no overlapping units and board is valid
  $('#play').click(function (e) {
    e.preventDefault(); // prevent default form submission initially

    let hasOverlap = false;
    $('.game-board.setup .unit').each(function() {
      if ($(this).data('units-array').length > 1) {    //If there are multiple units here
        hasOverlap = true;
        return false; // break out of the each loop
      }
    });

    if (hasOverlap) {
      alert('Cannot start game: Units are overlapping! Please rearrange your units so they do not overlap.');
      return;
    }

    // Build the board representation
    const board = [];
    for (let row = 1; row <= GRID_SIZE; row++) {
      const rowArray = [];
      for (let col = 0; col < GRID_SIZE; col++) {
        const coordinate = alphabet[col] + row;
        const $button = $('.game-board.setup').find('*[data-grid="'+coordinate+'"]');
        const units = $button.data('units-array') || [];

        if (units.length === 0) {
          rowArray.push('E'); // Empty
        } else {
          rowArray.push(units[0].name); // Unit name
        }
      }
      board.push(rowArray);
    }

    // Make call to validate the board
    $.ajax({
      url: '/validate-board',
      type: 'POST',
      contentType: 'application/json',
      dataType: 'json',
      data: JSON.stringify({
        gameId: GAME_ID,
        board: board
      }),
      success: function(response) {
        if (response.valid) {
          // Board is valid, turn off validation and submit the form
          $('#play-form').off('submit').submit();
        } else {
          // Board is invalid, show error message
          alert('Invalid board configuration: ' + (response.message || 'Please check your unit placement.'));
        }
      }
    });
  })
});
