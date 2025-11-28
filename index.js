const express = require('express');
const cors = require('cors');
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const { pool, initDB } = require('./database');
require('dotenv').config();

const app = express();
const port = process.env.PORT || 3000;
const JWT_SECRET = process.env.JWT_SECRET;

app.use(cors());
app.use(express.json());

// Initialize database on startup
initDB();

// Middleware to verify JWT token
const authenticateToken = (req, res, next) => {
  const authHeader = req.headers['authorization'];
  const token = authHeader && authHeader.split(' ')[1]; // Bearer TOKEN

  if (!token) {
    return res.status(401).json({ error: 'Access token required' });
  }

  jwt.verify(token, JWT_SECRET, (err, user) => {
    if (err) return res.status(403).json({ error: 'Invalid token' });
    req.user = user;
    next();
  });
};

// Your AI pipeline function
async function callYourAIPipeline(input) {
  // TODO: Replace with your actual AI service
  console.log('🤖 AI Processing:', input);
  return `AI analyzed: "${input}" - This would be your AI model output`;
}

// ===== AUTHENTICATION ROUTES =====
app.post('/api/auth/register', async (req, res) => {
  try {
    const { email, password, name } = req.body;
    
    if (!email || !password) {
      return res.status(400).json({ error: 'Email and password required' });
    }

    const passwordHash = await bcrypt.hash(password, 12);
    
    const result = await pool.query(
      'INSERT INTO users (email, password_hash, name) VALUES ($1, $2, $3) RETURNING id, email, name, created_at',
      [email, passwordHash, name]
    );
    
    res.json({ 
      success: true,
      user: result.rows[0] 
    });
  } catch (error) {
    if (error.code === '23505') { // Unique violation
      res.status(400).json({ error: 'Email already exists' });
    } else {
      res.status(500).json({ error: error.message });
    }
  }
});

app.post('/api/auth/login', async (req, res) => {
  try {
    const { email, password } = req.body;
    
    const result = await pool.query(
      'SELECT * FROM users WHERE email = $1',
      [email]
    );
    
    if (result.rows.length === 0) {
      return res.status(401).json({ error: 'Invalid credentials' });
    }
    
    const user = result.rows[0];
    const validPassword = await bcrypt.compare(password, user.password_hash);
    
    if (!validPassword) {
      return res.status(401).json({ error: 'Invalid credentials' });
    }
    
    const token = jwt.sign(
      { id: user.id, email: user.email }, 
      JWT_SECRET, 
      { expiresIn: '24h' }
    );
    
    res.json({
      success: true,
      token,
      user: {
        id: user.id,
        email: user.email,
        name: user.name
      }
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// ===== CLIENT ROUTES =====
app.post('/api/clients', authenticateToken, async (req, res) => {
  try {
    const { name, email, phone, company } = req.body;
    const result = await pool.query(
      `INSERT INTO clients (name, email, phone, company, created_by) 
       VALUES ($1, $2, $3, $4, $5) RETURNING *`,
      [name, email, phone, company, req.user.id]
    );
    res.json({ success: true, client: result.rows[0] });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.get('/api/clients', authenticateToken, async (req, res) => {
  try {
    const result = await pool.query(
      'SELECT * FROM clients WHERE created_by = $1 ORDER BY created_at DESC',
      [req.user.id]
    );
    res.json({ success: true, clients: result.rows });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// ===== DOCUMENT ROUTES WITH AI =====
app.post('/api/documents', authenticateToken, async (req, res) => {
  try {
    const { client_id, template_id, name, content } = req.body;
    
    // Use AI to enhance document content
    const ai_generated_content = await callYourAIPipeline(content);
    
    const result = await pool.query(
      `INSERT INTO documents (client_id, template_id, name, content, ai_generated_content, created_by) 
       VALUES ($1, $2, $3, $4, $5, $6) RETURNING *`,
      [client_id, template_id, name, content, ai_generated_content, req.user.id]
    );
    
    res.json({ success: true, document: result.rows[0] });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.get('/api/documents', authenticateToken, async (req, res) => {
  try {
    const result = await pool.query(
      `SELECT d.*, c.name as client_name 
       FROM documents d 
       JOIN clients c ON d.client_id = c.id 
       WHERE d.created_by = $1 
       ORDER BY d.created_at DESC`,
      [req.user.id]
    );
    res.json({ success: true, documents: result.rows });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// ===== COMPLIANCE DEADLINES =====
app.post('/api/deadlines', authenticateToken, async (req, res) => {
  try {
    const { client_id, title, description, deadline_date, priority } = req.body;
    const result = await pool.query(
      `INSERT INTO compliance_deadlines (client_id, title, description, deadline_date, priority, assigned_to) 
       VALUES ($1, $2, $3, $4, $5, $6) RETURNING *`,
      [client_id, title, description, deadline_date, priority, req.user.id]
    );
    res.json({ success: true, deadline: result.rows[0] });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.get('/api/deadlines/upcoming', authenticateToken, async (req, res) => {
  try {
    const result = await pool.query(
      `SELECT cd.*, c.name as client_name 
       FROM compliance_deadlines cd
       JOIN clients c ON cd.client_id = c.id
       WHERE cd.assigned_to = $1 AND cd.deadline_date >= CURRENT_DATE
       ORDER BY cd.deadline_date ASC
       LIMIT 10`,
      [req.user.id]
    );
    res.json({ success: true, deadlines: result.rows });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// ===== HEALTH CHECK =====
app.get('/', (req, res) => {
  res.json({ 
    status: 'Compliance AI Backend Running', 
    database: 'Neon PostgreSQL',
    timestamp: new Date().toISOString()
  });
});

app.get('/api/health', async (req, res) => {
  try {
    await pool.query('SELECT 1');
    res.json({ 
      status: 'OK', 
      database: 'Connected',
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    res.status(500).json({ 
      status: 'Error', 
      database: 'Disconnected',
      error: error.message 
    });
  }
});

app.listen(port, () => {
  console.log(`🚀 Compliance AI Backend running on port ${port}`);
  console.log(`📊 Database: Neon PostgreSQL`);
  console.log(`🔗 Health check: http://localhost:${port}/api/health`);
});