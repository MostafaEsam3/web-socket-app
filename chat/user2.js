var username = prompt("What is your name ")
var chatpage = document.getElementById('page')
var userheader = document.getElementById("SendUS")
var chatmessage = document.getElementById("meesage_to_user")
var sendmessage = document.getElementById("send_to")

userheader.innerHTML= `Hello ${username}`


let mywebsocket = new WebSocket("ws://localhost:8800")
console.log(mywebsocket)


mywebsocket.onopen=function (){
    console.log("connection opened")

    data_to_send ={
        username : username,
        type: "login"
    }

    data = JSON.stringify(data_to_send)
    this.send(data)
}


mywebsocket.onerror=function (){
    console.log("error happened ")
}


mywebsocket.onmessage= function (event){
    console.log("message received")
    console.log(event.data, typeof data)
    msg= JSON.parse(event.data)
    msg_color = msg.color
    newmessag= `<span style="color: ${msg_color} "> ${msg['content']} </span> </br>`
    chatpage.innerHTML +=newmessag
}



sendmessage.addEventListener("click", function (){
    mymessage = chatmessage.value
    chatmessage.value = ''
    console.log(mymessage)
    msgobj= {
        type: "chat",
        username: username,
        body: mymessage+"\n"

    }

    msgobj = JSON.stringify(msgobj)
    mywebsocket.send(msgobj)

})