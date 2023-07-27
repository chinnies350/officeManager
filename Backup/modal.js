// active user name getting
var activeUserName = userName();
// workspace name get
var workSpaceName = workSpaceName();
function modalFunction() {
    let obj = {};
    obj.groupName = document.getElementById("groupName").value;
    obj.Description = document.getElementById("groupDescription").value;
    obj.task = "createGroup";
    obj.workSpaceName = workSpaceName;
    // obj.Admin = sessionStorage.getItem("userName");
    obj.Admin = activeUserName;
    var x = document.getElementById("groupName").value;
    var y = document.getElementById("groupDescription").value;

    if (x !== "") {
        let jsonStringObj = JSON.stringify(obj);
        document.getElementById("groupName").value = '';
        document.getElementById("groupDescription").value = '';
        socket.send(jsonStringObj)
        location.reload();
    }
    else {
        document.getElementById("groupName").value = '';
        document.getElementById("groupDescription").value = '';
        alert("please fill the empty area")
    }
}

var input = document.getElementById("groupName");
var input1 = document.getElementById("groupDescription")
input.addEventListener("keyup", function (event) {
    if (event.keyCode === 13) {
        event.preventDefault();
        document.getElementById("btn").click();
    }
});


function addUserFunction() {
    let obj = {};
    // obj.requestingUser = sessionStorage.getItem("userName");
    obj.requestingUser = activeUserName;
    obj.addUserName = document.getElementById("addUserName").value;
    obj.groupName = $('.tab-content .active').attr('id').replace("-","");
    obj.task = "addUserToGroup";

    if (document.getElementById("addUserName").value !== "") {
        let jsonStringObj = JSON.stringify(obj);
        socket.send(jsonStringObj)
        document.getElementById('addUserName').value = '';
        location.reload();
    }
    else {
        return false;
    }
}


function addUserFromModal(activeUserName, addingUser) {
    id = addingUser.concat("-data")
    let obj = {};
    // obj.requestingUser = sessionStorage.getItem("userName");
    obj.requestingUser = activeUserName;
    obj.addUserName = $('#'+id).text();
    obj.groupName = $('.tab-content .active').attr('id').replace("-","");
    obj.task = "addUserToGroup";

    if (addUserName !== "") {
        let jsonStringObj = JSON.stringify(obj);
        console.log(jsonStringObj)
        socket.send(jsonStringObj)
        location.reload();
    }
    else {
        return false;
    }
}



function addUserToWorkSpace() {
    let obj = {};
    obj.task = "addUserToWorkSpace";
    obj.requestingUser = activeUserName;
    obj.workSpaceName = workSpaceName;
    obj.addUserMail = document.getElementById("email").value;

    if (document.getElementById("email").value !== "") {
        let jsonStringObj = JSON.stringify(obj);
        socket.send(jsonStringObj)
        document.getElementById('email').value = '';
        location.reload();
    }
    else {
        return false;
    }


}