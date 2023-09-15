const express = require('express');
const path = require('path');

const app = express();
const PORT = 3000;

// Servir arquivos estáticos a partir da pasta 'public'
app.use(express.static(path.join(__dirname, 'public')));


app.listen(PORT, () => {
    console.log(`Client server running on http://localhost:${PORT}`);
});
