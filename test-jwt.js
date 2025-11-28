require('dotenv').config();
const jwt = require('jsonwebtoken');

console.log('🔍 Checking environment variables...');
console.log('JWT_SECRET exists:', process.env.JWT_SECRET ? '✅ YES' : '❌ NO');
console.log('DATABASE_URL exists:', process.env.DATABASE_URL ? '✅ YES' : '❌ NO');

if (process.env.JWT_SECRET) {
  console.log('JWT Secret length:', process.env.JWT_SECRET.length);
  
  // Test if JWT works
  try {
    const token = jwt.sign({ test: 'data' }, process.env.JWT_SECRET);
    console.log('✅ JWT Secret works - Token generated');
    
    // Verify the token
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    console.log('✅ JWT verification works');
  } catch (error) {
    console.log('❌ JWT Error:', error.message);
  }
} else {
  console.log('❌ Add JWT_SECRET to your .env file');
}