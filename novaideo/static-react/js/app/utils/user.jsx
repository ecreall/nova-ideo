export function asyncLogin(login, password, token) {
  const url = `${window.location.origin}/json_login`;
  return fetch(url, {
    method: 'post',
    headers: { Accept: 'application/json', 'Content-Type': 'application/json' },
    body: JSON.stringify({ login: login, password: password, token: token })
  }).then((response) => {
    if (response.ok) {
      return response.json();
    }
    // login failed
    return undefined;
  });
}

export function asyncLogout() {
  const url = `${window.location.origin}/json_logout`;
  return fetch(url, {
    method: 'post',
    headers: { Accept: 'application/json', 'Content-Type': 'application/json' }
  }).then((response) => {
    if (response.ok) {
      return response.json();
    }
    // logout failed
    return undefined;
  });
}