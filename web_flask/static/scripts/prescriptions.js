
  // Get the dropdown element
  var dropdown = document.getElementById("dropdown");

  // Add event listener to the dropdown
  dropdown.addEventListener("change", function() {
    // Get the selected value
    var selectedValue = dropdown.value;

    // Perform actions based on the selected value
    if (selectedValue === "option1") {
      // Action for Option 1
      console.log("Option 1 selected");
    } else if (selectedValue === "option2") {
      // Action for Option 2
      console.log("Option 2 selected");
    } else if (selectedValue === "option3") {
      // Action for Option 3
      console.log("Option 3 selected");
    }
  });


  
  var input = document.getElementById("dateInput");
    var dropdown = document.getElementById("calendarDropdown");

    // Show/hide the dropdown when input is clicked
    input.addEventListener("click", function() {
      dropdown.style.display = dropdown.style.display === "block" ? "none" : "block";
    });

    // Handle date selection
    dropdown.addEventListener("click", function(event) {
      var selectedDateTime = event.target.dataset.datetime;
      input.value = selectedDateTime;
      dropdown.style.display = "none";
    });

    // Generate calendar content
    var today = new Date();
    var year = today.getFullYear();
    var month = today.getMonth();

    function generateCalendar(year, month) {
      var firstDay = new Date(year, month, 1);
      var lastDay = new Date(year, month + 1, 0);
      var daysInMonth = lastDay.getDate();
      var startDay = firstDay.getDay();

      var calendarHTML = "<div class='month-year'>";
      calendarHTML += "<button onclick='prevMonth()'>Previous</button>";
      calendarHTML += "<select id='monthSelect' onchange='changeMonth()'>";
      for (var i = 0; i < 12; i++) {
        calendarHTML += "<option value='" + i + "'" + (i === month ? " selected" : "") + ">" + monthName(i) + "</option>";
      }
      calendarHTML += "</select>";
      calendarHTML += "<select id='yearSelect' onchange='changeYear()'>";
      for (var i = year - 10; i <= year + 10; i++) {
        calendarHTML += "<option value='" + i + "'" + (i === year ? " selected" : "") + ">" + i + "</option>";
      }
      calendarHTML += "</select>";
      calendarHTML += "<button onclick='nextMonth()'>Next</button>";
      calendarHTML += "</div>";

      calendarHTML += "<table>";
      calendarHTML += "<tr><th colspan='7'>" + monthName(month) + " " + year + "</th></tr>";
      calendarHTML += "<tr><th>Sun</th><th>Mon</th><th>Tue</th><th>Wed</th><th>Thu</th><th>Fri</th><th>Sat</th></tr>";
      calendarHTML += "<tr>";

      // Fill in blank cells until the first day of the month
      for (var i = 0; i < startDay; i++) {
        calendarHTML += "<td></td>";
      }

      // Fill in the days of the month
      var day = 1;
      for (var i = startDay; i < 7; i++) {
        calendarHTML += "<td onclick='selectDateTime(" + day + ")' data-datetime='" + formatDateTime(year, month, day) + "'>" + day + "</td>";
        day++;
      }

      calendarHTML += "</tr>";

      // Fill in the remaining days of the month
      while (day <= daysInMonth) {
        calendarHTML += "<tr>";
        for (var i = 0; i < 7 && day <= daysInMonth; i++) {
          calendarHTML += "<td onclick='selectDateTime(" + day + ")' data-datetime='" + formatDateTime(year, month, day) + "'>" + day + "</td>";
          day++;
        }
        calendarHTML += "</tr>";
      }

      calendarHTML += "</table>";
      dropdown.innerHTML = calendarHTML;
    }

    function monthName(month) {
      var monthNames = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
      return monthNames[month];
    }

    function formatDateTime(year, month, day) {
      var selectedDate = new Date(year, month, day);
      var formattedDate = selectedDate.toLocaleString(undefined, { day: 'numeric', month: 'long', year: 'numeric', hour: 'numeric', minute: 'numeric' });
      return formattedDate;
    }

    function selectDateTime(day) {
      var selectedDate = new Date(year, month, day);
      input.value = formatDateTime(year, month, day);
      dropdown.style.display = "none";
    }

    function prevMonth() {
      month--;
      if (month < 0) {
        month = 11;
        year--;
      }
      generateCalendar(year, month);
    }

    function nextMonth() {
      month++;
      if (month > 11) {
        month = 0;
        year++;
      }
      generateCalendar(year, month);
    }

    function changeMonth() {
      month = parseInt(document.getElementById("monthSelect").value);
      generateCalendar(year, month);
    }

    function changeYear() {
      year = parseInt(document.getElementById("yearSelect").value);
      generateCalendar(year, month);
    }

    generateCalendar(year, month);

    document.addEventListener('DOMContentLoaded', function() {
      var addButton = document.getElementById('addButton');
      var cardPopup = document.getElementById('cardPopup');
    
      addButton.addEventListener('click', function(event) {
        event.preventDefault();
        cardPopup.classList.remove('hidden');
      });
    });