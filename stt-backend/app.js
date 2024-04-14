import express from 'express';
import { dirname } from 'path';
import { fileURLToPath } from 'url';
import net from 'net';

// Connect to the TCP server
const serverIP = '20.197.52.56';
const serverPort = 3001;
const clientSocket = new net.Socket();

const __dirname = dirname(fileURLToPath(import.meta.url));
const app = express();

// Set up EJS as the view engine
app.set('view engine', 'ejs');
app.set('views', `${__dirname}/views`);

// Serve static files from the 'public' directory
app.use(express.static(`${__dirname}/public`));
app.use(express.json());

// Route for the homepage
app.get('/', (req, res) => {
    res.render('index');
});

app.post('/speech-to-text', (req, res) => {
    // const encoder = new TextEncoder();
    // const byteArray = encoder.encode(req.body);
    console.log(req.body);
    clientSocket.write(JSON.stringify(req.body));
    return res.send('Data received successfully');
})

clientSocket.connect(serverPort, serverIP, () => {
    console.log('Connected to TCP server!');
});

clientSocket.on('error', error => {
    console.error('Socket error:', error);
});

clientSocket.on('close', () => {
    console.log('Connection to TCP server closed.');
});

app.listen(3000, () => {
    console.log('Express server listening on port 3000');
});

