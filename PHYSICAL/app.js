// Logic for services of SGCS  which is linked to the HTML script index.html

// Initialize Firebase
var firebaseConfig = {
 apiKey: "AIzaSyBUb98MeV2a0PcPvlPCM7OHg2MWrbJGUnI",
 authDomain: "sgcs-1f60d.firebaseapp.com",
 databaseURL: "https://sgcs-1f60d-default-rtdb.firebaseio.com",
 projectId: "sgcs-1f60d",
 storageBucket: "sgcs-1f60d.appspot.com",
 messagingSenderId: "245357317439",
 appId: "1:245357317439:web:c4b61061718497772f578a",
 measurementId: "G-DM72ERDD2W"
 };
 firebase.initializeApp(firebaseConfig);


 // Reference to your Firebase database, Sensor_Data contains data from the physical entity.
 var db = firebase.database().ref('Sensor_Data');

 // Set up a listener for real-time data updates
 db.on('value', function(snapshot) {
   var data = snapshot.val();

  // Local variables to extract data for charting
  var labels = [];
  var times = [];
  var Temperature_Organic = []; var Temperature_PMD = []; var Temperature_Paper = [];
  var Humidity_Organic = [];var Humidity_PMD = [];var Humidity_Paper = [];
  var Distance_Organic = []; var Distance_PMD = []; var Distance_Paper = [];

  // Loop through the latest 30 subnodes and extract data
 var keys = Object.keys(data).slice(-30); // Get the latest 30 keys
 keys.forEach(function(key) {
   labels.push(key);                
   times.push(data[key].Timestamp);      
   Temperature_Organic.push(data[key]['Temperature_Organic']);
   Temperature_PMD.push(data[key]['Temperature_PMD']);
   Temperature_Paper.push(data[key]['Temperature_Paper']);
   Humidity_Organic.push(data[key]['Humidity_Organic']);
   Humidity_PMD.push(data[key]['Humidity_PMD']); 
   Humidity_Paper.push(data[key]['Humidity_Paper']); 
   Distance_Organic.push(data[key]['Distance_Organic']);
   Distance_PMD.push(data[key]['Distance_PMD']);
   Distance_Paper.push(data[key]['Distance_Paper']);
 });
  
 // Upload latest value in the Real-time section
 document.getElementById("Temperature_Organic").innerHTML = Temperature_Organic[Temperature_Organic.length - 1]+ "C";
 document.getElementById("Humidity_Organic").innerHTML = Humidity_Organic[Humidity_Organic.length - 1]+ "%";
 document.getElementById("Distance_Organic").innerHTML = Distance_Organic[Distance_Organic.length - 1]+ "cm";

 document.getElementById("Temperature_PMD").innerHTML = Temperature_PMD[Temperature_PMD.length - 1]+ "C";
 document.getElementById("Humidity_PMD").innerHTML = Humidity_PMD[Humidity_PMD.length - 1]+ "%";
 document.getElementById("Distance_PMD").innerHTML = Distance_PMD[Distance_PMD.length - 1]+ "cm";

 document.getElementById("Temperature_Paper").innerHTML = Temperature_Paper[Temperature_Paper.length - 1]+ "C";
 document.getElementById("Humidity_Paper").innerHTML = Humidity_Paper[Humidity_Paper.length - 1]+ "%";
 document.getElementById("Distance_Paper").innerHTML = Distance_Paper[Distance_Paper.length - 1]+ "cm";
 
  // Change the fill level (0 to 100) to update the cylinder graphic
  var fillLevelOrganic = Distance_Organic[Distance_Organic.length - 1]; // Vary this value to change the fill level
  if(fillLevelOrganic>100){fillLevelOrganic=100;}
  var fillHeightOrganic = fillLevelOrganic + "%";
  document.getElementById("fillLevelOrganic").style.setProperty("--fill-height", fillHeightOrganic);

  var fillLevelPMD = Distance_PMD[Distance_PMD.length - 1]; // Vary this value to change the fill level
  if(fillLevelPMD>100){fillLevelPMD=100;}
  var fillHeightPMD = fillLevelPMD + "%";
  document.getElementById("fillLevelPMD").style.setProperty("--fill-height", fillHeightPMD);

  var fillLevelPaper = Distance_Paper[Distance_Paper.length - 1]; // Vary this value to change the fill level
  if(fillLevelPaper>100){fillLevelPaper=100;}
  var fillHeightPaper = fillLevelPaper + "%";
  document.getElementById("fillLevelPaper").style.setProperty("--fill-height", fillHeightPaper);


   // Temperature Organic chart using Chart.js
   var ctx2 = document.getElementById('dataChart1').getContext('2d');
   new Chart(ctx2, {
     type: 'line', // Use a different chart type if desired
     data: {
       labels: times,
       datasets: [{
         label: 'Temperature Organic',
         data: Temperature_Organic,
         borderColor: 'green',
         backgroundColor: 'rgba(0, 255, 0, 0.1)',
       }]
     },
   });

   // Temperature PMD chart using Chart.js
   var ctx2 = document.getElementById('dataChart2').getContext('2d');
   new Chart(ctx2, {
     type: 'line', // Use a different chart type if desired
     data: {
       labels: times,
       datasets: [{
         label: 'Temperature PMD',
         data: Temperature_PMD,
         borderColor: 'orange',
         backgroundColor: 'rgba(255, 165, 0, 0.1)',
       }]
     },
   });

   // Temperature Paper chart using Chart.js
   var ctx2 = document.getElementById('dataChart3').getContext('2d');
   new Chart(ctx2, {
     type: 'line', // Use a different chart type if desired
     data: {
       labels: times,
       datasets: [{
         label: 'Temperature Paper',
         data: Temperature_Paper,
         borderColor: 'blue',
         backgroundColor: 'rgba(0, 0, 255, 0.1)',
       }]
     },
   });


   // Humidity Organic chart using Chart.js
   var ctx = document.getElementById('dataChart4').getContext('2d');
   new Chart(ctx, {
     type: 'line',
     data: {
       labels: times,
       datasets: [{
         label: 'Humidity Organic',
         data: Humidity_Organic,
         borderColor: 'green',
         backgroundColor: 'rgba(0, 255, 0, 0.1)',
       }]
     },
   });

   // Humidity PMD chart using Chart.js
   var ctx2 = document.getElementById('dataChart5').getContext('2d');
   new Chart(ctx2, {
     type: 'line', // Use a different chart type if desired
     data: {
       labels: times,
       datasets: [{
         label: 'Humidity PMD',
         data: Humidity_PMD,
         borderColor: 'orange',
         backgroundColor: 'rgba(255, 165, 0, 0.1)',
       }]
     },
   });

   // Humidity Paper chart using Chart.js
   var ctx2 = document.getElementById('dataChart6').getContext('2d');
   new Chart(ctx2, {
     type: 'line', // Use a different chart type if desired
     data: {
       labels: times,
       datasets: [{
         label: 'Humidity Paper',
         data: Humidity_Paper,
         borderColor: 'blue',
         backgroundColor: 'rgba(0, 0, 255, 0.1)',
       }]
     },
   });

   // Distance Organic chart using Chart.js
   var ctx = document.getElementById('dataChart7').getContext('2d');
   new Chart(ctx, {
     type: 'line',
     data: {
       labels: times,
       datasets: [{
         label: 'Distance Organic',
         data: Distance_Organic,
         borderColor: 'green',
         backgroundColor: 'rgba(0, 255, 0, 0.1)',
       }]
     },
   });

   // Distance PMD chart using Chart.js
   var ctx2 = document.getElementById('dataChart8').getContext('2d');
   new Chart(ctx2, {
     type: 'line', // Use a different chart type if desired
     data: {
       labels: times,
       datasets: [{
         label: 'Distance PMD',
         data: Distance_PMD,
         borderColor: 'orange',
         backgroundColor: 'rgba(255, 165, 0, 0.1)',
       }]
     },
   });

   // Distance Paper chart using Chart.js
   var ctx2 = document.getElementById('dataChart9').getContext('2d');
   new Chart(ctx2, {
     type: 'line', // Use a different chart type if desired
     data: {
       labels: times,
       datasets: [{
         label: 'Distance Paper',
         data: Distance_Paper,
         borderColor: 'blue',
         backgroundColor: 'rgba(0, 0, 255, 0.1)',
       }]
     },
   });


// Function to populate the table with data from Firebase
//The function loops through all child nodes for the given input parent node
function populateTableWithFirebaseData(childKey) {
  path = "Result/" + childKey;
  var occupy = firebase.database().ref(path);
    occupy.once("value")
        .then(function(snapshot) {
            const data = snapshot.val(); // Retrieve the data from Firebase

            // Create a new table element
            var table = document.createElement("table");
            // Apply CSS styles for borders and spacing
            table.style.border = "1px solid #ccc"; // Border style
            table.style.borderCollapse = "collapse"; // Border-collapse
            table.style.margin = "20px"; // Margin
            table.style.padding = "10px"; // Padding

            // Create table caption (heading for the entire table)
            const caption = document.createElement("caption");
            // Apply CSS style for bold text
            caption.style.fontWeight = "bold";
            caption.style.fontSize = "22px"; 
            caption.textContent = childKey; // Replace with your desired caption text
            table.appendChild(caption);

            // Create table headers (optional)
            const headerRow = table.insertRow();
            var headers = ["House", "Organic(kg)", "PMD(kg)", "Paper(kg)", "Total Waste(kg)", "Rank"];
            var keys = ["Organic", "PMD", "Paper", "Total", "Rank"]; // Must exactly match the key values stored in the database
            for (let i = 0; i < headers.length; i++) {
                const headerCell = headerRow.insertCell();
                headerCell.textContent = headers[i];
                // Apply CSS styles for header cells
                headerCell.style.fontWeight = "bold";
                headerCell.style.border = "1px solid #ddd"; // Border style for headers
                headerCell.style.padding = "8px"; // Padding for headers
                headerCell.style.textAlign = "center"; 
            }

            // Create table rows and populate with Firebase data
            for (let key in data) {
                if (data.hasOwnProperty(key)) {
                    if (Object.keys(data).indexOf(key) < Object.keys(data).length - 2) // Ignore last two childern nodes(total & result)
                    {
                      const row = table.insertRow();
                      const cell = row.insertCell();
                      cell.textContent = key; // key refers to the Houses
                      // Apply CSS styles for names of children nodes
                      cell.style.border = "1px solid #ddd"; // Border style for data cells
                      cell.style.padding = "8px"; // Padding for data cells
                      cell.style.textAlign = "center";
                      if(data[key]["Rank"] == '1'){cell.style.backgroundColor = "green"; }// Change background colour for House ranked 1

                      for (let i = 0; i < headers.length-1; i++) {
                          const cell = row.insertCell();
                          if(data[key]["Rank"] == '1'){cell.style.backgroundColor = "green"; }// Change background colour for House ranked 1

                          // Pie- chart data collection for House Ranked 1
                          if(keys[i] == "Rank"){
                            if(data[key][keys[i]] == '1' && flag ==0)
                            {
                                pie_data.push(parseInt(data[key][keys[i-4]],10)); // Organic weight
                                pie_data.push(parseInt(data[key][keys[i-3]],10)); // PMD weight
                                pie_data.push(parseInt(data[key][keys[i-2]],10)); // Paper weight
                                flag = 1;
                                pieChartGeneration(); // Function to generate pie-chart
                            }
                            cell.textContent = (data[key][keys[i]]); 
                          }
                          else{
                          cell.textContent = (data[key][keys[i]])/1000; 
                          }
                          // Apply CSS styles for data cells
                          cell.style.border = "1px solid #ddd"; // Border style for data cells
                          cell.style.padding = "8px"; // Padding for data cells
                          cell.style.textAlign = "center";
                          if(data[key][keys[i]] == '1'){cell.style.backgroundColor = "green"; }
                      }
                  }
                }
              }
            // Append the table to the container
            document.getElementById("rank-table-container").appendChild(table);
        })
        .catch(function(error) {
            console.error("Error reading data from Firebase: " + error);
        });
}

let flag = 0; // Variable to generate only one pie-chart
let pie_data = []; // Variable to store pie-chart data
var parentRef = firebase.database().ref("Data");
// Using once() method to fetch the child keys
parentRef.once("value")
  .then(function(snapshot) {
    if (snapshot.exists()) {
      // Get an array of child keys
      var childKeys = Object.keys(snapshot.val()); // childKeys will now contain ["child1", "child2"]
      // You can iterate through childKeys to access each child node
      childKeys.forEach(function(childKey) {
        populateTableWithFirebaseData(childKey); // Sending each 'Neighbourhood' to genrate tables.
      });
    } 
    else {
      console.log("No data found in the parent node.");
    }
  })
  .catch(function(error) {
    console.error("Error fetching data: " + error);
  });


// Function to generate a pie-chart
function pieChartGeneration(){
  var data = {
    labels: ['Organic', 'PMD', 'Paper'],
    datasets: [{
        data: pie_data, // Values for each section of the pie chart
        backgroundColor: ['#228B22', '#FF9A00', '#5733FF'], // Colors for each section
      }]
    };

  // Get the canvas element and initialize the pie chart
  var ctx = document.getElementById('myPieChart').getContext('2d');
  var myPieChart = new Chart(ctx, {
      type: 'pie',
      data: data,
      options: {
        responsive: true, // Makes the chart responsive to container size
        title: {
          display: true,
          text: 'House', // Replace with your desired title text
          fontSize: 88, // Font size for the title
          fontStyle: 'bold', // Font style for the title
        },
    }
  });
}


 });


  
