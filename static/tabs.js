function openCity(evt, cityName) {
    // Declare all variables
    var i, tabcontent, tablinks;
  
    // Get all elements with class="tabcontent" and hide them
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
      tabcontent[i].style.display = "none";
    }
  
    // Get all elements with class="tablinks" and remove the class "active"
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
      tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
  
    // Show the current tab, and add an "active" class to the button that opened the tab
    document.getElementById(cityName).style.display = "block";
    evt.currentTarget.className += " active";
  }

function tabs2(evt, cityName) {
    // Declare all variables
    var i, tabkontent, tabgaming;
  
    // Get all elements with class="tabkontent" and hide them
    tabkontent = document.getElementsByClassName("tabkontent");
    for (i = 0; i < tabkontent.length; i++) {
      tabkontent[i].style.display = "none";
    }
  
    // Get all elements with class="tabgaming" and remove the class "active"
    tabgaming = document.getElementsByClassName("tabgaming");
    for (i = 0; i < tabgaming.length; i++) {
      tabgaming[i].className = tabgaming[i].className.replace(" active", "");
    }
  
    // Show the current tab, and add an "active" class to the button that opened the tab
    document.getElementById(cityName).style.display = "block";
    evt.currentTarget.className += " active";
  }

function bwTabs(evt, cityName) {
    // Declare all variables
    var i, bwTabContent, bwTabLinks;
  
    // Get all elements with class="bwTabContent" and hide them
    bwTabContent = document.getElementsByClassName("bwTabContent");
    for (i = 0; i < bwTabContent.length; i++) {
      bwTabContent[i].style.display = "none";
    }
  
    // Get all elements with class="bwTabLinks" and remove the class "active"
    bwTabLinks = document.getElementsByClassName("bwTabLinks");
    for (i = 0; i < bwTabLinks.length; i++) {
      bwTabLinks[i].className = bwTabLinks[i].className.replace(" active", "");
    }
  
    // Show the current tab, and add an "active" class to the button that opened the tab
    document.getElementById(cityName).style.display = "block";
    evt.currentTarget.className += " active";
  }

document.getElementById("defaultOpen").click();
document.getElementById("defaultOpen2").click();
document.getElementById("defaultOpenBw").click();