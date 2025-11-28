const express = require('express');
const cors = require('cors');
const axios = require('axios');
require('dotenv').config()

const app = express();
const port = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());

async function callYourAIPipeline(input) {
    //TODO: Replace this with actuall call to your hosted AI service
    //this could be:
    // -HTTP Call to your model endpoint
    // - databse lookup + processing
    // - calling a python script


    console.log("Processing: ", input)

    return  `Processed: ${input} + AI Maic`
}

app.post('/api/predict', async (req, res) => {
    try {
        const { input, parameters } = req.body;

        const result = await callYourAIPipeline(input);

        res.json({
            success: true,
            output: result,
            timestamp: new Date().toISOString()

        });
    } catch(error) {
        console.error('AI Pipeline error:', error);
        res.status(500).json({
            success: false,
            error: error.message
        });
    }

});

app.get('/', (req, rest) => {
    res.json({ status: 'AI wrapper ready - POST to /api/predict'});

});

app.listen(port, () => {
    console.log(`AI wrapper running on http://localhost:${port}`);
});