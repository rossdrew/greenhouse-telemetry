const BASE = '/api';

export async function getStatus() {
  const res = await fetch(`${BASE}/status`);
  if (!res.ok) {
    throw new Error(`GET /status failed: ${res.status}`);
  }
  return res.json();
}

export async function setLight(on) {
  const res = await fetch(`${BASE}/light`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ on }),
  });
  const body = await res.json();
  if (!res.ok) {
    throw new Error(body.error || `POST /light failed: ${res.status}`);
  }
  return body;
}

export async function water(seconds) {
  const res = await fetch(`${BASE}/water`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ seconds }),
  });
  const body = await res.json();
  if (!res.ok) {
    throw new Error(body.error || `POST /water failed: ${res.status}`);
  }
  return body;
}
