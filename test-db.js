require('dotenv').config();
const { pool, initDB } = require('./database');

async function testConnection() {
  try {
    console.log('🔌 Testing Neon PostgreSQL connection...');
    await initDB();
    
    const result = await pool.query('SELECT version()');
    console.log('✅ Connected to Neon PostgreSQL!');
    console.log('📊 Database version:', result.rows[0].version);
    
    // Test tables - fixed version
    const tables = await pool.query(`
      SELECT table_name 
      FROM information_schema.tables 
      WHERE table_schema = 'public'
    `);
    console.log('📋 Tables created:', tables.rows.map(row => row.table_name));
    
    process.exit(0);
  } catch (error) {
    console.error('❌ Connection failed:', error);
    process.exit(1);
  }
}

testConnection();