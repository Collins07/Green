let searchField4 = document.querySelector("#searchField4");

const appTable = document.querySelector(".app-table");

const tbody = document.querySelector(".table-body")

const paginationTable = document.querySelector("#pagination");

const tableOutput = document.querySelector(".table-output");
tableOutput.style.display = "none"


searchField4.addEventListener("keyup", (e) =>{
  const searchValue = e.target.value;

  if(searchValue.trim().length>0){
    paginationTable.style.display = "none"
    tbody.innerHTML = "";
   

    fetch("/forests/search-difference",{
        body: JSON.stringify({searchText: searchValue}),
        method:"POST",
  
    })
    .then(res=>res.json())
    .then(data=>{
        console.log("data", data);

        appTable.style.display = "none"

        tableOutput.style.display = "block"

        console.log("data.length", data.length);

        if (data===0){
            tableOutput.innerHTML = 'No results found !!'
        }
        else{
            data.forEach((item) => {

                tbody.innerHTML +=  `
                
                <tr> 
                <td>${item.description}</td>  
                <td>${item.trees_difference}</td>  
                <td>${item.percentage}</td> 
                </tr> 
                
                `;

        });

    }   
        
    });
  }
  else{
    appTable.style.display = "block"
    paginationTable.style.display = "block"
    tableOutput.style.display = "none"
  }
});