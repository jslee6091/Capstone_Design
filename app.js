const express = require('express');
const ip = require('ip');
const app = express();

app.get('/', (req, res) => {
  res.send('클라우드 과정 “6조 유민지, 유영재, 이재성” 입니다. 현재 접속한 인스턴스의 주소는 ' + ip.address() + ' 입니다.');
});

app.listen(3000, () => {
  console.log('Example app listening on port 3000!');
});

app.get('/health', (req, res) => {
  res.status(200).send();
});
