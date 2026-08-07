const API_URL = "http://127.0.0.1:52440/students";



function loadStudents(){


fetch(API_URL)


.then(response => response.json())


.then(data => {


let rows = "";


data.forEach(student => {


rows += `

<tr>

<td>${student.id}</td>

<td>${student.name}</td>

<td>${student.email}</td>

<td>${student.course}</td>


<td>

<button onclick="deleteStudent(${student.id})">

Delete

</button>

</td>


</tr>

`;



});


document.getElementById("students").innerHTML = rows;


})


.catch(error=>{

console.log(error);

});



}





function addStudent(){



let student = {


name: document.getElementById("name").value,


email: document.getElementById("email").value,


course: document.getElementById("course").value


};




fetch(API_URL,{


method:"POST",


headers:{


"Content-Type":"application/json"


},


body:JSON.stringify(student)



})


.then(response=>response.json())


.then(data=>{


alert(data.message);


loadStudents();



})


.catch(error=>{


console.log(error);


alert("Failed to add student");


});



}






function deleteStudent(id){



fetch(API_URL + "/" + id,{


method:"DELETE"


})


.then(response=>response.json())


.then(data=>{


alert(data.message);


loadStudents();



});



}




loadStudents();