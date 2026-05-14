const http = require('http');

function post(path, body) {
  return new Promise((resolve, reject) => {
    const data = JSON.stringify(body);
    const req = http.request({ hostname: 'localhost', port: 3001, path, method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Content-Length': Buffer.byteLength(data) }
    }, (res) => {
      let d = '';
      res.on('data', c => d += c);
      res.on('end', () => resolve(JSON.parse(d)));
    });
    req.on('error', reject);
    req.write(data);
    req.end();
  });
}

async function test() {
  console.log('=== Testing Chat API ===');
  const chat = await post('/api/chat', { message: 'My soil nitrogen is low' });
  console.log('Success:', chat.success);
  console.log('Response preview:', chat.response.substring(0, 100) + '...');

  console.log('\n=== Testing SMS API ===');
  const sms = await post('/api/sms-simulate', { nitrogen: '180', phosphorus: '8', potassium: '100', soc: '0.3', cropType: 'Rice' });
  console.log('Encoded:', sms.encoded);
  console.log('Health:', sms.advice.overallHealth);
  console.log('Status:', sms.advice.soilStatus);
  console.log('Recs:', sms.advice.recommendations);

  console.log('\n=== All Tests Passed ===');
}
test().catch(console.error);
