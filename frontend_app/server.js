const express = require("express");
const http = require('http');
const socket_io = require('socket.io');
const path = require("path");
const axios = require('axios');

const Server=socket_io.Server;
const Socket = socket_io.Socket;

const app = express();
const server = http.createServer(app);
const io = new Server(server);

app.use(express.static(path.join(__dirname, "./public")));

io.on("connection", (socket) => {
  console.log("A user connected");

  socket.on("disconnect", () => {
    console.log("User disconnected");
  });

  socket.on("chat message", async (msg) => {
    console.log("message: " + msg);
  
    // Emit user's message
    io.emit("chat message", "You: " + msg);
  
    try {
      // Send request to the API endpoint /ask with the message
      const apiResponse = await axios.post('http://<api-link>/ask', {
        question: msg
      });
  
      // Extract the response from the API's response object
      const aiResponse = apiResponse.data.response;
  
      // Emit the AI's response to the client
      io.emit("chat message", "AI: " + aiResponse);
  
    } catch (error) {
      console.error("Error fetching response from API:", error);
      io.emit("chat message", "AI: Sorry, I couldn't process your request.");
    }
  });
});

app.get("/", (req, res) => {
  res.sendFile(path.join(__dirname, "../public", "index.html"));
});

const PORT = process.env.PORT || 3000;

server.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});