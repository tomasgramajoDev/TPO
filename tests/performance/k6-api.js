import http from 'k6/http';
import { check, sleep } from 'k6';

const baseUrl = __ENV.BASE_URL || 'http://localhost:8081';

export const options = {
  vus: Number(__ENV.K6_VUS || 50),
  duration: __ENV.K6_DURATION || '5m',
  thresholds: {
    http_req_duration: ['p(95)<500'],
    http_req_failed: ['rate<0.01'],
    checks: ['rate>0.99'],
  },
};

export function setup() {
  const response = http.post(`${baseUrl}/api/auth/login`, JSON.stringify({
    username: __ENV.TEST_USERNAME,
    password: __ENV.TEST_PASSWORD,
  }), { headers: { 'Content-Type': 'application/json' } });

  check(response, { 'login responde 200': (res) => res.status === 200 });
  const token = response.json('accessToken');
  if (!token) throw new Error('El login no devolvió accessToken');
  return { token };
}

export default function ({ token }) {
  const params = { headers: { Authorization: `Bearer ${token}` } };
  const responses = http.batch([
    ['GET', `${baseUrl}/api/public-works/dashboard/summary`, null, params],
    ['GET', `${baseUrl}/api/public-works/projects?page=0&size=20`, null, params],
    ['GET', `${baseUrl}/api/public-works/work-orders?page=0&size=5`, null, params],
  ]);

  check(responses[0], { 'dashboard 200': (res) => res.status === 200 });
  check(responses[1], { 'proyectos 200': (res) => res.status === 200 });
  check(responses[2], { 'órdenes 200': (res) => res.status === 200 });
  sleep(1);
}

export function handleSummary(data) {
  const { setup_data: _sensitiveSetupData, ...sanitizedSummary } = data;
  return {
    'k6-summary.json': JSON.stringify(sanitizedSummary, null, 2),
    stdout: `k6: p95=${data.metrics.http_req_duration.values['p(95)']} ms, errores=${data.metrics.http_req_failed.values.rate}\n`,
  };
}
